"""Tests for configuration loading and validation."""

import sys
from pathlib import Path

import pytest

# Add brief_builder to path for imports
BRIEF_BUILDER_DIR = Path(__file__).resolve().parent.parent / "brief_builder"
if str(BRIEF_BUILDER_DIR) not in sys.path:
    sys.path.insert(0, str(BRIEF_BUILDER_DIR))

from config import Settings, load_settings


@pytest.mark.unit
def test_settings_dataclass():
    """Test Settings dataclass creation."""
    settings = Settings(
        openai_api_key="sk-test123",
        openai_model="gpt-4o-mini"
    )
    assert settings.openai_api_key == "sk-test123"
    assert settings.openai_model == "gpt-4o-mini"


@pytest.mark.unit
def test_settings_frozen():
    """Test that Settings is immutable (frozen)."""
    settings = Settings(
        openai_api_key="sk-test123",
        openai_model="gpt-4o-mini"
    )
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        settings.openai_api_key = "sk-changed"  # type: ignore


@pytest.mark.unit
def test_load_settings_with_valid_api_key(monkeypatch: pytest.MonkeyPatch):
    """Test successful settings loading with valid API key."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")

    settings = load_settings()

    assert settings.openai_api_key == "sk-test123"
    assert settings.openai_model == "gpt-4o"


@pytest.mark.unit
def test_load_settings_default_model(monkeypatch: pytest.MonkeyPatch):
    """Test that default model is gpt-4o-mini when not specified."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    settings = load_settings()

    assert settings.openai_model == "gpt-4o-mini"


@pytest.mark.unit
def test_load_settings_empty_model_uses_default(monkeypatch: pytest.MonkeyPatch):
    """Test that empty OPENAI_MODEL env var falls back to default."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
    monkeypatch.setenv("OPENAI_MODEL", "")

    settings = load_settings()

    assert settings.openai_model == "gpt-4o-mini"


@pytest.mark.unit
def test_load_settings_whitespace_model_uses_default(monkeypatch: pytest.MonkeyPatch):
    """Test that whitespace-only OPENAI_MODEL uses default."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
    monkeypatch.setenv("OPENAI_MODEL", "   ")

    settings = load_settings()

    assert settings.openai_model == "gpt-4o-mini"


@pytest.mark.unit
def test_load_settings_strips_whitespace(monkeypatch: pytest.MonkeyPatch):
    """Test that settings values are stripped of whitespace."""
    monkeypatch.setenv("OPENAI_API_KEY", "  sk-test123  ")
    monkeypatch.setenv("OPENAI_MODEL", "  gpt-4o  ")

    settings = load_settings()

    assert settings.openai_api_key == "sk-test123"
    assert settings.openai_model == "gpt-4o"


@pytest.mark.unit
def test_load_settings_missing_api_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Test that RuntimeError is raised when OPENAI_API_KEY is missing."""
    # Change to temp directory to avoid loading any .env file
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError) as exc_info:
        load_settings()

    assert "OPENAI_API_KEY no esta configurado" in str(exc_info.value)


@pytest.mark.unit
def test_load_settings_empty_api_key(monkeypatch: pytest.MonkeyPatch):
    """Test that RuntimeError is raised when OPENAI_API_KEY is empty."""
    monkeypatch.setenv("OPENAI_API_KEY", "")

    with pytest.raises(RuntimeError) as exc_info:
        load_settings()

    assert "OPENAI_API_KEY no esta configurado" in str(exc_info.value)


@pytest.mark.unit
def test_load_settings_whitespace_api_key(monkeypatch: pytest.MonkeyPatch):
    """Test that RuntimeError is raised when OPENAI_API_KEY is whitespace."""
    monkeypatch.setenv("OPENAI_API_KEY", "   ")

    with pytest.raises(RuntimeError) as exc_info:
        load_settings()

    assert "OPENAI_API_KEY no esta configurado" in str(exc_info.value)


@pytest.mark.unit
def test_load_settings_reads_from_dotenv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Test that settings can be loaded from .env file."""
    # Create temporary .env file
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=sk-from-dotenv\nOPENAI_MODEL=gpt-4\n")

    # Change to temp directory so .env is found
    monkeypatch.chdir(tmp_path)
    # Clear environment to ensure we're reading from .env
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    settings = load_settings()

    assert settings.openai_api_key == "sk-from-dotenv"
    assert settings.openai_model == "gpt-4"
