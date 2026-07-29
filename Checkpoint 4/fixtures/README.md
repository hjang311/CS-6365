# Fixture payloads (reference)

This directory does **not** store separate JSON fixture files.

Offline Scout candidates for `--fixture` / `--fixture-full` are embedded in
[`../engine/phase3_enrichment_cmds.py`](../engine/phase3_enrichment_cmds.py)
(`FIXTURE_SCOUT_CANDIDATES` and related proposal fixtures).

`--fixture-full` writes them to `phase3_results/*/agent_bus/source_candidates.json`
and forces the NTEE acquisition plan so the full bus runs without network.

**Run door:** `bash "Checkpoint 4/reproduce.sh"`  
**Extend door:** add fixtures in engine code (or new configs) — keep named adapters only.
