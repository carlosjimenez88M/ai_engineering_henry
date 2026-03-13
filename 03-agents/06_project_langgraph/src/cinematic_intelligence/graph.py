"""
graph.py

Objetivo del script: 
Main graph factory for the Cultural Intelligence system.

Usage:
    from cinematic_intelligence.graph import make_cultural_graph

    graph = make_cultural_graph()
    result = graph.invoke({"messages": [HumanMessage(content="Tell me about Inception")]})

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph

from cinematic_intelligence.config import settings
from cinematic_intelligence.data_loader import get_loader
from cinematic_intelligence.models import CulturalResponse, DomainEnum
from cinematic_intelligence.nodes.davis_agent import build_davis_node
from cinematic_intelligence.nodes.king_agent import build_king_node
from cinematic_intelligence.nodes.nolan_agent import build_nolan_node
from cinematic_intelligence.nodes.router import build_router_node
from cinematic_intelligence.nodes.synthesizer import build_synthesizer_node
from cinematic_intelligence.routes.domain_route import cultural_route
from cinematic_intelligence.state import CulturalState

GENERAL_FALLBACK_PROMPT = """You are a knowledgeable cultural assistant.
The user's query doesn't clearly match our specialized domains (Nolan films, King books, Davis albums).
Provide a helpful general response, or gently redirect them to one of our areas of expertise."""


def make_cultural_graph(
    checkpointer: BaseCheckpointSaver | None = None,
    data_dir=None,
) -> Any:
    """
    Build and compile the Cultural Intelligence LangGraph.

    Args:
        checkpointer: Optional checkpoint saver for conversation memory.
                      Use MemorySaver() for in-memory, or a DB-backed saver for production.
        data_dir: Optional path to override the default data directory.

    Returns:
        Compiled LangGraph graph ready for .invoke() or .stream()
    """
    llm = init_chat_model(settings.openai_model)
    loader = get_loader(data_dir)

    # Build node functions
    router_node = build_router_node(llm)
    nolan_node = build_nolan_node(llm, loader)
    king_node = build_king_node(llm, loader)
    davis_node = build_davis_node(llm, loader)
    synthesizer_node = build_synthesizer_node(llm)

    def general_fallback_node(state: CulturalState) -> dict:
        """Handle queries outside specialized domains."""
        messages = state["messages"]
        response = llm.invoke(
            [SystemMessage(content=GENERAL_FALLBACK_PROMPT), *messages]
        )
        fallback = CulturalResponse(
            domain=DomainEnum.GENERAL,
            query=messages[0].content if messages else "",
            final_answer=response.content,
        )
        return {
            "final_response": fallback,
            "messages": [AIMessage(content=response.content)],
        }

    # Build graph
    builder = StateGraph(CulturalState)

    # Add nodes
    builder.add_node("router", router_node)
    builder.add_node("nolan_specialist", nolan_node)
    builder.add_node("king_specialist", king_node)
    builder.add_node("davis_specialist", davis_node)
    builder.add_node("synthesizer", synthesizer_node)
    builder.add_node("general_fallback", general_fallback_node)

    # Add edges
    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",
        cultural_route,
        {
            "nolan_specialist": "nolan_specialist",
            "king_specialist": "king_specialist",
            "davis_specialist": "davis_specialist",
            "general_fallback": "general_fallback",
        },
    )
    builder.add_edge("nolan_specialist", "synthesizer")
    builder.add_edge("king_specialist", "synthesizer")
    builder.add_edge("davis_specialist", "synthesizer")
    builder.add_edge("synthesizer", END)
    builder.add_edge("general_fallback", END)

    # Compile
    compile_kwargs: dict[str, Any] = {}
    if checkpointer is not None:
        compile_kwargs["checkpointer"] = checkpointer

    return builder.compile(**compile_kwargs)
