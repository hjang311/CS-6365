# Checkpoint 1 Report: Project Plan

## 1. Project Overview
Provide a clear understanding of the current state of the respective idea/related work to provide context and the starting point.

**Goal:** To investigate the relationship between community infrastructure (specifically broadband internet access) and the operational efficiency of local non-profit organizations.

**Final Hypothesis:** "Non-profit organizations located in communities with lower broadband internet access have lower fundraising efficiency (higher cost ratio)."

---

## 2. Evolution of Approach & Pivots

### Initial Approach: LLM-Agent-Driven Discovery
- **Concept:** Initially attempted to leverage LLM-driven autonomous agents to orchestrate data collection, processing, and analysis.
- **Challenges Encountered:** 
  - **Timeouts & Reliability:** Agent prompts were timing out on large-scale data downloads and processing.
  - **Data Complexity:** Handling edge cases (e.g., IEEE 754 subnormal float encoding in NCCS datasets) required precise, low-level programmatic interventions that were difficult to strictly enforce via conversational agents alone.
  - **Scalability:** Managing the cross-referencing of large files (like Census APIs, Zip-ZCTA crosswalks, and IRS BMF data) exceeded the practical context window and execution limits of standard agent-based execution.

### The Pivot: Robust Python Data Pipelines
- **Decision:** Shifted from an end-to-end LLM agent workflow to using the LLM (Antigravity/Cursor) as a pair-programmer to build deterministic, robust Python pipelines.
- **Implementation:** Created a 4-stage programmatic architecture:
  1. `01_acquire_data.py`: Downloads from IRS BMF, Census Broadband API, and NCCS CORE.
  2. `02_merge_pipeline.py`: Handles complex joining (ZIP to ZCTA crosswalk matching 99.5% of rows) and critical data decryptions (resolving subnormal float corruption in NCCS data).
  3. `03_analysis.py`: Runs statistical tests (Pearson/Spearman, OLS regression with controls for Revenue and NTEE categories).
  4. `04_validator.py`: A data contract and validation script to ensure data integrity and statistical soundness.

---

## 3. Current State & Results
- **Dataset:** 457 validated non-profit observations in Georgia (filtered for organizations with active revenues and relevant expenses).
- **Findings:** The analysis resulted in a null finding ($p=0.367$). We found no statistically significant relationship between the percentage of households lacking broadband internet and a non-profit's fundraising cost ratio.
- **Artifacts Generated:** 
  - `FINDINGS.md` (Detailed statistical tables)
  - `walkthrough.md` (Technical execution log)
  - `merged_georgia.csv` (Final processed dataset)

---

## 4. Next Steps
*To be filled out based on feedback and next report requirements.*
- [ ] Define the scope for Checkpoint 2.
- [ ] Determine whether to expand geographically beyond Georgia or refine the metrics of operational efficiency.
- [ ] Explore incorporating additional control variables (e.g., demographic or economic indicators).
