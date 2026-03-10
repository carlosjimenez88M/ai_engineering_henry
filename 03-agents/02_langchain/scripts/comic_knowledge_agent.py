"""
Agente experto en comics completo con 4 herramientas.

Uso:
    from langchain.scripts.comic_knowledge_agent import ComicKnowledgeAgent
"""

from __future__ import annotations

import json
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
import chromadb


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class ComicKnowledgeAgent:
    """Agente experto en comics Batman y Spider-Man."""

    SYSTEM_PROMPT = (
        "Eres un experto en comics de Batman y Spider-Man. "
        "Usa las herramientas para buscar informacion antes de responder. "
        "Para comparaciones, busca en ambas bases. Responde en español."
    )

    def __init__(
        self,
        batman_collection: chromadb.Collection,
        spiderman_collection: chromadb.Collection,
        model: str = "gpt-5-mini",
    ):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.batman_col = batman_collection
        self.spider_col = spiderman_collection
        self.tools = self._create_tools()
        self.app = self._build_graph()

    def _search_collection(self, collection: chromadb.Collection, query: str, k: int = 3) -> str:
        """Busca en una coleccion de ChromaDB."""
        emb = self.embeddings.embed_query(query)
        results = collection.query(
            query_embeddings=[emb], n_results=k,
            include=["documents", "metadatas"]
        )
        parts = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            parts.append(f"[{meta.get('arco', 'N/A')}]: {doc}")
        return "\n\n".join(parts)

    def _create_tools(self) -> list:
        """Crea las herramientas del agente."""
        batman_col = self.batman_col
        spider_col = self.spider_col
        embeddings = self.embeddings

        @tool
        def buscar_batman(query: str) -> str:
            """Busca informacion sobre Batman en la base de datos de comics.

            Args:
                query: Pregunta o tema sobre Batman.
            """
            emb = embeddings.embed_query(query)
            results = batman_col.query(
                query_embeddings=[emb], n_results=3, include=["documents", "metadatas"]
            )
            return "\n\n".join([
                f"[{m.get('arco', '')}]: {d}"
                for d, m in zip(results["documents"][0], results["metadatas"][0])
            ])

        @tool
        def buscar_spiderman(query: str) -> str:
            """Busca informacion sobre Spider-Man en la base de datos de comics.

            Args:
                query: Pregunta o tema sobre Spider-Man.
            """
            emb = embeddings.embed_query(query)
            results = spider_col.query(
                query_embeddings=[emb], n_results=3, include=["documents", "metadatas"]
            )
            return "\n\n".join([
                f"[{m.get('arco', '')}]: {d}"
                for d, m in zip(results["documents"][0], results["metadatas"][0])
            ])

        @tool
        def comparar_heroes(aspecto: str) -> str:
            """Compara Batman y Spider-Man buscando en ambas bases de datos.

            Args:
                aspecto: Aspecto a comparar.
            """
            emb = embeddings.embed_query(aspecto)
            b_results = batman_col.query(query_embeddings=[emb], n_results=2, include=["documents"])
            s_results = spider_col.query(query_embeddings=[emb], n_results=2, include=["documents"])
            return (
                "BATMAN:\n" + "\n".join(b_results["documents"][0])
                + "\n\nSPIDER-MAN:\n" + "\n".join(s_results["documents"][0])
            )

        @tool
        def estadisticas_personaje(personaje: str) -> str:
            """Retorna estadisticas de poder de un personaje.

            Args:
                personaje: batman o spiderman.
            """
            stats = {
                "batman": {"fuerza": 35, "inteligencia": 95, "tecnologia": 90, "combate": 85, "total": 76},
                "spiderman": {"fuerza": 70, "inteligencia": 85, "agilidad": 95, "sentido": 90, "total": 85},
            }
            s = stats.get(personaje.lower())
            return json.dumps(s, indent=2) if s else f"Sin datos para {personaje}"

        return [buscar_batman, buscar_spiderman, comparar_heroes, estadisticas_personaje]

    def _build_graph(self):
        """Construye el grafo del agente."""
        llm_with_tools = self.llm.bind_tools(self.tools)

        def call_model(state: AgentState) -> dict:
            messages = [SystemMessage(content=self.SYSTEM_PROMPT)] + state["messages"]
            return {"messages": [llm_with_tools.invoke(messages)]}

        def should_continue(state: AgentState) -> str:
            last = state["messages"][-1]
            if hasattr(last, "tool_calls") and last.tool_calls:
                return "tools"
            return END

        graph = StateGraph(AgentState)
        graph.add_node("agent", call_model)
        graph.add_node("tools", ToolNode(self.tools))

        graph.add_edge(START, "agent")
        graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
        graph.add_edge("tools", "agent")

        return graph.compile()

    def invoke(self, query: str) -> str:
        """Ejecuta una query."""
        result = self.app.invoke({"messages": [HumanMessage(content=query)]})
        last = result["messages"][-1]
        return last.content if hasattr(last, "content") else str(last)
