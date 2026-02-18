"""Tests for langchain/scripts/tool_calling_agent.py"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from conftest import load_module

mod = load_module("langchain/scripts/tool_calling_agent.py")
ToolCallingAgent = mod.ToolCallingAgent


class TestToolCallingAgent:
    """Tests for the ToolCallingAgent class."""

    @patch.object(mod, "ChatOpenAI")
    def test_agent_creation(self, mock_llm_cls):
        from langchain_core.tools import tool

        @tool
        def dummy_tool(x: str) -> str:
            """A dummy tool for testing.

            Args:
                x: Input string.
            """
            return f"result: {x}"

        mock_llm = MagicMock()
        mock_llm_cls.return_value = mock_llm
        mock_llm.bind_tools.return_value = mock_llm

        agent = ToolCallingAgent(tools=[dummy_tool], model="gpt-5-mini")
        assert agent.tools == [dummy_tool]
        mock_llm.bind_tools.assert_called_once()
