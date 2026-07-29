# Phase 3 Execution Results & Runs Gallery

This folder contains the output logs, proposals, evaluation summaries, and verification tables produced by `09_phase3_agentic_loop.py` and `reproduce.sh`.

## Folder Organization

```
phase3_results/
├── README.md                          # This directory guide
├── validation_check.md                # Step 1: H4/H5 baseline reproduction check
├── round1_results.* & round2_results.* # Default Atlanta food-assistance multi-round run outputs
├── round99_results.*                  # TA verifier synthesis outputs
├── evaluation_summary.json / .md      # Overall performance metrics across rounds
├── proposals_round*.json              # Pre-registered proposals generated prior to OLS
├── decision_log.jsonl                 # Machine-readable step audit trail
├── ta_verify/                         # TA Verifier gate run outputs (I1-I4 / Q1 test suites)
├── housing_chicago/                   # NTEE housing services universality run outputs
├── agent_bus/                         # Active inter-agent payload bus (ephemeral during runs)
└── stale_archive/                     # Historical run dumps (gitignored)
```

## Key Student Inspection Points

1. **`validation_check.md`**: Open this file first after running `reproduce.sh` to confirm H4/H5 OLS coefficient reproduction (**PASS**).
2. **`round1_results.md` & `round2_results.md`**: Inspect how the multi-agent loop evaluates indicators (e.g. `F01` food assistance density) against the ΔR² ≥ 5e-4 & Wald F p < 0.05 verifier gates.
3. **`ta_verify/round99_results.md`**: Inspect how invalid / identity / post-hoc proposals (I1, I2, Q1) are correctly **REJECTED** by the Stats Engine.
