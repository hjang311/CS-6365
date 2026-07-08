# H5 Verification Run — Social-Service Provider Density & Fundraising Efficiency

## Objective
Following the architectural constraint to eliminate external API dependencies for iterative hypothesis testing, we built a **Deterministic Agentic Loop** (implemented in `07_deterministic_loop.py`). This verification run (H5) serves two purposes:
1. **Architectural Verification:** Ensure the orchestrator-processor hybrid loop works correctly, reliably reproducing OLS regression metrics on the modeling frame.
2. **Sociological Validation:** Validate the social-service provider density hypothesis using the robust outlier-capped DV across multiple organization size segments.

## Formal Hypothesis

**Hypothesis:** Among nonprofits with annual revenue ≥ $500,000, a higher local density of mission-critical social-service providers (food banks, food programs, soup kitchens, and homeless/related shelters per 10,000 residents) is associated with **lower** fundraising efficiency, because a denser field of providers intensifies competition for the same local donor base, raising fundraising expense relative to contributions. The effect is expected to be **stronger among smaller ($500K–$2M) organizations** — which have shallower donor bases — than larger (≥$2M) ones.

* **Independent Variable (IV):** `log_nonprofit_branch_density` — log of social-service nonprofits per 10,000 residents (NTEE K30/K31/K35/L40/L41/P43, from IRS BMF, normalized by ACS ZIP population).
* **Dependent Variable (DV):** `fundraising_efficiency_w` — winsorized fundraising efficiency (total contributions ÷ fundraising-expense proxy, capped at the 99th percentile).
* **Controls:** `log_total_revenue`, `C(ntee_major)`, `C(region)`, `poverty_rate`, `median_hh_income`.
* **Key Citations:** Rose-Ackerman (1982), Weisbrod (1988), Thornton (2006).

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
| Full (>=$500K) | 117,510 | 2.11963 | 0.002447 | [0.7485, 3.4908] | 0.1756 |
| Mid ($500K-$2M) | 53,972 | 1.10692 | 0.004737 | [0.3388, 1.8751] | 0.0904 |
| Large (>=$2M) | 63,537 | 3.05552 | 0.009074 | [0.7603, 5.3507] | 0.0973 |

**Interpretation:**
The hypothesis is **rejected**. The data reveals a highly statistically significant ($p < 0.01$) **positive** association between social-service provider density and fundraising efficiency across all size segments. Rather than intense competition depressing efficiency, a higher density of mission-critical nonprofits in a ZIP code is correlated with *better* fundraising efficiency. This may suggest an agglomeration effect or a clustering around high-donor capital that offsets the competition. Furthermore, contrary to expectations, the positive effect is stronger for large organizations ($\beta = +3.06$) than mid-sized ones ($\beta = +1.11$).

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
