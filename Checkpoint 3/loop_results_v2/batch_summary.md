# Phase 2 Unrolled Loop — Batch Summary

All List A hypotheses + List B limitation-harness rows executed by `08_unrolled_loop.py`.

| List | ID | IV | DV | β | p | R² | n | Sig | Status |
|---|---|---|---|---|---|---|---|---|---|
| A | H4 | `log_zhvi_2022` | `fundraising_efficiency_w` | -7.91647 | 2.427e-22 | 0.1766 | 116,587 | True | ok |
| A | H5 | `log_nonprofit_branch_density` | `fundraising_efficiency_w` | 2.11963 | 0.002447 | 0.1756 | 117,510 | True | ok |
| A | H2_replay | `bank_branch_density` | `fundraising_efficiency_w` | -0.11560 | 0.001764 | 0.1756 | 117,510 | True | ok |
| A | event_cost_drag | `fundraising_events_direct_expenses` | `fundraising_efficiency_w` | -0.00003 | 1.336e-19 | 0.1919 | 117,510 | True | ok |
| A | affluence_clustering | `log_zhvi_2022` | `log_nonprofit_branch_density` | 0.06781 | 1.692e-65 | 0.0748 | 116,587 | True | ok |
| A | identity_revenue_expenses | `total_expenses` | `total_revenue` | 1.03207 | 0 | 0.9875 | 117,510 | True | ok |
| A | weak_population | `population` | `fundraising_efficiency_w` | -0.00006 | 0.001325 | 0.1756 | 117,510 | True | ok |
| B | B01 | `log_zhvi_2022` | `fundraising_efficiency_w` | -7.91647 | 2.427e-22 | 0.1766 | 116,587 | True | ok |
| B | B02 | `log_nonprofit_branch_density` | `fundraising_efficiency_w` | 2.11963 | 0.002447 | 0.1756 | 117,510 | True | ok |
| B | B03 | `log_bank_branch_density` | `fundraising_efficiency_w` | -1.56054 | 0.0004427 | 0.1756 | 117,510 | True | ok |
| B | B04 | `social_service_count` | `fundraising_efficiency_w` | 0.39450 | 0.005765 | 0.1756 | 117,510 | True | ok |
| B | B05 | `population` | `fundraising_efficiency_w` | -0.00006 | 0.001325 | 0.1756 | 117,510 | True | ok |
| B | B06 | `total_revenue` | `fundraising_efficiency_w` | -0.00000 | 0.06292 | 0.1756 | 117,510 | False | ok |
| B | B07 | `total_expenses` | `fundraising_efficiency_w` | -0.00000 | 0.04677 | 0.1757 | 117,510 | True | ok |

---
*Generated: 2026-07-12 10:37:47 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 08_unrolled_loop.py v2.1 (2026-07-12)*
