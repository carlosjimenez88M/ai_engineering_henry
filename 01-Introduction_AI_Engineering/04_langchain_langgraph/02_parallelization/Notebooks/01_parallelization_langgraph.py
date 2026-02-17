"""Parallelization architecture with LangGraph for message composition."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import TypedDict

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


class OpenerCandidate(BaseModel):
    opener: str


class FollowUpCandidate(BaseModel):
    follow_up: str


class ToneGuardrails(BaseModel):
    tone_notes: list[str]
    avoid: list[str]


class FinalMessage(BaseModel):
    opener: str
    follow_up: str
    tone_notes: list[str]
    avoid: list[str]
    why_it_works: list[str]


class ParallelState(TypedDict):
    context_packet: dict
    opener_candidate: dict
    follow_up_candidate: dict
    tone_guardrails: dict
    final: dict


def run_parallelization(profile: dict | None = None, verbose: bool = True) -> dict:
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model, temperature=0.6, api_key=api_key)

    build_context_packet = load_context_builder(root)
    if profile is None:
        profile = {
            "tipo_persona": "cirujana cardiovascular con pasion por ballet clasico",
            "gustos": ["teatro de camara", "vinos biodinamicos", "alpinismo de altura"],
            "estilo": "precisa, elegante, conversacion intelectual",
            "contexto": "match con perfil verificado, ella dio like primero",
        }
    context_packet = build_context_packet(profile=profile, architecture="parallelization")

    def build_opener(state: ParallelState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Genera un opener elegante con referencia explicita a gustos del perfil."),
                ("human", "Context packet:\n{context_packet}"),
            ]
        )
        chain = prompt | llm.with_structured_output(OpenerCandidate, method="function_calling")
        result = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"opener_candidate": result.model_dump()}

    def build_follow_up(state: ParallelState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Genera una pregunta de seguimiento accionable y respetuosa."),
                ("human", "Context packet:\n{context_packet}"),
            ]
        )
        chain = prompt | llm.with_structured_output(FollowUpCandidate, method="function_calling")
        result = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"follow_up_candidate": result.model_dump()}

    def build_tone_guardrails(state: ParallelState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Define tono y anti-patrones para mantener respeto y naturalidad."),
                ("human", "Context packet:\n{context_packet}"),
            ]
        )
        chain = prompt | llm.with_structured_output(ToneGuardrails, method="function_calling")
        result = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"tone_guardrails": result.model_dump()}

    def aggregate(state: ParallelState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Fusiona componentes paralelos en una salida final coherente."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\n"
                    "Opener:\n{opener}\n\n"
                    "Follow up:\n{follow_up}\n\n"
                    "Tone/avoid:\n{tone}",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(FinalMessage, method="function_calling")
        result = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "opener": json.dumps(state["opener_candidate"], ensure_ascii=False, indent=2),
                "follow_up": json.dumps(state["follow_up_candidate"], ensure_ascii=False, indent=2),
                "tone": json.dumps(state["tone_guardrails"], ensure_ascii=False, indent=2),
            }
        )
        return {"final": result.model_dump()}

    graph = StateGraph(ParallelState)
    graph.add_node("build_opener", build_opener)
    graph.add_node("build_follow_up", build_follow_up)
    graph.add_node("build_tone", build_tone_guardrails)
    graph.add_node("aggregate", aggregate)

    graph.add_edge(START, "build_opener")
    graph.add_edge(START, "build_follow_up")
    graph.add_edge(START, "build_tone")
    graph.add_edge("build_opener", "aggregate")
    graph.add_edge("build_follow_up", "aggregate")
    graph.add_edge("build_tone", "aggregate")
    graph.add_edge("aggregate", END)

    app = graph.compile()
    graph_mermaid = app.get_graph().draw_mermaid()
    result = app.invoke({"context_packet": context_packet})
    result["__graph_mermaid"] = graph_mermaid
    result["__model"] = model
    result["__context_hash"] = context_packet["context_hash"]
    result["__agent"] = app

    if verbose:
        print("=" * 88)
        print("ARQUITECTURA: Parallelization")
        print(f"Modelo: {model}")
        print("Context hash:", context_packet["context_hash"])
        print("\nOpener branch:")
        print(json.dumps(result["opener_candidate"], ensure_ascii=False, indent=2))
        print("\nFollow-up branch:")
        print(json.dumps(result["follow_up_candidate"], ensure_ascii=False, indent=2))
        print("\nTone branch:")
        print(json.dumps(result["tone_guardrails"], ensure_ascii=False, indent=2))
        print("\nFinal aggregated output:")
        print(json.dumps(result["final"], ensure_ascii=False, indent=2))
        print("\n[Autocritica]")
        print("- Paralelizar reduce tiempo total cuando ramas son independientes.")
        print("- El costo de tokens puede subir por duplicacion de contexto en cada rama.")

    return result


if __name__ == "__main__":
    run_parallelization()
