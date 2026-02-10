"""ReAct con LangGraph: arquitectura con ToolNode y visualizacion PNG.

Este modulo migra la implementacion manual de ReAct a LangGraph, habilitando:
- Visualizacion de grafos con draw_mermaid_png()
- ToolNode integrado para ejecucion de herramientas
- Gestion de estado con mensajes (LangChain pattern)
- Routing automatico entre agent y tools
- Mejor debugging y trazabilidad
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Annotated, Any, Literal, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
import operator


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
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar modulo: {ctx_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_context_packet


# === DEFINICION DE HERRAMIENTAS ===


@tool
def analizar_perfil(context_packet_json: str) -> str:
    """Extrae insights accionables desde un context packet JSON.

    Args:
        context_packet_json: JSON string con el context packet

    Returns:
        JSON string con analisis del perfil
    """
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


@tool
def generar_mensaje(analysis_json: str) -> str:
    """Genera opener y follow_up a partir de analysis JSON.

    Args:
        analysis_json: JSON string con analisis del perfil

    Returns:
        JSON string con mensaje generado
    """
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


@tool
def auditar_respeto(message_json: str) -> str:
    """Audita respeto y ausencia de presion en el mensaje.

    Args:
        message_json: JSON string con el mensaje a auditar

    Returns:
        JSON string con resultado de auditoria
    """
    message = json.loads(message_json)
    texto = f"{message.get('opener', '')} {message.get('follow_up', '')}".lower()
    flags = [w for w in ["insiste", "presiona", "explicito"] if w in texto]
    result = {
        "ok": len(flags) == 0,
        "flags": flags,
        "suggestion": "Mantener pregunta abierta y evitar intensidad prematura.",
    }
    return json.dumps(result, ensure_ascii=False)


# === ESTADO DEL GRAFO ===


class ReActState(TypedDict):
    """Estado del grafo ReAct.

    Attributes:
        context_packet: Context packet estructurado
        messages: Historial de mensajes (agent, tools, human)
        verbose: Si imprimir outputs intermedios
    """

    context_packet: dict[str, Any]
    messages: Annotated[Sequence[BaseMessage], operator.add]
    verbose: bool


# === NODOS DEL GRAFO ===


def agent_node(state: ReActState) -> ReActState:
    """Nodo agente: decide que accion tomar.

    El agente analiza el estado actual y decide si:
    - Llamar una herramienta (analizar, generar, auditar)
    - Dar respuesta final (terminar)
    """
    # Crear LLM con tools
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.4,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    tools = [analizar_perfil, generar_mensaje, auditar_respeto]
    llm_with_tools = llm.bind_tools(tools)

    # System message para el agente
    system_message = HumanMessage(
        content=(
            "Eres un agente ReAct disciplinado. Tu flujo es:\n"
            "1. ANALIZAR_PERFIL: Extrae insights del context packet\n"
            "2. GENERAR_MENSAJE: Crea opener y follow_up\n"
            "3. AUDITAR_RESPETO: Valida respeto y tono\n"
            "4. FINAL_ANSWER: Responde con resultado final\n\n"
            f"Context packet:\n{json.dumps(state['context_packet'], ensure_ascii=False, indent=2)}"
        )
    )

    messages = [system_message] + list(state["messages"])
    result = llm_with_tools.invoke(messages)

    if state["verbose"]:
        if hasattr(result, "tool_calls") and result.tool_calls:
            print(f"\n[Agent Decision] Tool: {result.tool_calls[0]['name']}")
        else:
            print("\n[Agent Decision] Final answer")

    return {**state, "messages": [result]}


# === ROUTING ===


def should_continue(state: ReActState) -> Literal["tools", "end"]:
    """Decide si continuar con tools o terminar.

    Returns:
        "tools" si el ultimo mensaje tiene tool_calls, "end" si no
    """
    messages = state["messages"]
    last_message = messages[-1]

    # Si el ultimo mensaje es del agente y tiene tool calls, ir a tools
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Si no, terminar
    return "end"


# === CONSTRUCCION DEL GRAFO ===


def build_react_graph() -> StateGraph:
    """Construye el grafo ReAct con LangGraph.

    Returns:
        StateGraph compilado listo para ejecutar
    """
    # Definir tools
    tools = [analizar_perfil, generar_mensaje, auditar_respeto]
    tool_node = ToolNode(tools)

    # Crear grafo
    graph = StateGraph(ReActState)

    # Agregar nodos
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    # Definir flujo
    graph.set_entry_point("agent")

    # Conditional: agent -> tools o end
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )

    # tools siempre vuelve a agent
    graph.add_edge("tools", "agent")

    return graph.compile()


# === CLASES DE OUTPUT ===


class FinalAnswer(BaseModel):
    """Esquema de respuesta final."""

    opener: str
    follow_up: str
    why_it_works: list[str]
    trace_summary: list[str]


# === FUNCION PRINCIPAL ===


def run_react_langgraph(profile: dict[str, Any] | None = None, verbose: bool = True) -> dict[str, Any]:
    """Ejecuta ReAct con LangGraph y retorna payload completo.

    Args:
        profile: Perfil del usuario (None usa default)
        verbose: Si imprimir outputs intermedios

    Returns:
        Dict con resultados, estado final y metadata
    """
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    build_context_packet = load_context_builder(root)

    if profile is None:
        profile = {
            "tipo_persona": "arquitecta apasionada por fotografia urbana",
            "gustos": ["cafes tranquilos", "jazz", "viajes cortos"],
            "estilo": "intelectual pero relajado",
            "contexto": "match reciente, primera interaccion",
        }

    context_packet = build_context_packet(
        profile=profile,
        module="03_langchain_prompting",
        strategy="react_langgraph",
    )

    if verbose:
        print("=" * 80)
        print(f"Modelo: {model}")
        print("Context packet aplicado (context engineering):")
        print(json.dumps(context_packet, ensure_ascii=False, indent=2))

    # Construir grafo
    app = build_react_graph()

    # Estado inicial
    initial_state: ReActState = {
        "context_packet": context_packet,
        "messages": [],
        "verbose": verbose,
    }

    # Ejecutar grafo
    final_state = app.invoke(initial_state)

    # Extraer informacion del trace
    trace = []
    analysis_result = None
    draft_result = None
    audit_result = None

    for msg in final_state["messages"]:
        if isinstance(msg, ToolMessage):
            tool_name = msg.name
            content = msg.content
            trace.append({"tool": tool_name, "result": content[:200]})

            # Guardar resultados por tool
            if tool_name == "analizar_perfil":
                analysis_result = json.loads(content)
            elif tool_name == "generar_mensaje":
                draft_result = json.loads(content)
            elif tool_name == "auditar_respeto":
                audit_result = json.loads(content)

    # Generar respuesta final estructurada
    llm = ChatOpenAI(model=model, temperature=0.4, api_key=api_key)
    final_prompt = (
        "Genera la respuesta final usando estos resultados:\n\n"
        f"Analisis: {json.dumps(analysis_result, ensure_ascii=False)}\n"
        f"Draft: {json.dumps(draft_result, ensure_ascii=False)}\n"
        f"Auditoria: {json.dumps(audit_result, ensure_ascii=False)}\n\n"
        "Devuelve: opener, follow_up, why_it_works (lista de razones), trace_summary (lista de pasos ejecutados)"
    )

    final_chain = llm.with_structured_output(FinalAnswer, method="function_calling")
    final_answer = final_chain.invoke([HumanMessage(content=final_prompt)])

    # Construir payload
    payload = {
        "__model": model,
        "__context_hash": context_packet["context_hash"],
        "__architecture": "langgraph_react",
        "context_packet": context_packet,
        "analysis": analysis_result,
        "draft": draft_result,
        "audit": audit_result,
        "final_answer": final_answer.model_dump(),
        "trace": trace,
        "graph": app,  # Retornar grafo para visualizacion
    }

    if verbose:
        print("\n[Final Answer]")
        print(final_answer.model_dump_json(indent=2))

        print("\n[Trace Summary]")
        for i, step in enumerate(trace, 1):
            print(f"{i}. {step['tool']}: {step['result'][:100]}...")

        print("\n[Autocritica]")
        print("- LangGraph con ToolNode hace el patron ReAct mas idiomatico que loops manuales.")
        print("- El routing automatico (agent -> tools -> agent) reduce boilerplate.")
        print("- La visualizacion del grafo muestra claramente el ciclo ReAct.")
        print("- Los mensajes persistidos permiten debugging y replay de conversaciones.")

    return payload


def build_react_graph_with_custom_tools(custom_tools: list) -> StateGraph:
    """Construye el grafo ReAct con herramientas personalizadas.

    Args:
        custom_tools: Lista de herramientas LangChain tools

    Returns:
        StateGraph compilado listo para ejecutar
    """
    tool_node = ToolNode(custom_tools)

    # Crear grafo
    graph = StateGraph(ReActState)

    # Agregar nodos - necesitamos crear agent_node que use las custom tools
    def custom_agent_node(state: ReActState):
        """Nodo del agente que usa herramientas personalizadas."""
        context_packet = state["context_packet"]
        messages = state["messages"]
        verbose = state.get("verbose", False)

        # Cargar LLM
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        llm = ChatOpenAI(model=model, temperature=0.7, api_key=api_key)

        # Bind tools
        llm_with_tools = llm.bind_tools(custom_tools)

        # Si es primera invocacion, crear mensaje inicial
        if not messages:
            system_msg = (
                f"Eres un asistente especializado en analizar perfiles y generar estrategias de coqueteo.\n"
                f"Context packet: {json.dumps(context_packet, ensure_ascii=False)}\n\n"
                f"Usa las herramientas disponibles para:\n"
                f"1. Analizar compatibilidad entre perfiles\n"
                f"2. Generar icebreakers calibrados\n"
                f"3. Predecir probabilidad de respuesta\n"
                f"4. Escalar conversacion estrategicamente\n\n"
                f"Piensa paso a paso y usa las herramientas en orden logico."
            )
            messages = [HumanMessage(content=system_msg)]

        # Invocar LLM
        response = llm_with_tools.invoke(messages)

        if verbose:
            print(f"\n[Agent] {response.content[:200] if response.content else 'tool_calls'}...")

        return {"messages": messages + [response]}

    graph.add_node("agent", custom_agent_node)
    graph.add_node("tools", tool_node)

    # Definir flujo
    graph.set_entry_point("agent")

    # Conditional: agent -> tools o end
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )

    # tools siempre vuelve a agent
    graph.add_edge("tools", "agent")

    return graph.compile()


def run_react_with_coqueteo_tools(persona_dict: dict[str, Any], match_dict: dict[str, Any], verbose: bool = True) -> dict[str, Any]:
    """Ejecuta ReAct con herramientas especializadas de coqueteo.

    Args:
        persona_dict: Dict con estructura de PersonaLatino
        match_dict: Dict con perfil del match
        verbose: Si imprimir outputs intermedios

    Returns:
        Dict con resultados y metadata
    """
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Importar herramientas especializadas
    import sys
    sys.path.insert(0, str(root / "03_langchain_prompting"))
    from common.coqueteo_tools import COQUETEO_TOOLS

    # Construir context packet
    build_context_packet = load_context_builder(root)

    profile = {
        "tipo_persona": persona_dict["tipo_persona"],
        "gustos": persona_dict["gustos"],
        "estilo": persona_dict["estilo"],
        "contexto": persona_dict["contexto"],
    }

    context_packet = build_context_packet(
        profile=profile,
        module="03_langchain_prompting",
        strategy="react_coqueteo",
    )

    # Agregar info del match al context packet
    context_packet["match"] = match_dict

    if verbose:
        print("=" * 80)
        print(f"Modelo: {model}")
        print(f"Persona: {persona_dict['pais_origen']} - {persona_dict['tipo_persona']}")
        print(f"Match: {match_dict.get('nombre', 'Unknown')} - {match_dict.get('profesion', 'Unknown')}")
        print(f"Herramientas: {len(COQUETEO_TOOLS)} especializadas")

    # Construir grafo con herramientas personalizadas
    app = build_react_graph_with_custom_tools(COQUETEO_TOOLS)

    # Estado inicial
    initial_state: ReActState = {
        "context_packet": context_packet,
        "messages": [],
        "verbose": verbose,
    }

    # Ejecutar grafo
    final_state = app.invoke(initial_state)

    # Extraer trace
    trace = []
    tool_results = {}

    for msg in final_state["messages"]:
        if isinstance(msg, ToolMessage):
            tool_name = msg.name
            content = msg.content
            trace.append({"tool": tool_name, "result_preview": content[:200]})
            tool_results[tool_name] = json.loads(content) if content.startswith('{') else content

    # Construir payload
    payload = {
        "__model": model,
        "__context_hash": context_packet["context_hash"],
        "__architecture": "langgraph_react_coqueteo",
        "persona": persona_dict,
        "match": match_dict,
        "tool_results": tool_results,
        "trace": trace,
        "graph": app,
    }

    if verbose:
        print("\n[Tool Results Summary]")
        for tool_name, result in tool_results.items():
            print(f"\n{tool_name}:")
            if isinstance(result, dict):
                for key, value in result.items():
                    if isinstance(value, list) and value:
                        print(f"  {key}: {value[0] if len(value) == 1 else f'{len(value)} items'}")
                    elif isinstance(value, (str, int, float)):
                        print(f"  {key}: {value}")

    return payload


if __name__ == "__main__":
    result = run_react_langgraph()
    print("\n[Grafo construido exitosamente]")
    print("Para visualizar: app.get_graph().draw_mermaid_png()")
