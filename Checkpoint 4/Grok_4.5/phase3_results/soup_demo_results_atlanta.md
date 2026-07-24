# Phase 3 Round 98 Results

Pre-registered proposals: `Checkpoint 4/Grok_4.5/phase3_results/proposals_soup_demo.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1783862575).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | two_var | `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | 19.35194 | 0.293383 | 0.1869 | 949 | ok |
| S02 | interaction | `poverty_rate` × `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | -0.54618 | 0.869803 | 0.1869 | 949 | ok |

## Rationales

- **S01:** Finer-granularity ACFB pilot density should capture local food assistance presence better than IRS HQ NTEE proxy; competition story predicts negative association with fundraising efficiency.
- **S02:** Higher-order: poverty may intensify the soup-kitchen density link on the Atlanta-aware frame.

---
*Generated: 2026-07-12 13:23:36 UTC · Frame: `Checkpoint 4/Grok_4.5/data/cp4_atlanta_subsample.csv` (1,264 rows x 35 cols) · 09_phase3_agentic_loop.py v1.0 (Grok_4.5 / 2026-07-12) · built_by: Grok_4.5*
