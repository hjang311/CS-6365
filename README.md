# CS 6365 — NORP Agentic Data Exploration Pipeline

**Team 1** · Summer 2026 · Prof. Calton Pu  

Open-source **educational** package: Manual → Unrolled → Rolled workflow for
nonprofit (NORP) data exploration. The goal is to teach **loop engineering and
reproducibility**, not only to hunt significant correlations.

## Start here (next cohort)

1. Read [`docs/CURRICULUM.md`](docs/CURRICULUM.md)  
2. Skim [`Checkpoint 4/BENCHMARK.md`](Checkpoint%204/BENCHMARK.md)  
3. Run:

```bash
bash "Checkpoint 4/reproduce.sh"
```

4. Follow [`Checkpoint 4/STUDENT_QUICKSTART.md`](Checkpoint%204/STUDENT_QUICKSTART.md)

## Curriculum map

| Stage | Meaning | Path |
|-------|---------|------|
| **Manual (Phase 1)** | H2, H4, H5 — human adjusts the pipeline per hypothesis | [`Checkpoint 2/H2_Pipeline/`](Checkpoint%202/H2_Pipeline/), [`Checkpoint 3/PHASE1_MANUAL_PIPELINE.md`](Checkpoint%203/PHASE1_MANUAL_PIPELINE.md) |
| **Unrolled (Phase 2)** | Pre-registered List A/B + deterministic OLS | [`Checkpoint 3/08_unrolled_loop.py`](Checkpoint%203/08_unrolled_loop.py) |
| **Rolled (Phase 3)** | Multi-agent discover → acquire → propose → gated OLS | [`Checkpoint 4/`](Checkpoint%204/) |

## Repository layout

```
Checkpoint 0/     Reproducibility exercise (exemplar clones archived locally)
Checkpoint 1/     Early agentic experiments
Checkpoint 2/     Manual H2 / RQ2 pipeline
Checkpoint 3/     Manual H4/H5 + unrolled loop
Checkpoint 4/     Rolled multi-agent package (primary handoff)
docs/             Curriculum + archive notes
.agent/skills/    Phase 3 agent skills
archive/          Local historical clutter (bulky contents gitignored)
agentic_pipeline/ Legacy SDK scaffolding (not the Phase 3 entrypoint)
```

Personal office-hour notes (`Project Research & Initial Plan/`) are **local only**
and are not part of the public package.

## Course info

- **Instructor:** Dr. Calton Pu  
- **Team:** Hwando Jang, Carla Du Plessis  

## License / data ethics

Respect source licenses (e.g. Feed America CC BY). Do not scrape login-walled
partner directories. Named adapters + Critic ToS gates are intentional.
