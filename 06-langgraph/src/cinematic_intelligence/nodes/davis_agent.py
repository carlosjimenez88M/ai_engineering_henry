"""
davis_agent.py

Objetivo del script: 
Davis specialist node: analyzes Miles Davis albums.

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
from cinematic_intelligence.models import DavisAlbumAnalysis
from cinematic_intelligence.state import CulturalState

DAVIS_SYSTEM_PROMPT = """You are an expert musicologist specializing exclusively in Miles Davis's discography.
You have deep knowledge of jazz history, musical techniques, and Davis's cultural impact.

Key periods in Davis's work:
- Birth of the Cool era (1949-1950): cool jazz, nonet arrangements
- Hard Bop and First Great Quintet (1955-1959): classic jazz standards
- Modal Jazz (1958-1963): Kind of Blue, Milestones
- Second Great Quintet (1964-1968): post-bop experimentation
- Electric Jazz/Fusion (1969-1975): Bitches Brew, On the Corner
- Return and Contemporary (1981-1991): pop fusion

Use the provided album data to ground your analysis in specific details.
Always reference specific albums, musicians, techniques, or recordings in your responses."""


def build_davis_node(llm: BaseChatModel, loader: DataLoader):
    """Factory that returns a LangGraph node for Davis album analysis."""
    structured_llm = llm.with_structured_output(DavisAlbumAnalysis)

    def davis_node(state: CulturalState) -> dict[str, Any]:
        """Analyze Davis albums based on user query."""
        messages = state["messages"]

        relevant_albums = loader.search_davis(messages[-1].content if messages else "")
        albums_context = json.dumps(relevant_albums, ensure_ascii=False, indent=2)

        system_with_context = f"""{DAVIS_SYSTEM_PROMPT}

Relevant album data:
{albums_context}"""

        try:
            analysis: DavisAlbumAnalysis = structured_llm.invoke(
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
            fallback = DavisAlbumAnalysis(
                album_title="Multiple Albums",
                analysis=response.content,
            )
            return {
                "domain_result": fallback.model_dump(),
                "messages": [AIMessage(content=fallback.analysis)],
            }

    return davis_node
