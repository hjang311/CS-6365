# H2 Pipeline — Bank-Branch Density & Nonprofit Fundraising Efficiency

**Hypothesis (H2):** Among nonprofits with annual revenue ≥ $500,000, **lower bank-branch
density per ZIP** (a proxy for greater fintech adoption) is associated with **higher
fundraising efficiency**, with a stronger effect in smaller nonprofits.

| Role | Variable | Source |
|---|---|---|
| **IV** | bank-branch density per ZIP (branches / 10k residents) | FDIC BankFind locations API |
| **DV** | fundraising efficiency = contributions ÷ fundraising-cost proxy | NCCS CORE full-990 |
| Filter | total revenue ≥ $500K | NCCS CORE |
| Controls | log(revenue), NTEE major group, region, year | NCCS CORE + IRS BMF |
| Controls | poverty rate, median household income, population | Census ACS5 |
| Join keys | EIN (CORE↔BMF), ZIP (↔FDIC, ↔ACS) | — |

## Data sources (all verified live, June 2026)
- **NCCS CORE full-990:** `nccsdata.s3.us-east-1.amazonaws.com/processed/core/{YEAR}/990/core_{YEAR}_990.csv`
- **IRS EO BMF (ZIP, NTEE):** `irs.gov/pub/irs-soi/eo{1-4}.csv`
- **FDIC branches:** `api.fdic.gov/banks/locations` (no key)
- **Census ACS5:** `api.census.gov/data/2022/acs/acs5` — **needs a free key:**
  https://api.census.gov/data/key_signup.html → `export CENSUS_API_KEY=...`

## Run order
```bash
pip install -r requirements.txt
export CENSUS_API_KEY=your_key          # optional but recommended (enables per-capita IV + controls)
python 01_acquire_data.py --years 2018 2019 2020 2021 2022
python 02_merge_pipeline.py
python 03_analysis.py                    # writes findings_results.md
```
Quick single-year smoke test: `python 01_acquire_data.py --years 2022 --skip acs`

## ⚠️ Known limitations (documented for the write-up)
1. **DV denominator is a proxy.** NCCS CORE has no single Part IX Line 25 col-D
   "total fundraising expenses" field, so we use
   `professional_fundraising_fees + fundraising_events_direct_expenses`.
   Upgradeable to the true functional-expense column via 990 e-file XML later.
2. **IV is an adoption proxy, not direct fintech usage.** Branch density measures
   traditional banking infrastructure; the fintech link is inferential.
3. **Without a Census key**, the IV falls back to raw branch *count* (not per-capita
   density) and the poverty/income controls are dropped.

## Outputs (in `data/`, git-ignored if large)
- `core_{year}_filtered.csv`, `irs_bmf.csv`, `fdic_branches_by_zip.csv`, `census_acs_by_zip.csv`
- `h2_modeling_frame.csv` — the merged modeling table
- `findings_results.md` — auto-populated Week-1 metrics table
