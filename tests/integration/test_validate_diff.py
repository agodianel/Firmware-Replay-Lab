"""Integration tests for frl validate and frl diff commands."""

from firmware_replay_lab.cli import main


def test_validate_valid_bundle(tmp_path):
    bundle_path = str(tmp_path / "bundle.json")
    main(["capture", "-o", bundle_path, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "abc"])
    main(["pack", "--bundle", bundle_path, "--assertion-text", "x", "--note", "test"])

    rc = main(["validate", "--bundle", bundle_path])
    assert rc == 0


def test_validate_quiet_suppresses_warnings(tmp_path, capsys):
    bundle_path = str(tmp_path / "bundle.json")
    main(["capture", "-o", bundle_path, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "abc"])

    rc = main(["validate", "--bundle", bundle_path, "-q"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "warning" not in out.lower()


def test_diff_identical_bundles(tmp_path, capsys):
    a = str(tmp_path / "a.json")
    b = str(tmp_path / "b.json")
    main(["capture", "-o", a, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "abc"])
    main(["capture", "-o", b, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "abc"])

    rc = main(["diff", "--bundle-a", a, "--bundle-b", b])
    assert rc == 0
    out = capsys.readouterr().out
    assert "identical" in out.lower()


def test_diff_different_targets(tmp_path, capsys):
    a = str(tmp_path / "a.json")
    b = str(tmp_path / "b.json")
    main(["capture", "-o", a, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "abc"])
    main(["capture", "-o", b, "-t", "stm32", "-fw", "v1", "-b", "nucleo", "-c", "abc"])

    rc = main(["diff", "--bundle-a", a, "--bundle-b", b])
    assert rc == 0
    out = capsys.readouterr().out
    assert "difference" in out.lower()
