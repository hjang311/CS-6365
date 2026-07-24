# Data Time & Space Granularity Audit (Grok 4.5)

**Date:** 2026-07-12  
**Scope:** Checkpoint 3 modeling frame + Checkpoint 4 / `Grok_4.5/` food-assistance stretch  
**Authority:** Professor July 10 OH notes (`Project Research & Initial Plan/July 10th OH Notes.pdf`)

## July 10 diagnosis (paraphrased)

> Datasets have severe **time and space** granularity problems. Census publishes ZIP/county and is coarse in time (~decade-scale estimates) versus 990s every year. 990s only give **headquarters** addresses, not where nonprofits actually operate branches. ACFB-style soup-kitchen lists are an example of **finer-granularity** data that workflows can collect: *give me Atlanta ZIPs → talk to the ACFB site/MCP → bring soup kitchens in those ZIPs → density per ZIP → correlate; compare big vs local.*

## Measured inventory

| Dataset | Rows | Spatial grain | Temporal grain | Notes |
|---------|------|---------------|----------------|-------|
| `cp3_modeling_frame.csv` | 158,323 | Org **HQ ZIP5** (12,056 ZIPs, 55 states) | Org-**year** 2018–2022 | 50,928 unique EINs; pooled repeats |
| ACS on frame | — | ZIP | Static multi-year estimate on every tax_year | Treated as constant 2018–22 |
| ZHVI | — | ZIP | **Dec 2022 snapshot** | Same IV on 2018 rows |
| NTEE `nonprofit_branch_density` | — | HQ ZIP NTEE counts | Static on frame | Coarse “service presence” proxy |
| Feed America GA (`feedam_ga_locations.csv`) | 2,250 | Street → ZIP (470 ZIPs) | Verified mostly **2026-01 / 2026-04** | CC BY 4.0; not official ACFB partners |
| Merged `soup_kitchens.csv` | 1,432 | ZIP (293) | Snapshot `retrieved_at=2026-07-12` | Types: pantry 1263, soup_kitchen **23**, … |
| Density on national frame | — | ZIP left-join | 2026 stock on 2018–22 rows | **1.47%** rows have density &gt; 0 |

### Tax-year split (990)

| Year | Rows |
|------|------|
| 2018 | 34,842 |
| 2019 | 35,848 |
| 2020 | 26,883 |
| 2021 | 27,042 |
| 2022 | 33,708 |

## Time granularity — FAIL (severe mismatch)

Joining a **2026** food-assistance stock onto **2018–2022** org-years is temporally incoherent. ACS/ZHVI are also not annual panels aligned to each tax_year. Phase 2 already documented “no year FE / pooled org-years”; the soup stretch **worsens** the story if analyzed nationally across all years.

**Implication:** Headline OLS must use an **Atlanta (or ACFB-area) × latest tax_year (2022) cross-section**, with an explicit caveat that site data are a 2026 stock.

## Space granularity — PARTIAL pass

| Check | Verdict |
|-------|---------|
| Finer than HQ-only NTEE proxy? | **Yes** — site addresses aggregated to ZIP density |
| Matches professor ACFB ~700 partners? | **No** — Feed America GA proxy + pilot/CFCs |
| National OLS appropriate? | **No** — 98.5% structural zeros outside covered GA ZIPs |
| Soup kitchens vs pantries? | **Weak** — only 23 `soup_kitchen` vs 1,263 pantries |
| Big vs local = ACFB chains? | **No** — keyword heuristic only |
| Acquisition = “Atlanta ZIPs → ACFB website/MCP”? | **Not yet** — bulk API path, not per-ZIP agent/MCP demo |

## Hybrid pipeline lens

| Component | Status |
|-----------|--------|
| Propose → pre-register → deterministic OLS → interpret | **OK** (fixture + Cursor hybrid PASS) |
| Indicator theoretically aligned to July 10 | **Partial** (density idea yes; ACFB workflow no) |
| Join / sample design for soup tests | **Not OK** (national multi-year) |
| Reproducibility / provenance | **OK** (`built_by: Grok_4.5`, decision log, CC BY attribution) |

**One-line verdict:** *Loop mechanics are sound; join design and ACFB-oriented collection were incomplete relative to July 10.*

## July 10 alignment scorecard

| Professor ask | Score | Gap |
|---------------|-------|-----|
| Rolled evaluate → propose → test | Met | Continue |
| Higher-order (3+ var) specs | Met | Keep |
| Document 2-var limitation | Met (CP3) | Keep |
| Atlanta ZIPs → ACFB → soup list workflow | Missing | Agent ZIP collect (this stretch) |
| Soup-kitchen density per ZIP | Partial | Prefer soup/meal sites; Atlanta slice |
| Big vs local comparison | Partial | Improve classification |
| Finer time alignment | Missing | Latest-year xsection + caveats |

## Remediation in this stretch

1. `DATA_GRANULARITY_AUDIT.md` (this file).
2. `12_build_analysis_slice.py` → `cp4_atlanta_xsection.csv` (ACFB-area ZIPs × tax_year=2022).
3. ACFB ZIP-collect hybrid prompt + `acfb_zip_agent_collection.csv` (ToS-safe).
4. Re-test via hybrid loop **only** on the Atlanta xsection; update report/workflow.
