"""Tests for extended assertion engine (regex_match, timing_window, ordering, log_line_count)."""

from firmware_replay_lab.bundle import ReplayBundle, SessionMetadata, SerialLine
from firmware_replay_lab.replay import evaluate_bundle


def _make_bundle(messages, events=None, assertions=None):
    return ReplayBundle(
        metadata=SessionMetadata(
            target="test", firmware_version="1.0", board="test", commit="abc"
        ),
        serial_log=[
            SerialLine(timestamp_ms=i, direction="device->host", message=msg)
            for i, msg in enumerate(messages)
        ],
        events=events or [],
        assertions=assertions or [],
    )


class TestRegexMatch:
    def test_pass_simple_pattern(self):
        bundle = _make_bundle(
            ["ERROR: code 42", "OK"],
            assertions=[{"kind": "regex_match", "pattern": r"code \d+"}],
        )
        assert evaluate_bundle(bundle).passed

    def test_fail_no_match(self):
        bundle = _make_bundle(
            ["all fine"],
            assertions=[{"kind": "regex_match", "pattern": r"ERROR.*\d+"}],
        )
        result = evaluate_bundle(bundle)
        assert not result.passed
        assert "regex" in result.failures[0].lower()

    def test_invalid_pattern_reports_error(self):
        bundle = _make_bundle(
            ["test"],
            assertions=[{"kind": "regex_match", "pattern": r"[invalid"}],
        )
        result = evaluate_bundle(bundle)
        assert not result.passed
        assert "invalid" in result.failures[0].lower()


class TestTimingWindow:
    def test_pass_event_in_window(self):
        bundle = _make_bundle(
            ["boot"],
            events=[{"type": "panic", "timestamp_ms": 500}],
            assertions=[{
                "kind": "timing_window",
                "event_type": "panic",
                "after_ms": 100,
                "before_ms": 1000,
            }],
        )
        assert evaluate_bundle(bundle).passed

    def test_fail_event_outside_window(self):
        bundle = _make_bundle(
            ["boot"],
            events=[{"type": "panic", "timestamp_ms": 2000}],
            assertions=[{
                "kind": "timing_window",
                "event_type": "panic",
                "after_ms": 100,
                "before_ms": 1000,
            }],
        )
        assert not evaluate_bundle(bundle).passed

    def test_fail_no_matching_event(self):
        bundle = _make_bundle(
            ["boot"],
            events=[{"type": "reset", "timestamp_ms": 500}],
            assertions=[{
                "kind": "timing_window",
                "event_type": "panic",
                "after_ms": 0,
                "before_ms": 10000,
            }],
        )
        assert not evaluate_bundle(bundle).passed


class TestOrdering:
    def test_pass_correct_order(self):
        bundle = _make_bundle(
            ["BOOT", "INIT", "READY", "DONE"],
            assertions=[{
                "kind": "ordering",
                "sequence": ["BOOT", "INIT", "READY"],
            }],
        )
        assert evaluate_bundle(bundle).passed

    def test_fail_wrong_order(self):
        bundle = _make_bundle(
            ["READY", "INIT", "BOOT"],
            assertions=[{
                "kind": "ordering",
                "sequence": ["BOOT", "INIT", "READY"],
            }],
        )
        result = evaluate_bundle(bundle)
        assert not result.passed

    def test_fail_missing_item(self):
        bundle = _make_bundle(
            ["BOOT", "DONE"],
            assertions=[{
                "kind": "ordering",
                "sequence": ["BOOT", "INIT", "READY"],
            }],
        )
        result = evaluate_bundle(bundle)
        assert not result.passed
        assert "INIT" in result.failures[0]


class TestLogLineCount:
    def test_pass_min_lines(self):
        bundle = _make_bundle(
            ["a", "b", "c"],
            assertions=[{"kind": "log_line_count", "min_lines": 2}],
        )
        assert evaluate_bundle(bundle).passed

    def test_fail_below_min(self):
        bundle = _make_bundle(
            ["a"],
            assertions=[{"kind": "log_line_count", "min_lines": 5}],
        )
        assert not evaluate_bundle(bundle).passed

    def test_pass_max_lines(self):
        bundle = _make_bundle(
            ["a", "b"],
            assertions=[{"kind": "log_line_count", "max_lines": 10}],
        )
        assert evaluate_bundle(bundle).passed

    def test_fail_above_max(self):
        bundle = _make_bundle(
            ["a", "b", "c", "d", "e"],
            assertions=[{"kind": "log_line_count", "max_lines": 3}],
        )
        assert not evaluate_bundle(bundle).passed
