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
