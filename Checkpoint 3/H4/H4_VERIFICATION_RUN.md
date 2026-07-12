# H4 Verification Run — Spatial Mismatch & Fundraising Efficiency

## Objective
H4 is a **Phase 1 manual hypothesis test** built after the team acquired Zillow
ZHVI, merged it with the NCCS/BMF/ACS frame, and specified the cleaning and
control recipe. This run serves two purposes:

1. **Manual Pipeline Verification:** Confirm that the Phase 1 acquisition,
   merge, specialization, and cleaning choices produce a usable modeling frame.
2. **Sociological Validation:** Test the nonprofit spatial-mismatch hypothesis
   with the robust outlier-capped DV across organization-size segments.

Phase 2 later uses H4 as a known calibration row in the fixed-list unrolled
loop. The loop reproduces this manual test; it did not originate the hypothesis.

## Formal Hypothesis

**Hypothesis:** High local real estate prices (proxied by Zillow Home Value Index) increase overhead costs, reducing the fundraising efficiency of nonprofits located in those ZIP codes.

* **Independent Variable (IV):** `log_zhvi_2022` (Log of Zillow Home Value Index 2022)
* **Dependent Variable (DV):** `fundraising_efficiency_w` (Winsorized Fundraising Efficiency)
* **Rationale:** Higher local real estate prices increase operational and spatial overhead (rent, salary costs, logistics), which decreases the ratio of contributions secured relative to total fundraising expenses.
* **Key Citations:** Kain (1968), Bielefeld (2000), Harrison & Wolch (1998).

## Methodology & Control Set
We run a robust OLS regression (cov_type="HC1") on the `cp3_modeling_frame.csv` using the following control covariates:
- `log_total_revenue` (to control for organization scale)
- `C(ntee_major)` (to control for major nonprofit sectors)
- `C(region)` (to control for geographic macro-regions)
- `poverty_rate` (local socioeconomic demand control)
- `median_hh_income` (local donor capacity control)

The analysis is performed on:
1. **Full Sample** (Revenue >= $500,000)
2. **Mid-sized Nonprofits** (Revenue between $500,000 and $2,000,000)
3. **Large Nonprofits** (Revenue >= $2,000,000)

## Quantitative Findings

| Sample | n | IV coefficient (beta) | p-value | 95% CI | R-squared |
|---|---|---|---|---|---|
| Full (>=$500K) | 116,587 | -7.91647 | 2.427e-22 | [-9.5124, -6.3205] | 0.1766 |
| Mid ($500K-$2M) | 53,650 | -2.99536 | 3.615e-11 | [-3.8823, -2.1084] | 0.0912 |
| Large (>=$2M) | 62,936 | -11.53377 | 2.447e-16 | [-14.2913, -8.7762] | 0.0985 |

**Interpretation:**
There is a highly statistically significant ($p < 0.001$) negative association between local real estate prices and fundraising efficiency across all size segments. For the full sample, a 1-unit increase in the log of ZHVI decreases the winsorized fundraising efficiency by approximately 7.92 units. Notably, the penalty of operating in high-cost ZIP codes is much more severe for large organizations ($\beta = -11.53$) than for mid-sized organizations ($\beta = -3.00$). This provides strong evidence supporting the nonprofit spatial mismatch hypothesis.

## Phase 1 Execution and Phase 2 Replay

1. `01_acquire_data.py` acquires the exact December 2022 Zillow snapshot and
   creates the specialized NCCS subset.
2. `02_merge_pipeline.py` builds `cp3_modeling_frame.csv` and applies the fixed
   cleaning recipe.
3. `06_run_h4_h5_split.py` runs the manually specified H4 model for the full,
   mid-sized, and large samples.
4. `08_unrolled_loop.py` replays H4 as a pre-registered List A item and checks
   that its full-sample coefficient matches this accepted reference.

The earlier `07_deterministic_loop.py` combinatorial/LLM experiment is retained
only as historical context; it is not the primary H4 workflow.

## Sample Size Note
H4's full-sample n (116,587) is smaller than H5's (117,510) because ~12K organizations
are in ZIP codes without Zillow ZHVI coverage; those rows are listwise-deleted when
`log_zhvi_2022` enters the model.

## Artifacts (current — Phase 2 unrolled loop)
- `08_unrolled_loop.py` — Phase 2 pre-registered loop; List A row `H4` asserts this baseline β.
- `loop_results_v2/validation_check.md` — H4/H5 β reproduction check (β match = reproducibility, not theory verdict).
- `loop_results_v2/list_a_results.md` — theory outcome per hypothesis.
- `06_run_h4_h5_split.py` — regenerates the size-split tables above (`H4/H4_results.md`).

## Artifacts (historical — first loop iteration)
- `07_deterministic_loop.py` and `loop_results/` — the original 215-pair combinatorial batch. Superseded by `08`; kept for provenance.
