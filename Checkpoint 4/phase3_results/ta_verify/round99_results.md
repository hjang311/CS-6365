# Phase 3 Round 99 Results

Pre-registered proposals: `Checkpoint 4/phase3_results/ta_verify/proposals_ta_verify.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1784863482).

Higher-order specs use the TA Verifier gate: robust HC1 Wald F (p < 0.05) **and** ΔR² ≥ 0.0005 over main effects on identical rows (controls-only baseline also reported).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Gate | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| I1 | interaction | `log_zhvi_2022` × `log_nonprofit_branch_density` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | -0.49910 | 0.588083 | 0.1767 | 116587 | REJECT | ok |
| I2 | interaction | `log_zhvi_2022` × `log_bank_branch_density` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 0.16583 | 0.784593 | 0.1767 | 116587 | REJECT | ok |
| I3 | interaction | `log_zhvi_2022` × `size_segment` → `fundraising_efficiency_w` | unspecified | positive | exploratory (no prior) | 11.47542 | 9.83594e-43 | 0.1781 | 116586 | ACCEPT | ok |
| I4 | interaction | `log_nonprofit_branch_density` × `size_segment` → `fundraising_efficiency_w` | unspecified | negative | exploratory (no prior) | -5.10975 | 1.85266e-05 | 0.1761 | 117509 | REJECT | ok |
| Q1 | quadratic | `log_zhvi_2022` + `I(log_zhvi_2022**2)` → `fundraising_efficiency_w` | unspecified | none | exploratory (no prior) | 0.39319 | 0.433456 | 0.1766 | 116587 | REJECT | ok |

## Rationales

- **I1:** Does the H4 housing-cost penalty depend on provider-field density (H5)?
  - gate: **REJECT** — Added terms not jointly significant (robust F p=0.588).
  - Wald F=0.2933479363054665, p=0.5880840740339656; ΔR²(ho)=2.53871839728248e-06; R² full/main/ctrl=0.17669269894951434/0.17669016023111705/0.17593367323960063
- **I2:** Whether bank sparsity moderates the real-estate overhead effect.
  - gate: **REJECT** — Added terms not jointly significant (robust F p=0.785).
  - Wald F=0.07471377551241909, p=0.78459373238143; ΔR²(ho)=5.557185456250835e-07; R² full/main/ctrl=0.1766700931491092/0.17666953743056357/0.17593367323960063
- **I3:** CP3 size split: large orgs more ZHVI-sensitive than mid.
  - gate: **ACCEPT** — Added terms jointly significant (robust F p=1.06e-42) and add delta_R2=0.0012 over main effects.
  - Wald F=187.75300873141921, p=1.0616168100344125e-42; ΔR²(ho)=0.0011540973425441248; R² full/main/ctrl=0.17814258380278913/0.176988486460245/0.17593153261251138
- **I4:** Whether agglomeration (H5) strengthens with org size.
  - gate: **REJECT** — Statistically significant (p=1.85e-05) but delta_R2=0.0001 < 0.0005 — large-n significance without real explanatory gain (the Phase 2 limitation, re-detected).
  - Wald F=18.33506343770389, p=1.8541253836215215e-05; ΔR²(ho)=0.00010563922281536797; R² full/main/ctrl=0.17606236435411793/0.17595672513130256/0.17550305605268646
- **Q1:** Whether the housing-cost penalty accelerates (non-linear).
  - gate: **REJECT** — Added terms not jointly significant (robust F p=0.433).
  - Wald F=0.6135463198164344, p=0.4334572656374638; ΔR²(ho)=4.570584675733791e-06; R² full/main/ctrl=0.17662416363542532/0.1766195930507496/0.17593367323960063

---
*Generated: 2026-07-24 03:24:42 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 09_phase3_agentic_loop.py v2.1 (Phase3 Multi-Agent / 2026-07-21) · built_by: Phase3_MultiAgent*
