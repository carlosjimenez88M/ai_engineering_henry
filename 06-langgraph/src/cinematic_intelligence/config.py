"""Configuration settings for the Cultural Intelligence system."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-5-mini"))
    data_dir: Path = field(
        default_factory=lambda: Path(os.getenv("DATA_DIR", "./00_datos"))
    )
    langchain_tracing: bool = field(
        default_factory=lambda: os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    )

    def __post_init__(self) -> None:
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. "
                "Please set it in your .env file or environment variables."
            )


# Global settings instance
settings = Settings()
