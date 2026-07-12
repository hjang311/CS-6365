# Two-Variable Correlation Limitation (Phase 2 Evaluation)

**Important:** Limitation is *not* proven by “few significant p-values.”
With n ≈ 100k+, tiny coefficients routinely clear p < 0.05. The professor’s point is that
2-variable tests on this frame are **easy to light up and hard to trust as research** —
mechanical hits, wrong-direction theory, and nearly indistinguishable full-model R².

This note collects that evidence and motivates Phase 3 (new indicators / higher-order /
finer data) without implementing Phase 3 yet.

## Why “11 of 12 significant” would be the wrong headline

An earlier draft of the List B harness included IVs that are **components of the DV**:

`fundraising_efficiency = total_contributions / fundraising_expense_proxy`

So `total_contributions`, `fundraising_expense_proxy`, event expenses, and professional fees
are mechanically related to the DV. Calling those “discoveries” inflates the significant count
and **looks like the opposite** of a limitation argument. The harness now excludes those mechanical IVs.

Even after that filter, p < 0.05 is still common. That is expected at this sample size —
and it is exactly why significance count alone cannot prove the method is “working well.”

## Bounded limitation harness summary (non-mechanical candidate IVs)

- Pairs executed successfully: **7**
- Significant at p < 0.05: **6**
- Not significant: **1**
- Model R² range across the harness: **0.1756 – 0.1766** (span ≈ 0.0010)

The full-model R² values are nearly identical across the harness. This is descriptive,
not a formal incremental-R² estimate: no controls-only model is reported, and
IV-specific missingness changes n (notably for ZHVI).

| ID | IV | β | p | R² | Significant? | Note |
|---|---|---|---|---|---|---|
| B01 | `log_zhvi_2022` | -7.91647 | 2.427e-22 | 0.1766 | True | external/structural candidate |
| B02 | `log_nonprofit_branch_density` | 2.11963 | 0.002447 | 0.1756 | True | external/structural candidate |
| B03 | `log_bank_branch_density` | -1.56054 | 0.0004427 | 0.1756 | True | external/structural candidate |
| B04 | `social_service_count` | 0.39450 | 0.005765 | 0.1756 | True | external/structural candidate |
| B05 | `population` | -0.00006 | 0.001325 | 0.1756 | True | tiny β; p cheap at large n |
| B06 | `total_revenue` | -0.00000 | 0.06292 | 0.1756 | False | org-scale accounting; weak theory for efficiency |
| B07 | `total_expenses` | -0.00000 | 0.04677 | 0.1757 | True | org-scale accounting; weak theory for efficiency |

## Evidence 1 — Mechanical / definitional hits (List A identity + DV recipe)

- **identity_revenue_expenses** (`total_expenses` → `total_revenue`): R² = **0.9875**, p = 0. Near-accounting identity — not a sociological discovery.
- **event_cost_drag** (`fundraising_events_direct_expenses` → `fundraising_efficiency_w`): significant (β = -0.00003, p = 1.336e-19) but the IV enters the **denominator** of fundraising efficiency. This is partly mechanical; keep it labeled, not as free discovery.

## Evidence 2 — Significance ≠ correct theory (H5)

- **H4**: expected negative, observed negative → **confirmed** (β = -7.91647, p = 2.427e-22).
- **H5**: expected negative, observed positive → **rejected (opposite or mismatch)** (β = 2.11963, p = 0.002447).
- H5 is statistically significant **and** rejects the pre-registered competition story (positive agglomeration instead). A 2-var scanner that only counts p < 0.05 would call this a win.

## Evidence 3 — Large-n makes tiny effects “significant”

- **weak_population** (`population` → `fundraising_efficiency_w`): β = -0.00006, p = 0.001325, R² = 0.1756.
  The coefficient is economically tiny; with n > 100k it still clears p < 0.05. That shows how weak the “significant count” metric is for research quality.

## Evidence 4 — The frame is not a causal panel design

- The frame pools 2018–2022 organization-year rows; repeated organizations are not independent observations.
- The Phase 2 model has no tax-year fixed effects.
- HC1 robust errors are not clustered by EIN or ZIP.
- ACS controls and the December 2022 ZHVI snapshot are coarser in time and space than annual 990 records.
- IRS headquarters ZIP may not represent every location where a nonprofit delivers services.

These are intentional Phase 2 boundaries, not claims that the current coefficients are causal estimates.
The professor's July 10 guidance was to document the two-variable limitation rather than over-refine it here.

## Conclusion (what “2-var is limited” actually means)

1. The unrolled loop can **faithfully replay** Phase 1 confirmatory tests (H4/H5).
2. **Do not** argue limitation via “few significant results” — at this n, significance is cheap.
3. Argue limitation via: mechanical DV-component hits, near-identity R²≈0.99, wrong-direction theory (H5), near-identical full-model R², pooled organization-years, unclustered HC1 errors, and coarse ZIP/year granularity.
4. Therefore bivariate OLS on the current 990/ACS/ZHVI frame is a **useful Phase 2 harness**, not a finished research engine. Phase 3 should evaluate which links are *theoretically* meaningful, propose additional indicators, and (stretch) pursue finer-granularity data (e.g. soup-kitchen density by ZIP) or higher-order structure.

*Phase 3 is intentionally not implemented in this deliverable.*


---
*Generated: 2026-07-12 10:37:47 UTC · Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 rows x 30 cols) · 08_unrolled_loop.py v2.1 (2026-07-12)*
