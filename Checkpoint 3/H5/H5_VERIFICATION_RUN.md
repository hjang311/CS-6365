# H5 Verification Run — Social-Service Provider Density & Fundraising Efficiency

> **Note:** H5 is a distinct hypothesis from H4. H4 tests *real-estate cost* (`log_zhvi_2022`);
> H5 tests *provider density* (`log_nonprofit_branch_density`). They are run and documented
> separately, though they share the same CP3 modeling frame and control set.

## Objective
Test whether the local density of mission-critical social-service nonprofits affects the
fundraising efficiency of organizations operating in that area, and whether the effect
differs between smaller and larger organizations.

## Formal Hypothesis
**Hypothesis:** Among nonprofits with annual revenue ≥ $500,000, a higher local density of
mission-critical social-service providers (food banks, food programs, soup kitchens, and
homeless/related shelters per 10,000 residents) is associated with **lower** fundraising
efficiency, because a denser field of providers intensifies competition for the same local
donor base, raising fundraising expense relative to contributions. The effect is expected to
be **stronger among smaller ($500K–$2M) organizations** — which have shallower donor bases —
than larger (≥$2M) ones.

* **Independent Variable (IV):** `log_nonprofit_branch_density` — log of social-service
  nonprofits per 10,000 residents (NTEE K30/K31/K35/L40/L41/P43, from IRS BMF, normalized by
  ACS ZIP population).
* **Dependent Variable (DV):** `fundraising_efficiency_w` — winsorized fundraising efficiency
  (total contributions ÷ fundraising-expense proxy, capped at the 99th percentile).
* **Controls:** `log_total_revenue`, `C(ntee_major)`, `C(region)`, `poverty_rate`,
  `median_hh_income`.
* **Model:** `fundraising_efficiency_w ~ log_nonprofit_branch_density + [controls]`, run on
  the full sample and split by size segment (mid $500K–$2M vs large ≥$2M).
* **Key Citations:** Rose-Ackerman (1982), Weisbrod (1988), Thornton (2006).

## Quantitative Findings
*Pending execution of `06_run_h4_h5_split.py` on the CP3 modeling frame (requires the Census
key to build ACS population/controls). Results will be written to `H5/H5_results.md`.*

## Artifacts
- `../06_run_h4_h5_split.py` — deterministic runner (full + mid + large) shared with H4,
  writing this hypothesis's output to `H5/H5_results.md`.
- `../data/hypotheses.json` — hypothesis #4 (provider density) is the H5 entry.
