from firmware_replay_lab.bundle import ReplayBundle, SessionMetadata, SerialLine


def test_bundle_roundtrip(tmp_path):
    bundle = ReplayBundle(
        metadata=SessionMetadata(
            target="esp32",
            firmware_version="v0.0.1",
            board="devkitc",
            commit="deadbeef",
        ),
        serial_log=[SerialLine(timestamp_ms=1, direction="device->host", message="boot")],
        assertions=[{"kind": "contains_text", "text": "boot"}],
        notes=["captured in lab"],
    )

    out = tmp_path / "bundle.json"
    bundle.save_json(out)
    loaded = ReplayBundle.load_json(out)

    assert loaded.metadata.target == "esp32"
    assert loaded.serial_log[0].message == "boot"
    assert loaded.assertions[0]["kind"] == "contains_text"
