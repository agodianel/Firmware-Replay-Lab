from __future__ import annotations

import re
from dataclasses import dataclass, field

from .bundle import ReplayBundle


@dataclass
class ReplayResult:
    passed: bool
    failures: list[str] = field(default_factory=list)


def _check_contains_text(bundle: ReplayBundle, assertion: dict) -> str | None:
    expected = assertion.get("text", "")
    if not expected:
        return "contains_text assertion is missing 'text'"
    for line in bundle.serial_log:
        if expected in line.message:
            return None
    return f"Expected serial log to contain text: {expected!r}"


def _check_regex_match(bundle: ReplayBundle, assertion: dict) -> str | None:
    pattern = assertion.get("pattern", "")
    if not pattern:
        return "regex_match assertion is missing 'pattern'"
    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        return f"regex_match has invalid pattern {pattern!r}: {exc}"
    for line in bundle.serial_log:
        if compiled.search(line.message):
            return None
    return f"No serial log line matches regex: {pattern!r}"


def _check_event_count(bundle: ReplayBundle, assertion: dict) -> str | None:
    event_type = assertion.get("event_type", "")
    min_count = int(assertion.get("min_count", 1))
    count = sum(1 for event in bundle.events if event.get("type") == event_type)
    if count < min_count:
        return (
            f"Expected event type {event_type!r} at least {min_count} times, found {count}"
        )
    return None


def _check_timing_window(bundle: ReplayBundle, assertion: dict) -> str | None:
    event_type = assertion.get("event_type", "")
    after_ms = int(assertion.get("after_ms", 0))
    before_ms = int(assertion.get("before_ms", 0))
    if not event_type:
        return "timing_window assertion is missing 'event_type'"

    for event in bundle.events:
        if event.get("type") == event_type:
            ts = int(event.get("timestamp_ms", -1))
            if after_ms <= ts <= before_ms:
                return None

    return (
        f"No event {event_type!r} found in window [{after_ms}ms, {before_ms}ms]"
    )


def _check_ordering(bundle: ReplayBundle, assertion: dict) -> str | None:
    sequence = assertion.get("sequence", [])
    if not sequence:
        return "ordering assertion is missing 'sequence'"

    seq_idx = 0
    for line in bundle.serial_log:
        if seq_idx < len(sequence) and sequence[seq_idx] in line.message:
            seq_idx += 1
    if seq_idx < len(sequence):
        return (
            f"Ordering not satisfied: matched {seq_idx}/{len(sequence)} items. "
            f"Missing from: {sequence[seq_idx]!r}"
        )
    return None


def _check_log_line_count(bundle: ReplayBundle, assertion: dict) -> str | None:
    min_lines = int(assertion.get("min_lines", 0))
    max_lines = assertion.get("max_lines")
    count = len(bundle.serial_log)
    if count < min_lines:
        return f"Expected at least {min_lines} log lines, found {count}"
    if max_lines is not None and count > int(max_lines):
        return f"Expected at most {max_lines} log lines, found {count}"
    return None


_ASSERTION_HANDLERS = {
    "contains_text": _check_contains_text,
    "regex_match": _check_regex_match,
    "event_count": _check_event_count,
    "timing_window": _check_timing_window,
    "ordering": _check_ordering,
    "log_line_count": _check_log_line_count,
}


def evaluate_bundle(bundle: ReplayBundle) -> ReplayResult:
    failures: list[str] = []

    for idx, assertion in enumerate(bundle.assertions):
        kind = assertion.get("kind", "")
        handler = _ASSERTION_HANDLERS.get(kind)
        if handler is None:
            failures.append(f"Unknown assertion kind at index {idx}: {kind!r}")
            continue
        failure = handler(bundle, assertion)
        if failure:
            failures.append(failure)

    return ReplayResult(passed=not failures, failures=failures)
