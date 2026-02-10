"""Prompt chaining architecture with LangGraph for conversation coaching."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import unicodedata
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


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def score_personalization(text: str, gustos: list[str]) -> int:
    norm_text = _normalize(text)
    hits = 0
    for gusto in gustos:
        tokens = [t for t in _normalize(gusto).split() if len(t) > 2]
        if not tokens:
            continue
        match_hits = sum(1 for token in tokens if token in norm_text)
        if match_hits >= max(1, len(tokens) // 2):
            hits += 1
    return hits


class SignalSummary(BaseModel):
    key_signals: list[str]
    risks: list[str]


class DraftMessage(BaseModel):
    opener: str
    follow_up: str


class FinalMessage(BaseModel):
    opener: str
    follow_up: str
    why_it_works: list[str]


class ChainState(TypedDict):
    context_packet: dict
    signal_summary: dict
    draft: dict
    improved: dict
    final: dict


def run_prompt_chaining(profile: dict | None = None, verbose: bool = True) -> dict:
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
            "tipo_persona": "productora musical de jazz contemporaneo",
            "gustos": ["vinilos de Coltrane", "cocina japonesa izakaya", "fotografia analogica"],
            "estilo": "creativa, espontanea, valora referencias culturales",
            "contexto": "conversacion retomada tras 3 dias",
        }
    context_packet = build_context_packet(profile=profile, architecture="prompt_chaining")

    def analyze_signals(state: ChainState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Extrae senales accionables y riesgos conversacionales sin inventar datos.",
                ),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\nDevuelve key_signals y risks.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(SignalSummary, method="function_calling")
        result = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"signal_summary": result.model_dump()}

    def generate_draft(state: ChainState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Genera opener/follow_up personalizando con al menos 2 gustos exactos."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\nSignal summary:\n{summary}",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(DraftMessage, method="function_calling")
        result = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "summary": json.dumps(state["signal_summary"], ensure_ascii=False, indent=2),
            }
        )
        return {"draft": result.model_dump()}

    def improve_draft(state: ChainState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Refina el mensaje para subir personalizacion y mantener tono respetuoso.",
                ),
                (
                    "human",
                    "Draft actual:\n{draft}\n\nDebes mencionar al menos dos gustos de: {gustos}.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(DraftMessage, method="function_calling")
        result = chain.invoke(
            {
                "draft": json.dumps(state["draft"], ensure_ascii=False, indent=2),
                "gustos": ", ".join(state["context_packet"]["profile"]["gustos"]),
            }
        )
        return {"improved": result.model_dump()}

    def finalize(state: ChainState) -> dict:
        selected = state.get("improved") or state.get("draft")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Empaqueta la salida final y explica por que funciona."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\nMensaje elegido:\n{selected}",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(FinalMessage, method="function_calling")
        result = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "selected": json.dumps(selected, ensure_ascii=False, indent=2),
            }
        )
        return {"final": result.model_dump()}

    def quality_gate(state: ChainState) -> Literal["improve", "finalize"]:
        draft = state["draft"]
        gustos = state["context_packet"]["profile"]["gustos"]
        text = f"{draft['opener']} {draft['follow_up']}"
        personalization_hits = score_personalization(text, gustos)
        if personalization_hits >= 2 and "?" in text:
            return "finalize"
        return "improve"

    graph = StateGraph(ChainState)
    graph.add_node("analyze_node", analyze_signals)
    graph.add_node("draft_node", generate_draft)
    graph.add_node("improve_node", improve_draft)
    graph.add_node("finalize_node", finalize)

    graph.add_edge(START, "analyze_node")
    graph.add_edge("analyze_node", "draft_node")
    graph.add_conditional_edges("draft_node", quality_gate, {"improve": "improve_node", "finalize": "finalize_node"})
    graph.add_edge("improve_node", "finalize_node")
    graph.add_edge("finalize_node", END)

    app = graph.compile()
    graph_mermaid = app.get_graph().draw_mermaid()
    result = app.invoke({"context_packet": context_packet})
    result["__graph_mermaid"] = graph_mermaid
    result["__model"] = model
    result["__context_hash"] = context_packet["context_hash"]
    result["__agent"] = app

    if verbose:
        print("=" * 88)
        print("ARQUITECTURA: Prompt Chaining")
        print(f"Modelo: {model}")
        print("Context hash:", context_packet["context_hash"])
        print("\nSignal summary:")
        print(json.dumps(result["signal_summary"], ensure_ascii=False, indent=2))
        print("\nDraft:")
        print(json.dumps(result["draft"], ensure_ascii=False, indent=2))
        if result.get("improved"):
            print("\nImproved draft:")
            print(json.dumps(result["improved"], ensure_ascii=False, indent=2))
        print("\nFinal:")
        print(json.dumps(result["final"], ensure_ascii=False, indent=2))
        print("\n[Autocritica]")
        print("- La cadena secuencial mejora control, pero agrega latencia por nodos seriales.")
        print("- Si el quality gate es debil, se puede promover mensaje mediocre a final.")

    return result


if __name__ == "__main__":
    run_prompt_chaining()
