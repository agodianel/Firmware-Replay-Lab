"""STM32 adapter — parse HAL/LL serial output and HardFault dumps."""

from __future__ import annotations

import re
from typing import Any

from ..bundle import SerialLine

# Common STM32 log patterns
_HAL_ERROR_RE = re.compile(r"HAL\s+Error|Error_Handler|HAL_(\w+)_ErrorCallback")
_HARDFAULT_RE = re.compile(r"HardFault|Hard\s*Fault|MemManage|BusFault|UsageFault")
_REGISTER_RE = re.compile(r"^\s*(R\d+|SP|LR|PC|xPSR|MSP|PSP)\s*[:=]\s*(0x[\da-fA-F]+)")
_ASSERT_RE = re.compile(r"assert_failed|ASSERT|assert_param")
_CLOCK_RE = re.compile(r"SYSCLK\s*[:=]\s*(\d+)")


def parse_serial_log(raw_text: str) -> list[SerialLine]:
    """Parse STM32 serial output into SerialLine entries."""
    lines: list[SerialLine] = []
    ts = 0

    for raw in raw_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        lines.append(SerialLine(
            timestamp_ms=ts,
            direction="device->host",
            message=line,
        ))
        ts += 1

    return lines


def extract_events(serial_log: list[SerialLine]) -> list[dict[str, Any]]:
    """Extract structured events from parsed STM32 serial lines."""
    events: list[dict[str, Any]] = []

    for line in serial_log:
        msg = line.message

        if _HARDFAULT_RE.search(msg):
            events.append({
                "type": "hardfault",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _HAL_ERROR_RE.search(msg):
            events.append({
                "type": "hal_error",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _ASSERT_RE.search(msg):
            events.append({
                "type": "assert_failed",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        reg = _REGISTER_RE.match(msg)
        if reg:
            events.append({
                "type": "register_dump",
                "timestamp_ms": line.timestamp_ms,
                "detail": f"{reg.group(1)}={reg.group(2)}",
            })

    return events


def extract_metadata_hints(serial_log: list[SerialLine]) -> dict[str, str]:
    """Extract metadata hints from STM32 boot output."""
    hints: dict[str, str] = {}
    hints["target"] = "stm32"
    for line in serial_log:
        if _CLOCK_RE.search(line.message):
            m = _CLOCK_RE.search(line.message)
            if m and m.group(1):
                hints["sysclk_hz"] = m.group(1)
    return hints
