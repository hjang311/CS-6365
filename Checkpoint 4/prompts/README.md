# Checkpoint 4 prompts

Use these for hybrid IDE sessions. **Behavior contracts** live in `.agent/skills/norp-*` — do not duplicate long skill text here.

| File | Role |
|------|------|
| [`PHASE3_MULTI_AGENT_LOOP.md`](PHASE3_MULTI_AGENT_LOOP.md) | Master hybrid loop prompt |
| [`PHASE3_HYBRID_PROMPT.md`](PHASE3_HYBRID_PROMPT.md) | Shorter hybrid entry |
| [`PHASE3_ACFB_ZIP_COLLECT_PROMPT.md`](PHASE3_ACFB_ZIP_COLLECT_PROMPT.md) | ZIP collection helper (ToS-aware) |
| [`agents/`](agents/) | One-page role pointers → skills |

## Agent role pointers

| Stub | Skill |
|------|-------|
| `agents/ORCHESTRATOR.md` | `.agent/skills/norp-orchestrator/` |
| `agents/SCOUT.md` | `.agent/skills/norp-scout/` |
| `agents/CRITIC.md` | `.agent/skills/norp-validator-agent/` + Critic ToS rules in acquisition skill |
| `agents/ACQUISITION.md` | `.agent/skills/norp-acquisition/` |
| `agents/RESEARCHER.md` | `.agent/skills/norp-researcher/` |

Hard rule: **only** `09_phase3_agentic_loop.py` fits OLS. Paths in prompts use `$REPO_ROOT` (your clone root).
