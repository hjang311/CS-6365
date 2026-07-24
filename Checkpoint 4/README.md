# Checkpoint 4 — Multi-Agent Phase 3 (Rolled Loop)

**Canonical student package** for the rolled / agentic stage of the NORP
curriculum. Education-first open source (July 22 OH Option 2).

## 60-second start

```bash
# From repo root
bash "Checkpoint 4/reproduce.sh"
```

Then read [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md) and
[`BENCHMARK.md`](BENCHMARK.md).

## What this package does

Orchestrator → Scout → Critic → Acquisition → Researcher → Stats (`09 --run`) →
Interpret. Agents talk through `phase3_results/agent_bus/`. The LLM never fits
OLS. Higher-order specs use an HC1 Wald F + ΔR² Verifier gate.

## Key paths

| Item | Path |
|------|------|
| Runner | [`09_phase3_agentic_loop.py`](09_phase3_agentic_loop.py) |
| One-command demos | [`reproduce.sh`](reproduce.sh) |
| Effort comparison | [`BENCHMARK.md`](BENCHMARK.md) |
| Student onboarding | [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md) |
| Handoff / CLI | [`HANDOFF_GUIDE.md`](HANDOFF_GUIDE.md) |
| Adapters | [`enrichment_tools/`](enrichment_tools/) |
| Configs | [`configs/`](configs/) |
| Hybrid prompt | [`prompts/PHASE3_MULTI_AGENT_LOOP.md`](prompts/PHASE3_MULTI_AGENT_LOOP.md) |
| Report | [`Checkpoint_4_Report.md`](Checkpoint_4_Report.md) |
| Negatives | [`NEGATIVE_FINDINGS.md`](NEGATIVE_FINDINGS.md) |
| Provenance only | [`Grok_4.5/`](Grok_4.5/) (not the entrypoint) |

## Common commands

```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --validate
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --all --fixture-full --rounds 2
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --verify-ta-specs \
  --out "Checkpoint 4/phase3_results/ta_verify"
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/housing_services_chicago.json" \
  --all --fixture --rounds 1 \
  --out "Checkpoint 4/phase3_results/housing_chicago"
```

## Curriculum context

See [`docs/CURRICULUM.md`](../docs/CURRICULUM.md): Manual (H2/H4/H5) → Unrolled
(CP3) → **Rolled (this folder)**.
