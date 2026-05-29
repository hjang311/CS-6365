import pandas as pd
import os
import time

def profile_dataset(file_path):
    print(f"Loading dataset: {file_path}")
    start_time = time.time()
    
    # Load using pyarrow engine for speed and memory efficiency
    try:
        df = pd.read_csv(file_path, engine='pyarrow')
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return

    load_time = time.time() - start_time
    
    print("-" * 50)
    print(f"Data Profile")
    print("-" * 50)
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")
    print(f"Load Time: {load_time:.2f} seconds")
    
    print("\nSample Data (first 3 rows):")
    print(df.head(3))
    
    print("\nData Types Summary:")
    print(df.dtypes.value_counts())

if __name__ == "__main__":
    csv_path = "../query_result_2026-05-29T15_00_45.06955553-04_00.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
    else:
        profile_dataset(csv_path)
