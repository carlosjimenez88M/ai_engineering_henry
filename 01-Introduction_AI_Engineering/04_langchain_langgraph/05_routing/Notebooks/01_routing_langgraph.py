"""Routing architecture with LangGraph for profile-specific conversational strategy."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "pyproject.toml").exists():
            return path
    raise RuntimeError("No se encontro la raiz del repositorio")


def load_context_builder(root: Path):
    mod_path = root / "04_langchain_langgraph" / "common" / "context_engineering.py"
    spec = importlib.util.spec_from_file_location("ctx04", mod_path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar modulo: {mod_path}")
    spec.loader.exec_module(module)
    return module.build_context_packet


class RouteDecision(BaseModel):
    route: Literal["intelectual", "creativo", "aventura"]
    rationale: str


class FinalMessage(BaseModel):
    opener: str
    follow_up: str
    style_used: str


class RoutingState(TypedDict):
    context_packet: dict
    route: str
    route_rationale: str
    final: dict


def run_routing(profile: dict | None = None, verbose: bool = True) -> dict:
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model, temperature=0.5, api_key=api_key)

    build_context_packet = load_context_builder(root)
    if profile is None:
        profile = {
            "tipo_persona": "neurocientifica especializada en sueno",
            "gustos": ["documentales BBC", "yoga aereo", "cafes silenciosos"],
            "estilo": "curiosa, profunda, humor sutil",
            "contexto": "match tras mencionar un paper",
        }
    context_packet = build_context_packet(profile=profile, architecture="routing")

    def route_profile(state: RoutingState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Elige la mejor estrategia: intelectual, creativo o aventura."),
                ("human", "Context packet:\n{context_packet}"),
            ]
        )
        chain = prompt | llm.with_structured_output(RouteDecision, method="function_calling")
        result = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"route": result.route, "route_rationale": result.rationale}

    def intellectual_node(state: RoutingState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Estrategia intelectual: profundidad, evidencia y curiosidad."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\n"
                    "Genera opener/follow_up con estilo_used='intelectual'.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(FinalMessage, method="function_calling")
        res = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"final": res.model_dump()}

    def creative_node(state: RoutingState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Estrategia creativa: imagenes, referencias culturales y tono ligero."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\n"
                    "Genera opener/follow_up con estilo_used='creativo'.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(FinalMessage, method="function_calling")
        res = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"final": res.model_dump()}

    def adventure_node(state: RoutingState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Estrategia aventura: energia, accion y experiencias de campo."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\n"
                    "Genera opener/follow_up con estilo_used='aventura'.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(FinalMessage, method="function_calling")
        res = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"final": res.model_dump()}

    def route_selector(state: RoutingState) -> Literal["intelectual_node", "creative_node", "adventure_node"]:
        if state["route"] == "intelectual":
            return "intelectual_node"
        if state["route"] == "creativo":
            return "creative_node"
        return "adventure_node"

    graph = StateGraph(RoutingState)
    graph.add_node("route_profile", route_profile)
    graph.add_node("intelectual_node", intellectual_node)
    graph.add_node("creative_node", creative_node)
    graph.add_node("adventure_node", adventure_node)

    graph.add_edge(START, "route_profile")
    graph.add_conditional_edges(
        "route_profile",
        route_selector,
        {
            "intelectual_node": "intelectual_node",
            "creative_node": "creative_node",
            "adventure_node": "adventure_node",
        },
    )
    graph.add_edge("intelectual_node", END)
    graph.add_edge("creative_node", END)
    graph.add_edge("adventure_node", END)

    app = graph.compile()
    graph_mermaid = app.get_graph().draw_mermaid()
    result = app.invoke({"context_packet": context_packet})
    result["__graph_mermaid"] = graph_mermaid
    result["__model"] = model
    result["__context_hash"] = context_packet["context_hash"]
    result["__agent"] = app

    if verbose:
        print("=" * 88)
        print("ARQUITECTURA: Routing")
        print(f"Modelo: {model}")
        print("Context hash:", context_packet["context_hash"])
        print("\nRoute decision:")
        print(json.dumps({"route": result["route"], "rationale": result["route_rationale"]}, ensure_ascii=False, indent=2))
        print("\nFinal output:")
        print(json.dumps(result["final"], ensure_ascii=False, indent=2))
        print("\n[Autocritica]")
        print("- Routing reduce ruido cuando hay subtipos claros de input.")
        print("- Si el router clasifica mal, toda la rama posterior pierde calidad.")

    return result


if __name__ == "__main__":
    run_routing()
