"""Geography × tax_year analysis slice (generalized from 12_build_analysis_slice)."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


def slice_frame(
    df: pd.DataFrame,
    geography_zips: Optional[list[str]] = None,
    tax_year: Optional[int] = None,
    prefer_state: Optional[str] = None,
    min_n: int = 100,
) -> tuple[pd.DataFrame, dict]:
    """
    Restrict frame to a cross-section.

    If tax_year is None, uses max tax_year on the frame.
    If geography_zips is None/empty, keeps all ZIPs (national).
    """
    out = df.copy()
    out["ZIP5"] = out["ZIP5"].astype(str).str.zfill(5).str[:5]
    meta: dict = {"min_n": min_n, "degraded": False, "warnings": []}

    if "tax_year" not in out.columns:
        raise ValueError("tax_year missing from frame")

    year = int(tax_year) if tax_year is not None else int(out["tax_year"].max())
    out = out[out["tax_year"] == year].copy()
    meta["tax_year"] = year

    if geography_zips:
        allow = {str(z).zfill(5)[:5] for z in geography_zips}
        out = out[out["ZIP5"].isin(allow)].copy()
        meta["n_zips_allow"] = len(allow)

    if prefer_state and "STATE" in out.columns:
        narrowed = out[out["STATE"] == prefer_state]
        if len(narrowed) >= min_n:
            out = narrowed
            meta["prefer_state"] = prefer_state

    meta["n_rows"] = len(out)
    meta["n_zips"] = int(out["ZIP5"].nunique()) if len(out) else 0

    if len(out) < min_n:
        meta["degraded"] = True
        meta["warnings"].append(
            f"slice n={len(out)} < {min_n}; caller should fall back to broader geography"
        )

    return out, meta
