# Phase 3 Round 81 Results

Pre-registered proposals: `Checkpoint 4/Grok_4.5/phase3_results/proposals_atlanta_xsection.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1783863607).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| AX01 | two_var | `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | 13.55748 | 0.576359 | 0.2371 | 211 | ok |
| AX02 | interaction | `poverty_rate` × `log_soup_kitchen_density` → `fundraising_efficiency_w` | negative | none | not significant | 1.58515 | 0.40495 | 0.2403 | 211 | ok |
| AX03 | two_var | `soup_kitchen_local_count` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 1.57421 | 0.401727 | 0.2389 | 211 | ok |
| AX04 | two_var | `log_meal_site_density` → `fundraising_efficiency_w` | negative | none | not significant | 0.54299 | 0.985104 | 0.2360 | 211 | ok |
| AX05 | two_var | `open_days_mean` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | -2.06854 | 0.745457 | 0.2362 | 211 | ok |

## Rationales

- **AX01:** July 10 alignment retest: finer-granularity soup-kitchen density per ZIP should capture local food-assistance presence better than HQ NTEE proxy; competition / crowding story predicts lower fundraising efficiency where density is higher.
- **AX02:** Higher-order July 10 spec: poverty may intensify the soup-kitchen density–efficiency link in ACFB-area ZIPs where need and site stock co-locate.
- **AX03:** Big vs local stretch: keyword-heuristic local site count (not official ACFB chain census) tests whether smaller operators associate differently with efficiency than aggregate density.
- **AX04:** Soup/meal/CFC-only density (excludes pantry-heavy stock) as a mission-narrower July 10 indicator; crowding story predicts negative association.
- **AX05:** Effectiveness-lite probe: mean open days per site (hours coverage proxy) may signal operational intensity without a strong directional prior on efficiency.

---
*Generated: 2026-07-12 13:40:09 UTC · Frame: `Checkpoint 4/Grok_4.5/data/cp4_atlanta_pilot_xsection.csv` (272 rows x 40 cols) · 09_phase3_agentic_loop.py v1.0 (Grok_4.5 / 2026-07-12) · built_by: Grok_4.5*
