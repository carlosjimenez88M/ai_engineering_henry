"""
Router con especialistas.

Uso:
    from langchain.scripts.routing_agent import RoutingAgent
"""

from __future__ import annotations

from typing import TypedDict, Annotated

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class RouteDecision(BaseModel):
    """Decision de routing."""
    ruta: str = Field(description="Ruta seleccionada")
    confianza: float = Field(description="Nivel de confianza", ge=0.0, le=1.0)


class RouterState(TypedDict):
    messages: Annotated[list, add_messages]
    ruta: str


class RoutingAgent:
    """Agente con routing a especialistas."""

    def __init__(
        self,
        rutas: dict[str, str],
        model: str = "gpt-5-mini",
        router_prompt: str = "Clasifica la query en una ruta.",
    ):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.rutas = rutas  # {nombre_ruta: system_prompt_especialista}
        self.router_prompt = router_prompt
        self.router_llm = self.llm.with_structured_output(RouteDecision)
        self.app = self._build_graph()

    def _build_graph(self):
        """Construye el grafo de routing."""

        def nodo_router(state: RouterState) -> dict:
            rutas_desc = ", ".join(self.rutas.keys())
            query = state["messages"][-1].content
            decision = self.router_llm.invoke([
                SystemMessage(content=f"{self.router_prompt}\nRutas disponibles: {rutas_desc}"),
                HumanMessage(content=query),
            ])
            return {"ruta": decision.ruta}  # type: ignore[union-attr]

        def decidir_ruta(state: RouterState) -> str:
            ruta = state.get("ruta", "")
            if ruta in self.rutas:
                return ruta
            return list(self.rutas.keys())[0]

        graph = StateGraph(RouterState)
        graph.add_node("router", nodo_router)

        edges = {}
        for ruta_name, system_prompt in self.rutas.items():
            def make_node(sp: str):
                def node(state: RouterState) -> dict:
                    query = state["messages"][-1].content
                    response = self.llm.invoke([
                        SystemMessage(content=sp),
                        HumanMessage(content=query),
                    ])
                    return {"messages": [response]}
                return node

            graph.add_node(ruta_name, make_node(system_prompt))
            graph.add_edge(ruta_name, END)
            edges[ruta_name] = ruta_name

        graph.add_edge(START, "router")
        graph.add_conditional_edges("router", decidir_ruta, edges)

        return graph.compile()

    def invoke(self, query: str) -> dict:
        """Ejecuta query con routing."""
        result = self.app.invoke({"messages": [HumanMessage(content=query)]})
        return {
            "ruta": result.get("ruta", "unknown"),
            "respuesta": result["messages"][-1].content,
        }
