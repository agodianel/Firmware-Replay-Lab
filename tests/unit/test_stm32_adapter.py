"""Tests for STM32 adapter."""

from firmware_replay_lab.adapters.stm32 import (
    parse_serial_log,
    extract_events,
    extract_metadata_hints,
)


STM32_LOG = """\
SystemClockConfig: SYSCLK=168000000
HAL_Init OK
Sensor init complete
HardFault Handler entered
R0: 0x00000000
R1: 0x20001234
LR: 0x08001234
PC: 0x08005678
HAL Error in SPI callback
assert_failed: file main.c, line 42
"""


def test_parse_serial_log_extracts_lines():
    lines = parse_serial_log(STM32_LOG)
    assert len(lines) > 0
    assert all(line.direction == "device->host" for line in lines)


def test_extract_events_finds_hardfault():
    lines = parse_serial_log(STM32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "hardfault" in types


def test_extract_events_finds_hal_error():
    lines = parse_serial_log(STM32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "hal_error" in types


def test_extract_events_finds_assert_failed():
    lines = parse_serial_log(STM32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "assert_failed" in types


def test_extract_events_finds_register_dump():
    lines = parse_serial_log(STM32_LOG)
    events = extract_events(lines)
    types = [e["type"] for e in events]
    assert "register_dump" in types


def test_extract_metadata_hints():
    lines = parse_serial_log(STM32_LOG)
    hints = extract_metadata_hints(lines)
    assert hints.get("target") == "stm32"
    assert hints.get("sysclk_hz") == "168000000"
