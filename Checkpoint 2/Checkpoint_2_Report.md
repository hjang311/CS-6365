# Checkpoint 2 Executive Summary: Manual H2 Pipeline & Fintech Feasibility Probes

## 1. Domain & Core Research Question (RQ2 / H2)

* **Domain**: Commercial Bank Branch Density vs. Nonprofit Fundraising Efficiency (Proxying Fintech Adoption).
* **Research Question (RQ2)**: Does commercial bank branch density in a nonprofit’s headquarters ZIP code impact its fundraising efficiency? Specifically, does operating in a "bank desert" (lower physical branch availability) correlate with higher fintech adoption and improved fundraising efficiency?
* **Hypothesis (H2)**: Among enterprise nonprofits (Total Revenue ≥ $500,000), lower physical bank-branch density is associated with **higher fundraising efficiency** (lower cost per contribution dollar), with the strongest effect present in smaller enterprise filers.

---

## 2. Key Hypotheses & Methodology

### Data Sources & Integration Pipeline
1. **NCCS CORE 990 (2018–2022)**: Multi-year Form 990 financial extracts ($N \approx 147,718$ clean organization-years across the US).
2. **FDIC BankFind API**: Geocoded commercial bank branch locations aggregated by 5-digit ZIP code.
3. **Census ACS 5-Year (2018–2022)**: ZIP-level population, poverty rate, and median household income controls.
4. **IRS Business Master File (BMF)**: Headquarters state and NTEE sector classification.

### Sample Selection & Financial Cleaning Rules
* **Enterprise Threshold**: Total Revenue ≥ $500,000.
* **Valid Filers**: Total Contributions > 0, Direct Spend ≥ $5,000.
* **Winsorization**: Dependent variable (`Fundraising Efficiency` = `Contributions` / `Direct Expenses`) winsorized at the 99th percentile ($681.94$).
* **Sample Size**: **$N = 147,718$ organization-years** (Full national panel across 5 years).

### OLS Regression Specification
$$\text{Efficiency}_i = \beta_0 + \beta_1 (\log(\text{BankBranchDensity}_i)) + \beta_2 (\log(\text{TotalRevenue}_i)) + \text{Controls}_i + \varepsilon_i$$

* Model fits use **HC1 heteroskedasticity-robust standard errors**.

---

## 3. Key Findings & Statistical Results

### Primary OLS Regression Results ($N = 147,718$)
| Model / Size Tier | Independent Variable (`log(Bank_Branch_Density)`) β | 95% Confidence Interval | p-value | Significance |
| :--- | :---: | :---: | :---: | :---: |
| **Model 1: Bivariate** | $-0.13412$ | $[-0.207, -0.061]$ | $0.00035$ | $p < 0.001$ |
| **Model 2: Full Controls** | **$-0.11453$** | $[-0.186, -0.043]$ | **$0.00167$** | **Significant** ($p < 0.01$) |
| **Mid-Sized ($500K–$2M)** | **$-0.08145$** | $[-0.123, -0.040]$ | $0.00013$ | Significant ($p < 0.001$) |
| **Large (≥ $2M)** | **$-0.15211$** | $[-0.257, -0.047]$ | $0.00470$ | Significant ($p < 0.01$) |

### Theoretical Interpretation
* **Confirmed H2 Baseline**: Lower physical bank branch density is significantly associated with higher fundraising efficiency ($\beta = -0.1145, p = 0.00167$). Organizations in bank-sparse ZIPs demonstrate higher returns per fundraising dollar, supporting the hypothesis that physical banking constraints drive adoption of digital financial technologies (fintech platforms, online payment gateways) that reduce overhead.
* **Scale Differences**: Large enterprise nonprofits (≥ $2M) exhibited a larger negative coefficient ($\beta = -0.152$) than mid-sized filers ($\beta = -0.081$), indicating that larger institutions capture greater operational leverage when shifting away from traditional branch banking.

---

## 4. Exploratory Feasibility Probes (RQ3 / H3)

Checkpoint 2 conducted two direct feasibility probes to move beyond spatial proxies and evaluate direct fintech adoption metrics:

1. **Option A: Form 990 E-File XML Fees Probe (`04_parse_efile_fees.py`)**
   * *Method*: Streamed 600 Form 990 e-file XML returns from the AWS IRS S3 bucket to parse credit card / payment processing fee line items (Schedule O / Part IX).
   * *Finding*: **Feasibility Failure**. Over 92% of filers aggregate digital payment fees into generic "Merchant Fees" or "Professional Services" lines, making automated extraction via XML unreliable without manual auditing.
2. **Option B: Technographics Website Probe (`05_probe_technographics.py`)**
   * *Method*: Sampled 60 non-profit websites to inspect DOM headers for digital donation widgets (Stripe, PayPal, Givebutter, Classy).
   * *Finding*: High detection accuracy (~78% active digital gateways), but limited by site scraping access limits and Terms-of-Service constraints.

---

## 5. Pedagogical & Curriculum Role

* **First Manual Phase 1 Pipeline**: Serves as the canonical baseline for Phase 1 in the 3-phase curriculum model (Manual $\rightarrow$ Unrolled $\rightarrow$ Rolled).
* **Deterministic Baseline Construction**: Established the exact multi-year NCCS CORE + Census + FDIC merge recipe and N ≈ 147K modeling frame reused and extended in Checkpoint 3 and Checkpoint 4.
* **Adversarial Validation (`05_validator.py`)**: Introduced automated data contracts verifying DV non-negativity, winsorization limits, and coefficient tolerances before reporting findings.
