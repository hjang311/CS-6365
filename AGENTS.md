# AGENTS.md — Project State for Collaborators and LLMs

This file is the **handoff state** for humans and coding agents working in this repository.

## What this repo is

Education-first **Manual → Unrolled → Rolled** NORP pipeline (CS 4365/6365 Summer 2026, Team 1). July 22 OH Option 2: teach workflow / loop engineering to the next cohort — not promotional video packaging.

## Canonical vs provenance

| Path | Status |
|------|--------|
| `Checkpoint 4/09_phase3_agentic_loop.py`, `engine/`, `configs/`, `reproduce.sh` | **Canonical** Phase 3 Stats Engine |
| `Checkpoint 4/prompts/` | **Canonical** paste-ready hybrid orchestrator prompts |
| `Checkpoint 4/docs/` | CP4 teaching docs + `STRUCTURE.md` studio map |
| `.agent/skills/norp-*` | Canonical agent skill / role contracts |
| `Checkpoint 2/H2_Pipeline/`, `Checkpoint 3/H4/`, `H5/`, `08_unrolled_loop.py` | Canonical Manual / Unrolled |
| `Checkpoint 4/provenance/early_build/` | **Provenance only** — earlier build trail; not the student entrypoint |
| `archive/` (local) | Local-only semester clutter — gitignored |
| `Checkpoint 0/` | **Prior-semester case study only** — shows what earlier cohorts had to do. **Not** Phase 1 of this curriculum |
| `Checkpoint 4/docs/internal/PRESENTATION_OUTLINE.md` | Team presentation workspace — **gitignored**; not a student deliverable |
| `agentic_pipeline/` | **Legacy** Antigravity SDK scaffolding — documented; not Phase 3 entry |

## Hybrid IDE orchestration

Preferred live Phase 3 path (IDE-agnostic): **host agent as Orchestrator** → spawn Scout / Critic / Acquisition / Researcher as **sub-agents** → file bus under `phase3_results/agent_bus/` → **only** `09 --run` fits OLS.

- Prompts: `Checkpoint 4/prompts/PHASE3_MULTI_AGENT_LOOP.md` (full) or `PHASE3_HYBRID_PROMPT.md` (short)
- Skills: `.agent/skills/norp-*`
- Studio map: `Checkpoint 4/docs/STRUCTURE.md` (Run / Orchestrate / Extend)
- Hosts (examples, not requirements): Cursor, Claude Code, Codex, Antigravity 2.0
- Offline demos without live sub-agents: `bash "Checkpoint 4/reproduce.sh"`

`agentic_pipeline/agents.py` remains optional SDK wiring for a future Antigravity process — see that folder’s README.

## Complete / do not rebuild unless asked

- Manual H2 / H4 / H5 pipelines and verification write-ups
- Unrolled List A/B engine (`08`) and `loop_results_v2/`
- Rolled multi-agent loop + HC1 Wald F + ΔR² ≥ 5e-4 Verifier gate
- Offline `reproduce.sh` demos (requires `Checkpoint 3/data/cp3_modeling_frame.csv`)
- CP3 carry-forwards: `RQ2/RQ2_VERIFICATION_RUN.md`, `MODE_B_DRIFT.md`

## Hard scientific rules

1. **LLM never fits OLS.** Only `09_phase3_agentic_loop.py --run` / validation / verify paths fit models (HC1).
2. **Pre-register before OLS** for exploratory agendas (List A/B; Phase 3 proposals JSON).
3. **Higher-order ACCEPT** only if Wald F p < 0.05 **and** ΔR² ≥ 5e-4 on identical rows.
4. **Null / gate REJECT are first-class** — document them; do not bury them.
5. **Critic ToS gates** — do not scrape login-walled directories; use named adapters.

## Extend, don’t rewrite

Prefer extending configs, adapters, and docs over rewriting the Stats Engine or wiping results trees. If changing OLS formulas or gate thresholds, update `docs/HYPOTHESIS_REGISTRY.md`, `NEGATIVE_FINDINGS.md`, and the Checkpoint 4 report in the same change.

## Entrypoints

```bash
bash "Checkpoint 4/reproduce.sh"
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --validate
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --verify-ta-specs \
  --out "Checkpoint 4/phase3_results/ta_verify"
```

Prefer `reproduce.sh` first — it preflights the gitignored modeling frame and prints Mode A/B regenerate steps. Direct `09 --validate` / `--verify-ta-specs` / `--run` assume `Checkpoint 3/data/cp3_modeling_frame.csv` already exists (same cliff; see root README and `Checkpoint 3/MODE_B_DRIFT.md`).

Student path: `Checkpoint 4/docs/STUDENT_QUICKSTART.md` → `docs/CURRICULUM.md` → `Checkpoint 4/docs/BENCHMARK.md`.

## Skills

| Skill dir | Role |
|-----------|------|
| `.agent/skills/norp-orchestrator/` | Planning / delegation |
| `.agent/skills/norp-scout/` | Source discovery |
| `.agent/skills/norp-acquisition/` | Named adapters + degrade |
| `.agent/skills/norp-researcher/` | Propose / interpret |
| `.agent/skills/norp-validator-agent/` | Contracts / gates |
| `.agent/skills/norp-code-agent/` | Code edits when needed |

Prompt stubs under `Checkpoint 4/prompts/agents/` defer to these skills — see `Checkpoint 4/prompts/README.md`.
