# Hypothesis / Research-Question Registry

Single map of IDs used across reports, folders, and Phase 3 proposal JSON.  
**Folder aliases** (H4/H5) may remain on disk; prose prefers **RQ** labels.

## Confirmatory / Manual–Unrolled agenda

| ID | Folder alias | Statement (short) | Predicted | Observed | Verdict | Primary artifact |
|----|--------------|-------------------|-----------|----------|---------|------------------|
| **RQ1** | CP1 broadband | Low broadband → worse fundraising efficiency | negative | null (p ≈ 0.37, n = 457) | Null / baseline | `Checkpoint 1/` FINDINGS / report |
| **RQ2** | H2 | Lower ZIP bank-branch density → higher fundraising efficiency (rev ≥ $500K) | negative | β ≈ −0.11453, p ≈ 0.0017 | **Confirmed** | `Checkpoint 2/H2_Pipeline/findings_results.md`; List A replay; `Checkpoint 3/RQ2/RQ2_VERIFICATION_RUN.md` |
| **RQ3** | H3 | Higher payment-processing fee share → higher efficiency | negative/positive by size | Feasibility only (5.5% itemization) | Not confirmatory | `Checkpoint 2/H3_Testing/` |
| **RQ4** | H4 | Higher ZHVI → lower fundraising efficiency | negative | β = −7.91647 | **Confirmed** (PASS repro) | `Checkpoint 3/H4/`; `Checkpoint 4/phase3_results/validation_check.md` |
| **RQ5** | H5 | Higher social-service provider density → lower efficiency (competition) | negative | β = +2.11963 | **Rejected** (agglomeration reading) | `Checkpoint 3/H5/`; validation_check.md |

## Phase 3 — Food Atlanta (finer granularity)

| ID | Spec | Predicted | Observed | Gate | Verdict | Artifact |
|----|------|-----------|----------|------|---------|----------|
| **F01** | `log_food_assistance_density` → `fundraising_efficiency_w` | negative | β ≈ −21.47, p ≈ 0.118, n = 444 | n/a (two_var) | Not significant | `Checkpoint 4/phase3_results/round1_results.md` |
| **F02** | `poverty_rate` × `log_food_assistance_density` | negative interaction | β ≈ 0.39, p ≈ 0.85 | **REJECT** | Null / no higher-order gain | same |

## Phase 3 — Housing Chicago (universality / NTEE-only)

| ID | Spec | Observed | Gate | Verdict | Artifact |
|----|------|----------|------|---------|----------|
| **H01** | `log_housing_services_density` → efficiency | β ≈ 5.04, p ≈ 0.45, n = 403 | n/a | Exploratory / not significant | `phase3_results/housing_chicago/round1_results.md` |
| **H02** | poverty × housing density | β ≈ 0.43, p ≈ 0.77 | **REJECT** | Null | same |

## TA Verifier higher-order specs (`--verify-ta-specs`)

Pre-registered interaction / quadratic checks on the national CP3 frame (n ≈ 116k). ACCEPT only if HC1 Wald F p < 0.05 **and** ΔR² ≥ 5e-4.

| ID | Spec (short) | Gate (latest) | Artifact |
|----|--------------|---------------|----------|
| **I1** | ZHVI × nonprofit branch density | **REJECT** | `phase3_results/ta_verify/round99_results.md` |
| **I2** | ZHVI × bank branch density | **REJECT** | same |
| **I3** | ZHVI × size_segment | **ACCEPT** | same |
| **I4** | nonprofit density × size_segment | **REJECT** | same |
| **Q1** | ZHVI + ZHVI² | **REJECT** | same |

These were absorbed from TA higher-order proposal specs into `09 --verify-ta-specs` / `--run` gating — evidence is in-repo; there is no separate `ai-suggestions/cp4` tree required to verify.

## Naming rules

1. Prefer **RQ2–RQ5** in report prose; keep **H2/H4/H5** when pointing at folders.
2. Phase 3 food/housing IDs (**F01**, **H01**, …) are proposal JSON IDs — do not reuse as RQ numbers.
3. Update this file whenever a new confirmatory claim is added to the Checkpoint 4 report.
