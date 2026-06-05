# Code Execution Log — NORP_Spring26_G5 Reproduction

## Reproduction Date: May 25, 2026 (Day 3 of 3 — Final)
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

### 2.3 cp3_socioeco.py

**Executed:** May 25, 2026 ~20:30 CDT

```bash
source venv/bin/activate && python cp3_socioeco.py
```

**Status:** ✅ SUCCESS  
**Runtime:** ~5 seconds

**Output files generated:**

| File | Rows | Description |
|:-----|-----:|:------------|
| `data/cp3_community_socioeco.csv` | 77 | Community-area-level socioeconomic indicators |
| `data/cp3_community_to_district.csv` | 78 | Community area → district crosswalk (78 mappings → 14 unique districts) |
| `data/cp3_district_socioeco.csv` | 14 | District-level aggregated socioeconomic indicators |

**Execution details:**
- Made API call to Chicago Crimes API to build community_area → district crosswalk
- Only **14 of 23 districts** could be mapped to community areas
- Unmapped districts: 11, 15, 18, 19, 20, 22, 24, 25, 31 (no community area mappings available)
- This mapping limitation propagates to all downstream analysis (cp3_merge, cp3_analysis, cp4_analysis)

---

### 2.4 cp3_merge.py

**Executed:** May 25, 2026 ~20:32 CDT

```bash
source venv/bin/activate && python cp3_merge.py
```

**Status:** ✅ SUCCESS  
**Runtime:** <1 second

**Output file:** `data/cp3_panel.csv` — **140 rows** (14 districts × 10 years)

**Columns produced:**
`year`, `district`, `violent_crime_count`, `per_capita_income`, `pct_poverty`, `pct_unemployed`, `pct_no_hs`, `pct_crowded`, `hardship_index`, `post2020`, `log_crime`

**Execution details:**
- Merged `cp2_violent_crimes_by_district_year.csv` (221 rows) with `cp3_district_socioeco.csv` (14 rows)
- **81 rows (9 districts) could not be matched** to socioeconomic data — dropped during merge
- Pre-2020 rows: **70**, Post-2020 rows: **70** (balanced panel for remaining 14 districts)

> **Warning:** The 9 unmapped districts from cp3_socioeco.py result in ~37% data loss at the merge step. All subsequent analysis operates on only 14 of 23 districts.

---

### 2.5 cp3_analysis.py

**Executed:** May 25, 2026 ~20:35 CDT

```bash
source venv/bin/activate && python cp3_analysis.py
```

**Status:** ✅ SUCCESS  
**Runtime:** ~3 seconds

**Output files generated:**

| File | Description |
|:-----|:------------|
| `data/cp3_correlation_table.csv` | Pre/post-2020 correlations with delta |
| `data/cp3_regression_results.txt` | Full OLS regression output |
| `plots/cp3_correlation_heatmap.png` | Pre/post correlation comparison |
| `plots/cp3_scatter_*.png` | Scatter plots (3 plots) |

**Key correlation results (crime vs. socioeconomic indicators):**

| Indicator | Pre-2020 | Post-2020 | Delta |
|:----------|:--------:|:---------:|:-----:|
| `hardship_index` | +0.348 | +0.071 | **−0.277** |
| `per_capita_income` | −0.241 | +0.106 | **+0.346** |
| `pct_poverty` | +0.335 | +0.124 | **−0.211** |

**OLS regression models:**

| Model | Description | R² |
|:------|:------------|:---:|
| Model 1 | Socioeconomic predictors only | 0.397 |
| Model 2 | + post2020 dummy | 0.397 |
| Model 3 | + interaction terms | 0.067 |

**Interpretation:** Correlations between socioeconomic disadvantage and violent crime weakened substantially after 2020, suggesting the pandemic disrupted pre-existing spatial crime patterns.

---

### 2.6 cp4_analysis.py

**Executed:** May 25, 2026 ~20:40 CDT

```bash
source venv/bin/activate && python cp4_analysis.py
```

**Status:** ✅ SUCCESS (after Python 3.9 fix)  
**Runtime:** ~5 seconds

**Fix applied before execution:**  
Added `from __future__ import annotations` to resolve Python 3.9 incompatibility with lowercase generic type hints (same issue as cp2_extraction.py).

**Output files generated:**

| File | Description |
|:-----|:------------|
| `data/cp4_*.csv` | 5 CSV files (model results, coefficients, robustness) |
| `data/cp4_*_results.txt` | 2 text files (full OLS output) |
| `plots/cp4_*.png` | 6 plots (diagnostics, effects, robustness) |

**Population normalization:** Skipped — `cp4_district_population.csv` not provided (noted as optional in code).

**Regression results (4 models, outcome = log_crime):**

| Model | Description | R² | Interaction p-value |
|:------|:------------|:---:|:-------------------:|
| Model 1 | Socioeconomic predictors only | 0.447 | — |
| Model 2 | + post2020 dummy | 0.447 | — |
| Model 3 | + interaction terms | 0.067 | 0.084 (marginal) |
| Model 4 | + district fixed effects | **0.741** | **0.002** (significant) |

**Key finding:** The post-2020 × socioeconomic interaction is significant only with district fixed effects (Model 4). Without controlling for district-level heterogeneity, the effect is only marginally significant.

**Robustness check (excluding District 12):**
- Interaction becomes non-significant (p = 0.248)
- R² drops to 0.143
- Suggests District 12 is a high-leverage outlier driving the main result

---

### 2.7 main.py (RAG Pipeline)

**Executed:** May 25, 2026 ~21:00 CDT

```bash
source venv/bin/activate && python main.py
```

**Status:** ⚠️ PARTIAL FAILURE (as expected)  
**Runtime:** ~30 seconds (including model download)

**Execution details:**
- Successfully loaded **12 CSV files** from `data/` directory
- Skipped **3 `.txt` files** (unsupported format)
- Retrieved 5 chunks — all unparseable (CSV analysis data, not NL→SoQL example pairs)
- LLM returned `NOT_ENOUGH_CONTEXT`
- No valid SoQL JSON produced

**Root cause:** Missing `combined_dataset.csv` — the RAG knowledge base containing natural language → SoQL query example pairs. Without this file, the retrieval step returns irrelevant CSV data instead of query translation examples.

**Conclusion:** The RAG pipeline is non-functional without its intended knowledge base. This confirms **Critical Inconsistency #1** identified in the code audit: the pipeline's core dependency is absent from the repository.

> **Note:** `ingest.py` and `rag_pipeline.py` are utility modules imported by `main.py`. They were exercised as part of the `main.py` execution and do not need to be run separately.

---

## 3. Issues & Fixes Log

| # | Script | Issue | Fix Applied | Severity |
|:-:|:-------|:------|:------------|:--------:|
| 1 | `cp2_extraction.py` | `pd.DataFrame \| None` type hint fails on Python 3.9 | Added `from __future__ import annotations` | Minor |
| 2 | `cp4_analysis.py` | Lowercase generic type hints fail on Python 3.9 | Added `from __future__ import annotations` | Minor |
| 3 | `cp3_socioeco.py` | Only 14/23 districts mappable via community area crosswalk | None — data limitation | Moderate |
| 4 | `main.py` | `combined_dataset.csv` missing → RAG returns irrelevant chunks | None — missing dependency | **Critical** |

---

## 4. Execution Summary

| Script | Runs? | Correct Output? | Notes |
|:-------|:-----:|:---------------:|:------|
| `cp2_extraction.py` | ✅ Yes | ✅ Yes (221 rows) | +1 row vs expected due to District 31 in 2022 |
| `cp2_eda.py` | ✅ Yes | ✅ Yes (5 files) | 4 plots + 1 summary CSV generated |
| `cp3_socioeco.py` | ✅ Yes | ✅ Yes (3 CSVs) | Only 14/23 districts mappable |
| `cp3_merge.py` | ✅ Yes | ✅ Yes (140 rows) | 81 rows dropped (9 unmapped districts) |
| `cp3_analysis.py` | ✅ Yes | ✅ Yes (6 files) | 3 OLS models, correlation table |
| `cp4_analysis.py` | ✅ Yes | ✅ Yes (13 files) | 4 models; District 12 drives significance |
| `main.py` | ⚠️ Partial | ❌ No SoQL output | RAG fails — missing `combined_dataset.csv` |

**Final tally:** 6/7 scripts execute successfully. 1 script (`main.py` / RAG pipeline) fails due to missing knowledge base file.

> **All scripts have been executed. Reproduction exercise complete.**
