import os
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Set directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")

def analyze_data():
    print("Starting Statistical Analysis Stage...")
    
    # Load merged dataset
    merged_path = os.path.join(DATA_DIR, "merged_georgia.csv")
    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Merged dataset not found at {merged_path}. Run 02_merge_pipeline.py first.")
    df = pd.read_csv(merged_path)
    print(f"Loaded merged Georgia dataset: {df.shape[0]} rows")
    
    # Ensure numeric columns
    numeric_cols = ["F9_08_REV_CONTR_TOT", "F9_09_EXP_OTH_TOT_D", "F9_08_REV_TOT_TOT", "F9_09_EXP_TOT_TOT", "B28002_001E", "B28002_004E", "B28002_007E", "B28002_013E"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Exclude invalid data & run listwise deletion
    # 1. Total households must be > 0
    # 2. Total contributions must be > 0 (to compute efficiency ratio)
    # 3. Total revenue must be > 0 (for log control)
    clean_df = df[
        (df["B28002_001E"] > 0) & 
        (df["F9_08_REV_CONTR_TOT"] > 0) & 
        (df["F9_08_REV_TOT_TOT"] > 0)
    ].copy()
    
    print(f"Rows remaining after listwise deletion of non-positives: {len(clean_df)} (Dropped {len(df) - len(clean_df)} rows)")
    
    if len(clean_df) < 30:
        print("Warning: Sample size too small for statistical significance testing.")
        
    # Construct Variables
    # Dependent Variable: Fundraising Efficiency (Fundraising Expenses / Contributions)
    clean_df["fundraising_efficiency"] = clean_df["F9_09_EXP_OTH_TOT_D"] / clean_df["F9_08_REV_CONTR_TOT"]
    
    # Independent Variables: Broadband rates
    clean_df["broadband_rate"] = clean_df["B28002_004E"] / clean_df["B28002_001E"]
    clean_df["cable_fiber_dsl_rate"] = clean_df["B28002_007E"] / clean_df["B28002_001E"]
    clean_df["no_internet_rate"] = clean_df["B28002_013E"] / clean_df["B28002_001E"]
    
    # Control Variables
    clean_df["log_revenue"] = np.log(clean_df["F9_08_REV_TOT_TOT"])
    
    # Extract NTEE broad category (first letter of NTEE code from BMF)
    ntee_col = [c for c in clean_df.columns if c.upper() == "NTEE_CD"][0]
    clean_df["ntee_category"] = clean_df[ntee_col].astype(str).str[0].str.upper()
    # Replace empty/nan with 'U' (Unknown)
    clean_df["ntee_category"] = clean_df["ntee_category"].replace({np.nan: 'U', 'N': 'U', '': 'U', ' ': 'U'})
    
    # Winsorize Fundraising Efficiency to limit impact of extreme outliers (1st and 99th percentiles)
    p01 = clean_df["fundraising_efficiency"].quantile(0.01)
    p99 = clean_df["fundraising_efficiency"].quantile(0.99)
    clean_df["efficiency_winsorized"] = clean_df["fundraising_efficiency"].clip(lower=p01, upper=p99)
    print(f"Winsorized fundraising efficiency. 1st pct: {p01:.4f}, 99th pct: {p99:.4f}")
    
    # Pearson and Spearman Correlation between Broadband and Efficiency
    # High broadband should correlate with LOWER efficiency ratio (lower ratio = more efficient)
    pearson_r, pearson_p = stats.pearsonr(clean_df["broadband_rate"], clean_df["efficiency_winsorized"])
    spearman_r, spearman_p = stats.spearmanr(clean_df["broadband_rate"], clean_df["efficiency_winsorized"])
    
    print(f"Pearson Correlation (r): {pearson_r:.4f} (p-value: {pearson_p:.2e})")
    print(f"Spearman Correlation (rho): {spearman_r:.4f} (p-value: {spearman_p:.2e})")
    
    # Define OLS regression with controls
    # Create dummy variables for NTEE Categories to control for organization sector
    dummy_df = pd.get_dummies(clean_df["ntee_category"], prefix="ntee", drop_first=True)
    # Convert dummy columns to floats for statsmodels
    dummy_df = dummy_df.astype(float)
    
    X = clean_df[["broadband_rate", "log_revenue"]].join(dummy_df)
    X = sm.add_constant(X)
    y = clean_df["efficiency_winsorized"]
    
    model = sm.OLS(y, X)
    results = model.fit()
    
    print("\nOLS Regression Results:")
    print(results.summary().tables[1])
    
    # Generate Plots
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Plot 1: Scatter plot with regression line
    plt.figure(figsize=(10, 6))
    plt.scatter(clean_df["broadband_rate"] * 100, clean_df["efficiency_winsorized"], alpha=0.4, color="royalblue", label="Nonprofits")
    
    # Plot regression trendline
    ols_x = np.linspace(clean_df["broadband_rate"].min(), clean_df["broadband_rate"].max(), 100)
    ols_y = results.params["const"] + results.params["broadband_rate"] * ols_x
    plt.plot(ols_x * 100, ols_y, color="crimson", linewidth=2, label="OLS Trendline")
    
    plt.title("Broadband Access Rate vs. Winsorized Nonprofit Fundraising Cost Ratio (Georgia 2022)")
    plt.xlabel("Community Broadband Subscription Rate (%)")
    plt.ylabel("Fundraising Cost Ratio (Expenses / Contributions)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plot_path1 = os.path.join(DATA_DIR, "broadband_vs_efficiency.png")
    plt.savefig(plot_path1, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved scatter plot to {plot_path1}")
    
    # Plot 2: Quintile Bar Chart
    clean_df["broadband_quintile"] = pd.qcut(clean_df["broadband_rate"], 5, labels=["Q1 (Lowest)", "Q2", "Q3", "Q4", "Q5 (Highest)"])
    quintile_mean = clean_df.groupby("broadband_quintile", observed=False)["efficiency_winsorized"].mean()
    
    plt.figure(figsize=(8, 5))
    quintile_mean.plot(kind="bar", color="teal", alpha=0.85)
    plt.title("Average Fundraising Cost Ratio by Community Broadband Access Quintiles")
    plt.xlabel("Broadband Subscription Quintiles")
    plt.ylabel("Mean Fundraising Cost Ratio")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plot_path2 = os.path.join(DATA_DIR, "quintile_efficiency.png")
    plt.savefig(plot_path2, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved quintile bar chart to {plot_path2}")
    
    # Save results details to results.json
    results_dict = {
        "n_samples": int(len(clean_df)),
        "pearson": {
            "r": float(pearson_r),
            "p_value": float(pearson_p)
        },
        "spearman": {
            "rho": float(spearman_r),
            "p_value": float(spearman_p)
        },
        "ols": {
            "r2": float(results.rsquared),
            "r2_adj": float(results.rsquared_adj),
            "broadband_rate_coef": float(results.params["broadband_rate"]),
            "broadband_rate_pvalue": float(results.pvalues["broadband_rate"]),
            "log_revenue_coef": float(results.params["log_revenue"]),
            "log_revenue_pvalue": float(results.pvalues["log_revenue"])
        }
    }
    
    results_json_path = os.path.join(DATA_DIR, "results.json")
    with open(results_json_path, "w") as f:
        json.dump(results_dict, f, indent=4)
    print(f"Saved results summary to {results_json_path}")
    
if __name__ == "__main__":
    analyze_data()
