"""Routing orchestrator that delegates to specialized RAG agents."""

from __future__ import annotations

import time

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable, RunnableBranch, RunnableLambda, RunnableParallel

from .intent_classifier import build_intent_classifier
from .prompts import UNKNOWN_FALLBACK_TEXT
from .schemas import IntentLabel, RoutedResponse



def build_orchestrator(
    llm: BaseChatModel,
    hr_agent: Runnable,
    tech_agent: Runnable,
    classifier: Runnable | None = None,
    *,
    intent_min_confidence: float = 0.60,
):
    """Build conditional routing pipeline.

    classifier can be injected for tests.
    """
    intent_chain = classifier or build_intent_classifier(llm)

    preprocess = RunnableLambda(
        lambda payload: {
            "query": payload["query"].strip(),
            "conversation_id": payload.get("conversation_id", "n/a"),
            "history": payload.get("history", []),
            "_start_ts": time.perf_counter(),
        }
    )

    classify = RunnableParallel(
        payload=RunnableLambda(lambda x: x),
        intent=intent_chain,
    )

    hr_route = RunnableLambda(
        lambda x: {
            "intent": x["intent"],
            "rag": hr_agent.invoke({"query": x["payload"]["query"]}),
            "route_used": "hr_rag_agent",
            "payload": x["payload"],
        }
    )
    tech_route = RunnableLambda(
        lambda x: {
            "intent": x["intent"],
            "rag": tech_agent.invoke({"query": x["payload"]["query"]}),
            "route_used": "tech_rag_agent",
            "payload": x["payload"],
        }
    )
    unknown_route = RunnableLambda(
        lambda x: {
            "intent": x["intent"],
            "route_used": "fallback_unknown",
            "payload": x["payload"],
            "rag": {
                "answer": UNKNOWN_FALLBACK_TEXT,
                "citations": [],
                "confidence": 0.35,
                "follow_up_question": "Puedes detallar si tu consulta es de RRHH o de Tecnologia?",
                "retrieval_hits": 0,
                "evidence_notes": ["No retrieval executed due to low-confidence routing."],
            },
        }
    )

    router = RunnableBranch(
        (
            lambda x: x["intent"].intent == IntentLabel.HR and x["intent"].confidence >= intent_min_confidence,
            hr_route,
        ),
        (
            lambda x: x["intent"].intent == IntentLabel.TECH and x["intent"].confidence >= intent_min_confidence,
            tech_route,
        ),
        unknown_route,
    )

    def envelope(payload: dict) -> RoutedResponse:
        intent = payload["intent"]
        rag = payload["rag"]
        request_payload = payload.get("payload", {})
        processing_ms = int((time.perf_counter() - request_payload.get("_start_ts", time.perf_counter())) * 1000)
        retrieval_hits = (
            rag.get("retrieval_hits", 0) if isinstance(rag, dict) else getattr(rag, "retrieval_hits", 0)
        )
        evidence_notes = (
            rag.get("evidence_notes", []) if isinstance(rag, dict) else getattr(rag, "evidence_notes", [])
        )

        return RoutedResponse(
            intent=intent.intent,
            confidence=intent.confidence,
            rationale=intent.rationale,
            answer=rag["answer"] if isinstance(rag, dict) else rag.answer,
            citations=rag["citations"] if isinstance(rag, dict) else rag.citations,
            follow_up_question=(
                rag["follow_up_question"] if isinstance(rag, dict) else rag.follow_up_question
            ),
            route_used=payload["route_used"],
            conversation_id=request_payload.get("conversation_id", "n/a"),
            processing_ms=max(processing_ms, 0),
            retrieval_hits=max(0, retrieval_hits),
            debug={
                "threshold_used": intent_min_confidence,
                "history_turns": len(request_payload.get("history", [])),
                "evidence_notes": evidence_notes,
            },
        )

    return preprocess | classify | router | RunnableLambda(envelope)
