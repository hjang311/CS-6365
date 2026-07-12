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
