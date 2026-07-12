"""
08_unrolled_loop.py  —  Phase 2: Unrolled Deterministic Loop (Hybrid A+B)

Executes an explicit, pre-registered hypothesis agenda with deterministic OLS.
Does NOT invent new pairs mid-run (that is Phase 3).

Modes:
  --validate  Run H4 & H5 only; assert betas match baselines.
  --run       Execute List A (curated) + List B (bounded limitation harness);
              write loop_results_v2/ artifacts including the 2-var limitation note.

Optional flags:
  --frame PATH  Use an alternate modeling frame CSV (default: data/cp3_modeling_frame.csv)
  --out DIR     Write artifacts to an alternate directory (default: loop_results_v2/)

EXIT CODE SEMANTICS: exit 0 means the H4/H5 betas were REPRODUCED within
tolerance (coefficient match). It does NOT mean the hypotheses' theories were
confirmed — H5 passes validation while its competition theory is rejected
(observed positive beta). Theory outcomes are reported per-row in the artifacts.

Keep 07_deterministic_loop.py as a historical artifact (combinatorial batch).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

SCRIPT_VERSION = "08_unrolled_loop.py v2.1 (2026-07-12)"

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUTPUT_DIR = os.path.join(HERE, "loop_results_v2")
FRAME_PATH = os.path.join(DATA, "cp3_modeling_frame.csv")

# Columns the loop cannot run without (schema guard in load_frame).
REQUIRED_COLUMNS = [
    "fundraising_efficiency_w", "fundraising_efficiency", "log_fundraising_efficiency",
    "log_zhvi_2022", "log_nonprofit_branch_density",
    "total_revenue", "total_expenses", "total_contributions", "population",
    "log_total_revenue", "poverty_rate", "median_hh_income", "ntee_major", "region",
]

CONTROLS = "log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income"
CONTROL_COLS = [
    "log_total_revenue",
    "poverty_rate",
    "median_hh_income",
    "ntee_major",
    "region",
]

# Baselines from H4/H5 verification (must match within TOL)
H4_BASELINE_BETA = -7.91647
H5_BASELINE_BETA = 2.11963
BETA_TOL = 1e-3

IDENTIFIER_COLS = {
    "ein",
    "EIN",
    "ZIP5",
    "STATE",
    "NTEE_CD",
    "tax_year",
    "size_segment",
    "ntee_major",
    "region",
}

EFFICIENCY_VARS = {
    "fundraising_efficiency",
    "fundraising_efficiency_w",
    "log_fundraising_efficiency",
}

# DV = total_contributions / fundraising_expense_proxy.
# These IVs are mechanical components of that ratio — significant by construction, not discoveries.
MECHANICAL_IVS_FOR_EFFICIENCY_DV = {
    "total_contributions",  # numerator
    "fundraising_expense_proxy",  # denominator
    "fundraising_events_direct_expenses",  # component of proxy
    "professional_fundraising_fees",  # component of proxy
}

# Pairs that are definitional / near-identity (never put on the limitation harness)
BLOCKED_PAIRS = {
    ("total_revenue", "total_expenses"),
    ("total_expenses", "total_revenue"),
    ("total_contributions", "total_revenue"),
    ("total_revenue", "total_contributions"),
    ("fundraising_events_direct_expenses", "fundraising_expense_proxy"),
    ("fundraising_expense_proxy", "fundraising_events_direct_expenses"),
    ("professional_fundraising_fees", "fundraising_expense_proxy"),
    ("fundraising_expense_proxy", "professional_fundraising_fees"),
}

REDUNDANCY_GROUPS = {
    "total_revenue": ["total_revenue", "log_total_revenue"],
    "efficiency": [
        "fundraising_efficiency",
        "log_fundraising_efficiency",
        "fundraising_efficiency_w",
    ],
    "density": ["nonprofit_branch_density", "log_nonprofit_branch_density"],
    "zhvi": ["zhvi_2022", "log_zhvi_2022"],
    "bank": ["bank_branches", "bank_branch_density", "log_bank_branch_density"],
}

# ---------------------------------------------------------------------------
# List A — curated hypothesis agenda (theory-first, wraps Phase 1)
# ---------------------------------------------------------------------------
LIST_A: list[dict[str, Any]] = [
    {
        "id": "H4",
        "iv": "log_zhvi_2022",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "label": "Housing overhead (ZHVI)",
        "rationale_source": "Checkpoint 3/H4/H4_VERIFICATION_RUN.md",
        "role": "confirmatory",
        "baseline_beta": H4_BASELINE_BETA,
        "skip_if_missing": False,
    },
    {
        "id": "H5",
        "iv": "log_nonprofit_branch_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "label": "Provider density / competition",
        "rationale_source": "Checkpoint 3/H5/H5_VERIFICATION_RUN.md",
        "role": "confirmatory",
        "baseline_beta": H5_BASELINE_BETA,
        "skip_if_missing": False,
    },
    {
        "id": "H2_replay",
        "iv": "bank_branch_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "label": "Bank-branch density (CP2 H2 replay)",
        # CP2 found beta ~= -0.115 on h2_modeling_frame (different frame: year FE,
        # slightly different cleaning) — a QUALITATIVE reference only. We assert
        # direction, never the CP2 coefficient value, on the CP3 frame.
        "rationale_source": "Checkpoint 2/H2_Pipeline/findings_results.md (CP2 beta ~ -0.115, qualitative reference)",
        "role": "phase1_replay",
        "baseline_beta": None,  # intentionally no numeric assert (frames differ)
        "skip_if_missing": True,  # graceful on frames built before the FDIC merge in 02
    },
    {
        "id": "event_cost_drag",
        "iv": "fundraising_events_direct_expenses",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "label": "Mechanical denominator control: event fundraising expense",
        "rationale_source": "DV construction: event expense is part of fundraising_expense_proxy",
        "role": "mechanical_control",
        "baseline_beta": None,
        "skip_if_missing": False,
    },
    {
        "id": "affluence_clustering",
        "iv": "log_zhvi_2022",
        "dv": "log_nonprofit_branch_density",
        "expected_direction": "positive",
        "label": "Affluence clustering (secondary DV)",
        "rationale_source": "Geographic clustering context",
        "role": "exploratory",
        "baseline_beta": None,
        "skip_if_missing": False,
    },
    {
        "id": "identity_revenue_expenses",
        "iv": "total_expenses",
        "dv": "total_revenue",
        "expected_direction": "positive",
        "label": "Near-identity: expenses ~ revenue (NOT a discovery)",
        "rationale_source": "Accounting identity control case",
        "role": "identity_control",
        "baseline_beta": None,
        "skip_if_missing": False,
    },
    {
        "id": "weak_population",
        "iv": "population",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "none",
        "label": "Weak / diffuse: ZIP population → efficiency",
        "rationale_source": "Expected weak after controls; 2-var limitation case",
        "role": "weak_control",
        "baseline_beta": None,
        "skip_if_missing": False,
    },
]


# Provenance context — populated in main() after the frame is loaded, consumed
# by every artifact writer so outputs are traceable to a specific frame + run.
PROVENANCE: dict[str, str] = {}


def display_frame_path(frame_path: str) -> str:
    """Prefer a repo-relative path in artifacts (portable; no machine home prefix)."""
    abs_path = os.path.abspath(frame_path)
    repo_root = os.path.dirname(HERE)
    try:
        rel = os.path.relpath(abs_path, repo_root)
        if not rel.startswith(".."):
            return rel.replace("\\", "/")
    except ValueError:
        pass
    return abs_path


def set_provenance(frame_path: str, df: pd.DataFrame) -> None:
    PROVENANCE.update(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        frame=display_frame_path(frame_path),
        frame_shape=f"{df.shape[0]:,} rows x {df.shape[1]} cols",
        script=SCRIPT_VERSION,
    )


def prov_lines() -> list[str]:
    """Markdown-friendly provenance block."""
    return [
        "",
        "---",
        f"*Generated: {PROVENANCE.get('generated_at', '?')} · "
        f"Frame: `{PROVENANCE.get('frame', '?')}` ({PROVENANCE.get('frame_shape', '?')}) · "
        f"{PROVENANCE.get('script', '?')}*",
    ]


def get_redundancy_group(var: str) -> Optional[str]:
    for group_name, vars_list in REDUNDANCY_GROUPS.items():
        if var in vars_list:
            return group_name
    return None


def run_ols(df: pd.DataFrame, iv: str, dv: str):
    """Deterministic robust OLS with fixed controls (Phase 2 specialization)."""
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
    """Pull IV coefficient / p-value from fitted model."""
    if iv in m.params.index:
        key = iv
    else:
        # categorical fallback
        candidates = [k for k in m.params.index if k.startswith(f"C({iv})")]
        key = candidates[0] if candidates else None
    if key is None:
        return {"beta": float("nan"), "pvalue": float("nan"), "ci_low": float("nan"), "ci_high": float("nan")}
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
        # Limitation-harness rows carry no directional prior,
        # so "confirmed/rejected" language would be misleading.
        return "exploratory (no prior)"
    if expected == "none":
        return "n/a (no directional claim)"
    if observed == "none":
        return "not significant"
    return "confirmed" if expected == observed else "rejected (opposite or mismatch)"


def build_list_b(df: pd.DataFrame, max_ivs: int = 15) -> list[dict[str, Any]]:
    """
    Pre-register a DV-anchored filtered IV list (still an explicit list, not mid-run discovery).
    Primary DV = fundraising_efficiency_w.
    """
    primary_dv = "fundraising_efficiency_w"
    exclude = (
        set(IDENTIFIER_COLS)
        | set(CONTROL_COLS)
        | EFFICIENCY_VARS
        | MECHANICAL_IVS_FOR_EFFICIENCY_DV
        | {primary_dv}
    )

    candidates: list[str] = []
    for col in df.columns:
        if col in exclude:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue
        if (col, primary_dv) in BLOCKED_PAIRS or (primary_dv, col) in BLOCKED_PAIRS:
            continue
        # skip same redundancy group as DV
        if get_redundancy_group(col) == "efficiency":
            continue
        candidates.append(col)

    # Prefer theoretically external / structural IVs first, then fill.
    # Mechanical DV components are excluded above (not discoveries).
    # Log variants listed first so redundancy de-dup below keeps them.
    preferred_order = [
        "log_zhvi_2022",
        "log_nonprofit_branch_density",
        "log_bank_branch_density",
        "social_service_count",
        "population",
        "total_revenue",
        "total_expenses",
    ]
    ordered: list[str] = []
    for name in preferred_order:
        if name in candidates and name not in ordered:
            ordered.append(name)
    for name in sorted(candidates):
        if name not in ordered:
            ordered.append(name)

    # De-duplicate level/log variants: keep only the first member of each
    # redundancy group (log variants, given the ordering above).
    deduped: list[str] = []
    used_groups: set[str] = set()
    for name in ordered:
        group = get_redundancy_group(name)
        if group is not None:
            if group in used_groups:
                continue
            used_groups.add(group)
        deduped.append(name)

    ordered = deduped[:max_ivs]
    pairs = []
    for i, iv in enumerate(ordered, start=1):
        pairs.append(
            {
                "id": f"B{i:02d}",
                "iv": iv,
                "dv": primary_dv,
                "expected_direction": "unspecified",
                "label": f"Limitation harness: {iv} → {primary_dv}",
                "role": "limitation_harness",
            }
        )
    return pairs


def result_row(meta: dict[str, Any], m, err: Optional[str]) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": meta["id"],
        "list": meta.get("list_name", ""),
        "label": meta.get("label", ""),
        "role": meta.get("role", ""),
        "iv": meta["iv"],
        "dv": meta["dv"],
        "expected_direction": meta.get("expected_direction", "unspecified"),
        "rationale_source": meta.get("rationale_source", ""),
        "status": "ok",
        "n": None,
        "beta": None,
        "pvalue": None,
        "rsquared": None,
        "ci_low": None,
        "ci_high": None,
        "observed_direction": None,
        "direction_outcome": None,
        "significant": None,
        "error": None,
        "skipped": False,
        "skip_reason": None,
    }
    if err or m is None:
        if err:
            row["status"] = "error"
            row["error"] = err
        return row
    stats = extract_iv_stats(m, meta["iv"])
    row["n"] = int(m.nobs)
    row["beta"] = stats["beta"]
    row["pvalue"] = stats["pvalue"]
    row["rsquared"] = float(m.rsquared)
    row["ci_low"] = stats["ci_low"]
    row["ci_high"] = stats["ci_high"]
    row["significant"] = bool(stats["pvalue"] < 0.05)
    obs = observed_direction(stats["beta"], stats["pvalue"])
    row["observed_direction"] = obs
    if meta.get("role") == "mechanical_control":
        row["direction_outcome"] = "mechanical by construction (not a hypothesis)"
    elif meta.get("role") == "identity_control":
        row["direction_outcome"] = "near-identity control (not a hypothesis)"
    else:
        row["direction_outcome"] = direction_match(
            meta.get("expected_direction", "unspecified"), obs
        )
    return row


def execute_list(df: pd.DataFrame, items: list[dict[str, Any]], list_name: str) -> list[dict[str, Any]]:
    results = []
    for meta in items:
        meta = {**meta, "list_name": list_name}
        iv, dv = meta["iv"], meta["dv"]
        print(f"  [{list_name}] {meta['id']}: {dv} ~ {iv}")

        if meta.get("skip_if_missing") and iv not in df.columns:
            row = result_row(meta, None, None)
            row["status"] = "skipped"
            row["skipped"] = True
            row["skip_reason"] = (
                f"IV `{iv}` not in the modeling frame. This frame predates the FDIC merge — "
                "re-run `02_merge_pipeline.py` (with fdic_branches_by_zip.csv in data/) to "
                "enable the H2 replay. Original H2 run: Checkpoint 2/H2_Pipeline."
            )
            print(f"    SKIPPED: {row['skip_reason']}")
            results.append(row)
            continue

        if iv not in df.columns or dv not in df.columns:
            row = result_row(meta, None, f"missing iv/dv columns ({iv}, {dv})")
            print(f"    ERROR: {row['error']}")
            results.append(row)
            continue

        m, err = run_ols(df, iv, dv)
        row = result_row(meta, m, err)
        if err:
            print(f"    ERROR: {err}")
        else:
            print(
                f"    n={row['n']:,}  beta={row['beta']:.5f}  p={row['pvalue']:.4g}  "
                f"R2={row['rsquared']:.4f}  sig={row['significant']}"
            )
        results.append(row)
    return results


def write_markdown_table(path: str, title: str, intro: str, rows: list[dict[str, Any]]) -> None:
    lines = [f"# {title}", "", intro, ""]
    lines.append(
        "| ID | Role | IV → DV | Expected | Observed | Outcome | β | p | R² | n | Status |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        iv_dv = f"`{r['iv']}` → `{r['dv']}`"
        if r.get("skipped"):
            lines.append(
                f"| {r['id']} | {r['role']} | {iv_dv} | {r['expected_direction']} | — | — | — | — | — | — | skipped |"
            )
            continue
        if r["status"] != "ok":
            lines.append(
                f"| {r['id']} | {r['role']} | {iv_dv} | {r['expected_direction']} | — | — | — | — | — | — | error |"
            )
            continue
        lines.append(
            f"| {r['id']} | {r['role']} | {iv_dv} | {r['expected_direction']} | "
            f"{r['observed_direction']} | {r['direction_outcome']} | "
            f"{r['beta']:.5f} | {r['pvalue']:.4g} | {r['rsquared']:.4f} | {r['n']:,} | ok |"
        )
    # Skipped / error notes
    notes = [r for r in rows if r.get("skipped") or r.get("error")]
    if notes:
        lines.extend(["", "## Notes", ""])
        for r in notes:
            if r.get("skipped"):
                lines.append(f"- **{r['id']} skipped:** {r['skip_reason']}")
            elif r.get("error"):
                lines.append(f"- **{r['id']} error:** {r['error']}")
    # Rationale sources (List A rows carry provenance for each hypothesis)
    sourced = [r for r in rows if r.get("rationale_source")]
    if sourced:
        lines.extend(["", "## Rationale sources", ""])
        for r in sourced:
            lines.append(f"- **{r['id']}**: {r['rationale_source']}")
    lines.extend(prov_lines())
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_csv(path: str, rows: list[dict[str, Any]]) -> None:
    fields = [
        "list",
        "id",
        "role",
        "label",
        "iv",
        "dv",
        "expected_direction",
        "rationale_source",
        "observed_direction",
        "direction_outcome",
        "n",
        "beta",
        "pvalue",
        "rsquared",
        "ci_low",
        "ci_high",
        "significant",
        "status",
        "skipped",
        "skip_reason",
        "error",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        # Provenance as a comment line; readers can skip with pandas comment="#".
        f.write(f"# {PROVENANCE.get('generated_at', '?')} | {PROVENANCE.get('frame', '?')} | "
                f"{PROVENANCE.get('frame_shape', '?')} | {PROVENANCE.get('script', '?')}\n")
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_validation(path: str, list_a_rows: list[dict[str, Any]]) -> dict[str, str]:
    by_id = {r["id"]: r for r in list_a_rows}
    lines = [
        "# Phase 2 Validation Check (H4 & H5)",
        "",
        "Compares unrolled-loop List A confirmatory rows to known baselines.",
        "",
        "**PASS = beta REPRODUCTION** (coefficient matches baseline within tolerance).",
        "It does NOT mean the theory was confirmed — H5 passes validation while its",
        "competition theory is rejected (observed positive beta). See `list_a_results.md`",
        "for per-hypothesis theory outcomes.",
        "",
        "| Hypothesis | IV | Expected β | Loop β | |Δ| | Status |",
        "|---|---|---|---|---|---|",
    ]
    statuses: dict[str, str] = {}
    for hid, expected in [("H4", H4_BASELINE_BETA), ("H5", H5_BASELINE_BETA)]:
        r = by_id.get(hid)
        if not r or r["status"] != "ok":
            status = "FAIL"
            loop_beta = "N/A"
            delta = "N/A"
        else:
            loop_beta_f = float(r["beta"])
            delta_f = abs(loop_beta_f - expected)
            status = "PASS" if delta_f < BETA_TOL else "FAIL"
            loop_beta = f"{loop_beta_f:.5f}"
            delta = f"{delta_f:.6f}"
        statuses[hid] = status
        iv = r["iv"] if r else "?"
        lines.append(
            f"| {hid} | `{iv}` | `{expected:.5f}` | `{loop_beta}` | `{delta}` | **{status}** |"
        )
    lines.extend(prov_lines())
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return statuses


def write_two_var_limitation(
    path: str, list_a: list[dict[str, Any]], list_b: list[dict[str, Any]]
) -> None:
    b_ok = [r for r in list_b if r["status"] == "ok"]
    n_sig = sum(1 for r in b_ok if r["significant"])
    n_null = len(b_ok) - n_sig
    identity = [r for r in list_a if r.get("role") == "identity_control" and r["status"] == "ok"]
    weak = [r for r in list_a if r.get("role") == "weak_control" and r["status"] == "ok"]
    confirmatory = [r for r in list_a if r.get("role") == "confirmatory" and r["status"] == "ok"]
    event = [r for r in list_a if r.get("id") == "event_cost_drag" and r["status"] == "ok"]

    # Descriptive full-model R² range. This is not an incremental-R² estimate:
    # no controls-only model is fit, and IV-specific missingness can change n.
    r2_vals = [float(r["rsquared"]) for r in b_ok if r.get("rsquared") is not None]
    r2_min = min(r2_vals) if r2_vals else float("nan")
    r2_max = max(r2_vals) if r2_vals else float("nan")
    r2_span = (r2_max - r2_min) if r2_vals else float("nan")

    lines = [
        "# Two-Variable Correlation Limitation (Phase 2 Evaluation)",
        "",
        "**Important:** Limitation is *not* proven by “few significant p-values.”",
        "With n ≈ 100k+, tiny coefficients routinely clear p < 0.05. The professor’s point is that",
        "2-variable tests on this frame are **easy to light up and hard to trust as research** —",
        "mechanical hits, wrong-direction theory, and nearly indistinguishable full-model R².",
        "",
        "This note collects that evidence and motivates Phase 3 (new indicators / higher-order /",
        "finer data) without implementing Phase 3 yet.",
        "",
        "## Why “11 of 12 significant” would be the wrong headline",
        "",
        "An earlier draft of the List B harness included IVs that are **components of the DV**:",
        "",
        "`fundraising_efficiency = total_contributions / fundraising_expense_proxy`",
        "",
        "So `total_contributions`, `fundraising_expense_proxy`, event expenses, and professional fees",
        "are mechanically related to the DV. Calling those “discoveries” inflates the significant count",
        "and **looks like the opposite** of a limitation argument. The harness now excludes those mechanical IVs.",
        "",
        "Even after that filter, p < 0.05 is still common. That is expected at this sample size —",
        "and it is exactly why significance count alone cannot prove the method is “working well.”",
        "",
        "## Bounded limitation harness summary (non-mechanical candidate IVs)",
        "",
        f"- Pairs executed successfully: **{len(b_ok)}**",
        f"- Significant at p < 0.05: **{n_sig}**",
        f"- Not significant: **{n_null}**",
        f"- Model R² range across the harness: **{r2_min:.4f} – {r2_max:.4f}** (span ≈ {r2_span:.4f})",
        "",
        "The full-model R² values are nearly identical across the harness. This is descriptive,",
        "not a formal incremental-R² estimate: no controls-only model is reported, and",
        "IV-specific missingness changes n (notably for ZHVI).",
        "",
    ]
    if b_ok:
        lines.append("| ID | IV | β | p | R² | Significant? | Note |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in b_ok:
            note = ""
            if r["iv"] in ("population",):
                note = "tiny β; p cheap at large n"
            elif r["iv"] in ("total_revenue", "total_expenses"):
                note = "org-scale accounting; weak theory for efficiency"
            elif "zhvi" in r["iv"] or "density" in r["iv"] or r["iv"] == "social_service_count":
                note = "external/structural candidate"
            lines.append(
                f"| {r['id']} | `{r['iv']}` | {r['beta']:.5f} | {r['pvalue']:.4g} | "
                f"{r['rsquared']:.4f} | {r['significant']} | {note} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Evidence 1 — Mechanical / definitional hits (List A identity + DV recipe)",
            "",
        ]
    )
    if identity:
        for r in identity:
            lines.append(
                f"- **{r['id']}** (`{r['iv']}` → `{r['dv']}`): R² = **{r['rsquared']:.4f}**, "
                f"p = {r['pvalue']:.4g}. Near-accounting identity — not a sociological discovery."
            )
    if event:
        for r in event:
            lines.append(
                f"- **{r['id']}** (`{r['iv']}` → `{r['dv']}`): significant (β = {r['beta']:.5f}, "
                f"p = {r['pvalue']:.4g}) but the IV enters the **denominator** of fundraising efficiency. "
                "This is partly mechanical; keep it labeled, not as free discovery."
            )
    lines.append("")

    lines.extend(
        [
            "## Evidence 2 — Significance ≠ correct theory (H5)",
            "",
        ]
    )
    for r in confirmatory:
        lines.append(
            f"- **{r['id']}**: expected {r['expected_direction']}, observed {r['observed_direction']} "
            f"→ **{r['direction_outcome']}** (β = {r['beta']:.5f}, p = {r['pvalue']:.4g})."
        )
    lines.append(
        "- H5 is statistically significant **and** rejects the pre-registered competition story "
        "(positive agglomeration instead). A 2-var scanner that only counts p < 0.05 would call this a win."
    )
    lines.append("")

    lines.extend(["## Evidence 3 — Large-n makes tiny effects “significant”", ""])
    if weak:
        for r in weak:
            lines.append(
                f"- **{r['id']}** (`{r['iv']}` → `{r['dv']}`): β = {r['beta']:.5f}, "
                f"p = {r['pvalue']:.4g}, R² = {r['rsquared']:.4f}."
            )
            lines.append(
                "  The coefficient is economically tiny; with n > 100k it still clears p < 0.05. "
                "That shows how weak the “significant count” metric is for research quality."
            )
    else:
        lines.append("- (weak control did not run successfully)")
    lines.append("")

    lines.extend(
        [
            "## Evidence 4 — The frame is not a causal panel design",
            "",
            "- The frame pools 2018–2022 organization-year rows; repeated organizations are not independent observations.",
            "- The Phase 2 model has no tax-year fixed effects.",
            "- HC1 robust errors are not clustered by EIN or ZIP.",
            "- ACS controls and the December 2022 ZHVI snapshot are coarser in time and space than annual 990 records.",
            "- IRS headquarters ZIP may not represent every location where a nonprofit delivers services.",
            "",
            "These are intentional Phase 2 boundaries, not claims that the current coefficients are causal estimates.",
            "The professor's July 10 guidance was to document the two-variable limitation rather than over-refine it here.",
            "",
        ]
    )

    lines.extend(
        [
            "## Conclusion (what “2-var is limited” actually means)",
            "",
            "1. The unrolled loop can **faithfully replay** Phase 1 confirmatory tests (H4/H5).",
            "2. **Do not** argue limitation via “few significant results” — at this n, significance is cheap.",
            "3. Argue limitation via: mechanical DV-component hits, near-identity R²≈0.99, "
            "wrong-direction theory (H5), near-identical full-model R², pooled organization-years, "
            "unclustered HC1 errors, and coarse ZIP/year granularity.",
            "4. Therefore bivariate OLS on the current 990/ACS/ZHVI frame is a **useful Phase 2 harness**, "
            "not a finished research engine. Phase 3 should evaluate which links are *theoretically* "
            "meaningful, propose additional indicators, and (stretch) pursue finer-granularity data "
            "(e.g. soup-kitchen density by ZIP) or higher-order structure.",
            "",
            "*Phase 3 is intentionally not implemented in this deliverable.*",
            "",
        ]
    )
    lines.extend(prov_lines())
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_batch_summary_md(path: str, all_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 2 Unrolled Loop — Batch Summary",
        "",
        "All List A hypotheses + List B limitation-harness rows executed by `08_unrolled_loop.py`.",
        "",
        "| List | ID | IV | DV | β | p | R² | n | Sig | Status |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in all_rows:
        if r.get("skipped"):
            lines.append(
                f"| {r['list']} | {r['id']} | `{r['iv']}` | `{r['dv']}` | — | — | — | — | — | skipped |"
            )
        elif r["status"] != "ok":
            lines.append(
                f"| {r['list']} | {r['id']} | `{r['iv']}` | `{r['dv']}` | — | — | — | — | — | error |"
            )
        else:
            lines.append(
                f"| {r['list']} | {r['id']} | `{r['iv']}` | `{r['dv']}` | "
                f"{r['beta']:.5f} | {r['pvalue']:.4g} | {r['rsquared']:.4f} | {r['n']:,} | "
                f"{r['significant']} | ok |"
            )
    lines.extend(prov_lines())
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def load_frame(frame_path: str) -> pd.DataFrame:
    if not os.path.exists(frame_path):
        raise SystemExit(
            f"Missing modeling frame: {frame_path}\n"
            "Run `Checkpoint 3/02_merge_pipeline.py` first (see Checkpoint 3/README.md)."
        )
    df = pd.read_csv(frame_path, low_memory=False)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(
            f"Modeling frame is missing required columns: {missing}\n"
            "The frame likely predates the current merge recipe — re-run "
            "`Checkpoint 3/02_merge_pipeline.py` to regenerate it."
        )
    return df


def cmd_validate(df: pd.DataFrame, out_dir: str) -> int:
    os.makedirs(out_dir, exist_ok=True)
    print("=== Phase 2 Unrolled Loop: --validate (H4 & H5) ===")
    items = [h for h in LIST_A if h["id"] in ("H4", "H5")]
    rows = execute_list(df, items, "A")
    statuses = write_validation(os.path.join(out_dir, "validation_check.md"), rows)
    print(f"\nH4: {statuses.get('H4')}  H5: {statuses.get('H5')}")
    print("(PASS = beta reproduction within tolerance, not theory confirmation)")
    print(f"Wrote {os.path.join(out_dir, 'validation_check.md')}")
    return 0 if all(s == "PASS" for s in statuses.values()) else 1


def cmd_run(df: pd.DataFrame, out_dir: str) -> int:
    os.makedirs(out_dir, exist_ok=True)
    print("=== Phase 2 Unrolled Loop: --run (List A + limitation harness) ===")

    # List B is built once and written BEFORE OLS (pre-registered limitation harness)
    list_b_pairs = build_list_b(df, max_ivs=15)
    list_b_path = os.path.join(out_dir, "list_b_pairs.json")
    with open(list_b_path, "w", encoding="utf-8") as f:
        json.dump({"provenance": dict(PROVENANCE), "pairs": list_b_pairs}, f, indent=2)
    print(f"Pre-registered limitation harness ({len(list_b_pairs)} pairs) → {list_b_path}")

    print("\n--- List A: curated hypotheses ---")
    list_a_rows = execute_list(df, LIST_A, "A")

    print("\n--- List B: bounded two-variable limitation harness ---")
    list_b_rows = execute_list(df, list_b_pairs, "B")

    all_rows = list_a_rows + list_b_rows

    write_markdown_table(
        os.path.join(out_dir, "list_a_results.md"),
        "List A — Curated Hypothesis Agenda",
        "Theory-first hypotheses wrapping Phase 1 (H4/H5) plus labeled control cases.",
        list_a_rows,
    )
    write_markdown_table(
        os.path.join(out_dir, "list_b_results.md"),
        "List B — Bounded Two-Variable Limitation Harness",
        "This is not a discovery agenda. The primary DV is fixed to `fundraising_efficiency_w`; "
        "the IV list is pre-registered in `list_b_pairs.json` before OLS to demonstrate why "
        "large-n two-variable significance is insufficient. Level/log duplicates are removed.",
        list_b_rows,
    )
    write_csv(os.path.join(out_dir, "batch_summary.csv"), all_rows)
    write_batch_summary_md(os.path.join(out_dir, "batch_summary.md"), all_rows)
    statuses = write_validation(os.path.join(out_dir, "validation_check.md"), list_a_rows)
    write_two_var_limitation(
        os.path.join(out_dir, "two_variable_limitation.md"), list_a_rows, list_b_rows
    )

    # Light PoC summary (templated — no stdin approvals)
    summary_path = os.path.join(out_dir, "poc_summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Phase 2 PoC Summary (templated)\n\n")
        f.write("No per-pair agent approvals. This is a deterministic unrolled execution summary.\n\n")
        f.write("## List A vs expected directions\n\n")
        for r in list_a_rows:
            if r.get("skipped"):
                f.write(f"- **{r['id']}**: skipped — {r['skip_reason']}\n")
            elif r["status"] != "ok":
                f.write(f"- **{r['id']}**: error — {r['error']}\n")
            else:
                f.write(
                    f"- **{r['id']}** ({r['label']}): expected `{r['expected_direction']}`, "
                    f"observed `{r['observed_direction']}` → {r['direction_outcome']}\n"
                )
        b_ok = [r for r in list_b_rows if r["status"] == "ok"]
        n_sig = sum(1 for r in b_ok if r["significant"])
        f.write("\n## Limitation harness counts\n\n")
        f.write(f"- Executed: {len(b_ok)}\n")
        f.write(f"- Significant (p < 0.05): {n_sig}\n")
        f.write(f"- Null: {len(b_ok) - n_sig}\n")
        f.write("\nSee `two_variable_limitation.md` for the evaluation write-up.\n")
        f.write("\n".join(prov_lines()) + "\n")

    print("\n=== Outputs ===")
    for name in [
        "list_b_pairs.json",
        "list_a_results.md",
        "list_b_results.md",
        "batch_summary.csv",
        "batch_summary.md",
        "validation_check.md",
        "two_variable_limitation.md",
        "poc_summary.md",
    ]:
        print(f"  {os.path.join(out_dir, name)}")
    print(f"\nValidation: H4={statuses.get('H4')}  H5={statuses.get('H5')}")
    print("(exit 0 = H4/H5 beta reproduction PASS; theory outcomes are in the artifacts)")
    return 0 if all(s == "PASS" for s in statuses.values()) else 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phase 2 unrolled deterministic loop (Hybrid A+B)",
        epilog=(
            "Exit code 0 means H4/H5 betas were REPRODUCED within tolerance "
            "(coefficient match), not that the hypotheses' theories were confirmed. "
            "H5 passes validation while its competition theory is rejected."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--validate", action="store_true", help="H4/H5 baseline check only")
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute List A + the bounded limitation harness and write artifacts",
    )
    parser.add_argument("--frame", default=FRAME_PATH,
                        help=f"Path to modeling frame CSV (default: {FRAME_PATH})")
    parser.add_argument("--out", default=OUTPUT_DIR,
                        help=f"Output directory for artifacts (default: {OUTPUT_DIR})")
    args = parser.parse_args()

    df = load_frame(args.frame)
    set_provenance(args.frame, df)
    print(f"Loaded {args.frame}  shape={df.shape}")

    if args.validate:
        raise SystemExit(cmd_validate(df, args.out))
    raise SystemExit(cmd_run(df, args.out))


if __name__ == "__main__":
    main()
