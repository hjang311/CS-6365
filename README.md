# NORP Agentic Data Exploration Pipeline

**CS 4365/6365: Introduction to Enterprise Computing** · Georgia Institute of Technology · Summer 2026  
**Team 1:** Hwando Jang & Carla du Plessis · **Instructor:** Dr. Calton Pu  
**License:** [MIT](LICENSE) for code/docs · third-party datasets keep their own licenses

---

## Overview

Modern Non-Profit Organizations (NPOs) generate massive amounts of data through IRS Form 990 filings. Synthesizing this data with external sources (Census ACS, Zillow ZHVI, FDIC, Feed America) to discover actionable sociological correlations is highly labor-intensive.

This project builds a **multi-agent agentic data exploration pipeline** that evolves through three stages — **Manual → Unrolled → Rolled** — to teach **loop engineering and reproducibility** (July 22 OH Option 2: education-first packaging). The rolled stage uses specialized AI agents that scout data sources, acquire/merge datasets, propose hypotheses, and verify results through deterministic OLS with scientific guardrails.

**Where to start as a next-cohort student:** run the rolled loop first (`Checkpoint 4/reproduce.sh`), then read Manual/Unrolled recipes backward. Optionally skim Checkpoint 0 only as *historical* motivation (what prior semesters had to do by hand) — it is **not** Phase 1 of this curriculum.

## System Architecture (Phase 3 — Rolled Loop)

```
Orchestrator → Scout → Critic → Acquisition → Researcher → Stats Engine (09 --run) → Interpret
```

| Agent | Role |
|-------|------|
| **Orchestrator** | High-level strategic planner; delegates tasks to specialized agents |
| **Scout** | Discovers and ranks open data sources → `source_candidates.json` |
| **Critic** | Gates ToS/license compliance; blocks forbidden sources before acquisition |
| **Acquisition** | Runs named adapters (`ntee_density`, `http_open_api`, `web_download`) on approved plans |
| **Researcher** | Proposes and interprets hypotheses based on acquired data |
| **Stats Engine** | Deterministic OLS with HC1 robust errors — the **only** component that fits models. LLM never touches coefficients |

Agents communicate through `agent_bus/messages.jsonl` (a file-based message bus). Higher-order specs face an **HC1 Wald F + ΔR² ≥ 5e-4 Verifier gate** — ACCEPT only when jointly significant **and** explanatorily meaningful.

LLM / agent project state: [`AGENTS.md`](AGENTS.md). Skills: `.agent/skills/norp-*`.

## Quick Start (Next Cohort)

### Prerequisites

- Python **3.10+** (see [`.python-version`](.python-version); verified teaching stack: Python 3.10+ on macOS, Jul 2026)
- Census API key only if you regenerate federal sources from scratch ([signup](https://api.census.gov/data/key_signup.html))
- Offline demos need the CP3 modeling frame (gitignored CSV — see below)

```bash
git clone https://github.com/hjang311/CS-6365.git
cd CS-6365
python3 -m venv .venv
source .venv/bin/activate
pip install -r "Checkpoint 4/requirements.txt"
cp .env.example .env   # fill CENSUS_API_KEY only if doing Mode B acquire
```

### Modeling-frame prerequisite (important)

`Checkpoint 3/data/cp3_modeling_frame.csv` (~158k rows × 30 cols) is **gitignored**. Offline `reproduce.sh` **fails fast** with regenerate instructions if it is missing.

- **Mode A** (handoff CSVs under `Checkpoint 3/data/`): run `02_merge_pipeline.py` — see [`Checkpoint 3/README.md`](Checkpoint%203/README.md)
- **Mode B** (fresh acquire): follow Mode B in that same README (`CENSUS_API_KEY` + network)

### Run everything offline (≈ minutes once the frame exists)

```bash
bash "Checkpoint 4/reproduce.sh"
```

**Expected self-checks** (also printed by the script):

| Step | Artifact | What you should see |
|------|----------|---------------------|
| H4/H5 calibration | `Checkpoint 4/phase3_results/validation_check.md` | `H4: PASS` β ≈ **−7.91647**; `H5: PASS` β ≈ **+2.11963** |
| TA Verifier | `.../ta_verify/round99_results.md` | I1/I2/Q1 **REJECT**; I3 **ACCEPT**; I4 **REJECT** |
| Food Atlanta | `.../round1_results.md` | F01 not significant; F02 gate **REJECT** |
| Housing Chicago | `.../housing_chicago/round1_results.md` | H01 exploratory; H02 gate **REJECT** |

Then read [`Checkpoint 4/docs/STUDENT_QUICKSTART.md`](Checkpoint%204/docs/STUDENT_QUICKSTART.md) and [`docs/CURRICULUM.md`](docs/CURRICULUM.md).

## Curriculum Map (Manual → Unrolled → Rolled)

| Stage | What you do | Where |
|-------|-------------|-------|
| **Manual (Phase 1)** | Human adjusts acquire → merge → clean → specify → OLS per hypothesis (H2, H4, H5) | [`Checkpoint 2/H2_Pipeline/`](Checkpoint%202/H2_Pipeline/), [`Checkpoint 3/PHASE1_MANUAL_PIPELINE.md`](Checkpoint%203/PHASE1_MANUAL_PIPELINE.md) |
| **Unrolled (Phase 2)** | Pre-registered List A/B + deterministic OLS engine; human still picks agenda | [`Checkpoint 3/08_unrolled_loop.py`](Checkpoint%203/08_unrolled_loop.py) |
| **Rolled (Phase 3)** | Multi-agent discover → acquire → propose → gated OLS; agents own the agenda | [`Checkpoint 4/`](Checkpoint%204/) |

Optional history: [`Checkpoint 0/`](Checkpoint%200/) = prior-semester package reproduction (what earlier cohorts had to do). **Not** Phase 1 of this repo.

Full teaching narrative: [`docs/CURRICULUM.md`](docs/CURRICULUM.md)  
Effort comparison: [`Checkpoint 4/docs/BENCHMARK.md`](Checkpoint%204/docs/BENCHMARK.md)  
Hypothesis ID map: [`docs/HYPOTHESIS_REGISTRY.md`](docs/HYPOTHESIS_REGISTRY.md)  
Column definitions: [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md)

## Data Sources

| Dataset | Source | License / access | Used in |
|---------|--------|------------------|---------|
| NCCS CORE full-990 (2018–2022) | `nccsdata.s3.amazonaws.com` | Urban Institute / NCCS terms | CP2, CP3 |
| IRS Exempt Org BMF | `irs.gov/pub/irs-soi/` | Public IRS SOI | CP2, CP3, CP4 NTEE |
| Census ACS5 (poverty, income, population) | `api.census.gov` | Public (free API key) | CP2, CP3 |
| FDIC BankFind (branch locations) | `api.fdic.gov` | Public (no key) | CP2 (H2) |
| Zillow ZHVI (Dec 2022 snapshot) | `files.zillowstatic.com` | Zillow research CSV terms | CP3 (H4) |
| Feed America (GA food assistance sites) | `feedingamerica.org` | **CC BY** — see attribution file | CP4 |
| NTEE density (from BMF) | Derived | Same as BMF | CP4 |

Feed America attribution: [`Checkpoint 4/data/acquisitions/food_assistance/food_assistance_ATTRIBUTION.txt`](Checkpoint%204/data/acquisitions/food_assistance/food_assistance_ATTRIBUTION.txt).

## Key Findings (with numbers)

| ID | Result | Numbers | Artifact |
|----|--------|---------|----------|
| **RQ2 / H2** | Confirmed (fintech-substitution proxy) | OLS β ≈ **−0.11453**, p ≈ **0.0017** | `Checkpoint 2/H2_Pipeline/findings_results.md` |
| **RQ4 / H4** | Confirmed negative housing-cost effect | β = **−7.91647** (reproduced PASS) | `Checkpoint 4/phase3_results/validation_check.md` |
| **RQ5 / H5** | Theory **rejected** (positive / agglomeration) | β = **+2.11963** (reproduced PASS) | same validation check |
| **CP4 F01** | Food-density null on Atlanta slice | β ≈ **−21.47**, p ≈ **0.118**, n = **444** | `phase3_results/round1_results.md` |
| **CP4 F02** | Poverty × food density | Gate **REJECT** (ΔR² ≪ 5e-4) | same |
| **CP4 H01/H02** | Housing Chicago exploratory / null | H01 p ≈ 0.45; H02 gate **REJECT** | `phase3_results/housing_chicago/round1_results.md` |

Gate REJECT / nulls are **first-class** — see [`Checkpoint 4/docs/NEGATIVE_FINDINGS.md`](Checkpoint%204/docs/NEGATIVE_FINDINGS.md).

## Limitations

- **DV proxy:** fundraising efficiency uses reported fundraising expense fields; many orgs under-itemize.
- **Temporal join:** site / NTEE stock vs multi-year 990 filings — CP4 uses geography × latest-year slices.
- **ToS:** login-walled partner directories are Critic-blocked; Feed America is the licensed HTTP proxy, not an official ACFB census.
- **Offline vs live:** `reproduce.sh` uses fixtures / committed enrichments; live HTTP needs network and license respect.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `reproduce.sh` exits on missing frame | Regenerate `cp3_modeling_frame.csv` (CP3 Mode A/B) |
| `ImportError: statsmodels` / pandas | `pip install -r "Checkpoint 4/requirements.txt"` inside `.venv` |
| Census acquire fails | Export `CENSUS_API_KEY`; CP2 acquire does not auto-load `.env` |
| Feed America HTTP fails | Expected degrade to NTEE; see `decision_log.jsonl` |

## Repository Layout

```
Checkpoint 0/     Prior-semester case study only (optional skim)
Checkpoint 1/     Early broadband × fundraising experiments
Checkpoint 2/     Manual H2 pipeline (bank-branch density)
Checkpoint 3/     Manual H4/H5 + unrolled loop (Phases 1 & 2)
Checkpoint 4/     Rolled multi-agent package — primary student handoff (studio layout)
  docs/           Teaching + science write-ups + STRUCTURE.md
  prompts/        Hybrid IDE orchestrator paste prompts (canonical)
  engine/         Adapters + enrichment helpers (back-of-house)
  provenance/     Earlier build trail (early_build) — not the entrypoint
docs/             CURRICULUM, ARCHIVE, HYPOTHESIS_REGISTRY, DATA_DICTIONARY
AGENTS.md         LLM / collaborator project-state handoff
LICENSE           MIT (code/docs)
.agent/skills/    Phase 3 agent skill / role contracts (hybrid or SDK)
agentic_pipeline/ Legacy Antigravity SDK scaffolding (not Phase 3 entry)
```

Canonical Phase 3 entry: `Checkpoint 4/09_phase3_agentic_loop.py` (+ `prompts/` for live hybrid orchestration).  
Studio map: [`Checkpoint 4/docs/STRUCTURE.md`](Checkpoint%204/docs/STRUCTURE.md).  
Provenance only: `Checkpoint 4/provenance/early_build/`.  
Legacy SDK: `agentic_pipeline/` — see its README; students use hybrid prompts + skills + `09` instead.

## Current Progress

- [x] Phase 1: Manual hypothesis pipelines (H2, H4, H5)
- [x] Phase 2: Unrolled deterministic loop (List A/B)
- [x] Phase 3: Multi-agent rolled loop with Verifier gate
- [x] TA Verifier gate (HC1 Wald F + ΔR² ≥ 5e-4)
- [x] Live HTTP acquisition (Feed America) + NTEE fallback
- [x] Housing Chicago universality (NTEE-only)
- [x] Negative findings documented as first-class outputs
- [x] CP3 carry-forwards closed (RQ2, Mode B drift)
- [x] Education packaging (BENCHMARK, STUDENT_QUICKSTART, reproduce.sh)
- [x] Repo cleaned for open-source / next-cohort teaching
- [ ] Final course presentation (team-local; not a student deliverable)

## License / Data Ethics

- **This repository’s code and documentation:** [MIT](LICENSE).
- **Datasets:** remain under source licenses (e.g., Feed America CC BY). Do not scrape login-walled partner directories. Named adapters + Critic ToS gates are intentional design — not limitations.
