# Phase 7: Deterministic Agentic Loop — Student Guide & Documentation

This documentation covers the design, execution, and extension of the **Deterministic Agentic Loop** (`07_deterministic_loop.py`).

---

## 1. Architecture: Why a "Hybrid" Agentic Loop?

A purely programmatic loop (like a standard Python `for` loop) executes statistical equations rapidly but lacks the cognitive ability to contextualize results. A purely agentic loop (where the LLM writes and runs all the code) is highly flexible but prone to syntax errors, hallucinations, and API quota exhaustion.

The **Deterministic Agentic Loop** implements a **hybrid architecture**:
1. **Deterministic Orchestrator (Python):** Handles the data processing, listwise deletion, subsetting, and robust OLS regression math. This guarantees 100% mathematical reproducibility and zero hallucinations in the statistical metrics.
2. **Agentic Processor (LLM):** Acts as the active sociological researcher. In each iteration, it receives the variable names, reasons about the relationship, proposes a hypothesis direction and rationale *before* seeing the data, and then interprets the OLS results *after* they are generated.

---

## 2. The Per-Variable-Pair Agent Workflow

For every pair of variables $(IV, DV)$ tested, the loop executes a structured phase flow:

```
┌──────────────────────────────────────────────────────────┐
│ 1. SPECIALIZE & HYPOTHESIZE                              │
│    - Agent receives variable list + current IV & DV      │
│    - Agent suggests extra columns & cleaning rules       │
│    - Agent states hypothesis + lightweight prior art    │
└───────────────┬──────────────────────────────────────────┘
                ▼
┌──────────────────────────────────────────────────────────┐
│ 2. DETERMINISTIC OLS REGRESSION (Python)                 │
│    - Script subsets data, drops NaNs/Infs                │
│    - Runs OLS: DV ~ IV + controls (robust HC1)           │
│    - Records: beta, p-value, R², 95% CI, n               │
└───────────────┬──────────────────────────────────────────┘
                ▼
┌──────────────────────────────────────────────────────────┐
│ 3. AGENT INTERPRETATION                                  │
│    - Agent receives OLS coefficients & p-values          │
│    - Agent confirms/rejects the pre-analysis hypothesis  │
│    - Agent interprets findings sociologically            │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Execution Modes

The script features two mutually exclusive execution modes:

### A. Interactive Validation Mode (`--interactive`)
* **Purpose:** To verify that the loop architecture correctly reproduces established baseline findings (specifically H4 and H5) before running a full scan.
* **Usage:**
  ```bash
  python "Checkpoint 3/07_deterministic_loop.py" --interactive
  ```
* **Behavior:**
  - Evaluates only the two verification pairs: H4 (`log_zhvi_2022` $\to$ `fundraising_efficiency_w`) and H5 (`log_nonprofit_branch_density` $\to$ `fundraising_efficiency_w`).
  - Pauses at each stage and prompts the agent via standard input (`stdin`) to input its specialization, hypothesis, and interpretation in JSON format.
  - Automatically compares the resulting coefficients with baseline expected values and writes a `PASS/FAIL` report to `loop_results/validation_check.md`.

### B. Batch Combinatorial Mode (`--batch`)
* **Purpose:** To systematically scan all non-redundant combinations of variables in the modeling frame.
* **Usage:**
  ```bash
  python "Checkpoint 3/07_deterministic_loop.py" --batch
  ```
* **Behavior:**
  - Generates all valid, non-redundant pairs between the testable variables.
  - Runs the OLS regressions in a fast batch.
  - When a regression yields a statistically significant result ($p < 0.05$), the script pauses to prompt the agent to interpret the finding.
  - Outputs a complete summary table of all pairs to `loop_results/loop_summary.md` and detailed write-ups of significant results to `loop_results/significant_findings.md`.

---

## 4. Understanding the Output Files

All output is saved to the `Checkpoint 3/loop_results/` directory:

*   **`loop_summary.md`:** A comprehensive table containing every single pair tested, its OLS metrics, and whether the relationship was statistically significant.
*   **`significant_findings.md`:** Detailed sociological write-ups for all significant pairs ($p < 0.05$), documenting the pre-analysis hypothesis, OLS coefficients, post-analysis interpretation, and web-verified prior art citations.
*   **`validation_check.md`:** The PASS/FAIL validation report comparing interactive run results for H4 and H5 against expected baselines.
*   **`iteration_logs/`:** A subdirectory containing raw JSON files for each significant finding, serving as a complete audit trail.

---

## 5. Prior Art Search Methodology (Two-Tier Approach)

To balance speed and academic rigor, a **two-tier prior art approach** is utilized:
1.  **Lightweight Prior Art (In-Loop):** The agent cites 1-2 known papers or theoretical frameworks from its training memory during the loop iteration to help formulate the hypothesis.
2.  **Deep Prior Art & Novelty Search (Post-Loop):** For the top significant sociological findings, a focused web search is conducted to locate actual published papers testing the relationship. This verifies novelty and produces formal, verifiable citations appended to `significant_findings.md`.

---

## 6. How to Extend: Adding New Variables

To add new variables to the modeling loop:
1.  Add the new raw data files or columns to `Checkpoint 3/01_acquire_data.py` and `Checkpoint 3/02_merge_pipeline.py`.
2.  Add the column names to the testable variables pool in `Checkpoint 3/07_deterministic_loop.py`.
3.  If the new variables are closely related to existing ones (e.g. log transforms or winsorized variants), add them to a group in `REDUNDANCY_GROUPS` in `07_deterministic_loop.py` to prevent redundant loop pairs.
4.  Re-run the pipeline from Step 2:
    ```bash
    python "Checkpoint 3/02_merge_pipeline.py"
    python "Checkpoint 3/07_deterministic_loop.py" --batch
    ```
