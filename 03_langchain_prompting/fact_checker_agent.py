"""Agente Fact-Checker con LangChain + Tavily: busca y verifica informacion en internet."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from tavily import TavilyClient


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "pyproject.toml").exists():
            return path
    raise RuntimeError("No se encontro la raiz del repositorio")


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def tool_buscar_informacion(query: str, *, tavily: TavilyClient) -> str:
    """Busca informacion en internet usando Tavily y devuelve resultados."""
    response = tavily.search(query=query, max_results=5, search_depth="basic")
    resultados = []
    for r in response.get("results", []):
        resultados.append({
            "titulo": r.get("title", ""),
            "url": r.get("url", ""),
            "contenido": r.get("content", "")[:300],
        })
    return json.dumps({"query": query, "resultados": resultados}, ensure_ascii=False)


def tool_extraer_afirmaciones(texto: str) -> str:
    """Extrae afirmaciones verificables de un texto."""
    oraciones = [s.strip() for s in texto.replace("\n", ". ").split(".") if len(s.strip()) > 15]
    afirmaciones = oraciones[:5]
    return json.dumps({"afirmaciones": afirmaciones}, ensure_ascii=False)


def tool_generar_veredicto(afirmacion: str, evidencia_json: str) -> str:
    """Compara una afirmacion contra la evidencia encontrada y da un veredicto basico."""
    evidencia = json.loads(evidencia_json)
    resultados = evidencia.get("resultados", [])
    hay_evidencia = len(resultados) > 0
    return json.dumps({
        "afirmacion": afirmacion,
        "fuentes_encontradas": len(resultados),
        "evidencia_disponible": hay_evidencia,
        "urls": [r["url"] for r in resultados[:3]],
    }, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Structured output models
# ---------------------------------------------------------------------------

class AgentStep(BaseModel):
    thought: str
    action: Literal[
        "EXTRAER_AFIRMACIONES",
        "BUSCAR_INFORMACION",
        "GENERAR_VEREDICTO",
        "FINAL_ANSWER",
    ]
    action_input: str = Field(default="")


class AfirmacionVerificada(BaseModel):
    afirmacion: str
    veredicto: str = Field(description="verdadero, falso o parcialmente verdadero")


class VerificacionFinal(BaseModel):
    tema: str
    resumen: str
    afirmaciones_verificadas: list[AfirmacionVerificada]
    conclusion: str
    fuentes: list[str]


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run_fact_checker(
    afirmacion: str = "Python es el lenguaje de programacion mas usado en inteligencia artificial en 2025, busca referencias en ingles!",
    verbose: bool = True,
) -> dict:
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    tavily_key = os.getenv("TVLY_API_KEY")
    if not tavily_key:
        raise RuntimeError("TVLY_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    llm = ChatOpenAI(model=model, temperature=0.3, api_key=api_key)
    tavily = TavilyClient(api_key=tavily_key)

    # Decision prompt
    decision_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un agente fact-checker. Tu flujo es: "
                "EXTRAER_AFIRMACIONES -> BUSCAR_INFORMACION -> GENERAR_VEREDICTO -> FINAL_ANSWER. "
                "Decide una accion por iteracion.",
            ),
            (
                "human",
                "Estado actual del agente:\n{state_json}\n\n"
                "Acciones validas: EXTRAER_AFIRMACIONES, BUSCAR_INFORMACION, GENERAR_VEREDICTO, FINAL_ANSWER. "
                "Devuelve thought, action y action_input.",
            ),
        ]
    )
    decision_chain = decision_prompt | llm.with_structured_output(
        AgentStep,
        method="function_calling",
    )

    # Agent state
    state = {
        "afirmacion_original": afirmacion,
        "afirmaciones": None,
        "busqueda": None,
        "veredicto": None,
        "trace": [],
    }

    expected_sequence = [
        "EXTRAER_AFIRMACIONES",
        "BUSCAR_INFORMACION",
        "GENERAR_VEREDICTO",
        "FINAL_ANSWER",
    ]

    for idx in range(6):
        step = decision_chain.invoke(
            {"state_json": json.dumps(state, ensure_ascii=False, indent=2)}
        )
        expected_action = expected_sequence[min(idx, len(expected_sequence) - 1)]
        chosen_action = step.action

        # Guardrail: enforce canonical sequence
        if chosen_action != expected_action:
            state["trace"].append({
                "thought": step.thought,
                "action": f"override:{chosen_action}->{expected_action}",
                "observation": "Guardrail aplicado para mantener orden canonico.",
            })
            chosen_action = expected_action

        if chosen_action == "EXTRAER_AFIRMACIONES":
            observation = tool_extraer_afirmaciones(afirmacion)
            state["afirmaciones"] = json.loads(observation)

        elif chosen_action == "BUSCAR_INFORMACION":
            observation = tool_buscar_informacion(afirmacion, tavily=tavily)
            state["busqueda"] = json.loads(observation)

        elif chosen_action == "GENERAR_VEREDICTO":
            observation = tool_generar_veredicto(
                afirmacion,
                json.dumps(state["busqueda"], ensure_ascii=False),
            )
            state["veredicto"] = json.loads(observation)

        else:
            state["trace"].append({
                "thought": step.thought,
                "action": "FINAL_ANSWER",
                "observation": "Listo para generar verificacion final.",
            })
            break

        state["trace"].append({
            "thought": step.thought,
            "action": chosen_action,
            "observation": observation,
        })

    # Final structured output
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un fact-checker riguroso. Usa el estado consolidado del agente para generar "
                "una verificacion final. Analiza la evidencia encontrada en internet y da una conclusion "
                "clara sobre si la afirmacion es verdadera, falsa o parcialmente verdadera. "
                "Devuelve tema, resumen, afirmaciones_verificadas, conclusion y fuentes (URLs).",
            ),
            (
                "human",
                "Estado consolidado:\n{state_json}",
            ),
        ]
    )
    final_chain = final_prompt | llm.with_structured_output(
        VerificacionFinal,
        method="function_calling",
    )
    resultado = final_chain.invoke(
        {"state_json": json.dumps(state, ensure_ascii=False, indent=2)}
    )

    # Build payload
    trace_preview = [
        {
            "action": s["action"],
            "observation_excerpt": str(s["observation"])[:140],
        }
        for s in state["trace"]
    ]

    payload = {
        "__model": model,
        "afirmacion": afirmacion,
        "state": state,
        "resultado": resultado.model_dump(),
        "trace_preview": trace_preview,
    }

    if verbose:
        print("=" * 80)
        print(f"Modelo: {model}")
        print(f"Afirmacion a verificar: {afirmacion}")
        print("=" * 80)

        print(f"\n## {resultado.tema}\n")
        print(f"**Resumen:** {resultado.resumen}\n")

        print("**Afirmaciones verificadas:**")
        for av in resultado.afirmaciones_verificadas:
            print(f"  - {av}")

        print(f"\n**Conclusion:** {resultado.conclusion}\n")

        print("**Fuentes:**")
        for url in resultado.fuentes:
            print(f"  - {url}")

        print("\n" + "-" * 40)
        print("Trace preview:")
        print(json.dumps(trace_preview, ensure_ascii=False, indent=2))

    return payload


if __name__ == "__main__":
    run_fact_checker()
