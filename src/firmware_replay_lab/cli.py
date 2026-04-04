from __future__ import annotations

import argparse
import json
import sys

from .bundle import ReplayBundle, SessionMetadata
from .capture import append_serial_log_from_file
from .replay import evaluate_bundle


def _cmd_init_bundle(args: argparse.Namespace) -> int:
    metadata = SessionMetadata(
        target=args.target,
        firmware_version=args.firmware_version,
        board=args.board,
        commit=args.commit,
    )
    bundle = ReplayBundle(metadata=metadata)
    bundle.save_json(args.output)
    print(f"Bundle created at {args.output}")
    return 0


def _cmd_add_log(args: argparse.Namespace) -> int:
    bundle = ReplayBundle.load_json(args.bundle)
    append_serial_log_from_file(bundle, args.log_file)
    bundle.save_json(args.bundle)
    print(f"Appended serial log from {args.log_file} to {args.bundle}")
    return 0


def _cmd_add_assertion(args: argparse.Namespace) -> int:
    bundle = ReplayBundle.load_json(args.bundle)
    assertion = {"kind": args.kind}
    if args.kind == "contains_text":
        if not args.text:
            print("--text is required for contains_text assertions", file=sys.stderr)
            return 2
        assertion["text"] = args.text
    elif args.kind == "event_count":
        if not args.event_type:
            print("--event-type is required for event_count assertions", file=sys.stderr)
            return 2
        assertion["event_type"] = args.event_type
        assertion["min_count"] = args.min_count

    bundle.assertions.append(assertion)
    bundle.save_json(args.bundle)
    print(f"Added assertion to {args.bundle}: {json.dumps(assertion)}")
    return 0


def _cmd_replay(args: argparse.Namespace) -> int:
    bundle = ReplayBundle.load_json(args.bundle)
    result = evaluate_bundle(bundle)

    if result.passed:
        print("Replay passed: all assertions satisfied")
        return 0

    print("Replay failed:", file=sys.stderr)
    for failure in result.failures:
        print(f"- {failure}", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="firmware-replay")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_bundle = subparsers.add_parser("init-bundle", help="Create a new replay bundle")
    init_bundle.add_argument("--output", required=True)
    init_bundle.add_argument("--target", required=True)
    init_bundle.add_argument("--firmware-version", required=True)
    init_bundle.add_argument("--board", required=True)
    init_bundle.add_argument("--commit", required=True)
    init_bundle.set_defaults(func=_cmd_init_bundle)

    add_log = subparsers.add_parser("add-log", help="Append serial log lines to bundle")
    add_log.add_argument("--bundle", required=True)
    add_log.add_argument("--log-file", required=True)
    add_log.set_defaults(func=_cmd_add_log)

    add_assertion = subparsers.add_parser("add-assertion", help="Add replay assertion")
    add_assertion.add_argument("--bundle", required=True)
    add_assertion.add_argument(
        "--kind", required=True, choices=["contains_text", "event_count"]
    )
    add_assertion.add_argument("--text")
    add_assertion.add_argument("--event-type")
    add_assertion.add_argument("--min-count", type=int, default=1)
    add_assertion.set_defaults(func=_cmd_add_assertion)

    replay = subparsers.add_parser("replay", help="Evaluate bundle assertions")
    replay.add_argument("--bundle", required=True)
    replay.set_defaults(func=_cmd_replay)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
