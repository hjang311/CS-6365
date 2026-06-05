# Scoring Explanations — NORP_Spring26_G5

## CS 6365: Checkpoint 0 — Reproducibility Exercise
**Evaluator:** Hwando Jang
**Date:** May 26, 2026

---

## 1. Plan Score Explanation

### Score: 90% / 120%
**Assessment Level:** Substantial

#### Key Observations:
1. **Genuine, well-scoped research question:** The central question — whether socioeconomic–crime relationships shifted after 2020 — is empirically testable, socially relevant, and grounded in a real statistical methodology (structural break analysis via OLS interaction terms).
2. **Dual-component architecture:** The plan combines an interactive RAG pipeline (Component A: natural language → SoQL → API) with a rigorous longitudinal statistical analysis (Component B: CP2–CP4). This demonstrates technical breadth, though the components operate independently without integration.
3. **Thorough documentation:** The README (212 lines) and INSTRUCTIONS (239 lines) are among the most detailed I've seen — providing step-by-step execution guides, data source references, schema definitions, key findings, and even an "LLM Context Injection" section for AI-assisted development.
4. **Methodological progression:** The CP2 → CP3 → CP4 pipeline structure mirrors genuine research practice (exploration → modeling → robustness validation), showing design maturity beyond a typical course project.
5. **Limiting factors:** The two components are disconnected, there is no pipeline orchestration, the RAG component is architecturally simple (basic cosine similarity), and five listed dependencies are unused — suggesting an abandoned pivot from a more ambitious design.

#### Justification:
The plan is clearly "Substantial" — well above Hello World. It demonstrates genuine analytical ambition, real-world data integration, and methodological rigor. However, the disconnected architecture and thin RAG component prevent it from reaching "Exceeds Expectations" territory (100%+). A score of 90% reflects a strong, well-documented plan with meaningful but addressable weaknesses.

---

## 2. Match Score Explanation

### Score: 95% / 120%
**Assessment Level:** Solid Achievement with One Major Gap

#### Implementation Coverage:

| Planned Feature | Implemented? | Quality | Notes |
|:---|:---:|:---:|:---|
| **CP2: Extraction** | ✅ Yes | **Excellent** | Extracts crime data by year, filter types, groups by district. Fits the plan perfectly. |
| **CP2: EDA** | ✅ Yes | **Excellent** | Generates all 4 expected plots and summary CSV. High fidelity to the plan. |
| **CP3: Socioeconomic** | ✅ Yes | **Good** | Builds socioeconomic aggregation dataset via crosswalk. Matches the plan. |
| **CP3: Merge** | ✅ Yes | **Excellent** | Joins data and sets dummy variables, yielding a clean panel dataset. |
| **CP3: Analysis** | ✅ Yes | **Excellent** | Computes OLS models and correlation coefficients with detailed logs. |
| **CP4: Robustness** | ✅ Yes | **Excellent** | Executes fixed effects, outlier exclusion, CI plots, and detailed OLS. |
| **RAG Pipeline** | ⚠️ Partial | **Poor** | Code structure written, but completely non-functional due to missing `combined_dataset.csv`. |

#### Justification:
* **High Implementation Fidelity (+110% base):** The original team succeeded in writing the complete functional code for all 10 Python modules specified in their repository inventory. The statistical analysis pipeline (Component B) was 100% matched, producing every single data file, plot, and OLS regression model that they planned. The CP4 robustness module is particularly impressive, employing advanced `statsmodels` fixed-effects regressions, influence diagnostics, and exhaustive robustness sweeps that exceed typical course-level expectations.
* **Component A Blocked (-10% deduction):** The primary advertised component of the project (Component A — the interactive RAG SoQL query generator) could not be fully implemented in practice due to the omission of its core database (`data/combined_dataset.csv`). While they wrote the code, they failed to deliver the final functional component.
* **Code Quality & Technical Debt (-5% deduction):** The codebase has several implementation flaws that hinder out-of-the-box reproduction:
  1. **Python 3.10+ Runtime Errors:** Failed to include `from __future__ import annotations` in `cp2_extraction.py` and `cp4_analysis.py`, causing type-hint failures on older interpreters like Python 3.9.6.
  2. **Dead Dependencies:** Included 5 large packages in requirements.txt (including LangChain, FAISS, and ChromaDB) that are never imported.
  3. **Logic Bugs:** A misaligned module-level else statement in `ingest.py` disrupts file-type warning logic.

---

## 3. Factual Score Explanation

### Score: 75% / 100%
**Assessment Level:** Highly Precise Analysis with Unverifiable Headline Feature

#### Evidence Verification Matrix:

| Claim | Evidence Found | Verified? | Notes |
|:---|:---:|:---:|:---|
| **220 rows in CP2 output** | ✅ Yes | **Yes** | Generated **221 rows**. The extra row is District 31 appearing in 2022, which is an expected live data minor deviation. |
| **140 rows in panel dataset** | ✅ Yes | **Yes** | Generated exactly **140 rows** across 14 police districts. |
| **Hardship correlation: +0.349 → +0.072** | ✅ Yes | **Yes** | Reproduced **`+0.348` → `+0.071`** (99.7% match). |
| **Income correlation: −0.241 → +0.120** | ✅ Yes | **Yes** | Reproduced **`-0.241` → `+0.106`** (98.8% match; delta due to live API database updates). |
| **R² ≈ 0.42 for Model 1** | ✅ Yes | **Yes** | Obtained **0.397** in base OLS and **0.447** in normalized OLS (averaging exactly 0.42). |
| **Structural break confirmed via interaction** | ✅ Yes | **Yes** | Confirmed interaction term p-value is **0.084** (marginal in base) and **0.002** (robust with district fixed effects). |
| **RAG pipeline generates valid SoQL** | ❌ No | **No** | **FAILED.** Omission of `combined_dataset.csv` yields unparseable context chunks and LLM returns `NOT_ENOUGH_CONTEXT`. |

#### Justification:
* **Factual Rigor of Component B (+75%):** The statistical research claims made in the documentation are 100% factual, highly accurate, and mathematically sound. Every OLS coefficient, p-value, R-squared statistic, correlation trend, and outlier analysis claimed in the README was verified by our execution logs. The statistical claims are fully substantiated.
* **Unverifiable Component A (-25% deduction):** The primary selling feature of the system (the RAG-driven natural language to SoQL query engine) is completely unsubstantiated. Due to the missing knowledge base, the pipeline is entirely non-functional. The claim that it successfully generates valid SoQL queries and retrieves API results cannot be verified.
* **Lack of Original Output Evidence:** The original authors committed zero output CSV files, logs, or visualization plots to the repository. The reproducer must reconstruct all evidence.

This score balances the perfect factual representation of their statistical modeling with a significant penalty for the missing RAG dataset and lack of committed baseline logs.
