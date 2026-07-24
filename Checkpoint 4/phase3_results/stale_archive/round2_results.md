# Phase 3 Round 2 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/proposals_round2.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784538739).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| R2P01 | two_var | `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative |  |  |  |  |  |  | error |
| R2P02 | interaction | `poverty_rate` × `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative |  |  |  |  |  |  | error |
| R2P03 | two_var | `soup_kitchen_local_count` → `fundraising_efficiency_w` | unspecified |  |  |  |  |  |  | error |

## Rationales

- **R2P01:** Phase 3 finer-granularity track: Feed America–scaled / ACFB-area food-assistance density per 10k (not IRS HQ NTEE proxy).
  - note: missing columns: ['log_soup_kitchen_density']
- **R2P02:** Higher-order: poverty may intensify the soup-kitchen / pantry density association on the expanded ZIP coverage.
  - note: missing columns: ['log_soup_kitchen_density']
- **R2P03:** Exploratory big-vs-local stretch: count of local-classified sites per ZIP from merged soup_kitchens.csv.
  - note: missing columns: ['soup_kitchen_local_count']

---
*Generated: 2026-07-20 09:12:19 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 09_phase3_agentic_loop.py v2.0 (Phase3 Multi-Agent / 2026-07-20) · built_by: Phase3_MultiAgent*
