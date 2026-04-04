from firmware_replay_lab.cli import main


def test_capture_and_test_flow(tmp_path):
    """End-to-end: capture a bundle, then test its assertions."""
    log_file = tmp_path / "serial.log"
    log_file.write_text("BOOT OK\nPANIC: watchdog timeout\nRebooting...\n")

    bundle_path = str(tmp_path / "bundle.json")

    # Capture
    rc = main([
        "capture",
        "-o", bundle_path,
        "-t", "esp32",
        "-fw", "v1.0",
        "-b", "devkitc",
        "-c", "abc",
        "-l", str(log_file),
    ])
    assert rc == 0

    # Pack an assertion
    rc = main(["pack", "--bundle", bundle_path, "--assertion-text", "PANIC"])
    assert rc == 0

    # Test
    rc = main(["test", "--bundle", bundle_path])
    assert rc == 0


def test_inspect(tmp_path, capsys):
    log_file = tmp_path / "serial.log"
    log_file.write_text("hello device\n")

    bundle_path = str(tmp_path / "bundle.json")
    main(["capture", "-o", bundle_path, "-t", "stm32", "-fw", "2.0", "-b", "nucleo", "-c", "def", "-l", str(log_file)])

    rc = main(["inspect", "--bundle", bundle_path])
    assert rc == 0
    out = capsys.readouterr().out
    assert "stm32" in out
    assert "nucleo" in out


def test_export_json(tmp_path, capsys):
    bundle_path = str(tmp_path / "bundle.json")
    main(["capture", "-o", bundle_path, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "xyz"])

    rc = main(["export", "--bundle", bundle_path, "--format", "json"])
    assert rc == 0
    out = capsys.readouterr().out
    assert '"target": "esp32"' in out


def test_export_markdown(tmp_path, capsys):
    bundle_path = str(tmp_path / "bundle.json")
    main(["capture", "-o", bundle_path, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "xyz"])

    rc = main(["export", "--bundle", bundle_path, "--format", "markdown"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Replay Report" in out


def test_test_fails_on_missing_text(tmp_path):
    bundle_path = str(tmp_path / "bundle.json")
    main(["capture", "-o", bundle_path, "-t", "esp32", "-fw", "v1", "-b", "devkitc", "-c", "xyz"])
    main(["pack", "--bundle", bundle_path, "--assertion-text", "NEVER_PRESENT"])

    rc = main(["test", "--bundle", bundle_path])
    assert rc == 1
