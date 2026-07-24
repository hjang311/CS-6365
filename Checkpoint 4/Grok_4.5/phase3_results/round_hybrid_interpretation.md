# Phase 3 Hybrid Round Interpretation

Source: **hybrid** (Grok_4.5 orchestrator) · Results: `round_hybrid_results.md`

## Summary

Hybrid Round 1 pre-registered five proposals (H01–H05) before OLS. All five ran successfully (`status: ok`). Outcomes are scored by sign + significance vs `expected_direction`; coefficients are taken only from the runner output.

| ID | Spec | Expected | Observed | Outcome |
|---|---|---|---|---|
| H01 | `log_zhvi_2022` → DV | negative | negative | **confirmed** |
| H02 | `log_bank_branch_density` → DV | negative | negative | **confirmed** |
| H03 | `log_nonprofit_branch_density` → DV | negative | positive | **rejected** (opposite) |
| H04 | `log_zhvi_2022` × `log_nonprofit_branch_density` → DV | negative | none (p = 0.588) | **not significant** |
| H05 | `social_service_count` → DV | unspecified | positive | **exploratory** (no prior) |

## Observed vs expected

### H01 — ZHVI anchor (H4 replay)

**Expected:** negative (affluence reduces fundraising efficiency). **Observed:** negative, highly significant (β = -7.91647, p ≈ 2.43e-22, R² = 0.1766, n = 116,587). **Verdict:** Confirmed — identical to Phase 2 H4 / List B B01. The housing-wealth signal survives full socioeconomic controls and remains the strongest structural IV in this round.

### H02 — Bank branch density (H2 replay)

**Expected:** negative (financial infrastructure eases fundraising). **Observed:** negative, significant (β = -1.56054, p ≈ 4.43e-4, R² = 0.1756, n = 117,510). **Verdict:** Confirmed — consistent with Phase 2 H2_replay. External financial-infrastructure IV behaves as theory predicts under controls.

### H03 — Nonprofit branch density (H5 replay with controls)

**Expected:** negative (competition story). **Observed:** positive, significant (β = 2.11963, p ≈ 0.00245, R² = 0.1756, n = 117,510). **Verdict:** Rejected — the wrong-direction result from Phase 2 H5 persists even with poverty_rate, median_hh_income, revenue, NTEE, and region in the model. Controls do not rescue the competition hypothesis; density still associates with *higher* efficiency, opposite theory.

### H04 — Affluence × density interaction

**Expected:** negative interaction (high-ZHVI areas dampen the density–efficiency slope that failed H5). **Observed:** interaction β = -0.49910, p = 0.588, R² = 0.1767, n = 116,587 — not significant, observed direction labeled "none." **Verdict:** The higher-order moderation story is not supported at conventional thresholds. Affluence clustering alone does not explain H5's sign flip; the interaction term adds negligible incremental signal over main effects.

### H05 — Social service count (exploratory)

**Expected:** unspecified. **Observed:** positive, significant (β = 0.39450, p ≈ 0.00577, R² = 0.1756, n = 117,510). **Verdict:** Exploratory hit — mirrors List B B04. Without a directional prior this is descriptive, not confirmatory; it reinforces the Phase 2 limitation thesis that large-n specs with R² ≈ 0.176 are easy to light up.

## Cross-cutting patterns

1. **R² compression:** All specs cluster at R² ≈ 0.1756–0.1767 — the same near-flat full-model R² seen in the Phase 2 limitation harness. Significance does not imply meaningful explanatory gain.
2. **Theory-stable vs theory-unstable IVs:** H01 and H02 replicate cleanly; H03 remains theory-inconsistent despite identical control structure. The problem is substantive (wrong sign), not a bare 2-var artifact.
3. **Interaction null:** H04 was the deliberate Phase 3 higher-order test; its failure suggests the H5 anomaly is not simply "affluence moderates density" and motivates finer-granularity indicators rather than more pairwise interactions on the same frame.

## Round 2 recommendation

**Primary proposal:** `soup_kitchen_density` after the ACFB / Feeding America merge (`10_acquire_soup_kitchens.py` → `11_merge_soup_kitchen_density.py`). This is a finer-granularity, mission-adjacent external IV not yet on the modeling frame — directly aligned with the Phase 2 evaluation's third track (finer-granularity soup-kitchen density by ZIP).

**Secondary ideas (not yet on frame or under-tested):**
- Two-var `population` as a documented weak/large-n case (Phase 2 `weak_population`).
- Avoid re-proposing control-set columns (`poverty_rate`, `median_hh_income`, `log_total_revenue`) as lone two_var IVs.
- Avoid mechanical DV components (`total_contributions`, `fundraising_expense_proxy`, event/professional fees).

Round 2 should treat soup-kitchen density as the headline new indicator; if merged nationally, pair it with an interaction against `log_zhvi_2022` only if theory is stated before OLS.

---
*Written: 2026-07-12 · built_by: Grok_4.5 · source: hybrid · runner: 09_phase3_agentic_loop.py v1.0*
