# Checkpoint 4 Handoff Guide — Multi-Agent Phase 3

## What this pipeline does (30 seconds)

Phases 1–2 locked manual and pre-registered tests. Phase 3 is a **rolled multi-agent loop**:

**Orchestrator → Scout → Critic → Acquisition → Researcher → Stats Engine (`09 --run`) → Interpret**

Agents talk through `phase3_results/agent_bus/` (file “Slack”). The LLM never fits OLS.
Higher-order specs are gated by HC1 Wald F + ΔR² ≥ 5e-4 (TA Verifier absorbed into `09 --verify-ta-specs` / `--run`).

## Prerequisites

- Repo `.venv` with [`requirements.txt`](requirements.txt) installed
- `Checkpoint 3/data/cp3_modeling_frame.csv` present (or regenerate — [STUDENT_QUICKSTART Mode B](STUDENT_QUICKSTART.md#if-the-modeling-frame-is-missing--build-from-scratch-mode-b); full Mode A/B in CP3 README)
- Prefer `.venv/bin/python` over bare `python3`

## Quick start

```bash
cd /path/to/CS-6365
source .venv/bin/activate   # or call .venv/bin/python directly

# 0. One command (recommended)
bash "Checkpoint 4/reproduce.sh"
# Expected: validation PASS lines; ta_verify gates; food/housing result tables
# Elapsed seconds printed at end

# 1. H4/H5 calibration only
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --validate
# → phase3_results/validation_check.md

# 2. TA higher-order Verifier demo (I1–I4 / Q1)
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --verify-ta-specs \
  --out "Checkpoint 4/phase3_results/ta_verify"
# → ta_verify/round99_results.md

# 3. Full multi-agent bus offline (scout→critic→NTEE→OLS; 2 rounds)
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --all --fixture-full --rounds 2
# → round1_results.md, round2_results.md, agent_bus/

# 4. Live web acquisition (Feed America) + Atlanta slice (network)
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/food_assistance_atlanta_http.json"

# 5. Second topic (universality — NTEE-only housing)
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/housing_services_chicago.json" \
  --all --fixture --rounds 1 \
  --out "Checkpoint 4/phase3_results/housing_chicago"
# → housing_chicago/round1_results.md
```

## Scout vs Acquisition

| Agent | Job |
|-------|-----|
| **Scout** | Discovers/ranks open sources → `source_candidates.json` (does **not** download) |
| **Critic** | Blocks high/forbidden ToS, then approves next eligible candidate |
| **Acquisition** | Runs a **named adapter** on an approved plan → entity CSV + density merge |

Universal ≠ limitless scraper. Lanes: `ntee_density` | `http_open_api` | `web_download` | `manual_hybrid`.
Housing is NTEE-only by design (`data/acquisitions/housing_services/README.md`).

## Fixture levels

| Flag | Meaning |
|------|---------|
| `--fixture` | Offline propose/interpret only (no scout/acquire) |
| `--fixture-full` | Offline scout + Critic ToS demo + NTEE acquire + propose/run/interpret |

## CP3 carry-forwards

- RQ2 write-up: `Checkpoint 3/RQ2/RQ2_VERIFICATION_RUN.md`
- Mode B drift: `Checkpoint 3/docs/MODE_B_DRIFT.md`
- From-scratch ingest (Census key + public federal acquire): [STUDENT_QUICKSTART — Mode B](STUDENT_QUICKSTART.md#if-the-modeling-frame-is-missing--build-from-scratch-mode-b)

## How to add your own research question

1. Create `Checkpoint 4/configs/my_topic_city.json` (copy housing or food configs).
2. Set `topic`, `geography`, `source` (`ntee` / `http_open_api` / `web_download`), and `ntee_prefixes` or `http`/`url`.
3. Run `--enrich-config` then `--all --fixture`, or paste `prompts/PHASE3_MULTI_AGENT_LOOP.md` into any IDE/agent host.
4. Read `agent_bus/messages.jsonl` and `NEGATIVE_FINDINGS.md` patterns for nulls / gate REJECTs.
5. Beyond Phase 3: add a named adapter under `engine/enrichment_tools/` and keep OLS inside `09` only — see [`STRUCTURE.md`](STRUCTURE.md).

## Soup kitchen / food worked example

See `NEGATIVE_FINDINGS.md`. Live HTTP path writes `data/acquisitions/food_assistance/` (~2,250 GA rows, CC BY).

## Layout (studio)

```
Checkpoint 4/
  09_phase3_agentic_loop.py   # sole public Stats CLI
  reproduce.sh
  docs/                        # teaching + science (this file lives here)
  prompts/                     # hybrid orchestration
  configs/                     # topic/geo plans
  engine/                      # enrichment_tools + cmds (not a second CLI)
  phase3_results/              # runs gallery + bus
  data/
  provenance/early_build/         # earlier build trail only
```

Full map: [`STRUCTURE.md`](STRUCTURE.md).

## Skills (CP1 → CP4)

`.agent/skills/norp-{orchestrator,code-agent,validator-agent,scout,acquisition,researcher}/`  
See root [`AGENTS.md`](../../AGENTS.md). Factories: `agentic_pipeline/agents.py` → `create_phase3_agents()` (legacy).
