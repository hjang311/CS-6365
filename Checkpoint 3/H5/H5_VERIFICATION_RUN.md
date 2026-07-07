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
Using the full suite of socioeconomic controls (including Census ACS data), the deterministic regression run (`06_run_h4_h5_split.py`) yielded the following results for the model `fundraising_efficiency_w ~ log_nonprofit_branch_density + [controls]`:

| Sample | n | IV coefficient (beta) | p-value | 95% CI | R-squared |
|---|---|---|---|---|---|
| Full (>=$500K) | 117,510 | 2.11963 | 0.002447 | [0.7485, 3.4908] | 0.1756 |
| Mid ($500K-$2M) | 53,972 | 1.10692 | 0.004737 | [0.3388, 1.8751] | 0.0904 |
| Large (>=$2M) | 63,537 | 3.05552 | 0.009074 | [0.7603, 5.3507] | 0.0973 |

**Interpretation:** 
The hypothesis is **rejected**. The data reveals a highly statistically significant ($p < 0.01$) **positive** association between social-service provider density and fundraising efficiency across all size segments. Rather than intense competition depressing efficiency, a higher density of mission-critical nonprofits in a ZIP code is correlated with *better* fundraising efficiency. This may suggest an agglomeration effect or a clustering around high-donor capital that offsets the competition. Furthermore, contrary to expectations, the positive effect is stronger for large organizations ($\beta = +3.05$) than mid-sized ones ($\beta = +1.11$).

## Artifacts
- `H5_results.md` — The raw Markdown output produced by `06_run_h4_h5_split.py`.
