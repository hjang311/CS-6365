# H4 Verification Run — Spatial Mismatch & Fundraising Efficiency

## Objective
Following the architectural constraint to eliminate external API dependencies for iterative hypothesis testing, we instituted a **Dynamic Interactive Agent Engine**. This verification run (H4) serves two purposes:
1. **Architectural Verification:** Ensure the `03_hitl_hypothesis_engine.py` can execute locally without triggering `429 RESOURCE_EXHAUSTED` errors or incurring API costs by directly prompting the Antigravity Agent for hypotheses via standard input (`stdin`).
2. **Sociological Validation:** Test a highly novel hypothesis (Novelty Score: 5/5) regarding the spatial mismatch of real estate prices and nonprofit fundraising efficiency.

## Formal Hypothesis

**Hypothesis:** High local real estate prices (proxied by Zillow Home Value Index) increase overhead costs, reducing the fundraising efficiency of nonprofits located in those ZIP codes.

* **Independent Variable (IV):** `log_zhvi_2022` (Log of Zillow Home Value Index 2022)
* **Dependent Variable (DV):** `fundraising_efficiency_w` (Winsorized Fundraising Efficiency)
* **Rationale:** The spatial mismatch literature traditionally focuses on employment and housing, not nonprofit cost-efficiency. This is a highly novel application testing whether operating in high-cost ZIP codes intrinsically penalizes non-profit efficiency.
* **Key Citations:** Kain (1968), Bielefeld (2000), Harrison & Wolch (1998).

## Quantitative Findings

The offline Human-In-The-Loop (HITL) engine ran a deterministic, robust OLS regression (cov_type="HC1") on the `cp3_modeling_frame.csv` with the following control covariates: `log_total_revenue`, `C(ntee_major)`, `C(region)`, `poverty_rate`, and `median_hh_income`.

**Results Summary:**
- **Number of Observations (n):** 116,587
- **R-squared ($R^2$):** 0.1766
- **IV Coefficient (beta):** -7.91647
- **IV P-value:** 2.427e-22

**Interpretation:** There is a highly statistically significant ($p < 0.001$) negative association between local real estate prices and fundraising efficiency. For a 1-unit increase in the log of ZHVI, the winsorized fundraising efficiency decreases by approximately 7.92 units, assuming all other control variables are held constant. This provides strong preliminary evidence for the nonprofit spatial mismatch hypothesis.

## Agentic Engine & Hybrid Architecture Details

To address the limitations discovered during earlier phases (specifically the `429 RESOURCE_EXHAUSTED` errors when relying on high-frequency Google GenAI API calls):

1. **Interactive Prompt Pattern:** We removed the Google GenAI API dependencies. The Python scripts (`00_dataset_discovery_agent.py` and `03_hitl_hypothesis_engine.py`) now print explicit instructions to standard output when an LLM is required, and wait for standard input. 
2. **Antigravity Agent as the LLM:** When the user initiates a run, the Antigravity Agent executes the script, intercepts the prompt in the terminal, dynamically synthesizes the output (such as the JSON hypotheses array) using its unlimited local environment, and feeds the response back into the script via `stdin`.
3. **Reproducibility:** This dynamic approach guarantees that we get the full brainstorming intelligence of the agent on every run, but without relying on paid network APIs or static fallback files. The exact OLS mathematics remain deterministic and robust.

## Artifacts
- `H4_results.md` — The raw Markdown output produced by the HITL hypothesis engine during this verification run.
- `03_hitl_hypothesis_engine.py` — The refactored engine script that dynamically requests LLM inputs via the terminal.
