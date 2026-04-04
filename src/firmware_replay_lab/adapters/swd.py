"""SWD adapter — parse SWD/SWO trace output into replay bundle structures.

Handles common SWD debug and trace formats including:
- SWO ITM trace output (stimulus ports)
- SWD memory access logs
- DWT data trace / PC sampling
- Exception trace packets
- SEGGER J-Link log output
- PyOCD session logs
"""

from __future__ import annotations

import re
from typing import Any

from ..bundle import SerialLine

# SWO/ITM patterns
_ITM_PORT_RE = re.compile(
    r"ITM\s+(?:port|stimulus|channel)\s*(\d+)\s*[:]\s*(.*)"
    , re.IGNORECASE
)
_SWO_TIMESTAMP_RE = re.compile(
    r"(?:SWO|SWD)\s+(?:ts|timestamp)\s*[:=]\s*(\d+)"
    , re.IGNORECASE
)
# DWT patterns
_DWT_PC_RE = re.compile(
    r"PC\s*[:=]\s*(0x[\da-fA-F]+)"
    r"|DWT\s+PC\s+sample\s+(0x[\da-fA-F]+)"
    , re.IGNORECASE
)
_DWT_DATA_RE = re.compile(
    r"DWT\s+(?:data\s+)?(?:read|write)\s+(?:at\s+)?(0x[\da-fA-F]+)\s*[:=]\s*(0x[\da-fA-F]+)"
    , re.IGNORECASE
)
_EXCEPTION_RE = re.compile(
    r"exception\s+(?:entry|exit|return)\s*[:]\s*(\d+)"
    r"|exception\s+(\d+)\s+(?:entered|exited)"
    , re.IGNORECASE
)
# J-Link patterns
_JLINK_RE = re.compile(
    r"J-Link\s*[:>]"
    r"|SEGGER"
    , re.IGNORECASE
)
_JLINK_CONNECT_RE = re.compile(
    r"(?:connected|connecting)\s+(?:to|via)\s+SWD"
    r"|SWD\s+(?:selected|detected)"
    r"|target\s+(?:connected|identified)"
    , re.IGNORECASE
)
# PyOCD patterns
_PYOCD_RE = re.compile(
    r"pyocd"
    , re.IGNORECASE
)
# Fault / halt patterns
_FAULT_RE = re.compile(
    r"HardFault|BusFault|MemManage|UsageFault|SecureFault"
    , re.IGNORECASE
)
_HALT_RE = re.compile(
    r"target\s+halt|halt(?:ed)|debug\s+halt"
    , re.IGNORECASE
)
# Memory access
_MEM_RE = re.compile(
    r"(?:mem|memory)\s+(?:read|write|rd|wr)\s+(?:at\s+)?(0x[\da-fA-F]+)"
    , re.IGNORECASE
)


def parse_serial_log(raw_text: str) -> list[SerialLine]:
    """Parse SWD/SWO trace output into SerialLine entries."""
    lines: list[SerialLine] = []
    ts = 0

    for raw in raw_text.splitlines():
        line = raw.strip()
        if not line:
            continue

        # Try to extract SWO timestamp
        swo = _SWO_TIMESTAMP_RE.search(line)
        if swo:
            ts = int(swo.group(1))
        else:
            ts += 1

        lines.append(SerialLine(
            timestamp_ms=ts,
            direction="device->host",
            message=line,
        ))

    return lines


def extract_events(serial_log: list[SerialLine]) -> list[dict[str, Any]]:
    """Extract structured events from SWD/SWO trace output."""
    events: list[dict[str, Any]] = []

    for line in serial_log:
        msg = line.message

        itm = _ITM_PORT_RE.search(msg)
        if itm:
            events.append({
                "type": "itm_output",
                "timestamp_ms": line.timestamp_ms,
                "detail": f"port {itm.group(1)}: {itm.group(2).strip()}",
            })

        dwt_pc = _DWT_PC_RE.search(msg)
        if dwt_pc:
            addr = dwt_pc.group(1) or dwt_pc.group(2)
            events.append({
                "type": "pc_sample",
                "timestamp_ms": line.timestamp_ms,
                "detail": addr,
            })

        dwt_data = _DWT_DATA_RE.search(msg)
        if dwt_data:
            events.append({
                "type": "data_trace",
                "timestamp_ms": line.timestamp_ms,
                "detail": f"{dwt_data.group(1)}={dwt_data.group(2)}",
            })

        exc = _EXCEPTION_RE.search(msg)
        if exc:
            exc_num = exc.group(1) or exc.group(2)
            events.append({
                "type": "exception_trace",
                "timestamp_ms": line.timestamp_ms,
                "detail": f"exception {exc_num}",
            })

        if _FAULT_RE.search(msg):
            events.append({
                "type": "fault",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _HALT_RE.search(msg):
            events.append({
                "type": "target_halt",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _MEM_RE.search(msg):
            events.append({
                "type": "memory_access",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

        if _JLINK_CONNECT_RE.search(msg):
            events.append({
                "type": "connection",
                "timestamp_ms": line.timestamp_ms,
                "detail": msg,
            })

    return events


def extract_metadata_hints(serial_log: list[SerialLine]) -> dict[str, str]:
    """Extract metadata hints from SWD trace output."""
    hints: dict[str, str] = {}
    hints["source"] = "swd"
    for line in serial_log:
        msg = line.message.lower()
        if _JLINK_RE.search(line.message):
            hints["debugger"] = "jlink"
        elif _PYOCD_RE.search(line.message):
            hints["debugger"] = "pyocd"
        if "stm32" in msg:
            hints.setdefault("target", "stm32")
        elif "nrf" in msg:
            hints.setdefault("target", "nrf")
        elif "lpc" in msg:
            hints.setdefault("target", "lpc")
    return hints
