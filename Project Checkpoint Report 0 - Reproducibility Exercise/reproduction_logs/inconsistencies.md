# Inconsistencies Log — NORP_Spring26_G5 Reproduction

## Date: May 2026

---

## Purpose

This document tracks all inconsistencies, discrepancies, and issues found during the reproduction of the NORP_Spring26_G5 project. Each inconsistency is documented with its severity, location, and impact on the overall evaluation.

---

## Severity Legend

| Severity | Description |
|:---|:---|
| 🔴 **Critical** | Prevents reproduction entirely |
| 🟠 **Major** | Significantly impacts results or functionality |
| 🟡 **Minor** | Small discrepancies that don't affect core functionality |
| 🔵 **Info** | Observations that don't impact scoring |

---

## Inconsistencies Found

### Issue #1: Missing `data/combined_dataset.csv` — RAG Knowledge Base
- **Severity:** 🔴 Critical
- **Location:** `main.py` (line referencing `docs_dir = "data"`), `ingest.py` (loads CSV/Excel from `data/`)
- **Description:** The RAG pipeline's knowledge base file `data/combined_dataset.csv` is not included in the repository. This file contains natural language → SoQL query example pairs that are essential for the retrieval step.
- **Expected:** The file should be present in a `data/` directory for the RAG pipeline to function.
- **Actual:** No `data/` directory exists in the repository. Verified absent from both the GT fork (`github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5`) AND the original repository (`github.com/KhalidBargoti/NORP`) via GitHub API on May 25, 2026.
- **TA Confirmation:** Per discussion with TA Satvik Agrawal on May 25, 2026, the missing dataset is **intentional** and is part of the original team's submission. This should be noted and penalized in the evaluation.
- **Impact on Scoring:** Directly reduces **Factual** score for Component A (RAG pipeline). The headline feature of the project cannot be independently verified.

---

### Issue #2: LLM Model Name Mismatch
- **Severity:** 🟠 Major
- **Location:** `README.md` line 35 vs. `main.py` source code
- **Description:** Documentation and code disagree on the LLM model used.
- **Expected (per README):** `mistralai/devstral-2512:free`
- **Actual (in code):** `openai/gpt-oss-20b:free`
- **Impact on Scoring:** Reduces **Factual** score — documentation doesn't match implementation. A reproducer following the README would have incorrect expectations.

---

### Issue #3: README Step 6 References Wrong Script
- **Severity:** 🟠 Major
- **Location:** `README.md` — "Step 6 — Advanced Analysis & Robustness Checks" section
- **Description:** Step 6 instructs the user to run `python cp3_analysis.py` but then describes functionality that belongs to `cp4_analysis.py` (normalization, robustness checks, influential districts).
- **Expected:** `python cp4_analysis.py`
- **Actual:** `python cp3_analysis.py` (which is Step 5's script)
- **Impact on Scoring:** Reduces **Factual** score — incorrect execution instructions could confuse a reproducer.

---

### Issue #4: Dead Dependencies in requirements.txt
- **Severity:** 🟡 Minor
- **Location:** `requirements.txt`
- **Description:** Five packages are listed as dependencies but are never imported or used by any script in the repository:
  - `openai` — never imported (project uses OpenRouter via `requests`)
  - `langchain` — never imported
  - `chromadb` — never imported (RAG uses manual cosine similarity)
  - `tiktoken` — never imported
  - `faiss-cpu` — never imported
- **Expected:** requirements.txt should only list actually-used packages.
- **Actual:** 5 of 18 listed packages (28%) are unused, suggesting leftover artifacts from an earlier design that pivoted to a simpler architecture.
- **Impact on Scoring:** Minor **Match** impact — suggests planned-but-abandoned features. Increases install time and disk usage unnecessarily.

---

### Issue #5: Dead Imports in Source Files
- **Severity:** 🟡 Minor
- **Location:** Multiple files
- **Description:** Several files import modules that are never used:
  - `rag_pipeline.py`: imports `transformers.pipeline` (unused), sets `model_type = 'extraction'` (unused attribute)
  - `ingest.py`: imports `unstructured.partition.auto` (unused)
  - `cp3_analysis.py`: imports `LinearRegression` and `StandardScaler` from sklearn (unused)
  - `Crime_API.py`: imports `sys` and `HTTPBasicAuth` (unused)
- **Impact on Scoring:** Minimal — code still functions, but indicates incomplete cleanup.

---

### Issue #6: No `if __name__ == "__main__"` Guards
- **Severity:** 🟡 Minor
- **Location:** `cp3_socioeco.py`, `cp3_merge.py`
- **Description:** These scripts execute all code at module level. Importing them (e.g., for testing or reuse) would trigger full execution including API calls and file writes.
- **Impact on Scoring:** Minor code quality issue. No impact on direct execution, but poor practice for modularity.

---

### Issue #7: Logic Bug in `ingest.py`
- **Severity:** 🟡 Minor
- **Location:** `ingest.py`, `else` clause alignment
- **Description:** The `else` clause at the end of the file-loading logic is aligned with the CSV `if` check rather than the initial file-type `if` check. This means Excel files that pass the initial check will also trigger the "Skipping unsupported file type" warning.
- **Impact on Scoring:** Minor — would only matter if Excel files were used as input (current system uses CSV only).

---

### Issue #8: Typo in `main.py` Output
- **Severity:** 🔵 Info
- **Location:** `main.py`, print statement
- **Description:** Output text reads "Retrived" instead of "Retrieved".
- **Impact on Scoring:** None — cosmetic only.

---

## Summary

| Severity | Count |
|:---|:---:|
| 🔴 Critical | 1 |
| 🟠 Major | 2 |
| 🟡 Minor | 4 |
| 🔵 Info | 1 |
| **Total** | **8** |

### Overall Assessment
The project has **one critical reproducibility blocker** (missing RAG knowledge base) and **two major documentation mismatches**. The critical issue was confirmed as intentional by the course TA. The remaining issues are minor code quality observations that do not prevent the statistical pipeline (Component B) from functioning.
