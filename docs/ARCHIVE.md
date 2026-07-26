# Archive & Cleanup Notes

This repo's **curriculum path** is `Checkpoint 0` → `Checkpoint 4`. Historical
semester clutter was cleaned up so students are not dropped into nested
submission clones, test-run dumps, or scratch data.

## What was cleaned up

The following items exist **locally only** (not on GitHub) in an `archive/` directory:

| Category | What | Why not on GitHub |
|----------|------|-------------------|
| `archive/submissions/` | Graded submission trees (`616954-*`), zips, final PDFs | Multi-GB nested clones; no student value |
| `archive/cp0_exemplars/` | NORP Spring 2026 exemplar clones (Group 5) | Large git repos; curriculum report is in `Checkpoint 0/` |
| `archive/cp1_iterations/` | Early CP1 test-run dumps (Test 1, Test 2, Test 3) | Superseded by final `Broadband Access` pipeline |
| `archive/cp3_loop_v1/` | Superseded `loop_results/` (v1 combinatorial 215-pair era) | Use `Checkpoint 3/loop_results_v2/` for Phase 2 results |
| `archive/scratch/` | `Data for Tests/`, `dataverse_files/` | Re-downloadable external data |

## Also local-only (never in archive/)

- **`Project Research & Initial Plan/`** — personal office-hour notes and planning drafts. Covered by `.gitignore`. Never commit.
- **`NORP_PROJECT.md`** — early SDK-era project description (superseded by root `README.md`)
- **`CS6365_Checkpoint_Template.txt`** — raw course template

## Canonical vs provenance

- **Canonical Phase 3:** `Checkpoint 4/09_phase3_agentic_loop.py`, `enrichment_tools/`, `configs/`
- **Provenance only:** `Checkpoint 4/Grok_4.5/` (earlier build trail; not the student entrypoint)
- **Legacy SDK factories:** `agentic_pipeline/` (see its README); skills live in `.agent/skills/`

## Superseded loop results

Phase 2 unrolled results that graders should use are under
`Checkpoint 3/loop_results_v2/`. The older `loop_results/` tree was moved to
`archive/cp3_loop_v1/` (local only).
