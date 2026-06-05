import pandas as pd

try:
    df = pd.read_csv('/Users/hdj/Documents/CS-6365/dataverse_files/YEAR-04-DATA-PUF.csv')
    print('Benefits_Health value counts:')
    print(df['Benefits_Health'].value_counts(dropna=False))
    print('\nBenefitsImpact value counts:')
    print(df['BenefitsImpact'].value_counts(dropna=False))
except Exception as e:
    print(e)
