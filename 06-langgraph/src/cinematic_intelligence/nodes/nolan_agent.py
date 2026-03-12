"""Nolan specialist node: analyzes Christopher Nolan films."""

from __future__ import annotations

import json
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage

from cinematic_intelligence.data_loader import DataLoader
from cinematic_intelligence.models import NolanFilmAnalysis
from cinematic_intelligence.state import CulturalState

NOLAN_SYSTEM_PROMPT = """You are an expert film critic specializing exclusively in Christopher Nolan's filmography.
You have deep knowledge of Nolan's narrative techniques, recurring themes, and cinematic innovations.

Recurring themes in Nolan's work:
- Non-linear narrative structures and time manipulation
- Memory, identity, and subjective reality
- The thin line between heroism and moral compromise
- Sacrifice and obsession as drivers of human action

Use the provided film data to ground your analysis in specific details.
Always reference specific films, scenes, quotes, or techniques in your responses."""


def build_nolan_node(llm: BaseChatModel, loader: DataLoader):
    """Factory that returns a LangGraph node for Nolan film analysis."""
    structured_llm = llm.with_structured_output(NolanFilmAnalysis)

    def nolan_node(state: CulturalState) -> dict[str, Any]:
        """Analyze Nolan films based on user query."""
        messages = state["messages"]

        # RAG: keyword search on local data
        relevant_films = loader.search_nolan(messages[-1].content if messages else "")
        films_context = json.dumps(relevant_films, ensure_ascii=False, indent=2)

        system_with_context = f"""{NOLAN_SYSTEM_PROMPT}

Relevant film data:
{films_context}"""

        try:
            analysis: NolanFilmAnalysis = structured_llm.invoke(
                [SystemMessage(content=system_with_context), *messages]
            )
            return {
                "domain_result": analysis.model_dump(),
                "messages": [AIMessage(content=analysis.analysis)],
            }
        except Exception:
            # Fallback: unstructured response
            fallback_llm = llm
            response = fallback_llm.invoke(
                [SystemMessage(content=system_with_context), *messages]
            )
            fallback = NolanFilmAnalysis(
                film_title="Multiple Films",
                analysis=response.content,
            )
            return {
                "domain_result": fallback.model_dump(),
                "messages": [AIMessage(content=fallback.analysis)],
            }

    return nolan_node
