#!/usr/bin/env bash
# One-command offline reproducibility for Checkpoint 4 Phase 3 demos.
# Run from the repository root:  bash "Checkpoint 4/reproduce.sh"
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
START_TS=$(date +%s)

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
else
  echo "WARN: .venv/bin/python not found; using python3 on PATH" >&2
  PY="python3"
fi

CP3_FRAME="$ROOT/Checkpoint 3/data/cp3_modeling_frame.csv"
CP4="$ROOT/Checkpoint 4"
RUNNER="$CP4/09_phase3_agentic_loop.py"

echo "=== Preflight ==="
if [[ ! -f "$CP3_FRAME" ]]; then
  cat >&2 <<'EOF'
ERROR: Missing Checkpoint 3 modeling frame required for offline demos:

  Checkpoint 3/data/cp3_modeling_frame.csv

This CSV is gitignored (~large). Regenerate before re-running:

  Mode A (handoff CSVs already present under Checkpoint 3/data/):
    .venv/bin/python "Checkpoint 3/02_merge_pipeline.py"

  Mode B (fresh acquire — needs CENSUS_API_KEY + network):
    See Checkpoint 3/README.md → “Reproduction mode B”

Then re-run:  bash "Checkpoint 4/reproduce.sh"
EOF
  exit 1
fi

if ! "$PY" -c "import pandas, statsmodels" 2>/dev/null; then
  echo "ERROR: pandas/statsmodels missing for: $PY" >&2
  echo "Fix:  $PY -m pip install -r \"Checkpoint 4/requirements.txt\"" >&2
  exit 1
fi

ROWS=$("$PY" -c "import pandas as pd; print(len(pd.read_csv('$CP3_FRAME', usecols=[0])))")
echo "OK: modeling frame present ($ROWS rows)"
echo "OK: python deps importable ($PY)"
echo ""

echo "=== Step 1: H4/H5 calibration ==="
"$PY" "$RUNNER" --validate

echo "=== Step 2: TA Verifier gate (I1–I4 / Q1) ==="
"$PY" "$RUNNER" --verify-ta-specs --out "$CP4/phase3_results/ta_verify"

echo "=== Step 3: Food Atlanta fixture-full (2 rounds) ==="
"$PY" "$RUNNER" --all --fixture-full --rounds 2

echo "=== Step 4: Housing Chicago universality (NTEE) ==="
"$PY" "$RUNNER" \
  --enrich-config "$CP4/configs/housing_services_chicago.json" \
  --all --fixture --rounds 1 \
  --out "$CP4/phase3_results/housing_chicago"

END_TS=$(date +%s)
ELAPSED=$((END_TS - START_TS))

echo ""
echo "=== All offline demos complete (${ELAPSED}s) ==="
echo "Expected self-checks (open these files):"
echo "  validation_check.md  →  H4: PASS (β ≈ -7.91647)  H5: PASS (β ≈ +2.11963)"
echo "  ta_verify/round99_results.md  →  I1/I2/Q1 REJECT; I3 ACCEPT; I4 REJECT"
echo "  round1_results.md  →  F01 not significant; F02 gate REJECT"
echo "  housing_chicago/round1_results.md  →  H01 exploratory; H02 gate REJECT"
echo ""
echo "Artifacts:"
echo "  $CP4/phase3_results/validation_check.md"
echo "  $CP4/phase3_results/ta_verify/round99_results.md"
echo "  $CP4/phase3_results/round1_results.md"
echo "  $CP4/phase3_results/round2_results.md"
echo "  $CP4/phase3_results/housing_chicago/round1_results.md"
echo "Next: read Checkpoint 4/STUDENT_QUICKSTART.md and Checkpoint 4/BENCHMARK.md"
