# ACFB Soup-Kitchen / Pantry Acquisition Workflow

**Build:** Checkpoint 4 / `Grok_4.5/` (Grok 4.5)  
**Locator:** [https://www.acfb.org/get-help/food-map/](https://www.acfb.org/get-help/food-map/)  
**Goal:** Finer-granularity partner / food-assistance locations by ZIP → density per 10k residents → Phase 3 loop.

## Feasibility spike (2026-07-12)

| Finding | Detail |
|---------|--------|
| Public page | Interactive “food pantry map” with address + radius search |
| Embedded backend | Azure CDN **AccessFood** widget: `food-access-widget-cdn.azureedge.net/accessfood-widget/index.js?map=5ad1a3c8-675f-4c64-ad0a-1911f9a2bc67` |
| Documented bulk JSON API | **Not published** on the ACFB page |
| WordPress JSON | page metadata only — not the pantry inventory |
| SMS alternate | Text FINDFOOD / COMIDA to 888-976-2232 (3 nearest; not bulk) |

**Conclusion:** Do not scrape undocumented AccessFood endpoints without ACFB permission.

## Creative scale path (stretch — chosen)

Use **[Feed America research API](https://feedam.org/research)** (CC BY 4.0):

```text
GET https://feedam.org/api/resources/bulk?state=GA&type=food_pantry&limit=1000&page=N
```

Types pulled: `food_pantry`, `soup_kitchen`, `food_bank`, `mobile_pantry`.

**This is NOT the official ACFB ~700 partner census.** It is a licensed, attributable Georgia food-assistance directory that advances the professor’s ZIP-density track without ToS-violating scrapes. Supplement with the four publicly listed ACFB Community Food Centers.

Citation (required by CC BY 4.0): see `data/FEEDAM_ATTRIBUTION.txt`.

## ToS / ethics posture

1. Prefer open licensed research APIs (Feed America) over reverse-engineering AccessFood.
2. Prefer contacting ACFB partner-relations for an official research export if claiming “ACFB partners.”
3. Do **not** hammer the widget CDN.
4. Workflow documentation itself is a Checkpoint 4 deliverable.

## Commands

```bash
.venv/bin/python "Checkpoint 4/Grok_4.5/10_acquire_soup_kitchens.py" --feasibility
.venv/bin/python "Checkpoint 4/Grok_4.5/10_acquire_soup_kitchens.py" --pilot
.venv/bin/python "Checkpoint 4/Grok_4.5/10_acquire_soup_kitchens.py" --all-scale
# equivalent: --feedam-ga --acfb-cfcs --expand-zips --merge-sources
.venv/bin/python "Checkpoint 4/Grok_4.5/11_merge_soup_kitchen_density.py"
```

## Coverage log (stretch, 2026-07-12)

| Target | Status | Measured |
|--------|--------|----------|
| AccessFood full scrape | **Skipped** (ToS) | Widget ID documented only |
| Official ACFB ~700 partners | **Not obtained** | Would need ACFB export |
| Feed America GA pantry-class | **Done** | **2,250** raw rows → `feedam_ga_locations.csv` (**470** GA ZIPs) |
| ACFB CFCs (public pages) | **Done** | **4** sites (`acfb_cfcs.csv`) |
| Expanded ACFB-area ZIP allow-list | **Done** | **305** ZIPs (`acfb_29_county_zips.csv`) |
| Merged `soup_kitchens.csv` | **Done** | **1,432** agencies · **293** ZIPs · big=101 / local=1331 |
| Density merge | **Done** | 293 ZIP density rows; national frame 158,323×35; Atlanta pilot subsample 1,264; **ACFB-area subsample 2,593** |
| Phase 3 demos | **Done** | Round 2 fixture + soup demos national / ACFB-area (not significant; ACFB-area S01 p≈0.098) |

See also `data/coverage_report.md`.

## Schema (`soup_kitchens.csv`)

| Column | Description |
|--------|-------------|
| `name` | Agency / site name |
| `address` | Street / city |
| `ZIP5` | 5-digit ZIP |
| `agency_type` | pantry / soup_kitchen / cfc / food_bank / mobile_pantry / other |
| `parent_org_class` | `big` / `local` (heuristic keywords + CFC) |
| `county` | When known |
| `source` | URL or `feedam.org/research (CC BY 4.0)` |
| `retrieved_at` | ISO date |
| `notes` | Optional; Feed America rows note non-ACFB-official |

## July 10 alignment (granularity remediation)

See [`DATA_GRANULARITY_AUDIT.md`](DATA_GRANULARITY_AUDIT.md).

| Artifact | Role |
|----------|------|
| `prompts/PHASE3_ACFB_ZIP_COLLECT_PROMPT.md` | Agent ZIP→ACFB/public collect workflow |
| `data/acfb_zip_agent_collection.csv` | **317** sites / **41** pilot ZIPs (CFCs + curated + Feed America enrichment) |
| `data/acfb_zip_collection_log.md` | ToS + gap vs ~700 partners |
| `12_build_analysis_slice.py` | ACFB-area × tax_year=2022 → `cp4_atlanta_xsection.csv` (**583** rows) |
| `cp4_atlanta_pilot_xsection.csv` | Tighter pilot ZIP × 2022 (**272** rows) |
| `phase3_results/round_atlanta_xsection_results.md` | Hybrid retest on correct slice (nobs=211; not significant — honest) |

### Commands

```bash
.venv/bin/python "Checkpoint 4/Grok_4.5/10_acquire_soup_kitchens.py" --build-agent-collection --merge-agent-collection
.venv/bin/python "Checkpoint 4/Grok_4.5/11_merge_soup_kitchen_density.py"
.venv/bin/python "Checkpoint 4/Grok_4.5/12_build_analysis_slice.py"
```
