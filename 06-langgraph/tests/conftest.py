"""
Shared fixtures for 06-langgraph tests.

All tests mock OpenAI to avoid real API calls.
Strategy:
  - mock_env (autouse): sets OPENAI_API_KEY=sk-test-fake-key
  - fake_structured_llm: a mock that supports .with_structured_output(schema)
  - data fixtures: use tmp_path with real JSON structures
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

MODULE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = MODULE_ROOT / "00_datos"


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def mock_env():
    """Ensure OPENAI_API_KEY is set and tracing is disabled for all tests."""
    with patch.dict(
        os.environ,
        {
            "OPENAI_API_KEY": "sk-test-fake-key",
            "LANGCHAIN_TRACING_V2": "false",
            "OPENAI_MODEL": "gpt-5-mini",
        },
    ):
        yield


# ---------------------------------------------------------------------------
# LLM mocks
# ---------------------------------------------------------------------------


def make_fake_structured_llm(return_value: Any) -> MagicMock:
    """
    Create a mock LLM that supports .with_structured_output(schema).

    The inner .invoke() returns return_value directly.
    """
    inner_mock = MagicMock()
    inner_mock.invoke.return_value = return_value

    outer_mock = MagicMock()
    outer_mock.with_structured_output.return_value = inner_mock
    outer_mock.invoke.return_value = MagicMock(content="Mocked response text")
    return outer_mock


@pytest.fixture
def fake_llm():
    """A simple mock LLM with a text response."""
    mock = MagicMock()
    mock.invoke.return_value = MagicMock(content="Mocked LLM response")
    mock.with_structured_output.return_value = mock
    return mock


# ---------------------------------------------------------------------------
# Data fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def nolan_films_data() -> list[dict]:
    """Load real Nolan films data."""
    path = DATA_DIR / "nolan_films.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return [
        {
            "id": "nolan_01",
            "titulo": "Memento",
            "año": 2000,
            "genero": ["thriller"],
            "temas": ["memoria", "identidad"],
            "tecnica_narrativa": "narración inversa",
            "protagonista": "Leonard Shelby",
            "sinopsis": "Un hombre con amnesia investiga el asesinato de su esposa.",
            "frases_clave": ["Remember Sammy Jankis"],
            "influencias_cinematograficas": [],
            "premios": [],
            "conexiones_tematicas": [],
        }
    ]


@pytest.fixture
def king_books_data() -> list[dict]:
    """Load real King books data."""
    path = DATA_DIR / "king_books.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return [
        {
            "id": "king_01",
            "titulo": "It",
            "año_publicacion": 1986,
            "genero": ["horror"],
            "temas": ["miedo", "infancia"],
            "protagonistas": ["Bill Denbrough"],
            "antagonista": "Pennywise",
            "escenario": "Derry, Maine",
            "sinopsis": "Un payaso maligno aterroriza a un grupo de niños.",
            "citas_memorables": ["We all float down here"],
            "adaptaciones": [],
            "longitud_paginas": 1138,
        }
    ]


@pytest.fixture
def davis_albums_data() -> list[dict]:
    """Load real Davis albums data."""
    path = DATA_DIR / "davis_albums.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return [
        {
            "id": "davis_01",
            "titulo": "Kind of Blue",
            "año": 1959,
            "sello": "Columbia Records",
            "epocas": ["modal jazz"],
            "musicos": ["Miles Davis"],
            "tecnicas": ["jazz modal"],
            "temas": ["So What"],
            "influencias": [],
            "influenciados": [],
            "descripcion": "El álbum de jazz más vendido de la historia.",
            "importancia_historica": "Definió el jazz modal.",
        }
    ]


@pytest.fixture
def tmp_data_dir(tmp_path, nolan_films_data, king_books_data, davis_albums_data) -> Path:
    """Create a temporary data directory with all three JSON files."""
    (tmp_path / "nolan_films.json").write_text(
        json.dumps(nolan_films_data, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / "king_books.json").write_text(
        json.dumps(king_books_data, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / "davis_albums.json").write_text(
        json.dumps(davis_albums_data, ensure_ascii=False), encoding="utf-8"
    )
    return tmp_path
