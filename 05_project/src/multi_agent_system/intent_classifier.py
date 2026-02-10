"""Intent classifier chain for the orchestrator agent."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from .prompts import ORCHESTRATOR_INTENT_PROMPT
from .schemas import IntentClassification, IntentLabel



def build_intent_classifier(llm: BaseChatModel):
    """Build a structured classifier chain.

    Returns a runnable that expects: {"query": "..."}
    and outputs IntentClassification.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", ORCHESTRATOR_INTENT_PROMPT),
            (
                "human",
                "Recent conversation history:\n{history}\n\n"
                "Current user query:\n{query}\n\n"
                "Classify intent now.",
            ),
        ]
    )

    def preprocess(payload: dict) -> dict:
        history_lines = payload.get("history", [])
        if not history_lines:
            history = "N/A"
        else:
            history = "\n".join(f"- {line}" for line in history_lines)
        return {"query": payload["query"].strip(), "history": history}

    def normalize(result: IntentClassification) -> IntentClassification:
        conf = max(0.0, min(1.0, float(result.confidence)))
        result.confidence = conf
        result.rationale = result.rationale.strip()
        return result

    return (
        RunnableLambda(preprocess)
        | prompt
        | llm.with_structured_output(IntentClassification, method="function_calling")
        | RunnableLambda(normalize)
    )



def heuristic_intent_router(query: str) -> IntentClassification:
    """Cheap heuristic fallback for tests/local development."""
    text = query.lower()

    hr_terms = ["vacaciones", "beneficios", "onboarding", "rrhh", "desempeno", "reclutamiento"]
    tech_terms = ["kubernetes", "api", "deploy", "ci/cd", "microserv", "seguridad", "debug"]

    hr_hits = sum(1 for term in hr_terms if term in text)
    tech_hits = sum(1 for term in tech_terms if term in text)

    if hr_hits > tech_hits and hr_hits > 0:
        return IntentClassification(intent=IntentLabel.HR, confidence=0.75, rationale="Matched HR keywords")
    if tech_hits > hr_hits and tech_hits > 0:
        return IntentClassification(intent=IntentLabel.TECH, confidence=0.78, rationale="Matched TECH keywords")

    return IntentClassification(intent=IntentLabel.UNKNOWN, confidence=0.45, rationale="Ambiguous or weak evidence")
