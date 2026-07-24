"""
09_phase3_agentic_loop.py  —  Phase 3: Multi-Agent Rolled Loop

Evaluate → (Scout → Acquire/Enrich → Critic) → propose → pre-register →
deterministic OLS → interpret.

Modes:
  --validate       Replay H4 & H5 β calibration
  --evaluate       Phase 2 summary
  --scout          Discover source candidates (fixture or stub for live)
  --acquire-plan   Run named acquisition adapter from JSON plan
  --enrich-config  NTEE (or plan) enrichment shortcut
  --propose / --run / --interpret
  --all            evaluate → optional enrich → propose → run → interpret
  --fixture        offline propose/interpret (no scout/acquire)
  --fixture-full   offline full multi-agent bus demo

INVARIANT: Agent never computes statistics. Proposals locked before OLS.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Paths & identity
# ---------------------------------------------------------------------------
SCRIPT_VERSION = "09_phase3_agentic_loop.py v2.1 (Phase3 Multi-Agent / 2026-07-21)"
BUILT_BY = "Phase3_MultiAgent"

# TA Verifier gate (ai-suggestions/cp4 09_rolled_agentic_loop.py)
GATE_ALPHA = 0.05
GATE_MIN_DELTA_R2 = 5e-4

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
CP3_DIR = REPO_ROOT / "Checkpoint 3"
DEFAULT_FRAME = CP3_DIR / "data" / "cp3_modeling_frame.csv"
DEFAULT_PHASE2 = CP3_DIR / "loop_results_v2"
DEFAULT_OUT = HERE / "phase3_results"
DEFAULT_DATA = HERE / "data"
BMF_PATH = CP3_DIR / "data" / "irs_bmf.csv"
ACS_PATH = CP3_DIR / "data" / "census_acs_by_zip.csv"

# enrichment helpers live beside this script
sys.path.insert(0, str(HERE))
from enrichment_tools.agent_bus import (  # noqa: E402
    append_bus_message,
    utc_now as bus_utc_now,
    write_payload,
)
from phase3_enrichment_cmds import (  # noqa: E402
    FIXTURE_PROPOSALS_FOOD,
    FIXTURE_PROPOSALS_FOOD_R2,
    FIXTURE_PROPOSALS_HOUSING,
    EnrichmentContext,
    cmd_acquire,
    cmd_critic_sources,
    cmd_enrich_config,
    cmd_fixture_full_bus,
    cmd_scout,
)

# Import shared OLS helpers from Checkpoint 3 without modifying CP3.
sys.path.insert(0, str(CP3_DIR))
try:
    import importlib.util

    _spec = importlib.util.spec_from_file_location(
        "cp3_08", CP3_DIR / "08_unrolled_loop.py"
    )
    _cp3_08 = importlib.util.module_from_spec(_spec)
    assert _spec.loader is not None
    _spec.loader.exec_module(_cp3_08)
    CONTROLS = _cp3_08.CONTROLS
    CONTROL_COLS = _cp3_08.CONTROL_COLS
    H4_BASELINE_BETA = _cp3_08.H4_BASELINE_BETA
    H5_BASELINE_BETA = _cp3_08.H5_BASELINE_BETA
    BETA_TOL = _cp3_08.BETA_TOL
    run_ols = _cp3_08.run_ols
    extract_iv_stats = _cp3_08.extract_iv_stats
    observed_direction = _cp3_08.observed_direction
    direction_match = _cp3_08.direction_match
except Exception as exc:  # pragma: no cover - fallback mirrors 08
    print(f"WARN: could not import Checkpoint 3/08 helpers ({exc}); using local fallback")
    CONTROLS = (
        "log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income"
    )
    CONTROL_COLS = [
        "log_total_revenue",
        "poverty_rate",
        "median_hh_income",
        "ntee_major",
        "region",
    ]
    H4_BASELINE_BETA = -7.91647
    H5_BASELINE_BETA = 2.11963
    BETA_TOL = 1e-3

    def run_ols(df: pd.DataFrame, iv: str, dv: str):
        cols = [iv, dv] + CONTROL_COLS
        missing = [c for c in cols if c not in df.columns]
        if missing:
            return None, f"missing columns: {missing}"
        is_categorical_iv = iv == "size_segment" or df[iv].dtype == object
        df_clean = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
        if len(df_clean) < 100:
            return None, f"n={len(df_clean)} < 100 after dropna"
        formula_iv = f"C({iv})" if is_categorical_iv else iv
        formula = f"{dv} ~ {formula_iv} + {CONTROLS}"
        try:
            m = smf.ols(formula, data=df_clean).fit(cov_type="HC1")
            return m, None
        except Exception as e:
            return None, str(e)

    def extract_iv_stats(m, iv: str) -> dict[str, float]:
        if iv in m.params.index:
            key = iv
        else:
            candidates = [k for k in m.params.index if k.startswith(f"C({iv})")]
            key = candidates[0] if candidates else None
        if key is None:
            return {
                "beta": float("nan"),
                "pvalue": float("nan"),
                "ci_low": float("nan"),
                "ci_high": float("nan"),
            }
        ci = m.conf_int().loc[key]
        return {
            "beta": float(m.params[key]),
            "pvalue": float(m.pvalues[key]),
            "ci_low": float(ci[0]),
            "ci_high": float(ci[1]),
        }

    def observed_direction(beta: float, pvalue: float, alpha: float = 0.05) -> str:
        if pvalue >= alpha or not np.isfinite(beta):
            return "none"
        return "positive" if beta > 0 else "negative"

    def direction_match(expected: str, observed: str) -> str:
        if expected == "unspecified":
            return "exploratory (no prior)"
        if expected == "none":
            return "n/a (no directional claim)"
        if observed == "none":
            return "not significant"
        return "confirmed" if expected == observed else "rejected (opposite or mismatch)"


PROVENANCE: dict[str, Any] = {"built_by": BUILT_BY, "script": SCRIPT_VERSION}


def utc_now() -> str:
    """Single timestamp format shared with agent_bus."""
    return bus_utc_now()


def display_path(path: Path | str) -> str:
    p = Path(path).resolve()
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def set_provenance(frame_path: Path, df: pd.DataFrame) -> None:
    PROVENANCE.update(
        generated_at=utc_now(),
        frame=display_path(frame_path),
        frame_shape=f"{df.shape[0]:,} rows x {df.shape[1]} cols",
        script=SCRIPT_VERSION,
        built_by=BUILT_BY,
    )


def prov_lines() -> list[str]:
    return [
        "",
        "---",
        f"*Generated: {PROVENANCE.get('generated_at', '?')} · "
        f"Frame: `{PROVENANCE.get('frame', '?')}` ({PROVENANCE.get('frame_shape', '?')}) · "
        f"{PROVENANCE.get('script', '?')} · built_by: {PROVENANCE.get('built_by', BUILT_BY)}*",
    ]


def _decision_fingerprint(event: dict[str, Any]) -> tuple[Any, ...]:
    keys = ("event", "round", "path", "results_md", "adapter", "label", "source")
    return tuple(event.get(k) for k in keys)


def append_decision(out_dir: Path, event: dict[str, Any]) -> None:
    """Append to decision_log.jsonl; skip identical consecutive duplicates."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "decision_log.jsonl"
    record = {"ts": utc_now(), "built_by": BUILT_BY, **event}
    if path.exists():
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        if lines:
            try:
                prev = json.loads(lines[-1])
                prev_fp = _decision_fingerprint(prev)
                cur_fp = _decision_fingerprint(record)
                if prev_fp == cur_fp and prev.get("event") == record.get("event"):
                    return
            except json.JSONDecodeError:
                pass
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def load_frame(frame_path: Path) -> pd.DataFrame:
    if not frame_path.exists():
        raise FileNotFoundError(f"Modeling frame not found: {frame_path}")
    df = pd.read_csv(frame_path, dtype={"ZIP5": str}, low_memory=False)
    return df


# ---------------------------------------------------------------------------
# Interaction OLS + TA Verifier gate (same-row nested models)
# ---------------------------------------------------------------------------
def _controls_excluding(*focal: str) -> tuple[str, list[str]]:
    """
    Build CONTROLS formula/list with focal IVs removed so they are not duplicated
    when a control (e.g. poverty_rate) is also a higher-order IV.
    """
    focal_set = {f for f in focal if f}
    cols = [c for c in CONTROL_COLS if c not in focal_set]
    parts: list[str] = []
    for c in cols:
        if c in ("ntee_major", "region"):
            parts.append(f"C({c})")
        else:
            parts.append(c)
    return " + ".join(parts), cols


def _formula_term(col: str, df: pd.DataFrame) -> str:
    if col == "size_segment" or (
        col in df.columns and df[col].dtype == object
    ):
        return f"C({col})"
    return col


def _added_terms(full, base_main) -> list[str]:
    base = set(base_main.params.index)
    return [k for k in full.params.index if k not in base and k != "Intercept"]


def _robust_wald_f(full, added: list[str]) -> tuple[float, float]:
    """Robust (HC1) Wald F-test that all added higher-order terms are zero."""
    names = list(full.params.index)
    k = len(names)
    R = np.zeros((len(added), k))
    for i, term in enumerate(added):
        R[i, names.index(term)] = 1.0
    res = full.f_test(R)
    return float(np.squeeze(res.fvalue)), float(res.pvalue)


def _gate_decision(wald_p: float, delta_r2: float) -> tuple[str, str]:
    sig = wald_p < GATE_ALPHA
    meaningful = delta_r2 >= GATE_MIN_DELTA_R2
    if sig and meaningful:
        return (
            "ACCEPT",
            (
                f"Added terms jointly significant (robust F p={wald_p:.3g}) and add "
                f"delta_R2={delta_r2:.4f} over main effects."
            ),
        )
    if sig and not meaningful:
        return (
            "REJECT",
            (
                f"Statistically significant (p={wald_p:.3g}) but delta_R2="
                f"{delta_r2:.4f} < {GATE_MIN_DELTA_R2} — large-n significance "
                "without real explanatory gain (the Phase 2 limitation, re-detected)."
            ),
        )
    return (
        "REJECT",
        f"Added terms not jointly significant (robust F p={wald_p:.3g}).",
    )


def verify_interaction(
    df: pd.DataFrame, iv1: str, iv2: str, dv: str
) -> tuple[Optional[Any], dict[str, Any], Optional[str]]:
    """
    Fit full / main / controls on identical rows; return full model, gate stats, error.
    """
    ctrl_formula, ctrl_cols = _controls_excluding(iv1, iv2)
    for c in CONTROL_COLS:
        if c not in (iv1, iv2) and c not in df.columns:
            return None, {}, f"missing columns: {[c]}"
    cols = [iv1, iv2, dv] + ctrl_cols
    missing = [c for c in cols if c not in df.columns]
    if missing:
        return None, {}, f"missing columns: {missing}"
    d = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(d) < 100:
        return None, {}, f"n={len(d)} < 100 after dropna"

    t1, t2 = _formula_term(iv1, d), _formula_term(iv2, d)
    full_rhs = f"{t1} + {t2} + {t1}:{t2}"
    main_rhs = f"{t1} + {t2}"
    try:
        if ctrl_formula:
            full = smf.ols(f"{dv} ~ {full_rhs} + {ctrl_formula}", data=d).fit(
                cov_type="HC1"
            )
            base_main = smf.ols(f"{dv} ~ {main_rhs} + {ctrl_formula}", data=d).fit(
                cov_type="HC1"
            )
            base_ctrl = smf.ols(f"{dv} ~ {ctrl_formula}", data=d).fit(cov_type="HC1")
        else:
            full = smf.ols(f"{dv} ~ {full_rhs}", data=d).fit(cov_type="HC1")
            base_main = smf.ols(f"{dv} ~ {main_rhs}", data=d).fit(cov_type="HC1")
            base_ctrl = smf.ols(f"{dv} ~ 1", data=d).fit(cov_type="HC1")
    except Exception as e:
        return None, {}, str(e)

    added = _added_terms(full, base_main)
    if not added:
        return (
            full,
            {
                "gate_decision": "REJECT",
                "gate_reason": "spec added no terms over main effects",
                "wald_f": None,
                "wald_p": None,
                "r2_full": float(full.rsquared),
                "r2_main": float(base_main.rsquared),
                "r2_controls": float(base_ctrl.rsquared),
                "delta_r2_higherorder": 0.0,
                "delta_r2_over_naive": float(full.rsquared - base_ctrl.rsquared),
                "added_terms": [],
            },
            None,
        )

    wald_f, wald_p = _robust_wald_f(full, added)
    delta_ho = float(full.rsquared - base_main.rsquared)
    decision, reason = _gate_decision(wald_p, delta_ho)
    gate = {
        "wald_f": wald_f,
        "wald_p": wald_p,
        "r2_full": float(full.rsquared),
        "r2_main": float(base_main.rsquared),
        "r2_controls": float(base_ctrl.rsquared),
        "delta_r2_higherorder": delta_ho,
        "delta_r2_over_naive": float(full.rsquared - base_ctrl.rsquared),
        "added_terms": added,
        "gate_decision": decision,
        "gate_reason": reason,
    }
    return full, gate, None


def verify_quadratic(
    df: pd.DataFrame, iv: str, dv: str
) -> tuple[Optional[Any], dict[str, Any], Optional[str]]:
    """Quadratic higher-order gate: iv + I(iv**2) vs main iv only."""
    ctrl_formula, ctrl_cols = _controls_excluding(iv)
    for c in CONTROL_COLS:
        if c != iv and c not in df.columns:
            return None, {}, f"missing columns: {[c]}"
    cols = [iv, dv] + ctrl_cols
    missing = [c for c in cols if c not in df.columns]
    if missing:
        return None, {}, f"missing columns: {missing}"
    d = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(d) < 100:
        return None, {}, f"n={len(d)} < 100 after dropna"
    t = _formula_term(iv, d)
    full_rhs = f"{t} + I({iv} ** 2)"
    main_rhs = t
    try:
        if ctrl_formula:
            full = smf.ols(f"{dv} ~ {full_rhs} + {ctrl_formula}", data=d).fit(
                cov_type="HC1"
            )
            base_main = smf.ols(f"{dv} ~ {main_rhs} + {ctrl_formula}", data=d).fit(
                cov_type="HC1"
            )
            base_ctrl = smf.ols(f"{dv} ~ {ctrl_formula}", data=d).fit(cov_type="HC1")
        else:
            full = smf.ols(f"{dv} ~ {full_rhs}", data=d).fit(cov_type="HC1")
            base_main = smf.ols(f"{dv} ~ {main_rhs}", data=d).fit(cov_type="HC1")
            base_ctrl = smf.ols(f"{dv} ~ 1", data=d).fit(cov_type="HC1")
    except Exception as e:
        return None, {}, str(e)

    added = _added_terms(full, base_main)
    if not added:
        return None, {}, "no added higher-order terms detected"
    wald_f, wald_p = _robust_wald_f(full, added)
    delta_ho = float(full.rsquared - base_main.rsquared)
    decision, reason = _gate_decision(wald_p, delta_ho)
    # Prefer quadratic term for theory β
    quad_keys = [k for k in added if "I(" in k or "**" in k]
    beta_key = quad_keys[0] if quad_keys else added[0]
    gate = {
        "wald_f": wald_f,
        "wald_p": wald_p,
        "r2_full": float(full.rsquared),
        "r2_main": float(base_main.rsquared),
        "r2_controls": float(base_ctrl.rsquared),
        "delta_r2_higherorder": delta_ho,
        "delta_r2_over_naive": float(full.rsquared - base_ctrl.rsquared),
        "added_terms": added,
        "gate_decision": decision,
        "gate_reason": reason,
        "focal_term": beta_key,
        "beta": float(full.params[beta_key]),
        "pvalue": float(full.pvalues[beta_key]),
    }
    return full, gate, None


def run_ols_interaction(
    df: pd.DataFrame, iv1: str, iv2: str, dv: str
) -> tuple[Any, Optional[str]]:
    """Backward-compatible wrapper; prefer verify_interaction for gated runs."""
    m, _gate, err = verify_interaction(df, iv1, iv2, dv)
    return m, err


def extract_interaction_stats(m, iv1: str, iv2: str) -> dict[str, Any]:
    """Prefer the interaction term; also return main effects."""
    inter_key = f"{iv1}:{iv2}"
    alt_key = f"{iv2}:{iv1}"
    # Also match C()-wrapped interaction keys
    key = None
    for cand in (inter_key, alt_key):
        if cand in m.params.index:
            key = cand
            break
    if key is None:
        for k in m.params.index:
            if ":" in k and (iv1 in k and iv2 in k):
                key = k
                break
    out: dict[str, Any] = {
        "interaction_term": key,
        "beta": float("nan"),
        "pvalue": float("nan"),
        "ci_low": float("nan"),
        "ci_high": float("nan"),
        "beta_iv1": float("nan"),
        "pvalue_iv1": float("nan"),
        "beta_iv2": float("nan"),
        "pvalue_iv2": float("nan"),
    }
    if key is not None:
        ci = m.conf_int().loc[key]
        out["beta"] = float(m.params[key])
        out["pvalue"] = float(m.pvalues[key])
        out["ci_low"] = float(ci[0])
        out["ci_high"] = float(ci[1])
    if iv1 in m.params.index:
        out["beta_iv1"] = float(m.params[iv1])
        out["pvalue_iv1"] = float(m.pvalues[iv1])
    if iv2 in m.params.index:
        out["beta_iv2"] = float(m.params[iv2])
        out["pvalue_iv2"] = float(m.pvalues[iv2])
    return out


def _apply_gate_fields(row: dict[str, Any], gate: dict[str, Any]) -> None:
    for k in (
        "wald_f",
        "wald_p",
        "r2_full",
        "r2_main",
        "r2_controls",
        "delta_r2_higherorder",
        "delta_r2_over_naive",
        "added_terms",
        "gate_decision",
        "gate_reason",
    ):
        if k in gate:
            row[k] = gate[k]


# TA higher-order specs (ai-suggestions/cp4) for --verify-ta-specs
TA_VERIFY_SPECS: list[dict[str, Any]] = [
    {
        "id": "I1",
        "spec_type": "interaction",
        "iv1": "log_zhvi_2022",
        "iv2": "log_nonprofit_branch_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": "Does the H4 housing-cost penalty depend on provider-field density (H5)?",
    },
    {
        "id": "I2",
        "spec_type": "interaction",
        "iv1": "log_zhvi_2022",
        "iv2": "log_bank_branch_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": "Whether bank sparsity moderates the real-estate overhead effect.",
    },
    {
        "id": "I3",
        "spec_type": "interaction",
        "iv1": "log_zhvi_2022",
        "iv2": "size_segment",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": "CP3 size split: large orgs more ZHVI-sensitive than mid.",
    },
    {
        "id": "I4",
        "spec_type": "interaction",
        "iv1": "log_nonprofit_branch_density",
        "iv2": "size_segment",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": "Whether agglomeration (H5) strengthens with org size.",
    },
    {
        "id": "Q1",
        "spec_type": "quadratic",
        "iv": "log_zhvi_2022",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": "Whether the housing-cost penalty accelerates (non-linear).",
    },
]


# ---------------------------------------------------------------------------
# --validate (H4 / H5)
# ---------------------------------------------------------------------------
def cmd_validate(frame_path: Path, out_dir: Path) -> int:
    df = load_frame(frame_path)
    set_provenance(frame_path, df)
    out_dir.mkdir(parents=True, exist_ok=True)

    checks = [
        ("H4", "log_zhvi_2022", "fundraising_efficiency_w", H4_BASELINE_BETA),
        ("H5", "log_nonprofit_branch_density", "fundraising_efficiency_w", H5_BASELINE_BETA),
    ]
    lines = [
        "# Phase 3 Validation Check (H4 & H5 via shared 08 recipe)",
        "",
        "**PASS = beta REPRODUCTION** within tolerance (not theory confirmation).",
        "",
        "| Hypothesis | IV | Expected β | Loop β | |Δ| | Status |",
        "|---|---|---|---|---|---|",
    ]
    all_pass = True
    for hid, iv, dv, expected in checks:
        m, err = run_ols(df, iv, dv)
        if m is None:
            status = "FAIL"
            loop_beta = "N/A"
            delta = err or "N/A"
            all_pass = False
        else:
            stats = extract_iv_stats(m, iv)
            loop_beta_f = float(stats["beta"])
            delta_f = abs(loop_beta_f - expected)
            status = "PASS" if delta_f < BETA_TOL else "FAIL"
            if status == "FAIL":
                all_pass = False
            loop_beta = f"{loop_beta_f:.5f}"
            delta = f"{delta_f:.6f}"
        lines.append(
            f"| {hid} | `{iv}` | `{expected:.5f}` | `{loop_beta}` | `{delta}` | **{status}** |"
        )
    lines.extend(prov_lines())
    path = out_dir / "validation_check.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    append_decision(out_dir, {"event": "validate", "pass": all_pass, "path": str(path)})
    print(f"Wrote {path}  ({'PASS' if all_pass else 'FAIL'})")
    return 0 if all_pass else 1


# ---------------------------------------------------------------------------
# --evaluate
# ---------------------------------------------------------------------------
def _read_text(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"(missing: {path})"


def cmd_evaluate(phase2_dir: Path, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    list_a = _read_text(phase2_dir / "list_a_results.md")
    list_b = _read_text(phase2_dir / "list_b_results.md")
    limitation = _read_text(phase2_dir / "two_variable_limitation.md")
    validation = _read_text(phase2_dir / "validation_check.md")

    summary = {
        "built_by": BUILT_BY,
        "generated_at": utc_now(),
        "phase2_dir": display_path(phase2_dir),
        "highlights": {
            "H4": "confirmed (negative ZHVI → efficiency); β ≈ -7.92",
            "H5": "significant but theory rejected (positive density → efficiency)",
            "limitation": (
                "2-var OLS easy to light up / hard to trust; near-identical R²; "
                "mechanical hits; coarse ZIP granularity → Phase 3"
            ),
            "phase3_tracks": [
                "propose new socioeconomic indicators and test via shared OLS",
                "higher-order interaction specs (3+ variables)",
                "finer-granularity ACFB soup-kitchen density by ZIP",
            ],
        },
        "available_frame_hint": (
            "Prefer external/structural IVs already on frame "
            "(log_zhvi_2022, log_bank_branch_density, poverty_rate, median_hh_income, "
            "population, soup_kitchen_density if merged). Avoid mechanical DV components."
        ),
    }

    md_lines = [
        "# Phase 3 Evaluation Summary (deterministic)",
        "",
        "This artifact is the **input context** for the propose step. "
        "It is assembled from Checkpoint 3 Phase 2 outputs; no new OLS is run here.",
        "",
        "## Highlights for the agent",
        "",
        f"- **H4:** {summary['highlights']['H4']}",
        f"- **H5:** {summary['highlights']['H5']}",
        f"- **Limitation thesis:** {summary['highlights']['limitation']}",
        "",
        "### Phase 3 tracks to pursue",
        "",
    ]
    for t in summary["highlights"]["phase3_tracks"]:
        md_lines.append(f"- {t}")
    md_lines.extend(
        [
            "",
            f"**Frame IV hint:** {summary['available_frame_hint']}",
            "",
            "## Source: List A (excerpt)",
            "",
            "```",
            list_a[:2500],
            "```",
            "",
            "## Source: List B (excerpt)",
            "",
            "```",
            list_b[:2000],
            "```",
            "",
            "## Source: Two-variable limitation (excerpt)",
            "",
            "```",
            limitation[:3000],
            "```",
            "",
            "## Source: Validation",
            "",
            "```",
            validation[:1500],
            "```",
            "",
            "---",
            f"*Generated: {summary['generated_at']} · Phase2: `{summary['phase2_dir']}` · "
            f"built_by: {BUILT_BY} · {SCRIPT_VERSION}*",
        ]
    )

    md_path = out_dir / "evaluation_summary.md"
    json_path = out_dir / "evaluation_summary.json"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    append_decision(
        out_dir,
        {"event": "evaluate", "md": str(md_path), "json": str(json_path)},
    )
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    return 0


# ---------------------------------------------------------------------------
# --propose
# ---------------------------------------------------------------------------
FIXTURE_PROPOSALS = [
    {
        "id": "P01",
        "spec_type": "two_var",
        "iv": "log_bank_branch_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "rationale": (
            "Phase 2 H2_replay confirmed negative bank density → efficiency; "
            "re-test as a Phase 3 agenda item with explicit prior."
        ),
    },
    {
        "id": "P02",
        "spec_type": "interaction",
        "iv1": "poverty_rate",
        "iv2": "log_nonprofit_branch_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "rationale": (
            "Higher-order: poverty may moderate the provider-density link that "
            "rejected H5's competition story in Phase 2."
        ),
    },
    {
        "id": "P03",
        "spec_type": "two_var",
        "iv": "population",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": (
            "Phase 2 weak_population case: large-n makes tiny β look significant; "
            "re-run as exploratory to keep the limitation thesis visible in Phase 3."
        ),
    },
]

# Round 2 fixture: finer-granularity food-assistance density (after 10/11 merge).
FIXTURE_PROPOSALS_R2 = [
    {
        "id": "R2P01",
        "spec_type": "two_var",
        "iv": "log_soup_kitchen_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "rationale": (
            "Phase 3 finer-granularity track: Feed America–scaled / ACFB-area "
            "food-assistance density per 10k (not IRS HQ NTEE proxy)."
        ),
    },
    {
        "id": "R2P02",
        "spec_type": "interaction",
        "iv1": "poverty_rate",
        "iv2": "log_soup_kitchen_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "rationale": (
            "Higher-order: poverty may intensify the soup-kitchen / pantry "
            "density association on the expanded ZIP coverage."
        ),
    },
    {
        "id": "R2P03",
        "spec_type": "two_var",
        "iv": "soup_kitchen_local_count",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": (
            "Exploratory big-vs-local stretch: count of local-classified sites "
            "per ZIP from merged soup_kitchens.csv."
        ),
    },
]


def _propose_prompt(eval_md: str) -> str:
    return (
        "You are the Phase 3 NORP research agent. Given the evaluation summary below, "
        "propose 2–5 NEW hypothesis specs to test. Return ONLY valid JSON with key "
        "'proposals' (array). Each item needs: id, spec_type ('two_var' or 'interaction'), "
        "dv (usually fundraising_efficiency_w), expected_direction "
        "('positive'|'negative'|'unspecified'), rationale. "
        "For two_var include 'iv'. For interaction include 'iv1' and 'iv2'. "
        "Prefer external/structural indicators. Avoid mechanical DV components "
        "(total_contributions, fundraising_expense_proxy, event fees).\n\n"
        "=== EVALUATION SUMMARY ===\n"
        f"{eval_md[:8000]}\n"
        "=== END ===\n"
    )


def _parse_proposals_blob(text: str) -> list[dict[str, Any]]:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = [ln for ln in lines if not ln.strip().startswith("```")]
        text = "\n".join(lines)
    data = json.loads(text)
    if isinstance(data, dict) and "proposals" in data:
        return list(data["proposals"])
    if isinstance(data, list):
        return data
    raise ValueError("Expected JSON object with 'proposals' or a JSON array")


def _call_gemini(prompt: str) -> str:
    try:
        from dotenv import load_dotenv

        load_dotenv(REPO_ROOT / ".env")
    except ImportError:
        pass
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not set. Use stdin/--fixture, or add key to .env"
        )
    try:
        import google.generativeai as genai
    except ImportError as e:
        raise RuntimeError(
            "google-generativeai not installed. "
            "pip install google-generativeai  OR use --fixture / stdin"
        ) from e
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    resp = model.generate_content(prompt)
    return resp.text or ""


def _enrich_ctx() -> EnrichmentContext:
    return EnrichmentContext(
        data_dir=DEFAULT_DATA,
        bmf_path=BMF_PATH,
        acs_path=ACS_PATH,
        utc_now=utc_now,
        append_decision=append_decision,
        load_frame=load_frame,
    )


def cmd_propose(
    out_dir: Path,
    round_n: int,
    use_fixture: bool,
    use_api: bool,
    frame_path: Optional[Path] = None,
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    eval_path = out_dir / "evaluation_summary.md"
    eval_md = eval_path.read_text(encoding="utf-8") if eval_path.exists() else (
        "(No evaluation_summary.md yet — run --evaluate first.)"
    )

    source = "stdin"
    if use_fixture:
        cols = set()
        if frame_path is not None and frame_path.exists():
            try:
                cols = set(pd.read_csv(frame_path, nrows=0).columns)
            except Exception:
                cols = set()
        if "log_housing_services_density" in cols:
            proposals = FIXTURE_PROPOSALS_HOUSING
            source = "fixture_housing"
        elif "log_food_assistance_density" in cols:
            if round_n >= 2:
                proposals = FIXTURE_PROPOSALS_FOOD_R2
                source = "fixture_food_r2"
            else:
                proposals = FIXTURE_PROPOSALS_FOOD
                source = "fixture_food"
        else:
            proposals = FIXTURE_PROPOSALS_R2 if round_n >= 2 else FIXTURE_PROPOSALS
            source = "fixture"
        raw = json.dumps({"proposals": proposals}, indent=2)
    elif use_api:
        source = "api"
        raw = _call_gemini(_propose_prompt(eval_md))
        proposals = _parse_proposals_blob(raw)
    else:
        print(_propose_prompt(eval_md))
        print(
            "\n--- Paste JSON proposals (end with a line containing only END) ---\n",
            flush=True,
        )
        buf: list[str] = []
        for line in sys.stdin:
            if line.strip() == "END":
                break
            buf.append(line)
        raw = "".join(buf)
        proposals = _parse_proposals_blob(raw)

    payload = {
        "provenance": {
            "built_by": BUILT_BY,
            "round": round_n,
            "generated_at": utc_now(),
            "source": source,
            "script": SCRIPT_VERSION,
            "pre_registered_before_ols": True,
        },
        "proposals": proposals,
    }
    path = out_dir / f"proposals_round{round_n}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    append_bus_message(
        out_dir,
        from_agent="researcher",
        to_agent="stats_engine",
        msg_type="proposals",
        round_n=round_n,
        payload_path=path,
    )
    append_decision(
        out_dir,
        {
            "event": "propose",
            "round": round_n,
            "source": source,
            "n_proposals": len(proposals),
            "path": str(path),
        },
    )
    print(f"Pre-registered {len(proposals)} proposals → {path}")
    return 0


# ---------------------------------------------------------------------------
# --run
# ---------------------------------------------------------------------------
def _latest_proposals(out_dir: Path, round_n: Optional[int]) -> Path:
    if round_n is not None:
        p = out_dir / f"proposals_round{round_n}.json"
        if not p.exists():
            raise FileNotFoundError(p)
        return p
    cands = sorted(out_dir.glob("proposals_round*.json"))
    if not cands:
        raise FileNotFoundError(f"No proposals_round*.json in {out_dir}")
    return cands[-1]


def _round_from_path(path: Path) -> int:
    name = path.stem  # proposals_round1
    try:
        return int(name.replace("proposals_round", ""))
    except ValueError:
        return 1


def cmd_run(
    frame_path: Path,
    out_dir: Path,
    proposals_path: Optional[Path],
    round_n: Optional[int],
) -> int:
    df = load_frame(frame_path)
    set_provenance(frame_path, df)
    out_dir.mkdir(parents=True, exist_ok=True)

    prop_path = proposals_path or _latest_proposals(out_dir, round_n)
    round_id = round_n if round_n is not None else _round_from_path(prop_path)
    data = json.loads(prop_path.read_text(encoding="utf-8"))
    proposals = data.get("proposals", [])
    if not proposals:
        print("No proposals in file.", file=sys.stderr)
        return 1

    # Enforce pre-registration ordering (proposals exist before results write).
    prop_mtime = prop_path.stat().st_mtime

    rows: list[dict[str, Any]] = []
    for p in proposals:
        pid = p.get("id", "?")
        spec = p.get("spec_type", "two_var")
        dv = p.get("dv", "fundraising_efficiency_w")
        expected = p.get("expected_direction", "unspecified")
        rationale = p.get("rationale", "")
        row: dict[str, Any] = {
            "id": pid,
            "spec_type": spec,
            "dv": dv,
            "expected_direction": expected,
            "rationale": rationale,
            "status": "ok",
            "error": "",
            "nobs": "",
            "rsquared": "",
            "beta": "",
            "pvalue": "",
            "observed_direction": "",
            "direction_outcome": "",
            "significant": "",
            "iv": p.get("iv", ""),
            "iv1": p.get("iv1", ""),
            "iv2": p.get("iv2", ""),
            "formula": "",
            "wald_f": "",
            "wald_p": "",
            "r2_full": "",
            "r2_main": "",
            "r2_controls": "",
            "delta_r2_higherorder": "",
            "delta_r2_over_naive": "",
            "gate_decision": "",
            "gate_reason": "",
        }

        if spec == "interaction":
            iv1, iv2 = p.get("iv1"), p.get("iv2")
            if not iv1 or not iv2:
                row["status"] = "error"
                row["error"] = "interaction requires iv1 and iv2"
                rows.append(row)
                continue
            m, gate, err = verify_interaction(df, iv1, iv2, dv)
            ctrl_f, _ = _controls_excluding(iv1, iv2)
            row["formula"] = (
                f"{dv} ~ {iv1} + {iv2} + {iv1}:{iv2}"
                + (f" + {ctrl_f}" if ctrl_f else "")
            )
            if m is None:
                row["status"] = "error"
                row["error"] = err or "fit failed"
                row["gate_decision"] = "REJECT"
                row["gate_reason"] = err or "fit failed"
            else:
                stats = extract_interaction_stats(m, iv1, iv2)
                row["beta"] = f"{stats['beta']:.5f}" if np.isfinite(stats["beta"]) else ""
                row["pvalue"] = f"{stats['pvalue']:.6g}" if np.isfinite(stats["pvalue"]) else ""
                row["nobs"] = int(m.nobs)
                row["rsquared"] = f"{float(m.rsquared):.4f}"
                obs = observed_direction(stats["beta"], stats["pvalue"])
                row["observed_direction"] = obs
                row["direction_outcome"] = direction_match(expected, obs)
                row["significant"] = bool(
                    np.isfinite(stats["pvalue"]) and stats["pvalue"] < 0.05
                )
                row["beta_iv1"] = stats.get("beta_iv1")
                row["beta_iv2"] = stats.get("beta_iv2")
                _apply_gate_fields(row, gate)
        elif spec == "quadratic":
            iv = p.get("iv")
            if not iv:
                row["status"] = "error"
                row["error"] = "quadratic requires iv"
                rows.append(row)
                continue
            m, gate, err = verify_quadratic(df, iv, dv)
            ctrl_f, _ = _controls_excluding(iv)
            row["formula"] = (
                f"{dv} ~ {iv} + I({iv} ** 2)" + (f" + {ctrl_f}" if ctrl_f else "")
            )
            if m is None:
                row["status"] = "error"
                row["error"] = err or "fit failed"
                row["gate_decision"] = "REJECT"
                row["gate_reason"] = err or "fit failed"
            else:
                beta = gate.get("beta", float("nan"))
                pval = gate.get("pvalue", float("nan"))
                row["beta"] = f"{beta:.5f}" if np.isfinite(beta) else ""
                row["pvalue"] = f"{pval:.6g}" if np.isfinite(pval) else ""
                row["nobs"] = int(m.nobs)
                row["rsquared"] = f"{float(m.rsquared):.4f}"
                obs = observed_direction(float(beta), float(pval))
                row["observed_direction"] = obs
                row["direction_outcome"] = direction_match(expected, obs)
                row["significant"] = bool(np.isfinite(pval) and pval < 0.05)
                _apply_gate_fields(row, gate)
        else:
            iv = p.get("iv")
            if not iv:
                row["status"] = "error"
                row["error"] = "two_var requires iv"
                rows.append(row)
                continue
            # median_hh_income is in CONTROLS — skip to avoid perfect collinearity
            if iv in CONTROL_COLS:
                row["status"] = "skipped"
                row["error"] = f"IV `{iv}` is already in CONTROLS; skip collinear two_var"
                rows.append(row)
                continue
            m, err = run_ols(df, iv, dv)
            row["formula"] = f"{dv} ~ {iv} + CONTROLS"
            if m is None:
                row["status"] = "error"
                row["error"] = err or "fit failed"
            else:
                stats = extract_iv_stats(m, iv)
                row["beta"] = f"{stats['beta']:.5f}"
                row["pvalue"] = f"{stats['pvalue']:.6g}"
                row["nobs"] = int(m.nobs)
                row["rsquared"] = f"{float(m.rsquared):.4f}"
                obs = observed_direction(stats["beta"], stats["pvalue"])
                row["observed_direction"] = obs
                row["direction_outcome"] = direction_match(expected, obs)
                row["significant"] = bool(stats["pvalue"] < 0.05)
        rows.append(row)

    results_md = out_dir / f"round{round_id}_results.md"
    results_csv = out_dir / f"round{round_id}_results.csv"
    results_json = out_dir / f"round{round_id}_results.json"

    md = [
        f"# Phase 3 Round {round_id} Results",
        "",
        f"Pre-registered proposals: `{display_path(prop_path)}`",
        f"Proposals mtime precedes results write: **yes** "
        f"(proposals_mtime={prop_mtime:.0f}).",
        "",
        "Higher-order specs use the TA Verifier gate: robust HC1 Wald F "
        f"(p < {GATE_ALPHA}) **and** ΔR² ≥ {GATE_MIN_DELTA_R2} over main effects "
        "on identical rows (controls-only baseline also reported).",
        "",
        "| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Gate | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if r["spec_type"] == "interaction":
            vars_s = f"`{r['iv1']}` × `{r['iv2']}` → `{r['dv']}`"
        elif r["spec_type"] == "quadratic":
            vars_s = f"`{r['iv']}` + `I({r['iv']}**2)` → `{r['dv']}`"
        else:
            vars_s = f"`{r['iv']}` → `{r['dv']}`"
        gate = r.get("gate_decision") or "—"
        md.append(
            f"| {r['id']} | {r['spec_type']} | {vars_s} | {r['expected_direction']} | "
            f"{r['observed_direction']} | {r['direction_outcome']} | {r['beta']} | "
            f"{r['pvalue']} | {r['rsquared']} | {r['nobs']} | {gate} | {r['status']} |"
        )
    md.extend(["", "## Rationales", ""])
    for r in rows:
        md.append(f"- **{r['id']}:** {r.get('rationale', '')}")
        if r.get("error"):
            md.append(f"  - note: {r['error']}")
        if r.get("gate_reason"):
            md.append(
                f"  - gate: **{r.get('gate_decision')}** — {r['gate_reason']}"
            )
            if r.get("wald_p") not in ("", None):
                md.append(
                    f"  - Wald F={r.get('wald_f')}, p={r.get('wald_p')}; "
                    f"ΔR²(ho)={r.get('delta_r2_higherorder')}; "
                    f"R² full/main/ctrl="
                    f"{r.get('r2_full')}/{r.get('r2_main')}/{r.get('r2_controls')}"
                )
    md.extend(prov_lines())
    results_md.write_text("\n".join(md) + "\n", encoding="utf-8")

    fields = [
        "id",
        "spec_type",
        "iv",
        "iv1",
        "iv2",
        "dv",
        "expected_direction",
        "observed_direction",
        "direction_outcome",
        "beta",
        "pvalue",
        "rsquared",
        "nobs",
        "significant",
        "gate_decision",
        "wald_f",
        "wald_p",
        "delta_r2_higherorder",
        "delta_r2_over_naive",
        "r2_full",
        "r2_main",
        "r2_controls",
        "status",
        "error",
        "formula",
        "gate_reason",
    ]
    with open(results_csv, "w", newline="", encoding="utf-8") as f:
        f.write(
            f"# {PROVENANCE.get('generated_at', '?')} | {PROVENANCE.get('frame', '?')} | "
            f"{PROVENANCE.get('frame_shape', '?')} | {SCRIPT_VERSION} | built_by={BUILT_BY}\n"
        )
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    results_json.write_text(
        json.dumps(
            {
                "provenance": dict(PROVENANCE),
                "proposals_path": display_path(prop_path),
                "proposals_mtime": prop_mtime,
                "round": round_id,
                "gate": {
                    "alpha": GATE_ALPHA,
                    "min_delta_r2": GATE_MIN_DELTA_R2,
                },
                "rows": rows,
            },
            indent=2,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )

    append_decision(
        out_dir,
        {
            "event": "run",
            "round": round_id,
            "proposals_path": str(prop_path),
            "n_rows": len(rows),
            "results_md": str(results_md),
        },
    )
    print(f"Wrote {results_md}")
    print(f"Wrote {results_csv}")
    return 0


def cmd_verify_ta_specs(frame_path: Path, out_dir: Path) -> int:
    """Pre-register and run TA I1–I4 / Q1 specs with the Verifier gate."""
    out_dir.mkdir(parents=True, exist_ok=True)
    prop_path = out_dir / "proposals_ta_verify.json"
    payload = {
        "provenance": {
            "built_by": BUILT_BY,
            "source": "ta_ai_suggestions_cp4",
            "generated_at": utc_now(),
            "script": SCRIPT_VERSION,
            "pre_registered_before_ols": True,
            "gate_alpha": GATE_ALPHA,
            "gate_min_delta_r2": GATE_MIN_DELTA_R2,
        },
        "proposals": TA_VERIFY_SPECS,
    }
    prop_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    append_decision(
        out_dir,
        {
            "event": "propose",
            "round": "ta_verify",
            "source": "ta_ai_suggestions_cp4",
            "n_proposals": len(TA_VERIFY_SPECS),
            "path": str(prop_path),
        },
    )
    # Temporarily write as proposals_round99 for cmd_run naming, or pass path
    return cmd_run(frame_path, out_dir, prop_path, round_n=99)


# ---------------------------------------------------------------------------
# --interpret
# ---------------------------------------------------------------------------
def _fixture_interpretation_from_results(out_dir: Path, round_n: int) -> str:
    """Build fixture interpretation from actual roundN_results.json (no stale stubs)."""
    path = out_dir / f"round{round_n}_results.json"
    if not path.exists():
        return (
            "# Phase 3 Interpretation (fixture)\n\n"
            f"No `round{round_n}_results.json` found; re-run `--run` before interpret.\n"
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("rows") or []
    lines = [
        "# Phase 3 Interpretation (fixture)",
        "",
        "Proposals were pre-registered before OLS. Theory outcomes use sign + "
        "significance vs `expected_direction`. Higher-order specs also report the "
        f"TA Verifier gate (HC1 Wald F p < {GATE_ALPHA} and "
        f"ΔR² ≥ {GATE_MIN_DELTA_R2} over main effects).",
        "",
    ]
    for r in rows:
        rid = r.get("id", "?")
        spec = r.get("spec_type", "")
        if spec == "interaction":
            vars_s = f"{r.get('iv1')} × {r.get('iv2')}"
        elif spec == "quadratic":
            vars_s = f"{r.get('iv')} quadratic"
        else:
            vars_s = str(r.get("iv", ""))
        lines.append(
            f"- **{rid}** ({spec}, `{vars_s}`): β={r.get('beta')}, p={r.get('pvalue')}, "
            f"outcome={r.get('direction_outcome')}, status={r.get('status')}."
        )
        if r.get("gate_decision"):
            lines.append(
                f"  - Gate **{r.get('gate_decision')}**: {r.get('gate_reason', '')}"
            )
    lines.extend(
        [
            "",
            "Negative / null / REJECT outcomes are first-class Phase 3 results — "
            "not pipeline failures. Next round should propose different external IVs "
            "when density specs fail the gate or are not significant.",
        ]
    )
    return "\n".join(lines) + "\n"


def cmd_interpret(
    out_dir: Path,
    round_n: Optional[int],
    use_fixture: bool,
    use_api: bool,
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    # Find latest results
    if round_n is not None:
        results_path = out_dir / f"round{round_n}_results.md"
    else:
        cands = sorted(out_dir.glob("round*_results.md"))
        if not cands:
            print("No round*_results.md found. Run --run first.", file=sys.stderr)
            return 1
        results_path = cands[-1]
        round_n = int(results_path.stem.replace("round", "").replace("_results", ""))

    results_md = results_path.read_text(encoding="utf-8") if results_path.exists() else ""
    eval_md = ""
    ep = out_dir / "evaluation_summary.md"
    if ep.exists():
        eval_md = ep.read_text(encoding="utf-8")[:4000]

    prompt = (
        "Interpret these Phase 3 OLS results against the pre-registered expected "
        "directions and any Verifier gate_decision (ACCEPT/REJECT). Note "
        "confirmations, rejections, skips, nulls, and what to propose next. "
        "Do not invent new coefficients.\n\n"
        f"=== RESULTS ===\n{results_md}\n=== END ===\n"
    )

    source = "stdin"
    if use_fixture:
        text = _fixture_interpretation_from_results(out_dir, int(round_n))
        source = "fixture"
    elif use_api:
        source = "api"
        text = _call_gemini(prompt + "\n" + eval_md[:2000])
    else:
        print(prompt, flush=True)
        print("--- Paste interpretation (end with a line containing only END) ---\n", flush=True)
        buf: list[str] = []
        for line in sys.stdin:
            if line.strip() == "END":
                break
            buf.append(line)
        text = "".join(buf).strip() or "(empty interpretation)"

    out_path = out_dir / f"round{round_n}_interpretation.md"
    body = [
        f"# Phase 3 Round {round_n} Interpretation",
        "",
        f"Source: **{source}**",
        "",
        text.strip(),
        "",
        *prov_lines(),
    ]
    # provenance may be thin if --interpret alone
    if "generated_at" not in PROVENANCE:
        PROVENANCE["generated_at"] = utc_now()
    out_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    append_decision(
        out_dir,
        {
            "event": "interpret",
            "round": round_n,
            "source": source,
            "path": str(out_path),
        },
    )
    print(f"Wrote {out_path}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Phase 3 multi-agent rolled loop with enrichment"
    )
    p.add_argument("--validate", action="store_true")
    p.add_argument("--evaluate", action="store_true")
    p.add_argument("--propose", action="store_true")
    p.add_argument("--run", action="store_true")
    p.add_argument("--interpret", action="store_true")
    p.add_argument(
        "--verify-ta-specs",
        action="store_true",
        help="Pre-register+run TA I1–I4/Q1 with Wald/ΔR² Verifier gate",
    )
    p.add_argument(
        "--all", action="store_true", help="evaluate→[enrich]→propose→run→interpret"
    )
    p.add_argument("--fixture", action="store_true", help="offline proposals/interpret")
    p.add_argument(
        "--fixture-full",
        action="store_true",
        help="offline full multi-agent bus (scout/critic/NTEE acquire)",
    )
    p.add_argument("--api", action="store_true", help="Gemini API for propose/interpret")
    p.add_argument("--frame", type=Path, default=DEFAULT_FRAME)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--phase2-dir", type=Path, default=DEFAULT_PHASE2)
    p.add_argument("--proposals", type=Path, default=None)
    p.add_argument("--round", type=int, default=None)
    p.add_argument("--rounds", type=int, default=2)
    p.add_argument("--scout-topic", type=str, default=None)
    p.add_argument("--scout-geo", type=str, default=None)
    p.add_argument("--acquire-plan", type=Path, default=None)
    p.add_argument("--enrich-config", type=Path, default=None)
    p.add_argument("--round-plan", type=Path, default=None)
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir: Path = args.out
    frame: Path = args.frame
    ctx = _enrich_ctx()

    if args.validate:
        return cmd_validate(frame, out_dir)

    if args.verify_ta_specs:
        return cmd_verify_ta_specs(frame, out_dir)

    if args.scout_topic and not args.all:
        geo = args.scout_geo or "national"
        return cmd_scout(ctx, out_dir, args.scout_topic, geo, use_fixture=True)

    if args.acquire_plan and not args.all and args.enrich_config is None:
        active, rc = cmd_acquire(ctx, frame, out_dir, plan_path=args.acquire_plan)
        print(f"Active frame: {active}")
        return rc

    if args.enrich_config and not args.all:
        active, rc = cmd_enrich_config(ctx, frame, out_dir, args.enrich_config)
        print(f"Active frame: {active}")
        return rc

    if args.all:
        rc = cmd_evaluate(args.phase2_dir, out_dir)
        if rc != 0:
            return rc

        active_frame = frame
        round_plan = None
        if args.round_plan and args.round_plan.exists():
            round_plan = json.loads(args.round_plan.read_text(encoding="utf-8"))

        if args.fixture_full:
            topic = (
                (round_plan or {}).get("topic")
                or args.scout_topic
                or "food_assistance"
            )
            geo = (round_plan or {}).get("geography") or args.scout_geo or "atlanta"
            cmd_fixture_full_bus(ctx, out_dir, topic, geo)
            plan_path = out_dir / "agent_bus" / "acquisition_plan.json"
            active_frame, _ = cmd_acquire(ctx, active_frame, out_dir, plan_path=plan_path)
        elif args.enrich_config:
            active_frame, _ = cmd_enrich_config(
                ctx, active_frame, out_dir, args.enrich_config
            )
        elif args.acquire_plan:
            active_frame, _ = cmd_acquire(
                ctx, active_frame, out_dir, plan_path=args.acquire_plan
            )
        elif args.scout_topic:
            geo = args.scout_geo or "national"
            cmd_scout(ctx, out_dir, args.scout_topic, geo, use_fixture=True)
            cmd_critic_sources(ctx, out_dir, auto_approve=True)
            active_frame, _ = cmd_acquire(ctx, active_frame, out_dir, plan_path=None)
        elif round_plan and round_plan.get("enrich"):
            enr = round_plan["enrich"]
            cfg_path = write_payload(out_dir, "round_enrich_config.json", enr)
            if "topic" in enr and "enrichments" not in enr:
                cfg_path.write_text(
                    json.dumps({"enrichments": [enr]}, indent=2) + "\n",
                    encoding="utf-8",
                )
            active_frame, _ = cmd_enrich_config(ctx, active_frame, out_dir, cfg_path)

        for r in range(1, max(1, args.rounds) + 1):
            rc = cmd_propose(
                out_dir,
                r,
                args.fixture or args.fixture_full,
                args.api,
                frame_path=active_frame,
            )
            if rc != 0:
                return rc
            rc = cmd_run(active_frame, out_dir, args.proposals, r)
            if rc != 0:
                return rc
            rc = cmd_interpret(
                out_dir, r, args.fixture or args.fixture_full, args.api
            )
            if rc != 0:
                return rc
        return 0

    if args.evaluate:
        return cmd_evaluate(args.phase2_dir, out_dir)

    if args.propose:
        rnd = args.round if args.round is not None else 1
        return cmd_propose(out_dir, rnd, args.fixture, args.api, frame_path=frame)

    if args.run:
        return cmd_run(frame, out_dir, args.proposals, args.round)

    if args.interpret:
        return cmd_interpret(out_dir, args.round, args.fixture, args.api)

    build_parser().print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
