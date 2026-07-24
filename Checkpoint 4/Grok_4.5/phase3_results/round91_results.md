# Phase 3 Round 91 Results

Pre-registered proposals: `Checkpoint 4/Grok_4.5/phase3_results/proposals_round1_hybrid.json`
Proposals mtime precedes results write: **yes** (proposals_mtime=1783862971).

| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| H01 | two_var | `log_zhvi_2022` → `fundraising_efficiency_w` | negative | negative | confirmed | -7.91647 | 2.42671e-22 | 0.1766 | 116587 | ok |
| H02 | two_var | `log_bank_branch_density` → `fundraising_efficiency_w` | negative | negative | confirmed | -1.56054 | 0.00044273 | 0.1756 | 117510 | ok |
| H03 | two_var | `log_nonprofit_branch_density` → `fundraising_efficiency_w` | negative | positive | rejected (opposite or mismatch) | 2.11963 | 0.0024469 | 0.1756 | 117510 | ok |
| H04 | interaction | `log_zhvi_2022` × `log_nonprofit_branch_density` → `fundraising_efficiency_w` | negative | none | not significant | -0.49910 | 0.588083 | 0.1767 | 116587 | ok |
| H05 | two_var | `social_service_count` → `fundraising_efficiency_w` | unspecified | positive | exploratory (no prior) | 0.39450 | 0.00576507 | 0.1756 | 117510 | ok |

## Rationales

- **H01:** Phase 2 H4 confirmed negative ZHVI → efficiency (β ≈ -7.92); re-test under full controls as the anchor confirmatory spec for Phase 3.
- **H02:** Phase 2 H2_replay confirmed negative bank-branch density → efficiency; external financial-infrastructure IV not in CONTROLS.
- **H03:** Phase 2 H5 was significant but theory rejected (observed positive β); re-test with controls to see whether competition story holds once socioeconomic confounders are partialled out.
- **H04:** Affluence clustering (H4) may moderate the provider-density link that failed H5 in bare 2-var OLS; interaction tests whether high-ZHVI areas dampen the density–efficiency slope.
- **H05:** List B B04 lit up at large n (positive β, p < 0.01) with weak prior; exploratory external indicator to stress-test the 2-var limitation thesis under controls.

---
*Generated: 2026-07-12 13:29:35 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 09_phase3_agentic_loop.py v1.0 (Grok_4.5 / 2026-07-12) · built_by: Grok_4.5*
