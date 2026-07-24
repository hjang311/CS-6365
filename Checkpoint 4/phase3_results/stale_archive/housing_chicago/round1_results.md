# Phase 3 Round 1 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/housing_chicago/proposals_round1.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784538772).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| H01 | two_var | `log_housing_services_density` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 5.04243 | 0.447483 | 0.2822 | 403 | ok |
| H02 | interaction | `poverty_rate` × `log_housing_services_density` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 0.42692 | 0.766121 | 0.2823 | 403 | ok |

## Rationales

- **H01:** Universality demo: Chicago-area housing-services NTEE density vs fundraising efficiency (exploratory).
- **H02:** Higher-order: poverty may moderate housing-provider density.

---
*Generated: 2026-07-20 09:12:52 UTC · Frame: `Checkpoint 4/data/cp4_chicago_housing_services_xsection.csv` (503 rows x 33 cols) · 09_phase3_agentic_loop.py v2.0 (Phase3 Multi-Agent / 2026-07-20) · built_by: Phase3_MultiAgent*
