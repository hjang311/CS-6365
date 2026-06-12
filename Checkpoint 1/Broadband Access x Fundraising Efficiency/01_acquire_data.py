import os
import requests
import pandas as pd
from dotenv import load_dotenv
import ssl

# Bypass SSL certificate verification for downloads (common macOS Python issue)
ssl._create_default_https_context = ssl._create_unverified_context

# Set directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
os.makedirs(DATA_DIR, exist_ok=True)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(BASE_DIR), ".env"))
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Download complete.")
    else:
        raise Exception(f"Failed to download {url}. Status code: {response.status_code}")

def acquire_bmf_ga():
    bmf_url = "https://www.irs.gov/pub/irs-soi/eo_ga.csv"
    dest = os.path.join(DATA_DIR, "eo_ga.csv")
    download_file(bmf_url, dest)
    df = pd.read_csv(dest)
    print(f"BMF Georgia acquired. Shape: {df.shape}")

def acquire_nccs_subset():
    nccs_url = "https://nccsdata.s3.us-east-1.amazonaws.com/harmonized/core/501c3-pz/marts/CORE-2022-501C3-CHARITIES-PZ-HRMN-V1.csv"
    dest = os.path.join(DATA_DIR, "nccs_core_subset.csv")
    
    # Target columns in NCCS CORE 2022 PZ
    target_cols = [
        "EIN2",
        "F9_08_REV_CONTR_TOT",      # contributions
        "F9_09_EXP_OTH_TOT_D",      # fundraising expenses
        "F9_08_REV_TOT_TOT",        # total revenue
        "F9_09_EXP_TOT_TOT"         # total expenses
    ]
    
    print(f"Streaming NCCS CORE 2022 and extracting columns: {target_cols}...")
    
    # We will read in chunks and append to save memory
    chunk_size = 50000
    first_chunk = True
    
    try:
        # Check first row headers dynamically to handle any column case mismatch
        first_row = pd.read_csv(nccs_url, nrows=1)
        columns = list(first_row.columns)
        print(f"Headers found in remote NCCS file. Total: {len(columns)} columns.")
        
        # Determine exact header casing (e.g. EIN2 vs ein2)
        mapping = {}
        for tc in target_cols:
            matches = [c for c in columns if c.upper() == tc.upper()]
            if matches:
                mapping[tc] = matches[0]
            else:
                # If a column like F9_01_EXP_FUNDR_TOT_CY isn't found, check if F9_01_EXP_FUNDR_TOT_CY is inside
                potential = [c for c in columns if tc.upper() in c.upper()]
                if potential:
                    mapping[tc] = potential[0]
                else:
                    raise KeyError(f"Required NCCS column {tc} not found in remote headers: {columns}")
        
        actual_cols = list(mapping.values())
        print(f"Mapping requested columns to remote columns: {mapping}")
        
        chunks = pd.read_csv(nccs_url, chunksize=chunk_size, usecols=actual_cols)
        
        for idx, chunk in enumerate(chunks):
            # Rename back to standard casing if needed
            reverse_mapping = {v: k for k, v in mapping.items()}
            chunk = chunk.rename(columns=reverse_mapping)
            
            if first_chunk:
                chunk.to_csv(dest, index=False, mode="w")
                first_chunk = False
            else:
                chunk.to_csv(dest, index=False, mode="a", header=False)
                
            print(f"  Processed chunk {idx+1} (rows processed: {(idx+1)*chunk_size})...")
            
        print("NCCS CORE 2022 subset saved successfully.")
    except Exception as e:
        print("Error streaming NCCS data:", e)
        raise e

def acquire_census_broadband():
    if not CENSUS_API_KEY:
        raise ValueError("CENSUS_API_KEY is not defined in .env file.")
        
    print("Querying Census API for ZCTA Table B28002 variables...")
    # B28002_001E: Total Households
    # B28002_004E: Broadband of any type
    # B28002_007E: Broadband such as cable, fiber, or DSL
    # B28002_013E: No internet access
    url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B28002_001E,B28002_004E,B28002_007E,B28002_013E&for=zip%20code%20tabulation%20area:*&key={CENSUS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        headers = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        dest = os.path.join(DATA_DIR, "census_broadband.csv")
        df.to_csv(dest, index=False)
        print(f"Census broadband data acquired. Shape: {df.shape}")
    else:
        raise Exception(f"Census API request failed. Status code: {response.status_code}. Response: {response.text}")

def acquire_crosswalk():
    crosswalk_url = "https://raw.githubusercontent.com/censusreporter/acs-aggregate/master/crosswalks/zip_to_zcta/zip_zcta_xref.csv"
    dest = os.path.join(DATA_DIR, "zip_zcta_crosswalk.csv")
    try:
        download_file(crosswalk_url, dest)
        df = pd.read_csv(dest)
        print(f"ZIP-to-ZCTA Crosswalk acquired. Shape: {df.shape}")
    except Exception as e:
        print("Failed to acquire ZIP-to-ZCTA crosswalk programmatically:", e)
        print("Will fall back to Naive Join (assuming ZIP == ZCTA) during the merge stage.")

if __name__ == "__main__":
    print("Starting Data Acquisition Stage...")
    # acquire_bmf_ga()
    # acquire_census_broadband()
    # acquire_crosswalk()
    acquire_nccs_subset()
    print("Data Acquisition Stage Completed Successfully.")
