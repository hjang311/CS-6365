# Checkpoint 1 Report — Executive Summary

## 1. Domain & Core Research Question (RQ1)

* **Core Research Question (RQ1)**: Does community broadband access rate significantly impact nonprofit fundraising efficiency? Specifically, does a nonprofit organization operating within a digitally disconnected or low-internet community suffer from measurably worse fundraising returns (manifested as a higher fundraising cost ratio)?
* **Domain Focus**: Sociological and socioeconomic analysis of U.S. nonprofit operational performance by joining external infrastructure metrics—Census ACS broadband coverage (Table B28002)—with tax-exempt financial disclosures from IRS Form 990 filings (Part IX functional expenses) and the National Center for Charitable Statistics (NCCS) CORE dataset.

---

## 2. Key Hypotheses & Methodology

### Hypotheses
* **Primary Hypothesis (H1 — Broadband Access vs. Fundraising Efficiency)**: Nonprofits located in ZIP Code Tabulation Areas (ZCTAs) with lower household broadband subscription rates experience lower fundraising efficiency (i.e., higher fundraising costs relative to total contributions collected).
* **Secondary / Scale Hypothesis**: Explores how financial technology adoption impacts small vs. enterprise-level nonprofits, addressing structural differences in how volunteer labor vs. paid fundraising operations record costs.

### Data Sources & Joining Logic
1. **IRS Business Master File (BMF)**: Georgia nonprofit roster.
2. **Census ACS API (Table B28002)**: Household broadband subscription percentages at the ZCTA level.
3. **NCCS CORE 2022**: Form 990 financial extracts (Total Revenue, Contributions, Fundraising Expenses, NTEE codes).
4. **Crosswalk Matching**: HUD ZIP-to-ZCTA crosswalk achieving a **99.5% row match rate**.

### Sample Characteristics & Data Filtering
* **Initial Joined Dataset**: 11,028 Georgia nonprofit records.
* **Final Analysis Sample ($N$)**: **457 organizations** after listwise deletion of records with zero/negative contributions, zero/negative total revenue, or missing/invalid community household counts.
* **Winsorization**: To prevent extreme outliers from skewing OLS estimates, the fundraising cost ratio (`Expenses` / `Contributions`) was winsorized at the 1st (`0.0000`) and 99th (`4.3375`) percentiles.

### OLS Regression Specification & Control Framework
$$\text{CostRatio}_i = \beta_0 + \beta_1 (\text{BroadbandRate}_i) + \beta_2 (\log(\text{TotalRevenue}_i)) + \sum \gamma_k (\text{NTEEDummy}_{i,k}) + \varepsilon_i$$

* **Dependent Variable ($Y$)**: Winsorized Fundraising Cost Ratio (`Fundraising Expenses` / `Contributions`).
* **Key Independent Variable ($X_1$)**: Community Broadband Subscription Rate (%).
* **Controls**: `log(Total Revenue)` to control for organizational size and financial scale, plus **NTEE Category Dummies** for sector-specific cost structures.

---

## 3. Key Findings & Statistical Results

### Correlation Analysis
| Test Type | Coefficient ($\beta$ / $\rho$) | p-value | Significance ($p < 0.05$) |
| :--- | :---: | :---: | :---: |
| **Pearson Correlation ($r$)** | `+0.0650` | `0.1656` | Not Significant |
| **Spearman Correlation ($\rho$)** | `-0.0273` | `0.5598` | Not Significant |

### OLS Regression Parameter Estimates ($N = 457$)
| Variable | Coefficient ($\beta$) | Std. Error | t-statistic | p-value | Conclusion |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Intercept (`const`)** | `-0.0433` | `0.457` | `-0.095` | `0.925` | Not Significant |
| **Broadband Subscription Rate** | `+0.3678` | `0.407` | `+0.904` | `0.367` | **Null Result** ($p > 0.05$) |
| **Log Total Revenue** | `-0.0016` | `0.020` | `-0.080` | `0.936` | Not Significant |

### Model Fit Summary
* **$R^2$**: `0.0432` (Model explains ~4.3% of variance in fundraising cost ratios).
* **Adjusted $R^2$**: `-0.0076` (Additional features do not improve fit beyond random chance).

### Null Result & Sociological Interpretation
* **Confirmed Null Result**: With $p = 0.367$, there is no statistically significant linear relationship between local community broadband coverage and nonprofit fundraising efficiency.
* **Sociological Insights**:
  1. **Geographic Uncoupling**: Modern nonprofit fundraising is non-local. Donors, foundation grants, and corporate sponsorships are solicited regionally or nationally rather than strictly from the nonprofit's immediate ZIP code.
  2. **Infrastructure Access**: Local residential broadband metrics do not restrict an organization's commercial internet access or digital operations.
  3. **Operational Heterogeneity**: Small community nonprofits often rely on uncompensated volunteer labor (resulting in zero reported fundraising expense), while enterprise nonprofits deploy dedicated paid staff.

---

## 4. Pedagogical & Curriculum Role

* **Initial Pipeline Iteration**: Served as the exploratory stage for agentic data collection using early Google Antigravity SDK patterns.
* **Architecture Evolution**: Pivoted from an unconstrained, fully autonomous LLM discovery concept to a robust **deterministic 4-stage programmatic engine**:
  1. `01_acquire_data.py`: Automated retrieval from IRS BMF, Census Broadband API, and NCCS CORE.
  2. `02_merge_pipeline.py`: ZIP-to-ZCTA crosswalk joining (99.5% match rate) and data cleaning.
  3. `03_analysis.py`: OLS regression engine with logarithmic scale controls and NTEE category dummies.
  4. `04_validator.py`: Programmatic data contract enforcer and statistical soundness checker.
* **Lessons Learned**: Null results provide critical scientific direction. The need for a national, multi-state scope led directly to the nationwide ZIP-level NCCS CORE frame established in Checkpoint 2.
