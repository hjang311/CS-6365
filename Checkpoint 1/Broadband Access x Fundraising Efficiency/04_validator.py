import os
import json
import numpy as np
import pandas as pd
import scipy.stats as stats

# Set directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")

def validate_pipeline():
    print("Starting Adversarial Quality Validation Stage...")
    
    # 1. Load results.json
    results_json_path = os.path.join(DATA_DIR, "results.json")
    if not os.path.exists(results_json_path):
        raise FileNotFoundError(f"Analysis results not found at {results_json_path}. Run 03_analysis.py first.")
    with open(results_json_path, "r") as f:
        results = json.load(f)
        
    # 2. Load merged dataset
    merged_path = os.path.join(DATA_DIR, "merged_georgia.csv")
    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Merged dataset not found at {merged_path}. Run 02_merge_pipeline.py first.")
    df = pd.read_csv(merged_path)
    
    # Clean data exactly as done in 03_analysis.py
    numeric_cols = ["F9_08_REV_CONTR_TOT", "F9_09_EXP_OTH_TOT_D", "F9_08_REV_TOT_TOT", "F9_09_EXP_TOT_TOT", "B28002_001E", "B28002_004E", "B28002_007E", "B28002_013E"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    clean_df = df[
        (df["B28002_001E"] > 0) & 
        (df["F9_08_REV_CONTR_TOT"] > 0) & 
        (df["F9_08_REV_TOT_TOT"] > 0)
    ].copy()
    
    # Assertions
    # Assertion 1: Verify sample sizes match
    assert len(clean_df) == results["n_samples"], f"Sample size mismatch: {len(clean_df)} vs {results['n_samples']}"
    
    # Assertion 2: Verify zero nulls in key analysis columns
    key_cols = ["broadband_rate", "efficiency_winsorized", "log_revenue", "ntee_category"]
    clean_df["fundraising_efficiency"] = clean_df["F9_09_EXP_OTH_TOT_D"] / clean_df["F9_08_REV_CONTR_TOT"]
    clean_df["broadband_rate"] = clean_df["B28002_004E"] / clean_df["B28002_001E"]
    clean_df["log_revenue"] = np.log(clean_df["F9_08_REV_TOT_TOT"])
    ntee_col = [c for c in clean_df.columns if c.upper() == "NTEE_CD"][0]
    clean_df["ntee_category"] = clean_df[ntee_col].astype(str).str[0].str.upper()
    clean_df["ntee_category"] = clean_df["ntee_category"].replace({np.nan: 'U', 'N': 'U', '': 'U', ' ': 'U'})
    
    p01 = clean_df["fundraising_efficiency"].quantile(0.01)
    p99 = clean_df["fundraising_efficiency"].quantile(0.99)
    clean_df["efficiency_winsorized"] = clean_df["fundraising_efficiency"].clip(lower=p01, upper=p99)
    
    for col in key_cols:
        nulls = clean_df[col].isnull().sum()
        assert nulls == 0, f"Data Contract Violation: {nulls} unexpected null values in column {col}"
        
    # Assertion 3: Verify broadband rates are valid probabilities/ratios in [0, 1]
    assert clean_df["broadband_rate"].min() >= 0.0, f"Lower bound violation: broadband_rate min is {clean_df['broadband_rate'].min()}"
    assert clean_df["broadband_rate"].max() <= 1.0, f"Upper bound violation: broadband_rate max is {clean_df['broadband_rate'].max()}"
    
    # Assertion 4: Verify fundraising efficiency is non-negative
    assert clean_df["efficiency_winsorized"].min() >= 0.0, f"Value range violation: winsorized efficiency has negative values: {clean_df['efficiency_winsorized'].min()}"
    
    # Assertion 5: Independent statistical audit (verify correlation coefficients)
    ind_r, ind_p = stats.pearsonr(clean_df["broadband_rate"], clean_df["efficiency_winsorized"])
    ind_rho, ind_rhop = stats.spearmanr(clean_df["broadband_rate"], clean_df["efficiency_winsorized"])
    
    # Compare with precision bounds (e.g. 5 decimal places)
    assert np.allclose(ind_r, results["pearson"]["r"], atol=1e-5), f"Audit failed: Pearson r mismatch: {ind_r} vs {results['pearson']['r']}"
    assert np.allclose(ind_p, results["pearson"]["p_value"], atol=1e-5), f"Audit failed: Pearson p-value mismatch: {ind_p} vs {results['pearson']['p_value']}"
    assert np.allclose(ind_rho, results["spearman"]["rho"], atol=1e-5), f"Audit failed: Spearman rho mismatch: {ind_rho} vs {results['spearman']['rho']}"
    assert np.allclose(ind_rhop, results["spearman"]["p_value"], atol=1e-5), f"Audit failed: Spearman p-value mismatch: {ind_rhop} vs {results['spearman']['p_value']}"
    
    print("=" * 60)
    print("ALL ASSERTIONS PASSED successfully.")
    print("Data Contracts checked: Zero nulls, valid ranges, correct mathematical mappings.")
    print("Statistical Audit verified: Zero discrepancies in correlation values.")
    print("ALL_PASS")
    print("=" * 60)

if __name__ == "__main__":
    validate_pipeline()
