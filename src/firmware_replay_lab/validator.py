from __future__ import annotations

from .bundle import ReplayBundle

VALID_DIRECTIONS = {"device->host", "host->device"}
KNOWN_ASSERTION_KINDS = {"contains_text", "event_count", "regex_match", "timing_window", "ordering", "log_line_count"}


def validate_bundle(bundle: ReplayBundle) -> list[str]:
    """Validate a replay bundle against schema rules. Returns list of error strings (empty = valid)."""
    errors: list[str] = []

    # Metadata checks
    meta = bundle.metadata
    if not meta.target:
        errors.append("metadata.target is empty")
    if not meta.firmware_version:
        errors.append("metadata.firmware_version is empty")
    if not meta.board:
        errors.append("metadata.board is empty")
    if not meta.commit:
        errors.append("metadata.commit is empty")

    # Serial log checks
    for i, line in enumerate(bundle.serial_log):
        if line.timestamp_ms < 0:
            errors.append(f"serial_log[{i}].timestamp_ms is negative: {line.timestamp_ms}")
        if line.direction not in VALID_DIRECTIONS:
            errors.append(f"serial_log[{i}].direction is invalid: {line.direction!r}")
        if not line.message:
            errors.append(f"serial_log[{i}].message is empty")

    # Assertion checks
    for i, assertion in enumerate(bundle.assertions):
        kind = assertion.get("kind", "")
        if not kind:
            errors.append(f"assertions[{i}] is missing 'kind'")
        elif kind not in KNOWN_ASSERTION_KINDS:
            errors.append(f"assertions[{i}] has unknown kind: {kind!r}")
        else:
            if kind == "contains_text" and not assertion.get("text"):
                errors.append(f"assertions[{i}] (contains_text) is missing 'text'")
            if kind == "regex_match" and not assertion.get("pattern"):
                errors.append(f"assertions[{i}] (regex_match) is missing 'pattern'")
            if kind == "event_count" and not assertion.get("event_type"):
                errors.append(f"assertions[{i}] (event_count) is missing 'event_type'")
            if kind == "timing_window":
                if not assertion.get("event_type"):
                    errors.append(f"assertions[{i}] (timing_window) is missing 'event_type'")
                if "after_ms" not in assertion:
                    errors.append(f"assertions[{i}] (timing_window) is missing 'after_ms'")
                if "before_ms" not in assertion:
                    errors.append(f"assertions[{i}] (timing_window) is missing 'before_ms'")
            if kind == "ordering" and not assertion.get("sequence"):
                errors.append(f"assertions[{i}] (ordering) is missing 'sequence'")

    # Warnings as soft errors (prefixed)
    if not bundle.serial_log:
        errors.append("warning: serial_log is empty")
    if not bundle.assertions:
        errors.append("warning: no assertions defined")
    if not bundle.notes:
        errors.append("warning: no notes provided")

    return errors
