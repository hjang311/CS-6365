# Checkpoint 3 — Test Execution Plan (Phases 1 & 2)

Ordered, copy-pasteable steps to verify and ship the Phase 1 + Phase 2 deliverable.
Written for a human or an AI agent with **no additional context**. Run every step
from the **repository root** (the directory returned by `git rev-parse --show-toplevel`). Stop at the first hard
failure and report the step number plus the failing output.

**Precondition:** `Checkpoint 3/data/` contains the CSVs listed in
`Checkpoint 3/README.md` (§ Data inventory). If it does not, follow the README
fresh-clone acquisition section first (needs an exported `CENSUS_API_KEY`).

Steps 1–5 below validate **data-handoff reproducibility** when those source CSVs
are already present. They are not evidence that external-source acquisition works
until the fresh-clone path has also been run independently.

---

## Step 0 — Environment check

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "Checkpoint 3/requirements.txt"
.venv/bin/python --version
.venv/bin/python -c "import pandas, numpy, statsmodels; print('imports OK')"
```

**Accept:** Python ≥ 3.10 and `imports OK`.
**If it fails:** inspect the package-install error and retry Step 0 before continuing.

---

## Step 1 — Rebuild the modeling frame (activates the FDIC merge)

```bash
.venv/bin/python "Checkpoint 3/02_merge_pipeline.py"
```

**Accept (all of):**
- Log line `[Merge] Merged FDIC bank branches; density computed for N pre-clean rows` with N > 100,000
- Final line `[Merge] Saved final CP3 modeling frame with ~158,323 rows` (band: 140K–175K; small drift from upstream data is OK)
- No Python traceback

**Quick column check:**

```bash
.venv/bin/python -c "
import pandas as pd
cols = pd.read_csv('Checkpoint 3/data/cp3_modeling_frame.csv', nrows=0).columns
for c in ['bank_branches','bank_branch_density','log_bank_branch_density']:
    assert c in cols, f'MISSING: {c}'
print('FDIC columns present')"
```

**Accept:** `FDIC columns present`.
**If it fails:** confirm `Checkpoint 3/data/fdic_branches_by_zip.csv` exists (header: `ZIP5,bank_branches`); re-run.

---

## Step 2 — Frame data contracts

```bash
.venv/bin/python "Checkpoint 3/04_validate_frame.py"; echo "exit=$?"
```

**Accept:** every line starts `[PASS]`, final line `RESULT: all contracts PASSED`, `exit=0`.

Contracts checked: schema (incl. FDIC columns), row band 140K–175K, DV integrity
(no nulls, finite, non-negative, winsorized cap ≈ raw p99), ZHVI nulls in the
8K–16K band, bank_branch_density populated on >50% of rows, and H4/H5 smoke OLS
betas within 1e-3 of −7.91647 / +2.11963.

**If H4/H5 smoke fails but everything else passes:** the frame regeneration changed
the sample. Diff row counts vs Step 1 expectations before touching baselines —
do NOT edit the baseline constants without team sign-off.

---

## Step 3 — H4/H5 formal tables (fills the missing results files)

```bash
.venv/bin/python "Checkpoint 3/06_run_h4_h5_split.py"
```

**Accept:**
- `Checkpoint 3/H4/H4_results.md` and `Checkpoint 3/H5/H5_results.md` now exist
- Full-sample betas ≈ **H4: −7.91647** (n≈116,587), **H5: +2.11963** (n≈117,510) — matching the tables in `H4/H4_VERIFICATION_RUN.md` / `H5/H5_VERIFICATION_RUN.md`
- Mid/large split rows present for both hypotheses

---

## Step 4 — Phase 2 validation mode

```bash
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --validate; echo "exit=$?"
```

**Accept:** `H4: PASS  H5: PASS`, `exit=0`, and `loop_results_v2/validation_check.md`
regenerated with a provenance footer (timestamp + frame path + script version).

**Meaning of PASS:** β reproduction within 1e-3 — NOT theory confirmation
(H5's theory is rejected; that is expected and documented).

---

## Step 5 — Phase 2 full run

```bash
.venv/bin/python "Checkpoint 3/08_unrolled_loop.py" --run; echo "exit=$?"
```

This step regenerates `loop_results_v2/`. Before it is run, files from the
previous walkthrough may still use the older `filtered_scan` / “DV-Anchored
Filtered Scan” labels. The regenerated files should use
`limitation_harness` / “Bounded Two-Variable Limitation Harness.”

**Accept (all of):**
1. `exit=0` and final `Validation: H4=PASS  H5=PASS`
2. **H2_replay executes** (no longer skipped): a line like
   `[A] H2_replay: fundraising_efficiency_w ~ bank_branch_density` followed by
   `n=..., beta=..., p=...`. Expected direction is **negative**; record the actual
   β/p in the run notes. If β is positive or non-significant, that is a *finding*
   (frames differ from CP2), not a test failure — flag it for the report.
3. **The List B limitation harness has no level/log duplicates:** `loop_results_v2/list_b_pairs.json`
   contains `log_zhvi_2022` but NOT `zhvi_2022`; `log_nonprofit_branch_density`
   but NOT `nonprofit_branch_density`; `log_bank_branch_density` but NOT
   `bank_branch_density` or `bank_branches`. Expected IV list (7 pairs):
   `log_zhvi_2022`, `log_nonprofit_branch_density`, `log_bank_branch_density`,
   `social_service_count`, `population`, `total_revenue`, `total_expenses`.
4. **The limitation-harness outcome column** reads `exploratory (no prior)` — never
   `rejected (opposite or mismatch)` — for all B rows (check `list_b_results.md`).
5. All 8 artifacts regenerate under `loop_results_v2/` and each markdown file ends
   with a provenance footer; `batch_summary.csv` starts with a `#` provenance
   comment line (readable via `pandas.read_csv(..., comment='#')`).
6. `list_a_results.md` includes a "Rationale sources" section listing each List A row.

---

## Step 6 — Documentation spot-checks

```bash
if rg -n "loop_results/" \
  "Checkpoint 3/H4/H4_VERIFICATION_RUN.md" \
  "Checkpoint 3/H5/H5_VERIFICATION_RUN.md" \
  | rg -v "loop_results_v2|Artifacts \\(historical|kept for provenance"; then
  echo "FAIL: stale current-result reference found"
  exit 1
else
  echo "no stale current-result references"
fi
rg -n "PHASE2_UNROLLED_LOOP|README" "Checkpoint 3/LOOP_DOCUMENTATION.md" | head -3
```

**Accept:** first command prints `no stale current-result references` (any `loop_results/` mention
in H4/H5 docs sits in the explicitly historical section); second shows the
redirect to the Phase 2 guide. Also manually confirm `Checkpoint 3/README.md`
links resolve (PHASE2_UNROLLED_LOOP.md, TEST_EXECUTION_PLAN.md, H4/H5 docs).

---

## Step 7 — Ship (git)

Data CSVs are gitignored — only code + markdown ship. Note the repo already has
one unpushed commit (`44646b9`, the 07-loop work); this push delivers both.

```bash
git add "Checkpoint 3/README.md" "Checkpoint 3/requirements.txt" \
        "Checkpoint 3/TEST_EXECUTION_PLAN.md" "Checkpoint 3/PHASE2_UNROLLED_LOOP.md" \
        "Checkpoint 3/LOOP_DOCUMENTATION.md" \
        "Checkpoint 3/01_acquire_data.py" "Checkpoint 3/02_merge_pipeline.py" \
        "Checkpoint 3/03_hitl_hypothesis_engine.py" "Checkpoint 3/04_validate_frame.py" \
        "Checkpoint 3/08_unrolled_loop.py" \
        "Checkpoint 3/H4/" "Checkpoint 3/H5/" "Checkpoint 3/loop_results_v2/" \
        ".env.example"
git status   # verify: no CSVs staged, no .env staged
git commit -m "Ship Phase 1+2: FDIC merge, frame validator, unrolled loop v2.1, docs + test plan"
git push origin main
```

**Accept:** `git status` clean for staged intent (no data/secrets), push succeeds,
GitHub shows both commits.

---

## Acceptance summary (all must hold)

| # | Check | Value |
|---|-------|-------|
| 1 | Frame rebuilt with FDIC columns | ~158,323 rows; 3 new bank columns |
| 2 | `04_validate_frame.py` | exit 0, all `[PASS]` |
| 3 | `06` outputs exist | H4 β ≈ −7.91647, H5 β ≈ +2.11963 |
| 4 | `08 --validate` | exit 0, H4/H5 PASS |
| 5 | `08 --run` | exit 0; H2_replay ran; limitation harness deduped (7 pairs); provenance footers |
| 6 | Docs | no stale references; README links resolve |
| 7 | Git | code+md committed and pushed; no CSVs/.env |

## Known-good baseline values (do not edit without sign-off)

| Quantity | Value |
|----------|-------|
| H4 β (full) | −7.91647 (tol 1e-3) |
| H5 β (full) | +2.11963 (tol 1e-3) |
| Frame rows | 158,323 (band 140K–175K) |
| ZHVI null rows | ~12,227 (band 8K–16K) |
| H4 n / H5 n | 116,587 / 117,510 |
| CP2 H2 β (qualitative reference only) | ≈ −0.115 (different frame — never assert numerically) |
