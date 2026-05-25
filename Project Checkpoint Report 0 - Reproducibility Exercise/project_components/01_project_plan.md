# Project Plan Analysis — NORP_Spring26_G5

## Overview

This document analyzes the **Project Plan** component of the NORP_Spring26_G5 project package, focusing on the overall goals, design, and scope outlined by the original team.

---

## 1. Stated Goals

<!-- TODO: Fill in after reviewing the NORP project's README.md and INSTRUCTIONS.md -->

### 1.1 Primary Objectives
- Crime data extraction and integration
- Geospatial analysis of crime data
- RAG pipeline for intelligent querying of crime-related information
- Multi-stage pipeline architecture (CA1 through CA4)

### 1.2 Technical Scope
Based on the repository file structure, the project appears to follow a multi-checkpoint activity structure:

| Activity | File(s) | Apparent Goal |
|:---|:---|:---|
| **CA1: Setup** | `ca1_setup.py` | Environment and database setup |
| **CA2: Extraction** | `ca2_extraction.py` | Crime data extraction from APIs |
| **CA3: Analysis** | `ca3_analysis.py`, `ca3_merge.py`, `ca3_geodata.py` | Data analysis, merging, and geospatial processing |
| **CA4: Analysis** | `ca4_analysis.py` | Advanced analysis |
| **RAG Pipeline** | `rag_pipeline.py`, `ingest.py` | Retrieval-Augmented Generation system |

---

## 2. Design Architecture

<!-- TODO: Document the project's architectural choices -->

### 2.1 Pipeline Design
The project uses a sequential checkpoint activity (CA) architecture:
```
CA1 (Setup) → CA2 (Extraction) → CA3 (Analysis/Merge/Geo) → CA4 (Advanced Analysis)
                                                                      ↓
                                                              RAG Pipeline (ingest + query)
```

### 2.2 External Dependencies
- **Crime API:** External data source (key stored in `CrimeAPIkey`)
- **Environment variables:** Configuration via `.env` file
- **Python packages:** Specified in `requirements.txt`

---

## 3. Plan Assessment

### 3.1 Strengths
<!-- TODO: Document strengths of the plan -->

### 3.2 Weaknesses
<!-- TODO: Document weaknesses of the plan -->

### 3.3 Ambition Level
<!-- TODO: Classify: Empty Demo / Hello World / Substantial -->

---

## 4. Score Recommendation for "Plan" Metric
<!-- TODO: Assign percentage (up to 120%) -->

**Proposed Score:** TBD / 120%

**Reasoning:** TBD
