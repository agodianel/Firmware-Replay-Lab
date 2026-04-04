# ESP32 Example

## WiFi Timeout on Cold Boot

This example demonstrates capturing and replaying a WiFi connection timeout
failure on an ESP32 DevKitC.

### What happened

The device boots and attempts to connect to WiFi before the access point is
broadcasting. After a 10-second timeout, the firmware calls `abort()`,
causing a reboot loop.

### Capture

```bash
uv run frl capture \
  -o replays/wifi-timeout-esp32/bundle.json \
  -t esp32 -fw v2.1.0 -b devkitc-v4 -c a1b2c3d \
  -l examples/esp32/serial.log
```

### Test

```bash
uv run frl test --bundle replays/sample-bundles/wifi-timeout-esp32.json
```

### Sample serial output

See `serial.log` in this directory.
