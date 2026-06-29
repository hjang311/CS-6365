"""
02_merge_pipeline.py  —  H2 pipeline, merge + feature engineering

Joins the four acquired sources on EIN / ZIP and builds the modeling frame:

  IV  : bank_branch_density   = bank_branches per 10k residents in the org's ZIP
        (lower density  ->  proxy for greater fintech reliance)
  DV  : fundraising_efficiency = total_contributions / fundraising_expense_proxy
        fundraising_expense_proxy = professional_fundraising_fees
                                    + fundraising_events_direct_expenses
        (NOTE: NCCS CORE has no single Part IX Line 25 col-D total; this proxy is
         documented as a limitation and can be upgraded from 990 e-file XML later.)
  Controls: log(total_revenue), NTEE major group, STATE/region, year,
            poverty_rate, median_hh_income
  Segments: mid ($500K-$2M) vs large (>= $2M)

Output: data/h2_modeling_frame.csv
"""
import os
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load_core():
    parts = [pd.read_csv(os.path.join(DATA, f))
             for f in os.listdir(DATA) if f.startswith("core_") and f.endswith("_filtered.csv")]
    if not parts:
        raise SystemExit("No core_*_filtered.csv found — run 01_acquire_data.py first.")
    df = pd.concat(parts, ignore_index=True)
    df["EIN"] = df["ein"].astype(str).str.replace(r"\D", "", regex=True).str.zfill(9)
    return df


def census_region(state):
    NE = set("CT ME MA NH RI VT NJ NY PA".split())
    MW = set("IL IN MI OH WI IA KS MN MO NE ND SD".split())
    S = set("DE FL GA MD NC SC VA DC WV AL KY MS TN AR LA OK TX".split())
    W = set("AZ CO ID MT NV NM UT WY AK CA HI OR WA".split())
    if state in NE: return "Northeast"
    if state in MW: return "Midwest"
    if state in S:  return "South"
    if state in W:  return "West"
    return "Other"


def main():
    core = load_core()
    bmf = pd.read_csv(os.path.join(DATA, "irs_bmf.csv"), dtype=str)
    fdic = pd.read_csv(os.path.join(DATA, "fdic_branches_by_zip.csv"), dtype={"ZIP5": str})

    # --- merge org financials with geography/NTEE (BMF) ---
    bmf = bmf.drop_duplicates("EIN")
    df = core.merge(bmf[["EIN", "ZIP5", "STATE", "NTEE_CD"]], on="EIN", how="inner")

    # --- attach branch counts + ACS controls by ZIP ---
    df = df.merge(fdic[["ZIP5", "bank_branches"]], on="ZIP5", how="left")
    df["bank_branches"] = df["bank_branches"].fillna(0)

    acs_path = os.path.join(DATA, "census_acs_by_zip.csv")
    if os.path.exists(acs_path):
        acs = pd.read_csv(acs_path, dtype={"ZIP5": str})
        for c in ("median_hh_income", "population", "poverty_rate"):
            acs[c] = pd.to_numeric(acs[c], errors="coerce")
        acs.loc[acs["median_hh_income"] < 0, "median_hh_income"] = np.nan  # ACS uses -666666666 for N/A
        df = df.merge(acs[["ZIP5", "median_hh_income", "population", "poverty_rate"]],
                      on="ZIP5", how="left")
    else:
        print("[merge] census_acs_by_zip.csv missing — IV will use raw branch count, "
              "controls poverty/income will be NaN (set CENSUS_API_KEY and re-run 01).")
        df["population"] = np.nan
        df["median_hh_income"] = np.nan
        df["poverty_rate"] = np.nan

    # --- IV: branch density per 10k residents (fallback to raw count if no pop) ---
    df["bank_branch_density"] = np.where(
        df["population"] > 0,
        df["bank_branches"] / df["population"] * 10_000,
        np.nan)
    df["bank_branch_density_raw"] = df["bank_branches"]

    # --- DV: fundraising efficiency (contributions / fundraising-cost proxy) ---
    for c in ["total_revenue", "total_contributions",
              "professional_fundraising_fees", "fundraising_events_direct_expenses"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["fundraising_expense_proxy"] = (
        df["professional_fundraising_fees"].fillna(0)
        + df["fundraising_events_direct_expenses"].fillna(0))

    # ------------------------------------------------------------------
    # DV CLEANING RECIPE — removes the artifacts that make the ratio (and
    # therefore Pearson) meaningless. Each step prints its drop count so the
    # cleaning is fully auditable in the findings write-up.
    # ------------------------------------------------------------------
    FUND_SPEND_FLOOR = 5_000      # min plausible fundraising spend ($)
    EFFICIENCY_CAP   = 1_000      # >$1,000 raised per $1 spent = reporting artifact
    MIN_ZIP_POP      = 1_000      # drop tiny ZCTAs that inflate per-capita density

    def drop(mask, reason):
        nonlocal df
        n = (~mask).sum()
        df = df[mask].copy()
        print(f"[clean] dropped {n:,} rows — {reason}  (remaining {len(df):,})")

    # Step 1: validity — no negative/zero contributions or fundraising spend
    #         (these are amended/error returns, not real performance)
    drop((df["total_contributions"] > 0) & (df["fundraising_expense_proxy"] > 0),
         "invalid: contributions<=0 or fundraising spend<=0")

    # Step 2: sane denominator floor — kills ratio blow-ups from non-reporters
    drop(df["fundraising_expense_proxy"] >= FUND_SPEND_FLOOR,
         f"fundraising spend < ${FUND_SPEND_FLOOR:,}")

    df["fundraising_efficiency"] = df["total_contributions"] / df["fundraising_expense_proxy"]

    # Step 3: domain cap — implausible efficiency is a data artifact, not skill
    drop(df["fundraising_efficiency"] <= EFFICIENCY_CAP,
         f"efficiency > {EFFICIENCY_CAP} (>${EFFICIENCY_CAP} raised per $1)")

    # Step 5 (IV side): drop tiny-population ZIPs that inflate per-capita density
    if "population" in df.columns and df["population"].notna().any():
        drop(~(df["population"] < MIN_ZIP_POP),
             f"ZIP population < {MIN_ZIP_POP:,}")

    # --- controls / segments ---
    df = df[df["total_revenue"] >= 500_000].copy()
    df["log_total_revenue"] = np.log(df["total_revenue"].clip(lower=1))
    df["ntee_major"] = df["NTEE_CD"].astype(str).str.slice(0, 1)
    df["region"] = df["STATE"].map(census_region)
    df["size_segment"] = pd.cut(df["total_revenue"],
                                bins=[500_000, 2_000_000, float("inf")],
                                labels=["mid", "large"])

    # Step 4: analyze on logs — makes Pearson's linearity assumption valid on
    # these log-normal variables (this is the step that converges Pearson->Spearman)
    df["log_fundraising_efficiency"] = np.log(df["fundraising_efficiency"].clip(lower=1e-9))
    for cand in ("bank_branch_density", "bank_branch_density_raw"):
        if cand in df.columns:
            df[f"log_{cand}"] = np.log1p(df[cand].clip(lower=0))

    # keep a winsorized level DV too (for level-scale OLS / robustness)
    cap = df["fundraising_efficiency"].quantile(0.99)
    df["fundraising_efficiency_w"] = df["fundraising_efficiency"].clip(upper=cap)

    out = os.path.join(DATA, "h2_modeling_frame.csv")
    df.to_csv(out, index=False)
    print(f"[merge] final modeling frame: {len(df):,} orgs -> {out}")
    print(df[["size_segment"]].value_counts())


if __name__ == "__main__":
    main()
