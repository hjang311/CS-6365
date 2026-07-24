# Phase 3 Round 1 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/proposals_round1.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784863506).

Higher-order specs use the TA Verifier gate: robust HC1 Wald F (p < 0.05) **and** ΔR² ≥ 0.0005 over main effects on identical rows (controls-only baseline also reported).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Gate | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F01 | two_var | `log_food_assistance_density` → `fundraising_efficiency_w` | negative | none | not significant | -21.46836 | 0.117555 | 0.2246 | 444 | — | ok |
| F02 | interaction | `poverty_rate` × `log_food_assistance_density` → `fundraising_efficiency_w` | negative | none | not significant | 0.39393 | 0.852988 | 0.2247 | 444 | REJECT | ok |

## Rationales

- **F01:** Finer-granularity food-assistance density (NTEE or Feed America) vs fundraising efficiency on Atlanta cross-section.
- **F02:** Higher-order: poverty may intensify food-assistance density association.
  - gate: **REJECT** — Added terms not jointly significant (robust F p=0.853).
  - Wald F=0.03433898191908121, p=0.8530781490132895; ΔR²(ho)=8.081214846356044e-05; R² full/main/ctrl=0.22470654397836076/0.2246257318298972/0.21937666530077737

---
*Generated: 2026-07-24 03:25:06 UTC · Frame: `Checkpoint 4/data/cp4_atlanta_food_assistance_xsection.csv` (583 rows x 33 cols) · 09_phase3_agentic_loop.py v2.1 (Phase3 Multi-Agent / 2026-07-21) · built_by: Phase3_MultiAgent*
