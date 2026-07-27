# Archive & Cleanup Notes

This repo’s **curriculum path** is Manual (CP2/CP3) → Unrolled (CP3) → Rolled (CP4), with Checkpoint 0 as optional **prior-semester** context only. Historical semester clutter was cleaned so students are not dropped into nested submission clones, test-run dumps, or scratch data.

## What was cleaned up

The following items exist **locally only** (not on GitHub) under an `archive/` directory when present on a maintainer machine:

| Category | What | Why not on GitHub |
|----------|------|-------------------|
| `archive/submissions/` | Graded submission trees, zips, final PDFs | Multi-GB nested clones; no student value for the teaching path |
| `archive/cp0_prior_cohort/` | Prior-semester NORP package clones | Large git repos; curriculum pointer is `Checkpoint 0/` |
| `archive/cp1_iterations/` | Early CP1 test-run dumps | Superseded by final Broadband Access pipeline |
| `archive/cp3_loop_v1/` | Superseded `loop_results/` (v1 combinatorial era) | Use `Checkpoint 3/loop_results_v2/` for Phase 2 |
| `archive/scratch/` | Re-downloadable external scratch data | Not required to learn the loop |

**Recoverability:** these trees are **local-only** (gitignored). They are **not** required to run `Checkpoint 4/reproduce.sh` or to follow the curriculum. Do not expect them after `git clone`.

## Also local-only (never in archive/)

- **`Project Research & Initial Plan/`** — personal office-hour notes and planning drafts (gitignored)
- **`NORP_PROJECT.md`** — early SDK-era description (superseded by root `README.md` + `AGENTS.md`)
- **`CS6365_Checkpoint_Template.txt`** — raw course template
- **`Checkpoint 4/PRESENTATION_OUTLINE.md`** — team final-talk outline (gitignored; not student curriculum)

## Canonical vs provenance

- **Canonical Phase 3:** `Checkpoint 4/09_phase3_agentic_loop.py`, `enrichment_tools/`, `configs/`, `prompts/`
- **Canonical skills:** `.agent/skills/norp-*` (role contracts for hybrid IDE orchestration or SDK)
- **Provenance only:** `Checkpoint 4/Grok_4.5/` (earlier build trail; not the student entrypoint)
- **Legacy SDK factories:** `agentic_pipeline/` — early Antigravity SDK + CP1 triage demo; README explains the folder; **not** the Phase 3 entry (use `Checkpoint 4/prompts/` + skills + `09`)

## Superseded loop results

Phase 2 unrolled results graders should use are under `Checkpoint 3/loop_results_v2/`. Older `loop_results/` content lives under local `archive/cp3_loop_v1/` when archived.
