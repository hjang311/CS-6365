# Phase 3 Round 1 Results

Pre-registered proposals: `Checkpoint 4/Grok_4.5/phase3_results/proposals_round1.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1783863133).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| P01 | two_var | `log_bank_branch_density` → `fundraising_efficiency_w` | negative | negative | confirmed | -1.56054 | 0.00044273 | 0.1756 | 117510 | ok |
| P02 | interaction | `poverty_rate` × `log_nonprofit_branch_density` → `fundraising_efficiency_w` | negative | none | not significant | -0.08716 | 0.18555 | 0.1756 | 117510 | ok |
| P03 | two_var | `population` → `fundraising_efficiency_w` | unspecified | negative | exploratory (no prior) | -0.00006 | 0.00132522 | 0.1756 | 117510 | ok |

## Rationales

- **P01:** Phase 2 H2_replay confirmed negative bank density → efficiency; re-test as a Phase 3 agenda item with explicit prior.
- **P02:** Higher-order: poverty may moderate the provider-density link that rejected H5's competition story in Phase 2.
- **P03:** Phase 2 weak_population case: large-n makes tiny β look significant; re-run as exploratory to keep the limitation thesis visible in Phase 3.

---
*Generated: 2026-07-12 13:32:14 UTC · Frame: `Checkpoint 4/Grok_4.5/data/cp4_frame_with_soup_density.csv` (158,323 rows x 35 cols) · 09_phase3_agentic_loop.py v1.0 (Grok_4.5 / 2026-07-12) · built_by: Grok_4.5*
