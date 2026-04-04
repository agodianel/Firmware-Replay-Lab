"""Tests for JTAG adapter."""

from firmware_replay_lab.adapters.jtag import (
    parse_serial_log,
    extract_events,
    extract_metadata_hints,
)


JTAG_LOG = """\
Info: Listening on port 3333 for gdb connections
Info: target state: halted
Info: target halted due to debug-request, current mode: Thread
Info: flash write at 0x08000000, len=32768
Info: wrote 32768 bytes from file firmware.elf
breakpoint set at 0x08001234
#0 0x08001234 in main () at main.c:42
#1 0x08000abc in Reset_Handler () at startup.s:120
Program received signal SIGTRAP
PC: 0x08001234
LR: 0x08000abc
stm32 device detected
"""


def test_parse_serial_log():
    lines = parse_serial_log(JTAG_LOG)
    assert len(lines) > 0
    assert all(line.direction == "device->host" for line in lines)


def test_extract_events_finds_halt():
    lines = parse_serial_log(JTAG_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "target_halt" in types


def test_extract_events_finds_breakpoint():
    lines = parse_serial_log(JTAG_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "breakpoint" in types


def test_extract_events_finds_flash():
    lines = parse_serial_log(JTAG_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "flash_operation" in types


def test_extract_events_finds_stack_frame():
    lines = parse_serial_log(JTAG_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "stack_frame" in types


def test_extract_events_finds_signal():
    lines = parse_serial_log(JTAG_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "signal" in types


def test_extract_events_finds_register():
    lines = parse_serial_log(JTAG_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "register_dump" in types


def test_extract_metadata_hints():
    lines = parse_serial_log(JTAG_LOG)
    hints = extract_metadata_hints(lines)
    assert hints.get("source") == "jtag"
    assert hints.get("target") == "stm32"
