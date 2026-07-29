# Checkpoint 4 studio structure

How this folder is organized for someone **without semester context**: reproduce first, then extend beyond Phase 3.

## Front of house (start here)

| Path | Role |
|------|------|
| [`../README.md`](../README.md) | Front door: 60-second run + three doors |
| [`../reproduce.sh`](../reproduce.sh) | Offline demos (validate → TA gate → food ×2 → housing) |
| [`../09_phase3_agentic_loop.py`](../09_phase3_agentic_loop.py) | Sole public Stats CLI — **only** place that fits OLS |
| [`../requirements.txt`](../requirements.txt) | CP4 Python deps |

## Three doors

1. **Run** — `reproduce.sh` then open the **runs gallery** `../phase3_results/` (`validation_check.md`, `ta_verify/`, `round1_results.md`, `housing_chicago/`).
2. **Orchestrate** — paste [`../prompts/PHASE3_MULTI_AGENT_LOOP.md`](../prompts/PHASE3_MULTI_AGENT_LOOP.md) into any IDE/agent host; load [`.agent/skills/norp-*`](../../.agent/skills/); spawn Scout/Critic/Acquisition/Researcher as sub-agents; still call `09 --run` for OLS.
3. **Extend** — copy a file under [`../configs/`](../configs/), or add a named adapter under [`../engine/enrichment_tools/`](../engine/enrichment_tools/). Keep Critic ToS rules; never scrape login-walled directories.

## Back of house

| Path | Role |
|------|------|
| [`../engine/`](../engine/) | `phase3_enrichment_cmds.py` + `enrichment_tools/` — libraries used by `09`, **not** a second student CLI |
| [`../configs/`](../configs/) | Enrichment / round JSON |
| [`../prompts/`](../prompts/) | Hybrid orchestration paste prompts |
| [`../fixtures/`](../fixtures/) | Points at offline Scout fixtures embedded in engine code |
| [`../data/`](../data/) | Enriched frames / acquisitions (large CSVs usually local/gitignored) |
| [`../phase3_results/`](../phase3_results/) | Runs gallery + agent bus (golden demos are the `*.md` tables you are told to open) |

## Provenance (do not start here)

| Path | Role |
|------|------|
| [`../provenance/early_build/`](../provenance/early_build/) | Earlier build trail (soup-kitchen stretch, old reports). Tracked for history; **not** the entrypoint. |

## Teaching docs in this folder

| File | Role |
|------|------|
| [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md) | Fear-reducing onboarding |
| [`HANDOFF_GUIDE.md`](HANDOFF_GUIDE.md) | CLI flags and agent flow |
| [`BENCHMARK.md`](BENCHMARK.md) | Manual → Unrolled → Rolled effort |
| [`NEGATIVE_FINDINGS.md`](NEGATIVE_FINDINGS.md) | Null / gate REJECT as first-class |
| [`Checkpoint_4_Report.md`](Checkpoint_4_Report.md) | Stub only — full draft is local under gitignored `../report/` |

Cross-repo spine: [`../../docs/CURRICULUM.md`](../../docs/CURRICULUM.md), [`../../docs/HYPOTHESIS_REGISTRY.md`](../../docs/HYPOTHESIS_REGISTRY.md), [`../../AGENTS.md`](../../AGENTS.md).

## Beyond Phase 3 (extension checklist)

1. Reproduce (`reproduce.sh`) and confirm expected PASS / REJECT lines.
2. Copy `configs/*.json` → new topic/geography; run `--enrich-config`.
3. If you need a new data source: implement a **named** adapter in `engine/enrichment_tools/`, register it in Scout/Critic skill text, keep ToS gates.
4. Pre-register proposals JSON **before** any `09 --run`.
5. Document nulls and gate REJECTs; do not fish for significance by editing proposals after OLS.
6. Optional later phase: keep `09` as the Stats Engine and add a new outer loop — do not move OLS into the LLM.
