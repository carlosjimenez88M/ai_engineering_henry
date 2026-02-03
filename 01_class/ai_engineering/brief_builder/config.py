"""Configuration management for brief builder.

This module handles loading and validating configuration from environment variables.
Following the twelve-factor app methodology, all configuration is read from the
environment, with sensible defaults where appropriate.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

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

    Reads configuration from .env file and environment. The .env file is loaded
    automatically if present in the working directory or any parent directory.

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
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY no esta configurado. Agregalo en .env antes de ejecutar."
        )

    return Settings(openai_api_key=api_key, openai_model=model)
