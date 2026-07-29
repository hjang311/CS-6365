"""
enrichment_tools — Generic data enrichment for the Phase 3 rolled agentic loop.
"""
from __future__ import annotations

from enrichment_tools.ntee_density import compute_ntee_density
from enrichment_tools.merge_density import merge_density_into_frame, entities_to_density
from enrichment_tools.geographic import get_metro_zips
from enrichment_tools.slice_frame import slice_frame
from enrichment_tools.http_open_api import run_http_open_api
from enrichment_tools.web_download import web_download_entities, load_manual_entities
from enrichment_tools.agent_bus import append_bus_message, load_latest_payload, write_payload

__all__ = [
    "compute_ntee_density",
    "merge_density_into_frame",
    "entities_to_density",
    "get_metro_zips",
    "slice_frame",
    "run_http_open_api",
    "web_download_entities",
    "load_manual_entities",
    "append_bus_message",
    "load_latest_payload",
    "write_payload",
]
