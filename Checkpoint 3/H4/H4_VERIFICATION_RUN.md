# H4 Verification Run — Spatial Mismatch & Fundraising Efficiency

## Objective
Following the architectural constraint to eliminate external API dependencies for iterative hypothesis testing, we instituted an **offline-resilient hybrid engine**. This verification run (H4) serves two purposes:
1. **Architectural Verification:** Ensure the `03_hitl_hypothesis_engine.py` can execute locally without triggering 429 RESOURCE_EXHAUSTED errors or incurring API costs by reading offline-generated baseline schemas.
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

To address the limitations discovered during earlier phases (specifically the `429 RESOURCE_EXHAUSTED` errors when relying on high-frequency API calls for LLM brainstorming):

1. **Local Fallback Schema:** The engine was refactored to read from a local JSON payload (`data/hypotheses.json`) populated by the agent. This decoupling means the agent acts as an offline "brain" that stages the sociological logic, rather than an active dependency during the regression execution phase.
2. **Offline Resilience:** The orchestrator successfully called the regression tools (`run_ols`) strictly through local Python logic. The prompt templates and constraints defined in the `.agent/skills/` directory ensured the outputs adhered to the required deterministic structure.
3. **Reproducibility:** This hybrid approach guarantees that the exact same hypothesis and control variables can be re-run indefinitely without requiring API quotas, fulfilling the requirement for a fully autonomous yet stable pipeline.

## Artifacts
- `H4_results.md` — The raw Markdown output produced by the offline HITL hypothesis engine during this verification run.
- `03_hitl_hypothesis_engine.py` — The refactored local engine script.
- `data/hypotheses.json` — The offline baseline fallback used by the engine.
