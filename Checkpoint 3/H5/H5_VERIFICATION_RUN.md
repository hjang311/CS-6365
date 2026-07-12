# H5 Verification Run — Social-Service Provider Density & Fundraising Efficiency

## Objective
H5 is a **Phase 1 manual hypothesis test** built after the team used IRS BMF
NTEE codes and ACS population to construct ZIP-level social-service provider
density. This run serves two purposes:

1. **Manual Pipeline Verification:** Confirm that the Phase 1 merge, IV
   construction, specialization, and cleaning choices produce a usable model.
2. **Sociological Validation:** Test the provider-competition hypothesis with
   the robust outlier-capped DV across organization-size segments.

Phase 2 later uses H5 as a known calibration row in the fixed-list unrolled
loop. The loop reproduces the coefficient while preserving the substantive
result: the hypothesized negative direction was rejected.

## Formal Hypothesis

**Hypothesis:** Among nonprofits with annual revenue ≥ $500,000, a higher local density of mission-critical social-service providers (food banks, food programs, soup kitchens, and homeless/related shelters per 10,000 residents) is associated with **lower** fundraising efficiency, because a denser field of providers intensifies competition for the same local donor base, raising fundraising expense relative to contributions. The effect is expected to be **stronger among smaller ($500K–$2M) organizations** — which have shallower donor bases — than larger (≥$2M) ones.

* **Independent Variable (IV):** `log_nonprofit_branch_density` — log of social-service nonprofits per 10,000 residents (NTEE K30/K31/K35/L40/L41/P43, from IRS BMF, normalized by ACS ZIP population).
* **Dependent Variable (DV):** `fundraising_efficiency_w` — winsorized fundraising efficiency (total contributions ÷ fundraising-expense proxy, capped at the 99th percentile).
* **Controls:** `log_total_revenue`, `C(ntee_major)`, `C(region)`, `poverty_rate`, `median_hh_income`.
* **Key Citations:** Rose-Ackerman (1982), Weisbrod (1988), Thornton (2006).

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
| Full (>=$500K) | 117,510 | 2.11963 | 0.002447 | [0.7485, 3.4908] | 0.1756 |
| Mid ($500K-$2M) | 53,972 | 1.10692 | 0.004737 | [0.3388, 1.8751] | 0.0904 |
| Large (>=$2M) | 63,537 | 3.05552 | 0.009074 | [0.7603, 5.3507] | 0.0973 |

**Interpretation:**
The hypothesis is **rejected**. The data reveals a highly statistically significant ($p < 0.01$) **positive** association between social-service provider density and fundraising efficiency across all size segments. Rather than intense competition depressing efficiency, a higher density of mission-critical nonprofits in a ZIP code is correlated with *better* fundraising efficiency. This may suggest an agglomeration effect or a clustering around high-donor capital that offsets the competition. Furthermore, contrary to expectations, the positive effect is stronger for large organizations ($\beta = +3.06$) than mid-sized ones ($\beta = +1.11$).

## Phase 1 Execution and Phase 2 Replay

1. `02_merge_pipeline.py` counts the selected social-service NTEE categories,
   normalizes them by ACS population, and builds `cp3_modeling_frame.csv`.
2. The same script applies the fixed financial and geographic cleaning recipe.
3. `06_run_h4_h5_split.py` runs the manually specified H5 model for the full,
   mid-sized, and large samples.
4. `08_unrolled_loop.py` replays H5 as a pre-registered List A item and checks
   that its full-sample coefficient matches this accepted reference.

The earlier `07_deterministic_loop.py` combinatorial/LLM experiment is retained
only as historical context; it is not the primary H5 workflow.

## Sample Size Note
H5's full-sample n (117,510) exceeds H4's (116,587) because H5's IV
(`log_nonprofit_branch_density`) has no ZHVI dependency — the ~12K rows lacking
Zillow coverage are only dropped when `log_zhvi_2022` enters the model.

## Artifacts (current — Phase 2 unrolled loop)
- `08_unrolled_loop.py` — Phase 2 pre-registered loop; List A row `H5` asserts this baseline β. Note: `08`'s validation PASS means the β was **reproduced**; the hypothesis itself is rejected (positive sign) as documented above.
- `loop_results_v2/validation_check.md` — H4/H5 β reproduction check.
- `loop_results_v2/list_a_results.md` — theory outcome per hypothesis.
- `06_run_h4_h5_split.py` — regenerates the size-split tables above (`H5/H5_results.md`).

## Artifacts (historical — first loop iteration)
- `07_deterministic_loop.py` and `loop_results/` — the original 215-pair combinatorial batch. Superseded by `08`; kept for provenance.
