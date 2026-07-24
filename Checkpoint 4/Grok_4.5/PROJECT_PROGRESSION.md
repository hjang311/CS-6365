# Project Progression: Phase 1 → 2 → 3 (and Beyond)

**Audience:** next students continuing NORP / CS 6365  
**Build:** Checkpoint 4 / `Grok_4.5/` (implements the professor’s rolled Phase 3)

## Why the order matters

The course’s July 2026 office-hour model is pedagogical, not just engineering:

| Phase | Who chooses the next test? | What students learn |
|-------|----------------------------|--------------------|
| **1 — Manual** | You | Data contracts, merge pain, one hypothesis at a time |
| **2 — Unrolled** | You (list written *before* the run) | Pre-registration, reproducible OLS, why 2-var scanners lie |
| **3 — Rolled / agentic** | The LLM, after seeing results | Propose → verify; agent proposes, Python verifies |

Skipping Phase 2 and jumping to an autonomous loop hides the load-bearing idea: **verification, not generation**, is what makes agentic discovery credible.

## Phase 1 — Manual (Checkpoint 3)

- Acquire NCCS / BMF / ACS / ZHVI; build `cp3_modeling_frame.csv`.
- Hand-run H4 (ZHVI → fundraising efficiency) and H5 (provider density → efficiency).
- Artifacts: `01`–`06`, `H4/`, `H5/`, `PHASE1_MANUAL_PIPELINE.md`.

**Automated:** nothing about hypothesis choice. Humans pick and interpret every test.

## Phase 2 — Unrolled loop (Checkpoint 3)

- Explicit List A (theory-first) + List B (bounded limitation harness).
- Deterministic HC1 OLS; H4/H5 β calibration asserts.
- Agent does **not** invent pairs mid-run.
- Artifacts: `08_unrolled_loop.py`, `loop_results_v2/`, especially `two_variable_limitation.md`.

**Automated:** execution of a fixed agenda. **Not automated:** rewriting the agenda from results.

## Phase 3 — Rolled agentic loop (this folder)

Three tracks from the professor’s July 10 guidance:

1. **Evaluate → propose → test** — review which correlations held vs failed; ask the LLM which other socioeconomic indicators *could* correlate; pre-register; run the shared OLS recipe.
2. **Higher-order correlations** — 3+ variable / interaction specs (`DV ~ IV1 + IV2 + IV1:IV2 + controls`), because 2-var tests on this frame are easy to light up and hard to trust.
3. **Finer-granularity data (favorite)** — Atlanta Community Food Bank partner map → soup-kitchen / pantry density by ZIP → compare against the coarse IRS HQ-ZIP NTEE proxy.

**Automated:** evaluation summaries, proposal intake (stdin / hybrid / optional API), pre-registration, OLS, decision logging. **Not automated:** unsupervised overnight 100-hypothesis crawls (out of scope).

Key scripts: `09_phase3_agentic_loop.py`, `10_acquire_soup_kitchens.py`, `11_merge_soup_kitchen_density.py`.

## Differentiator (for the report)

Prior art such as Google Co-Scientist (generate–debate–evolve) and DiscoveryBench (~25% best LLM systems) shows that open-ended discovery is hard. Our differentiator is the **pedagogical unrolled→rolled progression** plus reproducibility guarantees (pre-registration, decision logs, H4/H5 calibration)—not raw autonomy.

## Beyond Phase 3 (next student generation)

Ideas intentionally left for the next cohort:

1. **Multi-domain reuse** — port the same evaluate→propose→pre-register→run loop to another sociological frame (not only 990 fundraising efficiency).
2. **Closed-loop acquisition** — when the agent proposes an indicator that is not on the frame, spawn a bounded acquisition sub-workflow (API/MCP) and re-merge before OLS.
3. **Richer big-vs-local effectiveness** — go beyond density counts: service hours, meals distributed, appointment vs walk-in, and outcome proxies for ACFB partner agencies.
4. **Causal design upgrades** (only after Phase 3 pedagogy is solid) — year FE, EIN/ZIP clustering, panel structure—documented as Phase 2 limitations today.
5. **Human-in-the-loop review gates** — require explicit approval of proposed indicators that fail a cheap mechanical/identity filter before they enter OLS.

Document coverage and blockers honestly; a partial ACFB build with a clear workflow is preferable to a silent incomplete scrape.
