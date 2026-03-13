"""
test_synthesizer.py

Objetivo del script: 
Unit tests for the synthesizer node.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, HumanMessage

from cinematic_intelligence.models import CulturalResponse, DomainEnum
from cinematic_intelligence.nodes.synthesizer import build_synthesizer_node


def _make_state(domain: DomainEnum, domain_result: dict) -> dict:
    return {
        "messages": [
            HumanMessage(content="Original query"),
            AIMessage(content="Specialist analysis"),
        ],
        "domain": domain,
        "routing_confidence": 0.9,
        "routing_reasoning": "test routing",
        "domain_result": domain_result,
        "final_response": None,
    }


class TestSynthesizerNode:
    def test_returns_final_response(self):
        expected = CulturalResponse(
            domain=DomainEnum.NOLAN,
            query="Original query",
            final_answer="Inception is a masterpiece about shared dreams.",
            sources_consulted=["Inception (2010)"],
        )
        structured = MagicMock()
        structured.invoke.return_value = expected
        llm = MagicMock()
        llm.with_structured_output.return_value = structured

        node = build_synthesizer_node(llm)
        state = _make_state(
            DomainEnum.NOLAN,
            {"film_title": "Inception", "analysis": "A dream heist film."},
        )
        result = node(state)

        assert result["final_response"] is not None
        assert result["final_response"].final_answer == expected.final_answer

    def test_final_answer_not_none(self):
        expected = CulturalResponse(
            domain=DomainEnum.KING,
            query="Original query",
            final_answer="It is about childhood fears.",
        )
        structured = MagicMock()
        structured.invoke.return_value = expected
        llm = MagicMock()
        llm.with_structured_output.return_value = structured

        node = build_synthesizer_node(llm)
        state = _make_state(
            DomainEnum.KING,
            {"book_title": "It", "analysis": "A horror classic."},
        )
        result = node(state)
        assert result["final_response"].final_answer is not None

    def test_fallback_on_structured_output_error(self):
        structured = MagicMock()
        structured.invoke.side_effect = ValueError("Schema error")
        llm = MagicMock()
        llm.with_structured_output.return_value = structured

        node = build_synthesizer_node(llm)
        state = _make_state(DomainEnum.DAVIS, {"album_title": "Kind of Blue"})
        result = node(state)

        # Fallback uses last AIMessage content
        assert result["final_response"] is not None
        assert result["final_response"].final_answer == "Specialist analysis"
