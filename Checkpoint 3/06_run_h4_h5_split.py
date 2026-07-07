"""
06_run_h4_h5_split.py  —  Deterministic batch runner for H4 & H5 with size split

Runs both confirmatory hypotheses on cp3_modeling_frame.csv, each on the full sample
and split into mid ($500K-$2M) vs large (>=$2M) segments, then writes formal result
tables to H4/H4_results.md and H5/H5_results.md. No API keys / interactive input.

  H4: fundraising_efficiency_w ~ log_zhvi_2022               (real-estate spatial mismatch)
  H5: fundraising_efficiency_w ~ log_nonprofit_branch_density (provider-density competition)

Usage:  python 06_run_h4_h5_split.py
"""
import os
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CONTROLS = "log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income"

HYPOTHESES = {
    "H4": dict(iv="log_zhvi_2022", dv="fundraising_efficiency_w",
               title="Real-Estate Cost & Fundraising Efficiency (Spatial Mismatch)"),
    "H5": dict(iv="log_nonprofit_branch_density", dv="fundraising_efficiency_w",
               title="Social-Service Provider Density & Fundraising Efficiency"),
}


def run_ols(df, iv, dv):
    cols = [iv, dv, "log_total_revenue", "poverty_rate", "median_hh_income",
            "ntee_major", "region"]
    d = df[cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 100:
        return None
    m = smf.ols(f"{dv} ~ {iv} + {CONTROLS}", data=d).fit(cov_type="HC1")
    return m


def row(model, iv, label):
    if model is None:
        return f"| {label} | — | insufficient data | — | — | — |"
    ci = model.conf_int().loc[iv]
    return (f"| {label} | {int(model.nobs):,} | {model.params[iv]:.5f} | "
            f"{model.pvalues[iv]:.4g} | [{ci[0]:.4f}, {ci[1]:.4f}] | {model.rsquared:.4f} |")


def main():
    frame = os.path.join(DATA, "cp3_modeling_frame.csv")
    if not os.path.exists(frame):
        raise SystemExit(f"Modeling frame not found at {frame}. Run 01 & 02 first.")
    df = pd.read_csv(frame)

    for hid, h in HYPOTHESES.items():
        iv, dv, title = h["iv"], h["dv"], h["title"]
        full = run_ols(df, iv, dv)
        mid = run_ols(df[df["size_segment"] == "mid"], iv, dv)
        large = run_ols(df[df["size_segment"] == "large"], iv, dv)

        lines = [
            f"# {hid} Results — {title}",
            "",
            f"**Model:** `{dv} ~ {iv} + {CONTROLS}`  (robust HC1 errors)",
            "",
            "| Sample | n | IV coefficient (beta) | p-value | 95% CI | R-squared |",
            "|---|---|---|---|---|---|",
            row(full, iv, "Full (>=$500K)"),
            row(mid, iv, "Mid ($500K-$2M)"),
            row(large, iv, "Large (>=$2M)"),
        ]
        out = os.path.join(HERE, hid, f"{hid}_results.md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"[{hid}] wrote {out}")
        for lbl, m in (("full", full), ("mid", mid), ("large", large)):
            if m is not None:
                print(f"    {lbl:5s} n={int(m.nobs):>7,}  beta={m.params[iv]:+.4f}  "
                      f"p={m.pvalues[iv]:.3g}")


if __name__ == "__main__":
    main()
