"""
router.py

Objetivo del script: 
Router node: classifies user queries into cultural domains.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage

from cinematic_intelligence.models import DomainRoute
from cinematic_intelligence.state import CulturalState

ROUTER_SYSTEM_PROMPT = """You are a cultural domain classifier for a system that specializes in:
- Christopher Nolan films (movies, cinema, narrative techniques)
- Stephen King books (horror novels, supernatural fiction, adaptations)
- Miles Davis albums (jazz music, musical eras, innovations)

Classify the user's query into exactly one of these domains:
- "nolan": Questions about Christopher Nolan films, cinema, narrative techniques
- "king": Questions about Stephen King books, horror literature, supernatural
- "davis": Questions about Miles Davis albums, jazz music, musical history
- "general": Queries that don't clearly fit any of the above

Be precise and confident in your classification."""


def build_router_node(llm: BaseChatModel):
    """
    Factory that returns a LangGraph node function for domain routing.

    The node uses structured output to classify the user's query domain.
    """
    structured_llm = llm.with_structured_output(DomainRoute)

    def router_node(state: CulturalState) -> dict[str, Any]:
        """Classify the user query into a cultural domain."""
        messages = state["messages"]

        result: DomainRoute = structured_llm.invoke(
            [SystemMessage(content=ROUTER_SYSTEM_PROMPT), *messages]
        )

        return {
            "domain": result.domain,
            "routing_confidence": result.confidence,
            "routing_reasoning": result.reasoning,
        }

    return router_node
