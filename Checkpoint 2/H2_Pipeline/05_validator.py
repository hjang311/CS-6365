"""
05_validator.py — H2 pipeline, adversarial validation

Implements the Validator Agent's data contracts:
  1. Schema validation (expected shape and required columns)
  2. Null audit (known ACS-merge gaps vs unexpected missingness)
  3. Value ranges (revenue filter, DV bounds, population floor)
  4. Independent statistical recalculation on the analysis subset (n≈147,718)
  5. Size-segment counts
  6. Quartile medians and monotonicity

Statistics are always computed on the analysis subset used by 03_analysis.py:
rows with non-null bank_branch_density and fundraising_efficiency_w.
The saved modeling frame retains ACS-gap rows (null IV/controls) for auditability.

Usage: python 05_validator.py
  Exit code 0 = all contracts pass
  Exit code 1 = at least one assertion failed
"""
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "h2_modeling_frame.csv")

REQUIRED = [
    "bank_branch_density", "fundraising_efficiency_w", "log_fundraising_efficiency",
    "log_bank_branch_density", "total_revenue", "size_segment", "ntee_major",
    "region", "source_year", "poverty_rate", "median_hh_income", "population",
]

CORE_COLS = [
    "bank_branch_density", "fundraising_efficiency_w", "total_revenue",
    "poverty_rate", "median_hh_income",
]

EXPECTED_QUARTILE_MEDIANS = {
    "Q1": 31.51,
    "Q2": 27.82,
    "Q3": 26.14,
    "Q4": 26.75,
}

passed = 0
failed = 0
failures = []


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        msg = f"  FAIL  {name}" + (f": {detail}" if detail else "")
        print(msg)
        failures.append(msg.strip())


def note(msg):
    print(f"  NOTE  {msg}")


def analysis_subset(df):
    return (
        df.replace([np.inf, -np.inf], np.nan)
        .dropna(subset=["fundraising_efficiency_w"])
        .dropna(subset=["bank_branch_density"])
        .copy()
    )


def contract_1_schema(df):
    print("\n--- Contract 1: Schema & Shape ---")
    check("modeling frame exists", os.path.exists(DATA_PATH))
    check("row count in 140K-160K range", 140_000 < len(df) < 160_000,
          f"got {len(df):,}")
    for col in REQUIRED:
        check(f"column present: {col}", col in df.columns)


def contract_2_null_audit(df):
    print("\n--- Contract 2: Null Audit & Analysis Subset ---")
    nulls_by_col = df[CORE_COLS].isnull().sum()
    total_null_cells = int(nulls_by_col.sum())
    note(f"null cells in core modeling columns: {total_null_cells:,}")
    for col in CORE_COLS:
        n = int(nulls_by_col[col])
        if n:
            note(f"  {col}: {n:,} null ({100 * n / len(df):.1f}%)")

    iv_nulls = int(nulls_by_col["bank_branch_density"])
    poverty_nulls = int(nulls_by_col["poverty_rate"])
    income_nulls = int(nulls_by_col["median_hh_income"])
    fe_nulls = int(nulls_by_col["fundraising_efficiency_w"])
    rev_nulls = int(nulls_by_col["total_revenue"])

    check("DV has no nulls in saved frame", fe_nulls == 0, f"got {fe_nulls}")
    check("total_revenue has no nulls in saved frame", rev_nulls == 0, f"got {rev_nulls}")
    check("ACS-gap IV nulls in expected range (9K-12K)",
          9_000 < iv_nulls < 12_000, f"got {iv_nulls:,}")
    check("poverty_rate nulls match IV nulls (same ZIP gaps)",
          iv_nulls == poverty_nulls,
          f"IV={iv_nulls:,}, poverty={poverty_nulls:,}")
    check("median_hh_income nulls within expected range (10K-13K)",
          10_000 < income_nulls < 13_000, f"got {income_nulls:,}")
    check("total core-column null cells in expected range (30K-35K)",
          30_000 < total_null_cells < 35_000, f"got {total_null_cells:,}")

    d = analysis_subset(df)
    note(f"analysis subset n={len(d):,} (rows with non-null IV + DV)")
    check("analysis subset n in 145K-150K range", 145_000 < len(d) < 150_000,
          f"got {len(d):,}")
    check("rows dropped for ACS gaps = total - analysis n",
          len(df) - len(d) == iv_nulls,
          f"saved={len(df):,}, analysis={len(d):,}, iv_nulls={iv_nulls:,}")

    raw_rho, raw_p = stats.spearmanr(
        df["bank_branch_density"], df["fundraising_efficiency_w"]
    )
    check("raw full-frame Spearman is NaN (NaNs in IV — do not use)",
          np.isnan(raw_rho) and np.isnan(raw_p))


def contract_3_value_ranges(df):
    print("\n--- Contract 3: Value Ranges ---")
    fe = df["fundraising_efficiency_w"]
    check("revenue >= $500K", df["total_revenue"].min() >= 500_000,
          f"min={df['total_revenue'].min()}")
    check("bank_branch_density non-negative",
          (df["bank_branch_density"].dropna() >= 0).all())
    check("no infinite DV values", np.isfinite(fe).all())
    check("DV values non-negative", (fe >= 0).all(), f"min={fe.min():.2f}")
    check("DV outlier cap respected (max <= 1000)",
          fe.max() <= 1000, f"max={fe.max():.2f}")
    note(f"fundraising efficiency range: {fe.min():.2f} to {fe.max():.2f}")
    check("size_segment in {mid, large}",
          set(df["size_segment"].dropna().unique()) == {"mid", "large"},
          f"got {set(df['size_segment'].dropna().unique())}")
    check("population floor >= 1000", df["population"].dropna().min() >= 1000,
          f"min={df['population'].dropna().min()}")


def contract_4_statistics(df):
    print("\n--- Contract 4: Independent Statistical Recalculation ---")
    d = analysis_subset(df)
    note(f"computing on analysis subset n={len(d):,}")

    sr, sp = stats.spearmanr(d["bank_branch_density"], d["fundraising_efficiency_w"])
    check("Spearman rho ~ -0.0365", abs(sr - (-0.0365)) < 0.005, f"got {sr:.4f}")
    check("Spearman p < 1e-40", sp < 1e-40, f"got {sp:.2e}")

    dl = d.dropna(subset=["log_bank_branch_density", "log_fundraising_efficiency"])
    pr, pp = stats.pearsonr(dl["log_bank_branch_density"], dl["log_fundraising_efficiency"])
    check("log-log Pearson ~ -0.0195", abs(pr - (-0.0195)) < 0.005, f"got {pr:.4f}")
    check("log-log Pearson p < 1e-10", pp < 1e-10, f"got {pp:.2e}")

    have_acs = d["poverty_rate"].notna().sum() > 0.5 * len(d)
    controls = "log_total_revenue + C(ntee_major) + C(region) + C(source_year)"
    if have_acs:
        controls += " + poverty_rate + median_hh_income"
    formula = f"fundraising_efficiency_w ~ bank_branch_density + {controls}"
    m = smf.ols(formula, data=d).fit(cov_type="HC1")
    check("OLS IV p < 0.05", m.pvalues["bank_branch_density"] < 0.05,
          f"p={m.pvalues['bank_branch_density']:.4g}")
    check("OLS IV coefficient negative", m.params["bank_branch_density"] < 0,
          f"beta={m.params['bank_branch_density']:.5f}")
    check("OLS IV beta ~ -0.115", abs(m.params["bank_branch_density"] - (-0.11453)) < 0.01,
          f"got {m.params['bank_branch_density']:.5f}")


def contract_5_size_segments(df):
    print("\n--- Contract 5: Size Segment Counts ---")
    d = analysis_subset(df)
    mid_n = (d["size_segment"] == "mid").sum()
    large_n = (d["size_segment"] == "large").sum()
    check("mid-size count 60K-80K", 60_000 < mid_n < 80_000, f"got {mid_n:,}")
    check("large count 70K-90K", 70_000 < large_n < 90_000, f"got {large_n:,}")
    check("segments sum to analysis total", abs(mid_n + large_n - len(d)) < 100,
          f"mid+large={mid_n + large_n:,}, total={len(d):,}")


def contract_6_quartile_medians(df):
    print("\n--- Contract 6: Quartile Medians & Monotonicity ---")
    d = analysis_subset(df)
    d["iv_q"] = pd.qcut(
        d["bank_branch_density"], 4,
        labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop",
    )
    medians = d.groupby("iv_q", observed=True)["fundraising_efficiency_w"].median()

    for q, expected in EXPECTED_QUARTILE_MEDIANS.items():
        got = medians[q]
        check(f"{q} median ~ {expected:.2f}",
              abs(got - expected) < 0.05, f"got {got:.2f}")

    check("Q1 median > Q3 median (monotonic trend)",
          medians["Q1"] > medians["Q3"],
          f"Q1={medians['Q1']:.2f} vs Q3={medians['Q3']:.2f}")


def main():
    print("H2 Pipeline Validator — running data contracts...")
    df = pd.read_csv(DATA_PATH)

    contract_1_schema(df)
    contract_2_null_audit(df)
    contract_3_value_ranges(df)
    contract_4_statistics(df)
    contract_5_size_segments(df)
    contract_6_quartile_medians(df)

    print()
    if failed == 0:
        print(f"✅ ALL 6 CONTRACTS PASSED ({passed} assertions)")
        sys.exit(0)
    print(f"❌ VALIDATION FAILED: {failed} assertion(s) failed")
    for f in failures:
        print(f"   {f}")
    sys.exit(1)


if __name__ == "__main__":
    main()
