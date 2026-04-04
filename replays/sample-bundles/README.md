# Benchmark Dataset

This directory contains anonymized firmware failure bundles for testing, benchmarking, and demonstration.

Each bundle represents a realistic failure scenario observed on real hardware platforms. All sensitive data has been redacted.

## Bundles

| File | Platform | Failure Type | Assertions |
|------|----------|-------------|------------|
| `wifi-timeout-esp32.json` | ESP32 | Wi-Fi connection timeout → abort | 3 |
| `hardfault-spi-stm32.json` | STM32 | HardFault during SPI transfer | 4 |
| `watchdog-ble-esp32.json` | ESP32 | BLE task watchdog timeout | 3 |
| `boot-loop-stm32.json` | STM32 | HAL init assert → infinite reset | 3 |
| `stack-overflow-esp32.json` | ESP32 | Stack overflow in ISR context | 4 |

## Usage

```bash
# Validate all bundles
for f in replays/sample-bundles/*.json; do uv run frl validate --bundle "$f"; done

# Run all assertions
for f in replays/sample-bundles/*.json; do uv run frl test --bundle "$f"; done

# Diff two bundles
uv run frl diff --bundle-a replays/sample-bundles/wifi-timeout-esp32.json \
                --bundle-b replays/sample-bundles/watchdog-ble-esp32.json
```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for instructions on submitting your own anonymized bundles.
