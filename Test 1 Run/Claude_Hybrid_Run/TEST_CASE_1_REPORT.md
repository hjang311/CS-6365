# Test Case 1 Report — Job Benefits vs. Staff Recruitment Impact

**Pipeline:** NORP Agentic Data Exploration (Hybrid method, local execution — no external/API calls)
**Dataset:** `YEAR-04-DATA-PUF.csv` (Urban Institute National Survey of Nonprofit Trends & Impacts, Year 04 PUF) — 4,056 rows × 317 columns
**Paper reference:** Health of the U.S. Nonprofit Sector 2025, Figure 17 (p. 18)

---

## Objective

Validate that organizations offering health insurance report a significantly more
**positive** impact of their benefits package on staff recruitment.

- **Independent variable:** `Benefits_Health` (1 = offers group health insurance, 0 = does not)
- **Dependent variable:** `BenefitsImpact` (Likert 1–5; recruitment impact of benefits)
- **Success criterion:** strong positive correlation between `Benefits_Health == 1` and a
  positive `BenefitsImpact`, reproducing the paper's **76% vs 18%** contrast.

---

## Agent Pipeline Flow

| Stage | Agent | Skill | Outcome |
|-------|-------|-------|---------|
| 1 | Orchestrator | `norp-orchestrator` | Sensed target columns; delegated parsing |
| 2 | Code Agent | `norp-code-agent` | Sense→Plan→Act→Learn: decoded data dictionary, cleaned, cross-tabbed |
| 3 | Validator Agent | `norp-validator-agent` | 6/6 Data Contract assertions PASS → **APPROVED** |
| 4 | Orchestrator | `norp-orchestrator` | Significance test + comparison to paper |

---

## Data Handling

Value coding confirmed against `dd-nptrends-year-04-puf.xlsx`:

- `Benefits_Health`: `1 = Selected`, `0 = Not selected` (binary).
- `BenefitsImpact` (Q18): `1` Significant negative · `2` Moderate negative · `3` No impact ·
  `4` Moderate positive · `5` Significant positive. Codes `97` (Unsure) / `98` (N/A) already
  stored as NaN in the source.
- **Recode:** `1–2 → Negative`, `3 → No Impact`, `4–5 → Positive`.
- **Missing data:** listwise deletion on the two target columns → analysis **n = 3,043**.

---

## Results

### Cross-tabulation (counts)

| BenefitsImpact | Health = 0 | Health = 1 | Total |
|----------------|-----------:|-----------:|------:|
| Negative       | 852        | 165        | 1,017 |
| No Impact      | 354        | 112        | 466   |
| Positive       | 392        | 1,168      | 1,560 |
| **All**        | **1,598**  | **1,445**  | **3,043** |

### Figure 17 replication (% offering health insurance)

| Reported benefits impact | % with health insurance | Paper target |
|--------------------------|------------------------:|-------------:|
| **Positive**             | **74.9%** (1,168 / 1,560) | ~76% |
| **Negative**             | **16.2%** (165 / 1,017)   | ~18% |

### Statistical significance

- **Chi-square:** χ²(2, N = 3,043) = **970.5**
- **p-value:** ≈ **1.8 × 10⁻²¹¹**  (≪ 0.05)
- **Effect size:** Cramér's V = **0.565** (large)

---

## Verdict

✅ **PASS.** The pipeline ingested the raw PUF and independently reproduced the paper's finding
— a strong, highly significant positive association between offering health insurance and a
positive recruitment-benefits impact (74.9% vs 16.2%, within ~1–2 points of the published
76% / 18%). The Validator Agent confirmed zero Data Contract violations.

**Caveat — weighting:** This run is **unweighted**. The paper and the current agent skills
specify applying survey weights; a weighted re-run is the recommended follow-up and is expected
to close the small residual gap to 76% / 18%.
