import pandas as pd
import os

file_path = '/Users/hdj/Documents/CS-6365/dataverse_files/YEAR-04-DATA-PUF.csv'
print("Loading data...")
df = pd.read_csv(file_path, low_memory=False)

print("\n--- Matching Columns ---")
cols = df.columns
weight_cols = [c for c in cols if 'weight' in c.lower() or 'wt' in c.lower()]
target_cols = [c for c in cols if c in ['Benefits_Health', 'BenefitsImpact']]

print("Weight columns:", weight_cols)
print("Target columns:", target_cols)

if 'Benefits_Health' in df.columns:
    print("\n--- Benefits_Health Value Counts ---")
    print(df['Benefits_Health'].value_counts(dropna=False))

if 'BenefitsImpact' in df.columns:
    print("\n--- BenefitsImpact Value Counts ---")
    print(df['BenefitsImpact'].value_counts(dropna=False))
