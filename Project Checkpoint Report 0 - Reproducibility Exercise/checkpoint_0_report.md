# Checkpoint 0: Reproducibility Exercise — Full Report

## CS 6365: Introduction to Enterprise Computing | Summer 2026
**Team:** Hwando Jang, Carla Du Plessis, Aayush Chandak
**Date:** May 2026
**Target Project:** [NORP_Spring26_G5](https://github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5)

---

## 1. Introduction

This report documents our team's reproducibility exercise of the **NORP_Spring26_G5** project package, originally created by Khalid A Bargoti and Khoa K Bui (CS 4365/6365, Spring 2026, Group 5). The project is formally titled *"Analysis of Socioeconomic Determinants of Violent Crime Using Retrieval-Augmented Query Generation"* and consists of two components: an interactive RAG pipeline for generating Socrata Query Language (SoQL) queries against the Chicago Crimes API, and a longitudinal statistical analysis of violent crime vs. socioeconomic factors across Chicago police districts (2015–2024).

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

<!-- TODO: Document environment setup process (Day 2) -->

### 3.2 Code Execution
> *See detailed log in: [execution_log.md](reproduction_logs/execution_log.md)*

<!-- TODO: Document code execution attempts (Day 2-3) -->

### 3.3 Inconsistencies
> *See detailed log in: [inconsistencies.md](reproduction_logs/inconsistencies.md)*

**Pre-Reproduction Findings:**
During code analysis (before running any scripts), we identified several inconsistencies:
1. 🔴 **Missing `data/combined_dataset.csv`** — The RAG knowledge base is absent from both the GT fork AND the original repository, making the interactive pipeline (Component A) non-functional.
2. 🟠 **Model name mismatch** — README says `mistralai/devstral-2512:free`; code uses `openai/gpt-oss-20b:free`.
3. 🟠 **README Step 6 error** — Says run `cp3_analysis.py` but describes `cp4_analysis.py` functionality.
4. 🟡 **5 dead dependencies** — `langchain`, `chromadb`, `tiktoken`, `faiss-cpu`, `openai` are in requirements.txt but never imported.

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
- **OS:** Windows 11
- **Python:** TBD
- **Date of Reproduction:** May 2026

### C. Critical Finding: Missing RAG Knowledge Base
The file `data/combined_dataset.csv` is referenced by `main.py` and `ingest.py` as the RAG knowledge base (NL→SoQL example pairs). This file does not exist in:
- The GT fork: `github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5`
- The original repository: `github.com/KhalidBargoti/NORP`

Verified via GitHub API listing on May 25, 2026 — the original repo contains exactly 15 root-level files with no `data/` directory.
