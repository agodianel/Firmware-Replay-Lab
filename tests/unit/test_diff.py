"""Tests for bundle diff analysis."""

from firmware_replay_lab.bundle import ReplayBundle, SessionMetadata, SerialLine
from firmware_replay_lab.diff import diff_bundles


def _make_bundle(**overrides):
    defaults = {
        "metadata": SessionMetadata(
            target="esp32", firmware_version="v1.0", board="devkitc", commit="abc"
        ),
        "serial_log": [
            SerialLine(timestamp_ms=0, direction="device->host", message="boot ok"),
        ],
        "events": [{"type": "reset", "timestamp_ms": 0}],
        "assertions": [{"kind": "contains_text", "text": "boot"}],
        "notes": ["test note"],
    }
    defaults.update(overrides)
    return ReplayBundle(**defaults)


def test_identical_bundles():
    a = _make_bundle()
    b = _make_bundle()
    report = diff_bundles(a, b)
    assert len(report.differences) == 0


def test_different_target():
    a = _make_bundle()
    b = _make_bundle(
        metadata=SessionMetadata(
            target="stm32", firmware_version="v1.0", board="devkitc", commit="abc"
        )
    )
    report = diff_bundles(a, b)
    assert any("target" in d.description for d in report.differences)


def test_different_log_count():
    a = _make_bundle()
    b = _make_bundle(serial_log=[
        SerialLine(timestamp_ms=0, direction="device->host", message="a"),
        SerialLine(timestamp_ms=1, direction="device->host", message="b"),
    ])
    report = diff_bundles(a, b)
    assert any("line count" in d.description for d in report.differences)


def test_different_event_types():
    a = _make_bundle(events=[{"type": "panic", "timestamp_ms": 100}])
    b = _make_bundle(events=[{"type": "reset", "timestamp_ms": 100}])
    report = diff_bundles(a, b)
    assert any("types only" in d.description for d in report.differences)


def test_different_notes():
    a = _make_bundle(notes=["note A"])
    b = _make_bundle(notes=["note B"])
    report = diff_bundles(a, b)
    assert any("notes differ" in d.description for d in report.differences)


def test_different_assertion_count():
    a = _make_bundle(assertions=[{"kind": "contains_text", "text": "a"}])
    b = _make_bundle(assertions=[
        {"kind": "contains_text", "text": "a"},
        {"kind": "contains_text", "text": "b"},
    ])
    report = diff_bundles(a, b)
    assert any("count" in d.description for d in report.differences)
