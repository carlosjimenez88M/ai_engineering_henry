"""Tests for production/scripts/resilient_agent.py"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from conftest import load_module

mod = load_module("production/scripts/resilient_agent.py")
CircuitBreaker = mod.CircuitBreaker
TokenBudget = mod.TokenBudget
CallResult = mod.CallResult
ResilientAgent = mod.ResilientAgent


class TestCircuitBreaker:
    """Tests for CircuitBreaker."""

    def test_initial_state(self):
        cb = CircuitBreaker(max_failures=3, cooldown_seconds=10)
        assert cb.state == "closed"
        assert cb.failure_count == 0
        assert cb.can_proceed() is True

    def test_opens_after_max_failures(self):
        cb = CircuitBreaker(max_failures=3, cooldown_seconds=10)

        for _ in range(3):
            cb.record_failure()

        assert cb.state == "open"
        assert cb.can_proceed() is False

    def test_success_resets(self):
        cb = CircuitBreaker(max_failures=3, cooldown_seconds=10)

        cb.record_failure()
        cb.record_failure()
        cb.record_success()

        assert cb.state == "closed"
        assert cb.failure_count == 0


class TestTokenBudget:
    """Tests for TokenBudget."""

    def test_initial_budget(self):
        budget = TokenBudget(max_tokens=1000, max_cost=0.01)
        assert budget.can_proceed() is True
        assert budget.used_tokens == 0

    def test_budget_exceeded(self):
        budget = TokenBudget(max_tokens=100, max_cost=1.0)

        budget.record(60, 50)  # 110 tokens, exceeds 100
        assert budget.can_proceed() is False

    def test_cost_tracking(self):
        budget = TokenBudget(model="gpt-5-mini", max_tokens=50000, max_cost=0.10)

        budget.record(100, 50)
        assert budget.used_tokens == 150
        assert budget.used_cost > 0


class TestCallResult:
    """Tests for CallResult dataclass."""

    def test_call_result(self):
        result = CallResult(status="ok", content="Hello", model="gpt-5-mini", tokens=100)
        assert result.status == "ok"
        assert result.content == "Hello"
        assert result.retries == 0


class TestResilientAgent:
    """Tests for ResilientAgent."""

    @patch.object(mod, "OpenAI")
    def test_budget_exceeded_returns_status(self, mock_openai_cls):
        agent = ResilientAgent(max_tokens=0, max_cost=0)  # Zero budget
        result = agent.call("Test")
        assert result.status == "budget_exceeded"

    @patch.object(mod, "OpenAI")
    def test_successful_call(self, mock_openai_cls, mock_openai_response):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_openai_response("OK response")

        agent = ResilientAgent()
        agent.client = mock_client
        result = agent.call("Test")
        assert result.status == "ok"
        assert result.content == "OK response"
