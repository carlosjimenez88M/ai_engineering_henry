"""Pytest fixtures for brief builder tests.

This module provides reusable test fixtures including:
- Mock OpenAI client with simulated responses
- Temporary output directories
- Sample brief responses for validation testing
"""

from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def mock_openai_client(mocker: Any) -> Any:
    """Provides a mock OpenAI client that simulates API responses.

    The mock returns a valid brief structure without making actual API calls.
    This allows testing the integration without incurring costs or rate limits.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        Mock OpenAI client with pre-configured responses.

    Examples:
        >>> def test_something(mock_openai_client):
        ...     # Use mock_openai_client instead of real client
        ...     response = mock_openai_client.chat.completions.create(...)
        ...     assert response.choices[0].message.content
    """
    mock_response = mocker.Mock()
    mock_choice = mocker.Mock()
    mock_message = mocker.Mock()
    mock_usage = mocker.Mock()

    # Configure usage stats
    mock_usage.prompt_tokens = 1000
    mock_usage.completion_tokens = 500
    mock_usage.total_tokens = 1500

    # Configure message content
    mock_message.content = """# Software Engineering vs AI Engineering

## Resumen Ejecutivo

Este brief compara los enfoques de Software Engineering y AI Engineering.

## Matriz Comparativa

| Dimension | Software Engineering | AI Engineering | Riesgo |
|-----------|---------------------|----------------|--------|
| Testing   | Unit tests          | Eval sets      | Low    |

## Deep Dive

Análisis profundo de cada fase del ciclo de vida.

## Recomendaciones

1. Usar testing riguroso
2. Monitorear métricas
"""

    # Wire up the mock
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_response.usage = mock_usage
    mock_response.model = "gpt-4o-mini"

    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response

    return mock_client


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Provides a temporary directory for output files.

    Args:
        tmp_path: pytest's built-in temporary directory fixture.

    Returns:
        Path to temporary output directory.

    Examples:
        >>> def test_save(temp_output_dir):
        ...     output_path = temp_output_dir / "test.md"
        ...     output_path.write_text("test")
        ...     assert output_path.exists()
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_brief_response() -> str:
    """Provides a sample brief response for validation testing.

    Returns:
        Valid brief markdown with all required sections.

    Examples:
        >>> def test_validation(sample_brief_response):
        ...     assert "## Resumen Ejecutivo" in sample_brief_response
    """
    return """# Software Engineering vs AI Engineering

## Resumen Ejecutivo

Este documento presenta una comparación crítica entre Software Engineering
tradicional y AI Engineering moderno, enfocándose en trade-offs prácticos
y decisiones operacionales.

## Matriz Comparativa

| Dimension | Software Engineering | AI Engineering | Riesgo si se aplica mal |
|-----------|---------------------|----------------|------------------------|
| Testing | Unit tests, integration tests | Eval sets, human review | Bugs en prod |
| Deployment | CI/CD pipelines | Model serving, monitoring | Degradación silenciosa |
| Data | Fixed schemas | Training data + feedback loops | Data drift |

## Deep Dive por Fase

### Discovery
- Artefactos: Requirements doc, tech specs
- Owner: Product + Engineering
- Failure mode: Building wrong thing
- Exit criteria: Approved design doc

### Build
- Artefactos: Code, tests
- Owner: Engineering
- Failure mode: Technical debt
- Exit criteria: Passing tests

### Test/Evaluación
- Artefactos: Test results
- Owner: QA + Engineering
- Failure mode: Insufficient coverage
- Exit criteria: 80%+ coverage

### Deployment
- Artefactos: Release artifacts
- Owner: DevOps
- Failure mode: Rollback required
- Exit criteria: Successful deployment

### Monitoreo
- Artefactos: Dashboards, alerts
- Owner: SRE
- Failure mode: Silent failures
- Exit criteria: All metrics green

## Recomendaciones

1. Validar inputs antes de procesamiento
2. Implementar retry logic con exponential backoff
3. Trackear costos y latencia por request
4. Versionar prompts en git
5. Establecer métricas de calidad
"""


@pytest.fixture
def sample_invalid_brief() -> str:
    """Provides an invalid brief for negative testing.

    Returns:
        Brief missing required sections.

    Examples:
        >>> def test_validation_failure(sample_invalid_brief):
        ...     result = validate_brief_structure(sample_invalid_brief)
        ...     assert not result['is_complete']
    """
    return """# Incomplete Brief

This brief is missing required sections like Resumen Ejecutivo
and Matriz Comparativa.
"""
