# Curriculum: Manual → Unrolled → Rolled

This repository teaches **workflow / loop engineering** for sociological data exploration on nonprofit (NORP) data — not only “find a significant correlation.”

Students inherit a finished pipeline. They should **run** the rolled loop first, then **read** Manual and Unrolled stages as recipes.

## Learning objectives

After working through this package you should be able to:

1. Explain why **who chooses the next test** (human vs pre-registered list vs agent) changes scientific risk.
2. Run offline Phase 3 demos and verify **PASS / REJECT** artifacts without trusting LLM-written coefficients.
3. Contrast **Manual** specialization cost (H2/H4/H5) with **Unrolled** batch execution and **Rolled** scout→critic→acquire.
4. Treat **null results and gate REJECT** as first-class outputs, not failed checkpoints.
5. Swap a `Checkpoint 4/configs/*.json` topic/geo and reason about ToS / adapter choices.

## Prerequisites

- Python 3.10+ and willingness to use a venv
- Comfort reading OLS tables (β, p, R², n); HC1 = heteroskedasticity-robust SEs
- Optional: Census API key only if regenerating federal sources from scratch

## Recommended order (fear-reducing)

1. [`Checkpoint 4/STUDENT_QUICKSTART.md`](../Checkpoint%204/STUDENT_QUICKSTART.md) + `bash "Checkpoint 4/reproduce.sh"`
2. [`Checkpoint 4/BENCHMARK.md`](../Checkpoint%204/BENCHMARK.md) — Manual vs Unrolled vs Rolled effort
3. Skim Manual H4/H5 or H2 only if you need the science recipe
4. Optional: [`Checkpoint 0/`](../Checkpoint%200/) — **prior-semester case study only** (what earlier cohorts had to do by hand). **Not** Phase 1 of *this* curriculum.

## The three stages (this project)

### 1. Manual (Phase 1)

Humans design acquire → merge → clean → specify → OLS **separately for each hypothesis**, adjusting the pipeline by hand.

| Hypothesis | Entry point |
|------------|-------------|
| H2 / RQ2 (bank-branch density) | [`Checkpoint 2/H2_Pipeline/`](../Checkpoint%202/H2_Pipeline/) |
| H4 / RQ4 (housing cost / ZHVI) | [`Checkpoint 3/H4/`](../Checkpoint%203/H4/) + [`PHASE1_MANUAL_PIPELINE.md`](../Checkpoint%203/PHASE1_MANUAL_PIPELINE.md) |
| H5 / RQ5 (provider density) | [`Checkpoint 3/H5/`](../Checkpoint%203/H5/) |

**Effort:** days–weeks per hypothesis (see BENCHMARK). Every merge key, cleaning rule, and control set is a human decision.

### 2. Unrolled (Phase 2)

Pre-register an agenda (List A / List B), then run deterministic OLS in batch. The human still chooses *what* to test; the engine prevents mid-run p-hacking.

- Engine: [`Checkpoint 3/08_unrolled_loop.py`](../Checkpoint%203/08_unrolled_loop.py)
- Narrative: [`Checkpoint 3/PHASE2_UNROLLED_LOOP.md`](../Checkpoint%203/PHASE2_UNROLLED_LOOP.md)
- Artifacts: `Checkpoint 3/loop_results_v2/`

**Effort:** setup once; each batch is minutes.

### 3. Rolled (Phase 3)

Agents scout sources, critic-gate ToS, acquire via named adapters, propose hypotheses, and interpret — while **only** `09 --run` fits OLS (HC1 + Verifier gate for higher-order specs).

- Package: [`Checkpoint 4/`](../Checkpoint%204/)
- One command: [`Checkpoint 4/reproduce.sh`](../Checkpoint%204/reproduce.sh)
- Student entry: [`Checkpoint 4/STUDENT_QUICKSTART.md`](../Checkpoint%204/STUDENT_QUICKSTART.md)

**Effort:** offline demos in minutes once `cp3_modeling_frame.csv` exists.

## Time estimates (honest)

| Stage | Calendar effort (this team) | Wall-clock to *run* |
|-------|----------------------------|---------------------|
| Manual H2 then H4 then H5 | Days–weeks each (new sources/joins) | Script runs: minutes–tens of minutes after data present |
| Unrolled List A/B | Hours to design lists; minutes to execute | Minutes |
| Rolled `reproduce.sh` | — | Typically a few minutes once the CP3 frame + `.venv` exist |

Methodology: effort = calendar time specializing pipelines; run times = local machine demos (Jul 2026). See BENCHMARK for caveats.

## Self-check exercises

1. Run `bash "Checkpoint 4/reproduce.sh"` and paste the H4/H5 PASS β lines from `validation_check.md`.
2. Open `round1_results.md` and explain in two sentences why F02 **REJECT** is not a pipeline failure.
3. Copy `Checkpoint 4/configs/housing_services_chicago.json`, change only `geography` or `ntee_prefixes` in a new file, and predict whether Critic would block an HTTP scrape of a login-walled directory.

## Glossary

| Term | Meaning |
|------|---------|
| **HC1** | Heteroskedasticity-robust covariance for OLS SEs / Wald tests |
| **ΔR² ≥ 5e-4** | Minimum R² gain for higher-order ACCEPT (with Wald p < 0.05) |
| **Verifier gate** | Joint test: robust Wald F **and** ΔR² threshold on identical rows |
| **Unrolled** | Pre-registered list executed by deterministic code; human owns agenda |
| **Rolled** | Agents propose/adapt agenda; Stats Engine still owns coefficients |
| **NTEE** | IRS nonprofit activity classification codes (BMF) |
| **ZHVI** | Zillow Home Value Index (ZIP housing-cost proxy) |
| **EIN** | Employer Identification Number for the org |
| **Agent bus** | File message bus under `phase3_results/agent_bus/` |
| **`--fixture` / `--fixture-full`** | Offline teaching modes (no live HTTP / fuller bus payloads) |
| **Winsorization** | Cap extreme DV values (here p99 → `fundraising_efficiency_w`) |

## Supporting case study (optional)

Earlier NORP cohorts spent roughly a semester on raw data → clean → SQL → validate → prompt-engineer by hand. That history motivates automation. **Your Phase 1 in this repo is still H2/H4/H5 above**, not a re-run of Checkpoint 0.

## Registry & schema

- [`docs/HYPOTHESIS_REGISTRY.md`](HYPOTHESIS_REGISTRY.md)
- [`docs/DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
- [`AGENTS.md`](../AGENTS.md)
