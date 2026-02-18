"""
RAG agentico con grading y hallucination check.

Uso:
    from langchain.scripts.agentic_rag import AgenticRAG
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
import chromadb


class GradeDocument(BaseModel):
    """Evaluacion de relevancia."""
    es_relevante: Literal["si", "no"] = Field(description="Es relevante para la query")


class HallucinationCheck(BaseModel):
    """Evaluacion de alucinacion."""
    esta_fundamentada: Literal["si", "no"] = Field(description="Esta fundamentada en el contexto")
    score: int = Field(description="Score 1-5", ge=1, le=5)


class RAGState(TypedDict):
    query: str
    query_original: str
    documentos: list[dict]
    docs_relevantes: list[dict]
    respuesta: str
    hallucination_check: dict | None
    intentos: int
    intentos_hallucination: int


class AgenticRAG:
    """RAG agentico con grading y hallucination check."""

    def __init__(
        self,
        collection: chromadb.Collection,
        model: str = "gpt-5-mini",
        k: int = 4,
        max_retries: int = 2,
    ):
        self.collection = collection
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.k = k
        self.max_retries = max_retries
        self.grader = self.llm.with_structured_output(GradeDocument)
        self.hallucination_checker = self.llm.with_structured_output(HallucinationCheck)
        self.app = self._build_graph()

    def _retrieve(self, query: str) -> list[dict]:
        """Recupera documentos de ChromaDB."""
        emb = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[emb], n_results=self.k,
            include=["documents", "metadatas", "distances"]
        )
        return [
            {"texto": d, "meta": m, "distancia": dist}
            for d, m, dist in zip(
                results["documents"][0], results["metadatas"][0], results["distances"][0]
            )
        ]

    def _grade(self, query: str, doc: str) -> bool:
        """Evalua relevancia de un documento."""
        result = self.grader.invoke(
            f"Query: {query}\nDocumento: {doc}\n¿Es relevante?"
        )
        return result.es_relevante == "si"  # type: ignore[union-attr]

    def _build_graph(self):
        """Construye el grafo RAG agentico."""

        def retrieve(state: RAGState) -> dict:
            docs = self._retrieve(state["query"])
            return {"documentos": docs}

        def grade(state: RAGState) -> dict:
            relevantes = [
                d for d in state["documentos"]
                if self._grade(state["query"], d["texto"])
            ]
            return {"docs_relevantes": relevantes}

        def decide_gen(state: RAGState) -> str:
            if len(state.get("docs_relevantes", [])) >= 2:
                return "generar"
            if state.get("intentos", 0) >= self.max_retries:
                return "generar"
            return "reescribir"

        def rewrite(state: RAGState) -> dict:
            response = self.llm.invoke([
                SystemMessage(content="Reescribe esta pregunta con diferentes palabras."),
                HumanMessage(content=state["query"]),
            ])
            return {"query": response.content, "intentos": state.get("intentos", 0) + 1}

        def generate(state: RAGState) -> dict:
            docs = state.get("docs_relevantes") or state.get("documentos", [])
            contexto = "\n\n".join([d["texto"] for d in docs[:4]])
            response = self.llm.invoke([
                SystemMessage(content=f"Responde SOLO con el contexto. En español.\n\n{contexto}"),
                HumanMessage(content=state["query_original"]),
            ])
            return {"respuesta": response.content}

        def check_hallucination(state: RAGState) -> dict:
            docs = state.get("docs_relevantes") or state.get("documentos", [])
            contexto = "\n\n".join([d["texto"] for d in docs[:4]])
            check = self.hallucination_checker.invoke(
                f"Contexto:\n{contexto}\n\nRespuesta:\n{state['respuesta']}\n\n¿Fundamentada?"
            )
            return {
                "hallucination_check": check.model_dump(),  # type: ignore[union-attr]
                "intentos_hallucination": state.get("intentos_hallucination", 0) + 1,
            }

        def decide_output(state: RAGState) -> str:
            check = state.get("hallucination_check") or {}
            if check.get("esta_fundamentada") == "si":
                return "output"
            if state.get("intentos_hallucination", 0) >= 2:
                return "output"
            return "regenerar"

        graph = StateGraph(RAGState)
        graph.add_node("retrieve", retrieve)
        graph.add_node("grade", grade)
        graph.add_node("reescribir", rewrite)
        graph.add_node("generar", generate)
        graph.add_node("hallucination_check", check_hallucination)

        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "grade")
        graph.add_conditional_edges("grade", decide_gen, {
            "generar": "generar", "reescribir": "reescribir",
        })
        graph.add_edge("reescribir", "retrieve")
        graph.add_edge("generar", "hallucination_check")
        graph.add_conditional_edges("hallucination_check", decide_output, {
            "output": END, "regenerar": "generar",
        })

        return graph.compile()

    def invoke(self, query: str) -> dict:
        """Ejecuta el RAG agentico."""
        result = self.app.invoke({
            "query": query, "query_original": query,
            "documentos": [], "docs_relevantes": [],
            "respuesta": "", "hallucination_check": None,
            "intentos": 0, "intentos_hallucination": 0,
        })
        return {
            "query": query,
            "respuesta": result["respuesta"],
            "docs_relevantes": len(result.get("docs_relevantes", [])),
            "hallucination_check": result.get("hallucination_check"),
        }
