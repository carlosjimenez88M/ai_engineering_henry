from __future__ import annotations

from langchain_core.runnables import RunnableLambda

from multi_agent_system.intent_classifier import heuristic_intent_router
from multi_agent_system.memory import InMemoryConversationStore
from multi_agent_system.orchestrator import build_orchestrator
from multi_agent_system.pipeline import MultiAgentService
from multi_agent_system.schemas import IntentClassification, IntentLabel, RoutedResponse


class DummyLLM:
    """Placeholder object, not used when classifier is injected."""



def test_heuristic_classifier_hr() -> None:
    result = heuristic_intent_router("Necesito revisar politica de vacaciones y beneficios")
    assert result.intent == IntentLabel.HR



def test_heuristic_classifier_tech() -> None:
    result = heuristic_intent_router("Como hacer deploy en kubernetes con rollback")
    assert result.intent == IntentLabel.TECH



def test_orchestrator_routes_hr_branch() -> None:
    classifier = RunnableLambda(lambda x: heuristic_intent_router(x["query"]))
    hr_agent = RunnableLambda(
        lambda x: {
            "answer": "HR answer",
            "citations": ["manual_rrhh.md#chunk-1"],
            "confidence": 0.9,
            "follow_up_question": "Quieres la politica completa?",
        }
    )
    tech_agent = RunnableLambda(
        lambda x: {
            "answer": "TECH answer",
            "citations": ["runbook_tech.md#chunk-1"],
            "confidence": 0.9,
            "follow_up_question": "Quieres un ejemplo de implementacion?",
        }
    )

    orchestrator = build_orchestrator(DummyLLM(), hr_agent, tech_agent, classifier=classifier)
    result = orchestrator.invoke({"query": "vacaciones y onboarding"})

    assert result.intent == IntentLabel.HR
    assert result.route_used == "hr_rag_agent"
    assert result.answer == "HR answer"
    assert result.retrieval_hits == 0
    assert result.processing_ms >= 0


def test_orchestrator_falls_back_when_confidence_below_threshold() -> None:
    classifier = RunnableLambda(
        lambda x: IntentClassification(intent=IntentLabel.HR, confidence=0.30, rationale="low confidence")
    )
    hr_agent = RunnableLambda(lambda x: {"answer": "HR answer", "citations": [], "confidence": 0.9, "follow_up_question": "?"})
    tech_agent = RunnableLambda(lambda x: {"answer": "TECH answer", "citations": [], "confidence": 0.9, "follow_up_question": "?"})

    orchestrator = build_orchestrator(
        DummyLLM(),
        hr_agent,
        tech_agent,
        classifier=classifier,
        intent_min_confidence=0.60,
    )
    result = orchestrator.invoke({"query": "vacaciones y onboarding"})
    assert result.route_used == "fallback_unknown"
    assert result.intent == IntentLabel.HR


def test_memory_store_keeps_recent_turns() -> None:
    store = InMemoryConversationStore(max_history_turns=2)
    store.append_user_turn("c1", "hola")
    store.append_user_turn("c1", "segunda")
    store.append_user_turn("c1", "tercera")
    assert store.get_history("c1") == ["segunda", "tercera"]


def test_multi_agent_service_appends_history() -> None:
    pipeline = RunnableLambda(
        lambda x: RoutedResponse(
            intent=IntentLabel.UNKNOWN,
            confidence=0.4,
            rationale="n/a",
            answer="ok",
            citations=[],
            follow_up_question="?",
            route_used="fallback_unknown",
            conversation_id=x["conversation_id"],
            processing_ms=1,
            retrieval_hits=0,
            debug={},
        )
    )
    memory = InMemoryConversationStore(max_history_turns=3)
    service = MultiAgentService(pipeline=pipeline, memory=memory)

    service.ask("consulta uno", conversation_id="thread-1")
    service.ask("consulta dos", conversation_id="thread-1")
    assert memory.get_history("thread-1") == ["consulta uno", "consulta dos"]
