import pandas as pd
import numpy as np
import scipy.stats as stats
import sys

csv_path = "/Users/hdj/Documents/CS-6365/Test 2 Run/cleaned_subset_benefits.csv"

try:
    df = pd.read_csv(csv_path)

    # 1 & 2. Check for nulls and missing codes in Benefits_Health and BenefitsImpact
    assert df['Benefits_Health'].isnull().sum() == 0, f"Found nulls in Benefits_Health"
    assert df['BenefitsImpact'].isnull().sum() == 0, f"Found nulls in BenefitsImpact"

    invalid_health = df[df['Benefits_Health'].isin([97, 98, 97.0, 98.0])]
    if len(invalid_health) > 0:
        raise AssertionError(f"Found 97/98 in Benefits_Health:\n{invalid_health.head()}")

    invalid_impact = df[df['BenefitsImpact'].isin([97, 98, 97.0, 98.0])]
    if len(invalid_impact) > 0:
        raise AssertionError(f"Found 97/98 in BenefitsImpact:\n{invalid_impact.head()}")

    # 3. Check out of bounds for Likert
    allowed_mappings = {'Negative', 'Neutral/No Impact', 'Positive'}
    if 'BenefitsImpact_Mapped' in df.columns:
        invalid_mapping = df[~df['BenefitsImpact_Mapped'].isin(allowed_mappings)]
        if len(invalid_mapping) > 0:
            raise AssertionError(f"Found out-of-bound mappings in BenefitsImpact_Mapped:\n{invalid_mapping.head()}")

    # 4. Correlation and p-value
    r, p = stats.pearsonr(df['Benefits_Health'], df['BenefitsImpact'])
    print(f"Calculated r: {r}")
    print(f"Calculated p-value: {p}")
    assert p < 0.05, f"P-value is not < 0.05 (Calculated: {p})"
    
    assert np.isclose(r, 0.54668, atol=1e-3), f"Calculated r {r} does not match claimed 0.54668"

    print("ALL VALIDATION PASSED.")

except Exception as e:
    print(f"VALIDATION FAILED: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

