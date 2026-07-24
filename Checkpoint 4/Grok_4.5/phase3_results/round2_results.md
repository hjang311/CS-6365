# Phase 3 Round 2 Results

Pre-registered proposals: `Checkpoint 4/Grok_4.5/phase3_results/proposals_round2.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1783863138).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| R2P01 | two_var | `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | 1.29805 | 0.568244 | 0.1755 | 117510 | ok |
| R2P02 | interaction | `poverty_rate` × `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | -0.23477 | 0.338177 | 0.1755 | 117510 | ok |
| R2P03 | two_var | `soup_kitchen_local_count` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 0.27011 | 0.363185 | 0.1755 | 117510 | ok |

## Rationales

- **R2P01:** Phase 3 finer-granularity track: Feed America–scaled / ACFB-area food-assistance density per 10k (not IRS HQ NTEE proxy).
- **R2P02:** Higher-order: poverty may intensify the soup-kitchen / pantry density association on the expanded ZIP coverage.
- **R2P03:** Exploratory big-vs-local stretch: count of local-classified sites per ZIP from merged soup_kitchens.csv.

---
*Generated: 2026-07-12 13:32:18 UTC · Frame: `Checkpoint 4/Grok_4.5/data/cp4_frame_with_soup_density.csv` (158,323 rows x 35 cols) · 09_phase3_agentic_loop.py v1.0 (Grok_4.5 / 2026-07-12) · built_by: Grok_4.5*
