# Phase 3 Round 2 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/proposals_round2.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784863506).

Higher-order specs use the TA Verifier gate: robust HC1 Wald F (p < 0.05) **and** ΔR² ≥ 0.0005 over main effects on identical rows (controls-only baseline also reported).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Gate | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F2P01 | two_var | `log_zhvi_2022` → `fundraising_efficiency_w` | negative | none | not significant | -30.60634 | 0.156028 | 0.2241 | 444 | — | ok |
| F2P02 | interaction | `log_zhvi_2022` × `log_bank_branch_density` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 61.80136 | 0.0781141 | 0.2369 | 444 | REJECT | ok |

## Rationales

- **F2P01:** Round 1 food-density nulls → adapt: re-test H4 housing-cost signal on the Atlanta × latest-year slice.
- **F2P02:** Higher-order adaptation: does bank sparsity moderate the ZHVI overhead effect on the Atlanta cross-section?
  - gate: **REJECT** — Added terms not jointly significant (robust F p=0.0789).
  - Wald F=3.103709643602143, p=0.07885213688679045; ΔR²(ho)=0.008018213007521702; R² full/main/ctrl=0.2369484295616634/0.2289302165541417/0.22117624629820465

---
*Generated: 2026-07-24 03:25:06 UTC · Frame: `Checkpoint 4/data/cp4_atlanta_food_assistance_xsection.csv` (583 rows x 33 cols) · 09_phase3_agentic_loop.py v2.1 (Phase3 Multi-Agent / 2026-07-21) · built_by: Phase3_MultiAgent*
