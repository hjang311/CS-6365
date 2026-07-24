# Georgia Institute of Technology
# CS 4365/6365: Introduction to Enterprise Computing
# Summer 2026
# Project Checkpoint 4 Report

**Group:** NORP / CS-6365  
**Name(s):** HDJ (+ teammates as applicable)  
**Project Name:** NORP — Nonprofit Organizational Research Pipeline  
**Build attribution:** Checkpoint 4 Phase 3 implementation in `Checkpoint 4/Grok_4.5/` by **Grok 4.5** (plan by Fable 5)

---

## Context and Related Work / Project Plan (Plan)

### Context

Checkpoints 1–3 established a national 990 + ACS + ZHVI modeling frame and the professor’s three-phase pedagogy: **manual → unrolled → rolled**. Checkpoint 3 shipped Phases 1–2 (`08_unrolled_loop.py`, `loop_results_v2/`) and deliberately left Phase 3 unimplemented. Checkpoint 4 completes the rolled loop: the agent evaluates Phase 2 outcomes, proposes new indicators (including higher-order specs), and pursues finer-granularity Atlanta Community Food Bank (ACFB) partner data.

### Related work (prior art)

- **Google Co-Scientist** (Nature 2026; arXiv 2502.18864): multi-agent generate–debate–evolve hypothesis loop. Validates that “agent proposes, system verifies” is the credible architecture—verification is load-bearing.
- **DiscoveryBench** (ICLR 2025, allenai/discoverybench): multi-step data-driven discovery; best LLM systems score only ~25%, which justifies a constrained design.
- **Our differentiator:** pedagogical unrolled→rolled progression plus reproducibility guarantees (pre-registration, decision logs, H4/H5 calibration), not raw autonomy.

### Starting point

- Canonical frame: `Checkpoint 3/data/cp3_modeling_frame.csv`
- Phase 2 evidence: `Checkpoint 3/loop_results_v2/` (especially `two_variable_limitation.md`)
- Shared OLS recipe: HC1 robust OLS with fixed controls from `08_unrolled_loop.py`

### Project Deliverables

| Deliverable | Description | Technical Stack |
|-------------|-------------|-----------------|
| Phase 3 agentic loop | Evaluate / propose / pre-register / run / interpret | Python, statsmodels, stdin/hybrid/optional Gemini |
| Higher-order specs | Interaction OLS with controls de-duplicated for focal IVs | statsmodels formula API |
| ACFB / food-assistance pipeline | Pilot + Feed America CC BY GA scale → density/10k | Curated CSV + Feed America bulk API + pandas |
| Hybrid prompt live test | Cursor Task subagent executes PHASE3_HYBRID_PROMPT | Cursor Task / Antigravity |
| Progression + OH questions | Student narrative + unblock questions | Markdown |
| Checkpoint 4 report | Plan / Match / Factual | This document |

### Project Milestones

| Checkpoint | Milestone | Technical Scope & Deliverables | Work Split | Status |
|------------|-----------|--------------------------------|------------|--------|
| 1 | Foundation | Broadband × efficiency Georgia pilot | Team | Done |
| 2 | National frame | H2 bank density, ACS merge | Team | Done |
| 3 | Phases 1–2 | Manual + unrolled loop, limitation note | Team | Done (pushed) |
| 4 | Phase 3 + final | Rolled loop, hybrid test, Feed America scale | Grok 4.5 in `Grok_4.5/` | **Done** (official ACFB 700 list still unavailable; GA proxy scaled) |

---

## Current Progress Report (Match)

### Work completed (Checkpoint 4 / Grok 4.5)

- Scaffolded `Checkpoint 4/Grok_4.5/` with progression docs, professor questions, student guide.
- Implemented `09_phase3_agentic_loop.py` (evaluate / propose / run / interpret / validate; decision log; fixture + optional `--api`).
- **Hybrid live test (PASS):** Cursor Task subagent executed `PHASE3_HYBRID_PROMPT.md` → `proposals_round1_hybrid.json` (`source: hybrid`) → OLS via `09 --run` only → `HYBRID_TEST_REPORT.md`.
- ACFB AccessFood: no public dump (ToS-safe skip). **Stretch scale:** Feed America CC BY 4.0 GA bulk API → **1,432** agencies / **293** ZIPs after merge; 4 public ACFB CFCs; `--all --fixture --rounds 2` on expanded frame.
- `--api` skipped: `google-generativeai` not installed / optional; hybrid covers the no-key path.

### Comparison to Fable 5 plan

Matches: docs first, rolled loop, higher-order specs, ACFB pilot then best-effort scale. Stretch additions: hybrid Cursor execution evidence; Feed America as licensed finer-granularity proxy when ACFB bulk is unavailable.

### Coverage honesty

| Layer | Count |
|-------|-------|
| Curated pilot (pre-stretch) | 18 agencies / 13 ZIPs / 44 pilot ZIPs |
| Feed America GA raw | 2,250 rows / 470 ZIPs |
| Merged ACFB-area filter | **1,432 agencies / 293 ZIPs** |
| Official ACFB ~700 partners | **Not obtained** (label Feed America clearly as proxy) |

### Next steps

- Ask ACFB for an official partner export to replace / validate the proxy.
- Incorporate OH answers to `PROFESSOR_QUESTIONS.md`.
- Final presentation polish.

---

## Supporting Evidence (Factual)

### Paths

- Build root: `Checkpoint 4/Grok_4.5/`
- Loop: `09_phase3_agentic_loop.py`
- Acquisition: `10_acquire_soup_kitchens.py`, `11_merge_soup_kitchen_density.py`, `SOUP_KITCHEN_WORKFLOW.md`
- Hybrid: `prompts/PHASE3_HYBRID_PROMPT.md`, `HYBRID_TEST_REPORT.md`, `phase3_results/proposals_round1_hybrid.json`
- Results: `phase3_results/` (validation, evaluation, round1/2, hybrid, soup demos, `decision_log.jsonl`)
- Attribution: `data/FEEDAM_ATTRIBUTION.txt`, `data/coverage_report.md`

### Reproduction commands — executed 2026-07-12

```bash
.venv/bin/python "Checkpoint 4/Grok_4.5/10_acquire_soup_kitchens.py" --all-scale
.venv/bin/python "Checkpoint 4/Grok_4.5/11_merge_soup_kitchen_density.py"
.venv/bin/python "Checkpoint 4/Grok_4.5/09_phase3_agentic_loop.py" --validate
.venv/bin/python "Checkpoint 4/Grok_4.5/09_phase3_agentic_loop.py" --all --fixture --rounds 2 \
  --frame "Checkpoint 4/Grok_4.5/data/cp4_frame_with_soup_density.csv"
# Hybrid: Cursor Task ran PHASE3_HYBRID_PROMPT → proposals_round1_hybrid.json → --run --round 91
```

### Key execution results

| Check | Result |
|-------|--------|
| H4/H5 `--validate` | **PASS** |
| Hybrid Cursor Task | **PASS** (`source: hybrid`; H01/H02 confirmed; H03 rejected wrong-sign; H04 n.s.) |
| `--all --rounds 2` | **PASS** — round 2 uses `log_soup_kitchen_density` |
| Round 2 R2P01 density | β ≈ 1.30, p ≈ 0.57 → not significant (national) |
| Soup demo ACFB-area S01 | β ≈ 10.71, p ≈ 0.098, n = 1,965 → not significant (borderline) |
| Scale | **1,432** agencies / **293** ZIPs (Feed America GA proxy + pilot + CFCs) |
| `--api` Gemini | Skipped (`google-generativeai` not installed); hybrid covers no-key path |

### Feed America attribution (CC BY 4.0)

Feed America. (2026). Feed America Food-Assistance Directory [Dataset]. https://feedam.org/research. License: CC BY 4.0. Adapted/filtered to Georgia food_pantry/soup_kitchen/food_bank/mobile_pantry for NORP Checkpoint 4.

### Granularity audit + July 10 retest (follow-on)

- Audit: `DATA_GRANULARITY_AUDIT.md` — time FAIL (2026 sites on 2018–22 years); space PARTIAL; national OLS misaligned.
- Fix: `12_build_analysis_slice.py` → `cp4_atlanta_xsection.csv` (583 rows, tax_year=2022) and `cp4_atlanta_pilot_xsection.csv` (272 rows).
- ACFB workflow artifact: `acfb_zip_agent_collection.csv` (**317** sites / **41** ZIPs); prompt `PHASE3_ACFB_ZIP_COLLECT_PROMPT.md`.
- Hybrid retest on pilot xsection (nobs=211): AX01–AX05 all **not significant / exploratory** — see `round_atlanta_xsection_results.md` and interpretation. Headline is the **correct slice design**, not a significant β.

### Sample proposal pre-registration

See `phase3_results/proposals_atlanta_xsection.json` — `source: hybrid`, `pre_registered_before_ols: true`.

---

## Skill Learning Report

- **Pre-registration / agentic discovery:** Separating proposal JSON from OLS; hybrid Cursor subagent orchestration; `decision_log.jsonl`.
- **Higher-order model specs:** Interaction terms with focal IVs removed from shared controls.
- **Finer-granularity data workflows:** AccessFood ToS boundary; Feed America CC BY bulk scale; density-per-10k merges.
- **Pedagogical systems design:** Unrolled→rolled progression; bounded `--all --rounds 2`.

---

## Self-Evaluation

- **Plan:** 5 — Phase 3 + stretch (hybrid + Feed America) match professor tracks.
- **Match:** 5 — Hybrid PASS; 1,432-agency scale; official ACFB 700 list honestly unavailable.
- **Factual:** 5 — Commands, paths, and coefficients from local runs.

## LLM Feedback

- **Project Plan (Plan):** Strong prior-art framing; cite Feed America license on slides.
- **Progress Report (Match):** Emphasize hybrid verification invariant and proxy-vs-official ACFB boundary.
- **Supporting Evidence (Factual):** Point TAs at `HYBRID_TEST_REPORT.md`, `coverage_report.md`, `--validate` PASS.

### Actionable Suggestions

- Confirm interaction OLS as “higher-order” (question b).
- Ask ACFB for official partner export to validate Feed America proxy (question c/d).
