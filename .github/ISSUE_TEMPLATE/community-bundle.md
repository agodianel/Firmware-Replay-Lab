---
name: Community Bundle Submission
about: Contribute an anonymized replay bundle from a real firmware failure
labels: community-bundle, replay-bundle
---

## Summary

<!-- One-line description of the failure this bundle captures -->

## Target Platform

- [ ] ESP32
- [ ] STM32
- [ ] nRF
- [ ] Other: <!-- specify -->

## Failure Category

- [ ] Panic / abort
- [ ] Watchdog timeout
- [ ] HardFault / BusFault / MemManage
- [ ] Communication timeout (Wi-Fi, BLE, SPI, I2C, UART)
- [ ] Boot failure / reset loop
- [ ] Memory corruption
- [ ] Peripheral initialization failure
- [ ] Timing / race condition
- [ ] Stack overflow
- [ ] Other: <!-- specify -->

## Bundle Checklist

- [ ] Bundle is valid JSON (`frl validate --bundle <path>`)
- [ ] At least one assertion passes (`frl test --bundle <path>`)
- [ ] Sensitive data removed (API keys, internal IPs, proprietary symbols)
- [ ] Notes describe the failure context
- [ ] Metadata has accurate target, board, and firmware version

## Anonymization Confirmation

- [ ] I confirm this bundle does not contain proprietary source code
- [ ] I confirm this bundle does not contain credentials, tokens, or internal network addresses
- [ ] I confirm I have permission to share this debug artifact

## Bundle File

<!-- Attach the .json bundle file or paste it below -->

<details>
<summary>Bundle JSON</summary>

```json
{
  "metadata": {},
  "serial_log": [],
  "events": [],
  "assertions": [],
  "notes": []
}
```

</details>

## Additional Context

<!-- Any extra details that would help engineers understand this failure -->
