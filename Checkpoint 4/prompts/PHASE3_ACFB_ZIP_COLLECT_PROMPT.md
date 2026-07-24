# Phase 3 — ACFB Atlanta ZIP Collection Prompt (Cursor / Antigravity)

*July 10 OH demo shape: “Give me all ZIPs of the Atlanta area → talk to the ACFB website → bring soup kitchens in these ZIPs.”*  
ToS-safe: **do not** scrape undocumented AccessFood JSON APIs. Use the public food-map UI, published CFC pages, and already-licensed Feed America rows as enrichment only.

**Repo root:** `/Users/hdj/Documents/CS-6365`

---

**Copy below:**

You are the NORP Phase 3 acquisition agent (Checkpoint 4 / Grok_4.5). Demonstrate the professor’s finer-granularity workflow. Do not ask for permission between steps. Do **not** reverse-engineer or bulk-scrape AccessFood private endpoints.

**Inputs:**
- ZIP list: `Checkpoint 4/Grok_4.5/data/atlanta_pilot_zips.csv` (Fulton/DeKalb core; expand with nearby metro ZIPs from `acfb_29_county_zips.csv` if needed, cap ~60 ZIPs for this run)
- Public ACFB pages: https://www.acfb.org/get-help/food-map/ and https://www.acfb.org/community-food-center/
- Optional enrichment (licensed): `Checkpoint 4/Grok_4.5/data/feedam_ga_locations.csv` filtered to the same ZIPs — tag `source` clearly

**Output CSV:** `Checkpoint 4/Grok_4.5/data/acfb_zip_agent_collection.csv`

Columns (exact):
`name,address,ZIP5,agency_type,parent_org_class,county,source,retrieved_at,notes,collection_method`

Rules:
1. `agency_type` ∈ {soup_kitchen, pantry, cfc, meal_site, food_bank, mobile_pantry, other}. Prefer labeling true meal/soup sites as `soup_kitchen` or `meal_site` when clear.
2. `parent_org_class` ∈ {big, local}. ACFB CFCs and national brands (Salvation Army, etc.) = big; independent = local.
3. `collection_method` ∈ {acfb_public_page, acfb_foodmap_manual, feedam_enrichment, curated_public_list}.
4. Include all 4 ACFB CFCs from the public CFC page.
5. For each pilot ZIP, attempt to record at least what is knowable from public pages / Feed America enrichment; if nothing found, skip (do not invent).
6. Write `Checkpoint 4/Grok_4.5/data/acfb_zip_collection_log.md` summarizing: ZIPs attempted, sites collected, ToS posture, remaining gaps vs official ~700 partners.

**Then run (do not compute OLS yourself):**
```bash
.venv/bin/python "Checkpoint 4/Grok_4.5/10_acquire_soup_kitchens.py" --merge-agent-collection
.venv/bin/python "Checkpoint 4/Grok_4.5/11_merge_soup_kitchen_density.py"
.venv/bin/python "Checkpoint 4/Grok_4.5/12_build_analysis_slice.py"
```

Return: row count, distinct ZIPs, path to CSV, and coverage vs Feed America-only proxy.
