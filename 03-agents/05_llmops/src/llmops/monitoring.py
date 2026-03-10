from __future__ import annotations

import json
from pathlib import Path

from llmops.models import MonitorEvent


class JsonlMonitor:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: MonitorEvent) -> None:
        with self.output_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
