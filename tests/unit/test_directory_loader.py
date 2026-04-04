"""Tests for bundle directory format loader."""

import json

from firmware_replay_lab.directory_loader import load_bundle_directory


def test_load_from_metadata_json(tmp_path):
    (tmp_path / "metadata.json").write_text(json.dumps({
        "target": "esp32",
        "firmware_version": "v1.0",
        "board": "devkitc",
        "commit": "abc123",
    }))
    (tmp_path / "serial.log").write_text("I (100) boot: starting\nI (200) wifi: ready\n")
    (tmp_path / "events.jsonl").write_text(
        '{"type": "reset", "timestamp_ms": 0}\n'
        '{"type": "panic", "timestamp_ms": 500}\n'
    )
    (tmp_path / "assertions.jsonl").write_text(
        '{"kind": "contains_text", "text": "boot"}\n'
    )
    (tmp_path / "notes.md").write_text("# Notes\n- first note\n- second note\n")

    bundle = load_bundle_directory(tmp_path)

    assert bundle.metadata.target == "esp32"
    assert bundle.metadata.board == "devkitc"
    assert len(bundle.serial_log) == 2
    assert len(bundle.events) == 2
    assert len(bundle.assertions) == 1
    assert len(bundle.notes) == 2


def test_load_minimal_directory(tmp_path):
    (tmp_path / "metadata.json").write_text(json.dumps({
        "target": "stm32",
        "firmware_version": "v2.0",
        "board": "nucleo",
        "commit": "def456",
    }))

    bundle = load_bundle_directory(tmp_path)
    assert bundle.metadata.target == "stm32"
    assert len(bundle.serial_log) == 0
    assert len(bundle.events) == 0


def test_load_missing_metadata_raises(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        load_bundle_directory(tmp_path)


def test_serial_log_assigns_timestamps(tmp_path):
    (tmp_path / "metadata.json").write_text(json.dumps({
        "target": "esp32", "firmware_version": "v1", "board": "b", "commit": "c"
    }))
    (tmp_path / "serial.log").write_text("I (100) tag: first\nplain line\n")

    bundle = load_bundle_directory(tmp_path)
    assert bundle.serial_log[0].timestamp_ms == 100
    assert bundle.serial_log[1].timestamp_ms == 101
