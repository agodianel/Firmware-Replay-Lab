"""Tests for timestamp normalizer."""

from firmware_replay_lab.timestamps import extract_timestamp_ms, normalize_timestamps


class TestExtractTimestampMs:
    def test_idf_format(self):
        assert extract_timestamp_ms("I (12345) boot: starting") == 12345

    def test_seconds_format(self):
        assert extract_timestamp_ms("[1.234s] message") == 1234

    def test_seconds_format_short_frac(self):
        assert extract_timestamp_ms("[1.2s] message") == 1200

    def test_ms_format(self):
        assert extract_timestamp_ms("[5000ms] message") == 5000

    def test_plain_number(self):
        assert extract_timestamp_ms("100 some text") == 100

    def test_no_timestamp(self):
        assert extract_timestamp_ms("just a plain line") is None


class TestNormalizeTimestamps:
    def test_preserves_known_timestamps(self):
        lines = [
            "I (100) tag: first",
            "I (200) tag: second",
        ]
        result = normalize_timestamps(lines)
        assert result[0][0] == 100
        assert result[1][0] == 200

    def test_assigns_monotonic_to_unknown(self):
        lines = [
            "I (100) tag: first",
            "plain line no timestamp",
            "another plain line",
        ]
        result = normalize_timestamps(lines)
        assert result[0][0] == 100
        assert result[1][0] == 101
        assert result[2][0] == 102

    def test_empty_input(self):
        assert normalize_timestamps([]) == []

    def test_all_unknown_starts_from_zero(self):
        lines = ["hello", "world"]
        result = normalize_timestamps(lines)
        assert result[0][0] == 1  # 0 + 1
        assert result[1][0] == 2
