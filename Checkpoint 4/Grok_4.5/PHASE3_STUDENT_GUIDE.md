# Phase 3 Student Guide — Rolled Agentic Loop

**Build:** `Checkpoint 4/Grok_4.5/` (Grok 4.5)  
**Prerequisite:** Checkpoint 3 Phase 2 artifacts (`loop_results_v2/`) and `data/cp3_modeling_frame.csv`.

## Mental model

```
Phase 2 results  →  evaluate (deterministic)
                 →  propose  (LLM / human / fixture)
                 →  pre-register JSON
                 →  run OLS  (deterministic; shared 08 recipe)
                 →  interpret (LLM / human / fixture)
                 →  (optional next round, bounded)
```

The agent **never** edits the proposal list after OLS starts for that round.

## Modes of `09_phase3_agentic_loop.py`

| Flag | What it does |
|------|----------------|
| `--validate` | Replay H4 & H5; assert β within 1e-3 of Phase 1 baselines |
| `--evaluate` | Write `phase3_results/evaluation_summary.md` (+ `.json`) from CP3 List A/B |
| `--propose` | Collect proposals; write `proposals_round{N}.json` **before** any OLS |
| `--run` | Execute pre-registered proposals (2-var and interaction) |
| `--interpret` | Compare results to expectations; append `decision_log.jsonl` |
| `--all` | Convenience: evaluate → propose → run → interpret for `--rounds` (default 2) |
| `--fixture` | Offline proposals/interpretations (no stdin, no API) for reproduction |
| `--api` | Optional Gemini (`GEMINI_API_KEY` in `.env`) |
| `--proposals PATH` | Point `--run` / `--interpret` at a specific proposals file |
| `--frame PATH` | Alternate modeling frame (default: CP3 `cp3_modeling_frame.csv`) |
| `--out DIR` | Alternate output directory (default: `phase3_results/`) |

## Proposal JSON schema

```json
{
  "provenance": {
    "built_by": "Grok_4.5",
    "round": 1,
    "generated_at": "..."
  },
  "proposals": [
    {
      "id": "P01",
      "spec_type": "two_var",
      "iv": "log_bank_branch_density",
      "dv": "fundraising_efficiency_w",
      "expected_direction": "negative",
      "rationale": "..."
    },
    {
      "id": "P02",
      "spec_type": "interaction",
      "iv1": "poverty_rate",
      "iv2": "log_nonprofit_branch_density",
      "dv": "fundraising_efficiency_w",
      "expected_direction": "negative",
      "rationale": "..."
    }
  ]
}
```

`expected_direction` ∈ {`positive`, `negative`, `unspecified`}.

## Hybrid path (no API key)

1. Run `--evaluate`.
2. Paste [`prompts/PHASE3_HYBRID_PROMPT.md`](prompts/PHASE3_HYBRID_PROMPT.md) into Antigravity/Cursor.
3. Let the IDE agent write `proposals_roundN.json`, then invoke `--run`, then write interpretation.

## Soup-kitchen track

1. Read [`SOUP_KITCHEN_WORKFLOW.md`](SOUP_KITCHEN_WORKFLOW.md).
2. `10_acquire_soup_kitchens.py --pilot` → `data/soup_kitchens.csv`.
3. `11_merge_soup_kitchen_density.py` → frame with `soup_kitchen_density`.
4. Propose/run a demo (e.g. density × poverty → efficiency on Atlanta subsample).

## Calibration vs discovery

- **H4/H5 `--validate`:** exact β reproduction (engineering check).
- **New proposals:** sign + significance vs `expected_direction` (research check). Do not treat p < 0.05 alone as success—see CP3 `two_variable_limitation.md`.
