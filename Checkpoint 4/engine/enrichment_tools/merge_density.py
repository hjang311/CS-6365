"""Merge density tables onto modeling frames; entity-table → density helper."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def entities_to_density(
    entities: pd.DataFrame,
    acs_path: Path,
    label: str,
    zip_col: str = "ZIP5",
) -> pd.DataFrame:
    """Aggregate an entity table (one row per site/org) to ZIP density per 10k."""
    df = entities.copy()
    if zip_col not in df.columns:
        # try common aliases
        for alt in ("zip", "Zip", "ZIP", "zipcode", "postal_code", "Zip Code"):
            if alt in df.columns:
                zip_col = alt
                break
        else:
            raise ValueError(f"No ZIP column found in entity table (cols={list(df.columns)})")

    df["ZIP5"] = (
        df[zip_col].astype(str).str.replace(r"\D", "", regex=True).str.zfill(5).str[:5]
    )
    df = df[df["ZIP5"].str.len() == 5]
    df = df[df["ZIP5"] != "00000"]
    counts = df.groupby("ZIP5").size().reset_index(name=f"{label}_count")

    if acs_path.exists():
        acs = pd.read_csv(acs_path, dtype={"ZIP5": str})
        acs["ZIP5"] = acs["ZIP5"].astype(str).str.zfill(5).str[:5]
        acs["population"] = pd.to_numeric(acs.get("population"), errors="coerce")
        dens = acs[["ZIP5", "population"]].merge(counts, on="ZIP5", how="right")
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
    return dens[["ZIP5", f"{label}_count", f"{label}_density", f"log_{label}_density"]]


def merge_density_into_frame(
    frame: pd.DataFrame,
    density_df: pd.DataFrame,
    label: str,
    fill_missing: float = 0.0,
) -> pd.DataFrame:
    """Left-join density columns onto the modeling frame by ZIP5."""
    out = frame.copy()
    out["ZIP5"] = out["ZIP5"].astype(str).str.zfill(5).str[:5]
    dens = density_df.copy()
    dens["ZIP5"] = dens["ZIP5"].astype(str).str.zfill(5).str[:5]

    drop_old = [
        c
        for c in out.columns
        if c in (f"{label}_count", f"{label}_density", f"log_{label}_density")
    ]
    if drop_old:
        out = out.drop(columns=drop_old)

    cols = ["ZIP5", f"{label}_count", f"{label}_density", f"log_{label}_density"]
    cols = [c for c in cols if c in dens.columns]
    out = out.merge(dens[cols], on="ZIP5", how="left")
    if f"{label}_count" in out.columns:
        out[f"{label}_count"] = out[f"{label}_count"].fillna(0).astype(int)
    if f"{label}_density" in out.columns:
        out[f"{label}_density"] = out[f"{label}_density"].fillna(fill_missing)
        out[f"log_{label}_density"] = np.log1p(out[f"{label}_density"])
    return out


def write_enriched_frame(
    frame: pd.DataFrame,
    out_path: Path,
) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out_path, index=False)
    return out_path
