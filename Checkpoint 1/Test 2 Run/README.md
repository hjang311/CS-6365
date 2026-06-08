# Test 2 Run — Standardized Survey-Weighted Reproduction (Test Case 1)

**Goal:** Re-run Gold-Standard Test Case 1 (Job Benefits vs. Staff Recruitment Impact)
so that **both LLM runners — Antigravity (Gemini) and Claude — produce the same result**,
matching the *Health of the U.S. Nonprofit Sector 2025* Figure 17 finding.

This is the follow-up to the first run, which exposed a cross-model discrepancy:

| Run | Method | Positive | Negative |
|-----|--------|---------:|---------:|
| Test 1 — Claude (initial) | **unweighted** | 74.9% | 16.2% |
| Test 1 — Antigravity | survey-weighted (`year4wt`) | 76.4% | 16.5% |
| **Test 2 — Claude (this run)** | **survey-weighted (`year4wt`)** | **76.4%** | **16.5%** |

Claude now matches Antigravity exactly. Report targets were ~76% / ~18%.

---

## Why the two models disagreed

The agent flow (Orchestrator → Code Agent → Validator Agent) was identical in both
environments. The *only* divergence was one analytical decision left to the model:

- **Antigravity** discovered and applied the dataset's survey weight (`year4wt`).
- **Claude** computed raw, unweighted percentages.

A second, subtler trap: a weighted share can be computed two different ways
(`mean()` of a 0/1 column vs. a ratio of summed weights), which can also disagree.

## How we standardized it

We removed all model discretion by pinning the exact computation in the prompt **and**
in `.agent/skills/norp-code-agent/SKILL.md` (so every future test case inherits it):

1. **Fixed weight column** — `year4wt` (precedence rule if absent: any numeric
   `*wt`/`*weight` column, reported explicitly).
2. **One weighting formula — summed-weight ratio, not a mean of a 0/1 column:**

   ```
   weighted_pct(group) = Σ year4wt[ Benefits_Health==1 & group ]
                         ────────────────────────────────────────  × 100
                                 Σ year4wt[ group ]
   ```

3. **Fixed cleaning order:** subset → numeric coerce → Likert map (1,2→Negative;
   3→No Impact; 4,5→Positive; codes 97/98 = missing) → listwise-drop analysis columns
   → **then** drop null/≤0/non-finite weights → report `n`.
4. **Audit + Validator gate:** always print weighted *and* unweighted side-by-side, and
   the Validator Agent independently re-derives the weighted shares and **rejects** any
   result that only matches the unweighted number (reproducibility band:
   Positive ∈ [0.74, 0.79], Negative ∈ [0.14, 0.20]).

With these four rules fixed, both environments are forced down the same numerical path.

---

## Result (this run)

- **Weight column:** `year4wt` (n=3,043; min 0.57, max 2.51, no nulls)
- **Weighted (official):** Positive **76.44%**, Negative **16.49%**, No Impact 24.07%
- **Unweighted (audit):** Positive 74.87%, Negative 16.22%
- **Significance:** χ²(2, N=3,043) = 970.5, p ≈ 1.8×10⁻²¹¹, Cramér's V = 0.565 (large)
- **Validator Agent:** 7/7 Data Contract assertions PASS → **APPROVED**

## Files

- `README.md` — this summary
- `tc1_weighted.py` — the standardized weighted analysis script
- `cleaned_test_case_1_weighted.csv` — validated output (3,043 rows;
  `Benefits_Health`, `BenefitsImpact_label`, `year4wt`)
