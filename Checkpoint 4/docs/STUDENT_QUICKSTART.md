# Student Quickstart — Checkpoint 4 (Rolled Loop)

You do **not** need to re-live a semester of manual SQL and prompt engineering.
This package is meant to reduce fear: run the offline demos first, then read
backward into Manual / Unrolled only as needed.

## Prerequisites

- Repo root: `CS-6365`
- Python 3.10+ with project `.venv` (recommended; see root `.python-version`)
- Checkpoint 3 modeling frame for calibration / TA specs
  (`Checkpoint 3/data/cp3_modeling_frame.csv` — gitignored; if missing, see **Build from scratch (Mode B)** below, or Mode A handoff merge in [`Checkpoint 3/README.md`](../Checkpoint%203/README.md))

```bash
cd /path/to/CS-6365
source .venv/bin/activate   # optional if you call .venv/bin/python directly
pip install -r "Checkpoint 4/requirements.txt"
```

## If the modeling frame is missing — build from scratch (Mode B)

Ingest public federal sources (+ one free Census key), merge into
`cp3_modeling_frame.csv`, then run the CP4 demos. This is the classic
“acquire → reproduce” path; it is separate from the offline golden suite.

| Source | Credential |
|--------|------------|
| Census ACS5 | **`CENSUS_API_KEY`** (free: https://api.census.gov/data/key_signup.html; see [`.env.example`](../../.env.example)) |
| NCCS CORE 990, IRS BMF, FDIC BankFind | Public — no key |
| Zillow ZHVI (Dec 2022) | Public download via CP3 `01` — no key |
| `GEMINI_API_KEY` | **Not** needed to build the frame |

```bash
# From repo root. (Auto-loads .env if CENSUS_API_KEY is defined, or reads shell env)
.venv/bin/python -m pip install -r "Checkpoint 2/H2_Pipeline/requirements.txt"
export CENSUS_API_KEY="YOUR_CENSUS_API_KEY"

.venv/bin/python "Checkpoint 2/H2_Pipeline/01_acquire_data.py"
# Downloads NCCS CORE 2018–2022, IRS BMF, FDIC, and Census ACS.

mkdir -p "Checkpoint 3/data"
cp "Checkpoint 2/H2_Pipeline/data/"core_*_filtered.csv "Checkpoint 3/data/"
cp "Checkpoint 2/H2_Pipeline/data/irs_bmf.csv" "Checkpoint 3/data/"
cp "Checkpoint 2/H2_Pipeline/data/census_acs_by_zip.csv" "Checkpoint 3/data/"
cp "Checkpoint 2/H2_Pipeline/data/fdic_branches_by_zip.csv" "Checkpoint 3/data/"

.venv/bin/python "Checkpoint 3/pipeline/01_acquire_data.py"   # core subset + Zillow ZHVI
.venv/bin/python "Checkpoint 3/pipeline/02_merge_pipeline.py" # → builds cp3_modeling_frame.csv

# 1. Validate data contracts on new frame
.venv/bin/python "Checkpoint 3/pipeline/04_validate_frame.py"

# 2. Reproduce Phase 2 Unrolled Loop (List A & List B hypotheses)
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --run

# 3. Reproduce Phase 3 Multi-Agent Loop
bash "Checkpoint 4/reproduce.sh"
```

Then:

```bash
bash "Checkpoint 4/reproduce.sh"
```

**Drift caveat:** Mode B proves the same recipe on live inputs. Exact β identity
vs a handoff frame is **not** guaranteed — see
[`Checkpoint 3/docs/MODE_B_DRIFT.md`](../../Checkpoint%203/docs/MODE_B_DRIFT.md). Bit-identical
PASS/REJECT demos assume a fixed handoff frame + offline `reproduce.sh`.

Full Mode A (handoff CSVs already present) vs Mode B detail:
[`Checkpoint 3/README.md`](../Checkpoint%203/README.md). Live Feed America
enrichment is a separate optional step (`--enrich-config` HTTP); housing is
NTEE-only by design.

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
| Missing `cp3_modeling_frame.csv` | [Build from scratch (Mode B)](#if-the-modeling-frame-is-missing--build-from-scratch-mode-b) above, or Mode A handoff merge in [`Checkpoint 3/README.md`](../Checkpoint%203/README.md) |
| `ModuleNotFoundError: statsmodels` | `pip install -r "Checkpoint 4/requirements.txt"` in `.venv` |
| Want live Feed America | Use `--enrich-config` HTTP config + network; respect CC BY attribution |
| Confused by IDs (H4 vs RQ4 vs F01) | [`docs/HYPOTHESIS_REGISTRY.md`](../../docs/HYPOTHESIS_REGISTRY.md) |

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
| Manual H4/H5 | `Checkpoint 3/H4/`, `Checkpoint 3/H5/`, `Checkpoint 3/docs/PHASE1_MANUAL_PIPELINE.md` |
| Unrolled | `Checkpoint 3/08_unrolled_loop.py`, `loop_results_v2/` |

## Provenance vs canonical

Use **`Checkpoint 4/09_phase3_agentic_loop.py`**, not `provenance/early_build/` (historical
build only). Skills: `.agent/skills/norp-*`. Studio map: [`STRUCTURE.md`](STRUCTURE.md).
See also root [`AGENTS.md`](../../AGENTS.md).
