# Student Quickstart — Checkpoint 4 (Rolled Loop)

You do **not** need to re-live a semester of manual SQL and prompt engineering.
This package is meant to reduce fear: run the offline demos first, then read
backward into Manual / Unrolled only as needed.

## Prerequisites

- Repo root: `CS-6365`
- Python 3.10+ with project `.venv` (recommended; see root `.python-version`)
- Checkpoint 3 modeling frame for calibration / TA specs
  (`Checkpoint 3/data/cp3_modeling_frame.csv` — gitignored; regenerate via CP3 Mode A/B if missing — see [`Checkpoint 3/README.md`](../Checkpoint%203/README.md))

```bash
cd /path/to/CS-6365
source .venv/bin/activate   # optional if you call .venv/bin/python directly
pip install -r "Checkpoint 4/requirements.txt"
```

## Step 1 — Run everything offline (≈ minutes)

```bash
bash "Checkpoint 4/reproduce.sh"
```

That validates H4/H5, runs the Verifier gate (I1–I4/Q1), demos the food Atlanta
multi-agent bus (2 rounds), and runs housing Chicago (NTEE universality).

### Success criteria (Step 1)

Open these files and confirm:

| Check | File | Pass look |
|-------|------|-----------|
| H4/H5 reproduction | `phase3_results/validation_check.md` | `H4: PASS` β ≈ −7.91647; `H5: PASS` β ≈ +2.11963 |
| TA gate | `phase3_results/ta_verify/round99_results.md` | I3 ACCEPT; I1/I2/I4/Q1 REJECT |
| Food nulls | `phase3_results/round1_results.md` | F01 not significant; F02 REJECT |
| Housing | `phase3_results/housing_chicago/round1_results.md` | H02 REJECT |

If preflight fails on a missing frame, follow the script’s regenerate hint — do not ignore it.

## What you should *not* fear

| Fear | Reality |
|------|---------|
| “The LLM will invent statistics” | Only `09 --run` fits OLS (HC1). Agents propose/interpret text. |
| “I must scrape login-walled sites” | Critic blocks high/forbidden ToS (AccessFood-style). Use named adapters. |
| “I must rebuild H2/H4/H5 by hand” | Read Manual docs; the recipes are already encoded. Start at the rolled loop. |
| “Null results mean I failed” | Nulls / gate REJECT are first-class — see `NEGATIVE_FINDINGS.md`. |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Missing `cp3_modeling_frame.csv` | CP3 Mode A merge or Mode B acquire ([`Checkpoint 3/README.md`](../Checkpoint%203/README.md)) |
| `ModuleNotFoundError: statsmodels` | `pip install -r "Checkpoint 4/requirements.txt"` in `.venv` |
| Want live Feed America | Use `--enrich-config` HTTP config + network; respect CC BY attribution |
| Confused by IDs (H4 vs RQ4 vs F01) | [`docs/HYPOTHESIS_REGISTRY.md`](../docs/HYPOTHESIS_REGISTRY.md) |

## Step 2 — Read the curriculum map

1. [`docs/CURRICULUM.md`](../docs/CURRICULUM.md) — Manual → Unrolled → Rolled  
2. [`BENCHMARK.md`](BENCHMARK.md) — time/effort comparison  
3. [`HANDOFF_GUIDE.md`](HANDOFF_GUIDE.md) — CLI flags and agents  

## Step 3 — Try your own topic (optional)

1. Copy a config under `configs/` (food Atlanta or housing Chicago).
2. Set fields (cheat-sheet):

| Field | Example |
|-------|---------|
| `topic` | `food_assistance` / `housing_services` |
| `geography` | `atlanta` / `chicago` |
| `ntee_prefixes` | list of NTEE prefixes for density |
| HTTP block | only open, Critic-approved endpoints |

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
build only). Skills: `.agent/skills/norp-*`. See also root [`AGENTS.md`](../AGENTS.md).
