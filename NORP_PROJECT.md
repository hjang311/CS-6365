# NORP: Agentic Data Exploration Pipeline
## CS 6365 Enterprise Computing Semester Project

---

## 📌 Executive Summary

Modern Non-Profit Organizations (NPOs) generate and report massive amounts of data (such as IRS Form 990s). However, synthesizing this data with external, often messy datasets (from Data.gov, Kaggle) to find actionable sociological correlations is highly labor-intensive.

The **NORP Agentic Data Exploration Pipeline** utilizes the **Google Antigravity SDK** to orchestrate an autonomous multi-agent system. This system acts as a "Data Scientist in a Box", autonomously triaging raw datasets, writing code to clean and merge them, and programmatically verifying the results before applying statistical models.

---

## 🛠️ System Architecture

Our architecture is structured around a pipeline of specialized AI agents:

### 1. The Orchestrator Agent
* **Role:** The high-level strategic planner.
* **Function:** Receives sociological hypotheses, determines the necessary data transformations, and delegates Python coding tasks to the subordinate agents. 

### 2. The Code Agent (REPL Sandbox)
* **Role:** The execution engine.
* **Function:** Operates inside a Python REPL environment. It writes, executes, and iteratively debugs `pandas` and `scikit-learn` scripts to process Form 990 data.

### 3. Pipeline Stages
* **Stage 1: Triage Gate:** The Code Agent writes statistical profiling scripts to assess the "health" of a raw dataset. If a dataset is completely unresolvable, the system applies a **"Drop and Move" heuristic** to skip it.
* **Stage 2: Cleaning Pipeline:** The system autonomously handles nulls, outliers, and schema alignment to join external data with the Form 990 anchor.
* **Stage 3: Programmatic Verification:** The system writes assertions (verifying distributions and schema integrity) to mathematically prove the data is clean.
* **Stage 4: Math & Correlation Engine:** The Code Agent generates regression models and calculates **Context-Adjusted Performance Scores** for non-profits based on geographic archetypes (e.g., Rust Belt vs. Sun Belt).

### 4. Hybrid Execution Architecture (Skills vs SDK)
The project utilizes a dual-engine "Hybrid Strategy" to separate the agent logic (the "Brain") from the execution environment (the "Engine"):
* **The Skills Model:** All agent behaviors, rules, and system instructions are written as declarative Markdown files and stored in the `.agent/skills/` directory. This allows for zero-cost, iterative testing and sub-agent delegation natively within the Antigravity desktop app.
* **The SDK Model:** When the pipeline is ready for production, the `google-antigravity` Python SDK is used as a headless framework. The `agents.py` scripts dynamically read the exact same Markdown files from the `.agent/skills/` directory, guaranteeing 100% reproducible outputs between local testing and remote server deployment.

---

## 📈 Project Milestones (Summer 2026)

Our progress is tracked through specific phases aligned with the CS 6365 DevOps checkpoints:

* **Phase 1: Foundation & Triage Gate**
  * Establish the Python `agentic_pipeline` environment.
  * Implement the Orchestrator and Code agents.
  * Build the initial data profiling script for the core 990 CSV.
* **Phase 2: Autonomous Cleaning Pipeline**
  * Implement the "Drop and Move" heuristic.
  * Autonomously merge external datasets with the anchor data.
* **Phase 3: Auto-Verification & Math Engine**
  * Implement the Context-Adjusted Performance Score mathematics.
  * Generate factual regression models proving sociological correlations.
* **Phase 4: Synthesis & Presentation**
  * Finalize the `#Factual` evidence and prepare the final deliverables.
