# Georgia Institute of Technology
## CS 4365/6365: Introduction to Enterprise Computing
### Summer 2026
**Project Checkpoint 1 Report**

**Group:** G5  
**Name(s):** HDJ, Carla  
**Project Name:** NORP Agentic Data Exploration Pipeline  

---

## Context and Related Work: Project Plan (Plan)
The project aims to build an Agentic Data Exploration Layer utilizing the Google Antigravity SDK. The primary goal is to use an autonomous 3-agent pipeline (Orchestrator, Code Agent, Validator/Critic) to discover insightful sociological correlations between external socioeconomic indicators and non-profit performance. Our starting point involved migrating from a legacy portal architecture to a fully agentic framework, utilizing the *Health of the U.S. Nonprofit Sector 2025* report as our baseline "Gold Standard" to mathematically validate the pipeline's logic against a Form 990 dataset.

## Project Deliverables

| Deliverable | Description | Technical Stack |
| :--- | :--- | :--- |
| **3-Agent Pipeline Codebase** | The Python scripts and declarative Markdown skills defining the Orchestrator, Code, and Validator agents. | Python, Google Antigravity SDK, `.agent/skills/` |
| **Cleaned Datasets & Scripts** | The `#Factual` evidence including the cleaned sub-schemes, applied survey weights, and auto-generated REPL `.py` scripts. | Pandas, Scipy, PyArrow |
| **Final Presentation** | A PowerPoint slide deck synthesizing the pipeline's autonomous discoveries. | PowerPoint |

## Project Milestones

| Checkpoint | Milestone | Technical Scope & Deliverables | Work Splitup | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Checkpoint 1** | Baseline Exploration & "Gold Standard" Validation | Build Hybrid Skills framework. Run targeted correlation test (e.g. Health Benefits vs Impact). Ensure mathematical reproducibility. | HDJ & Carla | **Complete** |
| **Checkpoint 2** | Fully Autonomous Discovery Execution | Upgrade to Autonomous EDA. Agents autonomously scan all columns and output top 5 correlations using p-values. | HDJ & Carla | In Progress |
| **Checkpoint 3** | External Data Integration | Source novel socioeconomic datasets (Kaggle/Data.gov). Merge with 990 anchor. Pipeline autonomously critiques and finds novel insights. | HDJ & Carla | Not Started |
| **Checkpoint 4** | Synthesis, Presentation & Final Deliverables | Compile `#Factual` evidence. Finalize PowerPoint presentation on methodology and sociological findings. | HDJ & Carla | Not Started |

## Current Progress Report (Match)
* **Report on work done:** During the last two weeks, we successfully re-architected the project into a 3-agent system (Orchestrator, Code, Validator) utilizing a Hybrid Skills Model to save API costs. We successfully executed Phase 1 by running a targeted test against the `YEAR-04-DATA-PUF.csv` dataset. The pipeline reproduced the 76.4% Likert finding from the 2025 Independent Sector report.
* **Comparison with initial plan:** We are ahead of schedule. We successfully achieved the Gold Standard validation. During this phase, we also resolved a mathematical reproducibility bug regarding survey weights (`year4wt`) and hardcoded the fix into the agents' instructions.
* **Planned work for next 2 weeks:** For Checkpoint 2, we will deploy the `autonomous_test_prompt.md`. This drops the "leash" and allows the agents to run a massive, generalized correlation matrix across all numerical columns without human intervention, returning only statistically significant findings ($p < 0.05$).
* **Changes to original plan:** Based on TA and Professor feedback, the pipeline itself is the primary novelty. We shifted to a "Targeted Approach" for Phase 1 to prove the tech works, and explicitly defined Phase 2 and 3 as the search for *new* external data (the "real project") rather than just cleaning the existing Metabase.

## Supporting Evidence (Factual)
*   **Pipeline Iteration Report:** Detailed breakdown of the test run, mathematical findings, and bug fixes: `Pipeline_Iteration_Report_Phase_1_to_2.md`
*   **Agent Skills Framework:** The declarative instructions for the 3 agents: `.agent/skills/`
*   **Autonomous Test Prompt:** The newly generated execution file for Ckpt 2: `agentic_pipeline/autonomous_test_prompt.md`
*   **Pipeline Codebase:** The Python SDK execution loop: `agentic_pipeline/agents.py` & `main.py`

## Skill Learning Report
*   **Google Antigravity SDK & Agent Architecture:** Learned how to decouple LLM reasoning from execution by building a 3-agent (Manager, Executor, Critic) structure using the Antigravity local sandbox environment.
*   **Python (Pandas/Scipy):** Implementing statistical programmatic validation and enforcing the application of survey weights (`year4wt`) to ensure data accuracy.
*   **Prompt Engineering:** Evolving from manual, targeted LLM prompts to "Autonomous Discovery" instructions where the agent initiates its own "Sweep-and-Propose" loop.

## Self-Evaluation
*   **Plan:** 5/5
*   **Match:** 5/5
*   **Factual:** 5/5

## LLM Feedback: 
*   **Project Plan (Plan):** 5/5 (The hybrid plan securely anchors the project's academic goals).
*   **Progress Report (Match):** 5/5 (Achieving Gold Standard validation and catching the survey weight bug proves technical competence).
*   **Supporting Evidence (Factual):** 5/5 (The GitHub repo cleanly separates the legacy code from the new agentic framework).

## Actionable Suggestions:
*   Ensure that the external datasets sourced for Checkpoint 3 have clear primary keys (e.g., ZIP codes, EINs) that can be easily merged with the Form 990 anchor data by the Code Agent.
