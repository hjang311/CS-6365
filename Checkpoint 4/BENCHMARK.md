# Benchmark — Manual vs Unrolled vs Rolled

Pedagogical comparison for the next cohort. The point is **workflow / loop engineering**, not only finding a significant β.

## Your three stages in this repo

| Stage | What you do | Effort (honest) | Entry |
|-------|-------------|-----------------|-------|
| **Manual (Phase 1)** | For each hypothesis (H2, then H4, then H5), adjust acquire → merge → clean → specify → OLS by hand | **Days–weeks per hypothesis**; every column and control is a human edit | [`Checkpoint 2/H2_Pipeline/`](../Checkpoint%202/H2_Pipeline/), [`Checkpoint 3/PHASE1_MANUAL_PIPELINE.md`](../Checkpoint%203/PHASE1_MANUAL_PIPELINE.md), H4/H5 folders |
| **Unrolled (Phase 2)** | Pre-register List A/B, run one deterministic engine | **Setup once** (frame + lists); each batch is **minutes** | [`08_unrolled_loop.py`](../Checkpoint%203/08_unrolled_loop.py), `loop_results_v2/` |
| **Rolled (Phase 3)** | Agents scout / critic / acquire / propose / interpret; Stats engine + Verifier gate | Offline demos in **minutes** once the CP3 frame exists | [`reproduce.sh`](reproduce.sh), [`09_phase3_agentic_loop.py`](09_phase3_agentic_loop.py) |

### Measured run profile (this team, Jul 2026)

| Activity | Approximate wall-clock | Notes |
|----------|------------------------|-------|
| Manual H2 pipeline specialization | **Days** | New FDIC join + DV cleaning recipe |
| Manual H4 then H5 specialization | **Days each** | ZHVI + NTEE density + size splits |
| Unrolled `08 --validate` + `--run` | **Minutes** | After `cp3_modeling_frame.csv` exists |
| `bash Checkpoint 4/reproduce.sh` (4 steps) | **Typically a few minutes** | Preflight + validate + TA verify + food + housing; machine-dependent |
| First-time federal acquire (Mode B) | **Tens of minutes–hours** | Network + disk; not what “minutes” refers to |

**Methodology footnote:** “Days–weeks” = calendar time this team spent designing joins/cleaning/specs for each Manual hypothesis. “Minutes” = local wall-clock to *execute* engines once data and `.venv` exist. Re-time on your machine; `reproduce.sh` prints elapsed seconds at the end.

### Why Manual hurt

Phase 1 was not “run the same notebook three times.” H2 (bank density), H4 (ZHVI), and H5 (provider density) each required **manual pipeline specialization**—new sources, join keys, cleaning rules, and specs—before Phase 2 wrapped those recipes in a pre-registered loop. See [`PHASE1_MANUAL_PIPELINE.md`](../Checkpoint%203/PHASE1_MANUAL_PIPELINE.md).

### What Unrolled bought

List A (theory-first) and List B (limitation harness) are written to JSON **before** OLS. The LLM never invents coefficients. Large-n significance without explanatory gain becomes visible as a *method* limitation, not a discovery factory.

### What Rolled adds

Scout → Critic (ToS blocks) → named adapters → pre-register → `09 --run` → interpret. Higher-order specs face an HC1 Wald F + ΔR² ≥ 5e-4 **Verifier gate**. Negative / REJECT findings are first-class ([`NEGATIVE_FINDINGS.md`](NEGATIVE_FINDINGS.md)).

## Supporting OH case study (optional)

Earlier NORP cohorts spent roughly a **semester** on raw data → clean → SQL → validate → prompt-engineer by hand. That motivates automation. **Do not confuse that history with Phase 1 in this repo** — your Manual stage is H2/H4/H5 above. Checkpoint 0 is that prior-semester case study only.

## Honest caveats for students

1. Offline `reproduce.sh` demos assume a working CP3 modeling frame and Python deps (`.venv`). First-time data acquisition is still real work.
2. Live HTTP (Feed America) needs network and license respect; fixture / NTEE paths exist for offline teaching.
3. “Minutes” means *running the loop*, not *building the national frame from zero*.

## One-command rolled demos

```bash
# From repo root
bash "Checkpoint 4/reproduce.sh"
```

Then read [`STUDENT_QUICKSTART.md`](STUDENT_QUICKSTART.md) and [`docs/CURRICULUM.md`](../docs/CURRICULUM.md).
