import pandas as pd
import json
import scipy.stats as stats
import sys

def main():
    csv_path = '/Users/hdj/Documents/CS-6365/[Test 3 Run]/cleaned_subset_analysis.csv'
    json_path = '/Users/hdj/Documents/CS-6365/[Test 3 Run]/top_5_correlations.json'

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        sys.exit(1)
        
    with open(json_path, 'r') as f:
        correlations = json.load(f)

    # Contract 1: No nulls in the dataset
    total_nulls = df.isnull().sum().sum()
    assert total_nulls == 0, f"Data contract violated: found {total_nulls} unexpected nulls."

    # Contract 2: Correct types
    for corr in correlations:
        col1 = corr['var1']
        col2 = corr['var2']
        assert pd.api.types.is_numeric_dtype(df[col1]), f"Data contract violated: {col1} is not numeric"
        assert pd.api.types.is_numeric_dtype(df[col2]), f"Data contract violated: {col2} is not numeric"

    # Contract 3: p-value < 0.05 for top 5 correlations
    all_passed = True
    for corr in correlations:
        col1 = corr['var1']
        col2 = corr['var2']
        
        # independently calculate pearson r and p-value
        r, p = stats.pearsonr(df[col1], df[col2])
        if p >= 0.05:
            print(f"FAILED: {col1} & {col2}: p-value = {p:.4e} (r = {r:.4f})")
            all_passed = False
        else:
            print(f"Passed: {col1} & {col2}: p-value = {p:.4e} < 0.05 (r = {r:.4f})")

    assert all_passed, "One or more p-value assertions failed."
    print("ALL_PASS")

if __name__ == '__main__':
    main()
