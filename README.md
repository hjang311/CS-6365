# NORP Agentic Data Exploration Pipeline

**CS 4365/6365: Introduction to Enterprise Computing** · Georgia Institute of Technology · Summer 2026  
**Team 1:** Hwando Jang & Carla du Plessis · **Instructor:** Dr. Calton Pu

---

## Overview

Modern Non-Profit Organizations (NPOs) generate massive amounts of data through IRS Form 990 filings. Synthesizing this data with external sources (Census ACS, Zillow ZHVI, FDIC, Feed America) to discover actionable sociological correlations is highly labor-intensive.

This project builds a **multi-agent agentic data exploration pipeline** that evolves through three stages — Manual → Unrolled → Rolled — to teach **loop engineering and reproducibility**. The rolled stage uses specialized AI agents that autonomously scout data sources, acquire/merge datasets, propose hypotheses, and verify results through deterministic OLS with scientific guardrails.

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

Agents communicate through `agent_bus/messages.jsonl` (a file-based message bus). Higher-order specs face an **HC1 Wald F + ΔR² ≥ 5e-4 Verifier gate** — ACCEPT only when jointly significant AND explanatorily meaningful.

## Quick Start (Next Cohort)

### Prerequisites
- Python 3.10+
- Census API key (free: https://api.census.gov/data/key_signup.html)
- Clone and set up:

```bash
git clone https://github.com/hjang311/CS-6365.git
cd CS-6365
python3 -m venv .venv
source .venv/bin/activate
pip install -r "Checkpoint 4/requirements.txt"
cp .env.example .env   # then fill in your CENSUS_API_KEY
```

### Run everything offline (≈ minutes)

```bash
bash "Checkpoint 4/reproduce.sh"
```

Then read [`Checkpoint 4/STUDENT_QUICKSTART.md`](Checkpoint%204/STUDENT_QUICKSTART.md).

## Curriculum Map (Manual → Unrolled → Rolled)

| Stage | What you do | Where |
|-------|-------------|-------|
| **Manual (Phase 1)** | Human adjusts acquire → merge → clean → specify → OLS per hypothesis (H2, H4, H5) | [`Checkpoint 2/H2_Pipeline/`](Checkpoint%202/H2_Pipeline/), [`Checkpoint 3/PHASE1_MANUAL_PIPELINE.md`](Checkpoint%203/PHASE1_MANUAL_PIPELINE.md) |
| **Unrolled (Phase 2)** | Pre-registered List A/B + deterministic OLS engine; human still picks agenda | [`Checkpoint 3/08_unrolled_loop.py`](Checkpoint%203/08_unrolled_loop.py) |
| **Rolled (Phase 3)** | Multi-agent discover → acquire → propose → gated OLS; agents own the agenda | [`Checkpoint 4/`](Checkpoint%204/) |

Full teaching narrative: [`docs/CURRICULUM.md`](docs/CURRICULUM.md)  
Effort comparison: [`Checkpoint 4/BENCHMARK.md`](Checkpoint%204/BENCHMARK.md)

## Data Sources

| Dataset | Source | Used in |
|---------|--------|---------|
| NCCS CORE full-990 (2018–2022) | `nccsdata.s3.amazonaws.com` | CP2, CP3 |
| IRS Exempt Org BMF | `irs.gov/pub/irs-soi/` | CP2, CP3 |
| Census ACS5 (poverty, income, population) | `api.census.gov` (free key required) | CP2, CP3 |
| FDIC BankFind (branch locations) | `api.fdic.gov` (no key) | CP2 (H2) |
| Zillow ZHVI (Dec 2022 snapshot) | `files.zillowstatic.com` | CP3 (H4) |
| Feed America (GA food assistance sites) | `feedingamerica.org` (CC BY) | CP4 |
| NTEE density (from BMF) | Derived from IRS BMF | CP4 |

## Key Findings

- **H2 (bank-branch density):** Confirmed — lower branch density associated with higher fundraising efficiency (CP2)
- **H4 (housing cost / ZHVI):** Confirmed negative β — higher housing costs, lower efficiency (CP3)
- **H5 (provider density):** Theory rejected — observed positive β, opposite to competition hypothesis (CP3)
- **Phase 3 food/housing explorations:** Null results on density interactions; gate REJECT is first-class, not a failure (CP4)

See [`Checkpoint 4/NEGATIVE_FINDINGS.md`](Checkpoint%204/NEGATIVE_FINDINGS.md) for honest treatment of nulls.

## Repository Layout

```
Checkpoint 0/     Reproducibility exercise (NORP Spring 2026 exemplar)
Checkpoint 1/     Early agentic experiments (broadband × fundraising)
Checkpoint 2/     Manual H2 pipeline (bank-branch density)
Checkpoint 3/     Manual H4/H5 + unrolled loop (Phases 1 & 2)
Checkpoint 4/     Rolled multi-agent package — primary handoff (Phase 3)
docs/             Curriculum map + archive notes
.agent/skills/    Phase 3 agent skill definitions
agentic_pipeline/ Legacy SDK scaffolding (not Phase 3 entrypoint)
```

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
- [x] Repo cleaned for open-source presentation
- [ ] Final presentation

## License / Data Ethics

Respect source licenses (e.g., Feed America CC BY). Do not scrape login-walled partner directories. Named adapters + Critic ToS gates are intentional design — not limitations.
