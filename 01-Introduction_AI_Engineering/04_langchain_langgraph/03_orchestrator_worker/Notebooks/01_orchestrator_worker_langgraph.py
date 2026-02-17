"""Orchestrator-worker architecture with LangGraph and dynamic worker spawning."""

from __future__ import annotations

import importlib.util
import json
import operator
import os
from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
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


class WorkItem(BaseModel):
    focus: str
    instruction: str


class WorkPlan(BaseModel):
    work_items: list[WorkItem]


class FinalSynthesis(BaseModel):
    opener: str
    follow_up: str
    why_it_works: list[str]


class OrchestratorState(TypedDict):
    context_packet: dict
    tasks: list[dict]
    task: dict
    worker_outputs: Annotated[list[str], operator.add]
    final: dict


def run_orchestrator_worker(profile: dict | None = None, verbose: bool = True) -> dict:
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model, temperature=0.4, api_key=api_key)

    build_context_packet = load_context_builder(root)
    if profile is None:
        profile = {
            "tipo_persona": "fundadora de startup climate-tech",
            "gustos": ["trail running", "cafes de especialidad", "documentales de ciencia", "arte contemporaneo"],
            "estilo": "directa, curiosa, orientada a impacto",
            "contexto": "primera conversacion luego de coincidir en evento tech",
        }
    context_packet = build_context_packet(profile=profile, architecture="orchestrator_worker")

    def orchestrate(state: OrchestratorState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Descompone la tarea en subtareas independientes, una por angulo conversacional.",
                ),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\n"
                    "Devuelve entre 2 y 4 work_items para construir un opener premium.",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(WorkPlan, method="function_calling")
        plan = chain.invoke({"context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2)})
        return {"tasks": [item.model_dump() for item in plan.work_items]}

    def dispatch_workers(state: OrchestratorState) -> list[Send]:
        return [
            Send("worker", {"context_packet": state["context_packet"], "task": task})
            for task in state["tasks"]
        ]

    def worker(state: OrchestratorState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Eres worker especialista: produce solo una contribucion concreta."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\nTask:\n{task}\n\n"
                    "Genera un snippet de maximo 30 palabras.",
                ),
            ]
        )
        chain = prompt | llm
        response = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "task": json.dumps(state["task"], ensure_ascii=False, indent=2),
            }
        )
        return {"worker_outputs": [response.content.strip()]}

    def synthesize(state: OrchestratorState) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Sintetiza aportes de workers en un opener y follow_up final."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\n"
                    "Worker outputs:\n{worker_outputs}",
                ),
            ]
        )
        chain = prompt | llm.with_structured_output(FinalSynthesis, method="function_calling")
        final = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "worker_outputs": json.dumps(state["worker_outputs"], ensure_ascii=False, indent=2),
            }
        )
        return {"final": final.model_dump()}

    graph = StateGraph(OrchestratorState)
    graph.add_node("orchestrate", orchestrate)
    graph.add_node("worker", worker)
    graph.add_node("synthesize", synthesize)

    graph.add_edge(START, "orchestrate")
    graph.add_conditional_edges("orchestrate", dispatch_workers, ["worker"])
    graph.add_edge("worker", "synthesize")
    graph.add_edge("synthesize", END)

    app = graph.compile()
    graph_mermaid = app.get_graph().draw_mermaid()
    result = app.invoke({"context_packet": context_packet, "worker_outputs": []})
    result["__graph_mermaid"] = graph_mermaid
    result["__model"] = model
    result["__context_hash"] = context_packet["context_hash"]
    result["__agent"] = app

    if verbose:
        print("=" * 88)
        print("ARQUITECTURA: Orchestrator-Worker")
        print(f"Modelo: {model}")
        print("Context hash:", context_packet["context_hash"])
        print("\nPlan de tareas:")
        print(json.dumps(result["tasks"], ensure_ascii=False, indent=2))
        print("\nOutputs de workers:")
        print(json.dumps(result["worker_outputs"], ensure_ascii=False, indent=2))
        print("\nSintesis final:")
        print(json.dumps(result["final"], ensure_ascii=False, indent=2))
        print("\n[Autocritica]")
        print("- Orchestrator-worker escala bien cuando el numero de subproblemas es variable.")
        print("- Si el orquestador planifica mal, los workers amplifican esa mala descomposicion.")

    return result


if __name__ == "__main__":
    run_orchestrator_worker()
