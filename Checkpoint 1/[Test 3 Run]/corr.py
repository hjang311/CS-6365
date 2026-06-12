import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import json
import os

df = pd.read_csv('/Users/hdj/Documents/CS-6365/dataverse_files/YEAR-04-DATA-PUF.csv', low_memory=False)
num_df = df.select_dtypes(include=[np.number])
print("Shape of numeric df:", num_df.shape)
