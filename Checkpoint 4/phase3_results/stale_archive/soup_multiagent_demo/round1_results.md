# Phase 3 Round 1 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/soup_multiagent_demo/proposals_round1.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784538982).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| F01 | two_var | `log_food_assistance_density` → `fundraising_efficiency_w` | negative | none | not significant | -21.46836 | 0.117555 | 0.2246 | 444 | ok |
| F02 | interaction | `poverty_rate` × `log_food_assistance_density` → `fundraising_efficiency_w` | negative | none | not significant | 0.39393 | 0.852988 | 0.2247 | 444 | ok |

## Rationales

- **F01:** Finer-granularity food-assistance density (NTEE or Feed America) vs fundraising efficiency on Atlanta cross-section.
- **F02:** Higher-order: poverty may intensify food-assistance density association.

---
*Generated: 2026-07-20 09:16:21 UTC · Frame: `Checkpoint 4/data/cp4_atlanta_food_assistance_xsection.csv` (583 rows x 33 cols) · 09_phase3_agentic_loop.py v2.0 (Phase3 Multi-Agent / 2026-07-20) · built_by: Phase3_MultiAgent*
