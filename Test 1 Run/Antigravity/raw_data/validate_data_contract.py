import pandas as pd
import sys

csv_path = '/Users/hdj/Documents/CS-6365/cleaned_test_case_1.csv'
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"Error loading CSV: {e}")
    sys.exit(1)

try:
    # 1. No NULL or missing values
    assert not df['Benefits_Health'].isna().any(), "Data Contract Violation: NULL or missing values found in Benefits_Health"
    assert not df['BenefitsImpact'].isna().any(), "Data Contract Violation: NULL or missing values found in BenefitsImpact"

    # 2. Benefits_Health valid binary indicators
    valid_health = {0, 1, '0', '1', 0.0, 1.0}
    invalid_health = df[~df['Benefits_Health'].isin(valid_health)]
    assert invalid_health.empty, f"Data Contract Violation: Invalid binary indicators in Benefits_Health. Found: {invalid_health['Benefits_Health'].unique()}"

    # 3. BenefitsImpact no 'NA' strings or unmapped invalid outliers
    # The valid Likert values
    valid_impact = {1, 2, 3, 4, 5, '1', '2', '3', '4', '5', 1.0, 2.0, 3.0, 4.0, 5.0}
    
    # Also explicitly check for 'NA' or 'na' strings
    impact_as_str = df['BenefitsImpact'].astype(str).str.strip().str.upper()
    na_mask = impact_as_str == 'NA'
    assert not na_mask.any(), f"Data Contract Violation: 'NA' strings found in BenefitsImpact"
    
    invalid_impact = df[~df['BenefitsImpact'].isin(valid_impact)]
    assert invalid_impact.empty, f"Data Contract Violation: Invalid Likert values in BenefitsImpact. Found: {invalid_impact['BenefitsImpact'].unique()}"

    print("SUCCESS: Data Contract verified. All assertions passed.")

except AssertionError as e:
    print(e)
    # Also print the traceback
    import traceback
    traceback.print_exc()
    sys.exit(1)
