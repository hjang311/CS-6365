# Phase 3 Round 1 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/housing_chicago/proposals_round1.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784863514).

Higher-order specs use the TA Verifier gate: robust HC1 Wald F (p < 0.05) **and** ΔR² ≥ 0.0005 over main effects on identical rows (controls-only baseline also reported).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Gate | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H01 | two_var | `log_housing_services_density` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 5.04243 | 0.447483 | 0.2822 | 403 | — | ok |
| H02 | interaction | `poverty_rate` × `log_housing_services_density` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 0.42692 | 0.766121 | 0.2823 | 403 | REJECT | ok |

## Rationales

- **H01:** Universality demo: Chicago-area housing-services NTEE density vs fundraising efficiency (exploratory).
- **H02:** Higher-order: poverty may moderate housing-provider density.
  - gate: **REJECT** — Added terms not jointly significant (robust F p=0.766).
  - Wald F=0.08847788223962343, p=0.7662859142322856; ΔR²(ho)=0.00012200215967927974; R² full/main/ctrl=0.28229021603882265/0.28216821387914337/0.27422094613474046

---
*Generated: 2026-07-24 03:25:13 UTC · Frame: `Checkpoint 4/data/cp4_chicago_housing_services_xsection.csv` (503 rows x 33 cols) · 09_phase3_agentic_loop.py v2.1 (Phase3 Multi-Agent / 2026-07-21) · built_by: Phase3_MultiAgent*
