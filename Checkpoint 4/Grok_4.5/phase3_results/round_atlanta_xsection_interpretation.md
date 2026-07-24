# Phase 3 Atlanta Cross-Section Interpretation (July 10 Alignment Retest)

Source: **hybrid** (Grok_4.5 orchestrator) · Results: `round_atlanta_xsection_results.md`  
Frame: `cp4_atlanta_pilot_xsection.csv` (272 rows; OLS nobs = 211 after listwise drop)

## Time & space caveats (from DATA_GRANULARITY_AUDIT.md)

- **Temporal mismatch:** Food-assistance site density is a **~2026 stock** joined to **tax_year = 2022** 990 org-years. ACS/ZHVI on the frame are also static multi-year estimates, not annual panels aligned to each filing year.
- **Spatial limitation:** 990s report **headquarters ZIP5**, not branch-level operations. Site density is aggregated to ZIP from street addresses; orgs may fundraise in ZIPs where they do not operate food sites.
- **Not official ACFB ~700:** Collection uses Feed America GA enrichment, curated public lists, and ACFB CFC pages — **not** a complete official ACFB partner census. Big vs local (`soup_kitchen_local_count`) is a keyword heuristic, not chain identification.
- **Pilot geography:** 44 pilot ZIPs (41 with ≥1 collected site); narrower than the full 29-county ACFB-area slice (583 rows in `cp4_atlanta_xsection.csv`).

These caveats bound any causal reading. This round tests whether finer-granularity indicators show signal under a **July 10–aligned** sample design (Atlanta-area × single tax year), not whether 2026 soup density caused 2022 efficiency.

## Summary

Five pre-registered proposals (AX01–AX05) ran successfully (`status: ok`). None reached conventional significance. Outcomes below use only runner-reported coefficients and p-values.

| ID | Spec | Expected | Observed | Outcome |
|---|---|---|---|---|
| AX01 | `log_soup_kitchen_density` → DV | negative | none (p = 0.576) | **not significant** |
| AX02 | `poverty_rate` × `log_soup_kitchen_density` → DV | negative | none (p = 0.405) | **not significant** |
| AX03 | `soup_kitchen_local_count` → DV | unspecified | none (p = 0.402) | **exploratory** (no prior) |
| AX04 | `log_meal_site_density` → DV | negative | none (p = 0.985) | **not significant** |
| AX05 | `open_days_mean` → DV | unspecified | none (p = 0.745) | **exploratory** (no prior) |

## Observed vs expected

### AX01 — Soup-kitchen density (July 10 headline IV)

**Expected:** negative (crowding / competition). **Observed:** β = 13.55748, p = 0.576, R² = 0.2371, n = 211 — not significant, observed direction labeled "none." **Verdict:** Theory not supported at this sample size and geography; the July 10 density idea does not replicate the national ZHVI/bank-branch signal on the pilot cross-section.

### AX02 — Poverty × soup density interaction

**Expected:** negative (need intensifies density link). **Observed:** interaction β = 1.58515, p = 0.405, R² = 0.2403, n = 211 — not significant. **Verdict:** Higher-order moderation null; poverty does not significantly reshape the soup-density slope in this pilot slice.

### AX03 — Local site count (big vs local stretch)

**Expected:** unspecified. **Observed:** β = 1.57421, p = 0.402, R² = 0.2389, n = 211 — exploratory, not significant. **Verdict:** No evidence that keyword-heuristic "local" counts associate with efficiency; big-vs-local comparison remains inconclusive pending better chain classification.

### AX04 — Meal-site density (soup/meal/CFC narrow)

**Expected:** negative. **Observed:** β = 0.54299, p = 0.985, R² = 0.2360, n = 211 — not significant. **Verdict:** Mission-narrower density does not improve signal over aggregate soup density; pantry-heavy stock exclusion does not rescue the crowding story here.

### AX05 — Open days mean (effectiveness lite)

**Expected:** unspecified. **Observed:** β = -2.06854, p = 0.745, R² = 0.2362, n = 211 — exploratory, not significant. **Verdict:** Hours-coverage proxy adds no detectable association with efficiency in this slice.

## Cross-cutting patterns

1. **R² modestly higher than national harness:** Specs cluster at R² ≈ 0.236–0.240 (vs ~0.176 nationally), consistent with a tighter geographic slice, but still far from explanatory dominance.
2. **All nulls:** Under July 10–aligned design, none of the food-assistance indicators reach p < 0.05. Temporal/spatial misalignment and incomplete ACFB coverage remain plausible confounds; alternatively, HQ-ZIP efficiency may be weakly linked to ZIP-level site stock.
3. **Loop mechanics validated:** Propose → pre-register → deterministic OLS → interpret pipeline completed on the intended cross-section without national multi-year pooling.

## Implications

- **Sample design improvement alone is insufficient** to generate significant soup-density signal on n ≈ 211 effective obs; full ACFB-area slice (round 82 fallback) or official partner export may be needed for power.
- **Continue documenting** time/space granularity limits in the final report; do not headline these coefficients as causal effects of 2026 food infrastructure on 2022 fundraising.
- **Big vs local** and **effectiveness-lite** probes (AX03, AX05) are appropriately exploratory until classification and hours data improve.

---
*Written: 2026-07-12 · built_by: Grok_4.5 · source: hybrid · runner: 09_phase3_agentic_loop.py v1.0 · round: 81*
