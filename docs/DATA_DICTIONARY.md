# Data Dictionary — Modeling Frames

Definitions for the national CP3 frame and CP4 enriched / sliced frames.  
Formulas match [`Checkpoint 3/README.md`](../Checkpoint%203/README.md) Key definitions — do not invent alternate DVs without updating that file and this one together.

## `Checkpoint 3/data/cp3_modeling_frame.csv`

**Shape (handoff):** ≈ 158,323 rows × 30 columns · org-year units · revenue filter ≥ $500K where applied upstream.

| Column | Type | Source / derivation |
|--------|------|---------------------|
| `ein` / `EIN` | str | NCCS CORE / BMF identifier (9-digit) |
| `tax_year` | int | Form 990 tax year |
| `ZIP5` | str | Org ZIP from BMF |
| `STATE` | str | BMF state |
| `NTEE_CD` | str | IRS BMF NTEE code |
| `ntee_major` | str | Major NTEE letter derived from `NTEE_CD` |
| `region` | str | Census region grouping (pipeline-derived) |
| `total_revenue` | float | NCCS CORE |
| `total_expenses` | float | NCCS CORE |
| `total_contributions` | float | NCCS CORE |
| `professional_fundraising_fees` | float | NCCS CORE |
| `fundraising_events_direct_expenses` | float | NCCS CORE |
| `fundraising_expense_proxy` | float | `professional_fundraising_fees + fundraising_events_direct_expenses` (zeros filled) |
| `fundraising_efficiency` | float | `total_contributions / fundraising_expense_proxy` (see Key definitions) |
| `fundraising_efficiency_w` | float | `fundraising_efficiency` winsorized at 99th percentile (**primary DV**) |
| `log_fundraising_efficiency` | float | log of efficiency (where used) |
| `log_total_revenue` | float | `log(total_revenue)` control |
| `median_hh_income` | float | Census ACS5 |
| `population` | float | Census ACS5 (ZCTA) |
| `poverty_rate` | float | Census ACS5 |
| `social_service_count` | float | BMF counts in selected NTEE social-service categories |
| `nonprofit_branch_density` | float | Provider / branch density per population (H5 IV base) |
| `log_nonprofit_branch_density` | float | log IV for H5 |
| `bank_branches` | float | FDIC branch count in ZIP |
| `bank_branch_density` | float | Branches per population (H2 IV base) |
| `log_bank_branch_density` | float | log IV for H2 |
| `zhvi_2022` | float | Zillow ZHVI Dec 2022 ZIP snapshot |
| `log_zhvi_2022` | float | log IV for H4 |
| `size_segment` | category | Mid vs large revenue split used in H4/H5 tables |

**Cleaning notes:** enterprise revenue filter; DV denominator proxy under-itemization; winsorization at p99 for `fundraising_efficiency_w`. See CP3 README Key definitions for exact thresholds.

## CP4 enriched frames

Built by named adapters + merge/slice utilities under `Checkpoint 4/engine/enrichment_tools/`.

### National / enriched (examples)

| Column pattern | Meaning |
|----------------|---------|
| `food_assistance_*` / `log_food_assistance_density` | Feed America or NTEE food-assistance density by ZIP |
| `housing_services_*` / `log_housing_services_density` | NTEE housing-services density by ZIP |
| `*_density_by_zip` side tables | ZIP-level density inputs before org merge |

### Cross-section slices (Phase 3 demos)

| Frame | Typical shape | Filter |
|-------|---------------|--------|
| `Checkpoint 4/data/cp4_atlanta_food_assistance_xsection.csv` | ≈ 583 rows × 33 cols (enrich); OLS n ≈ 444 | Atlanta-area × latest `tax_year` |
| `Checkpoint 4/data/cp4_chicago_housing_services_xsection.csv` | ≈ 503 rows × 33 cols; OLS n ≈ 403 | Chicago-area × latest `tax_year` |

CSVs under `Checkpoint 3/data/` and `Checkpoint 4/data/` are **gitignored** (except attribution / README exceptions). Regenerate via CP3 merge and CP4 acquire/enrich paths.

## Controls commonly included in OLS

- `log_total_revenue`
- `poverty_rate` and/or `median_hh_income` (hypothesis-dependent)
- Size splits via `size_segment` where tables report mid/large

Exact formulas for each pre-registered spec live in proposal JSON next to results (`proposals_round*.json`, `proposals_ta_verify.json`).
