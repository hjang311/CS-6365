"""Generic paginated open HTTP API adapter (generalized from pull_feedam_ga)."""
from __future__ import annotations

import csv
import json
import ssl
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional


def _http_get_json(url: str, retries: int = 3, timeout: int = 60) -> dict:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "NORP-CS6365-Phase3-research/1.0"},
            )
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            try:
                proc = subprocess.run(
                    ["curl", "-sL", "--max-time", str(timeout), url],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    return json.loads(proc.stdout)
                last_err = RuntimeError(proc.stderr or f"curl exit {proc.returncode}")
            except Exception as e2:
                last_err = e2
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed GET {url}: {last_err}")


def _http_get_bytes(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "NORP-CS6365-Phase3-research/1.0"}
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read()
    except Exception:
        proc = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), url],
            capture_output=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout:
            return proc.stdout
        raise


def run_http_open_api(
    config: dict[str, Any],
    out_dir: Path,
    label: str = "topic",
) -> tuple[Path, dict[str, Any]]:
    """
    Execute a configured open API pull.

    Config keys (Feed America–style example):
      base_url, query_params (dict), page_param, limit_param, limit,
      resource_key (default 'resources'), type_values (optional list → iterate),
      type_param, state_param / fixed query fields,
      zip_field (default 'zip'), name_field, map_fields (optional),
      attribution_text, host_allowlist (optional list of host substrings)
    """
    base_url = config["base_url"]
    if not str(base_url).startswith("https://"):
        raise ValueError("http_open_api requires HTTPS base_url")

    allow = config.get("host_allowlist") or []
    if allow and not any(h in base_url for h in allow):
        raise ValueError(f"base_url host not in allowlist: {base_url}")

    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"{label}_http_raw.jsonl"
    csv_path = out_dir / f"{label}_http_entities.csv"
    attr_path = out_dir / f"{label}_ATTRIBUTION.txt"
    attr_text = config.get(
        "attribution_text",
        f"Retrieved via http_open_api from {base_url}",
    )
    attr_path.write_text(attr_text + "\n", encoding="utf-8")

    resource_key = config.get("resource_key", "resources")
    zip_field = config.get("zip_field", "zip")
    page_param = config.get("page_param", "page")
    limit_param = config.get("limit_param", "limit")
    limit = int(config.get("limit", 1000))
    type_values = config.get("type_values") or [None]
    type_param = config.get("type_param", "type")
    base_params = dict(config.get("query_params") or {})

    all_rows: list[dict] = []
    with open(raw_path, "w", encoding="utf-8") as raw_f:
        for tval in type_values:
            page = 1
            while True:
                params = dict(base_params)
                params[limit_param] = limit
                params[page_param] = page
                if tval is not None:
                    params[type_param] = tval
                qs = urllib.parse.urlencode(params)
                url = f"{base_url}?{qs}" if "?" not in base_url else f"{base_url}&{qs}"
                payload = _http_get_json(url)
                resources = payload.get(resource_key) or []
                if not isinstance(resources, list):
                    raise RuntimeError(f"Expected list at key {resource_key}")
                for r in resources:
                    raw_f.write(json.dumps(r) + "\n")
                    all_rows.append(r if isinstance(r, dict) else {"value": r})
                if len(resources) < limit:
                    break
                page += 1
                time.sleep(float(config.get("sleep_s", 0.2)))

    # Normalize to entity CSV with ZIP5
    fields = ["name", "organization", "address", "city", "state", "ZIP5", "resource_type", "source_id"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in all_rows:
            zip_raw = str(r.get(zip_field) or r.get("ZIP5") or r.get("zipcode") or "")
            zip5 = "".join(c for c in zip_raw if c.isdigit())[:5].zfill(5) if zip_raw else ""
            w.writerow(
                {
                    "name": r.get(config.get("name_field", "name")) or "",
                    "organization": r.get("organization") or "",
                    "address": r.get("address") or "",
                    "city": r.get("city") or "",
                    "state": r.get("state") or "",
                    "ZIP5": zip5 if zip5 != "00000" else "",
                    "resource_type": r.get("resource_type") or r.get(type_param) or "",
                    "source_id": r.get("id") or "",
                }
            )

    meta = {
        "adapter": "http_open_api",
        "n_records": len(all_rows),
        "raw_path": str(raw_path),
        "csv_path": str(csv_path),
        "attribution_path": str(attr_path),
        "base_url": base_url,
    }
    if len(all_rows) == 0:
        raise RuntimeError(f"http_open_api returned 0 records from {base_url}")
    return csv_path, meta
