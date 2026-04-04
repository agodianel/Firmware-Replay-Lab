"""ESP32 adapter — parse ESP-IDF serial output into replay bundle structures."""

from __future__ import annotations

import re
from typing import Any

from ..bundle import SerialLine

# ESP-IDF log format:  I (timestamp) tag: message
_IDF_LOG_RE = re.compile(r"^([EWIDV])\s+\((\d+)\)\s+([\w_]+):\s+(.*)$")

# Panic/abort patterns
_PANIC_RE = re.compile(r"Guru Meditation Error|abort\(\) was called|panic_abort|PANIC")
_BACKTRACE_RE = re.compile(r"^Backtrace:\s*(.+)$")
_RESET_RE = re.compile(r"^rst:(0x[\da-fA-F]+)\s+\((\w+)\)")
_WATCHDOG_RE = re.compile(r"Task watchdog got triggered|Watchdog timeout")


def parse_serial_log(raw_text: str) -> list[SerialLine]:
    """Parse ESP-IDF serial output into SerialLine entries."""
    lines: list[SerialLine] = []
    fallback_ts = 0

    for raw in raw_text.splitlines():
        line = raw.strip()
        if not line:
            continue

        match = _IDF_LOG_RE.match(line)
        if match:
            ts = int(match.group(2))
            fallback_ts = ts
        else:
            fallback_ts += 1
            ts = fallback_ts

        lines.append(SerialLine(
            timestamp_ms=ts,
            direction="device->host",
            message=line,
        ))

    return lines


def extract_events(serial_log: list[SerialLine]) -> list[dict[str, Any]]:
    """Extract structured events from parsed ESP32 serial lines."""
    events: list[dict[str, Any]] = []

    for line in serial_log:
        msg = line.message

        if _RESET_RE.match(msg):
            m = _RESET_RE.match(msg)
            assert m is not None
            events.append({
                "type": "reset",
                "timestamp_ms": line.timestamp_ms,
                "detail": m.group(2),
            })

        if _PANIC_RE.search(msg):
            events.append({
                "type": "panic",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _WATCHDOG_RE.search(msg):
            events.append({
                "type": "watchdog",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        bt = _BACKTRACE_RE.match(msg)
        if bt:
            events.append({
                "type": "backtrace",
                "timestamp_ms": line.timestamp_ms,
                "detail": bt.group(1),
            })

        idf = _IDF_LOG_RE.match(msg)
        if idf and idf.group(1) == "E":
            events.append({
                "type": "error",
                "timestamp_ms": line.timestamp_ms,
                "detail": f"{idf.group(3)}: {idf.group(4)}",
            })

    return events


def extract_metadata_hints(serial_log: list[SerialLine]) -> dict[str, str]:
    """Extract metadata hints from boot log (target, reset reason)."""
    hints: dict[str, str] = {}
    for line in serial_log:
        m = _RESET_RE.match(line.message)
        if m:
            hints["reset_reason"] = m.group(2)
        if "cpu_start" in line.message:
            hints.setdefault("target", "esp32")
    return hints
