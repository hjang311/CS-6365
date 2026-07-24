"""Enrichment / scout / acquire / critic commands for Phase 3 (imported by 09)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

from enrichment_tools.agent_bus import append_bus_message, load_latest_payload, write_payload
from enrichment_tools.geographic import get_metro_zips
from enrichment_tools.http_open_api import run_http_open_api
from enrichment_tools.merge_density import (
    entities_to_density,
    merge_density_into_frame,
    write_enriched_frame,
)
from enrichment_tools.ntee_density import compute_ntee_density
from enrichment_tools.slice_frame import slice_frame
from enrichment_tools.web_download import load_manual_entities, web_download_entities

TOPIC_NTEE_MAP: dict[str, list[str]] = {
    "food_assistance": ["K30", "K31", "K34", "K35", "K36"],
    "soup_kitchens": ["K30", "K31", "K36"],
    "housing_services": ["L20", "L21", "L22", "L25", "L40", "L41"],
    "digital_literacy": ["B70", "B80", "B90"],
    "substance_abuse": ["F20", "F21", "F22", "F30"],
}

FIXTURE_SCOUT_CANDIDATES: dict[str, list[dict[str, Any]]] = {
    "food_assistance|atlanta": [
        {
            "rank": 1,
            "name": "AccessFood login-walled partner census",
            "url": "https://accessfood.example/partners",
            "license": "unknown / ToS-restricted",
            "format": "html_widget",
            "join_key": "zip",
            "recommended_adapter": "manual_hybrid",
            "tos_risk": "high",
            "notes": "Login-walled bulk scrape; Critic must block (fixture ToS demo).",
        },
        {
            "rank": 2,
            "name": "Feed America GA bulk API",
            "url": "https://feedam.org/api/resources/bulk",
            "license": "CC BY 4.0",
            "format": "json_api",
            "join_key": "zip",
            "recommended_adapter": "http_open_api",
            "tos_risk": "low",
            "notes": "Public bulk endpoint; pantry-class types; no API key.",
        },
        {
            "rank": 3,
            "name": "IRS BMF NTEE food assistance",
            "url": "local:irs_bmf.csv",
            "license": "public IRS BMF",
            "format": "local_csv",
            "join_key": "ZIP5",
            "recommended_adapter": "ntee_density",
            "tos_risk": "none",
            "ntee_prefixes": ["K30", "K31", "K34", "K35", "K36"],
            "notes": "Offline fallback; coarser than site lists.",
        },
    ],
    "housing_services|chicago": [
        {
            "rank": 1,
            "name": "IRS BMF NTEE housing services",
            "url": "local:irs_bmf.csv",
            "license": "public IRS BMF",
            "format": "local_csv",
            "join_key": "ZIP5",
            "recommended_adapter": "ntee_density",
            "tos_risk": "none",
            "ntee_prefixes": ["L20", "L21", "L22", "L25", "L40", "L41"],
            "notes": "Universal offline lane for housing density.",
        },
    ],
}

FIXTURE_PROPOSALS_FOOD = [
    {
        "id": "F01",
        "spec_type": "two_var",
        "iv": "log_food_assistance_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "rationale": (
            "Finer-granularity food-assistance density (NTEE or Feed America) "
            "vs fundraising efficiency on Atlanta cross-section."
        ),
    },
    {
        "id": "F02",
        "spec_type": "interaction",
        "iv1": "poverty_rate",
        "iv2": "log_food_assistance_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "rationale": "Higher-order: poverty may intensify food-assistance density association.",
    },
]

# Round 2 after food nulls: different external IVs already on the Atlanta frame.
FIXTURE_PROPOSALS_FOOD_R2 = [
    {
        "id": "F2P01",
        "spec_type": "two_var",
        "iv": "log_zhvi_2022",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "negative",
        "rationale": (
            "Round 1 food-density nulls → adapt: re-test H4 housing-cost signal "
            "on the Atlanta × latest-year slice."
        ),
    },
    {
        "id": "F2P02",
        "spec_type": "interaction",
        "iv1": "log_zhvi_2022",
        "iv2": "log_bank_branch_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": (
            "Higher-order adaptation: does bank sparsity moderate the ZHVI "
            "overhead effect on the Atlanta cross-section?"
        ),
    },
]

FIXTURE_PROPOSALS_HOUSING = [
    {
        "id": "H01",
        "spec_type": "two_var",
        "iv": "log_housing_services_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": (
            "Universality demo: Chicago-area housing-services NTEE density "
            "vs fundraising efficiency (exploratory)."
        ),
    },
    {
        "id": "H02",
        "spec_type": "interaction",
        "iv1": "poverty_rate",
        "iv2": "log_housing_services_density",
        "dv": "fundraising_efficiency_w",
        "expected_direction": "unspecified",
        "rationale": "Higher-order: poverty may moderate housing-provider density.",
    },
]

SOURCE_TO_ADAPTER = {
    "ntee": "ntee_density",
    "ntee_density": "ntee_density",
    "http": "http_open_api",
    "http_open_api": "http_open_api",
    "mcp": "http_open_api",
    "web": "web_download",
    "web_download": "web_download",
    "manual": "manual_hybrid",
    "manual_hybrid": "manual_hybrid",
}


class EnrichmentContext:
    """Paths + logging callbacks injected from 09."""

    def __init__(
        self,
        *,
        data_dir: Path,
        bmf_path: Path,
        acs_path: Path,
        utc_now: Callable[[], str],
        append_decision: Callable,
        load_frame: Callable,
    ):
        self.data_dir = data_dir
        self.bmf_path = bmf_path
        self.acs_path = acs_path
        self.utc_now = utc_now
        self.append_decision = append_decision
        self.load_frame = load_frame


def _log_degrade(ctx: EnrichmentContext, out_dir: Path, reason: str, **extra: Any) -> None:
    ctx.append_decision(out_dir, {"event": "degrade", "reason": reason, **extra})
    append_bus_message(
        out_dir,
        from_agent="orchestrator",
        to_agent="researcher",
        msg_type="degrade",
        payload={"reason": reason, **extra},
        note=reason,
    )
    print(f"DEGRADE: {reason}")


def cmd_scout(
    ctx: EnrichmentContext,
    out_dir: Path,
    topic: str,
    geography: str,
    use_fixture: bool = True,
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    key = f"{topic.strip().lower()}|{geography.strip().lower()}"
    candidates = list(FIXTURE_SCOUT_CANDIDATES.get(key, []))

    if not candidates:
        prefixes = TOPIC_NTEE_MAP.get(topic.strip().lower())
        if prefixes:
            candidates = [
                {
                    "rank": 1,
                    "name": f"IRS BMF NTEE {topic}",
                    "url": "local:irs_bmf.csv",
                    "license": "public IRS BMF",
                    "format": "local_csv",
                    "join_key": "ZIP5",
                    "recommended_adapter": "ntee_density",
                    "tos_risk": "none",
                    "ntee_prefixes": prefixes,
                    "notes": "Auto-generated NTEE fallback candidate.",
                }
            ]

    payload = {
        "topic": topic,
        "geography": geography,
        "source": "fixture" if use_fixture else "live_or_empty",
        "generated_at": ctx.utc_now(),
        "candidates": candidates,
    }
    path = write_payload(out_dir, "source_candidates.json", payload)
    append_bus_message(
        out_dir,
        from_agent="scout",
        to_agent="critic",
        msg_type="source_candidates",
        payload_path=path,
        note=f"{len(candidates)} candidates for {topic}/{geography}",
    )
    ctx.append_decision(
        out_dir,
        {
            "event": "scout",
            "topic": topic,
            "geography": geography,
            "n_candidates": len(candidates),
            "path": str(path),
        },
    )
    print(f"Scout wrote {len(candidates)} candidates → {path}")
    if not candidates:
        _log_degrade(ctx, out_dir, "scout_empty", topic=topic, geography=geography)
    return 0


def cmd_critic_sources(
    ctx: EnrichmentContext, out_dir: Path, auto_approve: bool = True
) -> int:
    cand = load_latest_payload(out_dir, "source_candidates")
    direct = out_dir / "agent_bus" / "source_candidates.json"
    if cand is None and direct.exists():
        cand = json.loads(direct.read_text(encoding="utf-8"))

    if cand is None:
        _log_degrade(ctx, out_dir, "critic_no_candidates")
        verdict: dict[str, Any] = {
            "approved": False,
            "reason": "no source_candidates",
            "chosen": None,
            "blocked": [],
        }
        path = write_payload(out_dir, "critic_verdict.json", verdict)
        append_bus_message(
            out_dir,
            from_agent="critic",
            to_agent="orchestrator",
            msg_type="critic_verdict",
            payload_path=path,
            note=verdict.get("reason", ""),
        )
        ctx.append_decision(
            out_dir,
            {"event": "critic", "approved": False, "path": str(path)},
        )
        print(f"Critic verdict → {path} (approved=False)")
        return 0

    candidates = sorted(cand.get("candidates") or [], key=lambda c: c.get("rank", 99))
    if not candidates:
        verdict = {
            "approved": False,
            "reason": "empty candidates",
            "chosen": None,
            "blocked": [],
        }
        _log_degrade(ctx, out_dir, "critic_empty_candidates")
        path = write_payload(out_dir, "critic_verdict.json", verdict)
        append_bus_message(
            out_dir,
            from_agent="critic",
            to_agent="orchestrator",
            msg_type="critic_verdict",
            payload_path=path,
            note=verdict.get("reason", ""),
        )
        ctx.append_decision(
            out_dir,
            {"event": "critic", "approved": False, "path": str(path)},
        )
        print(f"Critic verdict → {path} (approved=False)")
        return 0

    blocked: list[dict[str, Any]] = []
    chosen: Optional[dict[str, Any]] = None
    for c in candidates:
        risk = str(c.get("tos_risk", "")).lower()
        if risk in ("high", "forbidden"):
            blocked.append(c)
            # Explicit reject event for the ToS decoy (bus trail evidence).
            block_verdict = {
                "approved": False,
                "reason": f"tos_risk={c.get('tos_risk')}",
                "chosen": c,
                "topic": cand.get("topic"),
                "geography": cand.get("geography"),
                "blocked": list(blocked),
            }
            bpath = write_payload(out_dir, "critic_verdict_blocked.json", block_verdict)
            append_bus_message(
                out_dir,
                from_agent="critic",
                to_agent="orchestrator",
                msg_type="critic_verdict",
                payload_path=bpath,
                note=block_verdict["reason"],
            )
            ctx.append_decision(
                out_dir,
                {
                    "event": "critic",
                    "approved": False,
                    "reason": block_verdict["reason"],
                    "path": str(bpath),
                },
            )
            _log_degrade(
                ctx, out_dir, "critic_blocked_tos", chosen=c.get("name")
            )
            continue
        chosen = c
        break

    if chosen is None:
        verdict = {
            "approved": False,
            "reason": "all_candidates_blocked",
            "chosen": None,
            "blocked": blocked,
            "topic": cand.get("topic"),
            "geography": cand.get("geography"),
        }
    elif not auto_approve:
        verdict = {
            "approved": False,
            "reason": "manual_review_required",
            "chosen": chosen,
            "blocked": blocked,
            "topic": cand.get("topic"),
            "geography": cand.get("geography"),
        }
    else:
        reason = "auto_approve_lowest_eligible_rank"
        if blocked:
            reason = (
                f"blocked_{len(blocked)}_high_tos_then_approved_rank_"
                f"{chosen.get('rank')}"
            )
        verdict = {
            "approved": True,
            "reason": reason,
            "chosen": chosen,
            "blocked": blocked,
            "topic": cand.get("topic"),
            "geography": cand.get("geography"),
        }

    path = write_payload(out_dir, "critic_verdict.json", verdict)
    append_bus_message(
        out_dir,
        from_agent="critic",
        to_agent="acquisition" if verdict.get("approved") else "orchestrator",
        msg_type="critic_verdict",
        payload_path=path,
        note=verdict.get("reason", ""),
    )
    ctx.append_decision(
        out_dir,
        {"event": "critic", "approved": verdict.get("approved"), "path": str(path)},
    )
    print(f"Critic verdict → {path} (approved={verdict.get('approved')})")
    return 0


def build_plan_from_verdict(verdict: dict[str, Any], label: str) -> dict[str, Any]:
    chosen = verdict.get("chosen") or {}
    adapter = chosen.get("recommended_adapter", "ntee_density")
    topic = verdict.get("topic") or label
    geography = verdict.get("geography") or "national"
    plan: dict[str, Any] = {
        "adapter": adapter,
        "topic": topic,
        "geography": geography,
        "label": label,
        "ntee_prefixes": chosen.get("ntee_prefixes")
        or TOPIC_NTEE_MAP.get(str(topic).lower(), []),
    }
    if adapter == "http_open_api":
        plan["http"] = {
            "base_url": chosen.get("url")
            or "https://feedam.org/api/resources/bulk",
            "query_params": {"state": "GA", "format": "json"},
            "type_param": "type",
            "type_values": [
                "food_pantry",
                "soup_kitchen",
                "food_bank",
                "mobile_pantry",
            ],
            "zip_field": "zip",
            "resource_key": "resources",
            "host_allowlist": ["feedam.org"],
            "attribution_text": (
                "Feed America (feedam.org) resource data, CC BY 4.0. "
                "Retrieved via NORP Phase 3 http_open_api adapter."
            ),
        }
    if adapter == "web_download":
        plan["url"] = chosen.get("url")
        plan["attribution_text"] = chosen.get("notes", "")
    if adapter == "manual_hybrid":
        plan["manual_csv"] = chosen.get("url", "")
    return plan


def cmd_acquire(
    ctx: EnrichmentContext,
    frame_path: Path,
    out_dir: Path,
    plan_path: Optional[Path] = None,
    write_slice: bool = True,
) -> tuple[Path, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx.data_dir.mkdir(parents=True, exist_ok=True)

    plan: Optional[dict[str, Any]] = None
    if plan_path and plan_path.exists():
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    else:
        verdict_path = out_dir / "agent_bus" / "critic_verdict.json"
        if verdict_path.exists():
            verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
            if not verdict.get("approved"):
                _log_degrade(ctx, out_dir, "acquire_skipped_critic_block")
                return frame_path, 0
            label = (verdict.get("topic") or "topic").replace(" ", "_")
            plan = build_plan_from_verdict(verdict, label)
            write_payload(out_dir, "acquisition_plan.json", plan)
        else:
            _log_degrade(ctx, out_dir, "acquire_no_plan")
            return frame_path, 0

    assert plan is not None
    if "adapter" not in plan and "source" in plan:
        plan["adapter"] = SOURCE_TO_ADAPTER.get(plan["source"], plan["source"])

    adapter = plan.get("adapter", "ntee_density")
    label = str(plan.get("label") or plan.get("topic") or "topic").replace(" ", "_")
    geography = str(plan.get("geography") or "national")
    acq_dir = ctx.data_dir / "acquisitions" / label
    acq_dir.mkdir(parents=True, exist_ok=True)

    previous_adapter = None
    man_existing = out_dir / "agent_bus" / "enriched_frame_manifest.json"
    if man_existing.exists():
        try:
            previous_adapter = json.loads(
                man_existing.read_text(encoding="utf-8")
            ).get("adapter")
        except Exception:
            previous_adapter = None

    append_bus_message(
        out_dir,
        from_agent="acquisition",
        to_agent="critic",
        msg_type="acquire_start",
        payload={"adapter": adapter, "label": label},
    )

    try:
        density_df = None
        entity_meta: dict[str, Any] = {}
        geo_zips = get_metro_zips(geography, ctx.acs_path, ctx.data_dir)
        geo_arg = geo_zips if geo_zips else None

        if adapter == "ntee_density":
            prefixes = plan.get("ntee_prefixes") or TOPIC_NTEE_MAP.get(
                str(plan.get("topic", "")).lower(), []
            )
            if not prefixes:
                raise ValueError(f"No NTEE prefixes for topic={plan.get('topic')}")
            density_df = compute_ntee_density(
                ctx.bmf_path, ctx.acs_path, prefixes, geo_arg, label=label
            )
            entity_meta = {"adapter": "ntee_density", "ntee_prefixes": prefixes}

        elif adapter == "http_open_api":
            http_cfg = plan.get("http") or {}
            csv_path, entity_meta = run_http_open_api(http_cfg, acq_dir, label=label)
            entities = pd.read_csv(csv_path, dtype={"ZIP5": str})
            if geo_arg:
                entities = entities[entities["ZIP5"].isin(set(geo_arg))]
            density_df = entities_to_density(entities, ctx.acs_path, label=label)

        elif adapter == "web_download":
            url = plan.get("url")
            if not url:
                raise ValueError("web_download plan missing url")
            csv_path, entity_meta = web_download_entities(
                url,
                acq_dir,
                label=label,
                attribution_text=plan.get("attribution_text", ""),
            )
            entities = pd.read_csv(csv_path, dtype=str)
            density_df = entities_to_density(entities, ctx.acs_path, label=label)

        elif adapter == "manual_hybrid":
            man = Path(plan.get("manual_csv") or "")
            entities = load_manual_entities(man)
            density_df = entities_to_density(entities, ctx.acs_path, label=label)
            entity_meta = {"adapter": "manual_hybrid", "manual_csv": str(man)}

        else:
            raise ValueError(f"Unknown adapter: {adapter}")

        dens_path = ctx.data_dir / f"{label}_density_by_zip.csv"
        density_df.to_csv(dens_path, index=False)

        frame = ctx.load_frame(frame_path)
        enriched = merge_density_into_frame(frame, density_df, label=label)
        enriched_path = ctx.data_dir / f"cp4_frame_with_{label}_density.csv"
        write_enriched_frame(enriched, enriched_path)

        active = enriched_path
        slice_meta: dict[str, Any] = {}
        if write_slice and geo_arg:
            prefer = (
                "GA"
                if geography.lower() == "atlanta"
                else ("IL" if geography.lower() == "chicago" else None)
            )
            sliced, slice_meta = slice_frame(
                enriched, geography_zips=geo_arg, prefer_state=prefer
            )
            if slice_meta.get("degraded"):
                _log_degrade(
                    ctx,
                    out_dir,
                    "slice_n_below_min",
                    n=slice_meta.get("n_rows"),
                    fallback="enriched_national_frame",
                )
                active = enriched_path
            else:
                slice_path = (
                    ctx.data_dir / f"cp4_{geography.lower()}_{label}_xsection.csv"
                )
                sliced.to_csv(slice_path, index=False)
                active = slice_path

        manifest = {
            "label": label,
            "adapter": adapter,
            "entity_meta": entity_meta,
            "density_path": str(dens_path),
            "enriched_frame": str(enriched_path),
            "active_frame": str(active),
            "slice_meta": slice_meta,
            "generated_at": ctx.utc_now(),
        }
        if previous_adapter and previous_adapter != adapter:
            manifest["previous_adapter"] = previous_adapter
            manifest["overwrite_note"] = (
                f"last-write-wins: {previous_adapter} → {adapter}"
            )
        man_path = write_payload(out_dir, "enriched_frame_manifest.json", manifest)
        append_bus_message(
            out_dir,
            from_agent="acquisition",
            to_agent="researcher",
            msg_type="enriched_frame_manifest",
            payload_path=man_path,
            note=f"active_frame={active}",
        )
        acquire_evt: dict[str, Any] = {
            "event": "acquire",
            "adapter": adapter,
            "label": label,
            "frame": str(active),
        }
        if previous_adapter and previous_adapter != adapter:
            acquire_evt["previous_adapter"] = previous_adapter
            acquire_evt["overwrite"] = True
        ctx.append_decision(out_dir, acquire_evt)
        ctx.append_decision(
            out_dir, {"event": "enrich", "label": label, "frame": str(active)}
        )
        print(f"Acquisition OK → active frame {active}")
        return Path(active), 0

    except Exception as exc:
        print(f"Acquisition FAILED: {exc}", file=__import__("sys").stderr)
        ctx.append_decision(
            out_dir, {"event": "acquire", "status": "error", "error": str(exc)}
        )
        topic = str(plan.get("topic") or label)
        prefixes = plan.get("ntee_prefixes") or TOPIC_NTEE_MAP.get(topic.lower())
        if prefixes and adapter != "ntee_density":
            print("Falling back to ntee_density…")
            try:
                fallback_plan = {
                    "adapter": "ntee_density",
                    "topic": topic,
                    "geography": geography,
                    "label": label,
                    "ntee_prefixes": prefixes,
                }
                fp = write_payload(out_dir, "acquisition_plan_fallback.json", fallback_plan)
                return cmd_acquire(
                    ctx, frame_path, out_dir, plan_path=fp, write_slice=write_slice
                )
            except Exception as exc2:
                _log_degrade(ctx, out_dir, "ntee_fallback_failed", error=str(exc2))
                return frame_path, 0
        _log_degrade(ctx, out_dir, "acquire_failed", error=str(exc))
        return frame_path, 0


def cmd_enrich_config(
    ctx: EnrichmentContext,
    frame_path: Path,
    out_dir: Path,
    config_path: Path,
) -> tuple[Path, int]:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    if "enrichments" in cfg:
        active = frame_path
        for item in cfg["enrichments"]:
            plan = {
                "adapter": SOURCE_TO_ADAPTER.get(
                    item.get("source") or item.get("adapter") or "ntee_density",
                    item.get("source") or item.get("adapter") or "ntee_density",
                ),
                "topic": item.get("topic"),
                "geography": item.get("geography", "national"),
                "label": item.get("label") or item.get("topic"),
                "ntee_prefixes": item.get("ntee_prefixes"),
                "http": item.get("http"),
                "url": item.get("url"),
                "manual_csv": item.get("manual_csv"),
                "attribution_text": item.get("attribution_text"),
            }
            plan_path = write_payload(
                out_dir,
                f"acquisition_plan_{plan['label']}.json",
                plan,
            )
            active, _ = cmd_acquire(ctx, active, out_dir, plan_path=plan_path)
        return active, 0

    if "adapter" not in cfg and "source" in cfg:
        cfg["adapter"] = SOURCE_TO_ADAPTER.get(cfg["source"], cfg["source"])
    plan_path = write_payload(out_dir, "acquisition_plan.json", cfg)
    return cmd_acquire(ctx, frame_path, out_dir, plan_path=plan_path)


def cmd_fixture_full_bus(
    ctx: EnrichmentContext,
    out_dir: Path,
    topic: str = "food_assistance",
    geography: str = "atlanta",
) -> int:
    cmd_scout(ctx, out_dir, topic, geography, use_fixture=True)
    cmd_critic_sources(ctx, out_dir, auto_approve=True)
    verdict_path = out_dir / "agent_bus" / "critic_verdict.json"
    verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
    cands = (load_latest_payload(out_dir, "source_candidates") or {}).get(
        "candidates"
    ) or []
    ntee = next(
        (c for c in cands if c.get("recommended_adapter") == "ntee_density"), None
    )
    if ntee:
        verdict["chosen"] = ntee
        verdict["approved"] = True
        verdict["reason"] = "fixture_full_force_ntee_offline"
        write_payload(out_dir, "critic_verdict.json", verdict)
    label = topic.replace(" ", "_")
    plan = build_plan_from_verdict(verdict, label)
    plan["adapter"] = "ntee_density"
    write_payload(out_dir, "acquisition_plan.json", plan)
    append_bus_message(
        out_dir,
        from_agent="orchestrator",
        to_agent="acquisition",
        msg_type="acquisition_plan",
        payload=plan,
        note="fixture_full offline NTEE plan",
    )
    print("fixture-full bus payloads ready (scout→critic→plan)")
    return 0
