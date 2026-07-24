# Student Quickstart — Checkpoint 4 (Rolled Loop)

You do **not** need to re-live a semester of manual SQL and prompt engineering.
This package is meant to reduce fear: run the offline demos first, then read
backward into Manual / Unrolled only as needed.

## Prerequisites

- Repo root: `CS-6365`
- Python 3.10+ with project `.venv` (recommended)
- Checkpoint 3 modeling frame available for calibration / TA specs
  (`Checkpoint 3/data/cp3_modeling_frame.csv` — regenerate via CP3 scripts if missing)

```bash
cd /path/to/CS-6365
source .venv/bin/activate   # optional if you call .venv/bin/python directly
```

## Step 1 — Run everything offline (≈ minutes)

```bash
bash "Checkpoint 4/reproduce.sh"
```

That validates H4/H5, runs the Verifier gate (I1–I4/Q1), demos the food Atlanta
multi-agent bus (2 rounds), and runs housing Chicago (NTEE universality).

## What you should *not* fear

| Fear | Reality |
|------|---------|
| “The LLM will invent statistics” | Only `09 --run` fits OLS (HC1). Agents propose/interpret text. |
| “I must scrape login-walled sites” | Critic blocks high/forbidden ToS (AccessFood-style). Use named adapters. |
| “I must rebuild H2/H4/H5 by hand” | Read Manual docs; the recipes are already encoded. Start at the rolled loop. |
| “Null results mean I failed” | Nulls / gate REJECT are first-class — see `NEGATIVE_FINDINGS.md`. |

## Step 2 — Read the curriculum map

1. [`docs/CURRICULUM.md`](../docs/CURRICULUM.md) — Manual → Unrolled → Rolled  
2. [`BENCHMARK.md`](BENCHMARK.md) — time/effort comparison  
3. [`HANDOFF_GUIDE.md`](HANDOFF_GUIDE.md) — CLI flags and agents  

## Step 3 — Try your own topic (optional)

1. Copy a config under `configs/` (food Atlanta or housing Chicago).
2. Set `topic`, `geography`, `ntee_prefixes` or HTTP block.
3. Run:

```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/YOUR_CONFIG.json" \
  --all --fixture --rounds 1 \
  --out "Checkpoint 4/phase3_results/my_topic"
```

Or paste `prompts/PHASE3_MULTI_AGENT_LOOP.md` into Cursor / Antigravity for a
hybrid multi-agent session.

## Where Manual / Unrolled live (reading)

| Stage | Path |
|-------|------|
| Manual H2 | `Checkpoint 2/H2_Pipeline/` |
| Manual H4/H5 | `Checkpoint 3/H4/`, `Checkpoint 3/H5/`, `PHASE1_MANUAL_PIPELINE.md` |
| Unrolled | `Checkpoint 3/08_unrolled_loop.py`, `loop_results_v2/` |

## Provenance vs canonical

Use **`Checkpoint 4/09_phase3_agentic_loop.py`**, not `Grok_4.5/` (historical
build only). Skills: `.agent/skills/norp-*`.
