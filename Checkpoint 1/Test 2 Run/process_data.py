import pandas as pd
import numpy as np
import scipy.stats as stats
import os

file_path = '/Users/hdj/Documents/CS-6365/dataverse_files/YEAR-04-DATA-PUF.csv'
df = pd.read_csv(file_path, low_memory=False)

# 1. Cleaning
# Drop missing values in the target columns
target_cols = ['Benefits_Health', 'BenefitsImpact']
df_clean = df.dropna(subset=target_cols).copy()

# Filter out any 97/98 if they exist (just in case, though profile didn't show them)
df_clean = df_clean[~df_clean['Benefits_Health'].isin([97, 98])]
df_clean = df_clean[~df_clean['BenefitsImpact'].isin([97, 98])]

# 2. Correlation on numerical values before string mapping
# We'll calculate Pearson correlation and p-value
r, p_value = stats.pearsonr(df_clean['Benefits_Health'], df_clean['BenefitsImpact'])

# Also Spearman
rho, p_value_spearman = stats.spearmanr(df_clean['Benefits_Health'], df_clean['BenefitsImpact'])

# 3. Likert Scale Mapping
def map_likert(val):
    if val in [1.0, 2.0]:
        return 'Negative'
    elif val == 3.0:
        return 'Neutral/No Impact'
    elif val in [4.0, 5.0]:
        return 'Positive'
    return val

df_clean['BenefitsImpact_Mapped'] = df_clean['BenefitsImpact'].apply(map_likert)

# 4. Weighted Percentages / Aggregations
# Using 'year4wt' as the weight column
weight_col = 'year4wt'
if weight_col not in df_clean.columns:
    weight_col = 'stateweight'

# Cross-tabulation of Benefits_Health and Mapped BenefitsImpact with weights
crosstab_weighted = pd.crosstab(
    df_clean['Benefits_Health'], 
    df_clean['BenefitsImpact_Mapped'], 
    values=df_clean[weight_col], 
    aggfunc='sum', 
    normalize='index' # row percentages
) * 100

# 5. Save cleaned subset to "Test 2 Run" folder
out_dir = '/Users/hdj/Documents/CS-6365/Test 2 Run'
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, 'cleaned_subset_benefits.csv')

# Save only the relevant columns to save space, or the whole df? Prompt says "the cleaned subset data"
cols_to_save = ['Benefits_Health', 'BenefitsImpact', 'BenefitsImpact_Mapped', weight_col]
df_clean[cols_to_save].to_csv(out_file, index=False)

print("Correlation (Pearson): r =", r, "p =", p_value)
print("Correlation (Spearman): rho =", rho, "p =", p_value_spearman)
print("\nWeighted Row Percentages (Benefits_Health -> BenefitsImpact_Mapped):")
print(crosstab_weighted)
print("\nSaved cleaned dataset to:", out_file)
