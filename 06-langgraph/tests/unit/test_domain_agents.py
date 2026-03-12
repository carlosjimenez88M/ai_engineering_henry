"""Unit tests for the domain specialist nodes."""

from __future__ import annotations

from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, HumanMessage

from cinematic_intelligence.data_loader import DataLoader
from cinematic_intelligence.models import (
    DavisAlbumAnalysis,
    DomainEnum,
    KingBookAnalysis,
    NolanFilmAnalysis,
)
from cinematic_intelligence.nodes.davis_agent import build_davis_node
from cinematic_intelligence.nodes.king_agent import build_king_node
from cinematic_intelligence.nodes.nolan_agent import build_nolan_node


def _make_state(query: str, domain: DomainEnum = DomainEnum.NOLAN) -> dict:
    return {
        "messages": [HumanMessage(content=query)],
        "domain": domain,
        "routing_confidence": 0.9,
        "routing_reasoning": "test",
        "domain_result": None,
        "final_response": None,
    }


class TestNolanNode:
    def test_returns_domain_result(self, tmp_data_dir):
        analysis = NolanFilmAnalysis(
            film_title="Inception",
            analysis="A film about shared dreaming.",
        )
        structured = MagicMock()
        structured.invoke.return_value = analysis
        llm = MagicMock()
        llm.with_structured_output.return_value = structured

        loader = DataLoader(data_dir=tmp_data_dir)
        node = build_nolan_node(llm, loader)
        result = node(_make_state("Tell me about Inception"))

        assert result["domain_result"]["film_title"] == "Inception"
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)

    def test_fallback_on_structured_output_error(self, tmp_data_dir):
        structured = MagicMock()
        structured.invoke.side_effect = ValueError("Schema mismatch")
        llm = MagicMock()
        llm.with_structured_output.return_value = structured
        llm.invoke.return_value = MagicMock(content="Fallback nolan response")

        loader = DataLoader(data_dir=tmp_data_dir)
        node = build_nolan_node(llm, loader)
        result = node(_make_state("Tell me about Tenet"))

        assert result["domain_result"] is not None
        assert "analysis" in result["domain_result"]


class TestKingNode:
    def test_returns_domain_result(self, tmp_data_dir):
        analysis = KingBookAnalysis(
            book_title="It",
            analysis="A horror novel about Pennywise.",
        )
        structured = MagicMock()
        structured.invoke.return_value = analysis
        llm = MagicMock()
        llm.with_structured_output.return_value = structured

        loader = DataLoader(data_dir=tmp_data_dir)
        node = build_king_node(llm, loader)
        result = node(_make_state("Tell me about It", DomainEnum.KING))

        assert result["domain_result"]["book_title"] == "It"

    def test_fallback_on_error(self, tmp_data_dir):
        structured = MagicMock()
        structured.invoke.side_effect = RuntimeError("API error")
        llm = MagicMock()
        llm.with_structured_output.return_value = structured
        llm.invoke.return_value = MagicMock(content="Fallback king response")

        loader = DataLoader(data_dir=tmp_data_dir)
        node = build_king_node(llm, loader)
        result = node(_make_state("Stephen King", DomainEnum.KING))
        assert result["domain_result"]["analysis"] == "Fallback king response"


class TestDavisNode:
    def test_returns_domain_result(self, tmp_data_dir):
        analysis = DavisAlbumAnalysis(
            album_title="Kind of Blue",
            analysis="The most influential jazz album.",
        )
        structured = MagicMock()
        structured.invoke.return_value = analysis
        llm = MagicMock()
        llm.with_structured_output.return_value = structured

        loader = DataLoader(data_dir=tmp_data_dir)
        node = build_davis_node(llm, loader)
        result = node(_make_state("Kind of Blue", DomainEnum.DAVIS))

        assert result["domain_result"]["album_title"] == "Kind of Blue"

    def test_fallback_on_error(self, tmp_data_dir):
        structured = MagicMock()
        structured.invoke.side_effect = RuntimeError("API error")
        llm = MagicMock()
        llm.with_structured_output.return_value = structured
        llm.invoke.return_value = MagicMock(content="Fallback davis response")

        loader = DataLoader(data_dir=tmp_data_dir)
        node = build_davis_node(llm, loader)
        result = node(_make_state("Miles Davis", DomainEnum.DAVIS))
        assert result["domain_result"]["analysis"] == "Fallback davis response"
