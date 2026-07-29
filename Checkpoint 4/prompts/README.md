# Checkpoint 4 prompts

Paste-ready prompts for **hybrid IDE orchestration**: the host agent acts as Orchestrator, optionally spawns Scout / Critic / Acquisition / Researcher as sub-agents, and fits OLS **only** via `09_phase3_agentic_loop.py`.

**Behavior contracts** live in `.agent/skills/norp-*` — do not duplicate long skill text here.

| File | Role |
|------|------|
| [`PHASE3_MULTI_AGENT_LOOP.md`](PHASE3_MULTI_AGENT_LOOP.md) | Master hybrid loop (Scout → Critic → Acquire → Research → `09`) |
| [`PHASE3_HYBRID_PROMPT.md`](PHASE3_HYBRID_PROMPT.md) | Shorter single-round hybrid entry (**canonical** paths) |
| [`PHASE3_ACFB_ZIP_COLLECT_PROMPT.md`](PHASE3_ACFB_ZIP_COLLECT_PROMPT.md) | ZIP collection helper (ToS-aware) |
| [`agents/`](agents/) | One-page role pointers → skills |

**Provenance:** [`../provenance/early_build/prompts/`](../provenance/early_build/prompts/) keeps earlier-build hybrid prompts. Not the student entrypoint. Studio map: [`../docs/STRUCTURE.md`](../docs/STRUCTURE.md).

## How to run hybrid orchestration (any IDE / agent host)

Works in Cursor, Claude Code, Codex, Antigravity 2.0, or any host that can write repo files, spawn sub-agents, and run a local shell. No single vendor is required.

1. Open a new agent chat at the **repo root**.
2. Paste [`PHASE3_MULTI_AGENT_LOOP.md`](PHASE3_MULTI_AGENT_LOOP.md) (full round) or [`PHASE3_HYBRID_PROMPT.md`](PHASE3_HYBRID_PROMPT.md) (shorter propose → `--run` → interpret).
3. Host agent loads [`.agent/skills/norp-orchestrator/SKILL.md`](../../.agent/skills/norp-orchestrator/SKILL.md) and plans the round.
4. Spawn sub-agents for Scout / Critic / Acquisition / Researcher, each pointed at the matching `.agent/skills/norp-*/SKILL.md` and file bus under `Checkpoint 4/phase3_results/agent_bus/`.
5. Invoke Stats **only** via:
   ```bash
   .venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --run --round N ...
   ```
6. Offline alternative (no live sub-agents): `bash "Checkpoint 4/reproduce.sh"`.

Hard rule: **only** `09_phase3_agentic_loop.py` fits OLS. Paths in prompts use `$REPO_ROOT` (your clone root).

## Agent role pointers

| Stub | Skill |
|------|-------|
| `agents/ORCHESTRATOR.md` | `.agent/skills/norp-orchestrator/` |
| `agents/SCOUT.md` | `.agent/skills/norp-scout/` |
| `agents/CRITIC.md` | `.agent/skills/norp-validator-agent/` + Critic ToS rules in acquisition skill |
| `agents/ACQUISITION.md` | `.agent/skills/norp-acquisition/` |
| `agents/RESEARCHER.md` | `.agent/skills/norp-researcher/` |

Legacy Antigravity SDK factories (optional, not student entry): [`agentic_pipeline/`](../../agentic_pipeline/).
