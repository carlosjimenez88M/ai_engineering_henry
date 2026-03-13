"""
test_router_node.py

Objetivo del script: 
Unit tests for the router node.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from langchain_core.messages import HumanMessage

from cinematic_intelligence.models import DomainEnum, DomainRoute
from cinematic_intelligence.nodes.router import build_router_node


class TestRouterNode:
    def _make_llm(self, domain: DomainEnum) -> MagicMock:
        structured = MagicMock()
        structured.invoke.return_value = DomainRoute(
            domain=domain,
            confidence=0.95,
            reasoning=f"Query is about {domain.value}",
        )
        llm = MagicMock()
        llm.with_structured_output.return_value = structured
        return llm

    def test_routes_to_nolan(self):
        llm = self._make_llm(DomainEnum.NOLAN)
        node = build_router_node(llm)
        state = {"messages": [HumanMessage(content="Tell me about Inception")]}
        result = node(state)
        assert result["domain"] == DomainEnum.NOLAN
        assert result["routing_confidence"] == 0.95

    def test_routes_to_king(self):
        llm = self._make_llm(DomainEnum.KING)
        node = build_router_node(llm)
        state = {"messages": [HumanMessage(content="What is It about?")]}
        result = node(state)
        assert result["domain"] == DomainEnum.KING

    def test_routes_to_davis(self):
        llm = self._make_llm(DomainEnum.DAVIS)
        node = build_router_node(llm)
        state = {"messages": [HumanMessage(content="Kind of Blue album")]}
        result = node(state)
        assert result["domain"] == DomainEnum.DAVIS

    def test_returns_routing_reasoning(self):
        llm = self._make_llm(DomainEnum.NOLAN)
        node = build_router_node(llm)
        state = {"messages": [HumanMessage(content="Nolan films")]}
        result = node(state)
        assert "routing_reasoning" in result
        assert isinstance(result["routing_reasoning"], str)

    def test_calls_with_structured_output(self):
        llm = self._make_llm(DomainEnum.GENERAL)
        node = build_router_node(llm)
        state = {"messages": [HumanMessage(content="Hello")]}
        node(state)
        llm.with_structured_output.assert_called_once_with(DomainRoute)
