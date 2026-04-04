"""Tests for SWD adapter."""

from firmware_replay_lab.adapters.swd import (
    parse_serial_log,
    extract_events,
    extract_metadata_hints,
)


SWD_LOG = """\
J-Link: Connected to target via SWD
SWD selected, speed=4000 kHz
target connected: STM32L476RG
ITM port 0: Sensor init OK
ITM port 0: Reading data
DWT PC sample 0x08001234
DWT data read at 0x20000100: 0x0000FFFF
exception entry: 3
HardFault detected
exception 16 entered
target halt due to breakpoint
memory read at 0x08000000
SWD timestamp: 5000
ITM stimulus channel 1: Debug checkpoint
"""


def test_parse_serial_log():
    lines = parse_serial_log(SWD_LOG)
    assert len(lines) > 0
    assert all(line.direction == "device->host" for line in lines)


def test_swo_timestamp_extraction():
    lines = parse_serial_log(SWD_LOG)
    ts_line = [x for x in lines if "timestamp" in x.message.lower()]
    assert len(ts_line) > 0
    assert ts_line[0].timestamp_ms == 5000


def test_extract_events_finds_itm():
    lines = parse_serial_log(SWD_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "itm_output" in types


def test_extract_events_finds_pc_sample():
    lines = parse_serial_log(SWD_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "pc_sample" in types


def test_extract_events_finds_data_trace():
    lines = parse_serial_log(SWD_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "data_trace" in types


def test_extract_events_finds_exception_trace():
    lines = parse_serial_log(SWD_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "exception_trace" in types


def test_extract_events_finds_fault():
    lines = parse_serial_log(SWD_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "fault" in types


def test_extract_events_finds_connection():
    lines = parse_serial_log(SWD_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "connection" in types


def test_extract_metadata_hints():
    lines = parse_serial_log(SWD_LOG)
    hints = extract_metadata_hints(lines)
    assert hints.get("source") == "swd"
    assert hints.get("debugger") == "jlink"
    assert hints.get("target") == "stm32"
