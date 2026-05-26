# Checkpoint 0: Reproducibility Exercise — Full Report

## CS 6365: Introduction to Enterprise Computing | Summer 2026
**Author:** Hwando Jang
**Date:** May 2026
**Target Project:** [NORP_Spring26_G5](https://github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5)

---

## 1. Introduction

This report documents my reproducibility exercise of the **NORP_Spring26_G5** project package, originally created by Khalid A Bargoti and Khoa K Bui (CS 4365/6365, Spring 2026, Group 5). The project is formally titled *"Analysis of Socioeconomic Determinants of Violent Crime Using Retrieval-Augmented Query Generation"* and consists of two components: an interactive RAG pipeline for generating Socrata Query Language (SoQL) queries against the Chicago Crimes API, and a longitudinal statistical analysis of violent crime vs. socioeconomic factors across Chicago police districts (2015–2024).

### 1.1 Purpose
The purpose of this exercise is to:
- Evaluate the completeness and quality of the project's documentation
- Attempt to reproduce the project's claimed results
- Assess the project across three dimensions: **Plan**, **Match**, and **Factual**

### 1.2 Repository Overview

| Attribute | Value |
|:---|:---|
| **Repository URL** | `github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5` |
| **Original Repo** | [github.com/KhalidBargoti/NORP](https://github.com/KhalidBargoti/NORP) |
| **Uploader** | sagraval391 (minor changes) |
| **Original Authors** | Khalid A Bargoti, Khoa K Bui |
| **Language** | Python (100%) |
| **Commits** | 1 ("Adding Project Files") |
| **Branches** | 1 (main) |
| **Files** | 15 files (10 Python scripts, 2 Markdown docs, requirements.txt, .env, .gitignore) |

---

## 2. Project Components

### 2.1 Project Plan
> *See detailed analysis in: [01_project_plan.md](project_components/01_project_plan.md)*

The project proposes a dual-component system: (A) an interactive RAG pipeline that converts natural language questions into SoQL queries against the Chicago Crimes API, and (B) a multi-checkpoint longitudinal analysis investigating whether socioeconomic–crime relationships shifted after 2020. The research question is genuine, testable, and well-scoped. The documentation (451 combined lines of README + INSTRUCTIONS) is thorough and provides clear execution guides, data source references, and stated findings. The plan is assessed as **Substantial** — well above Hello World — with a preliminary score of **90% / 120%**.

### 2.2 Project Execution
> *See detailed analysis in: [02_project_execution.md](project_components/02_project_execution.md)*

<!-- TODO: Summarize their implementation approach and results after reproduction (Day 3-4) -->

### 2.3 Supporting Evidence
> *See detailed analysis in: [03_supporting_evidence.md](project_components/03_supporting_evidence.md)*

<!-- TODO: Summarize the evidence backing their claims after reproduction (Day 3-4) -->

---

## 3. Reproduction Process

### 3.1 Environment Setup
> *See detailed log in: [setup_log.md](reproduction_logs/setup_log.md)*

The reproduction environment was set up on **macOS (ARM64)** with **Python 3.9.6**. The target repository was cloned from Georgia Tech's enterprise GitHub (`github.gatech.edu`), requiring interactive authentication. A virtual environment was created and all 18 direct dependencies (plus 160+ transitive dependencies) were installed via `pip install -r requirements.txt`. Both required API keys — a **Socrata App Token** (Chicago Data Portal) and an **OpenRouter API Key** — were configured in the `.env` file.

**Key setup issue discovered:** The script `cp2_extraction.py` uses Python 3.10+ type hint syntax (`pd.DataFrame | None`) which causes a `TypeError` on Python 3.9. This was fixed by adding `from __future__ import annotations`. This is a **new reproducibility finding** — the repository does not document any minimum Python version requirement.

### 3.2 Code Execution
> *See detailed log in: [execution_log.md](reproduction_logs/execution_log.md)*

**CP2 Extraction (`cp2_extraction.py`):** ✅ Successfully extracted violent crime counts from the Chicago Data Portal API. Produced **221 rows** across 23 districts and 10 years (2015–2024), saved to `data/cp2_violent_crimes_by_district_year.csv`. This slightly exceeds the expected ~220 rows due to District 31 appearing only in 2022 with 1 crime.

**CP2 EDA (`cp2_eda.py`):** ✅ Successfully generated all 4 expected plots and a summary CSV:
- `plots/cp2_citywide_trend.png` — Citywide violent crime trend with 2020 COVID marker
- `plots/cp2_district_heatmap.png` — District × year heatmap
- `plots/cp2_pre_post_2020.png` — Pre/post 2020 comparison
- `plots/cp2_pct_change.png` — Percent change by district

Key EDA finding: 12 districts showed increased violent crime post-2020, 10 showed decreases. Median change was +5.4%. District 20 had the largest increase (+34.1%), District 7 the largest decrease (-14.7%).

**CP3 Socioeconomic Setup (`cp3_socioeco.py`):** ✅ Successfully built district-level socioeconomic indicators from hardcoded ACS data and API-derived community-to-district crosswalk. Produced data for **14 of 23 districts** — 9 districts could not be mapped, resulting in 37% data loss for the analysis panel.

**CP3 Merge (`cp3_merge.py`):** ✅ Merged crime panel with socioeconomic data. Final panel: **140 rows** (14 districts × 10 years). 81 rows dropped due to unmatched districts.

**CP3 Analysis (`cp3_analysis.py`):** ✅ Computed pre/post-2020 correlations and ran 3 OLS regression models. Key finding: hardship index correlation dropped from +0.348 to +0.071 (README claims +0.349 to +0.072 — **nearly identical**). Per capita income correlation shifted from -0.241 to +0.106 (README claims +0.120 — **close but slightly different**).

**CP4 Robustness (`cp4_analysis.py`):** ✅ After fixing a Python 3.9 compatibility issue (same class as CP2). Ran 4 models including district fixed effects (R²=0.741). Key finding: the hardship×post2020 interaction is marginally significant (p=0.084) in the base model but becomes highly significant (p=0.002) with district fixed effects — and **non-significant** (p=0.248) when District 12 is excluded, suggesting this district drives much of the structural break finding.

**RAG Pipeline (`main.py`):** ⚠️ Partial failure as expected. The pipeline loaded our CP2/CP3/CP4 output CSVs as context (12 files), but without the intended `combined_dataset.csv` knowledge base, retrieved chunks were unparseable and the LLM returned `NOT_ENOUGH_CONTEXT`. **Component A of the project is non-reproducible.**

### 3.3 Inconsistencies
> *See detailed log in: [inconsistencies.md](reproduction_logs/inconsistencies.md)*

**Pre-Reproduction Findings (Day 1):**
During code analysis (before running any scripts), I identified several inconsistencies:
1. 🔴 **Missing `data/combined_dataset.csv`** — The RAG knowledge base is absent from both the GT fork AND the original repository, making the interactive pipeline (Component A) non-functional.
2. 🟠 **Model name mismatch** — README says `mistralai/devstral-2512:free`; code uses `openai/gpt-oss-20b:free`.
3. 🟠 **README Step 6 error** — Says run `cp3_analysis.py` but describes `cp4_analysis.py` functionality.
4. 🟡 **5 dead dependencies** — `langchain`, `chromadb`, `tiktoken`, `faiss-cpu`, `openai` are in requirements.txt but never imported.

**Runtime Findings (Day 2):**
During actual code execution, three additional issues were identified:
5. 🟠 **Python 3.10+ type hint incompatibility** — `cp2_extraction.py` uses `pd.DataFrame | None` syntax requiring Python 3.10+. No minimum Python version is documented.
6. 🔵 **Row count deviation** — Extraction produced 221 rows vs. expected ~220 (District 31 appeared only in 2022).
7. 🟡 **No version pins** — All 18 dependencies in `requirements.txt` lack version constraints, risking reproducibility across different installation dates.

**Runtime Findings (Day 3):**
8. 🟠 **cp4_analysis.py Python 3.10+ type hints** — Same class of issue as #5, with `tuple[...]` and `list[...]` on lines 137, 223, 252.
9. 🟡 **Socioeconomic crosswalk data loss** — Only 14 of 23 districts matched, dropping 37% of crime data from CP3/CP4 analysis. Not documented in README.
10. 🔴 **RAG pipeline non-functional** — Confirmed Critical Inconsistency #1. LLM returned `NOT_ENOUGH_CONTEXT` when tested.
11. 🔵 **Slight correlation deviations** — Post-2020 values differ slightly from README (e.g., income: +0.106 vs claimed +0.120), likely due to live API data updates.

---

## 4. Evaluation Scores

> *See detailed scoring in: [scoring_summary.md](evaluation/scoring_summary.md)*
> *See detailed explanations in: [scoring_explanations.md](evaluation/scoring_explanations.md)*

| Metric | Score | Max | Description |
|:---|:---:|:---:|:---|
| **Plan** | 90% | 120% | Substantial plan with genuine research question |
| **Match** | TBD | 120% | Pending reproduction attempt |
| **Factual** | TBD | 100% | Pending reproduction attempt |

### 4.1 Combined Score
```
Combined = Plan × Match × Factual
         = 0.90 × TBD × TBD
         = TBD
```

---

## 5. Conclusion

<!-- TODO: Final summary of reproducibility findings (Day 5) -->

---

## 6. Additional Requirements

Per the NORP repository's README "Assignment Deliverables" section:

### 6.1 Project Overview
<!-- TODO: Provide brief overview in our own words (Day 5) -->

### 6.2 Natural Language Query Testing
<!-- TODO: Design and test varied NL queries against the RAG pipeline (Day 3) -->

### 6.3 Observations and Failure Cases
<!-- TODO: Discuss cases where the system didn't work as expected (Day 3-4) -->

### 6.4 Directions for Improvement
<!-- TODO: Suggest high-level improvements for retrieval, dataset design, prompting (Day 5) -->

---

## Appendix

### A. Repository File Inventory

| File | Size | Purpose |
|:---|:---:|:---|
| `.env` | 75B | Environment variables (placeholder API keys) |
| `.gitignore` | 47B | Git ignore rules (.DS_Store, __pycache__, .vscode) |
| `Crime_API.py` | 2.4KB | Socrata API query executor |
| `INSTRUCTIONS.md` | 11.3KB | Detailed AI workflow guide and execution instructions |
| `README.md` | 10.4KB | Project overview, setup, and findings |
| `cp2_extraction.py` | 5.6KB | CP2: Systematic district×year violent crime extraction |
| `cp2_eda.py` | 8.6KB | CP2: Exploratory data analysis and visualizations |
| `cp3_socioeco.py` | 7.9KB | CP3: Socioeconomic dataset (hardcoded ACS data + crosswalk) |
| `cp3_merge.py` | 2.9KB | CP3: Merge crime panel with socioeconomic indicators |
| `cp3_analysis.py` | 8.6KB | CP3: Correlations, scatter plots, OLS regression |
| `cp4_analysis.py` | 26.4KB | CP4: Advanced analysis, robustness checks, statsmodels OLS |
| `ingest.py` | 1.9KB | Data ingestion for RAG pipeline (CSV/Excel chunking) |
| `main.py` | 4.6KB | Interactive RAG-based SoQL query generator |
| `rag_pipeline.py` | 1.1KB | RAG retrieval (sentence-transformers + cosine similarity) |
| `requirements.txt` | 215B | Python dependencies (18 packages) |

### B. Reproduction Environment
- **OS:** macOS (Apple Silicon / ARM64)
- **Python:** 3.9.6 (system Python via CommandLineTools)
- **Virtual Environment:** `python3 -m venv venv`
- **Package Manager:** pip 21.2.4
- **API Keys:** Socrata App Token + OpenRouter API Key (configured in `.env`)
- **Date of Reproduction:** May 25–29, 2026
- **Note:** Python 3.9 required `from __future__ import annotations` fix for `cp2_extraction.py`

### C. Critical Finding: Missing RAG Knowledge Base
The file `data/combined_dataset.csv` is referenced by `main.py` and `ingest.py` as the RAG knowledge base (NL→SoQL example pairs). This file does not exist in:
- The GT fork: `github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5`
- The original repository: `github.com/KhalidBargoti/NORP`

Verified via GitHub API listing on May 25, 2026 — the original repo contains exactly 15 root-level files with no `data/` directory.
