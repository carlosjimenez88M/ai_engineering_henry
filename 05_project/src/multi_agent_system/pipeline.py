"""High-level assembly and service wrapper for multi-agent routing."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from .config import Settings
from .intent_classifier import heuristic_intent_router
from .memory import InMemoryConversationStore
from .orchestrator import build_orchestrator
from .rag_agents import build_hr_rag_agent, build_tech_rag_agent
from .retrievers import build_hr_retriever, build_tech_retriever
from .schemas import RoutedResponse


@dataclass
class MultiAgentService:
    """Facade around orchestrator pipeline with conversation memory."""

    pipeline: object
    memory: InMemoryConversationStore

    def ask(self, query: str, *, conversation_id: str = "default") -> RoutedResponse:
        query = query.strip()
        history = self.memory.get_history(conversation_id)
        result: RoutedResponse = self.pipeline.invoke(
            {
                "query": query,
                "conversation_id": conversation_id,
                "history": history,
            }
        )
        self.memory.append_user_turn(conversation_id, query)
        return result



def build_multi_agent_service(
    settings: Settings,
    *,
    use_heuristic_router: bool = False,
) -> MultiAgentService:
    """Assemble orchestrator + specialized agents + conversation memory.

    Args:
        settings: Environment/model settings.
        use_heuristic_router: Skip LLM intent classification and use keyword heuristic.
    """
    llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0.2)

    hr_retriever = build_hr_retriever(settings.project_root)
    tech_retriever = build_tech_retriever(settings.project_root)

    hr_agent = build_hr_rag_agent(llm, hr_retriever)
    tech_agent = build_tech_rag_agent(llm, tech_retriever)

    classifier = None
    if use_heuristic_router:
        classifier = RunnableLambda(lambda x: heuristic_intent_router(x["query"]))

    orchestrator = build_orchestrator(
        llm,
        hr_agent=hr_agent,
        tech_agent=tech_agent,
        classifier=classifier,
        intent_min_confidence=settings.intent_min_confidence,
    )

    memory = InMemoryConversationStore(max_history_turns=settings.max_history_turns)
    return MultiAgentService(pipeline=orchestrator, memory=memory)



def build_multi_agent_pipeline(settings: Settings):
    """Backwards-compatible builder returning bare pipeline.

    Prefer `build_multi_agent_service` for memory support.
    """
    return build_multi_agent_service(settings).pipeline
