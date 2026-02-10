"""Agent with feedback loop architecture using LangGraph + tools."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
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


class EvalResult(BaseModel):
    approved: bool
    score: int
    feedback: str


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    context_packet: dict
    feedback_rounds: int
    approved: bool
    evaluator_note: str
    final_response: str


def run_agent_feedback(profile: dict | None = None, verbose: bool = True) -> dict:
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model, temperature=0.4, api_key=api_key)
    evaluator_llm = ChatOpenAI(model=model, temperature=0.1, api_key=api_key)

    build_context_packet = load_context_builder(root)
    if profile is None:
        profile = {
            "tipo_persona": "fundador de startup de robotica educativa",
            "gustos": ["ajedrez", "cafes de especialidad", "senderismo de montana"],
            "estilo": "analitico, curioso, humor sobrio",
            "contexto": "primer mensaje luego de un match mutuo",
        }
    context_packet = build_context_packet(profile=profile, architecture="agent_feedback")

    @tool
    def profile_signal_lookup(gusto: str, context_packet_json: str) -> str:
        """Busca si un gusto existe en el perfil y devuelve una pista de conversacion."""
        packet = json.loads(context_packet_json)
        gustos = [g.lower() for g in packet.get("profile", {}).get("gustos", [])]
        gusto_norm = gusto.strip().lower()
        if gusto_norm in gustos:
            return f"Senal valida: {gusto}. Usa una pregunta abierta conectada a ese gusto."
        return f"Gusto {gusto} no esta en el perfil; evita inventar intereses."

    @tool
    def respect_audit(candidate_message: str) -> str:
        """Audita si el mensaje mantiene respeto y ausencia de presion."""
        text = _normalize(candidate_message)
        blocked = [w for w in ["insiste", "presiona", "explicito"] if re.search(rf"\b{w}\b", text)]
        if blocked:
            return f"audit=fail flags={blocked}"
        return "audit=pass"

    tools = [profile_signal_lookup, respect_audit]
    llm_with_tools = llm.bind_tools(tools)
    tool_node = ToolNode(tools)

    system_prompt = (
        "Eres un agente conversacional aplicado. Objetivo: generar opener y follow_up personalizados, "
        "respetuosos y accionables. Usa tools antes de responder de forma final."
    )

    def agent_node(state: AgentState) -> dict:
        context_blob = json.dumps(state["context_packet"], ensure_ascii=False)
        msgs = [
            SystemMessage(content=system_prompt + f" Context packet JSON: {context_blob}"),
            *state["messages"],
        ]
        response = llm_with_tools.invoke(msgs)
        return {"messages": [response]}

    def route_after_agent(state: AgentState) -> Literal["tools", "evaluate"]:
        last_msg = state["messages"][-1]
        if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
            return "tools"
        return "evaluate"

    def evaluate_node(state: AgentState) -> dict:
        last_msg = state["messages"][-1]
        candidate = last_msg.content if isinstance(last_msg, AIMessage) else str(last_msg)

        eval_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Evalua con severidad: personalizacion, respeto y accionabilidad."),
                (
                    "human",
                    "Context packet:\n{context_packet}\n\nCandidate response:\n{candidate}\n\n"
                    "Devuelve approved(bool), score(0-10), feedback(str).",
                ),
            ]
        )
        chain = eval_prompt | evaluator_llm.with_structured_output(EvalResult, method="function_calling")
        eval_res = chain.invoke(
            {
                "context_packet": json.dumps(state["context_packet"], ensure_ascii=False, indent=2),
                "candidate": candidate,
            }
        )

        approved = bool(eval_res.approved)
        rounds = state.get("feedback_rounds", 0)

        if not approved and rounds < 2:
            feedback_message = HumanMessage(
                content=(
                    "Feedback de calidad: "
                    f"{eval_res.feedback}. Reescribe la respuesta mejorando personalizacion y claridad."
                )
            )
            return {
                "messages": [feedback_message],
                "feedback_rounds": rounds + 1,
                "approved": False,
                "evaluator_note": eval_res.feedback,
                "final_response": candidate,
            }

        return {
            "approved": True,
            "evaluator_note": eval_res.feedback,
            "final_response": candidate,
        }

    def route_after_evaluation(state: AgentState) -> Literal["agent", "end"]:
        if state.get("approved", False):
            return "end"
        return "agent"

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_node("evaluate", evaluate_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", route_after_agent, {"tools": "tools", "evaluate": "evaluate"})
    graph.add_edge("tools", "agent")
    graph.add_conditional_edges("evaluate", route_after_evaluation, {"agent": "agent", "end": END})

    app = graph.compile()
    graph_mermaid = app.get_graph().draw_mermaid()

    user_task = (
        "Crea un opener y un follow_up para este perfil. "
        "Devuelve formato breve: OPENER: ... | FOLLOW_UP: ..."
    )
    result = app.invoke(
        {
            "messages": [HumanMessage(content=user_task)],
            "context_packet": context_packet,
            "feedback_rounds": 0,
            "approved": False,
            "evaluator_note": "",
            "final_response": "",
        }
    )

    payload = {
        "__graph_mermaid": graph_mermaid,
        "__model": model,
        "__context_hash": context_packet["context_hash"],
        "__agent": app,
        "feedback_rounds": result.get("feedback_rounds", 0),
        "evaluator_note": result.get("evaluator_note", ""),
        "final_response": result.get("final_response", ""),
        "approved": result.get("approved", False),
    }

    if verbose:
        print("=" * 88)
        print("ARQUITECTURA: Agent con Feedback")
        print(f"Modelo: {model}")
        print("Context hash:", context_packet["context_hash"])
        print("\nFeedback rounds usados:", result.get("feedback_rounds", 0))
        print("Evaluator note:", result.get("evaluator_note", ""))
        print("\nRespuesta final del agente:")
        print(result.get("final_response", ""))
        print("\n[Autocritica]")
        print("- El loop de feedback sube calidad, pero agrega latencia y costo de evaluacion.")
        print("- Si las tools son debiles, el agente parece sofisticado pero produce poco valor real.")

    return payload


if __name__ == "__main__":
    run_agent_feedback()
