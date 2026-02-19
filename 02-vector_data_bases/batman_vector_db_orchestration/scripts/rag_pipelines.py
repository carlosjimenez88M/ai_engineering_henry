"""Vanilla RAG and Agentic RAG pipelines for educational notebooks."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .common import generate_answer, tokenize
from .vector_store_lab import ComicsVectorDB


@dataclass
class RAGResult:
    query: str
    answer: str
    docs: list[dict[str, Any]]
    latency_seconds: float
    llm_provider: str
    retrieval_provider: str
    pipeline: str
    route: str = "n/a"
    rewritten_query: str = ""
    groundedness: float = 0.0
    steps: list[str] = field(default_factory=list)


def _groundedness(answer: str, docs: list[dict[str, Any]]) -> float:
    answer_tokens = set(tokenize(answer))
    if not answer_tokens:
        return 0.0

    context_tokens: set[str] = set()
    for doc in docs:
        context_tokens.update(tokenize(str(doc.get("text", ""))))

    overlap = len(answer_tokens & context_tokens)
    return round(overlap / max(len(answer_tokens), 1), 4)


def _context_from_docs(docs: list[dict[str, Any]]) -> list[str]:
    return [str(doc.get("text", "")) for doc in docs]


def _route_query_heuristic(query: str) -> str:
    q = query.lower()
    chronology_terms = {"orden", "cronologia", "timeline", "primero", "despues", "evolucion"}
    villain_terms = {"joker", "bane", "hush", "villano", "enemigo", "owls", "tribunal"}
    strategy_terms = {"estrategia", "plan", "contingencia", "tactica", "liga", "justicia"}

    if any(term in q for term in chronology_terms):
        return "chronology"
    if any(term in q for term in villain_terms):
        return "villains"
    if any(term in q for term in strategy_terms):
        return "strategy"
    return "lore"


def _rewrite_query(query: str, route: str) -> str:
    if route == "chronology":
        return f"{query}. Enfocate en orden temporal y eventos clave."
    if route == "villains":
        return f"{query}. Prioriza motivaciones, metodos y conflicto heroe-villano."
    if route == "strategy":
        return f"{query}. Prioriza decisiones tacticas, trade-offs y consecuencias."
    return f"{query}. Prioriza hechos canonicos y contexto narrativo."


def _filter_relevant_docs(query: str, docs: list[dict[str, Any]], min_overlap: int = 2) -> list[dict[str, Any]]:
    query_tokens = set(tokenize(query))
    filtered: list[dict[str, Any]] = []
    for doc in docs:
        text = str(doc.get("text", ""))
        overlap = len(query_tokens & set(tokenize(text)))
        if overlap >= min_overlap:
            filtered.append(doc)
    return filtered


class VanillaRAG:
    """Single-step retrieve + generate pipeline."""

    def __init__(
        self,
        vector_db: ComicsVectorDB,
        model: str = "gpt-5-mini",
        embedding_model: str = "text-embedding-3-small",
        k: int = 4,
    ) -> None:
        self.vector_db = vector_db
        self.model = model
        self.embedding_model = embedding_model
        self.k = k

    def run(self, query: str) -> RAGResult:
        start = time.perf_counter()
        docs, retrieval_provider = self.vector_db.query(
            query_text=query,
            n_results=self.k,
            embedding_model=self.embedding_model,
        )
        contexts = _context_from_docs(docs)
        answer, llm_provider = generate_answer(
            query=query,
            contexts=contexts,
            model=self.model,
            system_prompt=(
                "Eres un profesor senior de AI Engineering. "
                "Responde con rigor tecnico, usando solo el contexto entregado. "
                "Incluye citas [D#] cuando uses evidencia concreta."
            ),
        )

        groundedness = _groundedness(answer=answer, docs=docs)
        latency = round(time.perf_counter() - start, 4)
        return RAGResult(
            query=query,
            answer=answer,
            docs=docs,
            latency_seconds=latency,
            llm_provider=llm_provider,
            retrieval_provider=retrieval_provider,
            pipeline="vanilla_rag",
            groundedness=groundedness,
            steps=["retrieve", "generate"],
        )


class AgenticRAG:
    """RAG with routing, relevance filtering, and grounding self-check."""

    def __init__(
        self,
        vector_db: ComicsVectorDB,
        model: str = "gpt-5-mini",
        embedding_model: str = "text-embedding-3-small",
        k: int = 6,
        min_docs_after_filter: int = 3,
    ) -> None:
        self.vector_db = vector_db
        self.model = model
        self.embedding_model = embedding_model
        self.k = k
        self.min_docs_after_filter = min_docs_after_filter

    def run(self, query: str) -> RAGResult:
        start = time.perf_counter()
        steps: list[str] = []

        route = _route_query_heuristic(query)
        rewritten_query = _rewrite_query(query=query, route=route)
        steps.extend(["route", "rewrite_query"])

        docs, retrieval_provider = self.vector_db.query(
            query_text=rewritten_query,
            n_results=self.k,
            embedding_model=self.embedding_model,
        )
        steps.append("retrieve")

        filtered_docs = _filter_relevant_docs(query=rewritten_query, docs=docs)
        if len(filtered_docs) < self.min_docs_after_filter:
            fallback_docs, fallback_provider = self.vector_db.query(
                query_text=query,
                n_results=self.k,
                embedding_model=self.embedding_model,
            )
            docs = fallback_docs
            retrieval_provider = fallback_provider
            filtered_docs = _filter_relevant_docs(query=query, docs=fallback_docs, min_overlap=1)
            steps.append("retrieve_fallback")

        docs_for_generation = filtered_docs if filtered_docs else docs
        contexts = _context_from_docs(docs_for_generation)

        answer, llm_provider = generate_answer(
            query=query,
            contexts=contexts,
            model=self.model,
            system_prompt=(
                "Eres un profesor de MIT especializado en AI Engineering aplicado. "
                "Explica con precision, separa hechos de inferencias y da recomendaciones practicas. "
                "Usa solo el contexto disponible y agrega citas [D#]."
            ),
        )
        steps.append("generate")

        groundedness = _groundedness(answer=answer, docs=docs_for_generation)
        if groundedness < 0.18:
            answer, llm_provider = generate_answer(
                query=(
                    query
                    + "\n\nReintento: responde de forma mas corta, con afirmaciones estrictamente "
                    "sustentadas por los documentos y citas [D#]."
                ),
                contexts=contexts,
                model=self.model,
                system_prompt=(
                    "Modo estricto de verificabilidad. No inventes datos. "
                    "Si no hay evidencia suficiente, dilo explicitamente."
                ),
            )
            groundedness = _groundedness(answer=answer, docs=docs_for_generation)
            steps.append("regenerate_if_low_grounding")

        latency = round(time.perf_counter() - start, 4)
        return RAGResult(
            query=query,
            answer=answer,
            docs=docs_for_generation,
            latency_seconds=latency,
            llm_provider=llm_provider,
            retrieval_provider=retrieval_provider,
            pipeline="agentic_rag",
            route=route,
            rewritten_query=rewritten_query,
            groundedness=groundedness,
            steps=steps,
        )


class HeroRouterOrchestrator:
    """Simple orchestration layer that routes between hero-specific RAG pipelines."""

    def __init__(
        self,
        hero_pipelines: dict[str, AgenticRAG],
        default_hero: str = "batman",
    ) -> None:
        if default_hero not in hero_pipelines:
            raise ValueError(f"default_hero='{default_hero}' not present in hero_pipelines")
        self.hero_pipelines = hero_pipelines
        self.default_hero = default_hero

    def route(self, query: str) -> str:
        q = query.lower()
        if "spider" in q or "peter" in q or "venom" in q:
            if "spiderman" in self.hero_pipelines:
                return "spiderman"
        if "batman" in q or "gotham" in q or "joker" in q or "wayne" in q:
            if "batman" in self.hero_pipelines:
                return "batman"
        return self.default_hero

    def run(self, query: str) -> dict[str, Any]:
        hero = self.route(query)
        result = self.hero_pipelines[hero].run(query)
        return {
            "selected_hero": hero,
            "query": query,
            "answer": result.answer,
            "route": result.route,
            "pipeline": result.pipeline,
            "latency_seconds": result.latency_seconds,
            "groundedness": result.groundedness,
            "steps": result.steps,
        }
