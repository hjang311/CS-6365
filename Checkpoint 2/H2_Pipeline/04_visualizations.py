"""
04_visualizations.py — H2 pipeline, publication-quality plots

Reads the merged modeling frame and generates all checkpoint 2 visualizations.
Run after 03_analysis.py.

Usage: python 04_visualizations.py
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from scipy import stats

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PLOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
os.makedirs(PLOTS, exist_ok=True)

DPI = 300
IV = "bank_branch_density"
LOG_IV = "log_bank_branch_density"
DV = "fundraising_efficiency_w"
LOG_DV = "log_fundraising_efficiency"


def load_data():
    df = pd.read_csv(os.path.join(DATA, "h2_modeling_frame.csv"))
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=[DV])
    if df[IV].notna().sum() > 0.5 * len(df):
        iv = IV
    else:
        iv = "bank_branch_density_raw"
    d = df.dropna(subset=[iv]).copy()
    return d, iv


def run_ols(df, iv, label):
    have_acs = df["poverty_rate"].notna().sum() > 0.5 * len(df)
    controls = "log_total_revenue + C(ntee_major) + C(region) + C(source_year)"
    if have_acs:
        controls += " + poverty_rate + median_hh_income"
    formula = f"{DV} ~ {iv} + {controls}"
    return smf.ols(formula, data=df).fit(cov_type="HC1")


def setup_style():
    sns.set_theme(style="whitegrid", font="serif")
    plt.rcParams.update({
        "font.family": "serif",
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
    })


def plot_quartile_bar_chart(d, iv):
    labels = ["Q1\n(Lowest)", "Q2", "Q3", "Q4\n(Highest)"]
    dq = d.copy()
    dq["iv_q"] = pd.qcut(dq[iv], 4, labels=labels, duplicates="drop")
    agg = dq.groupby("iv_q", observed=True)[DV].agg(["mean", "median"])

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(agg))
    width = 0.35
    ax.bar(x - width / 2, agg["mean"], width, label="Mean", color="#5C6BC0", alpha=0.85)
    bars = ax.bar(x + width / 2, agg["median"], width, label="Median", color="#26A69A", alpha=0.85)
    for bar, val in zip(bars, agg["median"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.2f}", ha="center", va="bottom", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(agg.index)
    ax.set_xlabel("Bank-Branch Density Quartile")
    ax.set_ylabel("Fundraising Efficiency (winsorized)")
    ax.set_title("Fundraising Efficiency by Bank-Branch Density Quartile")
    ax.legend(loc="upper right")
    ax.text(
        0.02, 0.98,
        "Spearman ρ = -0.037, p < 10⁻⁴⁴\nn = 147,718",
        transform=ax.transAxes, va="top", ha="left",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "quartile_bar_chart.png"))
    plt.close(fig)


def plot_log_log_scatter(d):
    dl = d.dropna(subset=[LOG_IV, LOG_DV])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=dl, x=LOG_IV, y=LOG_DV, ax=ax,
        scatter_kws={"alpha": 0.02, "s": 1},
        line_kws={"color": "red", "linewidth": 2},
        ci=95,
    )
    ax.set_xlabel("ln(1 + Bank Branches per 10K Residents)")
    ax.set_ylabel("ln(Fundraising Efficiency)")
    ax.set_title("Log-Log Relationship: Bank-Branch Density vs Fundraising Efficiency")
    ax.text(
        0.02, 0.98,
        "Pearson r = -0.020 (p < 10⁻¹⁴)\nOLS β = -0.115 (p = 0.002)",
        transform=ax.transAxes, va="top", ha="left",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "log_log_scatter.png"))
    plt.close(fig)


def plot_size_comparison_coefficients(d, iv):
    models = [
        ("Full Sample (n=147,718)", run_ols(d, iv, "full"), "#2196F3"),
        ("Mid-Size $500K–$2M (n=69,683)", run_ols(d[d["size_segment"] == "mid"], iv, "mid"), "#FF5722"),
        ("Large ≥$2M (n=78,034)", run_ols(d[d["size_segment"] == "large"], iv, "large"), "#4CAF50"),
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(models))
    colors = [m[2] for m in models]

    for i, (label, model, color) in enumerate(models):
        beta = model.params[iv]
        ci_low, ci_high = model.conf_int().loc[iv]
        pval = model.pvalues[iv]
        ax.errorbar(beta, i, xerr=[[beta - ci_low], [ci_high - beta]],
                    fmt="o", color=color, capsize=5, markersize=8, linewidth=2)
        ax.text(ci_high + 0.01, i, f"β = {beta:.3f}, p = {pval:.4g}",
                va="center", fontsize=9)

    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([m[0] for m in models])
    ax.set_xlabel("OLS Coefficient (bank_branch_density)")
    ax.set_title("OLS Coefficients: Bank-Branch Density Effect by Organization Size")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "size_comparison_coefficients.png"))
    plt.close(fig)


def plot_distribution_diagnostics(d):
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    panels = [
        (axes[0, 0], IV, "Bank-Branch Density (raw)"),
        (axes[0, 1], LOG_IV, "ln(1 + Bank-Branch Density)"),
        (axes[1, 0], DV, "Fundraising Efficiency (winsorized)"),
        (axes[1, 1], LOG_DV, "ln(Fundraising Efficiency)"),
    ]
    for ax, col, title in panels:
        series = d[col].dropna()
        skew = stats.skew(series)
        ax.hist(series, bins=100, color="#42A5F5", edgecolor="white", alpha=0.85)
        ax.set_title(title)
        ann = f"Skewness = {skew:.2f}"
        if col in (IV, DV):
            ann += f"\nMedian = {series.median():.2f}"
        ax.text(0.97, 0.97, ann, transform=ax.transAxes, va="top", ha="right",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.9), fontsize=9)

    fig.suptitle("Distribution Diagnostics: Raw vs Log-Transformed Variables", y=1.01)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "distribution_diagnostics.png"), bbox_inches="tight")
    plt.close(fig)


def plot_correlation_heatmap(d):
    cols = [
        IV, DV, "total_revenue", "poverty_rate", "median_hh_income", "population",
    ]
    sub = d[cols].dropna()
    corr = sub.corr(method="spearman")

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".3f", cmap="RdBu_r", center=0,
                square=True, linewidths=0.5, ax=ax)
    ax.set_title("Spearman Rank Correlation Matrix — Key Variables")
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "correlation_heatmap.png"))
    plt.close(fig)


def plot_residual_diagnostics(d, iv):
    model = run_ols(d, iv, "residuals")
    residuals = model.resid
    fitted = model.fittedvalues

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    stats.probplot(residuals, dist="norm", plot=axes[0])
    axes[0].set_title("Q-Q Plot of OLS Residuals")
    axes[0].get_lines()[0].set_markersize(2)
    axes[0].get_lines()[0].set_alpha(0.3)

    axes[1].scatter(fitted, residuals, alpha=0.02, s=1, color="#1976D2")
    axes[1].axhline(0, color="red", linestyle="--", linewidth=1)
    axes[1].set_xlabel("Fitted Values")
    axes[1].set_ylabel("Residuals")
    axes[1].set_title("Residuals vs Fitted Values")

    fig.suptitle("OLS Model 2 Residual Diagnostics")
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS, "residual_diagnostics.png"))
    plt.close(fig)


def main():
    setup_style()
    d, iv = load_data()
    print(f"[viz] loaded n={len(d):,}, IV={iv}")

    plot_quartile_bar_chart(d, iv)
    print("[viz] saved quartile_bar_chart.png")

    plot_log_log_scatter(d)
    print("[viz] saved log_log_scatter.png")

    plot_size_comparison_coefficients(d, iv)
    print("[viz] saved size_comparison_coefficients.png")

    plot_distribution_diagnostics(d)
    print("[viz] saved distribution_diagnostics.png")

    plot_correlation_heatmap(d)
    print("[viz] saved correlation_heatmap.png")

    plot_residual_diagnostics(d, iv)
    print("[viz] saved residual_diagnostics.png")

    print(f"[viz] all plots written to {PLOTS}")


if __name__ == "__main__":
    main()
