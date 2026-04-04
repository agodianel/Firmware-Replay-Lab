from __future__ import annotations

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


def _check_event_count(bundle: ReplayBundle, assertion: dict) -> str | None:
    event_type = assertion.get("event_type", "")
    min_count = int(assertion.get("min_count", 1))
    count = sum(1 for event in bundle.events if event.get("type") == event_type)
    if count < min_count:
        return (
            f"Expected event type {event_type!r} at least {min_count} times, found {count}"
        )
    return None


def evaluate_bundle(bundle: ReplayBundle) -> ReplayResult:
    failures: list[str] = []

    for idx, assertion in enumerate(bundle.assertions):
        kind = assertion.get("kind", "")
        if kind == "contains_text":
            failure = _check_contains_text(bundle, assertion)
        elif kind == "event_count":
            failure = _check_event_count(bundle, assertion)
        else:
            failure = f"Unknown assertion kind at index {idx}: {kind!r}"

        if failure:
            failures.append(failure)

    return ReplayResult(passed=not failures, failures=failures)
