"""Tests for validation functions."""

import sys
from pathlib import Path

import pytest

# Add brief_builder to path for imports
BRIEF_BUILDER_DIR = Path(__file__).resolve().parent.parent / "brief_builder"
if str(BRIEF_BUILDER_DIR) not in sys.path:
    sys.path.insert(0, str(BRIEF_BUILDER_DIR))

from validator import (
    validate_brief_structure,
    validate_context_length,
    validate_markdown_format,
    validate_output_path,
    validate_temperature,
)


class TestValidateTemperature:
    """Tests for temperature validation."""

    @pytest.mark.unit
    def test_valid_temperature_low(self):
        """Test that 0.0 is valid."""
        validate_temperature(0.0)  # Should not raise

    @pytest.mark.unit
    def test_valid_temperature_mid(self):
        """Test that 1.0 is valid."""
        validate_temperature(1.0)  # Should not raise

    @pytest.mark.unit
    def test_valid_temperature_high(self):
        """Test that 2.0 is valid."""
        validate_temperature(2.0)  # Should not raise

    @pytest.mark.unit
    def test_invalid_temperature_negative(self):
        """Test that negative temperature raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            validate_temperature(-0.1)
        assert "must be between 0.0 and 2.0" in str(exc_info.value)

    @pytest.mark.unit
    def test_invalid_temperature_too_high(self):
        """Test that temperature > 2.0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            validate_temperature(2.1)
        assert "must be between 0.0 and 2.0" in str(exc_info.value)

    @pytest.mark.unit
    def test_invalid_temperature_way_too_high(self):
        """Test that very high temperature raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            validate_temperature(10.0)
        assert "must be between 0.0 and 2.0" in str(exc_info.value)


class TestValidateContextLength:
    """Tests for context length validation."""

    @pytest.mark.unit
    def test_valid_short_context(self):
        """Test that short context is valid."""
        validate_context_length("Short context")  # Should not raise

    @pytest.mark.unit
    def test_valid_medium_context(self):
        """Test that medium context is valid."""
        context = "x" * 1000
        validate_context_length(context)  # Should not raise

    @pytest.mark.unit
    def test_valid_near_limit(self):
        """Test context just under limit."""
        # 4000 tokens * 4 chars = 16000 chars
        context = "x" * 15999
        validate_context_length(context, max_tokens=4000)  # Should not raise

    @pytest.mark.unit
    def test_invalid_too_long(self):
        """Test that context exceeding limit raises ValueError."""
        # 4000 tokens * 4 chars = 16000 chars
        context = "x" * 20000
        with pytest.raises(ValueError) as exc_info:
            validate_context_length(context, max_tokens=4000)
        assert "Context too long" in str(exc_info.value)

    @pytest.mark.unit
    def test_custom_max_tokens(self):
        """Test validation with custom max_tokens."""
        context = "x" * 300
        validate_context_length(context, max_tokens=100)  # 75 tokens, should pass

        context = "x" * 1000
        with pytest.raises(ValueError):
            validate_context_length(context, max_tokens=200)  # 250 estimated tokens, should fail


class TestValidateOutputPath:
    """Tests for output path validation."""

    @pytest.mark.unit
    def test_valid_path_existing_dir(self, tmp_path: Path):
        """Test validation with existing writable directory."""
        output_path = tmp_path / "output.md"
        validate_output_path(output_path)  # Should not raise

    @pytest.mark.unit
    def test_valid_path_creates_parent(self, tmp_path: Path):
        """Test that missing parent directories are created."""
        output_path = tmp_path / "subdir" / "output.md"
        validate_output_path(output_path)
        assert output_path.parent.exists()

    @pytest.mark.unit
    def test_valid_path_nested_dirs(self, tmp_path: Path):
        """Test creating multiple nested directories."""
        output_path = tmp_path / "a" / "b" / "c" / "output.md"
        validate_output_path(output_path)
        assert output_path.parent.exists()

    @pytest.mark.unit
    def test_invalid_path_not_dir(self, tmp_path: Path):
        """Test that non-directory parent raises ValueError."""
        # Create a file where we expect a directory
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        output_path = file_path / "output.md"  # file.txt is not a dir
        with pytest.raises(ValueError) as exc_info:
            validate_output_path(output_path)
        assert "not a directory" in str(exc_info.value)


class TestValidateBriefStructure:
    """Tests for brief structure validation."""

    @pytest.mark.unit
    def test_complete_brief(self, sample_brief_response: str):
        """Test that complete brief passes all checks."""
        result = validate_brief_structure(sample_brief_response)

        assert result["has_executive_summary"] is True
        assert result["has_comparison_matrix"] is True
        assert result["has_deep_dive"] is True
        assert result["has_recommendations"] is True
        assert result["is_complete"] is True

    @pytest.mark.unit
    def test_missing_executive_summary(self):
        """Test detection of missing executive summary."""
        brief = """# Title

## Matriz Comparativa

Table here.

## Deep Dive

Analysis here.

## Recomendaciones

Recommendations here.
"""
        result = validate_brief_structure(brief)
        assert result["has_executive_summary"] is False
        assert result["is_complete"] is False

    @pytest.mark.unit
    def test_missing_comparison_matrix(self):
        """Test detection of missing comparison matrix."""
        brief = """# Title

## Resumen Ejecutivo

Summary here.

## Deep Dive

Analysis here.

## Recomendaciones

Recommendations here.
"""
        result = validate_brief_structure(brief)
        assert result["has_comparison_matrix"] is False
        assert result["is_complete"] is False

    @pytest.mark.unit
    def test_missing_deep_dive(self):
        """Test detection of missing deep dive."""
        brief = """# Title

## Resumen Ejecutivo

Summary here.

## Matriz Comparativa

Table here.

## Recomendaciones

Recommendations here.
"""
        result = validate_brief_structure(brief)
        assert result["has_deep_dive"] is False
        assert result["is_complete"] is False

    @pytest.mark.unit
    def test_missing_recommendations(self):
        """Test detection of missing recommendations."""
        brief = """# Title

## Resumen Ejecutivo

Summary here.

## Matriz Comparativa

Table here.

## Deep Dive

Analysis here.
"""
        result = validate_brief_structure(brief)
        assert result["has_recommendations"] is False
        assert result["is_complete"] is False

    @pytest.mark.unit
    def test_case_insensitive_matching(self):
        """Test that section headers are matched case-insensitively."""
        brief = """# Title

## RESUMEN EJECUTIVO

Summary here.

## MATRIZ COMPARATIVA

Table here.

## DEEP DIVE

Analysis here.

## RECOMENDACIONES

Recommendations here.
"""
        result = validate_brief_structure(brief)
        assert result["is_complete"] is True

    @pytest.mark.unit
    def test_analisis_profundo_alternative(self):
        """Test that 'Análisis Profundo' is accepted as alternative."""
        brief = """# Title

## Resumen Ejecutivo

Summary.

## Matriz Comparativa

Table.

## Análisis Profundo

Analysis.

## Recomendaciones

Recs.
"""
        result = validate_brief_structure(brief)
        assert result["has_deep_dive"] is True


class TestValidateMarkdownFormat:
    """Tests for markdown format validation."""

    @pytest.mark.unit
    def test_valid_simple_markdown(self):
        """Test valid simple markdown."""
        content = "# Title\n\nSome content here."
        assert validate_markdown_format(content) is True

    @pytest.mark.unit
    def test_valid_complex_markdown(self):
        """Test valid complex markdown with code blocks."""
        content = """# Title

## Section

Some text.

```python
def foo():
    pass
```

More text.
"""
        assert validate_markdown_format(content) is True

    @pytest.mark.unit
    def test_invalid_empty_content(self):
        """Test that empty content is invalid."""
        assert validate_markdown_format("") is False

    @pytest.mark.unit
    def test_invalid_whitespace_only(self):
        """Test that whitespace-only content is invalid."""
        assert validate_markdown_format("   \n\n  ") is False

    @pytest.mark.unit
    def test_invalid_no_headers(self):
        """Test that content without headers is invalid."""
        content = "Just some text without any markdown headers."
        assert validate_markdown_format(content) is False

    @pytest.mark.unit
    def test_invalid_unbalanced_code_blocks(self):
        """Test that unbalanced code blocks are invalid."""
        content = """# Title

Some text.

```python
def foo():
    pass
"""
        assert validate_markdown_format(content) is False

    @pytest.mark.unit
    def test_valid_multiple_code_blocks(self):
        """Test that multiple balanced code blocks are valid."""
        content = """# Title

```python
code1
```

```bash
code2
```
"""
        assert validate_markdown_format(content) is True
