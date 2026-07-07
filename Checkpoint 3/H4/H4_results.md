# H4 Results — Real-Estate Cost & Fundraising Efficiency (Spatial Mismatch)

**Model:** `fundraising_efficiency_w ~ log_zhvi_2022 + log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income`  (robust HC1 errors)

| Sample | n | IV coefficient (beta) | p-value | 95% CI | R-squared |
|---|---|---|---|---|---|
| Full (>=$500K) | 116,587 | -7.91647 | 2.427e-22 | [-9.5124, -6.3205] | 0.1766 |
| Mid ($500K-$2M) | 53,650 | -2.99536 | 3.615e-11 | [-3.8823, -2.1084] | 0.0912 |
| Large (>=$2M) | 62,936 | -11.53377 | 2.447e-16 | [-14.2913, -8.7762] | 0.0985 |
