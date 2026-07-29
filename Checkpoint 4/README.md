# Checkpoint 4 — Multi-Agent Phase 3 (Rolled Loop)

**Canonical student package** for the rolled / agentic stage of the NORP curriculum.  
Goal: an outsider can **reproduce** offline demos, then **extend** beyond Phase 3 (new topic/geo, new adapter, or a later phase) without reverse-engineering the semester.

## 60-second start (Run)

```bash
# From repo root — requires Checkpoint 3/data/cp3_modeling_frame.csv (gitignored)
bash "Checkpoint 4/reproduce.sh"
```

| Expected check | Where |
|----------------|-------|
| H4 PASS β ≈ −7.91647; H5 PASS β ≈ +2.11963 | `phase3_results/validation_check.md` |
| I1/I2/Q1 REJECT; I3 ACCEPT; I4 REJECT | `phase3_results/ta_verify/round99_results.md` |
| F01 null; F02 gate REJECT | `phase3_results/round1_results.md` |
| H01 exploratory; H02 gate REJECT | `phase3_results/housing_chicago/round1_results.md` |

Then: [`docs/STUDENT_QUICKSTART.md`](docs/STUDENT_QUICKSTART.md) · [`docs/STRUCTURE.md`](docs/STRUCTURE.md) · [`../docs/CURRICULUM.md`](../docs/CURRICULUM.md)

## Three doors

| Door | Use when | Open |
|------|----------|------|
| **Run** | Reproduce offline demos | `reproduce.sh` → `phase3_results/` (runs gallery) |
| **Orchestrate** | Live hybrid IDE loop (any host) | [`prompts/`](prompts/) + [`.agent/skills/norp-*`](../.agent/skills/) |
| **Extend** | New topic/geo or adapter beyond CP4 | [`configs/`](configs/) + [`engine/enrichment_tools/`](engine/enrichment_tools/) |

Hard rule: **only** [`09_phase3_agentic_loop.py`](09_phase3_agentic_loop.py) fits OLS. LLM agents never invent coefficients.

## Studio map

```
Checkpoint 4/
  README.md                 ← you are here (front door)
  reproduce.sh              ← one-command offline demos
  requirements.txt
  09_phase3_agentic_loop.py ← sole public Stats CLI

  docs/                     ← teaching + science write-ups
  prompts/                  ← paste-ready hybrid orchestration
  configs/                  ← topic/geo enrichment JSON
  engine/                   ← adapters + enrichment helpers (not a second CLI)
  fixtures/                 ← pointers to offline scout fixtures
  phase3_results/           ← runs gallery (golden demos + agent_bus)
  data/                     ← enriched frames / acquisitions (CSVs mostly local)
  provenance/early_build/      ← earlier build trail — do not start here
```

Full legend: [`docs/STRUCTURE.md`](docs/STRUCTURE.md).

## Key paths

| Item | Path |
|------|------|
| Stats CLI | [`09_phase3_agentic_loop.py`](09_phase3_agentic_loop.py) |
| One-command demos | [`reproduce.sh`](reproduce.sh) |
| Student onboarding | [`docs/STUDENT_QUICKSTART.md`](docs/STUDENT_QUICKSTART.md) |
| CLI reference | [`docs/HANDOFF_GUIDE.md`](docs/HANDOFF_GUIDE.md) |
| Effort comparison | [`docs/BENCHMARK.md`](docs/BENCHMARK.md) |
| Negatives | [`docs/NEGATIVE_FINDINGS.md`](docs/NEGATIVE_FINDINGS.md) |
| Report (local only) | Gitignored [`report/`](report/) — see stub [`docs/Checkpoint_4_Report.md`](docs/Checkpoint_4_Report.md) |
| Adapters | [`engine/enrichment_tools/`](engine/enrichment_tools/) |
| Configs | [`configs/`](configs/) |
| Hybrid prompts | [`prompts/README.md`](prompts/README.md) |
| Provenance | [`provenance/early_build/`](provenance/early_build/) |

## Config cheat-sheet (Extend door)

Working examples: `configs/food_assistance_atlanta_ntee.json`, `configs/food_assistance_atlanta_http.json`, `configs/housing_services_chicago.json`. Typical fields:

| Field | Role |
|-------|------|
| `topic` | Scout / narrative topic key (e.g. food_assistance) |
| `geography` | Slice geography (e.g. atlanta, chicago) |
| `ntee_prefixes` | NTEE prefix list for density adapter |
| HTTP / URL block | Feed America–style open endpoints (Critic-gated) |

Copy a config, change topic/geo/prefixes, run with `--enrich-config` (see [`docs/HANDOFF_GUIDE.md`](docs/HANDOFF_GUIDE.md)). To go **beyond Phase 3**, add a named adapter under `engine/enrichment_tools/` and teach Critic/Scout about it — keep OLS inside `09`.

## Common commands

```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --validate
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --verify-ta-specs \
  --out "Checkpoint 4/phase3_results/ta_verify"
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --all --fixture-full --rounds 2
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/housing_services_chicago.json" \
  --all --fixture --rounds 1 \
  --out "Checkpoint 4/phase3_results/housing_chicago"
```

## What this package does

Orchestrator → Scout → Critic → Acquisition → Researcher → Stats (`09 --run`) → Interpret. Agents talk through `phase3_results/agent_bus/`. Higher-order specs use an HC1 Wald F + ΔR² ≥ 5e-4 Verifier gate. Null / gate REJECT are first-class ([`docs/NEGATIVE_FINDINGS.md`](docs/NEGATIVE_FINDINGS.md)).

`agent_bus/enriched_frame_manifest.json` stores **repo-relative** frame paths (e.g. `Checkpoint 4/data/...`) so clones are portable; resolve them from the repository root when passing `--frame`.
