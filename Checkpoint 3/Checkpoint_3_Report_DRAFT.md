# Georgia Institute of Technology
## CS 4365/6365: Introduction to Enterprise Computing
### Summer 2026
**Project Checkpoint 3 Report**

**Group:** 1 / G5  
**Name(s):** Hwando Jang & Carla du Plessis  
**Project Name:** NORP Agentic Data Exploration Pipeline  

> Paste sections below into `Team_1_CS6365_Checkpoint_3.docx` (OneDrive).  
> Research questions use **RQ1–RQ5** (formerly H1–H5). Keep citations from the existing Word doc References section.

---

## Context and Related Work / Project Plan (Plan)

Nonprofit organizations publish high volumes of operational and financial data—primarily IRS Form 990 filings, sector surveys, and linked socioeconomic datasets. Extracting meaningful relationships from these sources is labor-intensive, so our project builds an agentic data-exploration layer that can formulate research questions, merge multi-source frames, and run auditable statistical tests. The work builds on prior NORP research and on Ma et al. (2023) InsightPilot, which restricts LLM exploration to named, auditable operations rather than free-form analysis.

**Starting point (end of Checkpoint 2).** We had a national modeling frame (~147K organization-years) joining NCCS CORE 990 (2018–2022), IRS BMF, FDIC BankFind, and Census ACS5. **RQ2** (bank-branch density → fundraising efficiency) was confirmed as a small but reliable negative signal after DV cleaning and log-log OLS. **RQ3** (direct payment-processing fees) remained a feasibility probe only (~5.5% itemization in e-file XML). CP2 feedback endorsed the three-agent separation (deterministic stats vs. LLM framing) and asked us to stabilize confirmatory results before diffusing into 20–30 exploratory tests. An AI-suggestions branch also offered quantile regression / year fixed-effects scripts as a robustness starting point.

**Checkpoint 3 direction (July office hours).** Rather than only running the AI-suggested quantile/FE robustness path, we followed the course’s pedagogical model:

| Phase | Who chooses the next test? | Checkpoint 3 status |
|-------|----------------------------|---------------------|
| **1 — Manual** | Humans | Done — Zillow + provider-density frame; RQ4/RQ5 hand tests |
| **2 — Unrolled loop** | Humans (list written *before* the run) | Done — `08_unrolled_loop.py` List A + List B |
| **3 — Rolled / agentic** | LLM after seeing results | Intentionally deferred to Checkpoint 4 |

**Research questions (RQ1–RQ5):**

| ID | Statement | Status |
|----|-----------|--------|
| **RQ1** | Do nonprofits in low-broadband communities have worse fundraising efficiency? (Census B28002 × 990) | Null in CP1; retained as reportable baseline / reusable pipeline case |
| **RQ2** | Among nonprofits with revenue ≥ $500K, lower ZIP bank-branch density is associated with higher fundraising efficiency (fintech-substitution proxy) | Confirmed in CP2; replayed and reconfirmed in CP3 Phase 2 |
| **RQ3** | Higher payment-processing fee share (direct fintech measure) is associated with higher fundraising efficiency, especially for mid-size orgs | Feasibility only (CP2); not a completed confirmatory result |
| **RQ4** | Higher local real-estate prices (Zillow ZHVI) are associated with lower fundraising efficiency (spatial cost / overhead pressure) | **Confirmed** (β ≈ −7.92, p ≪ 0.001) |
| **RQ5** | Higher local density of mission-critical social-service providers is associated with *lower* fundraising efficiency (competition for donors) | **Rejected** — significant *positive* association (agglomeration reading) |

**Data spine for CP3.** Same federal sources as CP2, plus Zillow ZHVI (exact `2022-12-31` snapshot) and a BMF-derived social-service provider count (NTEE K30/K31/K35/L40/L41/P43) normalized per 10,000 residents. Shared OLS recipe: `DV ~ IV + log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income` with HC1 robust errors; DV = winsorized fundraising efficiency.

---

## Project Deliverables

| Deliverable | Description | Technical Stack |
| :--- | :--- | :--- |
| **CP3 modeling frame** | National org-year frame (~158K cleaned rows) with ZHVI, bank density, and nonprofit provider density | Python, Pandas; NCCS, IRS BMF, FDIC, Census ACS5, Zillow |
| **Phase 1 manual pipeline** | Acquire → merge → validate → RQ4/RQ5 size-split OLS | `01_acquire_data.py`, `02_merge_pipeline.py`, `04_validate_frame.py`, `06_run_h4_h5_split.py` |
| **RQ4 / RQ5 verification write-ups** | Formal hypothesis docs with mid/large splits and theory outcomes | `Checkpoint 3/H4/`, `Checkpoint 3/H5/` |
| **Phase 2 unrolled loop** | Pre-registered List A (theory-first) + List B (bounded 2-var limitation harness); H4/H5 β calibration | `08_unrolled_loop.py`, `loop_results_v2/` |
| **Limitation evaluation** | Evidence that large-n 2-var significance alone is not a finished research result | `loop_results_v2/two_variable_limitation.md` |
| **Reproduction docs** | Student-facing Phase 1/2 guides + ordered test plan | `PHASE1_MANUAL_PIPELINE.md`, `PHASE2_UNROLLED_LOOP.md`, `TEST_EXECUTION_PLAN.md`, `README.md` |
| **3-agent skills (carry-forward)** | Orchestrator / Code / Validator skills from earlier checkpoints | `.agent/skills/`, Antigravity |
| **Final presentation (semester end)** | Slide deck synthesizing pipeline discoveries | PowerPoint (Checkpoint 4) |

---

## Project Milestones

| Checkpoint | Milestone | Technical Scope & Deliverables | Work Split | Status |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Baseline & Gold Standard | Hybrid skills; broadband RQ1; survey-weight fix | Hwando & Carla | **Complete** |
| **2** | National frame & RQ2/RQ3 | 4-source H2 pipeline; significant RQ2; RQ3 feasibility (XML + web probe) | Hwando: pipeline, transforms, plots. Carla: hypothesis framing, cleaning recipe, analysis | **Complete** |
| **3** | Phase 1 + Phase 2 | Manual RQ4/RQ5; Zillow merge; unrolled deterministic loop; 2-var limitation note; reproduction docs | Hwando: merge/validate/loop architecture, List A/B design, docs. Carla: RQ4/RQ5 specification & verification runs, size splits, interpretation | **Complete** |
| **4** | Phase 3 (rolled) + final | Agent evaluate→propose→pre-register→run; finer-granularity data (e.g. soup-kitchen / ACFB density); higher-order specs; final presentation | Hwando: agentic loop & acquisition workflows. Carla: interpretation, plots, presentation narrative | **In progress / next** |

---

## Current Progress Report (Match)

### Work done over the last ~2 weeks (Checkpoint 3)

**1. Phase 1 — Manual extension of the national frame (RQ4 & RQ5)**  
We extended the CP2 spine with Zillow ZHVI and BMF-based social-service provider density, rebuilt `cp3_modeling_frame.csv`, and enforced data contracts via `04_validate_frame.py`.

**RQ4 (housing cost → efficiency) — confirmed**

| Sample | n | β (`log_zhvi_2022`) | p-value | 95% CI | R² |
|--------|---|---------------------|---------|--------|-----|
| Full (≥$500K) | 116,587 | −7.916 | 2.4×10⁻²² | [−9.51, −6.32] | 0.177 |
| Mid ($500K–$2M) | 53,650 | −2.995 | 3.6×10⁻¹¹ | [−3.88, −2.11] | 0.091 |
| Large (≥$2M) | 62,936 | −11.534 | 2.4×10⁻¹⁶ | [−14.29, −8.78] | 0.099 |

**RQ5 (provider density → efficiency) — theory rejected (informative sign flip)**

| Sample | n | β (`log` density) | p-value | 95% CI | R² |
|--------|---|-------------------|---------|--------|-----|
| Full (≥$500K) | 117,510 | +2.120 | 0.0024 | [0.75, 3.49] | 0.176 |
| Mid ($500K–$2M) | 53,972 | +1.107 | 0.0047 | [0.34, 1.88] | 0.090 |
| Large (≥$2M) | 63,537 | +3.056 | 0.0091 | [0.76, 5.35] | 0.097 |

Cross-RQ finding: effects are larger for ≥$2M organizations than for mid-size orgs—opposite our initial “small orgs are more sensitive” intuition.

**2. Phase 2 — Unrolled deterministic loop**  
We replaced an earlier combinatorial scanner (`07`, ~215 pairs / ~155 HITL approvals) with `08_unrolled_loop.py`: an explicit List A (theory-first agenda + labeled controls) and List B (bounded limitation harness with pairs written to JSON *before* OLS). Validation reproduced RQ4/RQ5 baselines within 1e−3 (**PASS**). List A outcomes: RQ4 confirmed; RQ5 rejected (wrong direction); RQ2 replay confirmed (β ≈ −0.116); mechanical/identity controls correctly labeled, not claimed as discoveries.

**3. Two-variable limitation evaluation**  
List B executed 7 non-mechanical IV candidates; 6 were p < 0.05, but full-model R² stayed essentially flat (~0.1756–0.1766). Combined with mechanical hits and RQ5’s wrong-direction significance, this shows large-n 2-var scanners are easy to “light up” and hard to trust as finished research—motivating Phase 3 (new indicators, higher-order structure, finer-granularity data).

### Comparison to the CP2 milestone chart

| CP2 plan for Checkpoint 3 | What we delivered | Notes |
|---------------------------|-------------------|--------|
| Quantile regression at median | Not primary deliverable | Available as AI-suggestions starter (`06_robustness_quantile_fe.py` on `ai-suggestions/cp3`); deprioritized after July OH pedagogy |
| Year fixed-effects models | Not primary deliverable | Same as above; panel year FE remains a documented Phase 2 limitation / CP4 option |
| Strict Census-null culling | Done as part of merge/validate | Frame contracts + listwise deletion for ZHVI (~12K fewer rows on RQ4) |
| AI-driven 20–30 hypothesis exploration | Partial / redirected | Built **unrolled** multi-hypothesis execution (List A/B) rather than unsupervised overnight crawl; true agentic proposal loop deferred to Phase 3 |
| Nonprofit branch density / social services | Done as **RQ5** | Competition hypothesis rejected; agglomeration interpretation |

### Planned work for the next 2 weeks (Checkpoint 4 / Phase 3)

1. **Rolled agentic loop:** evaluate Phase 2 outcomes → LLM proposes indicators → pre-register → deterministic OLS verify (decision log).  
2. **Higher-order correlations:** 3+ variable / interaction specs (e.g. ZHVI × density).  
3. **Finer-granularity data:** soup-kitchen / food-pantry density (Atlanta Community Food Bank / licensed Feed America proxy) vs. coarse IRS HQ-ZIP NTEE counts.  
4. Begin final presentation narrative (confirmed vs. rejected RQs; limitation → Phase 3 arc).

### Changes to the original plan (past 2 weeks)

- **Pedagogy over pure robustness scripts:** CP2 feedback’s quantile/FE AI branch was treated as optional inspiration; July OH guidance made **manual → unrolled → rolled** the main CP3/CP4 spine.  
- **From “20–30 autonomous discoveries” to pre-registered agendas:** Phase 2 deliberately prevents the LLM from inventing pairs mid-run; credibility comes from verification and limitation analysis.  
- **RQ5 outcome changed the research story:** competition → agglomeration; reporting disconfirmation is now a first-class pipeline goal.  
- **Phase 3 not claimed as CP3 complete:** agentic proposal loop and soup-kitchen acquisition are next-checkpoint work (local scaffolding exists under `Checkpoint 4/`, not required for CP3 credit).

---

## Supporting Evidence (Factual)

**GitHub repository:** https://github.com/hjang311/CS-6365  

### Checkpoint 3 — past two weeks (primary)

| Claim | Link / path |
|-------|-------------|
| Phase 1+2 index & reproduction | https://github.com/hjang311/CS-6365/tree/main/Checkpoint%203 |
| Acquire / merge / validate / RQ4–RQ5 split | [`01_acquire_data.py`](https://github.com/hjang311/CS-6365/blob/main/Checkpoint%203/01_acquire_data.py), [`02_merge_pipeline.py`](https://github.com/hjang311/CS-6365/blob/main/Checkpoint%203/02_merge_pipeline.py), [`04_validate_frame.py`](https://github.com/hjang311/CS-6365/blob/main/Checkpoint%203/04_validate_frame.py), [`06_run_h4_h5_split.py`](https://github.com/hjang311/CS-6365/blob/main/Checkpoint%203/06_run_h4_h5_split.py) |
| Unrolled loop (Phase 2) | [`08_unrolled_loop.py`](https://github.com/hjang311/CS-6365/blob/main/Checkpoint%203/08_unrolled_loop.py) |
| List A / List B / limitation / validation | https://github.com/hjang311/CS-6365/tree/main/Checkpoint%203/loop_results_v2 |
| RQ4 write-up + table | https://github.com/hjang311/CS-6365/tree/main/Checkpoint%203/H4 |
| RQ5 write-up + table | https://github.com/hjang311/CS-6365/tree/main/Checkpoint%203/H5 |
| Phase docs | [`PHASE1_MANUAL_PIPELINE.md`](https://github.com/hjang311/CS-6365/blob/main/Checkpoint%203/PHASE1_MANUAL_PIPELINE.md), [`PHASE2_UNROLLED_LOOP.md`](https://github.com/hjang311/CS-6365/blob/main/Checkpoint%203/PHASE2_UNROLLED_LOOP.md) |

### Sample execution results (from `loop_results_v2/`)

- Validation: H4 PASS (β = −7.91647), H5 PASS (β = +2.11963) — *reproduction*, not theory verdict for RQ5.  
- List A: RQ4 confirmed; RQ5 rejected (positive); RQ2 replay confirmed.  
- List B: 7 IVs executed, 6 significant at p < 0.05, R² span ≈ 0.001 — see `two_variable_limitation.md`.

### Carry-forward (Checkpoint 2, still relevant)

| Artifact | Path |
|----------|------|
| RQ2 pipeline & plots | https://github.com/hjang311/CS-6365/tree/main/Checkpoint%202/H2_Pipeline |
| RQ3 feasibility | https://github.com/hjang311/CS-6365/tree/main/Checkpoint%202/H3_Testing |

### Optional: CP2 feedback AI starter (not our primary CP3 deliverable)

- Feedback zip branch note: `ai-suggestions/cp3` includes `Checkpoint 2/H2_Pipeline/06_robustness_quantile_fe.py` (quantile + year FE starter). We reviewed it and prioritized the Phase 1/2 pedagogy instead.

**Screenshots / tables to embed in Word:** paste the RQ4 and RQ5 result tables above; optionally screenshot `list_a_results.md` and `validation_check.md` from GitHub or local `loop_results_v2/`.

---

## Skill Learning Report

- **Pre-registration & unrolled loops:** Learned to write hypothesis lists *before* OLS (`list_b_pairs.json`) so the pipeline cannot silently invent “discoveries,” separating execution automation from agenda control.  
- **Multi-source ZIP merge with hard snapshot discipline:** Integrated Zillow ZHVI with an exact date fail-closed download so H4 cannot silently drift if the snapshot changes.  
- **Interpreting disconfirmation:** Practiced reporting RQ5’s significant wrong-direction result as agglomeration evidence rather than forcing the original competition story.  
- **Limitation evaluation vs. significance counting:** Documented why p < 0.05 at n ≈ 100k is cheap (mechanical IVs, flat R², tiny population β) and why that motivates Phase 3.  
- **Reproducibility engineering for peers:** Wrote ordered test plans and dual reproduction modes (data handoff vs. fresh acquire) so another student (e.g. Carla) can rebuild Phase 1/2 without tribal knowledge.  
- **Pedagogical agent design:** Clarified that credible agentic discovery is “agent proposes, Python verifies,” not unsupervised combinatorial scanning with LLM narration (`07` → `08` redesign).

---

## Self-Evaluation

1. **Plan:** 110/120 — Clear starting point from CP2, explicit Phase 1→2→3 plan aligned with July OH guidance, and honest deferral of Phase 3. Minor deduction: early CP3 still carried “20–30 autonomous hypotheses” language before the unrolled-loop redesign.  
2. **Match:** 115/120 — Delivered the manual RQ4/RQ5 frame, size splits, unrolled loop, β calibration, and limitation write-up matching the revised plan. Deduction: CP2-listed quantile/FE robustness was not completed as a primary artifact.  
3. **Factual:** 95/100 — GitHub paths, exact β/p/CI/n tables, and `loop_results_v2/` artifacts match the claims. Deduction: modeling CSVs are gitignored (expected); reviewers need the linked markdown results / local data handoff for full re-run.

---

## LLM Feedback

*(Run your preferred LLM on the filled report, then paste scores here.)*

1. **Project Plan (Plan):** _/120  
2. **Progress Report (Match):** _/120  
3. **Supporting Evidence (Factual):** _/100  

### Actionable Suggestions

*(Replace after LLM review; starter suggestions based on current state:)*

1. Embed RQ4/RQ5 tables and at least one `loop_results_v2` screenshot natively in the Word doc (do not rely only on GitHub links).  
2. Keep Phase 3 / Checkpoint 4 work clearly labeled as **next**, even if local scaffolding already exists—avoid claiming rolled-loop credit in CP3.  
3. In CP4, prioritize one finer-granularity indicator (food assistance density) plus one higher-order interaction rather than another large 2-var scan.  
4. If time allows, adapt the AI-suggestions quantile/FE script as a short robustness appendix for RQ2/RQ4—not as a substitute for Phase 3.  
5. Adopt the true Part IX fundraising-expense field when available (CP2 feedback) to strengthen the DV beyond the current proxy denominator.

---

## Quick paste checklist for the Word doc

- [ ] Update project title to **NORP Agentic Data Exploration Pipeline** (or keep FinTech subtitle as secondary).  
- [ ] Replace incomplete “H4: / H5:” stubs with full RQ4/RQ5 statements.  
- [ ] Replace Deliverables + Milestones tables with the versions above.  
- [ ] Replace Progress Report Week 1–2 CP2 narrative with CP3 Phase 1/2 work (keep a short “carried from CP2” paragraph only).  
- [ ] Replace Supporting Evidence links with Checkpoint 3 GitHub paths.  
- [ ] Update Skill / Self-Eval / leave LLM Feedback blank until reviewed.  
- [ ] Remove instructional lines (“Add the deliverables…”, “remove this line”, etc.).
