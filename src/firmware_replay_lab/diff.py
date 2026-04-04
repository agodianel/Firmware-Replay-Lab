"""Bundle diff — compare two replay bundles and report differences."""

from __future__ import annotations

from dataclasses import dataclass, field

from .bundle import ReplayBundle


@dataclass
class Difference:
    section: str
    description: str


@dataclass
class DiffReport:
    differences: list[Difference] = field(default_factory=list)


def diff_bundles(a: ReplayBundle, b: ReplayBundle) -> DiffReport:
    """Compare two replay bundles and return a structured diff report."""
    diffs: list[Difference] = []

    # Metadata comparison
    ma, mb = a.metadata, b.metadata
    for attr in ("target", "firmware_version", "board", "commit"):
        va, vb = getattr(ma, attr), getattr(mb, attr)
        if va != vb:
            diffs.append(Difference("metadata", f"{attr}: {va!r} -> {vb!r}"))

    # Serial log comparison
    la, lb = len(a.serial_log), len(b.serial_log)
    if la != lb:
        diffs.append(Difference("serial_log", f"line count: {la} -> {lb}"))

    if la == lb:
        for i, (sa, sb) in enumerate(zip(a.serial_log, b.serial_log)):
            if sa.message != sb.message:
                diffs.append(Difference(
                    "serial_log", f"line {i} message differs"
                ))
                break  # report first difference only

    # Events comparison
    ea, eb = len(a.events), len(b.events)
    if ea != eb:
        diffs.append(Difference("events", f"count: {ea} -> {eb}"))

    types_a = sorted(set(e.get("type", "") for e in a.events))
    types_b = sorted(set(e.get("type", "") for e in b.events))
    if types_a != types_b:
        only_a = set(types_a) - set(types_b)
        only_b = set(types_b) - set(types_a)
        if only_a:
            diffs.append(Difference("events", f"types only in A: {only_a}"))
        if only_b:
            diffs.append(Difference("events", f"types only in B: {only_b}"))

    # Assertions comparison
    aa, ab = len(a.assertions), len(b.assertions)
    if aa != ab:
        diffs.append(Difference("assertions", f"count: {aa} -> {ab}"))

    kinds_a = sorted(ass.get("kind", "") for ass in a.assertions)
    kinds_b = sorted(ass.get("kind", "") for ass in b.assertions)
    if kinds_a != kinds_b:
        diffs.append(Difference("assertions", f"kinds differ: {kinds_a} vs {kinds_b}"))

    # Notes comparison
    if a.notes != b.notes:
        diffs.append(Difference("notes", f"notes differ ({len(a.notes)} vs {len(b.notes)})"))

    return DiffReport(differences=diffs)
