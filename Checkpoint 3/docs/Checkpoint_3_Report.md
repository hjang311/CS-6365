# Checkpoint 3 Executive Summary: Manual to Unrolled NORP Exploration Pipeline

## 1. Core Research Questions & Domain Focus

The **NORP (Nonprofit Organization Research Pipeline)** combines multi-source federal and sectoral datasets—joining NCCS CORE 990 filings (2018–2022, ~158K organization-years), IRS Business Master File (BMF), FDIC BankFind, Census ACS5, and Zillow Home Value Index (ZHVI)—to investigate operational determinants of nonprofit fundraising efficiency (`fundraising_efficiency_w`).

Checkpoint 3 extended the core national modeling frame to evaluate two primary domain hypotheses:

*   **RQ4 / H4 — Local Real-Estate Costs (Spatial Mismatch Extension):** Grounded in spatial mismatch literature extended to nonprofit sector cost structures, testing whether higher local real-estate prices (measured by ZIP-level Zillow ZHVI) lower fundraising efficiency by inflating local operating overhead (rent, wages, facility maintenance).
*   **RQ5 / H5 — Local Social-Service Provider Density (Competition vs. Agglomeration):** Grounded in market density dynamics, testing whether higher local concentration of mission-critical social-service providers (food banks, soup kitchens, shelters per 10,000 residents) reduces fundraising efficiency due to intensified local donor competition.

---

## 2. Methodology & Progression

The project strictly adheres to the course's pedagogical **Manual $\rightarrow$ Unrolled $\rightarrow$ Rolled** progression model:

```
+-----------------------------------------------------------------------------------+
|  Phase 1: Manual Specialization                                                   |
|  - Human domain selection of indicators (ZHVI, IRS BMF provider counts)          |
|  - Automated data contract verification (pipeline/04_validate_frame.py)          |
|  - Hand-coded robust OLS models with size segmentation ($500K-$2M vs. ≥$2M)        |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|  Phase 2: Unrolled Deterministic Execution (08_unrolled_loop.py)                 |
|  - List A (Curated Theory Agenda): Pre-registered hypotheses & control baselines  |
|  - List B (2-Variable Limitation Harness): Pre-registered candidate IV scanner    |
|  - Prevents mid-run LLM drift / hallucination via strict JSON pre-registration    |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|  Phase 3: Rolled Agentic Loop (Done in Checkpoint 4)                              |
|  - Autonomous proposal by LLM agent after reviewing Phase 2 findings              |
|  - Strict OLS verification gate (HC1 standard errors, Wald F, ΔR² thresholds)     |
+-----------------------------------------------------------------------------------+
```

### Key Technical Implementation Details:
1. **Data Contract Validation (`pipeline/04_validate_frame.py`):** Enforces 11 automated schema, range, and integrity contracts on the national frame before statistical estimation. All 11 contracts pass on the committed handoff frame (N = 158,323).
2. **Deterministic Pre-Registration:** Replaced early unconstrained combinatorial scanners with `08_unrolled_loop.py`. Hypotheses are defined in pre-registered JSON manifests before fitting OLS models.
3. **Control & Model Specification:** All models apply robust OLS with HC1 standard errors, controlling for organizational scale (`log(total_revenue)`), sector (`C(ntee_major)`), region (`C(region)`), poverty rate, and median household income.

---

## 3. Key Scientific Findings & Verifications

| Hypothesis | Independent Variable (IV) | Expected β | Observed β (Full Sample) | p-value | Full Model R² | Outcome / Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RQ4 (H4)** | `log(ZHVI)` | Negative | **-7.916** | `2.4e-22` | `0.177` | **CONFIRMED** |
| **RQ5 (H5)** | `log(provider_density)` | Negative | **+2.120** | `0.0024` | `0.176` | **REJECTED (Sign Flip)** |
| **RQ2 (Replay)** | `log(bank_branch_density)` | Negative | **-0.116** | `p < 0.01` | `0.176` | **CONFIRMED** |

### Statistical Breakdown by Size Tier:

*   **RQ4 / H4 (Real-Estate Overhead Pressure):**
    *   *Full Sample (≥ $500K, n=116,587):* β = -7.916, `p = 2.4e-22`, R² = 0.177
    *   *Mid-Sized ($500K to $2M, n=53,650):* β = -2.995, `p = 3.6e-11`, R² = 0.091
    *   *Large (≥ $2M, n=62,936):* β = -11.534, `p = 2.4e-16`, R² = 0.099
    *   *Core Insight:* Supported. Higher real-estate costs significantly reduce fundraising efficiency across all groups. Large organizations experience a fourfold stronger negative impact (β = -11.53 vs -3.00), indicating that larger physical footprints and payrolls amplify market cost exposure.

*   **RQ5 / H5 (Provider Density & Donor Field):**
    *   *Full Sample (≥ $500K, n=117,510):* β = +2.120, `p = 0.0024`, R² = 0.176
    *   *Mid-Sized ($500K to $2M, n=53,972):* β = +1.107, `p = 0.0047`, R² = 0.090
    *   *Large (≥ $2M, n=63,537):* β = +3.056, `p = 0.0091`, R² = 0.097
    *   *Core Insight:* Rejected. Rather than donor cannibalization, the positive coefficient reveals an **agglomeration effect**—nonprofits cluster in geographic areas with concentrated donor capital and philanthropic infrastructure, out-weighing competitive crowding. Disconfirmation is reported as a first-class result.

*   **List B Limitation Harness Lessons:**
    *   Out of 7 non-mechanical candidate IVs scanned in List B, 6 achieved statistical significance (`p < 0.05`).
    *   However, overall model explanatory power remained virtually flat (ΔR² ≈ 0.001, spanning 0.1756 - 0.1766).
    *   *Takeaway:* Large-N datasets easily yield statistically significant 2-variable p-values that lack substantive explanatory power, highlighting the danger of unguided automated hypothesis scanning.

---

## 4. Transition to Phase 3 (Rolled Agentic Loop)

### Why Statistical Significance Alone is Insufficient
The Phase 2 List B experiments demonstrated that in large-sample observational frames (N ≈ 158K), simple 2-variable regressions routinely "light up" with `p < 0.05` without meaningfully improving model fit (ΔR² ≈ 0.001). Relying solely on p-values creates false positive discoveries and mechanical noise.

### Architectural Shift in Phase 3
Phase 3 transitions control of agenda proposal to an LLM agent while delegating statistical fitting to a deterministic verification engine:

1.  **Higher-Order & Multi-Variable Specifications:** The agent is required to propose interaction terms (e.g. `ZHVI * provider_density`) and non-linear specifications rather than single IV additions.
2.  **Finer Domain Granularity:** Shift from coarse county/NTEE counts to targeted indicators (e.g., licensed Feeding America / food pantry density).
3.  **Strict Verification Gates:** Proposed hypotheses must pass automated pre-registration, HC1 OLS estimation, Wald F-tests (`p < 0.05`), and a minimum effect threshold (ΔR² ≥ 5e-4) before acceptance. Null and gate-rejected findings remain first-class artifacts in the pipeline's decision log.
