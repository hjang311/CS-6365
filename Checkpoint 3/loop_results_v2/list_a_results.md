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
