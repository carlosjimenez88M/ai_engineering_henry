from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    api_key: str | None = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def default_dataset(module_root: Path) -> Path:
        return module_root / "LLMops" / "data" / "tickets_eval.jsonl"

    @staticmethod
    def default_output_dir(module_root: Path) -> Path:
        return module_root / "LLMops" / "outputs"
