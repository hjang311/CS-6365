# Phase 2: Unrolled Deterministic Loop

Student guide for the July 10 OH direction: wrap Phase 1 manual hypothesis work in an **explicit list** executed by deterministic Python OLS. True agentic discovery is **Phase 3** (not built yet).

**Script:** [`08_unrolled_loop.py`](08_unrolled_loop.py)
**Outputs:** [`loop_results_v2/`](loop_results_v2/)
**Historical artifact:** [`07_deterministic_loop.py`](07_deterministic_loop.py) (combinatorial 215-pair batch — not the pedagogical unrolled loop)

---

## 1. What “unrolled loop” means here

In compilers, *loop unrolling* replaces a compact `for` with an explicit sequence of similar steps. The professor’s metaphor for this project:

| Phase | Who chooses the next test? | What runs |
|-------|----------------------------|-----------|
| **1 – Manual** | You | One hypothesis at a time (H2 pipeline, H4/H5 verification) |
| **2 – Unrolled** | You (list written *before* the run) | `for item in LIST: run_ols(item)` |
| **3 – Rolled / agentic** | The LLM, after seeing results | Propose new indicators, finer data, higher-order structure |

Phase 2 control flow is fixed in advance. The model may help *summarize* results; it does **not** append new `(IV, DV)` pairs mid-run.

---

## 2. List A and the bounded limitation harness

| | **List A — Curated hypothesis agenda** | **List B — Bounded two-variable limitation harness** |
|--|--------------------------------|----------------------------------------|
| Who builds it? | Team, from Phase 1 work | A short pre-registered filter rule |
| Each item is… | Named hypothesis + expected direction | `(IV, DV)` fixed **before OLS**, without a directional prior |
| Purpose | The actual small hypothesis list requested by the professor | Demonstrate why large-n two-variable significance is an inadequate discovery rule |
| Not this | Agent invents the next test | Full 215-pair combinatorial scan (`07 --batch`) |

Both lists use the **same** OLS recipe:

```text
DV ~ IV + log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income
```

Robust HC1 errors; fixed column subset + `dropna` (deterministic specialization — intentional for Phase 2).

**List A is the Phase 2 research agenda.** List B is not a second discovery
agenda and its significant rows are not counted as new hypotheses. H4, H5, and
population intentionally overlap List A as calibration cases: the same model
must produce the same result when reached through the bounded filter.

### List A contents

| ID | Role | Pair |
|----|------|------|
| H4 | confirmatory | `log_zhvi_2022` → `fundraising_efficiency_w` |
| H5 | confirmatory | `log_nonprofit_branch_density` → `fundraising_efficiency_w` |
| H2_replay | phase1_replay | `bank_branch_density` → `fundraising_efficiency_w` (**active** once the frame is rebuilt with the FDIC merge in `02_merge_pipeline.py`; skips gracefully on older frames). CP2's β ≈ −0.115 is a *qualitative* reference only — we assert direction, not the coefficient, because the frames differ (year FE, cleaning). |
| event_cost_drag | mechanical_control | `fundraising_events_direct_expenses` → `fundraising_efficiency_w` (denominator component; not a hypothesis) |
| affluence_clustering | exploratory | `log_zhvi_2022` → `log_nonprofit_branch_density` |
| identity_revenue_expenses | identity_control | `total_expenses` → `total_revenue` (labeled, not a discovery) |
| weak_population | weak_control | `population` → `fundraising_efficiency_w` |

### List B limitation-harness rule

1. Fix primary DV = `fundraising_efficiency_w`
2. Candidate numeric IVs excluding identifiers, formula controls, efficiency variants, **and mechanical DV components** (`total_contributions`, `fundraising_expense_proxy`, event expenses, professional fees — these enter the efficiency ratio by construction)
3. Apply accounting-identity blocklist
4. **De-duplicate level/log variants** via redundancy groups — only the log variant of ZHVI / nonprofit density / bank density enters (level duplicates add no information)
5. The `max_ivs=15` cap rarely binds — after all filters the current frame yields **7 IVs** (log ZHVI, log nonprofit density, log bank density, social_service_count, population, total_revenue, total_expenses). That small count is expected, not a bug
6. Write `list_b_pairs.json` **before** any OLS, then execute with the same deterministic `for` loop as List A

**Limitation argument:** Do **not** claim “2-var is limited” because few pairs are significant. At n ≈ 100k, p < 0.05 is cheap. Argue via mechanical hits, identity R², wrong-direction theory (H5), near-identical full-model R², pooled organization-years, and coarse temporal/spatial granularity — see `two_variable_limitation.md`. The R² comparison is descriptive, not an incremental-R² estimate, because no controls-only model is reported and IV-specific missingness changes the samples.
---

## 3. How to run

From the repo root (with the project venv):

```bash
# H4/H5 baseline check only
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --validate

# Full Phase 2: List A + bounded limitation harness + evaluation artifacts
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --run

# Optional: alternate frame / output directory (useful for test runs)
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --run --frame /path/to/frame.csv --out /tmp/results
```

Requires [`data/cp3_modeling_frame.csv`](data/cp3_modeling_frame.csv) (from `02_merge_pipeline.py`). The script guards its schema and exits with a clear message if the frame predates the current merge recipe.

### Outputs (`loop_results_v2/`)

| File | Contents |
|------|----------|
| `list_b_pairs.json` | Pre-registered limitation-harness pairs (written before OLS) |
| `list_a_results.md` | Curated hypothesis outcomes vs expected directions |
| `list_b_results.md` | Bounded limitation-harness results (not additional discoveries) |
| `batch_summary.csv` / `.md` | All rows combined |
| `validation_check.md` | H4/H5 β match within 1e−3 |
| `two_variable_limitation.md` | Evidence that 2-var OLS on this frame is limited |
| `poc_summary.md` | Templated summary (no per-pair stdin approvals) |

Latest validation: **H4 PASS**, **H5 PASS**.

> **What PASS means:** the loop **reproduced the baseline coefficients** (β within 1e−3 of −7.91647 / +2.11963). It is a *reproducibility* check, not a theory verdict — H5 passes validation while its competition theory is **rejected** (observed β is positive). Theory outcomes live in `list_a_results.md`.

---

## 4. How this differs from `07 --batch`

| | `07 --batch` | `08 --run` (Phase 2) |
|--|--------------|----------------------|
| Agenda | ~215 combinatorial pairs | Explicit List A + bounded limitation harness |
| Agent | Stdin prompt per significant hit (~155 approvals) | No per-pair approvals |
| Pedagogy | Search the space | Execute a known agenda |
| Identity pairs | Often included | Labeled controls on List A; blocked from the limitation harness |

Keep `07` as history. Prefer `08` for Checkpoint 3 Phase 2 deliverables and reproducibility demos (e.g. Carla).

---

## 5. Phase 1 → Phase 2 mapping

| Phase 1 manual work | Where it lived | Phase 2 wrap |
|---------------------|----------------|--------------|
| H2 bank-branch density | `Checkpoint 2/H2_Pipeline/` | List A `H2_replay` (active after the FDIC merge in `02_merge_pipeline.py`; skips on pre-merge frames) |
| H4 ZHVI housing cost | `Checkpoint 3/H4/` + `06_run_h4_h5_split.py` | List A `H4` + validation assert |
| H5 provider density | `Checkpoint 3/H5/` | List A `H5` + validation assert |
| Acquire / merge (NCCS, BMF, Census, Zillow) | `01_acquire_data.py`, `02_merge_pipeline.py` | Shared modeling frame for the loop |

---

## 6. Next: Phase 3 (not implemented)

After Phase 2 artifacts exist:

1. **Evaluate** which List A/B links held vs failed (`two_variable_limitation.md` is the starting evidence).
2. **Ask the LLM** what other socioeconomic indicators *could* be relevant and should be tested next.
3. **Stretch:** finer-granularity collection (e.g. soup-kitchen density by ZIP via an ACFB-style / MCP workflow) or higher-order (3+ variable) structure — because 990 + ACS ZIP granularity is coarse.

Phase 3 is when the loop is “rolled”: the agent helps rewrite the agenda. Do not confuse that with Phase 2’s fixed list.

---

## 7. Extending List A or the limitation harness

- **List A:** edit the `LIST_A` constant in `08_unrolled_loop.py` (add `id`, `iv`, `dv`, `expected_direction`, `role`).
- **List B limitation harness:** adjust `build_list_b()` exclusions / `preferred_order` / `max_ivs`; do not describe added rows as hypotheses unless they are first moved into List A with a pre-stated direction and rationale.
- Re-run `--run`. Do not add pairs inside the OLS loop at runtime — that would be Phase 3 behavior.
