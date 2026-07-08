# Deterministic Agentic Loop - Summary of Results

Tested a total of 215 combinatorial variable pairs.

| ID | IV | DV | beta | p-value | R² | n | Significant? |
|---|---|---|---|---|---|---|---|
| 1 | `total_contributions` | `fundraising_events_direct_expenses` | 0.00228 | 1.863e-10 | 0.0649 | 117,510 | ✅ Yes |
| 2 | `total_contributions` | `total_revenue` | 2.94373 | 4.933e-28 | 0.3849 | 117,510 | ✅ Yes |
| 3 | `total_contributions` | `professional_fundraising_fees` | 0.00376 | 8.445e-06 | 0.0903 | 117,510 | ✅ Yes |
| 4 | `total_contributions` | `total_expenses` | 2.76017 | 4.017e-24 | 0.3676 | 117,510 | ✅ Yes |
| 5 | `total_contributions` | `population` | 0.00000 | 0.2678 | 0.0321 | 117,510 | No |
| 6 | `total_contributions` | `social_service_count` | -0.00000 | 0.4447 | 0.0186 | 117,510 | No |
| 7 | `total_contributions` | `nonprofit_branch_density` | 0.00000 | 0.4688 | 0.0663 | 117,510 | No |
| 8 | `total_contributions` | `zhvi_2022` | 0.00005 | 0.01954 | 0.5880 | 116,587 | ✅ Yes |
| 9 | `total_contributions` | `fundraising_expense_proxy` | 0.00604 | 7.83e-09 | 0.1346 | 117,510 | ✅ Yes |
| 10 | `total_contributions` | `fundraising_efficiency` | 0.00000 | 3.036e-11 | 0.1711 | 117,510 | ✅ Yes |
| 11 | `total_contributions` | `log_fundraising_efficiency` | 0.00000 | 0.0005462 | 0.2010 | 117,510 | ✅ Yes |
| 12 | `total_contributions` | `log_nonprofit_branch_density` | 0.00000 | 0.3071 | 0.0739 | 117,510 | No |
| 13 | `total_contributions` | `log_zhvi_2022` | 0.00000 | 0.001441 | 0.6936 | 116,587 | ✅ Yes |
| 14 | `total_contributions` | `fundraising_efficiency_w` | 0.00000 | 1.915e-11 | 0.1787 | 117,510 | ✅ Yes |
| 15 | `fundraising_events_direct_expenses` | `total_contributions` | 11.41825 | 5.823e-10 | 0.1335 | 117,510 | ✅ Yes |
| 16 | `fundraising_events_direct_expenses` | `total_revenue` | 32.12733 | 1.587e-05 | 0.1146 | 117,510 | ✅ Yes |
| 17 | `fundraising_events_direct_expenses` | `professional_fundraising_fees` | 0.05320 | 5.012e-06 | 0.0246 | 117,510 | ✅ Yes |
| 18 | `fundraising_events_direct_expenses` | `total_expenses` | 29.77376 | 1.956e-05 | 0.1094 | 117,510 | ✅ Yes |
| 19 | `fundraising_events_direct_expenses` | `population` | 0.00009 | 0.2788 | 0.0321 | 117,510 | No |
| 20 | `fundraising_events_direct_expenses` | `social_service_count` | 0.00000 | 0.007843 | 0.0187 | 117,510 | ✅ Yes |
| 21 | `fundraising_events_direct_expenses` | `nonprofit_branch_density` | 0.00000 | 0.03696 | 0.0663 | 117,510 | ✅ Yes |
| 22 | `fundraising_events_direct_expenses` | `zhvi_2022` | 0.01318 | 1.304e-07 | 0.5882 | 116,587 | ✅ Yes |
| 23 | `fundraising_events_direct_expenses` | `fundraising_expense_proxy` | 1.05320 | 0 | 0.5492 | 117,510 | ✅ Yes |
| 24 | `fundraising_events_direct_expenses` | `fundraising_efficiency` | -0.00003 | 1.315e-19 | 0.1827 | 117,510 | ✅ Yes |
| 25 | `fundraising_events_direct_expenses` | `log_fundraising_efficiency` | -0.00000 | 1.162e-20 | 0.2408 | 117,510 | ✅ Yes |
| 26 | `fundraising_events_direct_expenses` | `log_nonprofit_branch_density` | 0.00000 | 0.001831 | 0.0740 | 117,510 | ✅ Yes |
| 27 | `fundraising_events_direct_expenses` | `log_zhvi_2022` | 0.00000 | 2.299e-09 | 0.6939 | 116,587 | ✅ Yes |
| 28 | `fundraising_events_direct_expenses` | `fundraising_efficiency_w` | -0.00003 | 1.336e-19 | 0.1919 | 117,510 | ✅ Yes |
| 29 | `total_revenue` | `total_contributions` | 0.10544 | 3.595e-11 | 0.3865 | 117,510 | ✅ Yes |
| 30 | `total_revenue` | `fundraising_events_direct_expenses` | 0.00023 | 2.141e-18 | 0.0469 | 117,510 | ✅ Yes |
| 31 | `total_revenue` | `professional_fundraising_fees` | 0.00016 | 3.673e-09 | 0.0255 | 117,510 | ✅ Yes |
| 32 | `total_revenue` | `total_expenses` | 0.95532 | 0 | 0.9874 | 117,510 | ✅ Yes |
| 33 | `total_revenue` | `population` | 0.00000 | 0.1345 | 0.0321 | 117,510 | No |
| 34 | `total_revenue` | `social_service_count` | -0.00000 | 0.5797 | 0.0186 | 117,510 | No |
| 35 | `total_revenue` | `nonprofit_branch_density` | -0.00000 | 0.0001334 | 0.0663 | 117,510 | ✅ Yes |
| 36 | `total_revenue` | `zhvi_2022` | -0.00001 | 0.05149 | 0.5880 | 116,587 | No |
| 37 | `total_revenue` | `fundraising_expense_proxy` | 0.00039 | 1.362e-26 | 0.0625 | 117,510 | ✅ Yes |
| 38 | `total_revenue` | `fundraising_efficiency` | -0.00000 | 0.2285 | 0.1674 | 117,510 | No |
| 39 | `total_revenue` | `log_fundraising_efficiency` | -0.00000 | 6.453e-17 | 0.2021 | 117,510 | ✅ Yes |
| 40 | `total_revenue` | `log_nonprofit_branch_density` | -0.00000 | 0.1704 | 0.0739 | 117,510 | No |
| 41 | `total_revenue` | `log_zhvi_2022` | 0.00000 | 0.6013 | 0.6936 | 116,587 | No |
| 42 | `total_revenue` | `fundraising_efficiency_w` | -0.00000 | 0.06292 | 0.1756 | 117,510 | No |
| 43 | `professional_fundraising_fees` | `total_contributions` | 18.62409 | 5.977e-05 | 0.1726 | 117,510 | ✅ Yes |
| 44 | `professional_fundraising_fees` | `fundraising_events_direct_expenses` | 0.05265 | 0.03275 | 0.0425 | 117,510 | ✅ Yes |
| 45 | `professional_fundraising_fees` | `total_revenue` | 22.61811 | 0.001367 | 0.1113 | 117,510 | ✅ Yes |
| 46 | `professional_fundraising_fees` | `total_expenses` | 19.60780 | 0.001125 | 0.1060 | 117,510 | ✅ Yes |
| 47 | `professional_fundraising_fees` | `population` | -0.00013 | 0.1282 | 0.0321 | 117,510 | No |
| 48 | `professional_fundraising_fees` | `social_service_count` | -0.00000 | 0.0216 | 0.0186 | 117,510 | ✅ Yes |
| 49 | `professional_fundraising_fees` | `nonprofit_branch_density` | -0.00000 | 0.004892 | 0.0663 | 117,510 | ✅ Yes |
| 50 | `professional_fundraising_fees` | `zhvi_2022` | -0.00266 | 0.01382 | 0.5880 | 116,587 | ✅ Yes |
| 51 | `professional_fundraising_fees` | `fundraising_expense_proxy` | 1.05265 | 0 | 0.5538 | 117,510 | ✅ Yes |
| 52 | `professional_fundraising_fees` | `fundraising_efficiency` | -0.00001 | 0.0006111 | 0.1709 | 117,510 | ✅ Yes |
| 53 | `professional_fundraising_fees` | `log_fundraising_efficiency` | -0.00000 | 0.0004424 | 0.2047 | 117,510 | ✅ Yes |
| 54 | `professional_fundraising_fees` | `log_nonprofit_branch_density` | -0.00000 | 0.2017 | 0.0739 | 117,510 | No |
| 55 | `professional_fundraising_fees` | `log_zhvi_2022` | -0.00000 | 0.2095 | 0.6936 | 116,587 | No |
| 56 | `professional_fundraising_fees` | `fundraising_efficiency_w` | -0.00001 | 0.0006072 | 0.1792 | 117,510 | ✅ Yes |
| 57 | `total_expenses` | `total_contributions` | 0.10680 | 2.019e-10 | 0.3726 | 117,510 | ✅ Yes |
| 58 | `total_expenses` | `fundraising_events_direct_expenses` | 0.00023 | 2.859e-16 | 0.0464 | 117,510 | ✅ Yes |
| 59 | `total_expenses` | `total_revenue` | 1.03207 | 0 | 0.9875 | 117,510 | ✅ Yes |
| 60 | `total_expenses` | `professional_fundraising_fees` | 0.00015 | 2.943e-09 | 0.0248 | 117,510 | ✅ Yes |
| 61 | `total_expenses` | `population` | 0.00000 | 0.1242 | 0.0321 | 117,510 | No |
| 62 | `total_expenses` | `social_service_count` | -0.00000 | 0.5819 | 0.0186 | 117,510 | No |
| 63 | `total_expenses` | `nonprofit_branch_density` | -0.00000 | 8.881e-05 | 0.0663 | 117,510 | ✅ Yes |
| 64 | `total_expenses` | `zhvi_2022` | -0.00001 | 0.03605 | 0.5880 | 116,587 | ✅ Yes |
| 65 | `total_expenses` | `fundraising_expense_proxy` | 0.00038 | 5.248e-25 | 0.0614 | 117,510 | ✅ Yes |
| 66 | `total_expenses` | `fundraising_efficiency` | -0.00000 | 0.1842 | 0.1675 | 117,510 | No |
| 67 | `total_expenses` | `log_fundraising_efficiency` | -0.00000 | 2.29e-16 | 0.2022 | 117,510 | ✅ Yes |
| 68 | `total_expenses` | `log_nonprofit_branch_density` | -0.00000 | 0.1349 | 0.0739 | 117,510 | No |
| 69 | `total_expenses` | `log_zhvi_2022` | 0.00000 | 0.5979 | 0.6936 | 116,587 | No |
| 70 | `total_expenses` | `fundraising_efficiency_w` | -0.00000 | 0.04677 | 0.1757 | 117,510 | ✅ Yes |
| 71 | `population` | `total_contributions` | 8.31819 | 0.2506 | 0.1103 | 117,510 | No |
| 72 | `population` | `fundraising_events_direct_expenses` | 0.08313 | 0.2651 | 0.0399 | 117,510 | No |
| 73 | `population` | `total_revenue` | 54.13860 | 0.1236 | 0.1081 | 117,510 | No |
| 74 | `population` | `professional_fundraising_fees` | -0.12638 | 0.02285 | 0.0219 | 117,510 | ✅ Yes |
| 75 | `population` | `total_expenses` | 55.16904 | 0.111 | 0.1033 | 117,510 | No |
| 76 | `population` | `social_service_count` | 0.00003 | 1.345e-287 | 0.0495 | 117,510 | ✅ Yes |
| 77 | `population` | `nonprofit_branch_density` | -0.00002 | 0 | 0.1150 | 117,510 | ✅ Yes |
| 78 | `population` | `zhvi_2022` | 0.46946 | 1.049e-20 | 0.5882 | 116,587 | ✅ Yes |
| 79 | `population` | `fundraising_expense_proxy` | -0.04325 | 0.652 | 0.0529 | 117,510 | No |
| 80 | `population` | `fundraising_efficiency` | -0.00006 | 0.001756 | 0.1674 | 117,510 | ✅ Yes |
| 81 | `population` | `log_fundraising_efficiency` | -0.00000 | 1.344e-06 | 0.2010 | 117,510 | ✅ Yes |
| 82 | `population` | `log_nonprofit_branch_density` | -0.00001 | 0 | 0.1161 | 117,510 | ✅ Yes |
| 83 | `population` | `log_zhvi_2022` | 0.00000 | 0 | 0.6992 | 116,587 | ✅ Yes |
| 84 | `population` | `fundraising_efficiency_w` | -0.00006 | 0.001325 | 0.1756 | 117,510 | ✅ Yes |
| 85 | `social_service_count` | `total_contributions` | -23375.99707 | 0.4622 | 0.1103 | 117,510 | No |
| 86 | `social_service_count` | `fundraising_events_direct_expenses` | 1066.22054 | 0.01322 | 0.0399 | 117,510 | ✅ Yes |
| 87 | `social_service_count` | `total_revenue` | -95275.40164 | 0.5784 | 0.1080 | 117,510 | No |
| 88 | `social_service_count` | `professional_fundraising_fees` | -776.85824 | 0.0008937 | 0.0219 | 117,510 | ✅ Yes |
| 89 | `social_service_count` | `total_expenses` | -91887.75572 | 0.5811 | 0.1033 | 117,510 | No |
| 90 | `social_service_count` | `population` | 1020.96057 | 9.046e-14 | 0.0625 | 117,510 | ✅ Yes |
| 91 | `social_service_count` | `nonprofit_branch_density` | 0.31020 | 1.491e-31 | 0.3341 | 117,510 | ✅ Yes |
| 92 | `social_service_count` | `zhvi_2022` | 5686.56506 | 1.925e-07 | 0.5892 | 116,587 | ✅ Yes |
| 93 | `social_service_count` | `fundraising_expense_proxy` | 289.36230 | 0.5269 | 0.0529 | 117,510 | No |
| 94 | `social_service_count` | `fundraising_efficiency` | 0.44323 | 0.01212 | 0.1675 | 117,510 | ✅ Yes |
| 95 | `social_service_count` | `log_fundraising_efficiency` | 0.00734 | 2.044e-10 | 0.2011 | 117,510 | ✅ Yes |
| 96 | `social_service_count` | `log_nonprofit_branch_density` | 0.07848 | 2.189e-14 | 0.3134 | 117,510 | ✅ Yes |
| 97 | `social_service_count` | `log_zhvi_2022` | 0.01123 | 2.991e-08 | 0.6959 | 116,587 | ✅ Yes |
| 98 | `social_service_count` | `fundraising_efficiency_w` | 0.39450 | 0.005765 | 0.1756 | 117,510 | ✅ Yes |
| 99 | `nonprofit_branch_density` | `total_contributions` | 50634.71925 | 0.4486 | 0.1103 | 117,510 | No |
| 100 | `nonprofit_branch_density` | `fundraising_events_direct_expenses` | 1273.99312 | 0.02232 | 0.0399 | 117,510 | ✅ Yes |
| 101 | `nonprofit_branch_density` | `total_revenue` | -885106.44305 | 8.917e-05 | 0.1081 | 117,510 | ✅ Yes |
| 102 | `nonprofit_branch_density` | `professional_fundraising_fees` | -1564.48299 | 0.002606 | 0.0219 | 117,510 | ✅ Yes |
| 103 | `nonprofit_branch_density` | `total_expenses` | -853458.23140 | 6.478e-05 | 0.1034 | 117,510 | ✅ Yes |
| 104 | `nonprofit_branch_density` | `population` | -2270.83071 | 0 | 0.0826 | 117,510 | ✅ Yes |
| 105 | `nonprofit_branch_density` | `social_service_count` | 0.92473 | 7.507e-54 | 0.3001 | 117,510 | ✅ Yes |
| 106 | `nonprofit_branch_density` | `zhvi_2022` | 7673.18237 | 6.913e-41 | 0.5887 | 116,587 | ✅ Yes |
| 107 | `nonprofit_branch_density` | `fundraising_expense_proxy` | -290.48987 | 0.7113 | 0.0529 | 117,510 | No |
| 108 | `nonprofit_branch_density` | `fundraising_efficiency` | 0.70224 | 0.00195 | 0.1675 | 117,510 | ✅ Yes |
| 109 | `nonprofit_branch_density` | `log_fundraising_efficiency` | 0.01245 | 1.124e-09 | 0.2011 | 117,510 | ✅ Yes |
| 110 | `nonprofit_branch_density` | `log_zhvi_2022` | 0.01208 | 5.046e-56 | 0.6944 | 116,587 | ✅ Yes |
| 111 | `nonprofit_branch_density` | `fundraising_efficiency_w` | 0.64843 | 0.001427 | 0.1756 | 117,510 | ✅ Yes |
| 112 | `zhvi_2022` | `total_contributions` | 0.76882 | 0.005839 | 0.1087 | 116,587 | ✅ Yes |
| 113 | `zhvi_2022` | `fundraising_events_direct_expenses` | 0.03919 | 1.844e-20 | 0.0402 | 116,587 | ✅ Yes |
| 114 | `zhvi_2022` | `total_revenue` | -2.80963 | 0.05065 | 0.1075 | 116,587 | No |
| 115 | `zhvi_2022` | `professional_fundraising_fees` | -0.00775 | 0.0223 | 0.0209 | 116,587 | ✅ Yes |
| 116 | `zhvi_2022` | `total_expenses` | -2.84500 | 0.03526 | 0.1028 | 116,587 | ✅ Yes |
| 117 | `zhvi_2022` | `population` | 0.00148 | 1.242e-18 | 0.0309 | 116,587 | ✅ Yes |
| 118 | `zhvi_2022` | `social_service_count` | 0.00000 | 1.718e-76 | 0.0230 | 116,587 | ✅ Yes |
| 119 | `zhvi_2022` | `nonprofit_branch_density` | 0.00000 | 4.581e-32 | 0.0623 | 116,587 | ✅ Yes |
| 120 | `zhvi_2022` | `fundraising_expense_proxy` | 0.03144 | 6.234e-09 | 0.0520 | 116,587 | ✅ Yes |
| 121 | `zhvi_2022` | `fundraising_efficiency` | -0.00001 | 6.657e-08 | 0.1681 | 116,587 | ✅ Yes |
| 122 | `zhvi_2022` | `log_fundraising_efficiency` | -0.00000 | 3.787e-08 | 0.2014 | 116,587 | ✅ Yes |
| 123 | `zhvi_2022` | `log_nonprofit_branch_density` | 0.00000 | 4.233e-40 | 0.0736 | 116,587 | ✅ Yes |
| 124 | `zhvi_2022` | `fundraising_efficiency_w` | -0.00001 | 1.109e-08 | 0.1761 | 116,587 | ✅ Yes |
| 125 | `fundraising_expense_proxy` | `total_contributions` | 14.28388 | 1.594e-14 | 0.1871 | 117,510 | ✅ Yes |
| 126 | `fundraising_expense_proxy` | `fundraising_events_direct_expenses` | 0.49754 | 7.909e-08 | 0.5430 | 117,510 | ✅ Yes |
| 127 | `fundraising_expense_proxy` | `total_revenue` | 25.97357 | 1.209e-06 | 0.1172 | 117,510 | ✅ Yes |
| 128 | `fundraising_expense_proxy` | `professional_fundraising_fees` | 0.50246 | 5.887e-08 | 0.5392 | 117,510 | ✅ Yes |
| 129 | `fundraising_expense_proxy` | `total_expenses` | 23.42481 | 1.451e-06 | 0.1113 | 117,510 | ✅ Yes |
| 130 | `fundraising_expense_proxy` | `population` | -0.00002 | 0.6569 | 0.0321 | 117,510 | No |
| 131 | `fundraising_expense_proxy` | `social_service_count` | 0.00000 | 0.5208 | 0.0186 | 117,510 | No |
| 132 | `fundraising_expense_proxy` | `nonprofit_branch_density` | -0.00000 | 0.7057 | 0.0663 | 117,510 | No |
| 133 | `fundraising_expense_proxy` | `zhvi_2022` | 0.00507 | 0.0007725 | 0.5880 | 116,587 | ✅ Yes |
| 134 | `fundraising_expense_proxy` | `fundraising_efficiency` | -0.00002 | 2.104e-10 | 0.1833 | 117,510 | ✅ Yes |
| 135 | `fundraising_expense_proxy` | `log_fundraising_efficiency` | -0.00000 | 5.71e-10 | 0.2332 | 117,510 | ✅ Yes |
| 136 | `fundraising_expense_proxy` | `log_nonprofit_branch_density` | 0.00000 | 0.07078 | 0.0739 | 117,510 | No |
| 137 | `fundraising_expense_proxy` | `log_zhvi_2022` | 0.00000 | 1.073e-05 | 0.6937 | 116,587 | ✅ Yes |
| 138 | `fundraising_expense_proxy` | `fundraising_efficiency_w` | -0.00002 | 2.134e-10 | 0.1924 | 117,510 | ✅ Yes |
| 139 | `fundraising_efficiency` | `total_contributions` | 21900.75345 | 7.008e-16 | 0.1144 | 117,510 | ✅ Yes |
| 140 | `fundraising_efficiency` | `fundraising_events_direct_expenses` | -624.43306 | 5.257e-220 | 0.0576 | 117,510 | ✅ Yes |
| 141 | `fundraising_efficiency` | `total_revenue` | -15682.31547 | 0.2079 | 0.1081 | 117,510 | No |
| 142 | `fundraising_efficiency` | `professional_fundraising_fees` | -299.96445 | 2.377e-30 | 0.0260 | 117,510 | ✅ Yes |
| 143 | `fundraising_efficiency` | `total_expenses` | -16830.53168 | 0.1596 | 0.1034 | 117,510 | No |
| 144 | `fundraising_efficiency` | `population` | -1.36209 | 0.00176 | 0.0322 | 117,510 | ✅ Yes |
| 145 | `fundraising_efficiency` | `social_service_count` | 0.00030 | 0.01904 | 0.0187 | 117,510 | ✅ Yes |
| 146 | `fundraising_efficiency` | `nonprofit_branch_density` | 0.00016 | 0.002055 | 0.0664 | 117,510 | ✅ Yes |
| 147 | `fundraising_efficiency` | `zhvi_2022` | -39.99842 | 6.605e-08 | 0.5881 | 116,587 | ✅ Yes |
| 148 | `fundraising_efficiency` | `fundraising_expense_proxy` | -924.39751 | 5.722e-165 | 0.0710 | 117,510 | ✅ Yes |
| 149 | `fundraising_efficiency` | `log_nonprofit_branch_density` | 0.00004 | 0.003423 | 0.0740 | 117,510 | ✅ Yes |
| 150 | `fundraising_efficiency` | `log_zhvi_2022` | -0.00009 | 1.27e-20 | 0.6938 | 116,587 | ✅ Yes |
| 151 | `log_fundraising_efficiency` | `total_contributions` | 334478.79576 | 9.075e-08 | 0.1104 | 117,510 | ✅ Yes |
| 152 | `log_fundraising_efficiency` | `fundraising_events_direct_expenses` | -89243.13530 | 8.394e-153 | 0.0878 | 117,510 | ✅ Yes |
| 153 | `log_fundraising_efficiency` | `total_revenue` | -5954427.25180 | 1.509e-38 | 0.1095 | 117,510 | ✅ Yes |
| 154 | `log_fundraising_efficiency` | `professional_fundraising_fees` | -27618.08286 | 1.359e-26 | 0.0265 | 117,510 | ✅ Yes |
| 155 | `log_fundraising_efficiency` | `total_expenses` | -5863548.29381 | 6.884e-41 | 0.1048 | 117,510 | ✅ Yes |
| 156 | `log_fundraising_efficiency` | `population` | -184.35041 | 1.373e-06 | 0.0323 | 117,510 | ✅ Yes |
| 157 | `log_fundraising_efficiency` | `social_service_count` | 0.03781 | 3.709e-09 | 0.0189 | 117,510 | ✅ Yes |
| 158 | `log_fundraising_efficiency` | `nonprofit_branch_density` | 0.02151 | 1.574e-09 | 0.0665 | 117,510 | ✅ Yes |
| 159 | `log_fundraising_efficiency` | `zhvi_2022` | -3641.95881 | 3.718e-08 | 0.5881 | 116,587 | ✅ Yes |
| 160 | `log_fundraising_efficiency` | `fundraising_expense_proxy` | -116861.21816 | 6.515e-165 | 0.0912 | 117,510 | ✅ Yes |
| 161 | `log_fundraising_efficiency` | `log_nonprofit_branch_density` | 0.00697 | 1.442e-12 | 0.0742 | 117,510 | ✅ Yes |
| 162 | `log_fundraising_efficiency` | `log_zhvi_2022` | -0.00647 | 5.476e-14 | 0.6937 | 116,587 | ✅ Yes |
| 163 | `log_nonprofit_branch_density` | `total_contributions` | 322445.25348 | 0.2642 | 0.1103 | 117,510 | No |
| 164 | `log_nonprofit_branch_density` | `fundraising_events_direct_expenses` | 10609.53068 | 0.0004278 | 0.0399 | 117,510 | ✅ Yes |
| 165 | `log_nonprofit_branch_density` | `total_revenue` | -1514893.33996 | 0.1732 | 0.1081 | 117,510 | No |
| 166 | `log_nonprofit_branch_density` | `professional_fundraising_fees` | -2719.05549 | 0.218 | 0.0219 | 117,510 | No |
| 167 | `log_nonprofit_branch_density` | `total_expenses` | -1568101.34405 | 0.1389 | 0.1033 | 117,510 | No |
| 168 | `log_nonprofit_branch_density` | `population` | -7968.65350 | 0 | 0.0763 | 117,510 | ✅ Yes |
| 169 | `log_nonprofit_branch_density` | `social_service_count` | 3.29543 | 2.166e-292 | 0.2724 | 117,510 | ✅ Yes |
| 170 | `log_nonprofit_branch_density` | `zhvi_2022` | 30273.48595 | 4.297e-44 | 0.5888 | 116,587 | ✅ Yes |
| 171 | `log_nonprofit_branch_density` | `fundraising_expense_proxy` | 7890.47519 | 0.04295 | 0.0529 | 117,510 | ✅ Yes |
| 172 | `log_nonprofit_branch_density` | `fundraising_efficiency` | 2.22990 | 0.003406 | 0.1674 | 117,510 | ✅ Yes |
| 173 | `log_nonprofit_branch_density` | `log_fundraising_efficiency` | 0.05682 | 1.4e-12 | 0.2012 | 117,510 | ✅ Yes |
| 174 | `log_nonprofit_branch_density` | `log_zhvi_2022` | 0.04935 | 3.762e-67 | 0.6946 | 116,587 | ✅ Yes |
| 175 | `log_nonprofit_branch_density` | `fundraising_efficiency_w` | 2.11963 | 0.002447 | 0.1756 | 117,510 | ✅ Yes |
| 176 | `log_zhvi_2022` | `total_contributions` | 1116738.12110 | 0.0001614 | 0.1088 | 116,587 | ✅ Yes |
| 177 | `log_zhvi_2022` | `fundraising_events_direct_expenses` | 42317.17054 | 1.069e-42 | 0.0406 | 116,587 | ✅ Yes |
| 178 | `log_zhvi_2022` | `total_revenue` | 657173.86888 | 0.6 | 0.1075 | 116,587 | No |
| 179 | `log_zhvi_2022` | `professional_fundraising_fees` | -3417.16052 | 0.1759 | 0.0209 | 116,587 | No |
| 180 | `log_zhvi_2022` | `total_expenses` | 622019.91094 | 0.5972 | 0.1028 | 116,587 | No |
| 181 | `log_zhvi_2022` | `population` | 6005.20885 | 0 | 0.0480 | 116,587 | ✅ Yes |
| 182 | `log_zhvi_2022` | `social_service_count` | 0.67484 | 1.838e-206 | 0.0274 | 116,587 | ✅ Yes |
| 183 | `log_zhvi_2022` | `nonprofit_branch_density` | 0.22431 | 1.309e-47 | 0.0632 | 116,587 | ✅ Yes |
| 184 | `log_zhvi_2022` | `fundraising_expense_proxy` | 38900.01002 | 3.844e-21 | 0.0522 | 116,587 | ✅ Yes |
| 185 | `log_zhvi_2022` | `fundraising_efficiency` | -8.15774 | 1.096e-20 | 0.1685 | 116,587 | ✅ Yes |
| 186 | `log_zhvi_2022` | `log_fundraising_efficiency` | -0.07508 | 3.924e-14 | 0.2016 | 116,587 | ✅ Yes |
| 187 | `log_zhvi_2022` | `log_nonprofit_branch_density` | 0.06781 | 1.692e-65 | 0.0748 | 116,587 | ✅ Yes |
| 188 | `log_zhvi_2022` | `fundraising_efficiency_w` | -7.91647 | 2.427e-22 | 0.1766 | 116,587 | ✅ Yes |
| 189 | `fundraising_efficiency_w` | `total_contributions` | 21917.98153 | 1.575e-18 | 0.1138 | 117,510 | ✅ Yes |
| 190 | `fundraising_efficiency_w` | `fundraising_events_direct_expenses` | -698.10206 | 9.731e-226 | 0.0589 | 117,510 | ✅ Yes |
| 191 | `fundraising_efficiency_w` | `total_revenue` | -24056.60025 | 0.04568 | 0.1082 | 117,510 | ✅ Yes |
| 192 | `fundraising_efficiency_w` | `professional_fundraising_fees` | -332.79487 | 2.317e-30 | 0.0262 | 117,510 | ✅ Yes |
| 193 | `fundraising_efficiency_w` | `total_expenses` | -25077.41549 | 0.02961 | 0.1035 | 117,510 | ✅ Yes |
| 194 | `fundraising_efficiency_w` | `population` | -1.51314 | 0.001328 | 0.0322 | 117,510 | ✅ Yes |
| 195 | `fundraising_efficiency_w` | `social_service_count` | 0.00031 | 0.01035 | 0.0187 | 117,510 | ✅ Yes |
| 196 | `fundraising_efficiency_w` | `nonprofit_branch_density` | 0.00017 | 0.001514 | 0.0664 | 117,510 | ✅ Yes |
| 197 | `fundraising_efficiency_w` | `zhvi_2022` | -45.46065 | 1.08e-08 | 0.5881 | 116,587 | ✅ Yes |
| 198 | `fundraising_efficiency_w` | `fundraising_expense_proxy` | -1030.89693 | 2.799e-168 | 0.0723 | 117,510 | ✅ Yes |
| 199 | `fundraising_efficiency_w` | `log_nonprofit_branch_density` | 0.00004 | 0.002464 | 0.0740 | 117,510 | ✅ Yes |
| 200 | `fundraising_efficiency_w` | `log_zhvi_2022` | -0.00011 | 2.628e-22 | 0.6939 | 116,587 | ✅ Yes |
| 201 | `size_segment` | `total_contributions` | 0.00000 | 1 | 0.1432 | 117,509 | No |
| 202 | `size_segment` | `fundraising_events_direct_expenses` | 0.00000 | 1 | 0.0420 | 117,509 | No |
| 203 | `size_segment` | `total_revenue` | 0.00000 | 1 | 0.1591 | 117,509 | No |
| 204 | `size_segment` | `professional_fundraising_fees` | 0.00000 | 1 | 0.0269 | 117,509 | No |
| 205 | `size_segment` | `total_expenses` | 0.00000 | 1 | 0.1526 | 117,509 | No |
| 206 | `size_segment` | `population` | 0.00000 | 1 | 0.0321 | 117,509 | No |
| 207 | `size_segment` | `social_service_count` | 0.00000 | 1 | 0.0188 | 117,509 | No |
| 208 | `size_segment` | `nonprofit_branch_density` | 0.00000 | 1 | 0.0665 | 117,509 | No |
| 209 | `size_segment` | `zhvi_2022` | 0.00000 | 1 | 0.5880 | 116,586 | No |
| 210 | `size_segment` | `fundraising_expense_proxy` | 0.00000 | 1 | 0.0592 | 117,509 | No |
| 211 | `size_segment` | `fundraising_efficiency` | 0.00000 | 1 | 0.1676 | 117,509 | No |
| 212 | `size_segment` | `log_fundraising_efficiency` | 0.00000 | 1 | 0.2046 | 117,509 | No |
| 213 | `size_segment` | `log_nonprofit_branch_density` | 0.00000 | 1 | 0.0740 | 117,509 | No |
| 214 | `size_segment` | `log_zhvi_2022` | 0.00000 | 1 | 0.6936 | 116,586 | No |
| 215 | `size_segment` | `fundraising_efficiency_w` | 0.00000 | 1 | 0.1759 | 117,509 | No |
