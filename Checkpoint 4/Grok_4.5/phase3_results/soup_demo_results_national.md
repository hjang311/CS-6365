# Phase 3 Round 99 Results

Pre-registered proposals: `Checkpoint 4/Grok_4.5/phase3_results/proposals_soup_demo.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1783862575).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | two_var | `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | 1.29805 | 0.568244 | 0.1755 | 117510 | ok |
| S02 | interaction | `poverty_rate` × `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | -0.23477 | 0.338177 | 0.1755 | 117510 | ok |

## Rationales

- **S01:** Finer-granularity ACFB pilot density should capture local food assistance presence better than IRS HQ NTEE proxy; competition story predicts negative association with fundraising efficiency.
- **S02:** Higher-order: poverty may intensify the soup-kitchen density link on the Atlanta-aware frame.

---
*Generated: 2026-07-12 13:32:23 UTC · Frame: `Checkpoint 4/Grok_4.5/data/cp4_frame_with_soup_density.csv` (158,323 rows x 35 cols) · 09_phase3_agentic_loop.py v1.0 (Grok_4.5 / 2026-07-12) · built_by: Grok_4.5*
