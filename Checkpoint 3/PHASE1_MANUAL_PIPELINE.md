# Phase 1: Manual Data and Hypothesis Pipeline

Phase 1 records the work that was difficult to perform by hand before it was
wrapped in the Phase 2 unrolled loop. The team selected and acquired external
datasets, designed merge keys and variables, chose cleaning rules, specified
hypotheses, and ran each model separately.

This is intentionally not an agentic phase. The important artifact is the
reproducible research recipe that Phase 2 later repeats.

## 1. Starting point: Checkpoint 2 H2

The first complete manual pipeline is
[`Checkpoint 2/H2_Pipeline/`](../Checkpoint%202/H2_Pipeline/):

1. Download NCCS CORE 990 files for 2018–2022.
2. Download the IRS Exempt Organizations Business Master File (BMF).
3. Query FDIC BankFind for bank branches by ZIP code.
4. Query Census ACS5 for ZIP-level population, poverty, and median household
   income.
5. Join nonprofit financial records to geography and socioeconomic controls.
6. Construct bank branches per 10,000 residents.
7. Test whether lower bank-branch density is associated with greater
   fundraising efficiency.

The accepted H2 reference was a negative full-sample coefficient of about
`-0.115`. Phase 2 treats that value as qualitative context rather than a numeric
assertion because the CP2 and CP3 modeling frames are not identical.

## 2. Checkpoint 3 extension: Zillow and provider density

Checkpoint 3 extends the federal data spine rather than replacing it:

| Source | Granularity | Purpose |
|---|---|---|
| NCCS CORE 990 (2018–2022) | nonprofit organization-year | revenue, contributions, expenses |
| IRS BMF | nonprofit headquarters / ZIP | ZIP, state, NTEE sector |
| Census ACS5 | ZCTA | population, poverty, median income |
| FDIC BankFind | ZIP | H2 bank-branch density replay |
| Zillow ZHVI, December 2022 | ZIP | H4 local housing-cost proxy |

[`01_acquire_data.py`](01_acquire_data.py) performs the CP3-specific acquisition
step: it subsets the existing NCCS files and downloads the exact Zillow
`2022-12-31` snapshot. A missing or changed snapshot is a hard failure because
silently substituting another date would change H4.

[`02_merge_pipeline.py`](02_merge_pipeline.py) then:

- joins NCCS to IRS BMF by EIN;
- joins ACS, FDIC, and Zillow by five-digit ZIP;
- counts BMF organizations in social-service NTEE prefixes
  `K30/K31/K35/L40/L41/P43`;
- constructs social-service providers per 10,000 residents;
- constructs bank branches per 10,000 residents; and
- writes `data/cp3_modeling_frame.csv`.

The large counts printed before cleaning are **organization-year merge rows**,
not the final analysis sample. The cleaning steps reduce that intermediate
frame to approximately 158,323 rows.

## 3. Manual specialization and cleaning decisions

The “specialization” in Phase 1 is the set of human-designed decisions that
make a hypothesis testable. The LLM did not dynamically alter these decisions.

### Columns retained

- identifiers and merge keys: EIN, ZIP, state, NTEE code, tax year;
- financial variables needed for the fundraising-efficiency outcome;
- hypothesis IVs: ZHVI, nonprofit density, bank density;
- socioeconomic controls: population, poverty, median household income; and
- model controls: revenue scale, NTEE major group, Census region.

### Cleaning recipe

1. Keep nonprofits with annual revenue of at least `$500,000`.
2. Require positive contributions and positive fundraising expense.
3. Require at least `$5,000` in the fundraising-expense proxy.
4. Cap raw fundraising efficiency at `1,000` to remove implausible ratio
   artifacts.
5. Exclude observed ZIP populations below `1,000`.
6. Winsorize fundraising efficiency at its 99th percentile for level OLS.
7. Log-transform skewed revenue, ZHVI, and density variables.
8. Use listwise deletion for the IV, DV, and fixed control set at model time.

Rows with **missing** ACS population are retained in the saved modeling frame
for auditability. They are not treated as populations above 1,000; regressions
requiring ACS controls remove them through listwise deletion. This distinction
preserves the accepted Phase 1 frame and should not be changed casually.

## 4. Outcome and model

The outcome is:

```text
fundraising_efficiency =
    total_contributions
    / (professional_fundraising_fees + fundraising_events_direct_expenses)
```

The confirmatory model used for H4 and H5 is:

```text
DV ~ IV
   + log_total_revenue
   + C(ntee_major)
   + C(region)
   + poverty_rate
   + median_hh_income
```

OLS uses HC1 robust standard errors. The same formula is run for the full,
mid-sized (`$500K–$2M`), and large (`≥$2M`) samples by
[`06_run_h4_h5_split.py`](06_run_h4_h5_split.py).

## 5. Manual hypotheses

### H2 — bank-branch density

- **IV:** `bank_branch_density`
- **DV:** `fundraising_efficiency_w`
- **Expected direction:** negative
- **Source:** Checkpoint 2 H2 pipeline

### H4 — local housing cost

- **IV:** `log_zhvi_2022`
- **DV:** `fundraising_efficiency_w`
- **Expected direction:** negative
- **Accepted reference:** β ≈ `-7.91647`
- **Finding:** direction confirmed
- **Full write-up:** [`H4/H4_VERIFICATION_RUN.md`](H4/H4_VERIFICATION_RUN.md)

### H5 — social-service provider density

- **IV:** `log_nonprofit_branch_density`
- **DV:** `fundraising_efficiency_w`
- **Expected direction:** negative (competition)
- **Accepted reference:** β ≈ `+2.11963`
- **Finding:** theory rejected; the association is positive
- **Full write-up:** [`H5/H5_VERIFICATION_RUN.md`](H5/H5_VERIFICATION_RUN.md)

“PASS” in a loop validation report means that the accepted coefficient was
reproduced. It does not mean that the hypothesis direction was confirmed.

## 6. Why Phase 2 follows

Phase 1 repeats the same difficult sequence:

```text
name hypothesis
→ identify IV/DV and relevant columns
→ clean and subset
→ run controlled OLS
→ record coefficient, p-value, confidence interval, R², and n
→ compare result with the expected direction
```

Phase 2 places a small, explicit hypothesis agenda in a deterministic loop and
executes that sequence consistently. See
[`PHASE2_UNROLLED_LOOP.md`](PHASE2_UNROLLED_LOOP.md).

## 7. Scope and research limitations

Phase 1 establishes a reproducible intermediate research frame; it is not a
causal panel analysis:

- 2018–2022 organization-year rows are pooled;
- the model has no year fixed effects;
- HC1 errors are not clustered by EIN or ZIP;
- ACS and Zillow have coarser temporal/spatial granularity than the 990 panel;
- headquarters ZIP may not represent every service location; and
- the fundraising-expense proxy is constructed from available 990 fields.

The professor's July 10 guidance was not to over-refine this two-variable model
in Phase 2. These limitations motivate Phase 3's richer indicators,
higher-order relationships, and finer-granularity data.
