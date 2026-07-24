# Phase 3 Evaluation Summary (deterministic)

This artifact is the **input context** for the propose step. It is assembled from Checkpoint 3 Phase 2 outputs; no new OLS is run here.

## Highlights for the agent

- **H4:** confirmed (negative ZHVI → efficiency); β ≈ -7.92
- **H5:** significant but theory rejected (positive density → efficiency)
- **Limitation thesis:** 2-var OLS easy to light up / hard to trust; near-identical R²; mechanical hits; coarse ZIP granularity → Phase 3

### Phase 3 tracks to pursue

- propose new socioeconomic indicators and test via shared OLS
- higher-order interaction specs (3+ variables)
- finer-granularity ACFB soup-kitchen density by ZIP

**Frame IV hint:** Prefer external/structural IVs already on frame (log_zhvi_2022, log_bank_branch_density, poverty_rate, median_hh_income, population, soup_kitchen_density if merged). Avoid mechanical DV components.

## Source: List A (excerpt)

```
# List A — Curated Hypothesis Agenda

Theory-first hypotheses wrapping Phase 1 (H4/H5) plus labeled control cases.

| ID | Role | IV → DV | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| H4 | confirmatory | `log_zhvi_2022` → `fundraising_efficiency_w` | negative | negative | confirmed | -7.91647 | 2.427e-22 | 0.1766 | 116,587 | ok |
| H5 | confirmatory | `log_nonprofit_branch_density` → `fundraising_efficiency_w` | negative | positive | rejected (opposite or mismatch) | 2.11963 | 0.002447 | 0.1756 | 117,510 | ok |
| H2_replay | phase1_replay | `bank_branch_density` → `fundraising_efficiency_w` | negative | negative | confirmed | -0.11560 | 0.001764 | 0.1756 | 117,510 | ok |
| event_cost_drag | mechanical_control | `fundraising_events_direct_expenses` → `fundraising_efficiency_w` | negative | negative | mechanical by construction (not a hypothesis) | -0.00003 | 1.336e-19 | 0.1919 | 117,510 | ok |
| affluence_clustering | exploratory | `log_zhvi_2022` → `log_nonprofit_branch_density` | positive | positive | confirmed | 0.06781 | 1.692e-65 | 0.0748 | 116,587 | ok |
| identity_revenue_expenses | identity_control | `total_expenses` → `total_revenue` | positive | positive | near-identity control (not a hypothesis) | 1.03207 | 0 | 0.9875 | 117,510 | ok |
| weak_population | weak_control | `population` → `fundraising_efficiency_w` | none | negative | n/a (no directional claim) | -0.00006 | 0.001325 | 0.1756 | 117,510 | ok |

## Rationale sources

- **H4**: Checkpoint 3/H4/H4_VERIFICATION_RUN.md
- **H5**: Checkpoint 3/H5/H5_VERIFICATION_RUN.md
- **H2_replay**: Checkpoint 2/H2_Pipeline/findings_results.md (CP2 beta ~ -0.115, qualitative reference)
- **event_cost_drag**: DV construction: event expense is part of fundraising_expense_proxy
- **affluence_clustering**: Geographic clustering context
- **identity_revenue_expenses**: Accounting identity control case
- **weak_population**: Expected weak after controls; 2-var limitation case

---
*Generated: 2026-07-12 10:37:47 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 08_unrolled_loop.py v2.1 (2026-07-12)*

```

## Source: List B (excerpt)

```
# List B — Bounded Two-Variable Limitation Harness

This is not a discovery agenda. The primary DV is fixed to `fundraising_efficiency_w`; the IV list is pre-registered in `list_b_pairs.json` before OLS to demonstrate why large-n two-variable significance is insufficient. Level/log duplicates are removed.

| ID | Role | IV → DV | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| B01 | limitation_harness | `log_zhvi_2022` → `fundraising_efficiency_w` | unspecified | negative | exploratory (no prior) | -7.91647 | 2.427e-22 | 0.1766 | 116,587 | ok |
| B02 | limitation_harness | `log_nonprofit_branch_density` → `fundraising_efficiency_w` | unspecified | positive | exploratory (no prior) | 2.11963 | 0.002447 | 0.1756 | 117,510 | ok |
| B03 | limitation_harness | `log_bank_branch_density` → `fundraising_efficiency_w` | unspecified | negative | exploratory (no prior) | -1.56054 | 0.0004427 | 0.1756 | 117,510 | ok |
| B04 | limitation_harness | `social_service_count` → `fundraising_efficiency_w` | unspecified | positive | exploratory (no prior) | 0.39450 | 0.005765 | 0.1756 | 117,510 | ok |
| B05 | limitation_harness | `population` → `fundraising_efficiency_w` | unspecified | negative | exploratory (no prior) | -0.00006 | 0.001325 | 0.1756 | 117,510 | ok |
| B06 | limitation_harness | `total_revenue` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | -0.00000 | 0.06292 | 0.1756 | 117,510 | ok |
| B07 | limitation_harness | `total_expenses` → `fundraising_efficiency_w` | unspecified | negative | exploratory (no prior) | -0.00000 | 0.04677 | 0.1757 | 117,510 | ok |

---
*Generated: 2026-07-12 10:37:47 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 08_unrolled_loop.py v2.1 (2026-07-12)*

```

## Source: Two-variable limitation (excerpt)

```
# Two-Variable Correlation Limitation (Phase 2 Evaluation)

**Important:** Limitation is *not* proven by “few significant p-values.”
With n ≈ 100k+, tiny coefficients routinely clear p < 0.05. The professor’s point is that
2-variable tests on this frame are **easy to light up and hard to trust as research** —
mechanical hits, wrong-direction theory, and nearly indistinguishable full-model R².

This note collects that evidence and motivates Phase 3 (new indicators / higher-order /
finer data) without implementing Phase 3 yet.

## Why “11 of 12 significant” would be the wrong headline

An earlier draft of the List B harness included IVs that are **components of the DV**:

`fundraising_efficiency = total_contributions / fundraising_expense_proxy`

So `total_contributions`, `fundraising_expense_proxy`, event expenses, and professional fees
are mechanically related to the DV. Calling those “discoveries” inflates the significant count
and **looks like the opposite** of a limitation argument. The harness now excludes those mechanical IVs.

Even after that filter, p < 0.05 is still common. That is expected at this sample size —
and it is exactly why significance count alone cannot prove the method is “working well.”

## Bounded limitation harness summary (non-mechanical candidate IVs)

- Pairs executed successfully: **7**
- Significant at p < 0.05: **6**
- Not significant: **1**
- Model R² range across the harness: **0.1756 – 0.1766** (span ≈ 0.0010)

The full-model R² values are nearly identical across the harness. This is descriptive,
not a formal incremental-R² estimate: no controls-only model is reported, and
IV-specific missingness changes n (notably for ZHVI).

| ID | IV | β | p | R² | Significant? | Note |
|---|---|---|---|---|---|---|
| B01 | `log_zhvi_2022` | -7.91647 | 2.427e-22 | 0.1766 | True | external/structural candidate |
| B02 | `log_nonprofit_branch_density` | 2.11963 | 0.002447 | 0.1756 | True | external/structural candidate |
| B03 | `log_bank_branch_density` | -1.56054 | 0.0004427 | 0.1756 | True | external/structural candidate |
| B04 | `social_service_count` | 0.39450 | 0.005765 | 0.1756 | True | external/structural candidate |
| B05 | `population` | -0.00006 | 0.001325 | 0.1756 | True | tiny β; p cheap at large n |
| B06 | `total_revenue` | -0.00000 | 0.06292 | 0.1756 | False | org-scale accounting; weak theory for efficiency |
| B07 | `total_expenses` | -0.00000 | 0.04677 | 0.1757 | True | org-scale accounting; weak theory for efficiency |

## Evidence 1 — Mechanical / definitional hits (List A identity + DV recipe)

- **identity_revenue_expenses** (`total_expenses` → `total_revenue`): R² = **0.9875**, p = 0. Near-accounting identity — not a sociological discovery.
- **event_cost_drag** (`fundraising_events_direct_expenses` → `fundraising_efficiency_w`): significant (β = -0.00003, p = 1.336e-19) but the IV enters the **denominator** of fundraising efficiency. This is partly mechanical; keep it labeled, not as free discovery.

## 
```

## Source: Validation

```
# Phase 2 Validation Check (H4 & H5)

Compares unrolled-loop List A confirmatory rows to known baselines.

**PASS = beta REPRODUCTION** (coefficient matches baseline within tolerance).
It does NOT mean the theory was confirmed — H5 passes validation while its
competition theory is rejected (observed positive beta). See `list_a_results.md`
for per-hypothesis theory outcomes.

| Hypothesis | IV | Expected β | Loop β | |Δ| | Status |
|---|---|---|---|---|---|
| H4 | `log_zhvi_2022` | `-7.91647` | `-7.91647` | `0.000004` | **PASS** |
| H5 | `log_nonprofit_branch_density` | `2.11963` | `2.11963` | `0.000003` | **PASS** |

---
*Generated: 2026-07-12 10:37:47 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 08_unrolled_loop.py v2.1 (2026-07-12)*

```

---
*Generated: 2026-07-20 09:12:38 UTC · Phase2: `Checkpoint 3/loop_results_v2` · built_by: Phase3_MultiAgent · 09_phase3_agentic_loop.py v2.0 (Phase3 Multi-Agent / 2026-07-20)*
