# NORP Hybrid Pipeline — Autonomous Execution Prompt

*To run the NORP Agentic Pipeline on a new dataset seamlessly without back-and-forth guidance, copy and paste the prompt below into a new Antigravity chat. Replace the placeholder brackets `[ ]` with your specific dataset and variables before sending.*

---

**Copy the text below:**

You are the Orchestrator Agent for the NORP Data Exploration Pipeline. I need you to autonomously execute a statistical testing run on a new dataset using the "Hybrid Method" (running sub-agents locally within Antigravity).

**The Target:**
- **Dataset Path:** `[INSERT ABSOLUTE PATH TO DATASET CSV HERE]`
- **Independent Variable:** `[INSERT COLUMN NAME, e.g., Benefits_Health]`
- **Dependent Variable:** `[INSERT COLUMN NAME, e.g., BenefitsImpact]`

**Your Instructions:**
1. **Agent Initialization:** Immediately read the `SKILL.md` file located at `.agent/skills/norp-orchestrator/SKILL.md` to adopt your own specific workflow rules as the Orchestrator. Then, read the `SKILL.md` files located in the `.agent/skills/norp-code-agent` and `.agent/skills/norp-validator-agent` directories and use your `define_subagent` tool to register these two agents in your environment.
2. **Execute Code Agent:** Invoke the Code Agent and command it to load the target dataset, clean the independent and dependent variables, apply any necessary statistical weights (as per its Reproducibility Rules), and calculate the correlation between the two variables. Instruct it to save the cleaned subset data to a new folder named `[INSERT TEST FOLDER NAME, e.g., Test 2 Run]` and return the statistical percentages to you.
3. **Execute Validator Agent:** Without waiting for further user input, as soon as the Code Agent returns the cleaned dataset, invoke the Validator Agent. Command it to run programmatic Data Contracts (e.g., `assert` statements) against the cleaned dataset to prove there are no unexpected nulls or out-of-bound variables.
4. **Final Synthesis:** Once the Validator Agent confirms the data passes the contract, present me with a final summary of the statistical correlation findings. 

Do not ask me for permission to proceed between steps. Spawn the sub-agents and complete the entire pipeline autonomously, providing me only with the final validated findings and any artifacts generated.
