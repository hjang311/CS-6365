# Archive layout

This repo’s **curriculum path** is `Checkpoint 0` → `Checkpoint 4`. Historical
semester clutter was moved under `archive/` so students are not dropped into
nested submission clones or scratch data.

## What lives where

| Location | Purpose | On GitHub? |
|----------|---------|------------|
| `archive/submissions/` | Graded submission trees (`616954-*`), zips, final PDFs | **No** (gitignored bulky contents; folder may exist locally) |
| `archive/cp0_exemplars/` | Spring NORP exemplar clones used for CP0 | **No** (gitignored) |
| `archive/cp1_iterations/` | Early CP1 test-run dumps | **No** (gitignored) |
| `archive/cp3_loop_v1/` | Superseded `loop_results/` (v1 combinatorial era) | **No** (gitignored); use `Checkpoint 3/loop_results_v2/` |
| `archive/scratch/` | `Data for Tests`, `dataverse_files` | **No** (gitignored) |

## Intentionally local (never archived for push)

**`Project Research & Initial Plan/`** — personal office-hour notes and planning
drafts. Covered by `.gitignore`. Do not commit or push.

## Canonical vs provenance

- **Canonical Phase 3:** `Checkpoint 4/09_phase3_agentic_loop.py`, `enrichment_tools/`, `configs/`
- **Provenance only:** `Checkpoint 4/Grok_4.5/` (earlier build trail; not the student entrypoint)
- **Legacy SDK factories:** `agentic_pipeline/` (see its README); skills live in `.agent/skills/`

## Superseded loop results

Phase 2 unrolled results that graders should use are under
`Checkpoint 3/loop_results_v2/`. The older `loop_results/` tree was moved to
`archive/cp3_loop_v1/` when present.
