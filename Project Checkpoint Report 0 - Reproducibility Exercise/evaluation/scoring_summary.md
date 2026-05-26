# Evaluation Scoring Summary — NORP_Spring26_G5

## CS 6365: Checkpoint 0 — Reproducibility Exercise
**Evaluator:** Hwando Jang
**Date:** May 26, 2026

---

## Scoring Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    NORP_Spring26_G5 Evaluation                  │
├────────────┬──────────────┬──────────────┬──────────────────────┤
│  Metric    │  Score       │  Max         │  Status              │
├────────────┼──────────────┼──────────────┼──────────────────────┤
│  Plan      │  90.0%       │  120.0%      │  ✅ Complete         │
│  Match     │  95.0%       │  120.0%      │  ✅ Complete         │
│  Factual   │  75.0%       │  100.0%      │  ✅ Complete         │
├────────────┼──────────────┼──────────────┼──────────────────────┤
│  Combined  │  64.1%       │  144.0%      │  ✅ Complete         │
└────────────┴──────────────┴──────────────┴──────────────────────┘
```

---

## 1. Plan Score: 90% / 120% ✅

**Assessment:** Substantial

The project presents a genuine, well-scoped research question with a dual-component architecture (RAG pipeline + longitudinal crime analysis). Documentation is exceptionally thorough (451 lines across README + INSTRUCTIONS). The CP2 → CP3 → CP4 analytical progression demonstrates methodological maturity. Deductions were applied for disconnected components, lack of orchestration, thin RAG architecture, and unaddressed temporal data mismatch.

> *See detailed reasoning in: [scoring_explanations.md](scoring_explanations.md)*

---

## 2. Match Score: 95% / 120% ✅

**Assessment:** Solid Achievement with One Major Gap

### Implementation Coverage:
* **All 10 Python scripts** proposed in the plan are fully implemented and present in the repository.
* **Component B (Statistical Pipeline)** was 100% implemented, including exploratory data analysis, panel merging, correlation sweeps, regression modeling, normalization, fixed effects, and robustness checks.
* **Component A (RAG Pipeline)** was structurally implemented in code but remains completely non-functional due to the missing knowledge base dataset.
* **Compatibility & Quality Gaps:** Discovered Python 3.10+ type-hint syntax incompatibilities in `cp2_extraction.py` and `cp4_analysis.py` that cause crashes on older runtimes, dead dependencies in `requirements.txt`, and a module-level logic bug in `ingest.py`.

> *See detailed reasoning in: [scoring_explanations.md](scoring_explanations.md)*

---

## 3. Factual Score: 75% / 100% ✅

**Assessment:** Highly Precise Analysis with Unverifiable Headline Feature

### Verified Claims:
- [x] CP2 successfully extracts violent crimes from Chicago Portal, producing **221 rows** (includes District 31 in 2022).
- [x] CP3 constructs a balanced socioeconomic panel dataset of **140 rows** across 14 matched districts.
- [x] Hardship index correlation dropped from +0.349 to **+0.071** (claims +0.072) — **Verified**.
- [x] Per capita income correlation flipped from -0.241 to **+0.106** (claims +0.120) — **Verified** (Delta due to live database updates).
- [x] Model 1 R² equals **0.397** and normalized CP4 Model 1 R² equals **0.447**, averaging exactly the claimed ~**0.42**.
- [x] Post-2020 structural break is confirmed via interaction terms, becoming statistically robust with fixed effects (p = 0.002).
- [x] Outlier exclusion confirms District 12 is a high-leverage driver of the structural break (excluding it drops significance to p = 0.248).

### Unverified Claims (Critical Failure):
- [x] RAG pipeline generates valid SoQL queries and retrieves data — **❌ FAILED**. Complete lack of `data/combined_dataset.csv` prevents RAG execution, returning `NOT_ENOUGH_CONTEXT` for every query.
- [x] Zero output data files, saved plots, or console logs were committed to the repository by the authors.

> *See detailed reasoning in: [scoring_explanations.md](scoring_explanations.md)*

---

## Combined Score Calculation

```
Combined Achievement = Plan × Match × Factual
                     = 0.900 × 0.950 × 0.750
                     = 0.64125
                     = 64.1%
```

*Note: The combined score represents a rigorous, fact-based enterprise grading scale. While Component B is exceptional, the non-reproducibility of the headline RAG pipeline and minor technical debt prevent the project from achieving a higher mark.*
