# Checkpoint 3 Executive Summary: Manual to Unrolled NORP Exploration Pipeline

## 1. Core Research Questions & Domain Focus

The **NORP (Nonprofit Organization Research Pipeline)** combines multi-source federal and sectoral datasets—joining NCCS CORE 990 filings (2018–2022, ~$158\text{K}$ organization-years), IRS Business Master File (BMF), FDIC BankFind, Census ACS5, and Zillow Home Value Index (ZHVI)—to investigate operational determinants of nonprofit fundraising efficiency (`fundraising_efficiency_w`).

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
|  - Automated data contract verification (04_validate_frame.py, 11 contracts)      |
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
1. **Data Contract Validation (`pipeline/04_validate_frame.py`):** Enforces 11 automated schema, range, and integrity contracts on the national frame before statistical estimation. All 11 contracts pass on the committed handoff frame ($N = 158,323$).
2. **Deterministic Pre-Registration:** Replaced early unconstrained combinatorial scanners with `08_unrolled_loop.py`. Hypotheses are defined in pre-registered JSON manifests before fitting OLS models.
3. **Control & Model Specification:** All models apply robust OLS with HC1 standard errors, controlling for organizational scale ($\log(\text{total\_revenue})$), sector ($\text{C(ntee\_major)}$), region ($\text{C(region)}$), poverty rate, and median household income.

---

## 3. Key Scientific Findings & Verifications

| Hypothesis | Independent Variable (IV) | Expected $\beta$ | Observed $\beta$ (Full Sample) | $p$-value | Full Model $R^2$ | Outcome / Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RQ4 (H4)** | $\log(\text{ZHVI})$ | Negative | **$-7.916$** | $2.4 \times 10^{-22}$ | $0.177$ | **CONFIRMED** |
| **RQ5 (H5)** | $\log(\text{provider\_density})$ | Negative | **$+2.120$** | $0.0024$ | $0.176$ | **REJECTED (Sign Flip)** |
| **RQ2 (Replay)** | $\log(\text{bank\_branch\_density})$ | Negative | **$-0.116$** | $< 0.01$ | $0.176$ | **CONFIRMED** |

### Statistical Breakdown by Size Tier:

*   **RQ4 / H4 (Real-Estate Overhead Pressure):**
    *   *Full Sample ($\ge \$500\text{K}$, $n=116,587$):* $\beta = -7.916$, $p = 2.4 \times 10^{-22}$, $R^2 = 0.177$
    *   *Mid-Sized ($500\text{K} - \$2\text{M}$, $n=53,650$):* $\beta = -2.995$, $p = 3.6 \times 10^{-11}$, $R^2 = 0.091$
    *   *Large ($\ge \$2\text{M}$, $n=62,936$):* $\beta = -11.534$, $p = 2.4 \times 10^{-16}$, $R^2 = 0.099$
    *   *Core Insight:* Supported. Higher real-estate costs significantly reduce fundraising efficiency across all groups. Large organizations experience a fourfold stronger negative impact ($\beta = -11.53$ vs $-3.00$), indicating that larger physical footprints and payrolls amplify market cost exposure.

*   **RQ5 / H5 (Provider Density & Donor Field):**
    *   *Full Sample ($\ge \$500\text{K}$, $n=117,510$):* $\beta = +2.120$, $p = 0.0024$, $R^2 = 0.176$
    *   *Mid-Sized ($500\text{K} - \$2\text{M}$, $n=53,972$):* $\beta = +1.107$, $p = 0.0047$, $R^2 = 0.090$
    *   *Large ($\ge \$2\text{M}$, $n=63,537$):* $\beta = +3.056$, $p = 0.0091$, $R^2 = 0.097$
    *   *Core Insight:* Rejected. Rather than donor cannibalization, the positive coefficient reveals an **agglomeration effect**—nonprofits cluster in geographic areas with concentrated donor capital and philanthropic infrastructure, out-weighing competitive crowding. Disconfirmation is reported as a first-class result.

*   **List B Limitation Harness Lessons:**
    *   Out of 7 non-mechanical candidate IVs scanned in List B, 6 achieved statistical significance ($p < 0.05$).
    *   However, overall model explanatory power remained virtually flat ($\Delta R^2 \approx 0.001$, spanning $0.1756 - 0.1766$).
    *   *Takeaway:* Large-$N$ datasets easily yield statistically significant 2-variable $p$-values that lack substantive explanatory power, highlighting the danger of unguided automated hypothesis scanning.

---

## 4. Transition to Phase 3 (Rolled Agentic Loop)

### Why Statistical Significance Alone is Insufficient
The Phase 2 List B experiments demonstrated that in large-sample observational frames ($N \approx 158\text{K}$), simple 2-variable regressions routinely "light up" with $p < 0.05$ without meaningfully improving model fit ($\Delta R^2 \approx 0.001$). Relying solely on $p$-values creates false positive discoveries and mechanical noise.

### Architectural Shift in Phase 3
Phase 3 transitions control of agenda proposal to an LLM agent while delegating statistical fitting to a deterministic verification engine:

1.  **Higher-Order & Multi-Variable Specifications:** The agent is required to propose interaction terms (e.g., $\text{ZHVI} \times \text{provider\_density}$) and non-linear specifications rather than single IV additions.
2.  **Finer Domain Granularity:** Shift from coarse county/NTEE counts to targeted indicators (e.g., licensed Feeding America / food pantry density).
3.  **Strict Verification Gates:** Proposed hypotheses must pass automated pre-registration, HC1 OLS estimation, Wald F-tests ($p < 0.05$), and a minimum effect threshold ($\Delta R^2 \ge 5 \times 10^{-4}$) before acceptance. Null and gate-rejected findings remain first-class artifacts in the pipeline's decision log.
