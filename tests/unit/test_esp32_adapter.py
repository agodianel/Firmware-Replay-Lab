"""Tests for ESP32 adapter."""

from firmware_replay_lab.adapters.esp32 import (
    parse_serial_log,
    extract_events,
    extract_metadata_hints,
)


ESP32_LOG = """\
rst:0x1 (POWERON_RESET)
I (25) boot: ESP-IDF v5.1
I (30) cpu_start: Starting scheduler
I (100) wifi: Wi-Fi initialized
E (5000) wifi: Connection timeout
I (5001) app: Retrying connection
Guru Meditation Error: Core  0 panic'ed
Backtrace: 0x400d1234:0x3ffb5678 0x400d5678:0x3ffb9abc
"""


def test_parse_serial_log_extracts_lines():
    lines = parse_serial_log(ESP32_LOG)
    assert len(lines) > 0
    assert all(line.direction == "device->host" for line in lines)
    assert any("wifi" in line.message.lower() for line in lines)


def test_parse_serial_log_extracts_timestamps():
    lines = parse_serial_log(ESP32_LOG)
    # IDF lines should have real timestamps
    idf_lines = [x for x in lines if "boot" in x.message or "wifi" in x.message]
    assert any(x.timestamp_ms > 0 for x in idf_lines)


def test_extract_events_finds_panic():
    lines = parse_serial_log(ESP32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "panic" in types


def test_extract_events_finds_reset():
    lines = parse_serial_log(ESP32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "reset" in types


def test_extract_events_finds_backtrace():
    lines = parse_serial_log(ESP32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "backtrace" in types


def test_extract_events_finds_error():
    lines = parse_serial_log(ESP32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "error" in types


def test_extract_metadata_hints():
    lines = parse_serial_log(ESP32_LOG)
    hints = extract_metadata_hints(lines)
    assert hints.get("target") == "esp32"
    assert hints.get("reset_reason") == "POWERON_RESET"
