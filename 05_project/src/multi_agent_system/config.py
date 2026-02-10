"""Configuration helpers for the multi-agent project."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Settings:
    openai_api_key: str
    openai_model: str
    project_root: Path
    intent_min_confidence: float
    max_history_turns: int



def load_settings(project_root: Path | None = None) -> Settings:
    """Load environment settings.

    Args:
        project_root: Optional project root. If omitted, infer from this file.
    """
    root = project_root or Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Configure it in 05_project/.env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    raw_threshold = os.getenv("INTENT_MIN_CONFIDENCE", "0.60")
    raw_history = os.getenv("MAX_HISTORY_TURNS", "4")
    try:
        threshold = float(raw_threshold)
    except ValueError as exc:
        raise RuntimeError("INTENT_MIN_CONFIDENCE must be a float, e.g. 0.60") from exc
    try:
        max_history = int(raw_history)
    except ValueError as exc:
        raise RuntimeError("MAX_HISTORY_TURNS must be an int, e.g. 4") from exc

    if not 0.0 <= threshold <= 1.0:
        raise RuntimeError("INTENT_MIN_CONFIDENCE must be between 0 and 1")
    if max_history < 0:
        raise RuntimeError("MAX_HISTORY_TURNS must be >= 0")

    return Settings(
        openai_api_key=api_key,
        openai_model=model,
        project_root=root,
        intent_min_confidence=threshold,
        max_history_turns=max_history,
    )
