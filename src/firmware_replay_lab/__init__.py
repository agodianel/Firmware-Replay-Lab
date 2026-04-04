"""Firmware Replay Lab package."""

from .bundle import ReplayBundle, SessionMetadata, SerialLine
from .replay import ReplayResult, evaluate_bundle
from .validator import validate_bundle
from .diff import DiffReport, diff_bundles
from .directory_loader import load_bundle_directory
from .timestamps import extract_timestamp_ms, normalize_timestamps

__all__ = [
    "ReplayBundle",
    "ReplayResult",
    "SessionMetadata",
    "SerialLine",
    "DiffReport",
    "evaluate_bundle",
    "validate_bundle",
    "diff_bundles",
    "load_bundle_directory",
    "extract_timestamp_ms",
    "normalize_timestamps",
]
