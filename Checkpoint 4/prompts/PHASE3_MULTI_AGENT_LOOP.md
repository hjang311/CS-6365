# Phase 3 Multi-Agent Rolled Loop — Master Hybrid Prompt

*Paste into Cursor / Antigravity. Paths assume repo root `CS-6365`.*

---

You are the **Orchestrator** for the NORP Phase 3 multi-agent rolled loop (`Checkpoint 4/`). Execute one enrichment + research round using sub-agents. Communicate only through files under `Checkpoint 4/phase3_results/agent_bus/` and the decision log.

## Non-negotiable invariants
1. You NEVER compute OLS coefficients. Only:
   ```bash
   .venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --run ...
   ```
2. Proposals JSON must be written **before** `--run`.
3. Acquisition uses **named adapters only** (no arbitrary DOM scrapers; no AccessFood bulk scrape).
4. Prefer Atlanta/ACFB-area × latest tax_year slice after site-stock enrichment.

## Agent roster (spawn as sub-agents; load matching `.agent/skills/norp-*/SKILL.md`)
| Role | Skill | Duty |
|------|-------|------|
| Scout | `norp-scout` | `source_candidates.json` |
| Critic | `norp-validator-agent` | `critic_verdict.json` |
| Acquisition | `norp-acquisition` | run adapters / `--acquire-plan` |
| Researcher | `norp-researcher` | propose + interpret |
| Code / Stats | `norp-code-agent` | invoke `09` CLI only |

## Steps
1. Ensure evaluation exists:
   ```bash
   .venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --evaluate
   ```
2. Write `Checkpoint 4/phase3_results/round_plan.json` with topic/geography/enrich intent (e.g. food_assistance / Atlanta).
3. **Scout** — web-search or fixture candidates for the topic; write `agent_bus/source_candidates.json`.
4. **Critic** — approve/block; write `critic_verdict.json`.
5. **Acquisition** — if approved:
   ```bash
   .venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
     --enrich-config "Checkpoint 4/configs/food_assistance_atlanta_http.json" \
     --out "Checkpoint 4/phase3_results"
   ```
   On HTTP failure the runner degrades to NTEE automatically — confirm `degrade` / fallback in the decision log.
6. **Researcher** — write `proposals_round1.json` (include ≥1 interaction; use new density IV if present).
7. **Stats** — run OLS on the active frame from `enriched_frame_manifest.json` via `09 --run` only. Higher-order specs are gated by HC1 Wald F + ΔR² ≥ 5e-4 (TA Verifier); read `gate_decision` in results.
8. **Researcher** — write `round1_interpretation.md` from results only (include gate ACCEPT/REJECT).
9. **Optional Round 2** — if Round 1 is null / gate REJECT, Researcher proposes **different** external IVs, pre-registers `proposals_round2.json`, Stats `--run --round 2`, interpret again.
10. Summarize bus trail: scout → critic (ToS blocks explicit) → acquire → proposals → run → interpret (or degrade events).

## Offline alternative
```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --all --fixture-full --rounds 2
```

## TA higher-order verification (optional)
```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" --verify-ta-specs \
  --frame "Checkpoint 3/data/cp3_modeling_frame.csv" \
  --out "Checkpoint 4/phase3_results/ta_verify"
```

## Universality check (second topic — NTEE-only by design)
```bash
.venv/bin/python "Checkpoint 4/09_phase3_agentic_loop.py" \
  --enrich-config "Checkpoint 4/configs/housing_services_chicago.json" \
  --all --fixture --rounds 1 \
  --out "Checkpoint 4/phase3_results/housing_chicago"
```
Housing has no open HTTP site census in-repo; empty `data/acquisitions/housing_services/` is expected.
