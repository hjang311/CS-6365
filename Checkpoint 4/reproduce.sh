#!/usr/bin/env bash
# One-command offline reproducibility for Checkpoint 4 Phase 3 demos.
# Run from the repository root:  bash "Checkpoint 4/reproduce.sh"
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
else
  echo "WARN: .venv/bin/python not found; using python3 on PATH" >&2
  PY="python3"
fi

CP4="$ROOT/Checkpoint 4"
RUNNER="$CP4/09_phase3_agentic_loop.py"

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

echo ""
echo "=== All offline demos complete ==="
echo "Artifacts:"
echo "  $CP4/phase3_results/validation_check.md"
echo "  $CP4/phase3_results/ta_verify/round99_results.md"
echo "  $CP4/phase3_results/round1_results.md"
echo "  $CP4/phase3_results/round2_results.md"
echo "  $CP4/phase3_results/housing_chicago/round1_results.md"
echo "Next: read Checkpoint 4/STUDENT_QUICKSTART.md and Checkpoint 4/BENCHMARK.md"
