"""ReAct avanzado con LangChain: tools, guardrails y context engineering."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "pyproject.toml").exists():
            return path
    raise RuntimeError("No se encontro la raiz del repositorio")


def load_context_builder(root: Path):
    ctx_path = root / "03_langchain_prompting" / "common" / "context_engineering.py"
    spec = importlib.util.spec_from_file_location("context_engineering03", ctx_path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar modulo: {ctx_path}")
    spec.loader.exec_module(module)
    return module.build_context_packet


def tool_analizar_perfil(context_packet_json: str) -> str:
    context_packet = json.loads(context_packet_json)
    profile = context_packet["profile"]
    gustos = ", ".join(profile.get("gustos", []))
    analysis = {
        "persona": profile.get("tipo_persona", "desconocida"),
        "estilo_preferido": profile.get("estilo", "calido"),
        "insights": [
            f"Intereses detectados: {gustos}",
            "Conviene apertura breve con pregunta autentica.",
        ],
        "context_hash": context_packet.get("context_hash"),
    }
    return json.dumps(analysis, ensure_ascii=False)


def tool_generar_mensaje(analysis_json: str) -> str:
    analysis = json.loads(analysis_json)
    opener = (
        f"Vi que te mueves en {analysis.get('persona', 'tu mundo')}, "
        "que tema te entusiasma tanto que podrias hablar horas sin aburrirte?"
    )
    follow_up = "Si te parece, yo comparto uno y comparamos notas."
    output = {
        "opener": opener,
        "follow_up": follow_up,
        "why_it_works": [
            "Conecta con identidad e intereses.",
            "Mantiene tono curioso y respetuoso.",
        ],
    }
    return json.dumps(output, ensure_ascii=False)


def tool_auditar_respeto(message_json: str) -> str:
    message = json.loads(message_json)
    texto = f"{message.get('opener', '')} {message.get('follow_up', '')}".lower()
    flags = [w for w in ["insiste", "presiona", "explicito"] if w in texto]
    result = {
        "ok": len(flags) == 0,
        "flags": flags,
        "suggestion": "Mantener pregunta abierta y evitar intensidad prematura.",
    }
    return json.dumps(result, ensure_ascii=False)


class AgentStep(BaseModel):
    thought: str
    action: Literal["ANALIZAR_PERFIL", "GENERAR_MENSAJE", "AUDITAR_RESPETO", "FINAL_ANSWER"]
    action_input: str = Field(default="")


class FinalAnswer(BaseModel):
    opener: str
    follow_up: str
    why_it_works: list[str]
    trace_summary: list[str]


def run_react_langchain(profile: dict | None = None, verbose: bool = True) -> dict:
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    build_context_packet = load_context_builder(root)
    llm = ChatOpenAI(model=model, temperature=0.4, api_key=api_key)

    if profile is None:
        profile = {
            "tipo_persona": "arquitecta apasionada por fotografia urbana",
            "gustos": ["cafes tranquilos", "jazz", "viajes cortos", "cafes tranquilos"],
            "estilo": "intelectual pero relajado",
            "contexto": "match reciente, primera interaccion",
        }

    context_packet = build_context_packet(
        profile=profile,
        module="03_langchain_prompting",
        strategy="react_langchain",
    )

    analizar_tool = StructuredTool.from_function(
        func=tool_analizar_perfil,
        name="ANALIZAR_PERFIL",
        description="Extrae insights accionables desde un context packet JSON.",
    )
    mensaje_tool = StructuredTool.from_function(
        func=tool_generar_mensaje,
        name="GENERAR_MENSAJE",
        description="Genera opener y follow_up a partir de analysis JSON.",
    )
    auditar_tool = StructuredTool.from_function(
        func=tool_auditar_respeto,
        name="AUDITAR_RESPETO",
        description="Audita respeto y ausencia de presion.",
    )

    tool_map = {
        "ANALIZAR_PERFIL": analizar_tool,
        "GENERAR_MENSAJE": mensaje_tool,
        "AUDITAR_RESPETO": auditar_tool,
    }

    decision_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un agente ReAct disciplinado. Decide una accion por iteracion y respeta el protocolo canonico.",
            ),
            (
                "human",
                "Estado actual del agente:\n{state_json}\n\n"
                "Acciones validas: ANALIZAR_PERFIL, GENERAR_MENSAJE, AUDITAR_RESPETO, FINAL_ANSWER. "
                "Devuelve thought, action y action_input.",
            ),
        ]
    )
    decision_chain = decision_prompt | llm.with_structured_output(
        AgentStep,
        method="function_calling",
    )

    state = {
        "context_packet": context_packet,
        "analysis": None,
        "draft": None,
        "audit": None,
        "trace": [],
    }

    expected_sequence = ["ANALIZAR_PERFIL", "GENERAR_MENSAJE", "AUDITAR_RESPETO", "FINAL_ANSWER"]

    for idx in range(6):
        step = decision_chain.invoke({"state_json": json.dumps(state, ensure_ascii=False, indent=2)})
        expected_action = expected_sequence[min(idx, len(expected_sequence) - 1)]
        chosen_action = step.action

        if chosen_action != expected_action:
            state["trace"].append(
                {
                    "thought": step.thought,
                    "action": f"override:{chosen_action}->{expected_action}",
                    "observation": "Guardrail aplicado para mantener orden canonico.",
                }
            )
            chosen_action = expected_action

        if chosen_action == "ANALIZAR_PERFIL":
            observation = tool_map[chosen_action].invoke(
                {"context_packet_json": json.dumps(context_packet, ensure_ascii=False)}
            )
            state["analysis"] = json.loads(observation)
        elif chosen_action == "GENERAR_MENSAJE":
            observation = tool_map[chosen_action].invoke(
                {"analysis_json": json.dumps(state["analysis"], ensure_ascii=False)}
            )
            state["draft"] = json.loads(observation)
        elif chosen_action == "AUDITAR_RESPETO":
            observation = tool_map[chosen_action].invoke(
                {"message_json": json.dumps(state["draft"], ensure_ascii=False)}
            )
            state["audit"] = json.loads(observation)
        else:
            state["trace"].append(
                {
                    "thought": step.thought,
                    "action": "FINAL_ANSWER",
                    "observation": "Listo para responder.",
                }
            )
            break

        state["trace"].append(
            {
                "thought": step.thought,
                "action": chosen_action,
                "observation": observation,
            }
        )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Genera la respuesta final usando el estado consolidado del agente."),
            (
                "human",
                "Estado consolidado:\n{state_json}\n\n"
                "Devuelve opener, follow_up, why_it_works y trace_summary.",
            ),
        ]
    )
    final_chain = final_prompt | llm.with_structured_output(
        FinalAnswer,
        method="function_calling",
    )
    final_answer = final_chain.invoke({"state_json": json.dumps(state, ensure_ascii=False, indent=2)})

    flow_mermaid = (
        "graph TD\n"
        "A[State] --> B[Decide Action]\n"
        "B --> C[ANALIZAR_PERFIL]\n"
        "C --> D[GENERAR_MENSAJE]\n"
        "D --> E[AUDITAR_RESPETO]\n"
        "E --> F[FINAL_ANSWER]"
    )

    trace_preview = [
        {
            "action": step["action"],
            "observation_excerpt": str(step["observation"])[:140],
        }
        for step in state["trace"]
    ]
    payload = {
        "__model": model,
        "__context_hash": context_packet["context_hash"],
        "__flow_mermaid": flow_mermaid,
        "context_packet": context_packet,
        "state": state,
        "final_answer": final_answer.model_dump(),
        "trace_preview": trace_preview,
    }

    if verbose:
        print("=" * 80)
        print(f"Modelo: {model}")
        print("Context packet aplicado (context engineering):")
        print(json.dumps(context_packet, ensure_ascii=False, indent=2))

        print("\nFinal answer:")
        print(final_answer.model_dump_json(indent=2))
        print("\nTrace preview:")
        print(json.dumps(trace_preview, ensure_ascii=False, indent=2))

        print("\n[Autocritica]")
        print("- El guardrail de secuencia mejora predictibilidad y reduce deriva del agente.")
        print("- El agente depende de la calidad del context packet (GIGO sigue aplicando).")
        print("- Estas tools son pedagogicas; en produccion hay que endurecer validaciones y timeouts.")

    return payload


if __name__ == "__main__":
    run_react_langchain()
