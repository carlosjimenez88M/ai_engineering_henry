"""
test_tool_calling.py

Objetivo del script: 
Tests for 02_langchain/scripts/tool_calling_agent.py

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from conftest import load_module

mod = load_module("02_langchain/scripts/tool_calling_agent.py")
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
