import pandas as pd
df = pd.read_csv('/Users/hdj/Documents/CS-6365/[Test 3 Run]/cleaned_subset_analysis.csv')
nulls = df.isnull().sum()
print("Columns with nulls:")
print(nulls[nulls > 0])
print("\nRows with nulls (first 5):")
print(df[df.isnull().any(axis=1)].head())
