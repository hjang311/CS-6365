"""Generic NTEE-code-based ZIP density from local IRS BMF."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def compute_ntee_density(
    bmf_path: Path,
    acs_path: Path,
    ntee_prefixes: list[str],
    geography_zips: Optional[list[str]] = None,
    label: str = "topic",
) -> pd.DataFrame:
    """
    Count nonprofits matching NTEE prefixes per ZIP, density per 10k population.

    Returns DataFrame: ZIP5, {label}_count, {label}_density, log_{label}_density
    """
    if not bmf_path.exists():
        raise FileNotFoundError(f"BMF not found: {bmf_path}")
    if not ntee_prefixes:
        raise ValueError("ntee_prefixes must be non-empty")

    bmf = pd.read_csv(bmf_path, dtype={"ZIP5": str, "NTEE_CD": str}, low_memory=False)
    bmf["ZIP5"] = bmf["ZIP5"].astype(str).str.replace(r"\D", "", regex=True).str.zfill(5).str[:5]
    bmf["NTEE_CD"] = bmf["NTEE_CD"].fillna("").astype(str)
    prefixes = tuple(p.strip().upper() for p in ntee_prefixes if p.strip())
    matched = bmf[bmf["NTEE_CD"].str.upper().str.startswith(prefixes)].copy()
    matched = matched[matched["ZIP5"].str.len() == 5]
    matched = matched[matched["ZIP5"] != "00000"]

    if geography_zips is not None:
        allow = {str(z).zfill(5)[:5] for z in geography_zips}
        matched = matched[matched["ZIP5"].isin(allow)]

    counts = (
        matched.groupby("ZIP5").size().reset_index(name=f"{label}_count")
        if len(matched)
        else pd.DataFrame(columns=["ZIP5", f"{label}_count"])
    )

    if acs_path.exists():
        acs = pd.read_csv(acs_path, dtype={"ZIP5": str})
        acs["ZIP5"] = acs["ZIP5"].astype(str).str.zfill(5).str[:5]
        acs["population"] = pd.to_numeric(acs.get("population"), errors="coerce")
        dens = acs[["ZIP5", "population"]].merge(counts, on="ZIP5", how="left")
        if geography_zips is not None:
            allow = {str(z).zfill(5)[:5] for z in geography_zips}
            dens = dens[dens["ZIP5"].isin(allow)].copy()
    else:
        dens = counts.copy()
        dens["population"] = np.nan

    dens[f"{label}_count"] = dens[f"{label}_count"].fillna(0).astype(int)
    dens[f"{label}_density"] = np.where(
        dens["population"] > 0,
        (dens[f"{label}_count"] / dens["population"]) * 10_000,
        0.0,
    )
    dens[f"log_{label}_density"] = np.log1p(dens[f"{label}_density"])
    return dens[["ZIP5", f"{label}_count", f"{label}_density", f"log_{label}_density"]].copy()
