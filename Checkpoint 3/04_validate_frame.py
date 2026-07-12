"""
04_validate_frame.py  —  Phase 1: Modeling-Frame Data Contracts

Adversarial validation of data/cp3_modeling_frame.csv (mirrors CP2's
H2_Pipeline/05_validator.py). Run after 02_merge_pipeline.py and before any
Phase 2 loop work.

Checks:
  1. Schema        — all expected columns present
  2. Row count     — within expected band (~158K)
  3. DV integrity  — non-negative, finite, winsorized cap respected
  4. ZHVI coverage — null count in the documented band (~12K rows lack ZHVI)
  5. FDIC merge    — bank_branch_density present and populated (H2 replay enabler)
  6. H4/H5 smoke   — quick OLS reproduces baseline betas within tolerance

Exit code: 0 = all contracts pass, 1 = any failure.
No network, no API keys, no interactivity.
"""
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME_PATH = os.path.join(HERE, "data", "cp3_modeling_frame.csv")

CONTROLS = "log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income"

EXPECTED_COLUMNS = [
    "ein", "tax_year", "total_revenue", "total_expenses", "total_contributions",
    "fundraising_events_direct_expenses", "professional_fundraising_fees",
    "EIN", "ZIP5", "STATE", "NTEE_CD",
    "median_hh_income", "population", "poverty_rate",
    "social_service_count", "nonprofit_branch_density", "zhvi_2022",
    "fundraising_expense_proxy", "fundraising_efficiency",
    "log_total_revenue", "log_fundraising_efficiency",
    "log_nonprofit_branch_density", "log_zhvi_2022",
    "fundraising_efficiency_w", "region", "ntee_major", "size_segment",
]

# Columns added by the FDIC merge (02_merge_pipeline.py). Checked separately so
# the validator gives a targeted message if the frame predates that change.
FDIC_COLUMNS = ["bank_branches", "bank_branch_density", "log_bank_branch_density"]

# Bands observed from the committed Phase 1 run (July 2026).
ROW_COUNT_BAND = (140_000, 175_000)          # observed: 158,323
ZHVI_NULL_BAND = (8_000, 16_000)             # observed: ~12,227 rows lack ZHVI
EFFICIENCY_HARD_CAP = 1_000                  # cleaning recipe cap in 02

# H4/H5 baselines (same as 08_unrolled_loop.py)
H4_BASELINE_BETA = -7.91647   # log_zhvi_2022 -> fundraising_efficiency_w
H5_BASELINE_BETA = 2.11963    # log_nonprofit_branch_density -> fundraising_efficiency_w
BETA_TOL = 1e-3

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    if not ok:
        failures.append(name)


def smoke_ols(df: pd.DataFrame, iv: str, dv: str) -> float:
    """Same recipe as 08_unrolled_loop.py run_ols; returns the IV beta."""
    cols = [iv, dv, "log_total_revenue", "poverty_rate", "median_hh_income", "ntee_major", "region"]
    d = df[cols].replace([np.inf, -np.inf], np.nan).dropna()
    m = smf.ols(f"{dv} ~ {iv} + {CONTROLS}", data=d).fit(cov_type="HC1")
    return float(m.params[iv])


def main() -> int:
    print("CP3 Modeling Frame Validator — running data contracts...")
    print(f"Frame: {FRAME_PATH}\n")

    if not os.path.exists(FRAME_PATH):
        print("[FAIL] frame file exists")
        print("\ncp3_modeling_frame.csv not found. Run 02_merge_pipeline.py first.")
        return 1

    df = pd.read_csv(FRAME_PATH, low_memory=False)

    # 1. Schema
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    check("schema: expected columns present", not missing,
          f"missing: {missing}" if missing else f"{len(EXPECTED_COLUMNS)} columns")

    missing_fdic = [c for c in FDIC_COLUMNS if c not in df.columns]
    check("schema: FDIC bank-branch columns present", not missing_fdic,
          ("missing: " + str(missing_fdic) + " — re-run 02_merge_pipeline.py "
           "with fdic_branches_by_zip.csv in data/") if missing_fdic else "H2 replay enabled")

    # 2. Row count
    n = len(df)
    check("row count within expected band", ROW_COUNT_BAND[0] <= n <= ROW_COUNT_BAND[1],
          f"n={n:,}, band={ROW_COUNT_BAND[0]:,}-{ROW_COUNT_BAND[1]:,}")

    # 3. DV integrity
    dv = df["fundraising_efficiency_w"]
    check("DV: no nulls", int(dv.isna().sum()) == 0, f"nulls={int(dv.isna().sum())}")
    check("DV: all finite", bool(np.isfinite(dv.dropna()).all()))
    check("DV: non-negative", bool((dv.dropna() >= 0).all()), f"min={dv.min():.4f}")
    check("DV: raw efficiency respects cleaning cap",
          bool((df["fundraising_efficiency"].dropna() <= EFFICIENCY_HARD_CAP).all()),
          f"max={df['fundraising_efficiency'].max():.2f}, cap={EFFICIENCY_HARD_CAP}")
    # Winsorized DV should be capped at the 99th percentile of raw efficiency
    w_max, raw_p99 = float(dv.max()), float(df["fundraising_efficiency"].quantile(0.99))
    check("DV: winsorized cap ≈ raw 99th percentile", abs(w_max - raw_p99) < max(1.0, 0.01 * raw_p99),
          f"w_max={w_max:.2f}, p99={raw_p99:.2f}")

    # 4. ZHVI coverage (documented listwise-deletion driver: H4 n < H5 n)
    if "zhvi_2022" in df.columns:
        zhvi_nulls = int(df["zhvi_2022"].isna().sum())
        check("ZHVI: null count within documented band",
              ZHVI_NULL_BAND[0] <= zhvi_nulls <= ZHVI_NULL_BAND[1],
              f"nulls={zhvi_nulls:,}, band={ZHVI_NULL_BAND[0]:,}-{ZHVI_NULL_BAND[1]:,} "
              "(explains H4 n=116,587 vs H5 n=117,510)")

    # 5. FDIC merge population
    if "bank_branch_density" in df.columns:
        bbd_nonnull = int(df["bank_branch_density"].notna().sum())
        check("FDIC: bank_branch_density populated", bbd_nonnull > 0.5 * n,
              f"non-null={bbd_nonnull:,} of {n:,}")
        check("FDIC: density non-negative",
              bool((df["bank_branch_density"].dropna() >= 0).all()))

    # 6. H4/H5 smoke OLS
    try:
        h4_beta = smoke_ols(df, "log_zhvi_2022", "fundraising_efficiency_w")
        check("H4 smoke: beta matches baseline", abs(h4_beta - H4_BASELINE_BETA) < BETA_TOL,
              f"beta={h4_beta:.5f}, expected={H4_BASELINE_BETA}, tol={BETA_TOL}")
    except Exception as e:
        check("H4 smoke: beta matches baseline", False, f"OLS failed: {e}")

    try:
        h5_beta = smoke_ols(df, "log_nonprofit_branch_density", "fundraising_efficiency_w")
        check("H5 smoke: beta matches baseline", abs(h5_beta - H5_BASELINE_BETA) < BETA_TOL,
              f"beta={h5_beta:.5f}, expected={H5_BASELINE_BETA}, tol={BETA_TOL}")
    except Exception as e:
        check("H5 smoke: beta matches baseline", False, f"OLS failed: {e}")

    print()
    if failures:
        print(f"RESULT: {len(failures)} contract(s) FAILED: {failures}")
        return 1
    print("RESULT: all contracts PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
