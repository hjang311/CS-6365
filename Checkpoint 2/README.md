# Checkpoint 2 — Manual H2 Pipeline (Phase 1 Start)

Manual hypothesis pipeline testing bank-branch density as a proxy for fintech adoption and its effect on nonprofit fundraising efficiency.

## Hypothesis (H2)

Among nonprofits with annual revenue ≥ $500K, **lower bank-branch density per ZIP** (proxy for greater fintech adoption) is associated with **higher fundraising efficiency**, with a stronger effect in smaller nonprofits.

## Contents

| Item | Description |
|------|-------------|
| [`H2_Pipeline/`](H2_Pipeline/) | Full manual pipeline: acquire → merge → analyze → validate |
| [`H3_Testing/`](H3_Testing/) | Fintech measure feasibility probes (exploratory) |
| [`Checkpoint_2_Report.md`](Checkpoint_2_Report.md) | Checkpoint 2 report |

## Run order

```bash
cd H2_Pipeline
pip install -r requirements.txt
export CENSUS_API_KEY=your_key
python 01_acquire_data.py --years 2018 2019 2020 2021 2022
python 02_merge_pipeline.py
python 03_analysis.py
```

See [`H2_Pipeline/README.md`](H2_Pipeline/README.md) for detailed data source and limitations documentation.

## Context in this project

This is the **first Manual (Phase 1) hypothesis pipeline**. Each hypothesis (H2, then H4, then H5 in Checkpoint 3) required manual pipeline specialization. See [`docs/CURRICULUM.md`](../docs/CURRICULUM.md) and [`Checkpoint 3/PHASE1_MANUAL_PIPELINE.md`](../Checkpoint%203/PHASE1_MANUAL_PIPELINE.md).
