# Project Plan Analysis — NORP_Spring26_G5

## CS 6365: Checkpoint 0 — Reproducibility Exercise
**Evaluator:** Hwando Jang
**Date:** May 25, 2026

---

## 1. Project Identity

| Field | Details |
|:---|:---|
| **Title** | Analysis of Socioeconomic Determinants of Violent Crime Using Retrieval-Augmented Query Generation |
| **Course** | CS 4365/6365: Intro to Enterprise Computing — Spring 2026, Georgia Tech |
| **Group** | 5 |
| **Members** | Khoa Bui, Khalid A Bargoti |
| **Repository** | [NORP_Spring26_G5](https://github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5) (forked from [KhalidBargoti/NORP](https://github.com/KhalidBargoti/NORP)) |

---

## 2. Stated Goals & Research Question

### 2.1 Central Research Question

> *"Has the relationship between district-level socioeconomic factors and violent crime rates changed before and after 2020?"*

This is a clear, well-scoped empirical question. It targets the year 2020 as a structural breakpoint — a meaningful choice given the societal disruptions of the COVID-19 pandemic, civil unrest following George Floyd's death, and shifts in policing practices. The question is testable, time-bounded (2015–2024), and geographically specific (Chicago police districts).

### 2.2 Two-Component Architecture

The project proposes two distinct but connected systems:

**Component A — Interactive RAG Pipeline (Original NORP System)**
- Accept natural language questions from users
- Retrieve similar query examples from a knowledge base using sentence embeddings
- Send context to an LLM to generate SoQL (Socrata Query Language) parameters
- Execute the generated query against the Chicago Crimes API
- Display results to the user

**Component B — Group 5 Extension: Longitudinal Crime Analysis**
A multi-checkpoint statistical analysis pipeline:
- **CP2:** Systematic extraction of violent crime counts by district and year (2015–2024)
- **CP2 EDA:** Exploratory data analysis with visualizations
- **CP3:** Integration of socioeconomic data (Chicago Hardship Index), panel dataset construction, and correlation/regression analysis
- **CP4:** Robustness checks including normalization, fixed effects, outlier analysis, and confidence interval estimation

### 2.3 Scope Definition

The project explicitly defines its scope through the checkpoint activity structure:

| Stage | Input | Processing | Output |
|:---|:---|:---|:---|
| CP2: Extraction | Chicago Crimes API | Filter 5 violent crime types, group by 22 districts × 10 years | 220-row CSV |
| CP2: EDA | Extraction CSV | Citywide trends, heatmaps, pre/post-2020 comparisons | 4 plots + summary CSV |
| CP3: Socioeconomic | Hardcoded ACS data + API crosswalk | Community area → district aggregation | 3 CSVs |
| CP3: Merge | Crime + socioeconomic CSVs | Inner join on district, add dummy variables | 140-row panel CSV |
| CP3: Analysis | Panel CSV | Pearson correlations, scatter plots, OLS regression | Correlation table + regression results + 4 plots |
| CP4: Robustness | Panel CSV | Normalization, statsmodels OLS, CI estimation, outlier exclusion | 5 data files + 6 plots |
| RAG Pipeline | User query + knowledge base | Embedding similarity → LLM generation → API execution | Query results |

---

## 3. Design Architecture Assessment

### 3.1 Pipeline Design

The project employs a **linear, sequential pipeline** with clear checkpoint demarcation:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Component B: Statistical Pipeline                │
│                                                                          │
│  cp2_extraction.py ──→ cp2_eda.py ──→ cp3_socioeco.py ──→ cp3_merge.py │
│                                                     │                    │
│                                                     └──→ cp3_analysis.py │
│                                                               │          │
│                                                               └──→ cp4_analysis.py │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                   Component A: RAG Pipeline (Independent)                │
│                                                                          │
│  ingest.py ──→ rag_pipeline.py ──→ main.py ──→ Crime_API.py            │
└──────────────────────────────────────────────────────────────────────────┘
```

**Strengths of this design:**
- Each script is self-contained with clearly defined inputs and outputs
- Data flows through well-defined file-based interfaces (CSVs)
- Scripts can be run and debugged independently
- Natural mapping to course checkpoint milestones

**Weaknesses of this design:**
- No unified orchestration — user must know and follow exact execution order
- No error propagation between stages (e.g., if CP2 produces unexpected data, CP3 will silently consume it)
- Two components are essentially independent projects sharing a directory — the RAG pipeline and the statistical analysis are not integrated

### 3.2 Technology Stack Choices

| Technology | Purpose | Assessment |
|:---|:---|:---|
| **OpenRouter API** | LLM access (free tier) | Smart choice — avoids expensive OpenAI billing, provides access to multiple free models |
| **Socrata API (SoQL)** | Chicago crime data access | Appropriate — this is the official API for the Chicago Data Portal |
| **sentence-transformers (MiniLM-L6-v2)** | Embedding generation for RAG | Reasonable — lightweight, fast, effective for semantic similarity |
| **statsmodels** | OLS regression with full statistical output | Excellent choice for CP4 — provides p-values, CIs, R², which `numpy.linalg.lstsq` in CP3 lacks |
| **pandas + matplotlib + seaborn** | Data manipulation + visualization | Standard and appropriate |
| **Manual cosine similarity** | RAG retrieval | Functional but simplistic — could use vector databases like ChromaDB (which is in requirements.txt but unused) |

### 3.3 Data Sources

| Source | Type | Quality |
|:---|:---|:---|
| [Chicago Crimes API](https://data.cityofchicago.org/resource/crimes.json) | Live API (Socrata) | Authoritative — official City of Chicago data portal, well-documented |
| Chicago Hardship Index (2008-2012 ACS) | Hardcoded in `cp3_socioeco.py` | Valid data, but temporal mismatch — 2008-2012 socioeconomic data applied to 2015-2024 crime data |
| RAG knowledge base (`combined_dataset.csv`) | Pre-built CSV of NL→SoQL pairs | **Critical: NOT included in the repository** |

---

## 4. Ambition Assessment

### 4.1 Classification: **Substantial Project**

This project is clearly beyond "Hello World" and into **substantive territory** for several reasons:

1. **Genuine research question:** The pre/post-2020 structural break hypothesis is a real empirical question with social relevance — not a toy example.

2. **Multi-stage analytical pipeline:** The CP2→CP3→CP4 progression shows iterative refinement — from raw extraction to EDA to regression to robustness checks. This mirrors genuine research methodology.

3. **Statistical rigor:** CP4's use of proper OLS with p-values, confidence intervals, interaction terms for structural break testing, and outlier robustness analysis (excluding District 12) demonstrates methodological maturity.

4. **Dual-system architecture:** The combination of a RAG-powered natural language interface (Component A) and a systematic statistical analysis (Component B) shows breadth of technical scope.

5. **Real-world data integration:** Using live API data from the Chicago Data Portal and linking it with socioeconomic indicators via a community-area-to-district crosswalk demonstrates practical data engineering skills.

### 4.2 What Elevates It Beyond "Hello World"

| Aspect | Hello World Level | This Project's Level |
|:---|:---|:---|
| Data source | Static file or toy dataset | Live API with 10-year historical range |
| Analysis | Basic summary statistics | OLS regression with structural break interaction testing |
| Visualization | 1-2 simple plots | 14+ publication-quality plots with CI bands |
| Methodology | Single-pass analysis | Iterative: EDA → regression → robustness validation |
| AI component | Basic LLM prompt | Full RAG pipeline with embeddings + retrieval + generation |

### 4.3 What Keeps It Below 120%

The project does not quite reach "exceptional" territory because:

1. **Components are disconnected.** The RAG pipeline (Component A) and the statistical analysis (Component B) don't interact — you can't ask the RAG system questions about the CP3/CP4 findings, and the analysis pipeline doesn't use the RAG system.

2. **No automation.** There is no single command to run the full pipeline. No `Makefile`, no `run_all.sh`, no orchestration script.

3. **The RAG component is relatively thin.** The retrieval is basic cosine similarity over row-level chunks. There is no chunking strategy, no re-ranking, no evaluation of retrieval quality.

4. **Temporal mismatch in socioeconomic data.** Using 2008-2012 ACS data for a 2015-2024 analysis is a known limitation that they acknowledge but don't attempt to address.

---

## 5. Strengths of the Plan

1. **Clear documentation.** The README (212 lines) and INSTRUCTIONS (239 lines) are thorough, providing step-by-step execution guides, data source references, schema definitions, and key findings.

2. **Well-defined violent crime criteria.** Using the FBI UCR definition with 5 explicit crime types ensures analytical clarity.

3. **Methodological progression.** The CP2 → CP3 → CP4 structure mirrors genuine research practice: explore → model → validate.

4. **Reproducibility-conscious design.** Scripts auto-create `data/` and `plots/` directories, read API keys from `.env`, and document execution dependencies.

5. **Key findings are stated upfront.** The README and INSTRUCTIONS clearly state the major results (hardship correlation drop from +0.349 to +0.072, income sign reversal), making verification straightforward.

---

## 6. Weaknesses of the Plan

1. **Missing critical data file.** The `data/combined_dataset.csv` RAG knowledge base is not included in the repository, making Component A (the headline feature) non-functional out of the box.

2. **Documentation-code mismatches.** The README states the LLM model is `mistralai/devstral-2512:free` but the code uses `openai/gpt-oss-20b:free`. Step 6 in the README says to run `cp3_analysis.py` when describing `cp4_analysis.py` functionality.

3. **Dead dependencies.** Five packages in `requirements.txt` (`langchain`, `chromadb`, `tiktoken`, `faiss-cpu`, `openai`) are never used — suggesting leftover development artifacts or a pivot away from an original architecture.

4. **No testing framework.** There are no unit tests, integration tests, or validation scripts. The only way to verify correctness is manual inspection of outputs.

5. **Single commit history.** The entire project was submitted in one commit ("Adding Project Files"), providing no visibility into the development process, decision-making, or iterative progress.

6. **API-dependent reproducibility.** The pipeline requires two external API keys and live network access, introducing external failure points.

---

## 7. Score Recommendation for "Plan" Metric

### **Proposed Score: 90% / 120%**

### Reasoning:

The NORP_Spring26_G5 project presents a **substantial and well-structured plan** with a genuine research question, multi-stage analytical pipeline, and dual-system architecture. The research question is socially relevant and empirically testable. The documentation is thorough, with clear execution instructions and stated findings.

However, the plan falls short of the maximum for several reasons:

- The **two components are disconnected** — the RAG pipeline and the statistical analysis don't interact, reducing the system's cohesion as an enterprise computing project.
- **No automation or orchestration** is provided — the user must manually execute 6+ scripts in correct order.
- The **RAG component is architecturally thin** — basic cosine similarity over flat row chunks, with more sophisticated tools (ChromaDB, LangChain) listed as dependencies but never used, suggesting a planned-but-abandoned more sophisticated design.
- The **temporal mismatch** between socioeconomic data (2008-2012) and crime data (2015-2024) is acknowledged but not addressed.

The plan is clearly "Substantial" — well above Hello World — but does not reach the "Exceeds Expectations" threshold that would warrant scores above 100%.
