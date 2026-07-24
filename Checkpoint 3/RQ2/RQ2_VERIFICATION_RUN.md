# RQ2 Verification Run — Bank-Branch Density & Fundraising Efficiency

## Objective

RQ2 (CP2 H2) is the fintech-substitution / bank-sparsity hypothesis that was
confirmed on the national modeling frame and later **replayed** as List A
`H2_replay` in Checkpoint 3 Phase 2. This standalone write-up closes the CP3
Match gap: RQ4/RQ5 had dedicated verification docs; RQ2 did not.

## Formal Hypothesis

**Hypothesis:** Among nonprofits with revenue ≥ $500K, lower ZIP bank-branch
density is associated with higher fundraising efficiency (fintech-substitution
proxy: sparse bank presence → more digital fundraising relative to expense).

* **IV:** `bank_branch_density` (FDIC BankFind branches per ZIP population scale)
* **DV:** `fundraising_efficiency_w` (winsorized fundraising efficiency)
* **Expected direction:** negative

## Methodology & controls

Robust OLS (`cov_type="HC1"`) with the shared CP3 control set:

- `log_total_revenue`
- `C(ntee_major)`
- `C(region)`
- `poverty_rate`
- `median_hh_income`

## Quantitative findings

### Checkpoint 2 primary run (`H2_Pipeline/03_analysis.py`)

| Metric | Value |
|--------|-------|
| Modeling frame n (non-zero fundraising spend) | 147,718 |
| OLS β (IV) | −0.11453 |
| 95% CI | [−0.18593, −0.04313] |
| p | 0.001667 |
| R² | 0.1903 |
| Mid ($500K–$2M) β | −0.08145 (p=0.000127) |
| Large (≥$2M) β | −0.15211 (p=0.004687) |

Source: [`Checkpoint 2/H2_Pipeline/findings_results.md`](../../Checkpoint%202/H2_Pipeline/findings_results.md).

### Checkpoint 3 Phase 2 replay (List A `H2_replay`)

| Sample | n | β | p | R² | Outcome |
|--------|---|---|---|-----|---------|
| Full (shared CONTROLS) | 117,510 | −0.11560 | 0.001764 | 0.1756 | **confirmed** (expected negative) |

Source: [`loop_results_v2/list_a_results.md`](../loop_results_v2/list_a_results.md).

CP2 and CP3 betas agree within ~0.001 (recipe / frame-window differences).
Theory status: **confirmed** on both primary and replay runs.

## Artifacts

- `Checkpoint 2/H2_Pipeline/` — acquire, merge, analysis, plots, validator
- `Checkpoint 2/H2_Pipeline/plots/` — log-log scatter, size-split coefficients, diagnostics
- `Checkpoint 3/08_unrolled_loop.py` — List A row `H2_replay`
- `Checkpoint 3/loop_results_v2/list_a_results.md` — replay table

## Status

**PASS (theory confirmed)** — negative bank-density → efficiency association
holds under the shared control recipe. This document is the standalone RQ2
verification companion to `H4/H4_VERIFICATION_RUN.md` and `H5/H5_VERIFICATION_RUN.md`.
