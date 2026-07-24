"""
11_merge_soup_kitchen_density.py  —  ZIP soup-kitchen density merge (Grok 4.5)

Counts agencies in soup_kitchens.csv per ZIP5, computes density per 10k ACS
population (same recipe family as Checkpoint 3/02_merge_pipeline.py), left-joins
onto the modeling frame, and writes:

  data/soup_kitchen_density_by_zip.csv
  data/cp4_frame_with_soup_density.csv
  data/cp4_atlanta_subsample.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REPO_ROOT = HERE.parents[1]
DEFAULT_FRAME = REPO_ROOT / "Checkpoint 3" / "data" / "cp3_modeling_frame.csv"
ACS_PATH = REPO_ROOT / "Checkpoint 3" / "data" / "census_acs_by_zip.csv"
BUILT_BY = "Grok_4.5"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", type=Path, default=DEFAULT_FRAME)
    ap.add_argument("--soup", type=Path, default=DATA / "soup_kitchens.csv")
    ap.add_argument("--acs", type=Path, default=ACS_PATH)
    ap.add_argument("--pilot-zips", type=Path, default=DATA / "atlanta_pilot_zips.csv")
    args = ap.parse_args()

    if not args.soup.exists():
        raise SystemExit(f"Missing {args.soup}; run 10_acquire_soup_kitchens.py --pilot")
    if not args.frame.exists():
        raise SystemExit(f"Missing frame {args.frame}")

    soup = pd.read_csv(args.soup, dtype={"ZIP5": str})
    soup["ZIP5"] = soup["ZIP5"].str.zfill(5)
    counts = (
        soup.groupby("ZIP5")
        .size()
        .reset_index(name="soup_kitchen_count")
    )
    # True soup/meal sites only (July 10 wording)
    meal = soup[soup["agency_type"].isin(["soup_kitchen", "meal_site", "cfc"])]
    meal_counts = meal.groupby("ZIP5").size().reset_index(name="meal_site_count")

    # Big vs local counts for stretch analysis
    class_counts = (
        soup.groupby(["ZIP5", "parent_org_class"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    if "big" not in class_counts.columns:
        class_counts["big"] = 0
    if "local" not in class_counts.columns:
        class_counts["local"] = 0
    class_counts = class_counts.rename(
        columns={"big": "soup_kitchen_big_count", "local": "soup_kitchen_local_count"}
    )

    hours_agg = None
    if "has_hours" in soup.columns:
        soup["has_hours"] = pd.to_numeric(soup["has_hours"], errors="coerce").fillna(0)
        soup["open_days_approx"] = pd.to_numeric(
            soup.get("open_days_approx", 0), errors="coerce"
        ).fillna(0)
        hours_agg = soup.groupby("ZIP5", as_index=False).agg(
            sites_with_hours=("has_hours", "sum"),
            open_days_mean=("open_days_approx", "mean"),
        )

    if args.acs.exists():
        acs = pd.read_csv(args.acs, dtype={"ZIP5": str})
        acs["ZIP5"] = acs["ZIP5"].str.zfill(5)
        acs["population"] = pd.to_numeric(acs["population"], errors="coerce")
        dens = acs[["ZIP5", "population"]].merge(counts, on="ZIP5", how="right")
    else:
        frame_zip = pd.read_csv(
            args.frame, dtype={"ZIP5": str}, usecols=lambda c: c in ("ZIP5", "population")
        )
        frame_zip["ZIP5"] = frame_zip["ZIP5"].astype(str).str.zfill(5)
        pop = frame_zip.groupby("ZIP5", as_index=False)["population"].median()
        dens = pop.merge(counts, on="ZIP5", how="right")

    dens = dens.merge(class_counts, on="ZIP5", how="left")
    dens = dens.merge(meal_counts, on="ZIP5", how="left")
    if hours_agg is not None:
        dens = dens.merge(hours_agg, on="ZIP5", how="left")
        dens["sites_with_hours"] = dens["sites_with_hours"].fillna(0)
        dens["open_days_mean"] = dens["open_days_mean"].fillna(0)
    dens["meal_site_count"] = dens["meal_site_count"].fillna(0)
    dens["soup_kitchen_count"] = dens["soup_kitchen_count"].fillna(0)
    dens["soup_kitchen_density"] = np.where(
        dens["population"] > 0,
        (dens["soup_kitchen_count"] / dens["population"]) * 10_000,
        np.nan,
    )
    dens["meal_site_density"] = np.where(
        dens["population"] > 0,
        (dens["meal_site_count"] / dens["population"]) * 10_000,
        np.nan,
    )
    dens["log_soup_kitchen_density"] = np.log1p(dens["soup_kitchen_density"])
    dens["log_meal_site_density"] = np.log1p(dens["meal_site_density"].fillna(0))

    DATA.mkdir(parents=True, exist_ok=True)
    dens_path = DATA / "soup_kitchen_density_by_zip.csv"
    dens.to_csv(dens_path, index=False)

    df = pd.read_csv(args.frame, dtype={"ZIP5": str}, low_memory=False)
    df["ZIP5"] = df["ZIP5"].astype(str).str.zfill(5)
    drop_old = [
        c for c in df.columns
        if c.startswith("soup_kitchen_") or c.startswith("log_soup_")
        or c.startswith("meal_site") or c.startswith("log_meal_")
        or c in ("sites_with_hours", "open_days_mean")
    ]
    if drop_old:
        df = df.drop(columns=drop_old)
    merge_cols = [
        "ZIP5",
        "soup_kitchen_count",
        "soup_kitchen_density",
        "log_soup_kitchen_density",
        "soup_kitchen_big_count",
        "soup_kitchen_local_count",
        "meal_site_count",
        "meal_site_density",
        "log_meal_site_density",
        "sites_with_hours",
        "open_days_mean",
    ]
    merge_cols = [c for c in merge_cols if c in dens.columns]
    df = df.merge(dens[merge_cols], on="ZIP5", how="left")
    for c in (
        "soup_kitchen_count",
        "soup_kitchen_big_count",
        "soup_kitchen_local_count",
        "meal_site_count",
        "sites_with_hours",
    ):
        if c in df.columns:
            df[c] = df[c].fillna(0)
    if "soup_kitchen_density" in df.columns:
        df["soup_kitchen_density"] = df["soup_kitchen_density"].fillna(0.0)
        df["log_soup_kitchen_density"] = np.log1p(df["soup_kitchen_density"])
    if "meal_site_density" in df.columns:
        df["meal_site_density"] = df["meal_site_density"].fillna(0.0)
        df["log_meal_site_density"] = np.log1p(df["meal_site_density"])
    if "open_days_mean" in df.columns:
        df["open_days_mean"] = df["open_days_mean"].fillna(0.0)

    out_frame = DATA / "cp4_frame_with_soup_density.csv"
    df.to_csv(out_frame, index=False)

    if args.pilot_zips.exists():
        pilot = pd.read_csv(args.pilot_zips, dtype={"ZIP5": str})
        pilot_set = set(pilot["ZIP5"].astype(str).str.zfill(5))
        sub = df[df["ZIP5"].isin(pilot_set)].copy()
    else:
        sub = df[df["soup_kitchen_count"] > 0].copy()
    sub_path = DATA / "cp4_atlanta_subsample.csv"
    sub.to_csv(sub_path, index=False)

    # Broader ACFB-area subsample when expanded ZIP list exists
    expand_path = DATA / "acfb_29_county_zips.csv"
    if expand_path.exists():
        ez = pd.read_csv(expand_path, dtype={"ZIP5": str})
        ez_set = {z for z in ez["ZIP5"].astype(str).str.zfill(5) if z and z != "nan"}
        metro = df[df["ZIP5"].isin(ez_set)].copy()
        metro_path = DATA / "cp4_acfb_area_subsample.csv"
        metro.to_csv(metro_path, index=False)
        print(f"Wrote {metro_path} ({metro.shape[0]:,} ACFB-area rows)")

    n_pos = int((dens["soup_kitchen_count"] > 0).sum())
    print(f"Wrote {dens_path} ({len(dens)} ZIP rows; {n_pos} with agencies)")
    print(f"Wrote {out_frame} ({df.shape[0]:,} rows x {df.shape[1]} cols)")
    print(f"Wrote {sub_path} ({sub.shape[0]:,} Atlanta-pilot rows)")
    print(f"built_by={BUILT_BY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
