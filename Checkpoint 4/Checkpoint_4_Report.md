# Georgia Institute of Technology
# CS 4365/6365: Introduction to Enterprise Computing
# Summer 2026
# Project Checkpoint 4 Report

**Group:** 1  
**Name(s):** Hwando Jang & Carla du Plessis  
**Project Name:** NORP Agentic Data Exploration Pipeline  
**Build attribution:** Canonical Phase 3 multi-agent loop under `Checkpoint 4/` (Grok 4.5 provenance retained in `Grok_4.5/`)

---

## Context and Related Work / Project Plan (Plan)

### Context

Checkpoints 1–3 established the national 990 + ACS + ZHVI frame and the course pedagogy **manual → unrolled → rolled**. CP3 shipped Phases 1–2 and deferred Phase 3 (TA feedback: the ambitious agentic core remained unproven). Checkpoint 4 delivers that **multi-agent rolled loop** plus the TA Verifier gate from `ai-suggestions/cp4`.

### Related work

- InsightPilot (Ma et al., 2023): named, auditable operations — our adapter + Stats Engine design.
- Anthropic-style multi-agent orchestration: specialized roles + shared thread; we use a file message bus instead of Slack, and hard scientific guardrails (no LLM OLS).
- TA `09_rolled_agentic_loop.py`: deterministic higher-order proposer + Wald/ΔR² gate — absorbed into our `09 --run` engine while retaining live enrichment and multi-agent bus.

### Deliverables

| Deliverable | Path / stack |
|-------------|--------------|
| Multi-agent Phase 3 runner | `09_phase3_agentic_loop.py` (v2.1: Verifier gate) |
| Enrichment adapters | `enrichment_tools/` (ntee, http_open_api, web_download, merge, slice, agent_bus) |
| Configs (food Atlanta HTTP/NTEE; housing Chicago) | `configs/` |
| Skills CP1→CP4 | `.agent/skills/norp-{orchestrator,scout,acquisition,researcher,validator,code-agent}/` |
| Hybrid master prompt | `prompts/PHASE3_MULTI_AGENT_LOOP.md` |
| CP3 gaps closed | `Checkpoint 3/RQ2/RQ2_VERIFICATION_RUN.md`, `Checkpoint 3/MODE_B_DRIFT.md` |
| Handoff + negatives + slides | `HANDOFF_GUIDE.md`, `NEGATIVE_FINDINGS.md`, `PRESENTATION_OUTLINE.md` |
| Education packaging (July 22 OH Option 2) | `BENCHMARK.md`, `reproduce.sh`, `STUDENT_QUICKSTART.md`, `docs/CURRICULUM.md` |

### Milestone #4 status

**Phase 3 (rolled) + final** — **core complete**: live/hybrid multi-agent evaluate→scout→critic→acquire→pre-register→OLS with Wald/ΔR² gate; Round 2 adaptation; food HTTP + housing NTEE universality; CP3 RQ2 + Mode B artifacts closed; **repo packaged as an education-first open-source curriculum** (Manual → Unrolled → Rolled).

---

## Current Progress Report (Match)

### What we shipped

1. **Canonical `Checkpoint 4/` tree** with message bus (`agent_bus/messages.jsonl`) and extended decision log (`scout`, `acquire`, `critic`, `enrich`, `degrade`, acquire overwrite).
2. **Acquisition ladder** with real web: Feed America `http_open_api` (2,250 GA entities); NTEE fallback; Critic ToS-block then approve; Atlanta/Chicago × latest-year slices.
3. **Multi-agent protocol** — Scout / Critic / Acquisition / Researcher / Stats; `09 --run` is the only OLS engine.
4. **TA Verifier gate** — interaction/quadratic specs fit nested models on identical rows; ACCEPT only if HC1 Wald F p < 0.05 **and** ΔR² ≥ 5e-4 (`--verify-ta-specs` for I1–I4/Q1).
5. **Universality** — housing Chicago via NTEE (HTTP folder empty by design; see acquisitions README).
6. **Negative findings + Round 2 adaptation** after food nulls (`NEGATIVE_FINDINGS.md`).
7. **CP3 carry-forwards closed** — standalone RQ2 verification write-up; Mode B drift formalized.
8. **Packaging & pedagogy** — curriculum map, benchmark (Manual H2/H4/H5 vs Unrolled vs Rolled), one-command `reproduce.sh`, student quickstart; semester clutter moved under local `archive/` (personal research notes stay gitignored).

### Honest gaps

- Official ACFB ~700 partner census still unavailable (ToS); Feed America remains the licensed proxy.
- Temporal join caveat (site stock vs 990 years) still requires geography × latest-year slices.
- Housing has no open HTTP bulk API in-repo — NTEE universality, not HTTP parity.
- Antigravity SDK fleet runtime remains hybrid IDE-primary.

### Plans for next days

- Final presentation from `PRESENTATION_OUTLINE.md` (education / workflow arc).

---

## Packaging & Reproducibility (July 22 OH — Option 2)

Office hours prioritized **educating the next cohort** on workflow power over promotional video outreach. This checkpoint packages the rolled loop as a solid open-source teaching artifact:

| Artifact | Role |
|----------|------|
| [`docs/CURRICULUM.md`](../docs/CURRICULUM.md) | Manual → Unrolled → Rolled teaching map |
| [`BENCHMARK.md`](BENCHMARK.md) | Direct effort comparison; Phase 1 = **this project’s** H2/H4/H5 manual pipelines |
| [`reproduce.sh`](reproduce.sh) | One-command offline demos for future students |
| [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md) | Fear-reducing onboarding (no LLM math; ToS gates) |
| [`docs/ARCHIVE.md`](../docs/ARCHIVE.md) | What was cleaned from the semester dump (personal notes never pushed) |

Students are expected to **run the rolled loop**, then read backward into Manual/Unrolled recipes—not re-suffer per-hypothesis pipeline edits.

---

## Supporting Evidence (Factual)

| Claim | Evidence |
|-------|----------|
| H4/H5 calibration | `phase3_results/validation_check.md` (PASS) |
| Verifier gate | `round*_results.*` gate columns; `--verify-ta-specs` → `round99_results.*` |
| Live multi-agent food run | `phase3_results/` + `data/acquisitions/food_assistance/` |
| Fixture-full ToS block | `agent_bus/critic_verdict_blocked.json` then approved verdict |
| Food / housing nulls | `NEGATIVE_FINDINGS.md` |
| RQ2 standalone | `Checkpoint 3/RQ2/RQ2_VERIFICATION_RUN.md` |
| Mode B drift | `Checkpoint 3/MODE_B_DRIFT.md` |
| Housing NTEE-only | `data/acquisitions/housing_services/README.md` |
| Education packaging | `BENCHMARK.md`, `reproduce.sh`, `STUDENT_QUICKSTART.md`, root `README.md` |

### Self-evaluation (draft)

1. **Plan:** Strong — CP3 deferred Phase 3 delivered; July 22 packaging framed as educational OSS.  
2. **Match:** Strong — live loop, adapters, gate, Round 2, RQ2/Mode B, curriculum cleanup; ACFB official list still out of scope.  
3. **Factual:** Strong — real HTTP rows, gated OLS tables, decision log, negative findings, reproducible offline script.

### LLM feedback prompt

> Considering this report, score Plan / Match / Factual and suggest what to tighten before the final presentation.
