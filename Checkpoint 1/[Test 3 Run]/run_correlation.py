import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import itertools
import os
import json

def main():
    file_path = '/Users/hdj/Documents/CS-6365/dataverse_files/YEAR-04-DATA-PUF.csv'
    output_dir = '/Users/hdj/Documents/CS-6365/[Test 3 Run]'
    
    # Load dataset
    df = pd.read_csv(file_path, low_memory=False)
    
    # Identify numerical columns
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    weights = ['year4wt', 'stateweight']
    for w in weights:
        if w in num_cols:
            num_cols.remove(w)
            
    df_num = df[num_cols].copy()
    df_num.replace([97, 98], np.nan, inplace=True)
    
    valid_cols = df_num.columns[df_num.nunique() > 1].tolist()
    
    # Calculate full correlation matrix for initial fast screening
    corr_matrix = df_num[valid_cols].corr(method='pearson')
    
    correlations = []
    for i in range(len(valid_cols)):
        col1 = valid_cols[i]
        for j in range(i + 1, len(valid_cols)):
            col2 = valid_cols[j]
            r = corr_matrix.loc[col1, col2]
            if pd.isna(r) or abs(r) < 0.1:
                continue
            
            subset = df[[col1, col2]].copy()
            subset.replace([97, 98], np.nan, inplace=True)
            subset.dropna(inplace=True)
            if len(subset) < 30:
                continue
            
            try:
                r_exact, p_val = pearsonr(subset[col1], subset[col2])
                if p_val < 0.05:
                    correlations.append({
                        'var1': col1,
                        'var2': col2,
                        'r': r_exact,
                        'p_value': p_val,
                        'abs_r': abs(r_exact)
                    })
            except:
                pass
                
    correlations.sort(key=lambda x: (x['p_value'], -x['abs_r']))
    
    # Greedy selection to ensure listwise deletion across all selected columns 
    # still yields p < 0.05 for all top 5 pairs.
    top_5 = []
    top_cols = set()
    if 'year4wt' in df.columns:
        top_cols.add('year4wt')
        
    for c in correlations:
        candidate_cols = top_cols.union({c['var1'], c['var2']})
        
        df_test = df[list(candidate_cols)].copy()
        df_test.replace([97, 98], np.nan, inplace=True)
        df_test.dropna(inplace=True)
        
        if len(df_test) < 30:
            continue
            
        all_valid = True
        test_pairs = top_5 + [c]
        new_results = []
        
        for pair in test_pairs:
            col1, col2 = pair['var1'], pair['var2']
            try:
                r_exact, p_val = pearsonr(df_test[col1], df_test[col2])
                if p_val >= 0.05:
                    all_valid = False
                    break
                new_results.append({
                    'var1': col1,
                    'var2': col2,
                    'r': r_exact,
                    'p_value': p_val,
                    'abs_r': abs(r_exact)
                })
            except:
                all_valid = False
                break
                
        if all_valid:
            # Re-sort to maintain order based on updated p-values
            new_results.sort(key=lambda x: (x['p_value'], -x['abs_r']))
            top_5 = new_results
            top_cols = candidate_cols
            if len(top_5) == 5:
                break
                
    print("Top 5 Statistically Significant Correlations (after joint listwise deletion):")
    for idx, c in enumerate(top_5):
        print(f"{idx+1}. {c['var1']} & {c['var2']} -> r: {c['r']:.4f}, p-value: {c['p_value']:.4e}")
        
    df_subset = df[list(top_cols)].copy()
    df_subset.replace([97, 98], np.nan, inplace=True)
    df_subset.dropna(inplace=True)
    df_subset.to_csv(os.path.join(output_dir, 'cleaned_subset_analysis.csv'), index=False)
    
    # We only save var1, var2, r, p_value, abs_r, so json doesn't have extra stuff
    with open(os.path.join(output_dir, 'top_5_correlations.json'), 'w') as f:
        json.dump(top_5, f, indent=4)

if __name__ == '__main__':
    main()
