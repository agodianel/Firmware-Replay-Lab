"""Tests for bundle validator."""

from firmware_replay_lab.bundle import ReplayBundle, SessionMetadata, SerialLine
from firmware_replay_lab.validator import validate_bundle


def _make_bundle(**kwargs):
    defaults = {
        "metadata": SessionMetadata(
            target="esp32", firmware_version="v1.0", board="devkitc", commit="abc123"
        ),
        "serial_log": [SerialLine(timestamp_ms=0, direction="device->host", message="boot")],
        "assertions": [{"kind": "contains_text", "text": "boot"}],
        "notes": ["test note"],
    }
    defaults.update(kwargs)
    return ReplayBundle(**defaults)


def test_valid_bundle_no_errors():
    bundle = _make_bundle()
    errors = validate_bundle(bundle)
    assert not [e for e in errors if not e.startswith("warning:")]


def test_empty_target_is_error():
    meta = SessionMetadata(target="", firmware_version="v1", board="b", commit="c")
    bundle = _make_bundle(metadata=meta)
    errors = validate_bundle(bundle)
    assert any("target" in e for e in errors)


def test_negative_timestamp_is_error():
    bundle = _make_bundle(
        serial_log=[SerialLine(timestamp_ms=-1, direction="device->host", message="bad")]
    )
    errors = validate_bundle(bundle)
    assert any("negative" in e for e in errors)


def test_invalid_direction_is_error():
    bundle = _make_bundle(
        serial_log=[SerialLine(timestamp_ms=0, direction="invalid", message="x")]
    )
    errors = validate_bundle(bundle)
    assert any("direction" in e for e in errors)


def test_unknown_assertion_kind_is_error():
    bundle = _make_bundle(assertions=[{"kind": "nonexistent_kind"}])
    errors = validate_bundle(bundle)
    assert any("unknown kind" in e for e in errors)


def test_missing_assertion_kind_is_error():
    bundle = _make_bundle(assertions=[{"text": "oops"}])
    errors = validate_bundle(bundle)
    assert any("missing 'kind'" in e for e in errors)


def test_contains_text_missing_text_is_error():
    bundle = _make_bundle(assertions=[{"kind": "contains_text"}])
    errors = validate_bundle(bundle)
    assert any("missing 'text'" in e for e in errors)


def test_empty_serial_log_warning():
    bundle = _make_bundle(serial_log=[])
    errors = validate_bundle(bundle)
    assert any("serial_log is empty" in e for e in errors)


def test_no_assertions_warning():
    bundle = _make_bundle(assertions=[])
    errors = validate_bundle(bundle)
    assert any("no assertions" in e for e in errors)
