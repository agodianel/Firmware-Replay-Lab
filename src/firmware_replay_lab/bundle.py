from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


@dataclass
class SessionMetadata:
    target: str
    firmware_version: str
    board: str
    commit: str
    captured_at: str = field(
        default_factory=lambda: datetime.now(tz=timezone.utc).isoformat()
    )
    environment: dict[str, str] = field(default_factory=dict)


@dataclass
class SerialLine:
    timestamp_ms: int
    direction: str
    message: str


@dataclass
class ReplayBundle:
    metadata: SessionMetadata
    serial_log: list[SerialLine] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    mocked_inputs: list[dict[str, Any]] = field(default_factory=list)
    assertions: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": asdict(self.metadata),
            "serial_log": [asdict(line) for line in self.serial_log],
            "events": self.events,
            "mocked_inputs": self.mocked_inputs,
            "assertions": self.assertions,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReplayBundle":
        metadata = SessionMetadata(**data["metadata"])
        serial_log = [SerialLine(**line) for line in data.get("serial_log", [])]
        return cls(
            metadata=metadata,
            serial_log=serial_log,
            events=data.get("events", []),
            mocked_inputs=data.get("mocked_inputs", []),
            assertions=data.get("assertions", []),
            notes=data.get("notes", []),
        )

    def save_json(self, path: str | Path) -> None:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load_json(cls, path: str | Path) -> "ReplayBundle":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(payload)
