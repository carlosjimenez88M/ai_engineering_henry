"""Tests for main brief generation logic."""

import sys
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest

# Add brief_builder to path for imports
BRIEF_BUILDER_DIR = Path(__file__).resolve().parent.parent / "brief_builder"
if str(BRIEF_BUILDER_DIR) not in sys.path:
    sys.path.insert(0, str(BRIEF_BUILDER_DIR))

from main import generate_brief, parse_args, save_output


class TestParseArgs:
    """Tests for command-line argument parsing."""

    @pytest.mark.unit
    def test_default_arguments(self, monkeypatch: pytest.MonkeyPatch):
        """Test that default arguments are set correctly."""
        monkeypatch.setattr("sys.argv", ["main.py"])
        args = parse_args()

        assert args.output == Path(
            "01_class/ai_engineering/briefs/software_vs_ai_engineering.md"
        )
        assert args.context == ""
        assert args.temperature == 0.2

    @pytest.mark.unit
    def test_custom_output(self, monkeypatch: pytest.MonkeyPatch):
        """Test custom output path."""
        monkeypatch.setattr("sys.argv", ["main.py", "--output", "custom.md"])
        args = parse_args()

        assert args.output == Path("custom.md")

    @pytest.mark.unit
    def test_custom_context(self, monkeypatch: pytest.MonkeyPatch):
        """Test custom context."""
        monkeypatch.setattr(
            "sys.argv", ["main.py", "--context", "Fintech startup"]
        )
        args = parse_args()

        assert args.context == "Fintech startup"

    @pytest.mark.unit
    def test_custom_temperature(self, monkeypatch: pytest.MonkeyPatch):
        """Test custom temperature."""
        monkeypatch.setattr("sys.argv", ["main.py", "--temperature", "0.5"])
        args = parse_args()

        assert args.temperature == 0.5

    @pytest.mark.unit
    def test_all_custom_arguments(self, monkeypatch: pytest.MonkeyPatch):
        """Test all arguments customized."""
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--output",
                "test.md",
                "--context",
                "Healthcare",
                "--temperature",
                "0.1",
            ],
        )
        args = parse_args()

        assert args.output == Path("test.md")
        assert args.context == "Healthcare"
        assert args.temperature == 0.1


class TestGenerateBrief:
    """Tests for brief generation."""

    @pytest.mark.unit
    def test_generate_brief_returns_string(
        self, monkeypatch: pytest.MonkeyPatch, mock_openai_client: Any
    ):
        """Test that generate_brief returns a tuple with brief and metrics."""
        # Mock load_settings
        mock_settings = Mock()
        mock_settings.openai_api_key = "sk-test"
        mock_settings.openai_model = "gpt-4o-mini"

        # Mock OpenAI client
        monkeypatch.setattr("main.load_settings", lambda: mock_settings)
        monkeypatch.setattr("main.OpenAI", lambda api_key: mock_openai_client)

        brief, metrics = generate_brief(context="", temperature=0.2)

        assert isinstance(brief, str)
        assert len(brief) > 0
        assert "Software Engineering" in brief
        assert metrics.total_tokens == 1500
        assert metrics.estimated_cost_usd > 0

    @pytest.mark.unit
    def test_generate_brief_uses_temperature(
        self, monkeypatch: pytest.MonkeyPatch, mock_openai_client: Any
    ):
        """Test that temperature is passed to API."""
        mock_settings = Mock()
        mock_settings.openai_api_key = "sk-test"
        mock_settings.openai_model = "gpt-4o-mini"

        monkeypatch.setattr("main.load_settings", lambda: mock_settings)
        monkeypatch.setattr("main.OpenAI", lambda api_key: mock_openai_client)

        brief, metrics = generate_brief(context="", temperature=0.7)

        # Verify temperature was passed
        call_args = mock_openai_client.chat.completions.create.call_args
        assert call_args.kwargs["temperature"] == 0.7
        assert metrics.temperature == 0.7

    @pytest.mark.unit
    def test_generate_brief_uses_model(
        self, monkeypatch: pytest.MonkeyPatch, mock_openai_client: Any
    ):
        """Test that correct model is used."""
        mock_settings = Mock()
        mock_settings.openai_api_key = "sk-test"
        mock_settings.openai_model = "gpt-4o"

        monkeypatch.setattr("main.load_settings", lambda: mock_settings)
        monkeypatch.setattr("main.OpenAI", lambda api_key: mock_openai_client)

        brief, metrics = generate_brief(context="", temperature=0.2)

        # Verify model was passed
        call_args = mock_openai_client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "gpt-4o"
        assert metrics.model == "gpt-4o"

    @pytest.mark.unit
    def test_generate_brief_includes_context(
        self, monkeypatch: pytest.MonkeyPatch, mock_openai_client: Any
    ):
        """Test that custom context is included in prompt."""
        mock_settings = Mock()
        mock_settings.openai_api_key = "sk-test"
        mock_settings.openai_model = "gpt-4o-mini"

        monkeypatch.setattr("main.load_settings", lambda: mock_settings)
        monkeypatch.setattr("main.OpenAI", lambda api_key: mock_openai_client)

        brief, metrics = generate_brief(context="B2B SaaS", temperature=0.2)

        # Verify context was included in messages
        call_args = mock_openai_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        user_message = messages[1]["content"]
        assert "B2B SaaS" in user_message
        assert metrics.context == "B2B SaaS"

    @pytest.mark.unit
    def test_generate_brief_empty_response_raises(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        """Test that empty API response raises APIError."""
        from exceptions import APIError

        mock_settings = Mock()
        mock_settings.openai_api_key = "sk-test"
        mock_settings.openai_model = "gpt-4o-mini"

        # Create mock with empty content
        mock_client = Mock()
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = None  # Empty response
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_usage = Mock()
        mock_usage.prompt_tokens = 100
        mock_usage.completion_tokens = 0
        mock_usage.total_tokens = 100
        mock_response.usage = mock_usage
        mock_client.chat.completions.create.return_value = mock_response

        monkeypatch.setattr("main.load_settings", lambda: mock_settings)
        monkeypatch.setattr("main.OpenAI", lambda api_key: mock_client)

        with pytest.raises(APIError) as exc_info:
            generate_brief(context="", temperature=0.2)

        assert "vacia" in str(exc_info.value)


class TestSaveOutput:
    """Tests for saving output to file."""

    @pytest.mark.unit
    def test_save_output_creates_file(self, tmp_path: Path):
        """Test that save_output creates file with content."""
        output_path = tmp_path / "test.md"
        content = "# Test Brief\n\nContent here."

        result = save_output(content, output_path)

        assert result == output_path
        assert output_path.exists()
        assert output_path.read_text() == "# Test Brief\n\nContent here.\n"

    @pytest.mark.unit
    def test_save_output_creates_parent_dirs(self, tmp_path: Path):
        """Test that parent directories are created if missing."""
        output_path = tmp_path / "subdir" / "nested" / "test.md"
        content = "# Test"

        save_output(content, output_path)

        assert output_path.exists()
        assert output_path.parent.exists()

    @pytest.mark.unit
    def test_save_output_strips_content(self, tmp_path: Path):
        """Test that content is stripped before saving."""
        output_path = tmp_path / "test.md"
        content = "\n\n  # Test  \n\n"

        save_output(content, output_path)

        saved_content = output_path.read_text()
        assert saved_content == "# Test\n"

    @pytest.mark.unit
    def test_save_output_uses_utf8(self, tmp_path: Path):
        """Test that UTF-8 encoding is used."""
        output_path = tmp_path / "test.md"
        content = "# Test\n\n日本語 한글 العربية"

        save_output(content, output_path)

        # Read with explicit UTF-8 and verify
        saved = output_path.read_text(encoding="utf-8")
        assert "日本語" in saved
        assert "한글" in saved
        assert "العربية" in saved

    @pytest.mark.unit
    def test_save_output_overwrites_existing(self, tmp_path: Path):
        """Test that existing files are overwritten."""
        output_path = tmp_path / "test.md"
        output_path.write_text("Old content")

        save_output("New content", output_path)

        assert output_path.read_text() == "New content\n"


@pytest.mark.integration
class TestEndToEndIntegration:
    """Integration tests for the full brief generation workflow."""

    def test_full_workflow_with_mock_api(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mock_openai_client: Any
    ):
        """Test complete workflow from args to saved file."""
        # Setup
        mock_settings = Mock()
        mock_settings.openai_api_key = "sk-test"
        mock_settings.openai_model = "gpt-4o-mini"

        monkeypatch.setattr("main.load_settings", lambda: mock_settings)
        monkeypatch.setattr("main.OpenAI", lambda api_key: mock_openai_client)

        output_path = tmp_path / "brief.md"

        # Execute
        brief, metrics = generate_brief(context="Test context", temperature=0.2)
        result_path = save_output(brief, output_path, metrics)

        # Verify
        assert result_path == output_path
        assert output_path.exists()
        content = output_path.read_text()
        assert "Software Engineering" in content
        assert "Resumen Ejecutivo" in content
        assert "Matriz Comparativa" in content

        # Verify metrics file was created
        metrics_path = tmp_path / "brief.metrics.json"
        assert metrics_path.exists()
