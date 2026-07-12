"""
02_merge_pipeline.py  —  Phase 1: Modular Data Merging (manual pipeline)

Phase 1 in the professor's 3-phase model = manual acquisition + merging + hand-run
hypothesis tests. (Phase 2 = the unrolled loop in 08_unrolled_loop.py; Phase 3 = the
future agentic loop.)

Joins NCCS Core subset with IRS BMF, FDIC branch counts, Census controls,
and Zillow housing cost data at the ZIP level.
Calculates key IVs:
  - nonprofit_branch_density (social service nonprofits per 10k residents)
  - bank_branch_density (FDIC bank branches per 10k residents — CP2 H2 replay)
Outputs: data/cp3_modeling_frame.csv
"""
import os
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Social Service NTEE Prefixes (Soup Kitchens, Food Banks, Homeless Shelters, etc.)
SOCIAL_SERVICE_PREFIXES = ("K30", "K31", "K35", "L40", "L41", "P43")

def load_data():
    core_path = os.path.join(DATA, "core_subset.csv")
    bmf_path = os.path.join(DATA, "irs_bmf.csv")
    
    if not os.path.exists(core_path) or not os.path.exists(bmf_path):
        raise SystemExit("Required source files core_subset.csv and irs_bmf.csv not found in data/.")
        
    core = pd.read_csv(core_path)
    bmf = pd.read_csv(bmf_path, dtype=str)
    
    core["EIN"] = core["ein"].astype(str).str.zfill(9)
    bmf = bmf.drop_duplicates("EIN")
    
    # Inner merge to attach ZIP5, STATE, NTEE_CD to NCCS financials
    df = core.merge(bmf[["EIN", "ZIP5", "STATE", "NTEE_CD"]], on="EIN", how="inner")
    print(
        f"[Merge] Joined Core with BMF: {len(df):,} pre-clean "
        "organization-year rows (2018-2022 pooled)"
    )
    return df, bmf

def calculate_nonprofit_density(bmf, acs):
    """Calculate the ZIP-level density of social service nonprofits per 10k residents."""
    print("[IV Calculation] Computing nonprofit branch density per ZIP...")
    
    # Filter BMF for social service NTEE codes
    bmf_social = bmf[bmf["NTEE_CD"].fillna("").str.startswith(SOCIAL_SERVICE_PREFIXES)].copy()
    print(f"  found {len(bmf_social):,} registered social service nonprofits nationally")
    
    # Count by ZIP
    social_counts = bmf_social.groupby("ZIP5").size().reset_index(name="social_service_count")
    
    # Merge with ACS population data
    density_df = acs[["ZIP5", "population"]].merge(social_counts, on="ZIP5", how="left")
    density_df["social_service_count"] = density_df["social_service_count"].fillna(0)
    
    # nonprofit_branch_density = count per 10k residents
    density_df["nonprofit_branch_density"] = np.where(
        density_df["population"] > 0,
        (density_df["social_service_count"] / density_df["population"]) * 10_000,
        np.nan
    )
    return density_df[["ZIP5", "social_service_count", "nonprofit_branch_density"]]

def main():
    df, bmf = load_data()
    
    # --- Load Census ACS ---
    acs_path = os.path.join(DATA, "census_acs_by_zip.csv")
    if os.path.exists(acs_path):
        acs = pd.read_csv(acs_path, dtype={"ZIP5": str})
        for c in ("median_hh_income", "population", "poverty_rate"):
            acs[c] = pd.to_numeric(acs[c], errors="coerce")
        acs.loc[acs["median_hh_income"] < 0, "median_hh_income"] = np.nan
        
        # Merge ACS controls directly to org level
        df = df.merge(acs[["ZIP5", "median_hh_income", "population", "poverty_rate"]], on="ZIP5", how="left")
    else:
        print("[Merge] WARNING: census_acs_by_zip.csv not found!")
        df["population"] = np.nan
        df["median_hh_income"] = np.nan
        df["poverty_rate"] = np.nan
        acs = pd.DataFrame(columns=["ZIP5", "population"])
        
    # --- Calculate and merge nonprofit branch density ---
    density_df = calculate_nonprofit_density(bmf, acs)
    df = df.merge(density_df, on="ZIP5", how="left")

    # --- Merge FDIC bank branch counts (enables CP2 H2 replay in Phase 2 loop) ---
    fdic_path = os.path.join(DATA, "fdic_branches_by_zip.csv")
    if os.path.exists(fdic_path):
        fdic = pd.read_csv(fdic_path, dtype={"ZIP5": str})
        # One row per ZIP; left join preserves row count and existing columns.
        df = df.merge(fdic[["ZIP5", "bank_branches"]], on="ZIP5", how="left")
        df["bank_branches"] = df["bank_branches"].fillna(0)
        # Same recipe as CP2: branches per 10k residents (NaN where population unknown)
        df["bank_branch_density"] = np.where(
            df["population"] > 0,
            df["bank_branches"] / df["population"] * 10_000,
            np.nan,
        )
        print(
            "[Merge] Merged FDIC bank branches; density computed for "
            f"{df['bank_branch_density'].notna().sum():,} pre-clean rows"
        )
    else:
        print("[Merge] WARNING: fdic_branches_by_zip.csv not found — "
              "bank_branch_density will be absent (H2 replay will skip in Phase 2 loop)")

    
    # --- Merge Zillow Housing Cost Data ---
    zillow_path = os.path.join(DATA, "zillow_zhvi_2022.csv")
    if os.path.exists(zillow_path):
        zillow = pd.read_csv(zillow_path, dtype={"ZIP5": str})
        zillow["zhvi_2022"] = pd.to_numeric(zillow["zhvi_2022"], errors="coerce")
        df = df.merge(zillow[["ZIP5", "zhvi_2022"]], on="ZIP5", how="left")
        print(
            "[Merge] Merged Zillow housing value index to "
            f"{df['zhvi_2022'].notna().sum():,} pre-clean rows"
        )
    else:
        print("[Merge] WARNING: zillow_zhvi_2022.csv not found!")
        df["zhvi_2022"] = np.nan

    print(
        f"[Clean] Starting financial/geographic cleaning with {len(df):,} "
        "pre-clean organization-year rows; the final analysis frame will be smaller."
    )

    # --- Financial Data Clean & DV Calculation ---
    for c in ["total_revenue", "total_contributions",
              "professional_fundraising_fees", "fundraising_events_direct_expenses"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        
    df["fundraising_expense_proxy"] = (
        df["professional_fundraising_fees"].fillna(0)
        + df["fundraising_events_direct_expenses"].fillna(0)
    )

    # --- Cleaning Recipe ---
    FUND_SPEND_FLOOR = 5_000
    EFFICIENCY_CAP = 1_000
    MIN_ZIP_POP = 1_000

    def drop(mask, reason):
        nonlocal df
        n = (~mask).sum()
        df = df[mask].copy()
        print(f"  [clean] dropped {n:,} rows — {reason}  (remaining {len(df):,})")

    drop((df["total_contributions"] > 0) & (df["fundraising_expense_proxy"] > 0),
         "invalid contributions/fundraising spend <= 0")
    drop(df["fundraising_expense_proxy"] >= FUND_SPEND_FLOOR,
         f"fundraising spend < ${FUND_SPEND_FLOOR:,}")
         
    df["fundraising_efficiency"] = df["total_contributions"] / df["fundraising_expense_proxy"]
    
    drop(df["fundraising_efficiency"] <= EFFICIENCY_CAP,
         f"efficiency cap > {EFFICIENCY_CAP}")
         
    if "population" in df.columns and df["population"].notna().any():
        drop(~(df["population"] < MIN_ZIP_POP),
             f"ZIP population < {MIN_ZIP_POP:,}")

    # --- Transformations (Logs) ---
    df["log_total_revenue"] = np.log(df["total_revenue"].clip(lower=1))
    df["log_fundraising_efficiency"] = np.log(df["fundraising_efficiency"].clip(lower=1e-9))
    df["log_nonprofit_branch_density"] = np.log1p(df["nonprofit_branch_density"].fillna(0).clip(lower=0))
    df["log_zhvi_2022"] = np.log(df["zhvi_2022"].clip(lower=1))
    if "bank_branch_density" in df.columns:
        df["log_bank_branch_density"] = np.log1p(df["bank_branch_density"].clip(lower=0))

    # Winsorized Level DV for OLS robustness
    cap = df["fundraising_efficiency"].quantile(0.99)
    df["fundraising_efficiency_w"] = df["fundraising_efficiency"].clip(upper=cap)

    # Region and industry category mappings
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

    df["region"] = df["STATE"].map(census_region)
    df["ntee_major"] = df["NTEE_CD"].astype(str).str.slice(0, 1)

    # Size segment for the small-vs-large comparison ($500K-$2M vs >=$2M)
    df["size_segment"] = pd.cut(df["total_revenue"],
                                bins=[500_000, 2_000_000, float("inf")],
                                labels=["mid", "large"])

    out = os.path.join(DATA, "cp3_modeling_frame.csv")
    df.to_csv(out, index=False)
    print(f"[Merge] Saved final CP3 modeling frame with {len(df):,} rows to {out}")

if __name__ == "__main__":
    main()
