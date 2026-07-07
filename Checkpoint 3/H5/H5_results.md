# H5 Results — Social-Service Provider Density & Fundraising Efficiency

**Model:** `fundraising_efficiency_w ~ log_nonprofit_branch_density + log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income`  (robust HC1 errors)

| Sample | n | IV coefficient (beta) | p-value | 95% CI | R-squared |
|---|---|---|---|---|---|
| Full (>=$500K) | 117,510 | 2.11963 | 0.002447 | [0.7485, 3.4908] | 0.1756 |
| Mid ($500K-$2M) | 53,972 | 1.10692 | 0.004737 | [0.3388, 1.8751] | 0.0904 |
| Large (>=$2M) | 63,537 | 3.05552 | 0.009074 | [0.7603, 5.3507] | 0.0973 |
