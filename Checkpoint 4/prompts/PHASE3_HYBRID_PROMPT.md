# Phase 3 Hybrid Prompt — IDE / agent host (canonical)

*Paste into any IDE or agent host that can write files, spawn sub-agents, and run a local shell (examples: Cursor, Claude Code, Codex, Antigravity 2.0). No separate Stats API key is required for OLS — the Python runner fits models.*

**Paths assume repo root:** `$REPO_ROOT` (your clone of this repository).

**Provenance note:** For the earlier build trail under `Checkpoint 4/provenance/early_build/`, see [`../provenance/early_build/prompts/PHASE3_HYBRID_PROMPT.md`](../provenance/early_build/prompts/PHASE3_HYBRID_PROMPT.md). That copy is **not** the student entrypoint.

---

**Copy the text below:**

You are the Orchestrator for the NORP Phase 3 rolled agentic loop (`Checkpoint 4/`). Execute one full round using hybrid IDE orchestration: you plan and synthesize; spawn Scout / Critic / Acquisition / Researcher as sub-agents when useful; invoke the deterministic Stats Engine for all OLS. Do not ask for permission between steps.

**Targets:**
- **Evaluation artifact:** `Checkpoint 4/phase3_results/evaluation_summary.md`
- **Proposals output:** `Checkpoint 4/phase3_results/proposals_round1.json`
- **Runner:** `.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py"`
- **Interpretation output:** `Checkpoint 4/phase3_results/round1_interpretation.md`
- **Skills:** `.agent/skills/norp-{orchestrator,scout,acquisition,researcher,validator-agent,code-agent}/SKILL.md`

**Constraints (non-negotiable):**
1. You NEVER compute OLS coefficients yourself. Only the Python runner may fit models.
2. You MUST write `proposals_round1.json` **before** invoking `--run`.
3. Prefer external/structural IVs. Avoid mechanical DV components (`total_contributions`, `fundraising_expense_proxy`, fundraising event/professional fees).
4. Do not put control-set columns (`log_total_revenue`, `poverty_rate`, `median_hh_income`, `ntee_major`, `region`) as a lone two_var IV (collinearity with CONTROLS).
5. Include at least one `spec_type: "interaction"` proposal (`iv1`, `iv2`, `dv`).
6. For higher-order rows, interpret `gate_decision` (HC1 Wald F + ΔR² ≥ 5e-4), not only the single interaction p-value.

**Your Instructions:**

1. **Ensure evaluation exists.** If `evaluation_summary.md` is missing, run:
   ```bash
   .venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --evaluate
   ```
   Then read `evaluation_summary.md` fully.

2. **Propose (pre-register).** Write `proposals_round1.json` with this shape (Researcher skill / sub-agent may author it):
   ```json
   {
     "provenance": {
       "built_by": "Phase3_Hybrid",
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
         "expected_direction": "unspecified",
         "rationale": "..."
       }
     ]
   }
   ```
   Base rationales on what held vs failed in Phase 2 (H4 confirmed; H5 significant but theory rejected; 2-var limitation). Prefer new density columns if an enrichment already ran.

3. **Execute (deterministic).** Without waiting for further user input, run:
   ```bash
   .venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --run --round 1
   ```
   If an enriched frame / slice is active, pass `--frame` from `agent_bus/enriched_frame_manifest.json`.

4. **Interpret.** Read `round1_results.md` / `.json`. Write `round1_interpretation.md` comparing observed vs expected directions and reporting gate ACCEPT/REJECT for interactions. Suggest what Round 2 should propose. Do not invent coefficients not present in the results file.

5. **Final synthesis.** Return a short summary: proposals written, `--run` exit code, confirmations/rejections/gates, and path to `decision_log.jsonl`.

Do not ask for permission to proceed between steps. Complete the round autonomously and report only the final validated findings plus artifact paths.

---

For the full Scout → Critic → Acquire → Research multi-agent round, use [`PHASE3_MULTI_AGENT_LOOP.md`](PHASE3_MULTI_AGENT_LOOP.md).
