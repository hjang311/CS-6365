"""File-based multi-agent message bus (Slack analogue)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def utc_now() -> str:
    """Canonical bus/decision timestamp format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def bus_dir(out_dir: Path) -> Path:
    d = out_dir / "agent_bus"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _bus_fingerprint(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record.get("from"),
        record.get("to"),
        record.get("type"),
        record.get("round"),
        record.get("payload_path"),
        record.get("note"),
    )


def append_bus_message(
    out_dir: Path,
    *,
    from_agent: str,
    to_agent: str,
    msg_type: str,
    round_n: Optional[int] = None,
    payload_path: Optional[Path | str] = None,
    payload: Optional[dict[str, Any]] = None,
    note: str = "",
) -> Path:
    """
    Append one message to agent_bus/messages.jsonl.
    Optionally write payload JSON beside the bus and reference it.
    Skips identical consecutive duplicates (same agents/type/path/note).
    """
    d = bus_dir(out_dir)
    path_ref: Optional[str] = None
    if payload is not None:
        fname = f"{msg_type}"
        if round_n is not None:
            fname += f"_round{round_n}"
        fname += ".json"
        p = d / fname
        # avoid overwrite collisions
        if p.exists():
            stamp = datetime.now(timezone.utc).strftime("%H%M%S")
            p = d / f"{p.stem}_{stamp}{p.suffix}"
        p.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
        path_ref = str(p)
    elif payload_path is not None:
        path_ref = str(payload_path)

    record = {
        "ts": utc_now(),
        "from": from_agent,
        "to": to_agent,
        "type": msg_type,
        "round": round_n,
        "payload_path": path_ref,
        "note": note,
    }
    msg_path = d / "messages.jsonl"
    if msg_path.exists():
        lines = msg_path.read_text(encoding="utf-8").strip().splitlines()
        if lines:
            try:
                prev = json.loads(lines[-1])
                if _bus_fingerprint(prev) == _bus_fingerprint(record):
                    return msg_path
            except json.JSONDecodeError:
                pass
    with open(msg_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return msg_path


def load_latest_payload(
    out_dir: Path,
    msg_type: str,
    round_n: Optional[int] = None,
) -> Optional[dict[str, Any]]:
    """Scan messages.jsonl newest-first for a matching type; load its JSON payload."""
    msg_path = bus_dir(out_dir) / "messages.jsonl"
    if not msg_path.exists():
        return None
    lines = msg_path.read_text(encoding="utf-8").strip().splitlines()
    for line in reversed(lines):
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("type") != msg_type:
            continue
        if round_n is not None and rec.get("round") != round_n:
            continue
        pp = rec.get("payload_path")
        if not pp:
            continue
        p = Path(pp)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def write_payload(out_dir: Path, name: str, payload: dict[str, Any]) -> Path:
    d = bus_dir(out_dir)
    path = d / name
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return path
