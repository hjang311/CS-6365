# Phase 3 Round 1 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/fixture_full_demo/proposals_round1.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784538764).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| P01 | two_var | `log_bank_branch_density` → `fundraising_efficiency_w` | negative | none | not significant | -17.86540 | 0.0979097 | 0.2268 | 444 | ok |
| P02 | interaction | `poverty_rate` × `log_nonprofit_branch_density` → `fundraising_efficiency_w` | negative | none | not significant | 1.33701 | 0.480097 | 0.2288 | 444 | ok |
| P03 | two_var | `population` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | -0.00012 | 0.54673 | 0.2215 | 444 | ok |

## Rationales

- **P01:** Phase 2 H2_replay confirmed negative bank density → efficiency; re-test as a Phase 3 agenda item with explicit prior.
- **P02:** Higher-order: poverty may moderate the provider-density link that rejected H5's competition story in Phase 2.
- **P03:** Phase 2 weak_population case: large-n makes tiny β look significant; re-run as exploratory to keep the limitation thesis visible in Phase 3.

---
*Generated: 2026-07-20 09:12:44 UTC · Frame: `Checkpoint 4/data/cp4_atlanta_food_assistance_xsection.csv` (583 rows x 33 cols) · 09_phase3_agentic_loop.py v2.0 (Phase3 Multi-Agent / 2026-07-20) · built_by: Phase3_MultiAgent*
