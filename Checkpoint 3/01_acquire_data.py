"""
01_acquire_data.py  —  Phase 1: Data Acquisition & Subsetting (manual pipeline)

Pulls core data sources, enforces enterprise filtering (>= $500K revenue),
and aggressively subsets columns to preserve LLM context windows.
Downloads Zillow ZHVI Zip-level housing cost data.

COLD START NOTE: This script does NOT download NCCS CORE, IRS BMF, Census ACS,
or FDIC data. Those are acquired by `Checkpoint 2/H2_Pipeline/01_acquire_data.py`
(CENSUS_API_KEY needed for ACS) and then copied into `Checkpoint 3/data/`.
See Checkpoint 3/README.md for the full cold-start runbook.
"""
import os
import ssl
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA, exist_ok=True)

REV_FILTER = 500_000  # Enterprise-level nonprofits only

# Aggressively small column subset for LLM readability
CORE_COLS = [
    "ein", "tax_year", "total_revenue", "total_expenses", "total_contributions",
    "fundraising_events_direct_expenses", "professional_fundraising_fees"
]

ZILLOW_ZHVI_URL = "https://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"

def get_core_subset():
    """Load core files from Checkpoint 3 data directory, filter, and save subset."""
    print("[Ingestion] Loading and subsetting NCCS Core files...")
    parts = []
    for f in os.listdir(DATA):
        if f.startswith("core_") and f.endswith("_filtered.csv"):
            path = os.path.join(DATA, f)
            print(f"  reading {path}")
            df = pd.read_csv(path, usecols=lambda c: c in CORE_COLS, low_memory=False)
            parts.append(df)
            
    if not parts:
        raise SystemExit(
            "No core_*_filtered.csv found in Checkpoint 3/data/.\n"
            "Cold start: run `Checkpoint 2/H2_Pipeline/01_acquire_data.py` "
            "(downloads NCCS CORE 2018-2022, IRS BMF, FDIC, Census ACS; "
            "needs CENSUS_API_KEY for ACS), then copy the resulting CSVs from "
            "`Checkpoint 2/H2_Pipeline/data/` into `Checkpoint 3/data/`.\n"
            "See Checkpoint 3/README.md."
        )
        
    df_core = pd.concat(parts, ignore_index=True)
    df_core["ein"] = df_core["ein"].astype(str).str.replace(r"\D", "", regex=True).str.zfill(9)
    df_core["total_revenue"] = pd.to_numeric(df_core["total_revenue"], errors="coerce")
    
    # Strictly filter for Enterprise level
    df_core = df_core[df_core["total_revenue"] >= REV_FILTER]
    
    # Save the NCCS Core subset
    subset_path = os.path.join(DATA, "core_subset.csv")
    df_core.to_csv(subset_path, index=False)
    print(f"[Ingestion] Saved {len(df_core):,} rows to {subset_path}")

def acquire_zillow_data():
    """Download Zillow ZHVI data, keep the fixed 2022-12-31 snapshot, and subset columns."""
    print(f"[Zillow] Fetching ZHVI from: {ZILLOW_ZHVI_URL}")
    try:
        # Download in chunks or load directly (file is ~50MB, read_csv handles url directly)
        try:
            df = pd.read_csv(ZILLOW_ZHVI_URL)
        except Exception as ssl_err:
            # macOS Python installs sometimes lack a configured certificate store.
            # Retry once with verification disabled, warning loudly — do NOT make
            # this the default for every HTTPS request in the process.
            print(f"[Zillow] WARNING: first attempt failed ({ssl_err}); "
                  "retrying with SSL verification disabled for this download only.")
            _prev = ssl._create_default_https_context
            ssl._create_default_https_context = ssl._create_unverified_context
            try:
                df = pd.read_csv(ZILLOW_ZHVI_URL)
            finally:
                ssl._create_default_https_context = _prev
        
        # Freeze the analysis to the documented December 2022 snapshot.
        target_col = "2022-12-31"
        if target_col not in df.columns:
            raise ValueError(
                "Required Zillow snapshot column '2022-12-31' is missing. "
                "Refusing to substitute a newer date because that would change H4."
            )
        if "RegionName" not in df.columns:
            raise ValueError("Zillow file is missing required ZIP column 'RegionName'.")

        print(f"  keeping ZIP code and column: {target_col}")
        sub = df[["RegionName", target_col]].rename(
            columns={"RegionName": "ZIP5", target_col: "zhvi_2022"}
        )
        if sub.empty or sub["zhvi_2022"].notna().sum() == 0:
            raise ValueError("Zillow snapshot parsed but contains no usable ZHVI values.")
        
        # Ensure ZIP5 is string padded to 5 digits
        sub["ZIP5"] = sub["ZIP5"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(5)
        
        out_path = os.path.join(DATA, "zillow_zhvi_2022.csv")
        sub.to_csv(out_path, index=False)
        print(f"[Zillow] Saved {len(sub):,} ZIP codes to {out_path}")
    except Exception as e:
        raise SystemExit(
            f"[Zillow Error] Failed to acquire the required 2022 snapshot: {e}"
        ) from e

def main():
    get_core_subset()
    acquire_zillow_data()
    print("Phase 1 subsetting complete.")

if __name__ == "__main__":
    main()
