# Code Execution Log — NORP_Spring26_G5 Reproduction

## Reproduction Date: May 25, 2026 (Day 2 of 3)
## Reproducer Environment: macOS, Python 3.9, venv

---

## 1. Execution Order

Based on the file naming convention (`cp2`, `cp3`, `cp4`) and dependency analysis, the execution order is:

1. `cp2_extraction.py` — Extract violent crime data from Chicago Data Portal API
2. `cp2_eda.py` — Exploratory data analysis and visualization
3. `cp3_merge.py` — Merge crime data with socioeconomic data
4. `cp3_socioeco.py` — Socioeconomic factor analysis
5. `cp3_analysis.py` — Statistical analysis (correlation, regression)
6. `cp4_analysis.py` — Advanced/final analysis
7. `ingest.py` → `rag_pipeline.py` — RAG pipeline (document ingestion + retrieval)
8. `main.py` — Main orchestrator

> **Note:** `Crime_API.py` is a utility module imported by other scripts, not executed directly.

---

## 2. Execution Attempts

### 2.1 cp2_extraction.py

**Executed:** May 25, 2026 ~19:00 CDT

```bash
source venv/bin/activate && python cp2_extraction.py
```

**Status:** ✅ SUCCESS  
**Runtime:** ~13 seconds

**Output file:** `data/cp2_violent_crimes_by_district_year.csv`

**Fix applied before execution:**  
Had to add `from __future__ import annotations` at the top of the file to resolve a Python 3.9 incompatibility with the `pd.DataFrame | None` type hint (PEP 604 union syntax requires Python 3.10+).

**Execution details:**
- API calls: 10 requests (one per year, 2015–2024)
- Each year returned 22 districts, except 2022 which returned 23 (District 31)
- Total rows produced: **221** (vs. expected ~220; +1 due to District 31 in 2022)
- Districts found: 23 total — `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25, 31]`
- Years covered: 2015–2024

**Warnings:**
- `urllib3 NotOpenSSLWarning` — non-critical; urllib3 v2 prefers OpenSSL but LibreSSL works fine

**Sample output (first 5 rows):**
```csv
year,district,violent_crime_count
2015,1,326
2015,2,548
2015,3,596
2015,4,604
```

---

### 2.2 cp2_eda.py

**Executed:** May 25, 2026 ~19:05 CDT

```bash
source venv/bin/activate && python cp2_eda.py
```

**Status:** ✅ SUCCESS  
**Runtime:** ~20 seconds (includes matplotlib font cache build on first run)

**Output files generated:**

| File | Size | Description |
|:-----|-----:|:------------|
| `plots/cp2_citywide_trend.png` | 65,828 B | Citywide violent crime line chart 2015–2024 with COVID-2020 marker |
| `plots/cp2_district_heatmap.png` | 185,171 B | District × year heatmap with cell annotations |
| `plots/cp2_pre_post_2020.png` | 50,408 B | Grouped bar chart comparing pre- vs post-2020 averages |
| `plots/cp2_pct_change.png` | 44,011 B | Horizontal bar chart of % change by district |
| `data/cp2_eda_summary.csv` | 723 B | Summary statistics per district |

**Key findings from EDA:**

| Metric | Value |
|:-------|------:|
| Districts with **more** violent crime post-2020 | 12 |
| Districts with **less** violent crime post-2020 | 10 |
| Median % change across districts | **+5.4%** |
| Largest increase | District 20 (**+34.1%**) |
| Largest decrease | District 7 (**−14.7%**) |
| Highest total crimes (10-year sum) | District 11 (**9,599**) |
| Notable trend | District 12: 413 (2015) → 1,113 (2023), +32.7% avg |

---

### 2.3 cp3_merge.py

```bash
source venv/bin/activate && python cp3_merge.py
```
**Status:** 🔲 TODO (Day 3)

---

### 2.4 cp3_socioeco.py

```bash
source venv/bin/activate && python cp3_socioeco.py
```
**Status:** 🔲 TODO (Day 3)

---

### 2.5 cp3_analysis.py

```bash
source venv/bin/activate && python cp3_analysis.py
```
**Status:** 🔲 TODO (Day 3)

---

### 2.6 cp4_analysis.py

```bash
source venv/bin/activate && python cp4_analysis.py
```
**Status:** 🔲 TODO (Day 3)

---

### 2.7 ingest.py

```bash
source venv/bin/activate && python ingest.py
```
**Status:** 🔲 TODO (Day 3)

---

### 2.8 rag_pipeline.py

```bash
source venv/bin/activate && python rag_pipeline.py
```
**Status:** 🔲 TODO (Day 3)

---

### 2.9 main.py

```bash
source venv/bin/activate && python main.py
```
**Status:** 🔲 TODO (Day 3)

---

## 3. Issues & Fixes Log

| # | Script | Issue | Fix Applied | Severity |
|:-:|:-------|:------|:------------|:--------:|
| 1 | `cp2_extraction.py` | `pd.DataFrame \| None` type hint fails on Python 3.9 | Added `from __future__ import annotations` | Minor |

---

## 4. Execution Summary

| Script | Runs? | Correct Output? | Notes |
|:-------|:-----:|:---------------:|:------|
| `cp2_extraction.py` | ✅ Yes | ✅ Yes (221 rows) | +1 row vs expected due to District 31 in 2022 |
| `cp2_eda.py` | ✅ Yes | ✅ Yes (5 files) | 4 plots + 1 summary CSV generated |
| `cp3_merge.py` | 🔲 | 🔲 | TODO — Day 3 |
| `cp3_socioeco.py` | 🔲 | 🔲 | TODO — Day 3 |
| `cp3_analysis.py` | 🔲 | 🔲 | TODO — Day 3 |
| `cp4_analysis.py` | 🔲 | 🔲 | TODO — Day 3 |
| `ingest.py` | 🔲 | 🔲 | TODO — Day 3 |
| `rag_pipeline.py` | 🔲 | 🔲 | TODO — Day 3 |
| `main.py` | 🔲 | 🔲 | TODO — Day 3 |
