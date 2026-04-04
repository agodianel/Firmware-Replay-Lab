"""Timestamp normalizer — convert various log timestamp formats to monotonic ms."""

from __future__ import annotations

import re

# Matches common embedded timestamp formats
_MS_TIMESTAMP_RE = re.compile(r"^\[?\s*(\d+)\s*(?:ms)?\s*\]?")
_SEC_TIMESTAMP_RE = re.compile(r"^\[?\s*(\d+)\.(\d{1,3})\s*s?\s*\]?")
_IDF_TIMESTAMP_RE = re.compile(r"\((\d+)\)")


def extract_timestamp_ms(text: str) -> int | None:
    """Try to extract a millisecond timestamp from the beginning of a log line.

    Returns the timestamp in milliseconds, or None if no recognizable format found.
    """
    # ESP-IDF style: I (12345) tag: msg
    m = _IDF_TIMESTAMP_RE.search(text[:30])
    if m:
        return int(m.group(1))

    # Seconds with decimal: [1.234s] or 1.234
    m = _SEC_TIMESTAMP_RE.match(text)
    if m:
        secs = int(m.group(1))
        frac = m.group(2).ljust(3, "0")[:3]
        return secs * 1000 + int(frac)

    # Plain milliseconds: [12345ms] or 12345
    m = _MS_TIMESTAMP_RE.match(text)
    if m:
        return int(m.group(1))

    return None


def normalize_timestamps(lines: list[str]) -> list[tuple[int, str]]:
    """Parse timestamp from each line, assign monotonic ms to lines without timestamps.

    Returns list of (timestamp_ms, cleaned_message) tuples.
    """
    result: list[tuple[int, str]] = []
    last_ts = 0

    for line in lines:
        ts = extract_timestamp_ms(line)
        if ts is not None:
            last_ts = ts
        else:
            last_ts += 1
        result.append((last_ts, line))

    return result
