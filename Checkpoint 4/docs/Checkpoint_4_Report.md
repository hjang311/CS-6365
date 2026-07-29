# Checkpoint 4 Executive Report: Rolled Multi-Agent NORP Pipeline & Gated Hypothesis Verification

## 1. Domain & Core Research Question (RQ6 / Phase 3 Agentic Loop)

* **Domain Focus**: Autonomous agentic indicator discovery, spatial data acquisition, pre-registration, and gated statistical evaluation across sectoral datasets—joining NCCS CORE 990 filings (2018–2022, ~158K organization-years), IRS Business Master File (BMF), FDIC BankFind, Census ACS5, Zillow Home Value Index (ZHVI), Food Assistance cross-sections, and Housing Services NTEE classifications.
* **Core Research Question (RQ6)**: Can an LLM-driven multi-agent system autonomously discover candidate external indicators, acquire geo-spatial data feeds, and propose regression specifications without mid-run p-hacking, hallucinated statistical models, or direct execution of regression solvers by the LLM?
* **Hypothesis (Phase 3 Gated Evaluation)**: Grounded in spatial mismatch and organizational overhead literature, testing whether local social-infrastructure density (e.g. food banks, housing service providers per 10,000 residents) improves nonprofit fundraising efficiency (`fundraising_efficiency_w`), subject to a strict two-part statistical verifier gate.

---

## 2. Key Architecture & Scientific Safeguards

The project strictly completes the course's pedagogical **Manual $\rightarrow$ Unrolled $\rightarrow$ Rolled** progression model:

```
+-----------------------------------------------------------------------------------+
|  Phase 1: Manual Specialization (Checkpoint 2 & Checkpoint 3)                     |
|  - Human domain selection of indicators (ZHVI, IRS BMF provider counts)           |
|  - Automated data contract verification (Checkpoint 3/pipeline/04_validate_frame.py) |
|  - Hand-coded robust OLS models with size segmentation ($500K–$2M vs. ≥ $2M)         |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|  Phase 2: Unrolled Deterministic Execution (Checkpoint 3/08_unrolled_loop.py)     |
|  - List A (Curated Theory Agenda): Pre-registered hypotheses & control baselines   |
|  - List B (2-Variable Limitation Harness): Pre-registered candidate IV scanner    |
|  - Prevents mid-run LLM drift / hallucination via strict JSON pre-registration     |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|  Phase 3: Rolled Agentic Loop (Checkpoint 4 / 09_phase3_agentic_loop.py)          |
|  - Multi-agent team: Scout (discovery), Critic (ToS gate), Acquisition (ingest),  |
|    Researcher (proposals & interpretation), Stats Engine (HC1 OLS solver)         |
|  - Gated ACCEPT/REJECT verifier: Wald F (p < 0.05) AND ΔR² ≥ 5e-4 on identical rows|
+-----------------------------------------------------------------------------------+
```

### Four Hard Scientific Invariants

1. **LLM Never Fits OLS**: The LLM agent never directly computes statistical regressions or estimates parameters. A deterministic Python stats engine ([`Checkpoint 4/09_phase3_agentic_loop.py`](../09_phase3_agentic_loop.py)) performs all model estimations using **HC1 heteroskedasticity-robust standard errors**.
2. **Pre-Registration Before OLS**: All hypothesis proposals and control specifications are pre-registered into structured JSON manifests (`proposals_round1.json`) prior to model fitting, preventing post-hoc p-hacking.
3. **Higher-Order ACCEPT Gate Thresholds**: To achieve an **ACCEPT** verdict on a proposed higher-order indicator, the model must satisfy a dual statistical threshold on identical sample rows:
   $$\text{Wald } F \text{ test } p < 0.05 \quad \text{AND} \quad \Delta R^2 \ge 5 \times 10^{-4}$$
4. **First-Class REJECT Logging**: Rejections by the verifier gate or null findings are treated as first-class scientific outcomes. They are formally logged to `decision_log.jsonl` and summarized in [`NEGATIVE_FINDINGS.md`](NEGATIVE_FINDINGS.md) rather than discarded.

---

## 3. Key Scientific Findings & Empirical Case Studies

### Case Study 1: TA Verifier Suite (Synthetic Verification Benchmark)

The TA Verifier test suite evaluates the statistical verifier gate across pre-registered specifications (I1–I4 and Q1):

| Specification | Indicator Tested | Expected Outcome | Observed $\beta$ | Wald $F$ $p$-value | $\Delta R^2$ | Verifier Gate Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **I1** | Linear Indicator baseline | REJECT | $+0.0012$ | $0.214$ | $0.00011$ | **REJECT** ($p \ge 0.05$) |
| **I2** | Log Indicator baseline | REJECT | $+0.0024$ | $0.108$ | $0.00023$ | **REJECT** ($\Delta R^2 < 5\times 10^{-4}$) |
| **I3** | Interaction ($I_3 = X_1 \times \text{Size}$) | **ACCEPT** | **$+0.00512$** | **$0.0018$** | **$0.00392$** | **ACCEPT** ($\Delta R^2 \ge 5\times 10^{-4}$) |
| **I4** | Quadratic Indicator ($X_1^2$) | REJECT | $+0.00008$ | $0.452$ | $0.00004$ | **REJECT** ($\Delta R^2 < 5\times 10^{-4}$) |
| **Q1** | Quantile Binning | REJECT | $+0.00110$ | $0.310$ | $0.00009$ | **REJECT** ($p \ge 0.05$) |

* **Finding**: The verifier gate correctly isolates specification I3 as the single higher-order model meeting both the Wald $F$ significance and $\Delta R^2 \ge 5\times 10^{-4}$ magnitude thresholds on identical sample rows.

---

### Case Study 2: Food Assistance Atlanta Cross-Section (2-Round Agentic Loop)

* **Scout & Critic Operations**: The Scout agent identified local food bank indicators. When web scraping encountered login-walled directories, the Critic agent activated a **ToS Degraded Mode**, falling back to open named enrichment adapters (`cp4_atlanta_food_assistance_xsection.csv`).
* **Round 1 Results**:
  * Proposal F01 (`food_bank_count` linear): $\beta = +0.021, p = 0.412, R^2 = 0.1758$ $\rightarrow$ **Not Significant**.
  * Proposal F02 (`food_bank_density` per 10k): $\beta = +0.142, p = 0.038, \Delta R^2 = 0.00012$ $\rightarrow$ **REJECT** ($\Delta R^2 < 5\times 10^{-4}$).
* **Round 2 Results**: The Researcher agent proposed interaction terms with organizational revenue scale. The verifier gate maintained false-positive avoidance, rejecting marginal incremental predictors.

---

### Case Study 3: Housing Services Chicago (NTEE Universality Fallback)

* **Operational Fallback**: Demonstrates cross-sector applicability when local spatial web feeds are unavailable. The Acquisition agent gracefully degraded to NTEE sector classification counts from the committed modeling frame (`cp4_chicago_housing_services_xsection.csv`).
* **Results**:
  * Proposal H01 (`housing_provider_count` exploratory): $\beta = -0.045, p = 0.082$ $\rightarrow$ **Exploratory / Non-Significant**.
  * Proposal H02 (`housing_density_interaction`): $\beta = -0.012, p = 0.041, \Delta R^2 = 0.00018$ $\rightarrow$ **REJECT** ($\Delta R^2 < 5\times 10^{-4}$).

---

## 4. Pedagogical Benchmark & Takeaways

### Workflow Engineering vs. Prompt Engineering

| Dimension | Prompt Engineering (Traditional AI) | Workflow Engineering (This Repository) |
| :--- | :--- | :--- |
| **OLS Fitting** | LLM outputs regression numbers (risk of hallucination) | LLM writes JSON proposals; **Python engine fits OLS** |
| **Hypothesis Control** | Unconstrained LLM changes variables mid-run | Strict pre-registration into JSON before model fitting |
| **Quality Control** | Single $p$-value threshold ($p < 0.05$) | Dual gate: Wald $F$ $p < 0.05$ **AND** $\Delta R^2 \ge 5\times 10^{-4}$ |
| **Negative Results** | Discarded or retried until significant | Logged as first-class scientific findings (`NEGATIVE_FINDINGS.md`) |

---

### Measured Wall-Clock Run Profile across Stages

| Stage | What You Do | Wall-Clock Time | Primary Entrypoint |
| :--- | :--- | :---: | :--- |
| **Manual (Phase 1)** | Human hand-codes acquire $\rightarrow$ merge $\rightarrow$ clean $\rightarrow$ OLS per hypothesis | **Days–weeks per hypothesis** | [`Checkpoint 2/H2_Pipeline/`](../../Checkpoint%202/H2_Pipeline/), [`Checkpoint 3/docs/PHASE1_MANUAL_PIPELINE.md`](../../Checkpoint%203/docs/PHASE1_MANUAL_PIPELINE.md) |
| **Unrolled (Phase 2)** | Pre-registered List A/B + deterministic OLS engine | **Minutes per batch** | [`Checkpoint 3/08_unrolled_loop.py`](../../Checkpoint%203/08_unrolled_loop.py) |
| **Rolled (Phase 3)** | Multi-agent team discovery + gated OLS stats engine | **39 seconds** (offline) | [`bash Checkpoint 4/reproduce.sh`](../reproduce.sh) |

---

## Pointer & Historical Provenance

* **Student Onboarding Guide**: [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md)
* **Studio Layout & File Map**: [`STRUCTURE.md`](STRUCTURE.md)
* **Effort & Benchmark Comparison**: [`BENCHMARK.md`](BENCHMARK.md)
* **Negative Findings Log**: [`NEGATIVE_FINDINGS.md`](NEGATIVE_FINDINGS.md)
* **Curriculum Narrative**: [`docs/CURRICULUM.md`](../../docs/CURRICULUM.md)
* **Team Final Report (Gitignored Local Copy)**: `Checkpoint 4/report/CS6365_Checkpoint_4.docx` and `report/Checkpoint_4_Report.md`.
