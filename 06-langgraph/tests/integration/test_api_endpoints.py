"""Integration tests for the FastAPI endpoints."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from langchain_core.messages import HumanMessage

from cinematic_intelligence.models import CulturalResponse, DomainEnum


@pytest.fixture
def mock_graph():
    """Mock graph that returns a CulturalResponse without calling OpenAI."""
    mock = MagicMock()
    mock.invoke.return_value = {
        "messages": [HumanMessage(content="Test")],
        "domain": DomainEnum.NOLAN,
        "final_response": CulturalResponse(
            domain=DomainEnum.NOLAN,
            query="Test query",
            final_answer="This is a test response about Nolan films.",
            sources_consulted=["Inception (2010)"],
            confidence=0.9,
        ),
    }
    mock.stream.return_value = iter([
        {"router": {"domain": "nolan"}},
        {"nolan_specialist": {"domain_result": {"film_title": "Inception"}}},
    ])
    return mock


@pytest.fixture
def client(mock_graph):
    """Create a TestClient with a mocked graph."""
    with patch("cinematic_intelligence.graph.make_cultural_graph", return_value=mock_graph):
        from cinematic_intelligence.api.main import app
        with TestClient(app) as c:
            yield c


class TestRootEndpoint:
    def test_health_check(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestDomainsEndpoint:
    def test_returns_domain_list(self, client):
        response = client.get("/domains")
        assert response.status_code == 200
        domains = response.json()
        assert "nolan" in domains
        assert "king" in domains
        assert "davis" in domains
        assert "general" not in domains  # general is excluded


class TestChatEndpoint:
    def test_chat_returns_response(self, client):
        response = client.post(
            "/chat/test_thread_1",
            json={"message": "Tell me about Inception"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "final_answer" in data
        assert data["domain"] == "nolan"

    def test_chat_different_threads(self, client):
        resp1 = client.post("/chat/thread_a", json={"message": "Inception?"})
        resp2 = client.post("/chat/thread_b", json={"message": "Kind of Blue?"})
        assert resp1.status_code == 200
        assert resp2.status_code == 200


class TestStreamEndpoint:
    def test_stream_returns_event_stream(self, client):
        response = client.post(
            "/chat/stream_thread/stream",
            json={"message": "Tell me about Inception"},
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]


class TestDeleteEndpoint:
    def test_delete_returns_501(self, client):
        response = client.delete("/chat/some_thread")
        assert response.status_code == 501
