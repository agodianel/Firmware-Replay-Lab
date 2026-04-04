from __future__ import annotations

from pathlib import Path

from .bundle import ReplayBundle, SerialLine


def append_serial_log_from_text(bundle: ReplayBundle, log_text: str) -> None:
    start_ts = bundle.serial_log[-1].timestamp_ms + 1 if bundle.serial_log else 0
    for idx, raw in enumerate(log_text.splitlines()):
        line = raw.strip("\n")
        if not line:
            continue
        bundle.serial_log.append(
            SerialLine(timestamp_ms=start_ts + idx, direction="device->host", message=line)
        )


def append_serial_log_from_file(bundle: ReplayBundle, log_file: str | Path) -> None:
    payload = Path(log_file).read_text(encoding="utf-8")
    append_serial_log_from_text(bundle, payload)
