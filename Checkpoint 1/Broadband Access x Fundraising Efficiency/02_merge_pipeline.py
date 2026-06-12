import os
import struct
import numpy as np
import pandas as pd

def decode_nccs_float(val):
    if pd.isnull(val):
        return np.nan
    try:
        val_float = float(val)
        if val_float == 0.0:
            return 0.0
        if abs(val_float) < 1e-300:
            bits = struct.unpack('<Q', struct.pack('<d', val_float))[0]
            return float(bits & 0xFFFFFFFF)
        return val_float
    except Exception:
        return np.nan

# Set directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")

def clean_zip_zcta(val):
    if pd.isnull(val):
        return None
    val_str = str(val).strip()
    if not val_str:
        return None
    if val_str.endswith('.0'):
        val_str = val_str[:-2]
    digits = ''.join(c for c in val_str if c.isdigit())
    if not digits:
        return None
    return digits.zfill(5)

def merge_pipeline():
    print("Starting Data Merge Pipeline...")
    
    # Load BMF Georgia
    bmf_path = os.path.join(DATA_DIR, "eo_ga.csv")
    if not os.path.exists(bmf_path):
        raise FileNotFoundError(f"BMF Georgia data not found at {bmf_path}. Run 01_acquire_data.py first.")
    bmf = pd.read_csv(bmf_path)
    print(f"Loaded BMF Georgia: {len(bmf)} rows")
    
    # Filter BMF to 501(c)(3) public charities (SUBSECTION == 3)
    # Check column name (usually SUBSECTION)
    sub_col = [c for c in bmf.columns if c.upper() == "SUBSECTION"][0]
    bmf_3 = bmf[bmf[sub_col] == 3].copy()
    print(f"Filtered BMF to 501(c)(3) public charities: {len(bmf_3)} rows")
    
    # Load NCCS CORE 2022 subset
    nccs_path = os.path.join(DATA_DIR, "nccs_core_subset.csv")
    if not os.path.exists(nccs_path):
        raise FileNotFoundError(f"NCCS subset not found at {nccs_path}. Run 01_acquire_data.py first.")
    nccs = pd.read_csv(nccs_path)
    print(f"Loaded NCCS CORE 2022 subset: {len(nccs)} rows")
    
    # Clean EINs for joining
    # BMF EIN key is usually "EIN", NCCS is "EIN2" (standardized in our subset)
    ein_col_bmf = [c for c in bmf_3.columns if c.upper() == "EIN"][0]
    bmf_3['EIN_str'] = bmf_3[ein_col_bmf].astype(str).str.replace(r'\D', '', regex=True).str.zfill(9)
    nccs['EIN_str'] = nccs['EIN2'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(9)
    
    # Inner join BMF and NCCS on EIN
    merged_financials = bmf_3.merge(nccs, on='EIN_str', how='inner')
    print(f"Merged BMF and NCCS financials on EIN. Matched: {len(merged_financials)} organizations.")
    
    # Clean and truncate ZIP codes to 5-digit ZCTAs
    zip_col = [c for c in merged_financials.columns if c.upper() == "ZIP"][0]
    # Handle ZIP+4 formatting (e.g. 30082-4886 or 300824886)
    merged_financials['ZIP_5'] = (
        merged_financials[zip_col]
        .astype(str)
        .str.split('-')
        .str[0]
        .apply(clean_zip_zcta)
    )
    
    # Load Crosswalk if available
    xwalk_path = os.path.join(DATA_DIR, "zip_zcta_crosswalk.csv")
    use_crosswalk = os.path.exists(xwalk_path)
    if use_crosswalk:
        print("ZIP-to-ZCTA Crosswalk file found. Loading crosswalk...")
        xwalk = pd.read_csv(xwalk_path)
        # Standardize columns
        zip_col_xwalk = [c for c in xwalk.columns if 'zip' in c.lower()][0]
        zcta_col_xwalk = [c for c in xwalk.columns if 'zcta' in c.lower()][0]
        xwalk['zip_clean'] = xwalk[zip_col_xwalk].apply(clean_zip_zcta)
        xwalk['zcta_clean'] = xwalk[zcta_col_xwalk].apply(clean_zip_zcta)
        
        # Merge crosswalk
        merged_financials = merged_financials.merge(
            xwalk[['zip_clean', 'zcta_clean']],
            left_on='ZIP_5',
            right_on='zip_clean',
            how='left'
        )
        # Fallback to ZIP_5 if crosswalk mapping is missing
        merged_financials['ZCTA'] = merged_financials['zcta_clean'].fillna(merged_financials['ZIP_5'])
        # Drop temporary cols
        merged_financials = merged_financials.drop(columns=['zip_clean', 'zcta_clean'])
        print(f"Applied ZIP-to-ZCTA crosswalk. Non-trivial mappings: {merged_financials['ZCTA'].nunique()} unique ZCTAs.")
    else:
        print("No ZIP-to-ZCTA crosswalk found. Falling back to Naive Join (assuming ZIP == ZCTA)...")
        merged_financials['ZCTA'] = merged_financials['ZIP_5']
        
    # Load Census Broadband Data
    census_path = os.path.join(DATA_DIR, "census_broadband.csv")
    if not os.path.exists(census_path):
        raise FileNotFoundError(f"Census broadband data not found at {census_path}. Run 01_acquire_data.py first.")
    census = pd.read_csv(census_path)
    print(f"Loaded Census Broadband estimates: {len(census)} ZCTAs")
    
    # Locate ZCTA column in Census CSV
    # Usually "zip code tabulation area"
    zcta_col_census = [c for c in census.columns if 'zip' in c.lower() or 'zcta' in c.lower()][0]
    census['ZCTA_clean'] = census[zcta_col_census].astype(str).str.zfill(5)
    
    # Join with Census Broadband
    final_merged = merged_financials.merge(census, left_on='ZCTA', right_on='ZCTA_clean', how='inner')
    print(f"Joined with Census Broadband on ZCTA. Matched: {len(final_merged)} organizations.")
    
    # Drop temp cols
    if 'ZCTA_clean' in final_merged.columns:
        final_merged = final_merged.drop(columns=['ZCTA_clean'])
        
    # Decode NCCS float columns to recover actual integer values
    nccs_cols = ["F9_08_REV_CONTR_TOT", "F9_09_EXP_TOT_TOT", "F9_08_REV_TOT_TOT", "F9_09_EXP_OTH_TOT_D"]
    for col in nccs_cols:
        if col in final_merged.columns:
            final_merged[col] = final_merged[col].apply(decode_nccs_float)
        
    # Save output dataset
    out_path = os.path.join(DATA_DIR, "merged_georgia.csv")
    final_merged.to_csv(out_path, index=False)
    print(f"Merged dataset successfully saved to {out_path}. Total final rows: {len(final_merged)}")

if __name__ == "__main__":
    merge_pipeline()
