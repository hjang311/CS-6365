"""Geography helpers: metro / allow-list ZIP resolution."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

# Heuristic ZIP3 prefixes when no allow-list CSV is available.
METRO_ZIP3: dict[str, list[str]] = {
    "atlanta": ["300", "301", "302", "303", "311"],
    "chicago": ["606", "607", "608"],
    "seattle": ["980", "981", "982"],
}

# Known allow-list filenames relative to Checkpoint 4/data/
METRO_ALLOWLIST: dict[str, str] = {
    "atlanta": "acfb_29_county_zips.csv",
}


def get_metro_zips(
    metro_name: str,
    acs_path: Optional[Path] = None,
    data_dir: Optional[Path] = None,
) -> list[str]:
    """
    Resolve a metro area name to ZIP5 codes.

    Preference order:
      1. Explicit allow-list CSV in data_dir (Atlanta ACFB-area list)
      2. ACS rows whose ZIP5 starts with known metro ZIP3 prefixes
      3. Empty list if unresolved (caller should degrade)
    """
    key = metro_name.strip().lower().replace(" ", "_")
    if key in ("national", "all", "usa", "us"):
        return []  # national = no filter

    if data_dir is not None:
        fname = METRO_ALLOWLIST.get(key)
        if fname:
            path = data_dir / fname
            if path.exists():
                zdf = pd.read_csv(path, dtype={"ZIP5": str})
                return sorted(
                    {
                        str(z).zfill(5)[:5]
                        for z in zdf["ZIP5"]
                        if str(z).zfill(5)[:5] not in ("00000", "00nan")
                    }
                )
        # Also try metro_name_zips.csv convention
        alt = data_dir / f"{key}_zips.csv"
        if alt.exists():
            zdf = pd.read_csv(alt, dtype={"ZIP5": str})
            col = "ZIP5" if "ZIP5" in zdf.columns else zdf.columns[0]
            return sorted({str(z).zfill(5)[:5] for z in zdf[col]})

    prefixes = METRO_ZIP3.get(key)
    if prefixes and acs_path is not None and acs_path.exists():
        acs = pd.read_csv(acs_path, dtype={"ZIP5": str}, usecols=["ZIP5"])
        acs["ZIP5"] = acs["ZIP5"].astype(str).str.zfill(5).str[:5]
        mask = acs["ZIP5"].str[:3].isin(prefixes)
        return sorted(acs.loc[mask, "ZIP5"].unique().tolist())

    if prefixes:
        # No ACS: return nothing usable; caller must not invent ZIPs
        return []

    return []
