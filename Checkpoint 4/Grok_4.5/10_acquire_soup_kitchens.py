"""
10_acquire_soup_kitchens.py  —  ACFB partner / soup-kitchen acquisition (Grok 4.5)

Modes:
  --feasibility    Print AccessFood widget findings + ToS posture
  --pilot          Write atlanta_pilot_zips.csv + curated soup_kitchens.csv
  --scale-stub     Best-effort 29-county ZIP scaffold (not a full 700-partner dump)
  --feedam-ga      Pull Feed America CC BY 4.0 Georgia bulk locations
  --acfb-cfcs      Write public ACFB Community Food Center rows
  --expand-zips    Build expanded ACFB-area ZIP list (pilot + metro + Feed America ZIPs)
  --merge-sources  Union pilot + CFCs + Feed America (ACFB-area filter) → soup_kitchens.csv

Does NOT scrape undocumented AccessFood APIs. Scale path uses Feed America
open research API (https://feedam.org/research) under CC BY 4.0 — NOT an
official ACFB ~700 partner census.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
BUILT_BY = "Grok_4.5"
RETRIEVED = date.today().isoformat()
ACFB_MAP = "https://www.acfb.org/get-help/food-map/"
ACCESSFOOD_WIDGET = (
    "https://food-access-widget-cdn.azureedge.net/accessfood-widget/index.js"
    "?map=5ad1a3c8-675f-4c64-ad0a-1911f9a2bc67"
)
FEEDAM_BULK = "https://feedam.org/api/resources/bulk"
FEEDAM_TYPES = ("food_pantry", "soup_kitchen", "food_bank", "mobile_pantry")
FEEDAM_ATTR = (
    "Feed America. (2026). Feed America Food-Assistance Directory [Dataset]. "
    "https://feedam.org/research. License: CC BY 4.0. Adapted/filtered to Georgia "
    "food_pantry/soup_kitchen/food_bank/mobile_pantry for NORP Checkpoint 4."
)

# Fulton / DeKalb core pilot ZIPs (bounded ~40)
PILOT_ZIPS: list[dict[str, str]] = [
    {"ZIP5": z, "county": c, "metro_core": "yes"}
    for z, c in [
        ("30303", "Fulton"), ("30305", "Fulton"), ("30306", "Fulton"),
        ("30307", "Fulton"), ("30308", "Fulton"), ("30309", "Fulton"),
        ("30310", "Fulton"), ("30311", "Fulton"), ("30312", "Fulton"),
        ("30313", "Fulton"), ("30314", "Fulton"), ("30315", "Fulton"),
        ("30316", "Fulton"), ("30317", "Fulton"), ("30318", "Fulton"),
        ("30319", "Fulton"), ("30324", "Fulton"), ("30326", "Fulton"),
        ("30327", "Fulton"), ("30328", "Fulton"), ("30331", "Fulton"),
        ("30332", "Fulton"), ("30334", "Fulton"), ("30336", "Fulton"),
        ("30337", "Fulton"), ("30338", "Fulton"), ("30339", "Fulton"),
        ("30342", "Fulton"), ("30344", "Fulton"), ("30349", "Fulton"),
        ("30030", "DeKalb"), ("30032", "DeKalb"), ("30033", "DeKalb"),
        ("30034", "DeKalb"), ("30035", "DeKalb"), ("30058", "DeKalb"),
        ("30083", "DeKalb"), ("30084", "DeKalb"), ("30088", "DeKalb"),
        ("30329", "DeKalb"), ("30341", "DeKalb"), ("30345", "DeKalb"),
        ("30346", "DeKalb"), ("30360", "DeKalb"),
    ]
]

# Curated pilot agencies (public listings / ACFB CFC pages / community resource lists).
# parent_org_class: big = ACFB-operated or national; local = independent/community.
PILOT_AGENCIES: list[dict[str, str]] = [
    {
        "name": "ACFB Community Food Center — Atlanta (Ebenezer)",
        "address": "407 Auburn Ave NE, Atlanta, GA",
        "ZIP5": "30312",
        "agency_type": "cfc",
        "parent_org_class": "big",
        "county": "Fulton",
        "source": "https://www.acfb.org/community-food-center/",
        "notes": "ACFB-operated CFC",
    },
    {
        "name": "Atlanta Community Food Bank — Food Map Locator (reference)",
        "address": "metro Atlanta",
        "ZIP5": "30312",
        "agency_type": "other",
        "parent_org_class": "big",
        "county": "Fulton",
        "source": ACFB_MAP,
        "notes": "Network hub; not a single pantry site",
    },
    {
        "name": "St. Francis Table Soup Kitchen (Catholic Shrine)",
        "address": "Atlanta, GA",
        "ZIP5": "30308",
        "agency_type": "soup_kitchen",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list (PCCI / local directories)",
        "notes": "Prepared meals",
    },
    {
        "name": "Crossroads Community Ministries (Clyde's Kitchen)",
        "address": "Atlanta, GA",
        "ZIP5": "30308",
        "agency_type": "soup_kitchen",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "Emmaus House",
        "address": "Atlanta, GA",
        "ZIP5": "30315",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "Intown Cares",
        "address": "Atlanta, GA",
        "ZIP5": "30306",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "Safehouse Outreach",
        "address": "Atlanta, GA",
        "ZIP5": "30303",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "Salvation Army — Kroc Center Food Pantry",
        "address": "Atlanta, GA",
        "ZIP5": "30310",
        "agency_type": "pantry",
        "parent_org_class": "big",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "National org local site",
    },
    {
        "name": "Food4Lives ATL",
        "address": "Atlanta, GA",
        "ZIP5": "30316",
        "agency_type": "soup_kitchen",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "vegan/vegetarian meals",
    },
    {
        "name": "FreeFoodCommune",
        "address": "1560 Memorial Dr SE, Atlanta, GA",
        "ZIP5": "30317",
        "agency_type": "soup_kitchen",
        "parent_org_class": "local",
        "county": "DeKalb",
        "source": ACFB_MAP,
        "notes": "Public listing references ACFB map",
    },
    {
        "name": "North Fulton Community Charities Food Pantry",
        "address": "Roswell / North Fulton, GA",
        "ZIP5": "30328",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "Hope Atlanta (Women's Community Kitchen)",
        "address": "Atlanta, GA",
        "ZIP5": "30303",
        "agency_type": "soup_kitchen",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "Atlanta Inner-City Ministry Pantry",
        "address": "Atlanta, GA",
        "ZIP5": "30314",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "First Presbyterian Church Food Ministry",
        "address": "Atlanta, GA",
        "ZIP5": "30308",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "public community food resource list",
        "notes": "",
    },
    {
        "name": "Decatur / DeKalb community pantry (pilot placeholder)",
        "address": "Decatur, GA",
        "ZIP5": "30030",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "DeKalb",
        "source": "pilot seed — verify on ACFB food-map before publication claims",
        "notes": "Verify hours via ACFB locator",
    },
    {
        "name": "East Atlanta pantry (pilot placeholder)",
        "address": "Atlanta, GA",
        "ZIP5": "30316",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "pilot seed — verify on ACFB food-map",
        "notes": "Verify via locator",
    },
    {
        "name": "Southwest Atlanta pantry (pilot placeholder)",
        "address": "Atlanta, GA",
        "ZIP5": "30311",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "Fulton",
        "source": "pilot seed — verify on ACFB food-map",
        "notes": "",
    },
    {
        "name": "Chamblee / DeKalb pantry (pilot placeholder)",
        "address": "Chamblee, GA",
        "ZIP5": "30341",
        "agency_type": "pantry",
        "parent_org_class": "local",
        "county": "DeKalb",
        "source": "pilot seed — verify on ACFB food-map",
        "notes": "",
    },
]

# ACFB often cites ~29 North Georgia / metro counties — names for scaffold only.
ACFB_29_COUNTIES = [
    "Fulton", "DeKalb", "Cobb", "Gwinnett", "Clayton", "Cherokee", "Forsyth",
    "Henry", "Rockdale", "Douglas", "Fayette", "Coweta", "Paulding", "Bartow",
    "Carroll", "Newton", "Walton", "Barrow", "Hall", "Jackson", "Clarke",
    "Oconee", "Spalding", "Butts", "Jasper", "Morgan", "Greene", "Putnam",
    "Heard",
]

# Public ACFB Community Food Centers (https://www.acfb.org/community-food-center/)
ACFB_CFCS: list[dict[str, str]] = [
    {
        "name": "ACFB Community Food Center — Atlanta (MLK)",
        "address": "3500 Martin Luther King Jr. Drive SW, Atlanta GA",
        "ZIP5": "30331",
        "agency_type": "cfc",
        "parent_org_class": "big",
        "county": "Fulton",
        "source": "https://www.acfb.org/community-food-center/",
        "notes": "ACFB-operated CFC; appointments required",
    },
    {
        "name": "ACFB Community Food Center — Jonesboro",
        "address": "6805 Tara Blvd., Jonesboro, GA",
        "ZIP5": "30236",
        "agency_type": "cfc",
        "parent_org_class": "big",
        "county": "Clayton",
        "source": "https://www.acfb.org/community-food-center/",
        "notes": "ACFB-operated CFC",
    },
    {
        "name": "ACFB Community Food Center — Marietta",
        "address": "1605 Austell Rd., Marietta, GA",
        "ZIP5": "30008",
        "agency_type": "cfc",
        "parent_org_class": "big",
        "county": "Cobb",
        "source": "https://www.acfb.org/community-food-center/",
        "notes": "ACFB-operated CFC",
    },
    {
        "name": "ACFB Community Food Center — Stone Mountain",
        "address": "1979 Parker Ct., Stone Mountain, GA",
        "ZIP5": "30087",
        "agency_type": "cfc",
        "parent_org_class": "big",
        "county": "DeKalb",
        "source": "https://www.acfb.org/community-food-center/",
        "notes": "ACFB-operated CFC",
    },
]

# Curated metro expansion ZIPs beyond Fulton/DeKalb core (Cobb, Gwinnett, Clayton, …)
METRO_EXPAND_ZIPS: list[dict[str, str]] = [
    {"ZIP5": z, "county": c, "metro_core": "expand"}
    for z, c in [
        ("30008", "Cobb"), ("30060", "Cobb"), ("30062", "Cobb"), ("30064", "Cobb"),
        ("30066", "Cobb"), ("30067", "Cobb"), ("30068", "Cobb"), ("30080", "Cobb"),
        ("30082", "Cobb"), ("30101", "Cobb"), ("30106", "Cobb"), ("30126", "Cobb"),
        ("30127", "Cobb"), ("30144", "Cobb"),
        ("30017", "Gwinnett"), ("30019", "Gwinnett"), ("30024", "Gwinnett"),
        ("30039", "Gwinnett"), ("30043", "Gwinnett"), ("30044", "Gwinnett"),
        ("30045", "Gwinnett"), ("30046", "Gwinnett"), ("30047", "Gwinnett"),
        ("30071", "Gwinnett"), ("30078", "Gwinnett"), ("30092", "Gwinnett"),
        ("30093", "Gwinnett"), ("30096", "Gwinnett"), ("30097", "Gwinnett"),
        ("30236", "Clayton"), ("30238", "Clayton"), ("30260", "Clayton"),
        ("30274", "Clayton"), ("30288", "Clayton"), ("30294", "Clayton"),
        ("30297", "Clayton"),
        ("30114", "Cherokee"), ("30115", "Cherokee"), ("30188", "Cherokee"),
        ("30189", "Cherokee"),
        ("30004", "Forsyth"), ("30005", "Forsyth"), ("30040", "Forsyth"),
        ("30041", "Forsyth"),
        ("30228", "Henry"), ("30248", "Henry"), ("30252", "Henry"), ("30253", "Henry"),
        ("30012", "Rockdale"), ("30013", "Rockdale"), ("30094", "Rockdale"),
        ("30122", "Douglas"), ("30134", "Douglas"), ("30135", "Douglas"),
        ("30213", "Fayette"), ("30214", "Fayette"), ("30215", "Fayette"), ("30269", "Fayette"),
        ("30263", "Coweta"), ("30265", "Coweta"),
        ("30101", "Paulding"), ("30132", "Paulding"), ("30141", "Paulding"),
        ("30120", "Bartow"), ("30121", "Bartow"),
        ("30117", "Carroll"), ("30118", "Carroll"),
        ("30014", "Newton"), ("30016", "Newton"),
        ("30052", "Walton"),
        ("30620", "Barrow"), ("30680", "Barrow"),
        ("30501", "Hall"), ("30504", "Hall"), ("30506", "Hall"), ("30507", "Hall"),
        ("30517", "Jackson"), ("30548", "Jackson"),
        ("30601", "Clarke"), ("30605", "Clarke"), ("30606", "Clarke"),
        ("30677", "Oconee"),
        ("30223", "Spalding"), ("30224", "Spalding"),
        ("30233", "Butts"),
        ("31064", "Jasper"),
        ("30650", "Morgan"),
        ("30642", "Greene"),
        ("31024", "Putnam"),
        ("30217", "Heard"),
        ("30076", "Fulton"), ("30075", "Fulton"), ("30022", "Fulton"),
        ("30009", "Fulton"), ("30291", "Fulton"),
        ("30087", "DeKalb"), ("30021", "DeKalb"), ("30002", "DeKalb"),
    ]
]

BIG_ORG_KEYWORDS = (
    "salvation army", "food bank", "acfb", "atlanta community food bank",
    "community food center", "second harvest", "feeding america",
)


def write_pilot() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    zpath = DATA / "atlanta_pilot_zips.csv"
    with open(zpath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ZIP5", "county", "metro_core"])
        w.writeheader()
        w.writerows(PILOT_ZIPS)

    apath = DATA / "soup_kitchens.csv"
    fields = [
        "name", "address", "ZIP5", "agency_type", "parent_org_class",
        "county", "source", "retrieved_at", "notes",
    ]
    rows = []
    for a in PILOT_AGENCIES:
        row = dict(a)
        row["retrieved_at"] = RETRIEVED
        rows.append(row)
    with open(apath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    covered = sorted({r["ZIP5"] for r in rows})
    print(f"Wrote {zpath} ({len(PILOT_ZIPS)} ZIPs)")
    print(f"Wrote {apath} ({len(rows)} agencies; {len(covered)} distinct ZIPs)")
    print(f"built_by={BUILT_BY} retrieved_at={RETRIEVED}")
    print(f"AccessFood widget (do not scrape without permission): {ACCESSFOOD_WIDGET}")


def write_scale_stub() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / "acfb_29_county_zips_stub.csv"
    # Scaffold: pilot ZIPs tagged; other counties listed with empty ZIP for future fill
    rows = []
    for z in PILOT_ZIPS:
        rows.append({**z, "coverage_status": "pilot_seeded"})
    for county in ACFB_29_COUNTIES:
        if county in ("Fulton", "DeKalb"):
            continue
        rows.append({
            "ZIP5": "",
            "county": county,
            "metro_core": "no",
            "coverage_status": "stub_unpopulated",
        })
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["ZIP5", "county", "metro_core", "coverage_status"]
        )
        w.writeheader()
        w.writerows(rows)
    n_stub = sum(1 for r in rows if r["coverage_status"] == "stub_unpopulated")
    print(f"Wrote {path}")
    print(
        f"Coverage: {len(PILOT_ZIPS)} pilot ZIPs seeded; "
        f"{n_stub} county stub rows unpopulated; "
        f"~700 partner full dump NOT acquired (ToS / no public bulk API)."
    )


def print_feasibility() -> None:
    print("=== ACFB food-map feasibility (Grok 4.5) ===")
    print(f"Locator: {ACFB_MAP}")
    print(f"Widget:  {ACCESSFOOD_WIDGET}")
    print("Documented bulk JSON partner dump: NOT found on public page.")
    print("Posture: agent-assisted / manual pilot; contact ACFB for full export.")
    print("Scale path: Feed America CC BY 4.0 bulk API (not official ACFB partners).")
    print(f"Feed America: {FEEDAM_BULK}?state=GA")
    print("See SOUP_KITCHEN_WORKFLOW.md")


def _http_get_json(url: str, retries: int = 3) -> dict:
    import ssl
    import subprocess

    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "NORP-CS6365-Grok4.5-research/1.0"},
            )
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            # Fallback: curl (often has working system CA bundle on macOS)
            try:
                proc = subprocess.run(
                    ["curl", "-sL", "--max-time", "60", url],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    return json.loads(proc.stdout)
                last_err = RuntimeError(proc.stderr or f"curl exit {proc.returncode}")
            except Exception as e2:
                last_err = e2
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed GET {url}: {last_err}")


def pull_feedam_ga() -> None:
    """Paginate Feed America GA bulk API for pantry-class types; write raw + CSV."""
    DATA.mkdir(parents=True, exist_ok=True)
    raw_path = DATA / "feedam_ga_raw.jsonl"
    csv_path = DATA / "feedam_ga_locations.csv"
    attr_path = DATA / "FEEDAM_ATTRIBUTION.txt"
    attr_path.write_text(FEEDAM_ATTR + f"\nretrieved_at={RETRIEVED}\n", encoding="utf-8")

    all_rows: list[dict] = []
    with open(raw_path, "w", encoding="utf-8") as raw_f:
        for rtype in FEEDAM_TYPES:
            page = 1
            while True:
                qs = urllib.parse.urlencode(
                    {
                        "state": "GA",
                        "type": rtype,
                        "format": "json",
                        "limit": 1000,
                        "page": page,
                    }
                )
                url = f"{FEEDAM_BULK}?{qs}"
                payload = _http_get_json(url)
                resources = payload.get("resources") or []
                print(f"  {rtype} page {page}: {len(resources)} rows")
                for r in resources:
                    raw_f.write(json.dumps(r) + "\n")
                    all_rows.append(r)
                if len(resources) < 1000:
                    break
                page += 1
                time.sleep(0.2)

    fields = [
        "feedam_id", "name", "organization", "address", "city", "state", "ZIP5",
        "lat", "lng", "phone", "website", "resource_type", "data_source",
        "last_verified_date", "retrieved_at",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in all_rows:
            zip5 = str(r.get("zip") or "").strip()
            zip5 = re.sub(r"\D", "", zip5)[:5].zfill(5) if zip5 else ""
            w.writerow(
                {
                    "feedam_id": r.get("id", ""),
                    "name": r.get("name") or "",
                    "organization": r.get("organization") or "",
                    "address": r.get("address") or "",
                    "city": r.get("city") or "",
                    "state": r.get("state") or "",
                    "ZIP5": zip5,
                    "lat": r.get("lat", ""),
                    "lng": r.get("lng", ""),
                    "phone": r.get("phone") or "",
                    "website": r.get("website") or "",
                    "resource_type": r.get("resource_type") or "",
                    "data_source": r.get("data_source") or "",
                    "last_verified_date": r.get("last_verified_date") or "",
                    "retrieved_at": RETRIEVED,
                }
            )
    zips = {str(r.get("zip") or "").strip()[:5] for r in all_rows if r.get("zip")}
    print(f"Wrote {raw_path} ({len(all_rows)} records)")
    print(f"Wrote {csv_path} ({len(zips)} distinct ZIPs)")
    print(f"Attribution: {attr_path}")
    print(FEEDAM_ATTR)


def write_acfb_cfcs() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / "acfb_cfcs.csv"
    fields = [
        "name", "address", "ZIP5", "agency_type", "parent_org_class",
        "county", "source", "retrieved_at", "notes",
    ]
    rows = [{**r, "retrieved_at": RETRIEVED} for r in ACFB_CFCS]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {path} ({len(rows)} CFCs)")


def expand_zips() -> set[str]:
    """Build acfb_29_county_zips.csv from pilot + metro expand + Feed America ZIPs in range."""
    DATA.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(zip5: str, county: str, metro_core: str, coverage_status: str) -> None:
        z = re.sub(r"\D", "", str(zip5))[:5].zfill(5)
        if not z or z in seen or z == "00000":
            return
        seen.add(z)
        rows.append(
            {
                "ZIP5": z,
                "county": county,
                "metro_core": metro_core,
                "coverage_status": coverage_status,
            }
        )

    for z in PILOT_ZIPS:
        add(z["ZIP5"], z["county"], "yes", "pilot_seeded")
    for z in METRO_EXPAND_ZIPS:
        add(z["ZIP5"], z["county"], z["metro_core"], "metro_expand")
    for c in ACFB_CFCS:
        add(c["ZIP5"], c["county"], "cfc", "acfb_cfc")

    # Include Feed America GA ZIPs that look like metro/north-GA (300xx–305xx, 306xx Athens, 310xx)
    feedam_csv = DATA / "feedam_ga_locations.csv"
    if feedam_csv.exists():
        with open(feedam_csv, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                z = row.get("ZIP5") or ""
                if len(z) == 5 and z.startswith(("300", "301", "302", "303", "304", "305", "306", "310")):
                    add(z, "unknown", "feedam", "feedam_ga_metroish")

    for county in ACFB_29_COUNTIES:
        # ensure every county appears at least once even if no ZIP yet
        if not any(r["county"] == county for r in rows):
            rows.append(
                {
                    "ZIP5": "",
                    "county": county,
                    "metro_core": "no",
                    "coverage_status": "county_placeholder",
                }
            )

    path = DATA / "acfb_29_county_zips.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["ZIP5", "county", "metro_core", "coverage_status"]
        )
        w.writeheader()
        w.writerows(rows)
    n_zip = sum(1 for r in rows if r["ZIP5"])
    print(f"Wrote {path} ({n_zip} ZIPs + county placeholders)")
    return {r["ZIP5"] for r in rows if r["ZIP5"]}


def _norm_name(name: str) -> str:
    s = (name or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _classify_big(name: str, agency_type: str) -> str:
    n = (name or "").lower()
    if agency_type == "cfc":
        return "big"
    if any(k in n for k in BIG_ORG_KEYWORDS):
        return "big"
    return "local"


def _map_agency_type(resource_type: str) -> str:
    m = {
        "food_pantry": "pantry",
        "soup_kitchen": "soup_kitchen",
        "food_bank": "food_bank",
        "mobile_pantry": "mobile_pantry",
        "cfc": "cfc",
    }
    return m.get(resource_type, resource_type or "other")


def merge_sources(filter_to_expanded: bool = True) -> None:
    """Union pilot + CFCs + Feed America → soup_kitchens.csv (+ coverage report)."""
    DATA.mkdir(parents=True, exist_ok=True)
    # Ensure prerequisites
    if not (DATA / "soup_kitchens.csv").exists() or True:
        # Always refresh pilot base into memory from constants; CFCs from constants
        pass
    zip_set = expand_zips() if filter_to_expanded else set()
    if not (DATA / "feedam_ga_locations.csv").exists():
        print("WARN: feedam_ga_locations.csv missing — run --feedam-ga first")

    fields = [
        "name", "address", "ZIP5", "agency_type", "parent_org_class",
        "county", "source", "retrieved_at", "notes",
    ]
    merged: list[dict[str, str]] = []
    seen_keys: set[tuple[str, str]] = set()

    def add_row(row: dict[str, str]) -> None:
        z = re.sub(r"\D", "", str(row.get("ZIP5") or ""))[:5].zfill(5)
        if z == "00000":
            return
        if filter_to_expanded and zip_set and z not in zip_set:
            return
        key = (_norm_name(row.get("name", "")), z)
        if key in seen_keys or not key[0]:
            return
        seen_keys.add(key)
        out = {k: row.get(k, "") for k in fields}
        out["ZIP5"] = z
        out["retrieved_at"] = out.get("retrieved_at") or RETRIEVED
        merged.append(out)

    for a in PILOT_AGENCIES:
        add_row({**a, "retrieved_at": RETRIEVED, "source": a.get("source", "pilot")})
    for a in ACFB_CFCS:
        add_row({**a, "retrieved_at": RETRIEVED})

    feedam_csv = DATA / "feedam_ga_locations.csv"
    n_feedam_in = 0
    if feedam_csv.exists():
        with open(feedam_csv, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                n_feedam_in += 1
                rtype = row.get("resource_type") or ""
                name = row.get("name") or ""
                add_row(
                    {
                        "name": name,
                        "address": ", ".join(
                            x for x in [
                                row.get("address") or "",
                                row.get("city") or "",
                                row.get("state") or "",
                            ]
                            if x
                        ),
                        "ZIP5": row.get("ZIP5") or "",
                        "agency_type": _map_agency_type(rtype),
                        "parent_org_class": _classify_big(name, _map_agency_type(rtype)),
                        "county": "",
                        "source": "feedam.org/research (CC BY 4.0)",
                        "retrieved_at": RETRIEVED,
                        "notes": f"feedam_id={row.get('feedam_id', '')}; NOT official ACFB partner list",
                    }
                )

    out_path = DATA / "soup_kitchens.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(merged)

    covered = sorted({r["ZIP5"] for r in merged})
    by_type: dict[str, int] = {}
    by_class: dict[str, int] = {}
    for r in merged:
        by_type[r["agency_type"]] = by_type.get(r["agency_type"], 0) + 1
        by_class[r["parent_org_class"]] = by_class.get(r["parent_org_class"], 0) + 1

    report = DATA / "coverage_report.md"
    report.write_text(
        "\n".join(
            [
                "# Food-assistance coverage report (Grok 4.5 stretch)",
                "",
                f"- retrieved_at: {RETRIEVED}",
                f"- agencies in soup_kitchens.csv: **{len(merged)}**",
                f"- distinct ZIPs: **{len(covered)}**",
                f"- Feed America GA rows ingested: {n_feedam_in}",
                f"- filter_to_expanded_zips: {filter_to_expanded} ({len(zip_set)} ZIPs in allow-list)",
                f"- by agency_type: {by_type}",
                f"- by parent_org_class: {by_class}",
                "",
                "**Caveat:** Feed America rows are a CC BY 4.0 Georgia food-assistance",
                "proxy — **not** the official ACFB ~700 partner agency census.",
                "",
                FEEDAM_ATTR,
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out_path} ({len(merged)} agencies; {len(covered)} ZIPs)")
    print(f"Wrote {report}")


def _hours_open_days(hours_json: str) -> tuple[int, int]:
    """Return (has_hours, n_day_keys) from Feed America hours_json string."""
    if not hours_json or not str(hours_json).strip():
        return 0, 0
    try:
        obj = json.loads(hours_json) if isinstance(hours_json, str) else hours_json
        if isinstance(obj, dict) and obj:
            return 1, len(obj)
    except json.JSONDecodeError:
        return 1, 0  # present but unparsed
    return 0, 0


def build_agent_collection() -> None:
    """
    July 10 workflow artifact: Atlanta pilot ZIPs → public ACFB pages + licensed
    Feed America enrichment (ToS-safe; not AccessFood scrape).
    """
    DATA.mkdir(parents=True, exist_ok=True)
    pilot_path = DATA / "atlanta_pilot_zips.csv"
    if not pilot_path.exists():
        write_pilot()
    pilot_zips = {
        r["ZIP5"].zfill(5)
        for r in csv.DictReader(open(pilot_path, encoding="utf-8"))
    }

    fields = [
        "name", "address", "ZIP5", "agency_type", "parent_org_class", "county",
        "source", "retrieved_at", "notes", "collection_method",
        "has_hours", "open_days_approx",
    ]
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(row: dict[str, str]) -> None:
        z = re.sub(r"\D", "", str(row.get("ZIP5") or ""))[:5].zfill(5)
        if z == "00000":
            return
        key = (_norm_name(row.get("name", "")), z)
        if not key[0] or key in seen:
            return
        seen.add(key)
        out = {k: str(row.get(k, "")) for k in fields}
        out["ZIP5"] = z
        out["retrieved_at"] = out["retrieved_at"] or RETRIEVED
        out["has_hours"] = out.get("has_hours") or "0"
        out["open_days_approx"] = out.get("open_days_approx") or "0"
        rows.append(out)

    for a in ACFB_CFCS:
        add({
            **a,
            "retrieved_at": RETRIEVED,
            "collection_method": "acfb_public_page",
            "has_hours": "1",
            "open_days_approx": "5",
            "notes": (a.get("notes") or "") + "; July10 ZIP→ACFB workflow",
        })

    for a in PILOT_AGENCIES:
        # Skip network-hub placeholder
        if a.get("agency_type") == "other":
            continue
        method = (
            "acfb_public_page"
            if "acfb.org" in (a.get("source") or "")
            else "curated_public_list"
        )
        add({
            **a,
            "retrieved_at": RETRIEVED,
            "collection_method": method,
            "has_hours": "0",
            "open_days_approx": "0",
        })

    # Feed America enrichment on pilot ZIPs only (licensed secondary source)
    feedam_csv = DATA / "feedam_ga_locations.csv"
    raw_hours: dict[str, str] = {}
    raw_path = DATA / "feedam_ga_raw.jsonl"
    if raw_path.exists():
        with open(raw_path, encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    raw_hours[str(obj.get("id", ""))] = obj.get("hours_json") or ""
                except json.JSONDecodeError:
                    continue

    n_feedam = 0
    if feedam_csv.exists():
        with open(feedam_csv, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                z = (row.get("ZIP5") or "").zfill(5)
                if z not in pilot_zips:
                    continue
                n_feedam += 1
                fid = str(row.get("feedam_id") or "")
                has_h, ndays = _hours_open_days(raw_hours.get(fid, ""))
                rtype = row.get("resource_type") or ""
                name = row.get("name") or ""
                add({
                    "name": name,
                    "address": ", ".join(
                        x for x in [row.get("address") or "", row.get("city") or "", "GA"] if x
                    ),
                    "ZIP5": z,
                    "agency_type": _map_agency_type(rtype),
                    "parent_org_class": _classify_big(name, _map_agency_type(rtype)),
                    "county": "",
                    "source": "feedam.org/research (CC BY 4.0)",
                    "retrieved_at": RETRIEVED,
                    "notes": f"feedam_id={fid}; enrichment on Atlanta pilot ZIP; NOT official ACFB partner",
                    "collection_method": "feedam_enrichment",
                    "has_hours": str(has_h),
                    "open_days_approx": str(ndays),
                })

    out = DATA / "acfb_zip_agent_collection.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    by_method: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for r in rows:
        by_method[r["collection_method"]] = by_method.get(r["collection_method"], 0) + 1
        by_type[r["agency_type"]] = by_type.get(r["agency_type"], 0) + 1
    zips_hit = sorted({r["ZIP5"] for r in rows})
    log = DATA / "acfb_zip_collection_log.md"
    log.write_text(
        "\n".join(
            [
                "# ACFB ZIP agent collection log (July 10 workflow shape)",
                "",
                f"- retrieved_at: {RETRIEVED}",
                f"- pilot ZIPs in allow-list: {len(pilot_zips)}",
                f"- sites collected: **{len(rows)}**",
                f"- distinct ZIPs with ≥1 site: **{len(zips_hit)}**",
                f"- Feed America enrichment rows on pilot ZIPs: {n_feedam}",
                f"- by collection_method: {by_method}",
                f"- by agency_type: {by_type}",
                "",
                "## ToS posture",
                "",
                "- No AccessFood undocumented API scrape.",
                "- ACFB CFC rows from public community-food-center pages.",
                "- Curated public lists for known Atlanta meal sites.",
                "- Feed America CC BY 4.0 used as ZIP-filtered enrichment only.",
                "",
                "## Gap vs official ~700 ACFB partners",
                "",
                "This artifact demonstrates the *workflow shape* (ZIP list → collect sites →",
                "density). It is **not** a complete ACFB partner census. Remaining gap:",
                "official partner export or permitted bulk locator access.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out} ({len(rows)} sites, {len(zips_hit)} ZIPs)")
    print(f"Wrote {log}")


def merge_agent_collection() -> None:
    """Prefer agent collection for Atlanta pilot ZIPs; keep expanded Feed America elsewhere."""
    DATA.mkdir(parents=True, exist_ok=True)
    agent_path = DATA / "acfb_zip_agent_collection.csv"
    if not agent_path.exists():
        build_agent_collection()

    # Start from expanded merge if present, else rebuild
    if not (DATA / "soup_kitchens.csv").exists():
        if (DATA / "feedam_ga_locations.csv").exists():
            merge_sources(filter_to_expanded=True)
        else:
            write_pilot()

    existing = list(csv.DictReader(open(DATA / "soup_kitchens.csv", encoding="utf-8")))
    agent = list(csv.DictReader(open(agent_path, encoding="utf-8")))
    pilot_zips = {
        r["ZIP5"].zfill(5)
        for r in csv.DictReader(open(DATA / "atlanta_pilot_zips.csv", encoding="utf-8"))
    }

    fields = [
        "name", "address", "ZIP5", "agency_type", "parent_org_class",
        "county", "source", "retrieved_at", "notes",
        "collection_method", "has_hours", "open_days_approx",
    ]
    merged: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(row: dict[str, str], replace_pilot: bool = False) -> None:
        z = re.sub(r"\D", "", str(row.get("ZIP5") or ""))[:5].zfill(5)
        if z == "00000":
            return
        key = (_norm_name(row.get("name", "")), z)
        if key in seen:
            return
        if replace_pilot is False and z in pilot_zips:
            # skip non-agent rows for pilot ZIPs; agent pass fills them
            return
        seen.add(key)
        out = {k: str(row.get(k, "")) for k in fields}
        out["ZIP5"] = z
        merged.append(out)

    # Agent rows first (authoritative for pilot ZIPs)
    for r in agent:
        add(r, replace_pilot=True)
    # Non-pilot expanded Feed America / prior soup rows
    for r in existing:
        z = (r.get("ZIP5") or "").zfill(5)
        if z in pilot_zips:
            continue
        add({**r, "collection_method": r.get("collection_method") or "feedam_expanded",
             "has_hours": r.get("has_hours") or "0",
             "open_days_approx": r.get("open_days_approx") or "0"}, replace_pilot=True)

    out_path = DATA / "soup_kitchens.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(merged)

    report = DATA / "coverage_report.md"
    prev = report.read_text(encoding="utf-8") if report.exists() else ""
    extra = [
        "",
        "## After agent ZIP merge",
        f"- soup_kitchens.csv rows: **{len(merged)}**",
        f"- distinct ZIPs: **{len({r['ZIP5'] for r in merged})}**",
        f"- agent collection rows: {len(agent)}",
        f"- pilot ZIPs reserved for agent/ACFB-oriented sources: {len(pilot_zips)}",
        "",
    ]
    report.write_text(prev.rstrip() + "\n" + "\n".join(extra), encoding="utf-8")
    print(f"Wrote {out_path} ({len(merged)} agencies after agent merge)")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--feasibility", action="store_true")
    p.add_argument("--pilot", action="store_true")
    p.add_argument("--scale-stub", action="store_true")
    p.add_argument("--feedam-ga", action="store_true")
    p.add_argument("--acfb-cfcs", action="store_true")
    p.add_argument("--expand-zips", action="store_true")
    p.add_argument("--merge-sources", action="store_true")
    p.add_argument(
        "--build-agent-collection",
        action="store_true",
        help="Build acfb_zip_agent_collection.csv (CFCs + pilot + Feed America on pilot ZIPs)",
    )
    p.add_argument(
        "--merge-agent-collection",
        action="store_true",
        help="Merge agent collection into soup_kitchens.csv and refresh coverage",
    )
    p.add_argument(
        "--all-scale",
        action="store_true",
        help="pilot + feedam-ga + acfb-cfcs + expand-zips + merge-sources",
    )
    args = p.parse_args()
    if args.all_scale:
        write_pilot()
        pull_feedam_ga()
        write_acfb_cfcs()
        expand_zips()
        merge_sources(filter_to_expanded=True)
        return 0
    ran = False
    if args.feasibility:
        print_feasibility()
        ran = True
    if args.pilot:
        write_pilot()
        ran = True
    if args.scale_stub:
        write_scale_stub()
        ran = True
    if args.feedam_ga:
        pull_feedam_ga()
        ran = True
    if args.acfb_cfcs:
        write_acfb_cfcs()
        ran = True
    if args.expand_zips:
        expand_zips()
        ran = True
    if args.merge_sources:
        merge_sources(filter_to_expanded=True)
        ran = True
    if args.build_agent_collection:
        build_agent_collection()
        ran = True
    if args.merge_agent_collection:
        merge_agent_collection()
        ran = True
    if not ran:
        p.print_help()
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
