# Checkpoint 4 Handoff Guide — Multi-Agent Phase 3

## What this pipeline does (30 seconds)

Phases 1–2 locked manual and pre-registered tests. Phase 3 is a **rolled multi-agent loop**:

**Orchestrator → Scout → Critic → Acquisition → Researcher → Stats Engine (`09 --run`) → Interpret**

Agents talk through `phase3_results/agent_bus/` (file “Slack”). The LLM never fits OLS.
Higher-order specs are gated by HC1 Wald F + ΔR² ≥ 5e-4 (TA Verifier absorbed from `ai-suggestions/cp4`).

## Quick start

```bash
cd /path/to/CS-6365
source .venv/bin/activate   # or .venv/bin/python …

# 1. H4/H5 calibration
python "Checkpoint 4/09_phase3_agentic_loop.py" --validate

# 3. Full multi-agent bus offline (scout→critic→NTEE→OLS; 2 rounds)
python "Checkpoint 4/09_phase3_agentic_loop.py" --all --fixture-full --rounds 2

# Or one command:
# bash "Checkpoint 4/reproduce.sh"

# 3. TA higher-order Verifier demo (I1–I4 / Q1)
python "Checkpoint 4/09_phase3_agentic_loop.py" --verify-ta-specs \
  --out "Checkpoint 4/phase3_results/ta_verify"

# 4. Live web acquisition (Feed America) + Atlanta slice
python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/food_assistance_atlanta_http.json"

# 5. Second topic (universality — NTEE-only housing)
python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/housing_services_chicago.json" \
  --all --fixture --rounds 1 \
  --out "Checkpoint 4/phase3_results/housing_chicago"
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
- Mode B drift: `Checkpoint 3/MODE_B_DRIFT.md`

## How to add your own research question

1. Create `Checkpoint 4/configs/my_topic_city.json` (copy housing or food configs).
2. Set `topic`, `geography`, `source` (`ntee` / `http_open_api` / `web_download`), and `ntee_prefixes` or `http`/`url`.
3. Run `--enrich-config` then `--all --fixture`, or paste `prompts/PHASE3_MULTI_AGENT_LOOP.md` into Cursor/Antigravity.
4. Read `agent_bus/messages.jsonl` and `NEGATIVE_FINDINGS.md` patterns for nulls / gate REJECTs.

## Soup kitchen worked example

See `NEGATIVE_FINDINGS.md`. Live HTTP path writes `data/acquisitions/food_assistance/` (~2,250 GA rows).

## Layout

```
Checkpoint 4/
  09_phase3_agentic_loop.py
  phase3_enrichment_cmds.py
  enrichment_tools/          # adapters + agent_bus
  configs/                   # topic/geo plans
  prompts/                   # hybrid + per-agent
  data/                      # enriched frames + acquisitions
  phase3_results/            # OLS + bus
  Grok_4.5/                  # provenance archive
```

## Skills (CP1 → CP4)

`.agent/skills/norp-{orchestrator,code-agent,validator-agent,scout,acquisition,researcher}/`
Factories: `agentic_pipeline/agents.py` → `create_phase3_agents()`.
