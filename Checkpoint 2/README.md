# Checkpoint 2 — Manual H2 Pipeline (Phase 1 Start)

Manual hypothesis pipeline testing **bank-branch density** as a proxy for fintech adoption and its effect on nonprofit fundraising efficiency (**RQ2 / H2**).

## Hypothesis (H2 / RQ2)

Among nonprofits with annual revenue ≥ **$500K**, **lower bank-branch density per ZIP** (proxy for greater fintech adoption) is associated with **higher fundraising efficiency**, with a stronger effect in smaller nonprofits.

## Headline numbers

| Metric | Value |
|--------|-------|
| OLS β on IV (Model 2) | **−0.11453** (95% CI −0.186, −0.043) |
| p-value | **0.001667** |
| Mid-size β | −0.08145, p ≈ 1.3e-4 |
| Large β | −0.15211, p ≈ 0.0047 |

Source: [`H2_Pipeline/findings_results.md`](H2_Pipeline/findings_results.md). Replay also appears in CP3 List A / [`Checkpoint 3/RQ2/RQ2_VERIFICATION_RUN.md`](../Checkpoint%203/RQ2/RQ2_VERIFICATION_RUN.md).

## Contents

| Item | Description |
|------|-------------|
| [`H2_Pipeline/`](H2_Pipeline/) | Full manual pipeline: acquire → merge → analyze → validate |
| [`H3_Testing/`](H3_Testing/) | Fintech measure **feasibility** probes (RQ3 — not confirmatory; skip for the main teaching path) |
| [`Checkpoint_2_Report.md`](Checkpoint_2_Report.md) | Checkpoint 2 report |

> **Local-only note:** Draft `*.pdf` files (including `*NeedsEditing*`) may appear on maintainer machines; they are gitignored and not part of the curriculum. Prefer the markdown report.

## Run order

From repo root (recommended) or `cd H2_Pipeline`:

```bash
cd "Checkpoint 2/H2_Pipeline"
pip install -r requirements.txt   # or use repo .venv
export CENSUS_API_KEY=your_key    # required for ACS; script does not auto-load .env
python 01_acquire_data.py --years 2018 2019 2020 2021 2022
python 02_merge_pipeline.py
python 03_analysis.py
```

**Data note:** `Checkpoint 2/H2_Pipeline/data/` is **gitignored**. First acquire downloads multi-year NCCS CORE + BMF + FDIC + ACS — expect nontrivial disk and runtime (tens of minutes to hours depending on network).

See [`H2_Pipeline/README.md`](H2_Pipeline/README.md) for sources, join keys, and known limitations (DV proxy, bank-density as fintech proxy).

## Expected outputs

- Modeling frame under `H2_Pipeline/data/`
- Analysis tables / plots referenced from `findings_results.md`
- β on `log_bank_branch_density` (or pipeline IV name) matching the table above within rounding

## Curriculum context

This is the **first Manual (Phase 1) hypothesis pipeline**. H4/H5 in Checkpoint 3 each required further manual specialization. See [`docs/CURRICULUM.md`](../docs/CURRICULUM.md) and [`Checkpoint 3/docs/PHASE1_MANUAL_PIPELINE.md`](../Checkpoint%203/docs/PHASE1_MANUAL_PIPELINE.md).
