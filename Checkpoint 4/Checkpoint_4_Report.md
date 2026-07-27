# Georgia Institute of Technology
# CS 4365/6365: Introduction to Enterprise Computing
# Summer 2026
# Project Checkpoint 4 Report

**Group:** 1  
**Name(s):** Hwando Jang & Carla du Plessis  
**Project Name:** NORP Agentic Data Exploration Pipeline  
**Build attribution:** Canonical Phase 3 multi-agent loop under `Checkpoint 4/` (earlier build trail retained in `Grok_4.5/` as **provenance only**)

---

## Context and Related Work / Project Plan (Plan)

### Context (end of Checkpoint 3)

Checkpoints 1–3 established the national 990 + ACS + ZHVI frame and the course pedagogy **manual → unrolled → rolled**. Checkpoint 3 shipped Phases 1–2 (Manual H4/H5; Unrolled List A/B) and **intentionally deferred** Phase 3. CP3 also left two concrete repo gaps called out in self-eval / LLM feedback: a standalone RQ2 verification write-up and a Mode B drift note. Those are now closed under `Checkpoint 3/RQ2/` and `Checkpoint 3/MODE_B_DRIFT.md`.

July 22 office hours (Option 2) prioritized **educating the next cohort** on workflow / loop engineering over promotional outreach. Checkpoint 4 therefore delivers the **rolled multi-agent loop** *and* packages the repo as a teaching artifact (`reproduce.sh`, `STUDENT_QUICKSTART.md`, `BENCHMARK.md`, `docs/CURRICULUM.md`).

### Related work

- **InsightPilot (Ma et al., 2023):** named, auditable operations — our adapter + Stats Engine design (LLM does not free-form fit models).
- **Multi-agent orchestration pattern:** specialized roles + shared thread; we use a file message bus (`agent_bus/`) and hard scientific guardrails (no LLM OLS).
- **TA higher-order Verifier specs:** interaction/quadratic proposals with HC1 Wald F + ΔR² gate — absorbed into `09 --verify-ta-specs` / `--run`. Evidence is in-repo (`phase3_results/ta_verify/`); no separate suggestion-branch tree is required to verify claims.

### Research questions status (registry)

See [`docs/HYPOTHESIS_REGISTRY.md`](../docs/HYPOTHESIS_REGISTRY.md) for the full ID map. Headline status:

| ID | Status |
|----|--------|
| RQ1 | Null baseline (CP1) |
| RQ2 / H2 | Confirmed (CP2; CP3 List A replay; RQ2 verification write-up) |
| RQ3 | Feasibility only |
| RQ4 / H4 | Confirmed (β = −7.91647; PASS reproduction in CP4 validate) |
| RQ5 / H5 | Theory rejected (β = +2.11963; agglomeration reading) |
| F01/F02, H01/H02 | Phase 3 finer-granularity / universality — nulls & gate REJECT first-class |
| I1–I4 / Q1 | TA Verifier demo — mostly REJECT; I3 ACCEPT |

### Deliverables

| Deliverable | Path / stack |
|-------------|--------------|
| Multi-agent Phase 3 runner | `09_phase3_agentic_loop.py` (v2.1: Verifier gate) |
| Enrichment adapters | `enrichment_tools/` (ntee, http_open_api, web_download, merge, slice, agent_bus) |
| Configs (food Atlanta HTTP/NTEE; housing Chicago) | `configs/` |
| Skills | `.agent/skills/norp-{orchestrator,scout,acquisition,researcher,validator,code-agent}/` |
| Hybrid master prompt | `prompts/PHASE3_MULTI_AGENT_LOOP.md` |
| CP3 gaps closed | `Checkpoint 3/RQ2/RQ2_VERIFICATION_RUN.md`, `Checkpoint 3/MODE_B_DRIFT.md` |
| Education packaging (July 22 OH Option 2) | `BENCHMARK.md`, `reproduce.sh`, `STUDENT_QUICKSTART.md`, `docs/CURRICULUM.md`, root `README.md`, `AGENTS.md` |
| Negatives | `NEGATIVE_FINDINGS.md` |
| Handoff CLI | `HANDOFF_GUIDE.md` |

### Milestone #4 status

**Phase 3 (rolled) + final packaging — core complete:** live/hybrid multi-agent evaluate→scout→critic→acquire→pre-register→OLS with Wald/ΔR² gate; Round 2 adaptation; food HTTP + housing NTEE universality; CP3 RQ2 + Mode B artifacts closed; **repo packaged as an education-first open-source curriculum** (Manual → Unrolled → Rolled). Team final presentation outline remains **local** (gitignored) — not a student deliverable.

---

## Current Progress Report (Match)

### What we shipped

1. **Canonical `Checkpoint 4/` tree** with message bus (`agent_bus/messages.jsonl`) and extended decision log (`scout`, `acquire`, `critic`, `enrich`, `degrade`).
2. **Acquisition ladder** with real web: Feed America `http_open_api` (~**2,250** GA entities); NTEE fallback; Critic ToS-block then approve; Atlanta/Chicago × latest-year slices.
3. **Multi-agent protocol** — Scout / Critic / Acquisition / Researcher / Stats; `09 --run` is the only OLS engine.
4. **TA Verifier gate** — interaction/quadratic specs fit nested models on identical rows; ACCEPT only if HC1 Wald F p < 0.05 **and** ΔR² ≥ 5e-4.
5. **Universality** — housing Chicago via NTEE (HTTP folder empty by design; see acquisitions README).
6. **Negative findings + Round 2 adaptation** after food nulls (`NEGATIVE_FINDINGS.md` with embedded numbers).
7. **CP3 carry-forwards closed** — standalone RQ2 verification; Mode B drift formalized.
8. **Packaging & pedagogy** — curriculum map, benchmark, one-command `reproduce.sh` with preflight, student quickstart, hypothesis registry, data dictionary; semester clutter local-only under `archive/`.

### Embedded results (graders can verify without hunting)

#### H4/H5 calibration (`phase3_results/validation_check.md`)

| Hypothesis | IV | Expected β | Loop β | Status |
|------------|-----|------------|--------|--------|
| H4 / RQ4 | `log_zhvi_2022` | −7.91647 | −7.91647 | **PASS** |
| H5 / RQ5 | `log_nonprofit_branch_density` | +2.11963 | +2.11963 | **PASS** |

Frame: `Checkpoint 3/data/cp3_modeling_frame.csv` (158,323 × 30).

#### Food Atlanta Round 1 (`phase3_results/round1_results.md`)

| ID | β | p | n | Gate | Outcome |
|----|---|---|---|------|---------|
| F01 food density | −21.46836 | 0.1176 | 444 | n/a | Not significant |
| F02 poverty × density | 0.39393 | 0.8530 | 444 | **REJECT** | Null |

#### Housing Chicago Round 1 (`phase3_results/housing_chicago/round1_results.md`)

| ID | β | p | n | Gate | Outcome |
|----|---|---|---|------|---------|
| H01 housing density | 5.04243 | 0.4475 | 403 | n/a | Exploratory / n.s. |
| H02 poverty × housing | 0.42692 | 0.7661 | 403 | **REJECT** | Null |

#### TA Verifier (`phase3_results/ta_verify/round99_results.md`)

| ID | Gate |
|----|------|
| I1, I2, I4, Q1 | **REJECT** |
| I3 (ZHVI × size_segment) | **ACCEPT** |

### Honest gaps

- Official ACFB ~700 partner census still unavailable (ToS); Feed America remains the licensed proxy.
- Temporal join caveat (site stock vs 990 years) still requires geography × latest-year slices.
- Housing has no open HTTP bulk API in-repo — NTEE universality, not HTTP parity.
- Antigravity SDK fleet runtime remains hybrid IDE-primary.
- Fresh-clone Mode B drift vs handoff frame is documented rather than forced to 1e-3 PASS (`MODE_B_DRIFT.md`).

### Plans for next days

- Team final presentation (outline local / gitignored — not pushed as student curriculum).

---

## Packaging & Reproducibility (July 22 OH — Option 2)

Office hours prioritized **educating the next cohort** on workflow power. Mapping OH goals → artifacts:

| OH Option 2 goal | Artifact |
|------------------|----------|
| Manual vs automated effort comparison | [`BENCHMARK.md`](BENCHMARK.md) |
| Students run the loop without fear | [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md), fear table |
| One-command offline demos | [`reproduce.sh`](reproduce.sh) (preflight + elapsed + expected checks) |
| Teaching map Manual → Unrolled → Rolled | [`docs/CURRICULUM.md`](../docs/CURRICULUM.md) |
| Clean public GitHub surface | [`docs/ARCHIVE.md`](../docs/ARCHIVE.md); local `archive/` |
| LLM / collaborator state | [`AGENTS.md`](../AGENTS.md) |
| ID clarity | [`docs/HYPOTHESIS_REGISTRY.md`](../docs/HYPOTHESIS_REGISTRY.md) |
| Schema clarity | [`docs/DATA_DICTIONARY.md`](../docs/DATA_DICTIONARY.md) |

Students are expected to **run the rolled loop**, then read backward into Manual/Unrolled recipes — not re-suffer per-hypothesis pipeline edits. Checkpoint 0 remains **optional prior-semester context only**.

---

## Supporting Evidence (Factual)

| Claim | Evidence | What to look for |
|-------|----------|------------------|
| H4/H5 calibration | `phase3_results/validation_check.md` | PASS rows; β match within 1e-3 |
| Verifier gate | `ta_verify/round99_results.md` | Gate column; I3 ACCEPT |
| Live multi-agent food run | `phase3_results/` + `data/acquisitions/food_assistance/` | ~2250 entities; attribution CC BY |
| Fixture-full ToS path | `agent_bus/` critic verdicts + decision_log | Block then approve / degrade events |
| Food / housing nulls | `NEGATIVE_FINDINGS.md` + `round*_results.md` | Embedded β/p/n/gate |
| RQ2 standalone | `Checkpoint 3/RQ2/RQ2_VERIFICATION_RUN.md` | Parallel to H4/H5 write-ups |
| Mode B drift | `Checkpoint 3/MODE_B_DRIFT.md` | Contracts + β deltas vs handoff |
| Housing NTEE-only | `data/acquisitions/housing_services/README.md` | Empty HTTP folder by design |
| Education packaging | root `README.md`, `reproduce.sh`, CURRICULUM, BENCHMARK | Expected outputs + preflight |
| Code license | root `LICENSE` | MIT for code/docs |

`Checkpoint 4/Grok_4.5/Checkpoint_4_Report.md` is **provenance only** — graders should use **this** file.

### Self-evaluation

1. **Plan: 118/120** — Delivered deferred Phase 3 plus July 22 educational packaging with concrete paths (runner, adapters, gate, reproduce, curriculum). Deduction: team presentation is intentionally not a public student artifact yet.
2. **Match: 112/120** — Live/hybrid loop, HTTP acquisition, universality, negatives with numbers, RQ2/Mode B closed, teaching docs deepened. Deduction: ACFB official list still out of scope; Mode B remains drift-documented rather than bit-identical to handoff PASS.
3. **Factual: 96/100** — Embedded tables for validate / food / housing / TA gates; decision log; attribution; registry. Deduction: some live HTTP counts depend on network snapshot date; offline fixtures are the guaranteed teaching path.

### LLM feedback prompt

> Considering this report and our self-evaluation, score Plan ( /120), Match ( /120), and Factual ( /100). Suggest what to tighten before the final team presentation (local outline only — not student GitHub curriculum).

---

## References

[1] Federal Deposit Insurance Corporation. BankFind Suite / Summary of Deposits API. https://banks.data.fdic.gov/  
[2] Ma, P., Ding, R., Wang, S., Han, S., & Zhang, D. (2023). InsightPilot: An LLM-empowered automated data exploration system. *EMNLP 2023 System Demonstrations*. https://aclanthology.org/2023.emnlp-demo.31  
[3] National Center for Charitable Statistics, Urban Institute. Core data series (Form 990). https://nccs.urban.org/  
[4] Feeding America. Food bank locator / open data (CC BY). Attribution: `Checkpoint 4/data/acquisitions/food_assistance/food_assistance_ATTRIBUTION.txt`  
[5] U.S. Census Bureau. American Community Survey 5-year estimates. https://www.census.gov/programs-surveys/acs  
[6] Zillow Research. ZHVI ZIP time series (research CSV terms). https://www.zillow.com/research/data/  
[7] Internal Revenue Service. Exempt Organizations Business Master File. https://www.irs.gov/charities-non-profits  
