from firmware_replay_lab.bundle import ReplayBundle, SessionMetadata, SerialLine
from firmware_replay_lab.replay import evaluate_bundle


def _bundle_with_log(text: str) -> ReplayBundle:
    return ReplayBundle(
        metadata=SessionMetadata(
            target="stm32",
            firmware_version="1.0",
            board="nucleo",
            commit="abc",
        ),
        serial_log=[SerialLine(timestamp_ms=0, direction="device->host", message=text)],
    )


def test_replay_passes_contains_text():
    bundle = _bundle_with_log("sensor init ok")
    bundle.assertions.append({"kind": "contains_text", "text": "init"})

    result = evaluate_bundle(bundle)
    assert result.passed is True
    assert result.failures == []


def test_replay_fails_contains_text():
    bundle = _bundle_with_log("sensor init ok")
    bundle.assertions.append({"kind": "contains_text", "text": "panic"})

    result = evaluate_bundle(bundle)
    assert result.passed is False
    assert len(result.failures) == 1
