# Curriculum: Manual → Unrolled → Rolled

This repository teaches **workflow / loop engineering** for sociological
data exploration on nonprofit (NORP) data—not only “find a significant
correlation.”

Students inherit a finished pipeline. They should **read** the manual and
unrolled stages, then **run** the rolled loop.

## The three stages (this project)

### 1. Manual (Phase 1)

Humans design acquire → merge → clean → specify → OLS **separately for each
hypothesis**, adjusting the pipeline by hand.

| Hypothesis | Entry point |
|------------|-------------|
| H2 / RQ2 (bank-branch density) | [`Checkpoint 2/H2_Pipeline/`](../Checkpoint%202/H2_Pipeline/) |
| H4 / RQ4 (housing cost / ZHVI) | [`Checkpoint 3/H4/`](../Checkpoint%203/H4/) + [`PHASE1_MANUAL_PIPELINE.md`](../Checkpoint%203/PHASE1_MANUAL_PIPELINE.md) |
| H5 / RQ5 (provider density) | [`Checkpoint 3/H5/`](../Checkpoint%203/H5/) |

Effort story: days–weeks per hypothesis; every merge key, cleaning rule, and
control set is a human decision.

### 2. Unrolled (Phase 2)

Pre-register an agenda (List A / List B), then run deterministic OLS in batch.
The human still chooses *what* to test; the engine prevents mid-run p-hacking.

- Engine: [`Checkpoint 3/08_unrolled_loop.py`](../Checkpoint%203/08_unrolled_loop.py)
- Narrative: [`Checkpoint 3/PHASE2_UNROLLED_LOOP.md`](../Checkpoint%203/PHASE2_UNROLLED_LOOP.md)
- Artifacts: `Checkpoint 3/loop_results_v2/`

### 3. Rolled (Phase 3)

Agents scout sources, critic-gate ToS, acquire via named adapters, propose
hypotheses, and interpret—while **only** `09 --run` fits OLS (HC1 + Verifier
gate for higher-order specs).

- Package: [`Checkpoint 4/`](../Checkpoint%204/)
- One command: [`Checkpoint 4/reproduce.sh`](../Checkpoint%204/reproduce.sh)
- Student entry: [`Checkpoint 4/STUDENT_QUICKSTART.md`](../Checkpoint%204/STUDENT_QUICKSTART.md)
- Effort comparison: [`Checkpoint 4/BENCHMARK.md`](../Checkpoint%204/BENCHMARK.md)

## Supporting case study (optional reading)

Earlier NORP cohorts spent roughly a semester on raw data → clean → SQL →
validate → prompt-engineer by hand. That history motivates automation; **your**
Phase 1 in this repo is still H2/H4/H5 above, not a re-run of that semester.

## Where to start as a new student

1. Skim this file and [`Checkpoint 4/BENCHMARK.md`](../Checkpoint%204/BENCHMARK.md).
2. Run `bash "Checkpoint 4/reproduce.sh"` (offline demos).
3. Read Manual H4/H5 write-ups if you need the science recipe.
4. Swap a config under `Checkpoint 4/configs/` for a new topic/geo.
