# H4 Verification Run — Spatial Mismatch & Fundraising Efficiency

## Objective
Following the architectural constraint to eliminate external API dependencies for iterative hypothesis testing, we built a **Deterministic Agentic Loop** (implemented in `07_deterministic_loop.py`). This verification run (H4) serves two purposes:
1. **Architectural Verification:** Ensure the orchestrator-processor hybrid loop works correctly, reliably reproducing OLS regression metrics on the modeling frame.
2. **Sociological Validation:** Validate the nonprofit spatial mismatch hypothesis using the robust outlier-capped DV across multiple organization size segments.

## Formal Hypothesis

**Hypothesis:** High local real estate prices (proxied by Zillow Home Value Index) increase overhead costs, reducing the fundraising efficiency of nonprofits located in those ZIP codes.

* **Independent Variable (IV):** `log_zhvi_2022` (Log of Zillow Home Value Index 2022)
* **Dependent Variable (DV):** `fundraising_efficiency_w` (Winsorized Fundraising Efficiency)
* **Rationale:** Higher local real estate prices increase operational and spatial overhead (rent, salary costs, logistics), which decreases the ratio of contributions secured relative to total fundraising expenses.
* **Key Citations:** Kain (1968), Bielefeld (2000), Harrison & Wolch (1998).

## Methodology & Control Set
We run a robust OLS regression (cov_type="HC1") on the `cp3_modeling_frame.csv` using the following control covariates:
- `log_total_revenue` (to control for organization scale)
- `C(ntee_major)` (to control for major nonprofit sectors)
- `C(region)` (to control for geographic macro-regions)
- `poverty_rate` (local socioeconomic demand control)
- `median_hh_income` (local donor capacity control)

The analysis is performed on:
1. **Full Sample** (Revenue >= $500,000)
2. **Mid-sized Nonprofits** (Revenue between $500,000 and $2,000,000)
3. **Large Nonprofits** (Revenue >= $2,000,000)

## Quantitative Findings

| Sample | n | IV coefficient (beta) | p-value | 95% CI | R-squared |
|---|---|---|---|---|---|
| Full (>=$500K) | 116,587 | -7.91647 | 2.427e-22 | [-9.5124, -6.3205] | 0.1766 |
| Mid ($500K-$2M) | 53,650 | -2.99536 | 3.615e-11 | [-3.8823, -2.1084] | 0.0912 |
| Large (>=$2M) | 62,936 | -11.53377 | 2.447e-16 | [-14.2913, -8.7762] | 0.0985 |

**Interpretation:**
There is a highly statistically significant ($p < 0.001$) negative association between local real estate prices and fundraising efficiency across all size segments. For the full sample, a 1-unit increase in the log of ZHVI decreases the winsorized fundraising efficiency by approximately 7.92 units. Notably, the penalty of operating in high-cost ZIP codes is much more severe for large organizations ($\beta = -11.53$) than for mid-sized organizations ($\beta = -3.00$). This provides strong evidence supporting the nonprofit spatial mismatch hypothesis.

## Deterministic Loop & Hybrid Architecture Details

To address the limitations of network API calls and rate-limiting issues (e.g., `429 RESOURCE_EXHAUSTED` errors):
1. **Orchestrator (Python):** `07_deterministic_loop.py` handles dataset subsetting, OLS regression execution, and result recording deterministically, ensuring mathematical precision and full reproducibility.
2. **Agentic Processor (LLM via stdin):** The Antigravity Agent acts as the sociological researcher. When prompted via standard output, the agent evaluates the variables and results, supplying hypotheses rationales and interpretations in a structured JSON payload fed back to standard input.
3. **Interactive vs. Batch Mode:**
   - `--interactive`: Evaluates the validation pairs (H4 & H5) step-by-step.
   - `--batch`: Systematically loops through all 215 combinatorial variable pairs, filtering out redundancy and prompting the agent to interpret only the statistically significant results ($p < 0.05$).

## Artifacts
- `07_deterministic_loop.py` — The core orchestrator-agent hybrid loop script.
- `loop_results/loop_summary.md` — Complete summary table of all tested combinatorial pairs.
- `loop_results/significant_findings.md` — Detailed write-up of the agent's interpretations and citations for all significant correlations.
- `loop_results/validation_check.md` — Automatic verification log confirming loop output matches these baseline results.
