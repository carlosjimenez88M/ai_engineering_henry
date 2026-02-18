"""Tests for multi-agent/scripts/orchestrator_workers.py"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from conftest import load_module

mod = load_module("multi-agent/scripts/orchestrator_workers.py")
SubtaskPlan = mod.SubtaskPlan
WorkerResult = mod.WorkerResult
Orchestrator = mod.Orchestrator


class TestOrchestrationPlan:
    """Test orchestration models."""

    def test_subtask_plan(self):
        plan = SubtaskPlan(description="Investigate Batman", worker="batman")
        assert plan.description == "Investigate Batman"
        assert plan.worker == "batman"

    def test_worker_result(self):
        result = WorkerResult(
            worker_type="batman",
            subtask="Find origin",
            result="Batman started in Year One",
        )
        assert result.worker_type == "batman"
        assert result.tokens_used == 0


class TestOrchestratorCreation:
    """Test Orchestrator class."""

    @patch.object(mod, "ChatOpenAI")
    def test_orchestrator_init(self, mock_llm_cls):
        mock_llm = MagicMock()
        mock_llm_cls.return_value = mock_llm
        mock_llm.with_structured_output.return_value = mock_llm

        orch = Orchestrator(worker_types=["batman", "spiderman"])
        assert "batman" in orch.worker_types
        assert "spiderman" in orch.worker_types
