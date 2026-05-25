# Scoring Explanations — NORP_Spring26_G5

## CS 6365: Checkpoint 0 — Reproducibility Exercise
**Evaluator:** Hwando Jang
**Date:** May 25, 2026

---

## 1. Plan Score Explanation

### Score: 90% / 120%

**Assessment Level:** Substantial

**Key Observations:**

1. **Genuine, well-scoped research question.** The central question — whether socioeconomic–crime relationships shifted after 2020 — is empirically testable, socially relevant, and grounded in a real statistical methodology (structural break analysis via OLS interaction terms).

2. **Dual-component architecture.** The plan combines an interactive RAG pipeline (Component A: natural language → SoQL → API) with a rigorous longitudinal statistical analysis (Component B: CP2–CP4). This demonstrates technical breadth, though the components operate independently without integration.

3. **Thorough documentation.** The README (212 lines) and INSTRUCTIONS (239 lines) are among the most detailed I've seen — providing step-by-step execution guides, data source references, schema definitions, key findings, and even an "LLM Context Injection" section for AI-assisted development.

4. **Methodological progression.** The CP2→CP3→CP4 pipeline structure mirrors genuine research practice (exploration → modeling → robustness validation), showing design maturity beyond a typical course project.

5. **Limiting factors.** The two components are disconnected, there is no pipeline orchestration, the RAG component is architecturally simple (basic cosine similarity), and five listed dependencies are unused — suggesting an abandoned pivot from a more ambitious design.

**Justification:** The plan is clearly "Substantial" — well above Hello World. It demonstrates genuine analytical ambition, real-world data integration, and methodological rigor. However, the disconnected architecture and thin RAG component prevent it from reaching "Exceeds Expectations" territory (100%+). A score of 90% reflects a strong, well-documented plan with meaningful but addressable weaknesses.

---

## 2. Match Score Explanation

### Score: TBD / 120%

> *To be completed after reproduction attempt (Day 3–4)*

**Implementation Coverage:**

| Planned Feature | Implemented? | Quality | Notes |
|:---|:---:|:---:|:---|
| CP2: Extraction | TBD | TBD | |
| CP2: EDA | TBD | TBD | |
| CP3: Socioeconomic | TBD | TBD | |
| CP3: Merge | TBD | TBD | |
| CP3: Analysis | TBD | TBD | |
| CP4: Robustness | TBD | TBD | |
| RAG Pipeline | TBD | TBD | Missing `combined_dataset.csv` — may be non-functional |

**Justification:** TBD

---

## 3. Factual Score Explanation

### Score: TBD / 100%

> *To be completed after reproduction attempt (Day 3–4)*

**Evidence Verification Matrix:**

| Claim | Evidence Found | Verified? | Notes |
|:---|:---:|:---:|:---|
| 220 rows in CP2 output | TBD | TBD | |
| 140 rows in panel dataset | TBD | TBD | |
| Hardship correlation: +0.349 → +0.072 | TBD | TBD | |
| Income correlation: −0.241 → +0.120 | TBD | TBD | |
| R² ≈ 0.42 for Model 1 | TBD | TBD | |
| Structural break confirmed via interaction model | TBD | TBD | |
| RAG pipeline generates valid SoQL | TBD | TBD | Requires `combined_dataset.csv` |

**Preliminary Note on `combined_dataset.csv`:**
Confirmed absent from **both** the GT fork (`github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5`) **and** the original repository (`github.com/KhalidBargoti/NORP`). The GitHub API listing of the original repo shows 15 root-level files with no `data/` directory. This means the RAG pipeline's core knowledge base was never committed to either repository, constituting a critical reproducibility failure for Component A.

**Justification:** TBD
