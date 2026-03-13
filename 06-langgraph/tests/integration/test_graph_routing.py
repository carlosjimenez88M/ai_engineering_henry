"""
test_graph_routing.py

Objetivo del script: 
Integration tests for the Cultural Intelligence graph routing.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from cinematic_intelligence.models import (
    CulturalResponse,
    DavisAlbumAnalysis,
    DomainEnum,
    DomainRoute,
    KingBookAnalysis,
    NolanFilmAnalysis,
)


def _make_mock_llm(
    route_domain: DomainEnum,
    nolan_result: NolanFilmAnalysis | None = None,
    king_result: KingBookAnalysis | None = None,
    davis_result: DavisAlbumAnalysis | None = None,
    synth_result: CulturalResponse | None = None,
) -> MagicMock:
    """
    Create a mock LLM whose .with_structured_output(Schema) returns
    the appropriate result based on the schema type.
    """

    def fake_with_structured_output(schema):
        inner = MagicMock()
        if schema is DomainRoute:
            inner.invoke.return_value = DomainRoute(
                domain=route_domain, confidence=0.95, reasoning="test"
            )
        elif schema is NolanFilmAnalysis:
            result = nolan_result or NolanFilmAnalysis(
                film_title="Inception", analysis="Test nolan analysis."
            )
            inner.invoke.return_value = result
        elif schema is KingBookAnalysis:
            result = king_result or KingBookAnalysis(
                book_title="It", analysis="Test king analysis."
            )
            inner.invoke.return_value = result
        elif schema is DavisAlbumAnalysis:
            result = davis_result or DavisAlbumAnalysis(
                album_title="Kind of Blue", analysis="Test davis analysis."
            )
            inner.invoke.return_value = result
        elif schema is CulturalResponse:
            result = synth_result or CulturalResponse(
                domain=route_domain,
                query="test query",
                final_answer=f"Final answer for {route_domain.value} domain.",
            )
            inner.invoke.return_value = result
        else:
            inner.invoke.return_value = MagicMock(content="generic mock")
        return inner

    llm = MagicMock()
    llm.with_structured_output.side_effect = fake_with_structured_output
    llm.invoke.return_value = AIMessage(content="Fallback response")
    return llm


class TestGraphRouting:
    def test_routes_nolan_query(self, tmp_data_dir):
        mock_llm = _make_mock_llm(DomainEnum.NOLAN)
        with patch("cinematic_intelligence.graph.init_chat_model", return_value=mock_llm):
            from cinematic_intelligence.graph import make_cultural_graph

            graph = make_cultural_graph(data_dir=tmp_data_dir)
            result = graph.invoke(
                {"messages": [HumanMessage(content="Tell me about Inception")]}
            )

        assert result["domain"] == DomainEnum.NOLAN
        assert result["final_response"] is not None
        assert result["final_response"].domain == DomainEnum.NOLAN

    def test_routes_king_query(self, tmp_data_dir):
        mock_llm = _make_mock_llm(DomainEnum.KING)
        with patch("cinematic_intelligence.graph.init_chat_model", return_value=mock_llm):
            from cinematic_intelligence.graph import make_cultural_graph

            graph = make_cultural_graph(data_dir=tmp_data_dir)
            result = graph.invoke(
                {"messages": [HumanMessage(content="What is The Shining about?")]}
            )

        assert result["domain"] == DomainEnum.KING
        assert result["final_response"].domain == DomainEnum.KING

    def test_routes_davis_query(self, tmp_data_dir):
        mock_llm = _make_mock_llm(DomainEnum.DAVIS)
        with patch("cinematic_intelligence.graph.init_chat_model", return_value=mock_llm):
            from cinematic_intelligence.graph import make_cultural_graph

            graph = make_cultural_graph(data_dir=tmp_data_dir)
            result = graph.invoke(
                {"messages": [HumanMessage(content="Describe Kind of Blue")]}
            )

        assert result["domain"] == DomainEnum.DAVIS
        assert result["final_response"].domain == DomainEnum.DAVIS

    def test_thread_isolation_with_memory_saver(self, tmp_data_dir):
        """Two different thread_ids should have independent state."""
        mock_llm = _make_mock_llm(DomainEnum.NOLAN)
        checkpointer = MemorySaver()

        with patch("cinematic_intelligence.graph.init_chat_model", return_value=mock_llm):
            from cinematic_intelligence.graph import make_cultural_graph

            graph = make_cultural_graph(checkpointer=checkpointer, data_dir=tmp_data_dir)

            result1 = graph.invoke(
                {"messages": [HumanMessage(content="Tell me about Inception")]},
                config={"configurable": {"thread_id": "thread_a"}},
            )
            result2 = graph.invoke(
                {"messages": [HumanMessage(content="Tell me about Memento")]},
                config={"configurable": {"thread_id": "thread_b"}},
            )

        # Both should succeed independently
        assert result1["final_response"] is not None
        assert result2["final_response"] is not None
