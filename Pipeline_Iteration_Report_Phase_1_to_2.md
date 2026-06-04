# Project Checkpoint: Pipeline Iteration & Autonomous Discovery Transition
**Course:** CS 6365 Enterprise Computing
**Project:** NORP Agentic Data Exploration Pipeline

## Executive Summary
This document outlines the iteration and development progress of the NORP Multi-Agent Data Pipeline. Based on recent feedback, we transitioned the pipeline from a targeted execution engine into a "Data Scientist in a Box"—capable of fully autonomous correlation discovery while maintaining strict programmatic validation against statistical hallucinations.

---

## 1. Phase 1: The "Gold Standard" Targeted Test
To ensure the mathematical foundation of our pipeline was sound, we executed a targeted "Gold Standard" test against the `YEAR-04-DATA-PUF.csv` dataset. Our goal was to independently reproduce the correlations cited in the *Health of the U.S. Nonprofit Sector 2025* report.

### The Runthrough
* **Method:** We used a Hybrid Execution model, loading the declarative agent rules from `.agent/skills/` into local sub-agents.
* **The Test:** We instructed the Orchestrator to calculate the correlation between `Benefits_Health` and `BenefitsImpact`.
* **The Finding:** The Code Agent successfully flattened the data, mapped the 1-5 Likert scales, and mathematically calculated that **76.4%** of organizations reporting a positive impact offer health insurance, compared to **16.5%** for those reporting a negative impact.
* **The Validation:** The Validator Agent enforced a strict Python Data Contract, running `assert` statements to mathematically prove the final dataset contained zero nulls or outlier Likert variables. 

### The Reproducibility Fix
During testing, we discovered a discrepancy between different LLM environments (Claude Code vs. Antigravity/Gemini). Claude calculated unweighted raw percentages (74.9%), while Antigravity correctly discovered and applied the dataset survey weights (`year4wt`) to hit the 76.4% target.
* **The Solution:** We updated the Code Agent's system prompt (`SKILL.md`) with explicit **Statistical & Data Reproducibility Rules**, hardcoding the instruction to *always* search for and apply statistical survey weights, ensuring 100% mathematical reproducibility regardless of the LLM runner.

---

## 2. Phase 2: Upgrading to Fully Autonomous Discovery
With the mathematical foundation validated, we shifted our architecture to mirror state-of-the-art academic frameworks (such as the *Data Interpreter* methodology) to enable proactive, unprompted discovery.

### The "Brain" Upgrades (.agent/skills/ changes)
We upgraded the system instructions for all three agents to handle autonomous execution:

1. **The Orchestrator:** Instead of waiting for specific variables, the Orchestrator is now programmed to initiate a "Sweep-and-Propose" workflow, commanding the Code Agent to run generalized correlation matrices (e.g., Pearson/Spearman) across all numerical columns.
2. **The Code Agent:** The Code Agent was upgraded to autonomously calculate the exact p-values (e.g., via `scipy.stats`) for every correlation it discovers. It filters the output to only return statistically significant findings ($p < 0.05$).
3. **The Validator Agent (Statistical Peer Review):** We transformed the Validator from a basic schema checker into a strict statistical auditor. It now writes programmatic assertions to independently calculate the p-value of the Code Agent's claims. If `assert p < 0.05` fails, the insight is rejected.

---

## 3. The New Testing Environment
Our project now features two distinct prompts stored in `agentic_pipeline/` to trigger different execution modes within the Antigravity desktop app or headless SDK:
*   `hybrid_test_prompt_template.md`: Forces manual variable targeting for Phase 1 baseline checks.
*   `autonomous_test_prompt.md`: Drops the leash and commands the Orchestrator to independently hunt for new, undiscovered sociological correlations for Phase 2.
