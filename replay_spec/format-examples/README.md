# Format Examples

This directory contains example replay bundles demonstrating the schema.

## Minimal bundle (JSON)

See `../../../replays/sample-bundles/wifi-timeout-esp32.json` for a complete example.

## Minimal valid bundle

```json
{
  "metadata": {
    "target": "esp32",
    "firmware_version": "v1.0.0",
    "board": "devkitc",
    "commit": "abc123"
  },
  "serial_log": [
    {"timestamp_ms": 0, "direction": "device->host", "message": "boot ok"}
  ],
  "events": [],
  "mocked_inputs": [],
  "assertions": [
    {"kind": "contains_text", "text": "boot ok"}
  ],
  "notes": ["Minimal example bundle"]
}
```

## Directory-based bundle (planned)

```text
my-replay/
  replay.yaml         # top-level config
  metadata.json       # device and session metadata
  serial.log          # raw serial log (one line per entry)
  events.jsonl        # one JSON event per line
  inputs/             # mocked inputs
    sensor_feed.json
  assertions.yaml     # expected outcomes
  notes.md            # human/agent context
```
