"""CoT con LangGraph: arquitectura de grafo con visualizacion PNG.

Este modulo migra la implementacion manual de CoT a LangGraph, habilitando:
- Visualizacion de grafos con draw_mermaid_png()
- Gestion de estado explicita con StateGraph
- Mejor debugging y trazabilidad
- Arquitectura componible y mantenible
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Any, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field


def find_repo_root(start: Path) -> Path:
    """Encuentra la raiz del repositorio buscando pyproject.toml."""
    for path in [start, *start.parents]:
        if (path / "pyproject.toml").exists():
            return path
    raise RuntimeError("No se encontro la raiz del repositorio")


def load_context_builder(root: Path):
    """Carga dinamicamente el modulo de context engineering."""
    ctx_path = root / "03_langchain_prompting" / "common" / "context_engineering.py"
    spec = importlib.util.spec_from_file_location("context_engineering03", ctx_path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar modulo: {ctx_path}")
    spec.loader.exec_module(module)
    return module.build_context_packet


class CoTOutput(BaseModel):
    """Esquema de salida estructurada para CoT."""

    chain_of_thought: list[str] = Field(description="Cuatro pasos de razonamiento breve")
    opener: str
    follow_up: str
    tone_notes: list[str]
    avoid: list[str]


class CoTState(TypedDict):
    """Estado del grafo de CoT.

    Attributes:
        context_packet: Contexto estructurado del perfil
        zero_shot_result: Resultado del CoT zero-shot (None si no ejecutado)
        few_shot_result: Resultado del CoT few-shot (None si no ejecutado)
        evaluation: Evaluacion del draft (None si no ejecutado)
        refined_result: Resultado refinado (None si no ejecutado)
        final_result: Resultado final seleccionado
        llm_creative: Instancia de LLM con temperatura alta
        llm_deterministic: Instancia de LLM con temperatura baja
        verbose: Si imprimir outputs intermedios
    """

    context_packet: dict[str, Any]
    zero_shot_result: CoTOutput | None
    few_shot_result: CoTOutput | None
    evaluation: dict[str, Any] | None
    refined_result: CoTOutput | None
    final_result: CoTOutput | None
    llm_creative: ChatOpenAI
    llm_deterministic: ChatOpenAI
    verbose: bool


def _normalize(text: str) -> str:
    """Normaliza texto para comparacion."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9\\s]", " ", text.lower())
    text = re.sub(r"\\s+", " ", text).strip()
    return text


def _match_gusto(texto: str, gusto: str) -> bool:
    """Verifica si un gusto esta mencionado en el texto."""
    gusto_tokens = [t for t in _normalize(gusto).split() if len(t) > 2]
    if not gusto_tokens:
        return False
    normalized_text = _normalize(texto)
    hits = sum(1 for token in gusto_tokens if token in normalized_text)
    threshold = max(1, len(gusto_tokens) // 2)
    return hits >= threshold


def evaluar_salida(perfil: dict[str, Any], salida: CoTOutput) -> dict[str, Any]:
    """Evalua la calidad de una salida CoT con rubrica cuantitativa."""
    opener = salida.opener
    follow_up = salida.follow_up
    texto = f"{opener} {follow_up}".strip()
    gustos = [str(x) for x in perfil.get("gustos", [])]

    hits = sum(1 for gusto in gustos if _match_gusto(texto, gusto))
    personalizacion = 9 if hits >= 3 else 7 if hits == 2 else 5 if hits == 1 else 3
    naturalidad = 8 if 12 <= len(opener.split()) <= 28 else 6
    respeto = 9 if not re.search(r"\b(insiste|presiona|explicito)\b", _normalize(texto)) else 4
    accionable = 8 if "?" in texto else 5

    promedio = round((personalizacion + naturalidad + respeto + accionable) / 4, 2)
    return {
        "scores": {
            "personalizacion": personalizacion,
            "naturalidad": naturalidad,
            "respeto": respeto,
            "accionable": accionable,
        },
        "promedio": promedio,
    }


# === NODOS DEL GRAFO ===


def node_zero_shot_cot(state: CoTState) -> CoTState:
    """Nodo: ejecuta CoT zero-shot (sin ejemplos)."""
    context_packet = state["context_packet"]
    llm = state["llm_creative"]

    zero_shot_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un coach conversacional elegante, respetuoso y practico. "
                "Siempre prioriza consentimiento, autenticidad y respeto.",
            ),
            (
                "human",
                "Disena una recomendacion personalizada usando este context packet:\n"
                "{context_packet}\n\n"
                "Usa Chain of Thought visible en 4 pasos breves:\n"
                "1) Senales clave.\n"
                "2) Estrategia de apertura.\n"
                "3) Riesgos a evitar.\n"
                "4) Recomendacion final.\n\n"
                "Incluye al menos dos gustos textuales del perfil en opener o follow_up.\n\n"
                "Devuelve campos: chain_of_thought, opener, follow_up, tone_notes, avoid.",
            ),
        ]
    )

    zero_shot_chain = zero_shot_prompt | llm.with_structured_output(
        CoTOutput,
        method="function_calling",
    )
    result = zero_shot_chain.invoke(
        {"context_packet": json.dumps(context_packet, ensure_ascii=False, indent=2)}
    )

    if state["verbose"]:
        print("\n[Zero-shot CoT]")
        print(result.model_dump_json(indent=2))

    return {**state, "zero_shot_result": result}


def node_few_shot_cot(state: CoTState) -> CoTState:
    """Nodo: ejecuta CoT few-shot (con ejemplos)."""
    context_packet = state["context_packet"]
    llm = state["llm_creative"]

    few_shot_examples = [
        {
            "input": json.dumps(
                {
                    "tipo_persona": "fan de senderismo",
                    "gustos": ["montana", "cafes de especialidad"],
                    "estilo": "humor suave",
                    "contexto": "primer contacto",
                },
                ensure_ascii=False,
            ),
            "output": json.dumps(
                {
                    "chain_of_thought": [
                        "Perfil outdoor",
                        "Apertura ligera",
                        "Evitar intensidad",
                        "Cerrar con pregunta",
                    ],
                    "opener": "Vi que te gusta la montana, tienes una ruta favorita para desconectarte un domingo?",
                    "follow_up": "Si me recomiendas una, yo llevo el cafe.",
                    "tone_notes": ["curioso", "ligero"],
                    "avoid": ["mensaje largo", "halago intenso"],
                },
                ensure_ascii=False,
            ),
        },
        {
            "input": json.dumps(
                {
                    "tipo_persona": "lectora analitica",
                    "gustos": ["novela historica", "cine europeo"],
                    "estilo": "profundo",
                    "contexto": "retomar conversacion",
                },
                ensure_ascii=False,
            ),
            "output": json.dumps(
                {
                    "chain_of_thought": [
                        "Valora contenido",
                        "Evitar cliches",
                        "Pregunta con sustancia",
                        "Invitar intercambio",
                    ],
                    "opener": "Tu perfil suena a buena conversacion, que libro te dejo pensando ultimamente?",
                    "follow_up": "Si quieres, intercambiamos recomendaciones.",
                    "tone_notes": ["intelectual", "calido"],
                    "avoid": ["frase prefabricada", "elogio vacio"],
                },
                ensure_ascii=False,
            ),
        },
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [("human", "Perfil:\n{input}"), ("ai", "{output}")]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        examples=few_shot_examples,
        example_prompt=example_prompt,
    )

    full_few_shot_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un estratega conversacional. Responde en formato estructurado y manten respeto.",
            ),
            few_shot_prompt,
            (
                "human",
                "Perfil actual:\n{context_packet}\n\n"
                "Debes mencionar al menos dos gustos exactos del perfil en opener o follow_up.\n\n"
                "Genera salida en el mismo formato del ejemplo.",
            ),
        ]
    )

    few_shot_chain = full_few_shot_prompt | llm.with_structured_output(
        CoTOutput,
        method="function_calling",
    )
    result = few_shot_chain.invoke(
        {"context_packet": json.dumps(context_packet["profile"], ensure_ascii=False, indent=2)}
    )

    if state["verbose"]:
        print("\n[Few-shot CoT]")
        print(result.model_dump_json(indent=2))

    return {**state, "few_shot_result": result}


def node_evaluate(state: CoTState) -> CoTState:
    """Nodo: evalua el resultado few-shot con rubrica."""
    few_shot_result = state["few_shot_result"]
    context_packet = state["context_packet"]

    if few_shot_result is None:
        raise RuntimeError("few_shot_result es None en node_evaluate")

    evaluation = evaluar_salida(context_packet["profile"], few_shot_result)

    if state["verbose"]:
        print("\n[Evaluacion Draft]")
        print(json.dumps(evaluation, indent=2, ensure_ascii=False))

    return {**state, "evaluation": evaluation}


def node_refine(state: CoTState) -> CoTState:
    """Nodo: refina el resultado si la evaluacion es baja."""
    context_packet = state["context_packet"]
    few_shot_result = state["few_shot_result"]
    llm = state["llm_deterministic"]
    evaluation = state["evaluation"]

    if few_shot_result is None or evaluation is None:
        raise RuntimeError("Estado invalido en node_refine")

    review_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un revisor critico de prompting. Mejora calidad sin perder respeto ni naturalidad.",
            ),
            (
                "human",
                "Perfil:\n{profile}\n\nDraft actual:\n{draft}\n\n"
                "Refina el draft para mejorar personalizacion, naturalidad y accionabilidad. "
                "Debes mencionar al menos dos gustos exactos de esta lista: {gustos_obligatorios}. "
                "Devuelve el mismo esquema: chain_of_thought, opener, follow_up, tone_notes, avoid.",
            ),
        ]
    )

    review_chain = review_prompt | llm.with_structured_output(
        CoTOutput,
        method="function_calling",
    )
    refined = review_chain.invoke(
        {
            "profile": json.dumps(context_packet["profile"], ensure_ascii=False, indent=2),
            "draft": few_shot_result.model_dump_json(indent=2),
            "gustos_obligatorios": ", ".join(context_packet["profile"]["gustos"]),
        }
    )

    refined_eval = evaluar_salida(context_packet["profile"], refined)

    # Si aun es bajo, aplicar refinamiento estricto
    if refined_eval["scores"]["personalizacion"] < 7:
        strict_review_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Eres un revisor estricto. Tu prioridad es personalizacion verificable.",
                ),
                (
                    "human",
                    "Perfil:\n{profile}\n\nDraft:\n{draft}\n\n"
                    "Regenera obligatoriamente mencionando al menos dos gustos exactos en opener/follow_up: "
                    "{gustos_obligatorios}. Mantener respeto y naturalidad.",
                ),
            ]
        )
        strict_review_chain = strict_review_prompt | llm.with_structured_output(
            CoTOutput,
            method="function_calling",
        )
        refined = strict_review_chain.invoke(
            {
                "profile": json.dumps(context_packet["profile"], ensure_ascii=False, indent=2),
                "draft": refined.model_dump_json(indent=2),
                "gustos_obligatorios": ", ".join(context_packet["profile"]["gustos"]),
            }
        )
        refined_eval = evaluar_salida(context_packet["profile"], refined)

    if state["verbose"]:
        print("\n[Refinamiento]")
        print(refined.model_dump_json(indent=2))
        print("\nEvaluacion refinada:")
        print(json.dumps(refined_eval, indent=2, ensure_ascii=False))

    return {**state, "refined_result": refined, "evaluation": refined_eval}


def node_finalize(state: CoTState) -> CoTState:
    """Nodo: selecciona la mejor version (draft vs refinada)."""
    few_shot_result = state["few_shot_result"]
    refined_result = state["refined_result"]
    context_packet = state["context_packet"]

    if few_shot_result is None:
        raise RuntimeError("few_shot_result es None en node_finalize")

    # Evaluar ambas versiones
    base_eval = evaluar_salida(context_packet["profile"], few_shot_result)

    if refined_result is not None:
        refined_eval = evaluar_salida(context_packet["profile"], refined_result)
        # Seleccionar mejor version
        if refined_eval["promedio"] >= base_eval["promedio"]:
            final_result = refined_result
            final_eval = refined_eval
        else:
            final_result = few_shot_result
            final_eval = base_eval
    else:
        final_result = few_shot_result
        final_eval = base_eval

    if state["verbose"]:
        print("\n[Version Final Seleccionada]")
        print(final_result.model_dump_json(indent=2))
        print("\nEvaluacion final:")
        print(json.dumps(final_eval, indent=2, ensure_ascii=False))

    return {**state, "final_result": final_result, "evaluation": final_eval}


# === FUNCION DE ROUTING ===


def should_refine(state: CoTState) -> Literal["refine", "finalize"]:
    """Decide si refinar o finalizar basado en la evaluacion."""
    evaluation = state["evaluation"]
    if evaluation is None:
        return "finalize"

    # Si el promedio es bajo, refinar
    if evaluation["promedio"] < 7:
        return "refine"
    return "finalize"


# === CONSTRUCCION DEL GRAFO ===


def build_cot_graph() -> StateGraph:
    """Construye el grafo de CoT con LangGraph.

    Returns:
        StateGraph compilado listo para ejecutar
    """
    graph = StateGraph(CoTState)

    # Agregar nodos
    graph.add_node("zero_shot", node_zero_shot_cot)
    graph.add_node("few_shot", node_few_shot_cot)
    graph.add_node("evaluate", node_evaluate)
    graph.add_node("refine", node_refine)
    graph.add_node("finalize", node_finalize)

    # Definir flujo
    graph.set_entry_point("zero_shot")
    graph.add_edge("zero_shot", "few_shot")
    graph.add_edge("few_shot", "evaluate")

    # Conditional: evaluar -> refinar o finalizar
    graph.add_conditional_edges(
        "evaluate",
        should_refine,
        {
            "refine": "refine",
            "finalize": "finalize",
        },
    )

    # Refine siempre va a finalize
    graph.add_edge("refine", "finalize")

    # Finalize es el final
    graph.add_edge("finalize", END)

    return graph.compile()


# === FUNCION PRINCIPAL ===


def run_cot_langgraph(profile: dict[str, Any] | None = None, verbose: bool = True) -> dict[str, Any]:
    """Ejecuta CoT con LangGraph y retorna payload completo.

    Args:
        profile: Perfil del usuario (None usa default)
        verbose: Si imprimir outputs intermedios

    Returns:
        Dict con resultados, evaluaciones y metadata
    """
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    build_context_packet = load_context_builder(root)

    llm_creative = ChatOpenAI(model=model, temperature=0.7, api_key=api_key)
    llm_deterministic = ChatOpenAI(model=model, temperature=0.3, api_key=api_key)

    if profile is None:
        profile = {
            "tipo_persona": "neurocientifica especializada en sueno",
            "gustos": ["documentales BBC", "yoga aereo", "cafes silenciosos para leer"],
            "estilo": "curiosa, valora profundidad y evidencia, humor sutil",
            "contexto": "match tras leer biografia completa, ella menciono paper tuyo",
        }

    context_packet = build_context_packet(
        profile=profile,
        module="03_langchain_prompting",
        strategy="cot_langgraph",
    )

    if verbose:
        print("=" * 80)
        print(f"Modelo: {model}")
        print("Context packet aplicado (context engineering):")
        print(json.dumps(context_packet, ensure_ascii=False, indent=2))

    # Construir grafo
    app = build_cot_graph()

    # Estado inicial
    initial_state: CoTState = {
        "context_packet": context_packet,
        "zero_shot_result": None,
        "few_shot_result": None,
        "evaluation": None,
        "refined_result": None,
        "final_result": None,
        "llm_creative": llm_creative,
        "llm_deterministic": llm_deterministic,
        "verbose": verbose,
    }

    # Ejecutar grafo
    final_state = app.invoke(initial_state)

    # Construir payload
    payload = {
        "__model": model,
        "__context_hash": context_packet["context_hash"],
        "__architecture": "langgraph_cot",
        "context_packet": context_packet,
        "zero_shot": final_state["zero_shot_result"].model_dump() if final_state["zero_shot_result"] else None,
        "few_shot": final_state["few_shot_result"].model_dump() if final_state["few_shot_result"] else None,
        "refined": final_state["refined_result"].model_dump() if final_state["refined_result"] else None,
        "final": final_state["final_result"].model_dump() if final_state["final_result"] else None,
        "evaluation": final_state["evaluation"],
        "graph": app,  # Retornar grafo para visualizacion
    }

    if verbose:
        print("\n[Autocritica]")
        print("- LangGraph hace el flujo mas explicito y debuggeable que cadenas manuales.")
        print("- El estado compartido evita pasar parametros manualmente entre pasos.")
        print("- La visualizacion del grafo ayuda a entender el flujo sin leer codigo.")
        print("- El overhead de LangGraph es minimo comparado con los beneficios de mantenibilidad.")

    return payload


def run_cot_with_persona(persona_dict: dict[str, Any], verbose: bool = True) -> dict[str, Any]:
    """Ejecuta CoT con una persona Latino personalizada.

    Args:
        persona_dict: Dict con estructura de PersonaLatino
        verbose: Si imprimir outputs intermedios

    Returns:
        Dict con resultados, evaluaciones y metadata
    """
    # Convertir persona a formato de perfil esperado por CoT
    profile = {
        "tipo_persona": persona_dict["tipo_persona"],
        "gustos": persona_dict["gustos"],
        "estilo": persona_dict["estilo"],
        "contexto": persona_dict["contexto"],
    }

    return run_cot_langgraph(profile=profile, verbose=verbose)


if __name__ == "__main__":
    result = run_cot_langgraph()
    print("\n[Grafo construido exitosamente]")
    print("Para visualizar: app.get_graph().draw_mermaid_png()")
