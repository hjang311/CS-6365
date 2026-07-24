# Phase 3 Hybrid Prompt — Antigravity / Cursor

*Copy and paste the prompt below into a new Antigravity or Cursor chat. No API key required. The IDE agent drives one Phase 3 round by writing files and invoking the deterministic runner.*

**Paths assume repo root:** `/Users/hdj/Documents/CS-6365` (adjust if your clone differs).

---

**Copy the text below:**

You are the Orchestrator for the NORP Phase 3 rolled agentic loop (Checkpoint 4 / Grok_4.5). Execute one full round autonomously using the Hybrid Method (local tools / sub-agents). Do not ask for permission between steps.

**Targets:**
- **Evaluation artifact:** `Checkpoint 4/Grok_4.5/phase3_results/evaluation_summary.md`
- **Proposals output:** `Checkpoint 4/Grok_4.5/phase3_results/proposals_round1.json`
- **Runner:** `.venv/bin/python "Checkpoint 4/Grok_4.5/09_phase3_agentic_loop.py"`
- **Interpretation output:** `Checkpoint 4/Grok_4.5/phase3_results/round1_interpretation.md`

**Constraints (non-negotiable):**
1. You NEVER compute OLS coefficients yourself. Only the Python runner may fit models.
2. You MUST write `proposals_round1.json` **before** invoking `--run`.
3. Prefer external/structural IVs. Avoid mechanical DV components (`total_contributions`, `fundraising_expense_proxy`, fundraising event/professional fees).
4. Do not put control-set columns (`log_total_revenue`, `poverty_rate`, `median_hh_income`, `ntee_major`, `region`) as a lone two_var IV (collinearity with CONTROLS).
5. Include at least one `spec_type: "interaction"` proposal (`iv1`, `iv2`, `dv`).

**Your Instructions:**

1. **Ensure evaluation exists.** If `evaluation_summary.md` is missing, run:
   ```bash
   .venv/bin/python "Checkpoint 4/Grok_4.5/09_phase3_agentic_loop.py" --evaluate
   ```
   Then read `evaluation_summary.md` fully.

2. **Propose (pre-register).** Write `proposals_round1.json` with this shape:
   ```json
   {
     "provenance": {
       "built_by": "Grok_4.5",
       "round": 1,
       "source": "hybrid",
       "pre_registered_before_ols": true
     },
     "proposals": [
       {
         "id": "P01",
         "spec_type": "two_var",
         "iv": "...",
         "dv": "fundraising_efficiency_w",
         "expected_direction": "negative",
         "rationale": "..."
       },
       {
         "id": "P02",
         "spec_type": "interaction",
         "iv1": "...",
         "iv2": "...",
         "dv": "fundraising_efficiency_w",
         "expected_direction": "negative",
         "rationale": "..."
       }
     ]
   }
   ```
   Base rationales on what held vs failed in Phase 2 (H4 confirmed; H5 significant but theory rejected; 2-var limitation).

3. **Execute (deterministic).** Without waiting for further user input, run:
   ```bash
   .venv/bin/python "Checkpoint 4/Grok_4.5/09_phase3_agentic_loop.py" --run --round 1
   ```

4. **Interpret.** Read `round1_results.md`. Write `round1_interpretation.md` comparing observed vs expected directions. Suggest what Round 2 should propose (e.g. `soup_kitchen_density` after ACFB merge). Do not invent coefficients not present in the results file.

5. **Final synthesis.** Return a short summary: proposals written, `--run` exit code, confirmations/rejections, and path to `decision_log.jsonl`.

Do not ask for permission to proceed between steps. Complete the round autonomously and report only the final validated findings plus artifact paths.
