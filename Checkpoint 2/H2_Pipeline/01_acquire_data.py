"""
01_acquire_data.py  —  H2 pipeline, data acquisition

Hypothesis (H2): Among nonprofits with annual revenue >= $500K, lower bank-branch
density per ZIP (a proxy for greater fintech adoption) is associated with higher
fundraising efficiency, with a stronger effect in smaller nonprofits.

Pulls four sources into ./data/ :
  1. NCCS CORE full-990 financials (2018-2022) — streamed + revenue-filtered (>= $500K)
  2. IRS EO Business Master File (eo1-4) — EIN -> ZIP, NTEE, STATE
  3. FDIC branch locations -> branch count per ZIP (the IV)
  4. Census ACS5 controls per ZCTA — poverty, median income, population

All endpoints verified live (June 2026). Census requires a free API key:
  https://api.census.gov/data/key_signup.html  ->  export CENSUS_API_KEY=...

Usage:
  python 01_acquire_data.py --years 2018 2019 2020 2021 2022
  python 01_acquire_data.py --years 2022          # quick single-year run
"""
import argparse, io, os, sys, time
import requests
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA, exist_ok=True)

REV_FILTER = 500_000  # H2 sample: nonprofits with total revenue >= $500K

NCCS_CORE = ("https://nccsdata.s3.us-east-1.amazonaws.com/"
             "processed/core/{year}/990/core_{year}_990.csv")
IRS_BMF = "https://www.irs.gov/pub/irs-soi/eo{n}.csv"
FDIC_LOCATIONS = "https://api.fdic.gov/banks/locations"
CENSUS_ACS5 = "https://api.census.gov/data/2022/acs/acs5"
CENSUS_ACS5_SUBJECT = "https://api.census.gov/data/2022/acs/acs5/subject"

# Columns we keep from the NCCS CORE full-990 file (verified names).
CORE_COLS = [
    "ein", "tax_year", "total_revenue", "total_expenses", "total_contributions",
    "professional_fundraising_fees",        # Part IX Line 11e
    "fundraising_events_direct_expenses",   # Part VIII Line 8b / events cost
    "office_expenses",
]


def acquire_nccs_core(years):
    """Stream each yearly CORE file and keep only rows with total_revenue >= $500K."""
    for year in years:
        url = NCCS_CORE.format(year=year)
        out = os.path.join(DATA, f"core_{year}_filtered.csv")
        print(f"[NCCS] {year}: streaming {url}")
        kept = []
        # chunked read keeps memory bounded on the large national files
        reader = pd.read_csv(url, usecols=lambda c: c in CORE_COLS,
                             chunksize=100_000, low_memory=False)
        n_total = 0
        for chunk in reader:
            n_total += len(chunk)
            chunk = chunk[pd.to_numeric(chunk["total_revenue"], errors="coerce")
                          >= REV_FILTER]
            if len(chunk):
                kept.append(chunk)
        df = pd.concat(kept, ignore_index=True) if kept else pd.DataFrame(columns=CORE_COLS)
        df["source_year"] = year
        df.to_csv(out, index=False)
        print(f"[NCCS] {year}: {n_total:,} rows scanned -> {len(df):,} kept (>= ${REV_FILTER:,})")


def acquire_irs_bmf():
    """IRS EO BMF (4 regional files) -> EIN, ZIP, NTEE_CD, STATE lookup."""
    frames = []
    for n in (1, 2, 3, 4):
        url = IRS_BMF.format(n=n)
        print(f"[BMF] eo{n}.csv")
        df = pd.read_csv(url, usecols=["EIN", "ZIP", "STATE", "NTEE_CD"],
                         dtype=str, low_memory=False)
        frames.append(df)
    bmf = pd.concat(frames, ignore_index=True)
    bmf["EIN"] = bmf["EIN"].str.zfill(9)
    bmf["ZIP5"] = bmf["ZIP"].str.slice(0, 5)
    bmf.to_csv(os.path.join(DATA, "irs_bmf.csv"), index=False)
    print(f"[BMF] {len(bmf):,} orgs -> irs_bmf.csv")


def acquire_fdic_branches():
    """FDIC branch locations -> count of branches per ZIP (the IV numerator)."""
    print("[FDIC] paging branch locations...")
    rows, offset, limit = [], 0, 10_000
    while True:
        r = requests.get(FDIC_LOCATIONS, params={
            "fields": "ZIP,STALP", "limit": limit, "offset": offset,
            "format": "json"}, timeout=60)
        r.raise_for_status()
        data = r.json().get("data", [])
        if not data:
            break
        rows.extend(d["data"] for d in data)
        offset += limit
        print(f"[FDIC]   fetched {len(rows):,} branches")
        time.sleep(0.2)
    df = pd.DataFrame(rows)
    df["ZIP5"] = df["ZIP"].astype(str).str.slice(0, 5)
    counts = (df.groupby("ZIP5").size().reset_index(name="bank_branches"))
    counts.to_csv(os.path.join(DATA, "fdic_branches_by_zip.csv"), index=False)
    print(f"[FDIC] {len(df):,} branches -> {len(counts):,} ZIPs -> fdic_branches_by_zip.csv")


def acquire_census_acs():
    """Census ACS5 per ZCTA: poverty rate, median household income, population."""
    key = os.getenv("CENSUS_API_KEY")
    if not key:
        print("[ACS] SKIPPED — set CENSUS_API_KEY (free: "
              "https://api.census.gov/data/key_signup.html)")
        return
    # detailed table: median household income + total population
    det = requests.get(CENSUS_ACS5, params={
        "get": "NAME,B19013_001E,B01003_001E",
        "for": "zip code tabulation area:*", "key": key}, timeout=120)
    det.raise_for_status()
    d = pd.DataFrame(det.json()[1:], columns=det.json()[0]).rename(columns={
        "B19013_001E": "median_hh_income", "B01003_001E": "population",
        "zip code tabulation area": "ZIP5"})
    # subject table: percent of people below poverty (S1701_C03_001E)
    sub = requests.get(CENSUS_ACS5_SUBJECT, params={
        "get": "S1701_C03_001E", "for": "zip code tabulation area:*",
        "key": key}, timeout=120)
    sub.raise_for_status()
    s = pd.DataFrame(sub.json()[1:], columns=sub.json()[0]).rename(columns={
        "S1701_C03_001E": "poverty_rate", "zip code tabulation area": "ZIP5"})
    acs = d.merge(s[["ZIP5", "poverty_rate"]], on="ZIP5", how="left")
    acs.to_csv(os.path.join(DATA, "census_acs_by_zip.csv"), index=False)
    print(f"[ACS] {len(acs):,} ZCTAs -> census_acs_by_zip.csv")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs="+", type=int,
                    default=[2018, 2019, 2020, 2021, 2022])
    ap.add_argument("--skip", nargs="*", default=[],
                    help="any of: nccs bmf fdic acs")
    args = ap.parse_args()

    if "nccs" not in args.skip: acquire_nccs_core(args.years)
    if "bmf" not in args.skip:  acquire_irs_bmf()
    if "fdic" not in args.skip: acquire_fdic_branches()
    if "acs" not in args.skip:  acquire_census_acs()
    print("Done. Files written to", DATA)
