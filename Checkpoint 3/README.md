# Checkpoint 3 — Deterministic Hypothesis Pipeline (Phases 1 & 2)

Single index for the Checkpoint 3 deliverable: what each script does, how the data flows, and how to reproduce everything from a fresh machine.

## The 3-phase model (July 2026 OH guidance)

| Phase | Meaning | Status | Artifacts |
|-------|---------|--------|-----------|
| **1 — Manual** | Hand-run data acquisition, merging, and hypothesis tests (H4/H5, plus H2 from Checkpoint 2) | Done | `01`, `02`, `04`, `06`, `H4/`, `H5/` |
| **2 — Unrolled loop** | Explicit pre-registered hypothesis list executed by deterministic Python OLS. The LLM never picks the next test | Done | `08_unrolled_loop.py`, `loop_results_v2/`, `PHASE2_UNROLLED_LOOP.md` |
| **3 — Agentic loop** | Agent evaluates results, proposes new indicators, pursues finer-granularity data (e.g. soup-kitchen density) | **Not built** (intentional) | design notes in `PHASE2_UNROLLED_LOOP.md` §6 |

## Script map

| Script | Phase | Role | Interactive? |
|--------|-------|------|--------------|
| `00_dataset_discovery_agent.py` | pre-1 | LLM librarian prompt for dataset ideation | Yes (stdin) |
| `01_acquire_data.py` | 1 | Subset NCCS core files; download Zillow ZHVI | No (network for Zillow) |
| `02_merge_pipeline.py` | 1 | Build `data/cp3_modeling_frame.csv` (BMF, ACS, density, ZHVI, FDIC) | No |
| `03_hitl_hypothesis_engine.py` | prototype | Single-hypothesis HITL runner (predates phase model) | Yes (stdin) |
| `04_validate_frame.py` | 1 | Data contracts on the modeling frame (exit 0/1) | No |
| `06_run_h4_h5_split.py` | 1 | H4/H5 formal tables with mid/large size splits | No |
| `07_deterministic_loop.py` | historical | 215-pair combinatorial batch with per-hit agent prompts. **Superseded by 08** | Yes (stdin) |
| `08_unrolled_loop.py` | 2 | Unrolled loop: List A (curated hypotheses) + List B (pre-registered two-variable limitation harness) | No |

There is no `05` — CP2's validator role is filled by `04_validate_frame.py` here.

**Which results to trust:** `loop_results_v2/` (from `08`). The older `loop_results/` directory is the historical `07 --batch` output (155 "significant" findings, many mechanical) kept for provenance only.

## Professor read order

For the shortest path through the project argument:

1. [`PHASE1_MANUAL_PIPELINE.md`](PHASE1_MANUAL_PIPELINE.md) — acquisition,
   merging, human-designed specialization/cleaning, and manual H2/H4/H5 tests.
2. [`H4/H4_VERIFICATION_RUN.md`](H4/H4_VERIFICATION_RUN.md) and
   [`H5/H5_VERIFICATION_RUN.md`](H5/H5_VERIFICATION_RUN.md) — substantive
   findings (including H5's rejected direction).
3. [`PHASE2_UNROLLED_LOOP.md`](PHASE2_UNROLLED_LOOP.md) — how the repeated
   manual sequence became a fixed-list deterministic loop.
4. [`loop_results_v2/two_variable_limitation.md`](loop_results_v2/two_variable_limitation.md)
   — why statistical significance in this frame is not a finished research
   result and what Phase 3 must add.

`07_deterministic_loop.py`, `LOOP_DOCUMENTATION.md`, and `loop_results/` are
historical implementation context, not part of the main presentation path.

## Reproduction mode A — data handoff (CSV inputs already present)

The `data/` directory (~470 MB) is **gitignored** — a fresh clone has no CSVs. If you have the data (course machine or handoff), run:

```bash
# from the repo root
python3 -m venv .venv
.venv/bin/python -m pip install -r "Checkpoint 3/requirements.txt"

.venv/bin/python "Checkpoint 3/02_merge_pipeline.py"        # rebuild modeling frame
.venv/bin/python "Checkpoint 3/04_validate_frame.py"        # data contracts (exit 0 = pass)
.venv/bin/python "Checkpoint 3/06_run_h4_h5_split.py"       # H4/H5 formal tables
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --validate
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --run
```

Expected: validator passes all contracts; `08 --validate` prints `H4: PASS  H5: PASS` (β reproduction: −7.91647 and +2.11963 within 1e-3).

This mode proves deterministic reconstruction from handed-off source CSVs. It does **not** prove that every external source can still be reacquired from a fresh clone.

## Reproduction mode B — fresh clone (no CSV inputs)

This path has not yet been independently exercised end-to-end. All commands below are run from the **repo root**.

1. **Create the environment and export the Census key.** The CP2 acquisition script reads the shell environment; it does not automatically load `.env`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "Checkpoint 2/H2_Pipeline/requirements.txt"
export CENSUS_API_KEY="YOUR_CENSUS_API_KEY"
```

2. **Acquire the federal sources through the manual CP2 pipeline:**

```bash
.venv/bin/python "Checkpoint 2/H2_Pipeline/01_acquire_data.py"
# Downloads NCCS CORE 2018–2022, IRS BMF, FDIC, and Census ACS.
```

3. **Copy the required source CSVs into Checkpoint 3:**

```bash
mkdir -p "Checkpoint 3/data"
cp "Checkpoint 2/H2_Pipeline/data/"core_*_filtered.csv "Checkpoint 3/data/"
cp "Checkpoint 2/H2_Pipeline/data/irs_bmf.csv" "Checkpoint 3/data/"
cp "Checkpoint 2/H2_Pipeline/data/census_acs_by_zip.csv" "Checkpoint 3/data/"
cp "Checkpoint 2/H2_Pipeline/data/fdic_branches_by_zip.csv" "Checkpoint 3/data/"
```

4. **Run the CP3 pipeline** (adds the exact December 2022 Zillow snapshot and builds the frame):

```bash
.venv/bin/python "Checkpoint 3/01_acquire_data.py"   # core subset + Zillow ZHVI download
.venv/bin/python "Checkpoint 3/02_merge_pipeline.py"
```

Then continue with validation and analysis commands from mode A, starting at `04_validate_frame.py`.

## Data inventory (`data/`, gitignored)

| File | Source | Used by |
|------|--------|---------|
| `core_2018..2022_filtered.csv` | NCCS CORE via CP2 | `01` |
| `core_subset.csv` | `01` output | `02` |
| `irs_bmf.csv` | IRS EO BMF via CP2 | `02` |
| `census_acs_by_zip.csv` | Census ACS5 via CP2 (needs API key) | `02` |
| `fdic_branches_by_zip.csv` | FDIC BankFind via CP2 | `02` (bank_branch_density — H2 replay) |
| `zillow_zhvi_2022.csv` | `01` download | `02` |
| `cp3_modeling_frame.csv` | `02` output (~158K rows) | `04`, `06`, `07`, `08` |
| `h2_modeling_frame.csv` | CP2 artifact | orphan (reference only) |

## Key definitions

- **DV:** `fundraising_efficiency = total_contributions / (professional_fundraising_fees + fundraising_events_direct_expenses)`; winsorized at the 99th percentile as `fundraising_efficiency_w`.
- **Controls (all OLS):** `log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income`, HC1 robust errors.
- **Cleaning:** contributions/spend > 0, spend ≥ $5K, efficiency ≤ 1,000, ZIP population ≥ 1,000, revenue ≥ $500K.
- **H4:** `log_zhvi_2022` → efficiency (negative, confirmed). **H5:** `log_nonprofit_branch_density` → efficiency (expected negative, observed **positive** — theory rejected). Note H4 n (116,587) < H5 n (117,510) because ~12K rows lack ZHVI and are listwise-deleted.

## Documentation

- `PHASE1_MANUAL_PIPELINE.md` — Phase 1 acquisition, merge, cleaning, and manual-hypothesis narrative
- `PHASE2_UNROLLED_LOOP.md` — Phase 2 student guide (unrolled-loop metaphor, List A vs B)
- `LOOP_DOCUMENTATION.md` — historical guide for `07`
- `H4/H4_VERIFICATION_RUN.md`, `H5/H5_VERIFICATION_RUN.md` — formal hypothesis write-ups
- `TEST_EXECUTION_PLAN.md` — ordered test/ship checklist with acceptance criteria
