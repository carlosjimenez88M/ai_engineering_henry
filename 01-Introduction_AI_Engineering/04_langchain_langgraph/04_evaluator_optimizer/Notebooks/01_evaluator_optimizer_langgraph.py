"""Evaluator-optimizer architecture with LangGraph quality loop."""

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


class GeneratedDraft(BaseModel):
    opener: str
    follow_up: str


class DraftEvaluation(BaseModel):
    score: int
    decision: Literal["pass", "fail"]
    feedback: str


class FinalPackage(BaseModel):
    opener: str
    follow_up: str
    evaluation_score: int
    why_it_works: list[str]


class EvalOptState(TypedDict):
    context_packet: dict
    draft: dict
    evaluation: dict
    iteration: int
    final: dict


def run_evaluator_optimizer(profile: dict | None = None, verbose: bool = True) -> dict:
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
            "tipo_persona": "arquitecta apasionada por fotografia urbana",
            "gustos": ["cafes tranquilos", "jazz", "viajes cortos"],
            "estilo": "intelectual y relajado",
            "contexto": "primera interaccion tras match reciente",
        }
    context_packet = build_context_packet(profile=profile, architecture="evaluator_optimizer")

    def generate(state: EvalOptState) -> dict:
        feedback = ""
        if state.get("evaluation"):
            feedback = state["evaluation"].get("feedback", "")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Genera opener/follow_up personalizado, natural y respetuoso."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\n"
                    "Feedback previo (si existe): {feedback}\n\n"
                    "Debes mencionar al menos dos gustos exactos del perfil.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(GeneratedDraft, method="function_calling")
        draft = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "feedback": feedback,
            }
        )
        return {"draft": draft.model_dump(), "iteration": state.get("iteration", 0) + 1}

    def evaluate(state: EvalOptState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Evalua con severidad: personalizacion, naturalidad, respeto, accionabilidad.",
                ),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\nDraft:\n{draft}\n\n"
                    "score de 0-10, decision pass/fail y feedback concreto.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(DraftEvaluation, method="function_calling")
        evaluation = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "draft": json.dumps(state["draft"], ensure_ascii=False, indent=2),
            }
        )
        data = evaluation.model_dump()
        if data["score"] >= 8:
            data["decision"] = "pass"
        return {"evaluation": data}

    def decide_next(state: EvalOptState) -> Literal["generate", "finalize"]:
        if state["evaluation"]["decision"] == "pass":
            return "finalize"
        if state.get("iteration", 0) >= 3:
            return "finalize"
        return "generate"

    def finalize(state: EvalOptState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Empaqueta la salida final incorporando score final."),
                (
                    "human",
                    "Draft final:\n{draft}\n\nEvaluation:\n{evaluation}",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(FinalPackage, method="function_calling")
        final = chain.invoke(
            {
                "draft": json.dumps(state["draft"], ensure_ascii=False, indent=2),
                "evaluation": json.dumps(state["evaluation"], ensure_ascii=False, indent=2),
            }
        )
        return {"final": final.model_dump()}

    graph = StateGraph(EvalOptState)
    graph.add_node("generate", generate)
    graph.add_node("evaluate", evaluate)
    graph.add_node("finalize", finalize)

    graph.add_edge(START, "generate")
    graph.add_edge("generate", "evaluate")
    graph.add_conditional_edges("evaluate", decide_next, {"generate": "generate", "finalize": "finalize"})
    graph.add_edge("finalize", END)

    app = graph.compile()
    graph_mermaid = app.get_graph().draw_mermaid()
    result = app.invoke({"context_packet": context_packet, "iteration": 0})
    result["__graph_mermaid"] = graph_mermaid
    result["__model"] = model
    result["__context_hash"] = context_packet["context_hash"]
    result["__agent"] = app

    if verbose:
        print("=" * 88)
        print("ARQUITECTURA: Evaluator-Optimizer")
        print(f"Modelo: {model}")
        print("Context hash:", context_packet["context_hash"])
        print("\nIteration count:", result["iteration"])
        print("\nDraft final evaluado:")
        print(json.dumps(result["draft"], ensure_ascii=False, indent=2))
        print("\nEvaluation:")
        print(json.dumps(result["evaluation"], ensure_ascii=False, indent=2))
        print("\nFinal package:")
        print(json.dumps(result["final"], ensure_ascii=False, indent=2))
        print("\n[Autocritica]")
        print("- Este patron mejora calidad de salida, pero aumenta costo por iteraciones.")
        print("- Si el evaluador no esta bien calibrado, puede forzar loops innecesarios.")

    return result


if __name__ == "__main__":
    run_evaluator_optimizer()
