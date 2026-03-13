"""
king_agent.py

Objetivo del script: 
King specialist node: analyzes Stephen King books.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import json
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage

from cinematic_intelligence.data_loader import DataLoader
from cinematic_intelligence.models import KingBookAnalysis
from cinematic_intelligence.state import CulturalState

KING_SYSTEM_PROMPT = """You are an expert literary critic specializing exclusively in Stephen King's bibliography.
You have deep knowledge of King's horror techniques, recurring themes, and literary innovations.

Recurring themes in King's work:
- Small-town New England communities hiding dark secrets
- The supernatural as manifestation of psychological trauma
- Children and adolescents as protagonists with special abilities
- Addiction, alcoholism, and the darkness within ordinary people
- The fragility of the social fabric under extreme pressure

Use the provided book data to ground your analysis in specific details.
Always reference specific novels, characters, settings, or quotes in your responses."""


def build_king_node(llm: BaseChatModel, loader: DataLoader):
    """Factory that returns a LangGraph node for King book analysis."""
    structured_llm = llm.with_structured_output(KingBookAnalysis)

    def king_node(state: CulturalState) -> dict[str, Any]:
        """Analyze King books based on user query."""
        messages = state["messages"]

        relevant_books = loader.search_king(messages[-1].content if messages else "")
        books_context = json.dumps(relevant_books, ensure_ascii=False, indent=2)

        system_with_context = f"""{KING_SYSTEM_PROMPT}

Relevant book data:
{books_context}"""

        try:
            analysis: KingBookAnalysis = structured_llm.invoke(
                [SystemMessage(content=system_with_context), *messages]
            )
            return {
                "domain_result": analysis.model_dump(),
                "messages": [AIMessage(content=analysis.analysis)],
            }
        except Exception:
            fallback_llm = llm
            response = fallback_llm.invoke(
                [SystemMessage(content=system_with_context), *messages]
            )
            fallback = KingBookAnalysis(
                book_title="Multiple Books",
                analysis=response.content,
            )
            return {
                "domain_result": fallback.model_dump(),
                "messages": [AIMessage(content=fallback.analysis)],
            }

    return king_node
