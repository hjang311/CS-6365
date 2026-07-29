# `agentic_pipeline/` — Legacy Antigravity SDK scaffolding

**Not the Phase 3 student entrypoint.** Do **not** run `python main.py` for the rolled loop.

## What this folder was

Early-semester **Google Antigravity SDK** factories and a Checkpoint 1 triage demo: load skill text into `Agent` objects, profile Form 990 CSVs, and drive short orchestrator chats. That path proved useful for learning the SDK; it is **not** how Phase 3 is taught now.

## What to use instead (hybrid IDE orchestration)

Phase 3 uses **host agent + sub-agents + deterministic Stats Engine**:

1. Paste [`Checkpoint 4/prompts/PHASE3_MULTI_AGENT_LOOP.md`](../Checkpoint%204/prompts/PHASE3_MULTI_AGENT_LOOP.md) (or the shorter [`PHASE3_HYBRID_PROMPT.md`](../Checkpoint%204/prompts/PHASE3_HYBRID_PROMPT.md)) into your IDE / agent host.
2. Load role contracts from [`.agent/skills/norp-*`](../.agent/skills/).
3. Spawn Scout / Critic / Acquisition / Researcher as **sub-agents** (whatever your host provides).
4. Fit OLS **only** via:

```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --run ...
```

Works in Cursor, Claude Code, Codex, Antigravity 2.0, or any host that can orchestrate, spawn sub-agents, and invoke the local CLI. Offline demos: `bash "Checkpoint 4/reproduce.sh"`. Curriculum: [`docs/CURRICULUM.md`](../docs/CURRICULUM.md). Studio map: [`Checkpoint 4/docs/STRUCTURE.md`](../Checkpoint%204/docs/STRUCTURE.md). Project state: [`AGENTS.md`](../AGENTS.md).

## File map

| File | Status | Meaning |
|------|--------|---------|
| `agents.py` | Optional / future SDK wiring | Factories that load `.agent/skills/norp-*` into Antigravity `Agent` objects (`create_phase3_agents()`). Not required for hybrid IDE runs. |
| `main.py` | Historical CP1 | Old triage-gate orchestrator demo — **not** Phase 3. |
| `ingest_and_profile.py` | Historical CP1 | Form 990 profiling helper from the foundation phase. |
| `autonomous_test_prompt.md` | Superseded | CP1 discovery prompt (correlation sweeps). Conflicts with Phase 3 scientific rules. |
| `hybrid_test_prompt_template.md` | Superseded | CP1 hybrid prompt template. Use `Checkpoint 4/prompts/` instead. |
| `requirements.txt` | SDK-era deps | Only needed if you intentionally revive the Antigravity SDK path. |
| `.env` / `venv/` | Local only | Gitignored; never commit secrets. |

## Scientific reminder

LLM agents **never** invent OLS coefficients. Named adapters only; Critic ToS gates; pre-register proposals before `--run`. See hard rules in [`AGENTS.md`](../AGENTS.md).
