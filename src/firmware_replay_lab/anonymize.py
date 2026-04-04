"""Bundle anonymizer — strip sensitive data from bundles before sharing.

Removes or redacts:
- IP addresses
- MAC addresses
- API keys and tokens
- URLs with credentials
- Email addresses
- File paths that may leak internal structure
"""

from __future__ import annotations

import re

from .bundle import ReplayBundle

_IP_RE = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
_MAC_RE = re.compile(r"\b([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b")
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_TOKEN_RE = re.compile(
    r"(?:api[_-]?key|token|secret|password|bearer|authorization)\s*[:=]\s*\S+",
    re.IGNORECASE,
)
_URL_CRED_RE = re.compile(r"https?://\S+:\S+@")
_ABS_PATH_RE = re.compile(r"(?:/home/\w+|/Users/\w+|C:\\Users\\\w+)[^\s]*")


def anonymize_text(text: str) -> str:
    """Redact sensitive patterns from a single text string."""
    text = _IP_RE.sub("<REDACTED_IP>", text)
    text = _MAC_RE.sub("<REDACTED_MAC>", text)
    text = _EMAIL_RE.sub("<REDACTED_EMAIL>", text)
    text = _TOKEN_RE.sub("<REDACTED_CREDENTIAL>", text)
    text = _URL_CRED_RE.sub("https://<REDACTED>@", text)
    text = _ABS_PATH_RE.sub("<REDACTED_PATH>", text)
    return text


def anonymize_bundle(bundle: ReplayBundle) -> ReplayBundle:
    """Return a new bundle with sensitive data redacted.

    Does not modify the original bundle.
    """
    from dataclasses import replace
    from .bundle import SerialLine

    new_log = [
        SerialLine(
            timestamp_ms=line.timestamp_ms,
            direction=line.direction,
            message=anonymize_text(line.message),
        )
        for line in bundle.serial_log
    ]

    new_events = []
    for event in bundle.events:
        new_event = dict(event)
        if "detail" in new_event:
            new_event["detail"] = anonymize_text(str(new_event["detail"]))
        new_events.append(new_event)

    new_notes = [anonymize_text(note) for note in bundle.notes]

    new_meta = replace(
        bundle.metadata,
        environment={
            k: anonymize_text(v) for k, v in bundle.metadata.environment.items()
        },
    )

    return replace(
        bundle,
        metadata=new_meta,
        serial_log=new_log,
        events=new_events,
        notes=new_notes,
    )
