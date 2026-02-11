"""Specialized RAG agents for each domain."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableLambda

from .prompts import HR_AGENT_PROMPT, TECH_AGENT_PROMPT
from .schemas import RAGAnswer



def _format_docs_with_sources(docs) -> tuple[str, list[str]]:
    lines = []
    citations = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown_source")
        chunk_id = doc.metadata.get("chunk_id", "n/a")
        score = doc.metadata.get("keyword_score", "n/a")
        tag = f"{source}#chunk-{chunk_id}"
        citations.append(tag)
        lines.append(f"[{tag}] (score={score}) {doc.page_content}")
    return "\n\n".join(lines), citations



def _build_domain_rag_agent(
    llm: BaseChatModel,
    retriever: BaseRetriever,
    system_prompt: str,
    domain: str,
):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                "Domain: {domain}\n"
                "User query: {query}\n\n"
                "Retrieved context:\n{context}\n\n"
                "Answer using only retrieved evidence.",
            ),
        ]
    )

    def enrich(payload: dict) -> dict:
        query = payload["query"]
        docs = retriever.invoke(query)
        context, citations = _format_docs_with_sources(docs)
        return {
            "query": query,
            "domain": domain,
            "context": context,
            "citations_seed": citations,
            "retrieval_hits": len(docs),
        }

    def merge_citations(result: RAGAnswer, payload: dict) -> RAGAnswer:
        merged = list(dict.fromkeys([*result.citations, *payload["citations_seed"]]))
        result.citations = merged
        result.retrieval_hits = max(result.retrieval_hits, payload["retrieval_hits"])
        if not result.evidence_notes:
            result.evidence_notes = [f"{payload['retrieval_hits']} context chunks retrieved for {domain}"]
        return result

    return (
        RunnableLambda(enrich)
        | {
            "payload": RunnableLambda(lambda x: x),
            "result": prompt | llm.with_structured_output(RAGAnswer, method="function_calling"),
        }
        | RunnableLambda(lambda x: merge_citations(x["result"], x["payload"]))
    )


def _build_local_rag_agent(retriever: BaseRetriever, domain: str):
    """Fallback RAG without LLM dependency (useful for local demos/tests)."""

    def answer(payload: dict) -> RAGAnswer:
        query = payload["query"]
        docs = retriever.invoke(query)
        _, citations = _format_docs_with_sources(docs)

        if docs:
            top_snippets = [doc.page_content.strip().split("\n")[0] for doc in docs[:2]]
            answer_text = (
                f"[Modo local sin LLM] Hallazgos de {domain}: " + " | ".join(top_snippets)
            )
            follow_up = "Quieres que lo convierta en un checklist accionable?"
            confidence = 0.62
            evidence_notes = [f"{len(docs)} context chunks retrieved for {domain} (local mode)."]
        else:
            answer_text = (
                f"[Modo local sin LLM] No encontre evidencia suficiente en {domain} para esta consulta."
            )
            follow_up = "Puedes agregar mas detalles o palabras clave?"
            confidence = 0.35
            evidence_notes = [f"0 context chunks retrieved for {domain} (local mode)."]

        return RAGAnswer(
            answer=answer_text,
            citations=citations,
            confidence=confidence,
            follow_up_question=follow_up,
            retrieval_hits=len(docs),
            evidence_notes=evidence_notes,
        )

    return RunnableLambda(answer)



def build_hr_rag_agent(llm: BaseChatModel, retriever: BaseRetriever):
    return _build_domain_rag_agent(llm, retriever, HR_AGENT_PROMPT, domain="HR")



def build_tech_rag_agent(llm: BaseChatModel, retriever: BaseRetriever):
    return _build_domain_rag_agent(llm, retriever, TECH_AGENT_PROMPT, domain="TECH")


def build_hr_local_rag_agent(retriever: BaseRetriever):
    return _build_local_rag_agent(retriever, domain="HR")


def build_tech_local_rag_agent(retriever: BaseRetriever):
    return _build_local_rag_agent(retriever, domain="TECH")
