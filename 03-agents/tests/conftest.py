"""
Shared fixtures for 03-agents tests.

All tests mock the OpenAI API to avoid real API calls and costs.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

AGENTS_ROOT = Path(__file__).resolve().parent.parent


def load_module(relative_path: str, module_name: str | None = None):
    """Carga un modulo Python por ruta relativa al root de 03-agents."""
    file_path = AGENTS_ROOT / relative_path
    if module_name is None:
        module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(autouse=True)
def mock_env():
    """Ensure OPENAI_API_KEY is set for all tests."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-fake-key"}):
        yield


@pytest.fixture
def mock_openai_response():
    """Factory for mock OpenAI chat completion responses."""

    def _make(content: str = "Mock response", input_tokens: int = 10, output_tokens: int = 20):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = content
        mock_response.choices[0].message.tool_calls = None
        mock_response.usage.prompt_tokens = input_tokens
        mock_response.usage.completion_tokens = output_tokens
        mock_response.usage.total_tokens = input_tokens + output_tokens
        return mock_response

    return _make


@pytest.fixture
def batman_comics_data():
    """Load Batman comics test data."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "batman_comics.json")
    if os.path.exists(data_path):
        with open(data_path) as f:
            return json.load(f)
    return [
        {
            "id": "batman_01",
            "personaje": "batman",
            "arco": "Year One",
            "tema": "origen",
            "titulo": "Batman: Year One",
            "contenido": "Bruce Wayne regresa a Gotham tras doce anos de entrenamiento.",
        }
    ]


@pytest.fixture
def spiderman_comics_data():
    """Load Spider-Man comics test data."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "spiderman_comics.json")
    if os.path.exists(data_path):
        with open(data_path) as f:
            return json.load(f)
    return [
        {
            "id": "spiderman_01",
            "personaje": "spiderman",
            "arco": "Origen",
            "tema": "origen",
            "titulo": "El origen de Spider-Man",
            "contenido": "Peter Parker fue mordido por una arana radiactiva.",
        }
    ]


@pytest.fixture
def eval_questions():
    """Load evaluation questions."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "comics_eval.jsonl")
    questions = []
    if os.path.exists(data_path):
        with open(data_path) as f:
            for line in f:
                questions.append(json.loads(line))
    return questions or [
        {
            "id": "eval_01",
            "pregunta": "Como se convirtio Bruce Wayne en Batman?",
            "ruta_esperada": "batman",
            "keywords": ["Wayne", "Gotham"],
        }
    ]
