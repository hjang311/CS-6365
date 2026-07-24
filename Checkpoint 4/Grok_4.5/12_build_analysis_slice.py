"""
12_build_analysis_slice.py  —  Atlanta / ACFB-area × latest tax_year slice (Grok 4.5)

Fixes the national multi-year join problem called out in DATA_GRANULARITY_AUDIT.md:
soup / Feed America sites are a ~2026 stock; analyze against tax_year == max only,
restricted to ACFB-area (or Atlanta pilot) ZIPs.

Writes:
  data/cp4_atlanta_xsection.csv
  data/slice_manifest.md
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REPO = HERE.parents[1]
BUILT_BY = "Grok_4.5"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--frame",
        type=Path,
        default=DATA / "cp4_frame_with_soup_density.csv",
        help="Frame already merged with soup density (run 11 first)",
    )
    ap.add_argument(
        "--fallback-frame",
        type=Path,
        default=REPO / "Checkpoint 3" / "data" / "cp3_modeling_frame.csv",
    )
    ap.add_argument(
        "--zips",
        type=Path,
        default=DATA / "acfb_29_county_zips.csv",
        help="Allow-list ZIPs (falls back to atlanta_pilot_zips.csv)",
    )
    ap.add_argument("--pilot-zips", type=Path, default=DATA / "atlanta_pilot_zips.csv")
    args = ap.parse_args()

    if args.frame.exists():
        df = pd.read_csv(args.frame, dtype={"ZIP5": str}, low_memory=False)
        frame_src = args.frame
    elif args.fallback_frame.exists():
        df = pd.read_csv(args.fallback_frame, dtype={"ZIP5": str}, low_memory=False)
        frame_src = args.fallback_frame
        print(f"WARN: using fallback frame without soup density: {frame_src}")
    else:
        raise SystemExit("No modeling frame found")

    df["ZIP5"] = df["ZIP5"].astype(str).str.zfill(5)
    if "tax_year" not in df.columns:
        raise SystemExit("tax_year missing from frame")

    max_year = int(df["tax_year"].max())
    zip_path = args.zips if args.zips.exists() else args.pilot_zips
    if not zip_path.exists():
        raise SystemExit(f"ZIP allow-list missing: {zip_path}")
    zdf = pd.read_csv(zip_path, dtype={"ZIP5": str})
    allow = {z for z in zdf["ZIP5"].astype(str).str.zfill(5) if z and z != "nan" and z != "00000"}

    slice_df = df[(df["tax_year"] == max_year) & (df["ZIP5"].isin(allow))].copy()

    # Prefer rows with STATE==GA when present
    if "STATE" in slice_df.columns:
        ga = slice_df[slice_df["STATE"] == "GA"]
        if len(ga) >= 100:
            slice_df = ga

    out = DATA / "cp4_atlanta_xsection.csv"
    DATA.mkdir(parents=True, exist_ok=True)
    slice_df.to_csv(out, index=False)

    n_nonzero = (
        int((slice_df["soup_kitchen_density"] > 0).sum())
        if "soup_kitchen_density" in slice_df.columns
        else 0
    )
    manifest = [
        "# Analysis slice manifest",
        "",
        f"- built_by: {BUILT_BY}",
        f"- source_frame: `{frame_src}`",
        f"- zip_allow_list: `{zip_path}` ({len(allow)} ZIPs)",
        f"- tax_year: **{max_year}** (cross-section; soup density is a ~2026 stock)",
        f"- rows: **{len(slice_df):,}**",
        f"- distinct ZIP5: **{slice_df['ZIP5'].nunique()}**",
        f"- rows with soup_kitchen_density > 0: **{n_nonzero}**",
        "",
        "## Rationale",
        "",
        "National multi-year OLS with 2026 site density is temporally and spatially",
        "misaligned (see DATA_GRANULARITY_AUDIT.md). This slice matches July 10 intent:",
        "Atlanta / ACFB-area geography and a single 990 year.",
        "",
    ]
    man_path = DATA / "slice_manifest.md"
    man_path.write_text("\n".join(manifest) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(slice_df):,} rows, tax_year={max_year}, ZIPs={slice_df['ZIP5'].nunique()})")
    print(f"Wrote {man_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
