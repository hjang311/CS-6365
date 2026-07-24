# Negative Findings (Checkpoint 4 Phase 3)

Negative / null results are first-class pipeline outputs — same posture as CP3 RQ5 rejection.
Higher-order specs also report the **TA Verifier gate** (HC1 Wald F + ΔR² ≥ 5e-4 over main effects).

## Food-assistance density (Atlanta × latest tax_year)

**Frame:** `data/cp4_atlanta_food_assistance_xsection.csv`  
**Pre-registered:** `log_food_assistance_density` and poverty × density interaction.

| Spec | β | p | Gate | Outcome |
|------|---|---|------|---------|
| F01 two_var `log_food_assistance_density` | (see latest `round1_results.*`) | — | n/a (two_var) | typically **not significant** |
| F02 interaction poverty × density | (see latest) | — | **REJECT** when Wald/ΔR² fail | null / no higher-order gain |

**Reading:** Finer food-assistance density does **not** support a reliable competition (negative) story for fundraising efficiency on this cross-section. Gate REJECT on F02 is expected when the interaction adds no joint explanatory power — not a pipeline failure. Temporal caveat remains: site/NTEE stock vs 990 year alignment.

## Round 2 adaptation (after Round 1 nulls)

Round 2 must **not** re-test the same density IV. Fixture / hybrid adaptation uses e.g. `log_zhvi_2022` and `log_zhvi_2022 × log_bank_branch_density` on the Atlanta slice (`FIXTURE_PROPOSALS_FOOD_R2`). Interaction rows still face the Verifier gate.

## Housing-services density (Chicago × latest tax_year) — universality

**Path:** `phase3_results/housing_chicago/`  
**Frame:** `data/cp4_chicago_housing_services_xsection.csv`  
**Acquisition:** NTEE-only by design (`data/acquisitions/housing_services/README.md`).

| Spec | Outcome |
|------|---------|
| H01 `log_housing_services_density` | exploratory / typically not significant |
| H02 poverty × housing density | gate usually **REJECT** |

Same loop, different topic/geo/NTEE map. No confirmatory claim.

## Degradation events (also first-class)

When Feed America HTTP fails, `http_open_api` degrades to NTEE and may later overwrite the manifest (last-write-wins; `previous_adapter` logged). Both outcomes appear in `decision_log.jsonl`.

## TA higher-order specs (`--verify-ta-specs`)

I1–I4 / Q1 from `ai-suggestions/cp4` are pre-registered and gated. ACCEPT is rare by design: large-n significance without ΔR² ≥ 5e-4 is explicitly REJECT (Phase 2 limitation re-detected).
