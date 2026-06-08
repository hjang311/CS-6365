# Test Case 1 — Job Benefits vs. Staff Recruitment Impact (Claude Hybrid Run)

Local execution of the NORP agentic pipeline (Hybrid method) on `YEAR-04-DATA-PUF.csv`.
No external/API calls. Agent "brains" loaded from `.agent/skills/*/SKILL.md`; sub-agents
spawned locally for the Code Agent and Validator Agent.

## Agent flow

| Stage | Agent | Skill loaded | Outcome |
|---|---|---|---|
| 1 | Orchestrator | norp-orchestrator | Sensed columns, delegated parsing |
| 2 | Code Agent | norp-code-agent | Sense→Plan→Act→Learn: read data dictionary, decoded Likert, cleaned, cross-tabbed |
| 3 | Validator Agent | norp-validator-agent | 6/6 Data Contract assertions PASS → APPROVED |
| 4 | Orchestrator synthesis | — | Chi-square significance + report comparison |

## Coding (from `dd-nptrends-year-04-puf.xlsx`)

- `Benefits_Health`: `1 = offers group health insurance`, `0 = not selected` (binary).
- `BenefitsImpact` (Q18 Likert 1–5): `1–2 → Negative`, `3 → No Impact`, `4–5 → Positive`.
  Codes 97 (Unsure) / 98 (N/A) were already NaN in the source CSV.
- Cleaning: listwise-dropped rows missing either field → **n = 3,043**.

## Finding (Figure 17 replication, unweighted)

| Reported benefits impact | % offering health insurance | Report target |
|---|---|---|
| Positive | **74.9%** (1,168 / 1,560) | ~76% |
| Negative | **16.2%** (165 / 1,017) | ~18% |

**Significance:** χ²(2, N=3043) = 970.5, p ≈ 1.8 × 10⁻²¹¹, Cramér's V = 0.565 (large effect).

> Note: this run is **unweighted**. The current agent skills mandate applying survey
> weights; a weighted re-run is a follow-up item.

## Files

- `cleaned_test_case_1.csv` — validated 2-column dataset (3,043 rows)
- `tc1_agent_flow.csv` / `tc1_figure17_finding.csv` — the two tables above
- `tc1_tables.xlsx` — both tables as one workbook (2 sheets)
