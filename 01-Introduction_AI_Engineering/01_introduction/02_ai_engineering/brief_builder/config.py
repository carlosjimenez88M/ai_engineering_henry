"""Configuration management for brief builder.

This module handles loading and validating configuration from environment variables.
Following the twelve-factor app methodology, all configuration is read from the
environment, with sensible defaults where appropriate.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Immutable configuration settings for brief builder.

    Attributes:
        openai_api_key: API key for OpenAI (required).
        openai_model: OpenAI model to use (defaults to gpt-4o-mini).
    """

    openai_api_key: str
    openai_model: str


def load_settings() -> Settings:
    """Loads and validates settings from environment variables.

    Reads configuration from .env file and environment. It first loads the
    `.env` located in the current working directory. If the command is being
    executed from somewhere inside this repository and no local `.env` is found,
    it falls back to the repository root `.env`.

    Environment variables:
        OPENAI_API_KEY (required): OpenAI API key.
        OPENAI_MODEL (optional): Model to use (default: gpt-4o-mini).

    Returns:
        Settings object with validated configuration.

    Raises:
        RuntimeError: If OPENAI_API_KEY is not set or is empty.

    Examples:
        >>> # With .env file containing OPENAI_API_KEY=sk-...
        >>> settings = load_settings()
        >>> settings.openai_model
        'gpt-4o-mini'
    """
    cwd = Path.cwd().resolve()
    repo_root = Path(__file__).resolve().parents[4]
    env_candidates = [cwd / ".env"]

    if cwd == repo_root or cwd.is_relative_to(repo_root):
        env_candidates.append(repo_root / ".env")

    for env_path in env_candidates:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            break

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY no esta configurado. Agregalo en .env antes de ejecutar."
        )

    return Settings(openai_api_key=api_key, openai_model=model)
