# Analysis slice manifest

- built_by: early_build
- source_frame: `$REPO_ROOT/Checkpoint 4/early_build/data/cp4_frame_with_soup_density.csv`
- zip_allow_list: `$REPO_ROOT/Checkpoint 4/early_build/data/acfb_29_county_zips.csv` (305 ZIPs)
- tax_year: **2022** (cross-section; soup density is a ~2026 stock)
- rows: **583**
- distinct ZIP5: **159**
- rows with soup_kitchen_density > 0: **524**

## Rationale

National multi-year OLS with 2026 site density is temporally and spatially
misaligned (see DATA_GRANULARITY_AUDIT.md). This slice matches July 10 intent:
Atlanta / ACFB-area geography and a single 990 year.

