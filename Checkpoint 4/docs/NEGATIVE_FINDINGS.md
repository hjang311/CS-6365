# Negative Findings (Checkpoint 4 Phase 3)

Negative / null results are first-class pipeline outputs — same posture as CP3 RQ5 rejection.
Higher-order specs also report the **TA Verifier gate** (HC1 Wald F + ΔR² ≥ 5e-4 over main effects).

**Why 5e-4?** Phase 2 List B showed large-n two-variable scanners can light up p < 0.05 while full-model R² stays nearly flat (~0.1756–0.1766). The Verifier requires joint significance **and** a minimum explanatory gain so “significant” interactions are not treated as discoveries by default.

Numbers below are from the Jul 24 2026 offline demo run (`09_phase3_agentic_loop.py` v2.1). Re-run `reproduce.sh` to refresh artifacts.

## Food-assistance density (Atlanta × latest tax_year)

**Frame:** `data/cp4_atlanta_food_assistance_xsection.csv` (enrich ≈ 583 × 33; OLS n below)  
**Pre-registered:** `log_food_assistance_density` and poverty × density interaction.

| Spec | β | p | R² | n | Gate | Outcome |
|------|---|---|----|---|------|---------|
| **F01** two_var `log_food_assistance_density` → `fundraising_efficiency_w` | **−21.46836** | **0.1176** | 0.2246 | **444** | n/a (two_var) | **Not significant** |
| **F02** interaction `poverty_rate` × `log_food_assistance_density` | **0.39393** | **0.8530** | 0.2247 | **444** | **REJECT** (Wald F≈0.034, ΔR²≈8.1e-5) | Null / no higher-order gain |

**Reading:** Finer food-assistance density does **not** support a reliable competition (negative) story for fundraising efficiency on this cross-section. Gate REJECT on F02 is expected when the interaction adds no joint explanatory power — **not** a pipeline failure. Temporal caveat remains: site/NTEE stock vs 990 year alignment.

Source: `phase3_results/round1_results.md`.

## Round 2 adaptation (after Round 1 nulls)

Round 2 must **not** re-test the same density IV. Adaptation used `log_zhvi_2022` and `log_zhvi_2022 × log_bank_branch_density` on the Atlanta slice:

| Spec | β | p | n | Gate | Outcome |
|------|---|---|---|------|---------|
| **F2P01** ZHVI two_var on Atlanta slice | −30.606 | 0.156 | 444 | n/a | Not significant |
| **F2P02** ZHVI × bank density | 61.801 | 0.078 | 444 | **REJECT** (Wald p≈0.079; ΔR²≈0.008 but F fails 0.05) | No ACCEPT |

Source: `phase3_results/round2_results.md`.

## Housing-services density (Chicago × latest tax_year) — universality

**Path:** `phase3_results/housing_chicago/`  
**Frame:** `data/cp4_chicago_housing_services_xsection.csv`  
**Acquisition:** NTEE-only by design (`data/acquisitions/housing_services/README.md`).

| Spec | β | p | R² | n | Gate | Outcome |
|------|---|---|----|---|------|---------|
| **H01** `log_housing_services_density` | 5.04243 | 0.4475 | 0.2822 | 403 | n/a | Exploratory / not significant |
| **H02** poverty × housing density | 0.42692 | 0.7661 | 0.2823 | 403 | **REJECT** (ΔR²≈1.2e-4) | Null |

Same loop, different topic/geo/NTEE map. No confirmatory claim.

## Degradation events (also first-class)

When Feed America HTTP fails, `http_open_api` degrades to NTEE and may later overwrite the manifest (last-write-wins; `previous_adapter` logged). Both outcomes appear in `decision_log.jsonl`. Live HTTP success wrote ~**2,250** GA entities under `data/acquisitions/food_assistance/` (CC BY — see attribution file).

## TA higher-order specs (`--verify-ta-specs`)

Pre-registered I1–I4 / Q1 on the national CP3 frame (n ≈ 116k). Latest `ta_verify/round99_results.md`:

| ID | Gate | Note |
|----|------|------|
| I1 ZHVI × nonprofit density | **REJECT** | Wald p ≈ 0.59 |
| I2 ZHVI × bank density | **REJECT** | Wald p ≈ 0.78 |
| I3 ZHVI × size_segment | **ACCEPT** | Meets Wald + ΔR² |
| I4 nonprofit density × size_segment | **REJECT** | |
| Q1 ZHVI + ZHVI² | **REJECT** | |

ACCEPT is rare by design: large-n significance without ΔR² ≥ 5e-4 is explicitly REJECT (Phase 2 limitation re-detected).

---
*Teaching snapshot aligned to Jul 24 2026 `reproduce.sh` artifacts. Registry: `docs/HYPOTHESIS_REGISTRY.md`.*
