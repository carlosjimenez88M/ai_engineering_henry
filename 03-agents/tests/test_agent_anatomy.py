"""Tests for intro/scripts/agent_anatomy.py"""

from __future__ import annotations

from unittest.mock import MagicMock

from conftest import load_module

mod = load_module("intro/scripts/agent_anatomy.py")
CostTracker = mod.CostTracker
AgentResult = mod.AgentResult
AgentMetrics = mod.AgentMetrics
react_agent = mod.react_agent


class TestCostTracker:
    """Tests for the CostTracker class."""

    def test_cost_tracker_init(self):
        tracker = CostTracker(model="gpt-5-mini")
        assert tracker.model == "gpt-5-mini"
        assert tracker.total_costo == 0.0
        assert tracker.total_tokens == 0

    def test_cost_tracker_track(self):
        tracker = CostTracker(model="gpt-5-mini")

        mock_usage = MagicMock()
        mock_usage.prompt_tokens = 100
        mock_usage.completion_tokens = 50
        mock_usage.total_tokens = 150

        entry = tracker.track(mock_usage, latency_ms=200.0, label="test")

        assert entry["label"] == "test"
        assert entry["input_tokens"] == 100
        assert entry["output_tokens"] == 50
        assert entry["total_tokens"] == 150
        assert entry["latencia_ms"] == 200.0
        assert entry["costo_total"] > 0
        assert tracker.total_tokens == 150
        assert len(tracker.calls) == 1

    def test_cost_tracker_multiple_calls(self):
        tracker = CostTracker(model="gpt-5-mini")

        for _i in range(5):
            mock_usage = MagicMock()
            mock_usage.prompt_tokens = 100
            mock_usage.completion_tokens = 50
            mock_usage.total_tokens = 150
            tracker.track(mock_usage, latency_ms=100.0)

        assert len(tracker.calls) == 5
        assert tracker.total_tokens == 750


class TestAgentResult:
    """Tests for AgentResult dataclass."""

    def test_agent_result_creation(self):
        result = AgentResult(
            pregunta="Test?",
            respuesta="Test response",
            metricas=AgentMetrics(total_steps=1),
        )

        assert result.pregunta == "Test?"
        assert result.respuesta == "Test response"
        assert result.metricas.total_steps == 1


class TestReactAgent:
    """Tests for the react_agent function."""

    def test_react_agent_no_tools(self, mock_openai_response):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response("Respuesta directa")

        result = react_agent(
            pregunta="Hola",
            tools_schema=[],
            tools_registry={},
            client=mock_client,
        )

        assert result.respuesta == "Respuesta directa"
        assert result.metricas.total_steps >= 1
