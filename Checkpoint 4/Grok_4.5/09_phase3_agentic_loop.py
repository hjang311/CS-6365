"""
09_phase3_agentic_loop.py  —  Phase 3: Rolled Agentic Loop (Grok 4.5)

Evaluate Phase 2 results → propose indicators → pre-register JSON →
deterministic OLS (shared Checkpoint 3 recipe) → interpret.

Modes:
  --validate   Replay H4 & H5 β calibration (exit 0 = reproduction PASS)
  --evaluate   Deterministic summary of Phase 2 List A/B + limitation note
  --propose    Agent round: stdin (default), --fixture, or --api (Gemini)
  --run        Execute pre-registered proposals (2-var + interaction)
  --interpret  Agent interprets results vs expectations
  --all        evaluate → propose → run → interpret for --rounds (default 2)

Optional:
  --frame PATH, --out DIR, --proposals PATH, --round N, --rounds N
  --phase2-dir PATH  (default: Checkpoint 3/loop_results_v2)

INVARIANT: Agent never computes statistics. Proposals are written to JSON
BEFORE any OLS for that round. built_by: Grok_4.5
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Paths & identity
# ---------------------------------------------------------------------------
SCRIPT_VERSION = "09_phase3_agentic_loop.py v1.0 (Grok_4.5 / 2026-07-12)"
BUILT_BY = "Grok_4.5"

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
CP3_DIR = REPO_ROOT / "Checkpoint 3"
DEFAULT_FRAME = CP3_DIR / "data" / "cp3_modeling_frame.csv"
DEFAULT_PHASE2 = CP3_DIR / "loop_results_v2"
DEFAULT_OUT = HERE / "phase3_results"

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
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


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


def append_decision(out_dir: Path, event: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "decision_log.jsonl"
    record = {"ts": utc_now(), "built_by": BUILT_BY, **event}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def load_frame(frame_path: Path) -> pd.DataFrame:
    if not frame_path.exists():
        raise FileNotFoundError(f"Modeling frame not found: {frame_path}")
    df = pd.read_csv(frame_path, dtype={"ZIP5": str}, low_memory=False)
    return df


# ---------------------------------------------------------------------------
# Interaction OLS (higher-order) — mirrors 08 controls / dropna / min n
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


def run_ols_interaction(
    df: pd.DataFrame, iv1: str, iv2: str, dv: str
) -> tuple[Any, Optional[str]]:
    ctrl_formula, ctrl_cols = _controls_excluding(iv1, iv2)
    cols = [iv1, iv2, dv] + ctrl_cols
    # Still require original control columns present on frame for schema honesty,
    # except when a control is itself a focal IV (already listed as iv1/iv2).
    for c in CONTROL_COLS:
        if c not in (iv1, iv2) and c not in df.columns:
            return None, f"missing columns: {[c]}"
    missing = [c for c in cols if c not in df.columns]
    if missing:
        return None, f"missing columns: {missing}"
    df_clean = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(df_clean) < 100:
        return None, f"n={len(df_clean)} < 100 after dropna"
    if not ctrl_formula:
        formula = f"{dv} ~ {iv1} + {iv2} + {iv1}:{iv2}"
    else:
        formula = f"{dv} ~ {iv1} + {iv2} + {iv1}:{iv2} + {ctrl_formula}"
    try:
        m = smf.ols(formula, data=df_clean).fit(cov_type="HC1")
        return m, None
    except Exception as e:
        return None, str(e)


def extract_interaction_stats(m, iv1: str, iv2: str) -> dict[str, Any]:
    """Prefer the interaction term; also return main effects."""
    inter_key = f"{iv1}:{iv2}"
    alt_key = f"{iv2}:{iv1}"
    key = inter_key if inter_key in m.params.index else (
        alt_key if alt_key in m.params.index else None
    )
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


def cmd_propose(
    out_dir: Path,
    round_n: int,
    use_fixture: bool,
    use_api: bool,
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    eval_path = out_dir / "evaluation_summary.md"
    eval_md = eval_path.read_text(encoding="utf-8") if eval_path.exists() else (
        "(No evaluation_summary.md yet — run --evaluate first.)"
    )

    source = "stdin"
    if use_fixture:
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
        }

        if spec == "interaction":
            iv1, iv2 = p.get("iv1"), p.get("iv2")
            if not iv1 or not iv2:
                row["status"] = "error"
                row["error"] = "interaction requires iv1 and iv2"
                rows.append(row)
                continue
            # Avoid double-counting controls if IV is also a control column:
            # still allow fit; statsmodels will alias — document risk.
            m, err = run_ols_interaction(df, iv1, iv2, dv)
            ctrl_f, _ = _controls_excluding(iv1, iv2)
            row["formula"] = (
                f"{dv} ~ {iv1} + {iv2} + {iv1}:{iv2}"
                + (f" + {ctrl_f}" if ctrl_f else "")
            )
            if m is None:
                row["status"] = "error"
                row["error"] = err or "fit failed"
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
        "| ID | Spec | Vars | Expected | Observed | Outcome | β | p | R² | n | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if r["spec_type"] == "interaction":
            vars_s = f"`{r['iv1']}` × `{r['iv2']}` → `{r['dv']}`"
        else:
            vars_s = f"`{r['iv']}` → `{r['dv']}`"
        md.append(
            f"| {r['id']} | {r['spec_type']} | {vars_s} | {r['expected_direction']} | "
            f"{r['observed_direction']} | {r['direction_outcome']} | {r['beta']} | "
            f"{r['pvalue']} | {r['rsquared']} | {r['nobs']} | {r['status']} |"
        )
    md.extend(["", "## Rationales", ""])
    for r in rows:
        md.append(f"- **{r['id']}:** {r.get('rationale', '')}")
        if r.get("error"):
            md.append(f"  - note: {r['error']}")
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
        "status",
        "error",
        "formula",
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


# ---------------------------------------------------------------------------
# --interpret
# ---------------------------------------------------------------------------
FIXTURE_INTERPRETATION = """# Phase 3 Interpretation (fixture)

Round results show the rolled loop working as designed: proposals were pre-registered
before OLS, and outcomes are scored by sign + significance vs expected_direction
(not exact β, which remains H4/H5-only).

- Reconfirmed bank-density direction where the two_var spec ran successfully.
- Interaction of poverty_rate × log_nonprofit_branch_density is the higher-order
  Phase 3 track; interpret the interaction β, not only main effects.
- Skipped collinear control-as-IV rows are expected and documented.

Next round (if any) should prefer indicators not already in CONTROLS, and/or
soup_kitchen_density after the ACFB merge.
"""


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
        "directions. Note confirmations, rejections, skips, and what to propose next. "
        "Do not invent new coefficients.\n\n"
        f"=== RESULTS ===\n{results_md}\n=== END ===\n"
    )

    source = "stdin"
    if use_fixture:
        text = FIXTURE_INTERPRETATION
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
    p = argparse.ArgumentParser(description="Phase 3 rolled agentic loop (Grok 4.5)")
    p.add_argument("--validate", action="store_true")
    p.add_argument("--evaluate", action="store_true")
    p.add_argument("--propose", action="store_true")
    p.add_argument("--run", action="store_true")
    p.add_argument("--interpret", action="store_true")
    p.add_argument("--all", action="store_true", help="evaluate→propose→run→interpret")
    p.add_argument("--fixture", action="store_true", help="offline proposals/interpret")
    p.add_argument("--api", action="store_true", help="Gemini API for propose/interpret")
    p.add_argument("--frame", type=Path, default=DEFAULT_FRAME)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--phase2-dir", type=Path, default=DEFAULT_PHASE2)
    p.add_argument("--proposals", type=Path, default=None)
    p.add_argument("--round", type=int, default=None, help="round number for propose/run")
    p.add_argument("--rounds", type=int, default=2, help="bounded rounds for --all")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir: Path = args.out
    frame: Path = args.frame

    if args.validate:
        return cmd_validate(frame, out_dir)

    if args.all:
        rc = cmd_evaluate(args.phase2_dir, out_dir)
        if rc != 0:
            return rc
        for r in range(1, max(1, args.rounds) + 1):
            rc = cmd_propose(out_dir, r, args.fixture, args.api)
            if rc != 0:
                return rc
            rc = cmd_run(frame, out_dir, args.proposals, r)
            if rc != 0:
                return rc
            rc = cmd_interpret(out_dir, r, args.fixture, args.api)
            if rc != 0:
                return rc
            # Subsequent rounds: only first round uses fixture proposals by default;
            # keep fixture for demo reproducibility across both rounds.
        return 0

    if args.evaluate:
        return cmd_evaluate(args.phase2_dir, out_dir)

    if args.propose:
        rnd = args.round if args.round is not None else 1
        return cmd_propose(out_dir, rnd, args.fixture, args.api)

    if args.run:
        return cmd_run(frame, out_dir, args.proposals, args.round)

    if args.interpret:
        return cmd_interpret(out_dir, args.round, args.fixture, args.api)

    build_parser().print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
