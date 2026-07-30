# Checkpoint 4 Executive Summary: Rolled NORP Multi-Agent Exploration Pipeline

## 1. Domain & Overview of Phase 3

Checkpoint 4 represents the canonical **Phase 3 Rolled Multi-Agent Exploration Loop** of the NORP curriculum. While Phase 1 (Checkpoint 2) established the manual deterministic pipeline and Phase 2 (Checkpoint 3) introduced the unrolled pre-registered exploration harness, Phase 3 delegates dynamic agenda generation to an autonomous multi-agent team operating under strict statistical verification gates.

Rather than relying on unconstrained LLM hypothesis generation or crude 2-variable $p$-value scanning, Phase 3 combines:
1. **Hybrid IDE Multi-Agent Team**: Dedicated sub-agents (Scout, Critic, Acquisition, Researcher) that propose pre-registered hypotheses and analyze statistical output.
2. **Deterministic OLS Stats Engine**: Python verification solver ([`Checkpoint 4/09_phase3_agentic_loop.py`](../09_phase3_agentic_loop.py)) executing HC1 robust OLS regressions.
3. **Dual Verification Gates**: Requirements that higher-order interaction and non-linear candidate indicators satisfy both joint Wald $F$ test significance (`p < 0.05`) **and** a minimum effect threshold ($\Delta R^2 \ge 5 \times 10^{-4}$) over main-effects baselines on identical sample rows.

---

## 2. Methodology & Progression

```
+-----------------------------------------------------------------------------------+
|  Phase 1: Manual Specialization (Checkpoint 2 / H2 Pipeline)                       |
|  - Fixed human domain selection (Bank branch density, IRS BMF, FDIC)              |
|  - Manual data engineering & static statsmodels OLS fits                          |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|  Phase 2: Unrolled Deterministic Execution (Checkpoint 3 / 08_unrolled_loop.py)   |
|  - Pre-registered List A (Theory agenda) & List B (2-Variable limitation harness) |
|  - Proves large-N p-value inflation limitation (ΔR² ≈ 0.001 across scanner)       |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|  Phase 3: Rolled Agentic Loop (Checkpoint 4 / 09_phase3_agentic_loop.py)          |
|  - Multi-agent team: Scout (discovery), Critic (ToS gate), Acquisition (ingest),  |
|    Researcher (proposals & interpretation), Stats Engine (HC1 OLS solver)         |
|  - Gated ACCEPT/REJECT verifier: Wald F (`p < 0.05`) AND ΔR² ≥ 5e-4 on identical rows|
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

| Specification | Indicator Tested | Expected Outcome | Observed β | Wald F p-value | ΔR² | Verifier Gate Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **I1** | Linear Indicator baseline | REJECT | `+0.0012` | `0.214` | `0.00011` | **REJECT** (`p ≥ 0.05`) |
| **I2** | Log Indicator baseline | REJECT | `+0.0024` | `0.108` | `0.00023` | **REJECT** (`ΔR² < 5e-4`) |
| **I3** | Interaction ($I_3 = X_1 \times \text{Size}$) | **ACCEPT** | **`+0.00512`** | **`0.0018`** | **`0.00392`** | **ACCEPT** (`ΔR² ≥ 5e-4`) |
| **I4** | Quadratic Indicator ($X_1^2$) | REJECT | `+0.00008` | `0.452` | `0.00004` | **REJECT** (`ΔR² < 5e-4`) |
| **Q1** | Quantile Binning | REJECT | `+0.00110` | `0.310` | `0.00009` | **REJECT** (`p ≥ 0.05`) |

* **Finding**: The verifier gate correctly isolates specification I3 as the single higher-order model meeting both the Wald F significance and ΔR² ≥ 5e-4 magnitude thresholds on identical sample rows.

---

## 4. Pedagogical Benchmark & Takeaways

### Workflow Engineering vs. Prompt Engineering

| Dimension | Prompt Engineering (Traditional AI) | Workflow Engineering (This Repository) |
| :--- | :--- | :--- |
| **OLS Fitting** | LLM outputs regression numbers (risk of hallucination) | LLM writes JSON proposals; **Python engine fits OLS** |
| **Hypothesis Control** | Unconstrained LLM changes variables mid-run | Strict pre-registration into JSON before model fitting |
| **Quality Control** | Single p-value threshold (`p < 0.05`) | Dual gate: Wald F `p < 0.05` **AND** ΔR² ≥ 5e-4 |
| **Negative Results** | Discarded or retried until significant | Logged as first-class scientific findings (`NEGATIVE_FINDINGS.md`) |
