# Empirical Report: Broadband Access x Fundraising Efficiency (Georgia 2022)

This report details the statistical findings from our empirical analysis of the relationship between community broadband access rates and nonprofit fundraising efficiency in the state of Georgia. 

## Executive Summary
* **Hypothesis**: Non-profit organizations located in communities with lower broadband internet access have lower fundraising efficiency (which manifests as a higher fundraising cost ratio: expenses divided by contributions).
* **Finding**: **No statistically significant relationship was found.** Neither Pearson/Spearman correlations nor control-adjusted OLS regressions show a significant effect of broadband access rates on fundraising cost ratios at the standard 5% significance level.

---

## Sample Characteristics
* **Initial Joined Dataset**: 11,028 organizations (IRS BMF Georgia matched with NCCS CORE 2022 and Census ZCTA).
* **Final Analysis Sample**: **457 organizations** (after listwise deletion of organizations with zero/negative contributions, zero/negative total revenue, or zero/negative community households).
* **Winsorization**: The fundraising functional cost ratio (Expenses / Contributions) was winsorized at the 1st and 99th percentiles (1st pct: `0.0000`, 99th pct: `4.3375`) to mitigate the leverage of extreme outliers.

---

## Statistical Results

### 1. Correlation Analysis
We conducted both parametric (Pearson) and non-parametric (Spearman) correlation tests between the community broadband subscription rate and the winsorized fundraising cost ratio.

| Test | Coefficient (r / rho) | p-value | Significance |
| :--- | :---: | :---: | :---: |
| **Pearson Correlation** | `0.0650` | `0.1656` | Not Significant ($p > 0.05$) |
| **Spearman Correlation** | `-0.0273` | `0.5598` | Not Significant ($p > 0.05$) |

### 2. OLS Regression Model (with Controls)
To control for confounding variables, we estimated an Ordinary Least Squares (OLS) regression model. 
* **Dependent Variable ($Y$)**: Winsorized Fundraising Cost Ratio (Expenses / Contributions).
* **Key Independent Variable ($X_1$)**: Community Broadband Subscription Rate (%).
* **Control Variables**:
  * **Log of Total Revenue** (control for organization size/scale).
  * **NTEE Category Dummies** (control for sector/activity type, base category = Category A, e.g., Arts/Culture).

#### Model Fit Summary
* **$R^2$**: `0.0432` (The model explains ~4.3% of the variance in fundraising cost ratios).
* **Adjusted $R^2$**: `-0.0076` (Indicates that the added variables do not improve model fit beyond chance).

#### Parameter Estimates
| Variable | Coefficient | Std. Error | t-statistic | p-value | Significance |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Intercept (const)** | `-0.0433` | `0.457` | `-0.095` | `0.925` | Not Significant |
| **Broadband Subscription Rate** | `0.3678` | `0.407` | `0.904` | `0.367` | Not Significant |
| **Log of Total Revenue** | `-0.0016` | `0.020` | `-0.080` | `0.936` | Not Significant |

*(Note: Coefficients for the NTEE category dummies were all statistically insignificant ($p > 0.05$); full parameters are stored in `results.json`.)*

---

## Discussion & Sociological Interpretation

The sociological hypothesis suggested that nonprofits in digitally disconnected communities face systemic disadvantages in soliciting online contributions, leading to lower fundraising efficiency (higher cost-to-contribution ratios). 

However, our findings do not support this hypothesis:
1. **Lack of Significance**: The p-value for the broadband rate in the regression model is `0.367`, meaning there is a 36.7% probability of observing this relationship by random chance.
2. **Direction of Coefficient**: The positive coefficient of the broadband rate (`0.3678`) actually points in the opposite direction of the hypothesis (suggesting higher broadband is weakly associated with *higher* cost ratios, though this is not statistically meaningful).
3. **Implications**: Fundraising is a highly nationalized/regionalized activity. A nonprofit located in a low-broadband ZIP code in Georgia does not necessarily solicit donors exclusively from that ZIP code. Large donors, institutional grants, and regional foundations are often accessed outside of the immediate community. Furthermore, local broadband access does not restrict a nonprofit's internal ability to access high-speed internet (e.g., through commercial business lines or mobile cellular networks) for digital campaigns.
