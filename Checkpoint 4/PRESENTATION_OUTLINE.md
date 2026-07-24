# Checkpoint 4 Presentation Outline

Education-first framing (July 22 OH Option 2): convince the next cohort that
**workflow / loop engineering** beats lone correlation hunting.

## Slide 1 — Title
NORP Agentic Data Exploration Pipeline — Checkpoint 4  
Team 1 · Phase 3 Rolled Loop · Reproducibility for the next cohort

## Slide 2 — Professor ask
Package an open-source teaching artifact.  
Show Manual vs Unrolled vs Rolled so students appreciate **workflow**, not only β.

## Slide 3 — Evolution (this project)
1. **Manual (Phase 1):** H2 → H4 → H5 — pipeline adjusted by hand per hypothesis  
2. **Unrolled (Phase 2):** List A/B pre-registered before OLS  
3. **Rolled (Phase 3):** agents discover/acquire/propose; deterministic gated OLS  

Point to `BENCHMARK.md` time/effort table.

## Slide 4 — One command
`bash "Checkpoint 4/reproduce.sh"`  
Future students reproduce calibration + Verifier + food + housing demos in minutes
(once the frame exists). Link `STUDENT_QUICKSTART.md`.

## Slide 5 — Scientific guardrails
- LLM never fits OLS — only `09 --run`  
- Proposals locked before results (pre-registration)  
- Higher-order Verifier: HC1 Wald F + ΔR² ≥ 5e-4 (ACCEPT/REJECT)

## Slide 6 — Multi-agent bus (brief)
Orchestrator · Scout · Critic · Acquisition · Researcher · Stats  
File “Slack”: `agent_bus/messages.jsonl`. Critic blocks high-ToS sources.

## Slide 7 — Demo: Food Atlanta
Feed America HTTP (licensed) + NTEE fallback; Atlanta × latest-year slice.  
**Null / REJECT** on food-density specs — documented, not buried.

## Slide 8 — Demo: Housing Chicago (universality)
Same protocol, new config; **NTEE-only by design** (no fake housing HTTP).  
Proves students can swap topic/geo without new hardcoded scripts.

## Slide 9 — Confirmed carry-forwards
RQ2 / RQ4 signals remain; Phase 2 two-var limitation still stands.  
TA gate: e.g. ZHVI × size (I3) can ACCEPT when ΔR² is real; tiny ΔR² REJECTs.

## Slide 10 — Open-source handoff
Clean curriculum path (`docs/CURRICULUM.md`).  
`HANDOFF_GUIDE.md` + configs + `.agent/skills/`.  
Personal research notes stay local — not part of the public package.
