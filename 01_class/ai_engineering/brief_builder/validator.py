"""Input and output validation for brief builder.

This module provides validation functions for inputs (temperature, context length, paths)
and outputs (brief structure, markdown format) to ensure quality and catch errors early.
"""

import re
from pathlib import Path


def validate_temperature(temperature: float) -> None:
    """Validates that temperature is within valid range for OpenAI models.

    Args:
        temperature: The temperature parameter to validate.

    Raises:
        ValueError: If temperature is not in range [0.0, 2.0].

    Examples:
        >>> validate_temperature(0.7)  # OK
        >>> validate_temperature(2.5)  # Raises ValueError
    """
    if not 0.0 <= temperature <= 2.0:
        raise ValueError(
            f"Temperature must be between 0.0 and 2.0, got {temperature}"
        )


def validate_context_length(context: str, max_tokens: int = 4000) -> None:
    """Validates that context doesn't exceed token limit.

    Uses a simple heuristic: ~4 characters per token for English text.
    This is approximate but catches egregiously long contexts.

    Args:
        context: The context string to validate.
        max_tokens: Maximum allowed tokens (default 4000).

    Raises:
        ValueError: If estimated token count exceeds max_tokens.

    Examples:
        >>> validate_context_length("Short context")  # OK
        >>> validate_context_length("x" * 20000)  # Raises ValueError
    """
    # Rough estimate: 4 chars per token
    estimated_tokens = len(context) / 4
    if estimated_tokens > max_tokens:
        raise ValueError(
            f"Context too long: ~{int(estimated_tokens)} tokens "
            f"(max {max_tokens}). Consider shortening your context."
        )


def validate_output_path(path: Path) -> None:
    """Validates that output path is writable.

    Args:
        path: The output path to validate.

    Raises:
        ValueError: If path is not writable or parent directory doesn't exist.
        PermissionError: If insufficient permissions to write to path.

    Examples:
        >>> validate_output_path(Path("./output/brief.md"))  # OK if ./output exists
        >>> validate_output_path(Path("/root/brief.md"))  # Raises PermissionError
    """
    parent = path.parent

    # Check parent directory exists or can be created
    if not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise PermissionError(
                f"Cannot create directory {parent}: insufficient permissions"
            ) from e

    # Check if parent is writable
    if not parent.is_dir():
        raise ValueError(f"Parent path {parent} is not a directory")

    if not parent.stat().st_mode & 0o200:  # Check write permission
        raise PermissionError(f"Directory {parent} is not writable")


def validate_brief_structure(content: str) -> dict[str, bool]:
    """Validates that generated brief has required sections.

    Checks for key sections that should be present in a well-structured
    comparative brief according to the prompt template.

    Args:
        content: The generated brief content as markdown string.

    Returns:
        Dictionary with boolean flags for each required section:
        - has_executive_summary: Has "Resumen Ejecutivo" section
        - has_comparison_matrix: Has "Matriz Comparativa" section
        - has_deep_dive: Has "Deep Dive" or detailed analysis section
        - has_recommendations: Has "Recomendaciones" section
        - is_complete: True if all sections present

    Examples:
        >>> brief = "## Resumen Ejecutivo\\n...\\n## Matriz Comparativa\\n..."
        >>> result = validate_brief_structure(brief)
        >>> result['has_executive_summary']
        True
    """
    # Case-insensitive search for section headers
    content_lower = content.lower()

    checks = {
        "has_executive_summary": bool(
            re.search(r"##\s*resumen\s+ejecutivo", content_lower)
        ),
        "has_comparison_matrix": bool(
            re.search(r"##\s*matriz\s+comparativa", content_lower)
        ),
        "has_deep_dive": bool(
            re.search(r"##\s*(deep\s+dive|análisis\s+profundo)", content_lower)
        ),
        "has_recommendations": bool(
            re.search(r"##\s*recomendaciones", content_lower)
        ),
    }

    # Check if all sections present
    checks["is_complete"] = all(
        checks[key] for key in checks if key != "is_complete"
    )

    return checks


def validate_markdown_format(content: str) -> bool:
    """Validates basic markdown syntax.

    Performs lightweight checks for common markdown issues:
    - Has at least one header
    - No unclosed code blocks
    - Content is not empty

    Args:
        content: The markdown content to validate.

    Returns:
        True if content appears to be valid markdown, False otherwise.

    Examples:
        >>> validate_markdown_format("# Title\\nSome content")
        True
        >>> validate_markdown_format("")
        False
    """
    if not content or not content.strip():
        return False

    # Check for at least one markdown header
    if not re.search(r"^#+\s+.+$", content, re.MULTILINE):
        return False

    # Check for balanced code blocks (``` pairs)
    code_block_count = content.count("```")
    if code_block_count % 2 != 0:
        return False

    return True
