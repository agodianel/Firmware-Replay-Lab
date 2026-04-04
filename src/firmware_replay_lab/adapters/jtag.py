"""JTAG adapter — parse JTAG debug trace output into replay bundle structures.

Handles common JTAG/GDB debug session output formats including:
- OpenOCD log messages
- GDB remote serial protocol session logs
- Memory read/write traces
- Breakpoint hit records
- Target halt/resume events
"""

from __future__ import annotations

import re
from typing import Any

from ..bundle import SerialLine

# OpenOCD log patterns
_OPENOCD_LOG_RE = re.compile(
    r"^(?:Info|Warn|Error|Debug)\s*:\s*(.*)"
)
_TARGET_HALT_RE = re.compile(
    r"target (?:state|halted)|halted due to|halt(?:ed)?|target was reset"
    , re.IGNORECASE
)
_BREAKPOINT_RE = re.compile(
    r"breakpoint|bkpt|hardware breakpoint|watchpoint"
    , re.IGNORECASE
)
_MEM_ACCESS_RE = re.compile(
    r"(?:read|write)\s+(?:memory|mem)\s+(?:at\s+)?0x([\da-fA-F]+)"
    r"|mdw\s+0x([\da-fA-F]+)"
    r"|mww\s+0x([\da-fA-F]+)"
    , re.IGNORECASE
)
_RESET_RE = re.compile(
    r"SRST|TRST|(?:system|target)\s+reset|jtag\s+reset"
    , re.IGNORECASE
)
_FLASH_RE = re.compile(
    r"flash\s+(?:write|erase|program)|wrote\s+\d+\s+bytes"
    , re.IGNORECASE
)
_REG_RE = re.compile(
    r"^\s*(r\d+|sp|lr|pc|cpsr|xpsr|msp|psp)\s*(?::\s*|\(\d+\)\s*[:=]\s*)(0x[\da-fA-F]+)"
    , re.IGNORECASE
)
# GDB output patterns
_GDB_FRAME_RE = re.compile(
    r"#(\d+)\s+(0x[\da-fA-F]+)\s+in\s+(\S+)"
)
_GDB_SIGNAL_RE = re.compile(
    r"Program received signal\s+(\w+)"
)


def parse_serial_log(raw_text: str) -> list[SerialLine]:
    """Parse JTAG/OpenOCD/GDB debug output into SerialLine entries."""
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
    """Extract structured events from JTAG debug output."""
    events: list[dict[str, Any]] = []

    for line in serial_log:
        msg = line.message

        if _TARGET_HALT_RE.search(msg):
            events.append({
                "type": "target_halt",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _BREAKPOINT_RE.search(msg):
            events.append({
                "type": "breakpoint",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _MEM_ACCESS_RE.search(msg):
            events.append({
                "type": "memory_access",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _RESET_RE.search(msg):
            events.append({
                "type": "reset",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _FLASH_RE.search(msg):
            events.append({
                "type": "flash_operation",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        reg = _REG_RE.match(msg)
        if reg:
            events.append({
                "type": "register_dump",
                "timestamp_ms": line.timestamp_ms,
                "detail": f"{reg.group(1).upper()}={reg.group(2)}",
            })

        frame = _GDB_FRAME_RE.match(msg)
        if frame:
            events.append({
                "type": "stack_frame",
                "timestamp_ms": line.timestamp_ms,
                "detail": f"#{frame.group(1)} {frame.group(3)} at {frame.group(2)}",
            })

        sig = _GDB_SIGNAL_RE.search(msg)
        if sig:
            events.append({
                "type": "signal",
                "timestamp_ms": line.timestamp_ms,
                "detail": sig.group(1),
            })

    return events


def extract_metadata_hints(serial_log: list[SerialLine]) -> dict[str, str]:
    """Extract metadata hints from JTAG debug output."""
    hints: dict[str, str] = {}
    hints["source"] = "jtag"
    for line in serial_log:
        if "openocd" in line.message.lower():
            hints["debugger"] = "openocd"
        elif "gdb" in line.message.lower():
            hints["debugger"] = "gdb"
        # Detect target from transport adapter mentions
        if "stm32" in line.message.lower():
            hints.setdefault("target", "stm32")
        elif "esp32" in line.message.lower() or "esp" in line.message.lower():
            hints.setdefault("target", "esp32")
        elif "nrf" in line.message.lower():
            hints.setdefault("target", "nrf")
    return hints
