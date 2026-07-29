"""Direct HTTPS download of CSV/JSON/GeoJSON entity tables with a ZIP column."""
from __future__ import annotations

import csv
import json
import ssl
import subprocess
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd


ZIP_ALIASES = (
    "ZIP5",
    "zip",
    "Zip",
    "ZIP",
    "zipcode",
    "postal_code",
    "Zip Code",
    "zip_code",
    "POSTAL",
    "postal",
)


def _get_bytes(url: str, timeout: int = 90) -> bytes:
    if not url.startswith("https://"):
        raise ValueError("web_download requires HTTPS URL")
    req = urllib.request.Request(
        url, headers={"User-Agent": "NORP-CS6365-Phase3-research/1.0"}
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read()
    except Exception:
        proc = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), url],
            capture_output=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout:
            return proc.stdout
        raise RuntimeError(f"Failed to download {url}")


def _normalize_zip_series(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
        .str.replace(r"\D", "", regex=True)
        .str.zfill(5)
        .str[:5]
    )


def web_download_entities(
    url: str,
    out_dir: Path,
    label: str = "topic",
    format_hint: str | None = None,
    attribution_text: str = "",
) -> tuple[Path, dict[str, Any]]:
    """
    Download a machine-readable file and write a normalized entity CSV with ZIP5.

    Supports CSV, JSON array, JSON {features: GeoJSON}, or dict-with-list.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_bytes = _get_bytes(url)
    raw_path = out_dir / f"{label}_web_raw.bin"
    raw_path.write_bytes(raw_bytes)

    fmt = (format_hint or "").lower()
    if not fmt:
        lower = url.lower().split("?")[0]
        if lower.endswith(".csv"):
            fmt = "csv"
        elif lower.endswith(".geojson") or lower.endswith(".json"):
            fmt = "json"
        else:
            # sniff
            head = raw_bytes[:200].lstrip()
            fmt = "json" if head.startswith(b"{") or head.startswith(b"[") else "csv"

    if fmt == "csv":
        text = raw_bytes.decode("utf-8", errors="replace")
        tmp = out_dir / f"{label}_web_raw.csv"
        tmp.write_text(text, encoding="utf-8")
        df = pd.read_csv(tmp, low_memory=False)
    else:
        data = json.loads(raw_bytes.decode("utf-8"))
        if isinstance(data, list):
            df = pd.json_normalize(data)
        elif isinstance(data, dict) and "features" in data:
            # GeoJSON
            props = []
            for feat in data["features"]:
                row = dict(feat.get("properties") or {})
                geom = feat.get("geometry") or {}
                if geom.get("type") == "Point" and geom.get("coordinates"):
                    row["_lon"], row["_lat"] = geom["coordinates"][0], geom["coordinates"][1]
                props.append(row)
            df = pd.DataFrame(props)
        elif isinstance(data, dict):
            # find first list-of-dicts value
            for v in data.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    df = pd.json_normalize(v)
                    break
            else:
                df = pd.json_normalize(data)
        else:
            raise ValueError("Unsupported JSON structure for web_download")

    zip_col = None
    for cand in ZIP_ALIASES:
        if cand in df.columns:
            zip_col = cand
            break
    if zip_col is None:
        raise ValueError(
            f"Downloaded table has no ZIP column. Columns={list(df.columns)[:30]}"
        )

    df["ZIP5"] = _normalize_zip_series(df[zip_col])
    df = df[df["ZIP5"].str.len() == 5]
    df = df[df["ZIP5"] != "00000"]

    csv_path = out_dir / f"{label}_web_entities.csv"
    df.to_csv(csv_path, index=False)

    attr_path = out_dir / f"{label}_ATTRIBUTION.txt"
    attr_path.write_text(
        (attribution_text or f"Downloaded from {url}") + "\n",
        encoding="utf-8",
    )

    meta = {
        "adapter": "web_download",
        "url": url,
        "n_records": len(df),
        "csv_path": str(csv_path),
        "raw_path": str(raw_path),
        "attribution_path": str(attr_path),
        "zip_column": zip_col,
    }
    if len(df) == 0:
        raise RuntimeError(f"web_download produced 0 rows with valid ZIP5 from {url}")
    return csv_path, meta


def load_manual_entities(csv_path: Path) -> pd.DataFrame:
    """Load a human/IDE-collected entity CSV (manual_hybrid lane)."""
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)
    df = pd.read_csv(csv_path, low_memory=False)
    zip_col = None
    for cand in ZIP_ALIASES:
        if cand in df.columns:
            zip_col = cand
            break
    if zip_col is None:
        raise ValueError(f"manual entity CSV missing ZIP column: {csv_path}")
    df["ZIP5"] = _normalize_zip_series(df[zip_col])
    return df
