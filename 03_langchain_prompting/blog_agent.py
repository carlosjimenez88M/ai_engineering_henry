"""Agente Blog Writer con LangChain: investiga, escribe y revisa un blog post."""

from __future__ import annotations

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


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def tool_investigar_tema(tema: str) -> str:
    """Dado un tema, genera puntos clave para estructurar un blog post."""
    puntos = {
        "tema": tema,
        "puntos_clave": [
            f"Definicion clara de {tema} y su importancia en la cultura Argentina",
            f"Conceptos fundamentales que el lector debe conocer sobre {tema}.",
            f"Casos de uso o ejemplos practicos de {tema}.",
            f"Errores comunes al trabajar con {tema} y como evitarlos.",
            f"Recursos recomendados para profundizar en {tema}.",
        ],
        "audiencia_sugerida": "Desarrolladores y profesionales tech con interes en el tema.",
    }
    return json.dumps(puntos, ensure_ascii=False)


def tool_escribir_borrador(investigacion_json: str) -> str:
    """Dado los puntos clave de la investigacion, genera un borrador de blog post."""
    investigacion = json.loads(investigacion_json)
    tema = investigacion["tema"]
    puntos = investigacion["puntos_clave"]

    secciones = []
    for i, punto in enumerate(puntos, 1):
        secciones.append(f"## Seccion {i}\n\n{punto}\n")

    borrador = {
        "titulo": f"Guia practica: {tema}",
        "contenido": f"# Guia practica: {tema}\n\n"
        + "**Introduccion**\n\n"
        + f"En este articulo exploraremos {tema} de forma practica y accesible.\n\n"
        + "\n".join(secciones)
        + "\n**Conclusion**\n\n"
        + f"Dominar {tema} es una inversion que vale la pena para cualquier profesional tech.\n",
        "tags_sugeridos": [tema.lower().replace(" ", "-"), "tecnologia", "guia-practica"],
    }
    return json.dumps(borrador, ensure_ascii=False)


def tool_revisar_blog(borrador_json: str) -> str:
    """Revisa el borrador del blog y sugiere mejoras concretas."""
    borrador = json.loads(borrador_json)
    contenido = borrador.get("contenido", "")
    titulo = borrador.get("titulo", "")

    sugerencias = []
    if len(contenido) < 200:
        sugerencias.append("El contenido es muy corto. Expandir cada seccion con mas detalle.")
    if not titulo:
        sugerencias.append("Falta un titulo claro y atractivo.")
    sugerencias.append("Agregar ejemplos de codigo o diagramas donde sea posible.")
    sugerencias.append("Incluir una seccion de 'Proximos pasos' para el lector.")

    revision = {
        "aprobado": len(sugerencias) <= 2,
        "sugerencias": sugerencias,
        "nota": "El borrador tiene buena estructura base. Las sugerencias son para mejorar engagement.",
    }
    return json.dumps(revision, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Structured output models
# ---------------------------------------------------------------------------

class AgentStep(BaseModel):
    thought: str
    action: Literal["INVESTIGAR_TEMA", "ESCRIBIR_BORRADOR", "REVISAR_BLOG", "FINAL_ANSWER"]
    action_input: str = Field(default="")


class BlogPost(BaseModel):
    titulo: str
    contenido: str
    tags: list[str]


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run_blog_agent(tema: str = "Sobre la biografía de Evita Perón", verbose: bool = True) -> dict:
    root = find_repo_root(Path.cwd())
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no esta definida en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-4.1")
    llm = ChatOpenAI(model=model, 
                     temperature=0.1, 
                     api_key=api_key)

    # Register tools
    investigar_tool = StructuredTool.from_function(
        func=tool_investigar_tema,
        name="INVESTIGAR_TEMA",
        description="Genera puntos clave para un blog post dado un tema.",
    )
    escribir_tool = StructuredTool.from_function(
        func=tool_escribir_borrador,
        name="ESCRIBIR_BORRADOR",
        description="Genera un borrador de blog post a partir de la investigacion JSON.",
    )
    revisar_tool = StructuredTool.from_function(
        func=tool_revisar_blog,
        name="REVISAR_BLOG",
        description="Revisa el borrador del blog y sugiere mejoras.",
    )

    tool_map = {
        "INVESTIGAR_TEMA": investigar_tool,
        "ESCRIBIR_BORRADOR": escribir_tool,
        "REVISAR_BLOG": revisar_tool,
    }

    # Decision prompt
    decision_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un agente ReAct que escribe blog posts. "
                "Sigue este flujo: INVESTIGAR_TEMA -> ESCRIBIR_BORRADOR -> REVISAR_BLOG -> FINAL_ANSWER. "
                "Decide una accion por iteracion.",
            ),
            (
                "human",
                "Estado actual del agente:\n{state_json}\n\n"
                "Acciones validas: INVESTIGAR_TEMA, ESCRIBIR_BORRADOR, REVISAR_BLOG, FINAL_ANSWER. "
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
        "tema": tema,
        "investigacion": None,
        "borrador": None,
        "revision": None,
        "trace": [],
    }

    expected_sequence = ["INVESTIGAR_TEMA", "ESCRIBIR_BORRADOR", "REVISAR_BLOG", "FINAL_ANSWER"]

    for idx in range(6):
        step = decision_chain.invoke(
            {"state_json": json.dumps(state, ensure_ascii=False, indent=2)}
        )
        expected_action = expected_sequence[min(idx, len(expected_sequence) - 1)]
        chosen_action = step.action

        # Guardrail: enforce canonical sequence
        if chosen_action != expected_action:
            state["trace"].append(
                {
                    "thought": step.thought,
                    "action": f"override:{chosen_action}->{expected_action}",
                    "observation": "Guardrail aplicado para mantener orden canonico.",
                }
            )
            chosen_action = expected_action

        if chosen_action == "INVESTIGAR_TEMA":
            observation = tool_map[chosen_action].invoke({"tema": tema})
            state["investigacion"] = json.loads(observation)
        elif chosen_action == "ESCRIBIR_BORRADOR":
            observation = tool_map[chosen_action].invoke(
                {"investigacion_json": json.dumps(state["investigacion"], ensure_ascii=False)}
            )
            state["borrador"] = json.loads(observation)
        elif chosen_action == "REVISAR_BLOG":
            observation = tool_map[chosen_action].invoke(
                {"borrador_json": json.dumps(state["borrador"], ensure_ascii=False)}
            )
            state["revision"] = json.loads(observation)
        else:
            state["trace"].append(
                {
                    "thought": step.thought,
                    "action": "FINAL_ANSWER",
                    "observation": "Listo para generar el blog post final.",
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

    # Final structured output
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Genera el blog post final usando el estado consolidado del agente. "
                "Mejora el borrador incorporando las sugerencias de la revision. "
                "Devuelve titulo, contenido (en markdown) y tags.",
            ),
            (
                "human",
                "Estado consolidado:\n{state_json}",
            ),
        ]
    )
    final_chain = final_prompt | llm.with_structured_output(
        BlogPost,
        method="function_calling",
    )
    blog_post = final_chain.invoke(
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
        "tema": tema,
        "state": state,
        "blog_post": blog_post.model_dump(),
        "trace_preview": trace_preview,
    }

    if verbose:
        print("=" * 80)
        print(f"Modelo: {model}")
        print(f"Tema: {tema}")
        print("=" * 80)

        print(f"\n## {blog_post.titulo}\n")
        print(blog_post.contenido)
        print(f"\nTags: {', '.join(blog_post.tags)}")

        print("\n" + "-" * 40)
        print("Trace preview:")
        print(json.dumps(trace_preview, ensure_ascii=False, indent=2))

    return payload


if __name__ == "__main__":
    run_blog_agent()
