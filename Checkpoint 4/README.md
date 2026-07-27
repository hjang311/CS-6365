# Checkpoint 4 — Multi-Agent Phase 3 (Rolled Loop)

**Canonical student package** for the rolled / agentic stage of the NORP curriculum. Education-first open source (July 22 OH Option 2).

> Provenance only: [`Grok_4.5/`](Grok_4.5/) is an earlier build trail — **not** the entrypoint. Use `09_phase3_agentic_loop.py` here.

## 60-second start

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

Then read [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md) and [`BENCHMARK.md`](BENCHMARK.md).

## What this package does

Orchestrator → Scout → Critic → Acquisition → Researcher → Stats (`09 --run`) → Interpret. Agents talk through `phase3_results/agent_bus/`. The LLM never fits OLS. Higher-order specs use an HC1 Wald F + ΔR² ≥ 5e-4 Verifier gate.

## Key paths

| Item | Path |
|------|------|
| Runner | [`09_phase3_agentic_loop.py`](09_phase3_agentic_loop.py) |
| One-command demos | [`reproduce.sh`](reproduce.sh) |
| Effort comparison | [`BENCHMARK.md`](BENCHMARK.md) |
| Student onboarding | [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md) |
| Handoff / CLI | [`HANDOFF_GUIDE.md`](HANDOFF_GUIDE.md) |
| Negatives | [`NEGATIVE_FINDINGS.md`](NEGATIVE_FINDINGS.md) |
| Report | [`Checkpoint_4_Report.md`](Checkpoint_4_Report.md) |
| Adapters | [`enrichment_tools/`](enrichment_tools/) |
| Configs | [`configs/`](configs/) |
| Prompts index | [`prompts/README.md`](prompts/README.md) |
| Hybrid master prompt | [`prompts/PHASE3_MULTI_AGENT_LOOP.md`](prompts/PHASE3_MULTI_AGENT_LOOP.md) |
| Provenance only | [`Grok_4.5/`](Grok_4.5/) |

## Config field cheat-sheet

Working examples: `configs/food_assistance_atlanta.json`, `configs/housing_services_chicago.json` (and siblings). Typical fields:

| Field | Role |
|-------|------|
| `topic` | Scout / narrative topic key (e.g. food_assistance) |
| `geography` | Slice geography (e.g. atlanta, chicago) |
| `ntee_prefixes` | NTEE prefix list for density adapter |
| HTTP / URL block | Feed America–style open endpoints (Critic-gated) |

Copy a config, change topic/geo/prefixes, run with `--enrich-config` (see commands below).

## Common commands + expected outputs

```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --validate
# → phase3_results/validation_check.md  (H4/H5 PASS lines)

.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --verify-ta-specs \
  --out "Checkpoint 4/phase3_results/ta_verify"
# → ta_verify/round99_results.md  (I1–I4 / Q1 gate column)

.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --all --fixture-full --rounds 2
# → round1_results.md / round2_results.md + agent_bus payloads

.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/housing_services_chicago.json" \
  --all --fixture --rounds 1 \
  --out "Checkpoint 4/phase3_results/housing_chicago"
# → housing_chicago/round1_results.md
```

## Artifact index (`phase3_results/`)

| Artifact | Role |
|----------|------|
| `validation_check.md` | H4/H5 β reproduction |
| `decision_log.jsonl` | scout / critic / acquire / degrade events |
| `agent_bus/` | message bus + manifests |
| `round*_results.md` | Food Atlanta OLS + gate |
| `housing_chicago/` | NTEE universality run |
| `ta_verify/` | TA higher-order specs |
| `stale_archive/` | gitignored / local provenance dumps |

## Curriculum context

See [`docs/CURRICULUM.md`](../docs/CURRICULUM.md): Manual (H2/H4/H5) → Unrolled (CP3) → **Rolled (this folder)**. Registry: [`docs/HYPOTHESIS_REGISTRY.md`](../docs/HYPOTHESIS_REGISTRY.md).
