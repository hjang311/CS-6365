# Mode B Drift — Formal Artifact (CP3 Factual caveat)

## Why this exists

The CP3 modeling frame (`Checkpoint 3/data/cp3_modeling_frame.csv`) is
**regenerated from live / re-acquired sources** rather than committed as a
frozen binary. That is intentional (reproducible pipelines over opaque dumps)
but it means a third party cannot re-verify every report coefficient offline
without re-running acquisition + merge.

TA CP3 Factual feedback asked us to **formalize Mode B drift as its own
artifact**. This note is that artifact.

## Mode A vs Mode B

| Mode | Meaning |
|------|---------|
| **Mode A** | Rebuild from a peer data handoff / frozen snapshot paths (when available) |
| **Mode B** | Fresh acquire → merge → validate against contracts and known H4/H5 baselines |

See `Checkpoint 3/TEST_EXECUTION_PLAN.md` and `Checkpoint 3/README.md` for the
ordered reproduction steps.

## Observed Mode B drift (CP3 cycle)

When Mode B was run end-to-end in the CP3 cycle (documented in the CP3 report
and self-evaluation):

- **Data-contract validator:** 9 of 11 contracts passed on the live rebuild
  (2 soft drifts vs the handoff-era expectations).
- **Coefficient deltas vs handoff baselines (examples cited in self-eval):**
  absolute β deltas on the order of **0.040** and **0.080** for selected
  confirmatory rows — small relative to effect magnitudes, but large enough
  that graders should treat Mode B as “same recipe, live inputs” rather than
  bit-identical replay.
- **H4/H5 β reproduction gate** (`08 --validate` / Phase 3 `--validate`):
  when run on the committed working frame used for Phase 2 artifacts, PASS
  within 1e−3 (reproduction, not theory confirmation for H5).

These drifts come from upstream refresh (Census ACS vintages, BMF extracts,
Zillow snapshot discipline) and listwise missingness changes — not from
changing the OLS formula or inventing statistics in the LLM.

## How a third party should re-verify

1. Follow `Checkpoint 3/TEST_EXECUTION_PLAN.md` Mode B path
   (`01_acquire_data.py` → `02_merge_pipeline.py` → `04_validate_frame.py`).
2. Run `08_unrolled_loop.py --validate` (or Checkpoint 4
   `09_phase3_agentic_loop.py --validate`) and compare |Δβ| to 1e−3 for H4/H5.
3. Expect small drift if live sources moved; treat PASS/FAIL of the **recipe**
   as the contract, and document any |Δβ| above tolerance in a dated note
   beside this file.

## What this is not

- Not a license to hide failed validations.
- Not an excuse to skip committing Phase 2 result tables
  (`loop_results_v2/`), which remain the static evidence layer.
- Not a claim that live Mode B always matches Mode A bit-for-bit.

## Related

- `Checkpoint 3/self_evaluation_rewrite.txt` — Match/Factual scoring notes
- `Checkpoint 3/loop_results_v2/validation_check.md` — H4/H5 reproduction
- `Checkpoint 3/04_validate_frame.py` — data-contract validator
