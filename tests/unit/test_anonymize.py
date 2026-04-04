"""Tests for bundle anonymizer."""

from firmware_replay_lab.bundle import ReplayBundle, SessionMetadata, SerialLine
from firmware_replay_lab.anonymize import anonymize_text, anonymize_bundle


class TestAnonymizeText:
    def test_redacts_ip_address(self):
        assert "<REDACTED_IP>" in anonymize_text("Server at 192.168.1.100")

    def test_redacts_mac_address(self):
        assert "<REDACTED_MAC>" in anonymize_text("MAC: AA:BB:CC:DD:EE:FF")

    def test_redacts_email(self):
        assert "<REDACTED_EMAIL>" in anonymize_text("Contact: user@example.com")

    def test_redacts_api_key(self):
        assert "<REDACTED_CREDENTIAL>" in anonymize_text("api_key: sk-12345abc")

    def test_redacts_absolute_path(self):
        assert "<REDACTED_PATH>" in anonymize_text("File: /home/user/project/main.c")

    def test_preserves_hex_addresses(self):
        result = anonymize_text("PC: 0x08001234")
        assert "0x08001234" in result

    def test_preserves_normal_text(self):
        text = "HardFault Handler entered"
        assert anonymize_text(text) == text


class TestAnonymizeBundle:
    def test_returns_new_bundle(self):
        bundle = ReplayBundle(
            metadata=SessionMetadata(
                target="esp32", firmware_version="v1", board="b", commit="c",
            ),
            serial_log=[
                SerialLine(timestamp_ms=0, direction="device->host",
                           message="Connected to 192.168.1.1"),
            ],
            notes=["Debug by user@corp.com"],
        )
        cleaned = anonymize_bundle(bundle)

        # Original unchanged
        assert "192.168.1.1" in bundle.serial_log[0].message
        # Cleaned is redacted
        assert "192.168.1.1" not in cleaned.serial_log[0].message
        assert "<REDACTED_IP>" in cleaned.serial_log[0].message
        assert "<REDACTED_EMAIL>" in cleaned.notes[0]

    def test_preserves_metadata_fields(self):
        bundle = ReplayBundle(
            metadata=SessionMetadata(
                target="stm32", firmware_version="v2", board="nucleo", commit="abc",
            ),
        )
        cleaned = anonymize_bundle(bundle)
        assert cleaned.metadata.target == "stm32"
        assert cleaned.metadata.commit == "abc"

    def test_redacts_event_details(self):
        bundle = ReplayBundle(
            metadata=SessionMetadata(
                target="esp32", firmware_version="v1", board="b", commit="c",
            ),
            events=[{"type": "error", "detail": "Failed connecting to 10.0.0.1"}],
        )
        cleaned = anonymize_bundle(bundle)
        assert "10.0.0.1" not in cleaned.events[0]["detail"]
