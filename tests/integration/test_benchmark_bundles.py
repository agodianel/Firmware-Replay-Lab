"""Integration tests for benchmark bundles — ensure all sample bundles are valid and pass."""

from pathlib import Path

import pytest

from firmware_replay_lab.bundle import ReplayBundle
from firmware_replay_lab.replay import evaluate_bundle
from firmware_replay_lab.validator import validate_bundle

BUNDLE_DIR = Path(__file__).resolve().parents[2] / "replays" / "sample-bundles"


def _bundle_paths():
    if not BUNDLE_DIR.exists():
        return []
    return sorted(BUNDLE_DIR.glob("*.json"))


@pytest.mark.parametrize("bundle_path", _bundle_paths(), ids=lambda p: p.name)
def test_bundle_is_loadable(bundle_path):
    bundle = ReplayBundle.load_json(bundle_path)
    assert bundle.metadata.target


@pytest.mark.parametrize("bundle_path", _bundle_paths(), ids=lambda p: p.name)
def test_bundle_is_valid(bundle_path):
    bundle = ReplayBundle.load_json(bundle_path)
    errors = validate_bundle(bundle)
    hard_errors = [e for e in errors if not e.startswith("warning:")]
    assert not hard_errors, f"Validation errors: {hard_errors}"


@pytest.mark.parametrize("bundle_path", _bundle_paths(), ids=lambda p: p.name)
def test_bundle_assertions_pass(bundle_path):
    bundle = ReplayBundle.load_json(bundle_path)
    result = evaluate_bundle(bundle)
    assert result.passed, f"Assertion failures: {result.failures}"
