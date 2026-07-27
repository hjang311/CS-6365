# Checkpoint 1 — Early Agentic Experiments

Initial exploration of the Antigravity SDK and agentic pipeline design using **broadband access × nonprofit fundraising efficiency** as a test case (RQ1).

## Headline finding (null — first-class)

| Item | Value |
|------|-------|
| Hypothesis | Low broadband communities → worse fundraising efficiency |
| OLS broadband coefficient | ≈ **0.368** |
| p-value | ≈ **0.367** (not significant) |
| n | **457** (survey-weighted frame; see report) |
| Reading | Well-supported **null** — retained as a reportable baseline, not a failed checkpoint |

Details: [`Broadband Access x Fundraising Efficiency/FINDINGS.md`](Broadband%20Access%20x%20Fundraising%20Efficiency/FINDINGS.md).

## Important discontinuity vs later checkpoints

CP1 used a **different dataset and unit of analysis** (ACS/PUF-style survey path documented in the report) than the national ZIP-level NCCS CORE frame used from **Checkpoint 2 onward**. Do not expect CP1 coefficients to match H2/H4/H5 tables.

## Contents

| Item | Description |
|------|-------------|
| [`Broadband Access x Fundraising Efficiency/`](Broadband%20Access%20x%20Fundraising%20Efficiency/) | Pipeline scripts (acquire, merge, analyze, validate) + findings |
| [`Checkpoint_1_Report.md`](Checkpoint_1_Report.md) | Checkpoint 1 report |
| [`Pipeline_Iteration_Report_Phase_1_to_2.md`](Pipeline_Iteration_Report_Phase_1_to_2.md) | Iteration report documenting pipeline evolution |

## How to run (historical)

From the broadband pipeline folder, follow that directory’s README / script order (`acquire` → `merge` → `analyze` → `validate`). Large `Data/` trees are gitignored — regenerate or use a handoff machine.

## Limitations

- Null result is expected under this measure / sample; do not over-claim.
- SDK-era scaffolding here is **not** the Phase 3 entrypoint (`Checkpoint 4/`).
- Authorship in older report text may say “HDJ”; canonical team credit is Hwando Jang & Carla du Plessis (root README).

## Curriculum context

Exploratory agentic experiments. Patterns evolved into the Manual H2 pipeline in Checkpoint 2. See [`docs/CURRICULUM.md`](../docs/CURRICULUM.md) and [`docs/HYPOTHESIS_REGISTRY.md`](../docs/HYPOTHESIS_REGISTRY.md) (RQ1).
