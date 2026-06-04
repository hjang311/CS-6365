import pandas as pd

def main():
    # 1. Load the CSV file
    df = pd.read_csv('/Users/hdj/Documents/CS-6365/dataverse_files/YEAR-04-DATA-PUF.csv')

    # 2. Focus on the Benefits_Health and BenefitsImpact columns
    target_cols = ['ResponseId', 'Benefits_Health', 'BenefitsImpact', 'year4wt']
    subset = df[target_cols].copy()

    # 3. Clean and map these columns (filter out NA)
    # Filter out missing values 'NA' which might be read as NaN or string 'NA'
    subset = subset.dropna(subset=['Benefits_Health', 'BenefitsImpact'])
    subset = subset[(subset['Benefits_Health'] != 'NA') & (subset['BenefitsImpact'] != 'NA')]
    
    # Convert types to numeric
    subset['Benefits_Health'] = pd.to_numeric(subset['Benefits_Health'])
    subset['BenefitsImpact'] = pd.to_numeric(subset['BenefitsImpact'])

    # Determine values:
    # 1, 2 = Negative impact
    # 3 = No impact
    # 4, 5 = Positive impact

    # 4. Calculate cross-tabulated correlation
    positive_mask = subset['BenefitsImpact'].isin([4, 5])
    negative_mask = subset['BenefitsImpact'].isin([1, 2])

    pos_df = subset[positive_mask]
    neg_df = subset[negative_mask]

    pos_pct = pos_df['Benefits_Health'].mean() * 100
    neg_pct = neg_df['Benefits_Health'].mean() * 100

    print(f"Unweighted - Positive impact offering health insurance: {pos_pct:.1f}%")
    print(f"Unweighted - Negative impact offering health insurance: {neg_pct:.1f}%")

    # Weighted
    if 'year4wt' in subset.columns:
        subset['year4wt'] = pd.to_numeric(subset['year4wt'])
        pos_df = subset[positive_mask]
        neg_df = subset[negative_mask]
        
        w_pos_health = (pos_df['Benefits_Health'] * pos_df['year4wt']).sum() / pos_df['year4wt'].sum() * 100
        w_neg_health = (neg_df['Benefits_Health'] * neg_df['year4wt']).sum() / neg_df['year4wt'].sum() * 100
        
        print(f"Weighted - Positive impact offering health insurance: {w_pos_health:.1f}%")
        print(f"Weighted - Negative impact offering health insurance: {w_neg_health:.1f}%")

    # 5. Save the cleaned, filtered subset DataFrame
    final_cols = ['ResponseId', 'Benefits_Health', 'BenefitsImpact']
    subset[final_cols].to_csv('/Users/hdj/Documents/CS-6365/cleaned_test_case_1.csv', index=False)
    print("Saved cleaned data to /Users/hdj/Documents/CS-6365/cleaned_test_case_1.csv")

if __name__ == "__main__":
    main()
