from __future__ import annotations

import argparse
import json
import sys

from .bundle import ReplayBundle, SessionMetadata
from .capture import append_serial_log_from_file
from .replay import evaluate_bundle
from .validator import validate_bundle
from .diff import diff_bundles
from .anonymize import anonymize_bundle


def _cmd_capture(args: argparse.Namespace) -> int:
    """Capture logs, metadata, and optional event streams into a new bundle."""
    metadata = SessionMetadata(
        target=args.target,
        firmware_version=args.firmware_version,
        board=args.board,
        commit=args.commit,
    )
    bundle = ReplayBundle(metadata=metadata)
    if args.log_file:
        append_serial_log_from_file(bundle, args.log_file)
    bundle.save_json(args.output)
    print(f"Captured bundle at {args.output}")
    return 0


def _cmd_pack(args: argparse.Namespace) -> int:
    """Build or update a replay bundle from raw artifacts."""
    bundle = ReplayBundle.load_json(args.bundle)
    if args.log_file:
        append_serial_log_from_file(bundle, args.log_file)
    if args.assertion_text:
        bundle.assertions.append({"kind": "contains_text", "text": args.assertion_text})
    if args.note:
        bundle.notes.append(args.note)
    bundle.save_json(args.bundle)
    print(f"Packed updates into {args.bundle}")
    return 0


def _cmd_inspect(args: argparse.Namespace) -> int:
    """Summarize a replay bundle for humans and agents."""
    bundle = ReplayBundle.load_json(args.bundle)
    meta = bundle.metadata
    print(f"Bundle: {args.bundle}")
    print(f"  Target:   {meta.target}")
    print(f"  Board:    {meta.board}")
    print(f"  FW:       {meta.firmware_version}")
    print(f"  Commit:   {meta.commit}")
    print(f"  Captured: {meta.captured_at}")
    print(f"  Log lines:    {len(bundle.serial_log)}")
    print(f"  Events:       {len(bundle.events)}")
    print(f"  Assertions:   {len(bundle.assertions)}")
    print(f"  Notes:        {len(bundle.notes)}")
    if bundle.notes:
        print("  Notes:")
        for note in bundle.notes:
            print(f"    - {note}")
    return 0


def _cmd_test(args: argparse.Namespace) -> int:
    """Execute replay bundle assertions as deterministic checks."""
    bundle = ReplayBundle.load_json(args.bundle)
    result = evaluate_bundle(bundle)

    if result.passed:
        print(f"PASS: {args.bundle} — all {len(bundle.assertions)} assertions satisfied")
        return 0

    print(f"FAIL: {args.bundle}", file=sys.stderr)
    for failure in result.failures:
        print(f"  - {failure}", file=sys.stderr)
    return 1


def _cmd_export(args: argparse.Namespace) -> int:
    """Export a bundle to markdown summary or JSON report."""
    bundle = ReplayBundle.load_json(args.bundle)
    fmt = args.format

    if fmt == "json":
        print(json.dumps(bundle.to_dict(), indent=2))
    elif fmt == "markdown":
        meta = bundle.metadata
        lines = [
            f"# Replay Report: {meta.target} / {meta.board}",
            "",
            f"- **Firmware**: {meta.firmware_version}",
            f"- **Commit**: {meta.commit}",
            f"- **Captured**: {meta.captured_at}",
            "",
            f"## Serial Log ({len(bundle.serial_log)} lines)",
            "",
        ]
        for entry in bundle.serial_log:
            lines.append(f"  [{entry.timestamp_ms}ms] {entry.message}")
        lines.append("")
        lines.append(f"## Assertions ({len(bundle.assertions)})")
        lines.append("")
        for assertion in bundle.assertions:
            lines.append(f"  - {assertion.get('kind')}: {assertion}")
        if bundle.notes:
            lines.append("")
            lines.append("## Notes")
            lines.append("")
            for note in bundle.notes:
                lines.append(f"  - {note}")
        print("\n".join(lines))
    else:
        print(f"Unknown format: {fmt}", file=sys.stderr)
        return 2
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    """Validate a replay bundle against the schema."""
    bundle = ReplayBundle.load_json(args.bundle)
    errors = validate_bundle(bundle)

    warnings = [e for e in errors if e.startswith("warning:")]
    hard_errors = [e for e in errors if not e.startswith("warning:")]

    if hard_errors:
        print(f"INVALID: {args.bundle}", file=sys.stderr)
        for err in hard_errors:
            print(f"  error: {err}", file=sys.stderr)
        for warn in warnings:
            print(f"  {warn}", file=sys.stderr)
        return 1

    if warnings and not args.quiet:
        print(f"VALID (with warnings): {args.bundle}")
        for warn in warnings:
            print(f"  {warn}")
    else:
        print(f"VALID: {args.bundle}")
    return 0


def _cmd_diff(args: argparse.Namespace) -> int:
    """Compare two replay bundles and show differences."""
    a = ReplayBundle.load_json(args.bundle_a)
    b = ReplayBundle.load_json(args.bundle_b)
    report = diff_bundles(a, b)

    if not report.differences:
        print("Bundles are identical.")
        return 0

    print(f"Found {len(report.differences)} difference(s):")
    for diff in report.differences:
        print(f"  [{diff.section}] {diff.description}")
    return 0


def _cmd_ui(args: argparse.Namespace) -> int:
    """Launch Dash UI for bundle inspection."""
    try:
        from .ui_launcher import launch_ui
    except ImportError:
        print(
            "Dash is required for the UI. Install it with:\n"
            "  uv pip install dash",
            file=sys.stderr,
        )
        return 1
    launch_ui(bundle_dir=args.bundle_dir, port=args.port, debug=args.debug)
    return 0


def _cmd_anonymize(args: argparse.Namespace) -> int:
    """Strip sensitive data from a bundle for safe sharing."""
    bundle = ReplayBundle.load_json(args.bundle)
    cleaned = anonymize_bundle(bundle)
    output = args.output or args.bundle
    cleaned.save_json(output)
    print(f"Anonymized bundle saved to {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="frl",
        description="Firmware Replay Lab — capture once, replay everywhere",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # frl capture
    capture = subparsers.add_parser(
        "capture", help="Capture logs and metadata into a new replay bundle"
    )
    capture.add_argument("--output", "-o", required=True, help="Output bundle path")
    capture.add_argument("--target", "-t", required=True, help="Target platform")
    capture.add_argument("--firmware-version", "-fw", required=True)
    capture.add_argument("--board", "-b", required=True)
    capture.add_argument("--commit", "-c", required=True)
    capture.add_argument("--log-file", "-l", help="Serial log file to include")
    capture.set_defaults(func=_cmd_capture)

    # frl pack
    pack = subparsers.add_parser(
        "pack", help="Add logs, assertions, or notes to an existing bundle"
    )
    pack.add_argument("--bundle", required=True, help="Path to existing bundle")
    pack.add_argument("--log-file", "-l", help="Serial log file to append")
    pack.add_argument("--assertion-text", help="Add a contains_text assertion")
    pack.add_argument("--note", help="Add a note")
    pack.set_defaults(func=_cmd_pack)

    # frl inspect
    inspect_cmd = subparsers.add_parser(
        "inspect", help="Summarize a replay bundle for humans and agents"
    )
    inspect_cmd.add_argument("--bundle", required=True)
    inspect_cmd.set_defaults(func=_cmd_inspect)

    # frl test
    test = subparsers.add_parser(
        "test", help="Execute replay bundle assertions"
    )
    test.add_argument("--bundle", required=True)
    test.set_defaults(func=_cmd_test)

    # frl export
    export = subparsers.add_parser(
        "export", help="Export bundle to markdown or JSON report"
    )
    export.add_argument("--bundle", required=True)
    export.add_argument(
        "--format", "-f", choices=["json", "markdown"], default="json",
        help="Output format"
    )
    export.set_defaults(func=_cmd_export)

    # frl validate
    validate = subparsers.add_parser(
        "validate", help="Validate a replay bundle against the schema"
    )
    validate.add_argument("--bundle", required=True)
    validate.add_argument("--quiet", "-q", action="store_true", help="Suppress warnings")
    validate.set_defaults(func=_cmd_validate)

    # frl diff
    diff = subparsers.add_parser(
        "diff", help="Compare two replay bundles"
    )
    diff.add_argument("--bundle-a", required=True, help="First bundle")
    diff.add_argument("--bundle-b", required=True, help="Second bundle")
    diff.set_defaults(func=_cmd_diff)

    # frl ui
    ui = subparsers.add_parser(
        "ui", help="Launch browser-based Dash UI for replay inspection"
    )
    ui.add_argument(
        "--bundle-dir", default="replays/sample-bundles",
        help="Directory containing replay bundles",
    )
    ui.add_argument("--port", type=int, default=8050)
    ui.add_argument("--debug", action="store_true")
    ui.set_defaults(func=_cmd_ui)

    # frl anonymize
    anonymize = subparsers.add_parser(
        "anonymize", help="Strip sensitive data from a bundle for safe sharing"
    )
    anonymize.add_argument("--bundle", required=True, help="Bundle to anonymize")
    anonymize.add_argument(
        "--output", "-o",
        help="Output path (default: overwrite input)",
    )
    anonymize.set_defaults(func=_cmd_anonymize)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
