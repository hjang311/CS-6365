# Evaluation Scoring Summary — NORP_Spring26_G5

## CS 6365: Checkpoint 0 — Reproducibility Exercise
**Evaluator:** Hwando Jang

---

## Scoring Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    NORP_Spring26_G5 Evaluation                  │
├────────────┬──────────────┬──────────────┬──────────────────────┤
│  Metric    │  Score       │  Max         │  Status              │
├────────────┼──────────────┼──────────────┼──────────────────────┤
│  Plan      │  90%         │  120%        │  ✅ Complete         │
│  Match     │  TBD         │  120%        │  ⏳ Pending          │
│  Factual   │  TBD         │  100%        │  ⏳ Pending          │
├────────────┼──────────────┼──────────────┼──────────────────────┤
│  Combined  │              │              │  ⏳ Pending          │
└────────────┴──────────────┴──────────────┴──────────────────────┘
```

---

## 1. Plan Score: 90% / 120% ✅

**Assessment:** Substantial

The project presents a genuine, well-scoped research question with a dual-component architecture (RAG pipeline + longitudinal crime analysis). Documentation is thorough (451 lines across README + INSTRUCTIONS). The CP2→CP3→CP4 analytical progression demonstrates methodological maturity. Deductions for disconnected components, no orchestration, thin RAG architecture, and unaddressed temporal data mismatch.

> *See detailed reasoning in: [scoring_explanations.md](scoring_explanations.md)*

---

## 2. Match Score: TBD / 120%

**Status:** Pending reproduction attempt (Day 3-4)

### Pre-Reproduction Notes:
- All 10 Python scripts present in repository
- Code analysis shows quality ranging from "Moderate" (main.py) to "Excellent" (cp4_analysis.py)
- Critical blocker: `data/combined_dataset.csv` missing — Component A may be non-functional
- Strict execution order required (no orchestration)
- Two API keys needed (Socrata + OpenRouter)

---

## 3. Factual Score: TBD / 100%

**Status:** Pending reproduction attempt (Day 3-4)

### Key Claims to Verify:
- [ ] CP2 produces 220 rows (22 districts × 10 years)
- [ ] CP3 panel has 140 rows (14 districts × 10 years)
- [ ] Hardship correlation: +0.349 (pre-2020) → +0.072 (post-2020)
- [ ] Income correlation: −0.241 → +0.120
- [ ] Model 1 R² ≈ 0.42
- [ ] Structural break confirmed via interaction term
- [ ] RAG pipeline generates valid SoQL queries

### Pre-Reproduction Risk:
The missing `combined_dataset.csv` (absent from both the GT fork AND the original repo at github.com/KhalidBargoti/NORP) will directly impact the Factual score for Component A claims.

---

## Combined Score Calculation

```
Combined Achievement = Plan × Match × Factual
                     = 0.90 × (TBD) × (TBD)
                     = TBD
```
