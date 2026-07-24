# Hybrid Prompt Live Test Report (Grok 4.5)

**Date:** 2026-07-12  
**Method:** Cursor Task subagent (`generalPurpose`) executing [`prompts/PHASE3_HYBRID_PROMPT.md`](prompts/PHASE3_HYBRID_PROMPT.md)  
**Subagent:** [hybrid round](b5ac2df6-fbf1-4e7b-a372-d41e4ef98721)

## Verdict: PASS

The hybrid path works in Cursor the same way it is designed for Antigravity: the IDE agent writes pre-registered proposals, invokes deterministic `09 --run`, then writes an interpretation — **without computing OLS itself**.

## Checklist

| Check | Result |
|-------|--------|
| `evaluation_summary.md` present / used | PASS |
| `proposals_round1_hybrid.json` written before OLS | PASS (`source: hybrid`) |
| ≥1 interaction proposal | PASS (H04) |
| No mechanical DV-component IVs | PASS |
| No lone control-as-IV | PASS |
| `09 --run` exit 0 | PASS |
| Interpretation cites only runner coefficients | PASS |
| Decision log updated | PASS |

## Hybrid vs fixture (brief)

| | Fixture round 1 | Hybrid round |
|--|-----------------|--------------|
| Source | `fixture` | `hybrid` |
| Specs | P01 bank, P02 poverty×density, P03 population | H01 ZHVI, H02 bank, H03 density, H04 ZHVI×density, H05 social_service_count |
| Confirmed | P01 | H01, H02 |
| Rejected / wrong-sign | — | H03 (H5 theory still fails) |
| Interaction | n.s. (poverty×density) | n.s. (ZHVI×density, p≈0.59) |

Hybrid independently rediscovered Phase 2 anchors (H4/H2) and again rejected the H5 competition story — evidence the prompt steers a useful agenda without API keys.

## Artifacts

- `phase3_results/proposals_round1_hybrid.json`
- `phase3_results/round_hybrid_results.md` (+ `.csv` / `.json`)
- `phase3_results/round_hybrid_interpretation.md`
- `phase3_results/decision_log.jsonl`

## Round 2 suggestion (from hybrid interpretation)

Lead with finer-granularity `soup_kitchen_density` / Feed America–scaled food-assistance density after the stretch merge.
