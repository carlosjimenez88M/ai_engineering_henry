"""CoT avanzado con LangChain: zero-shot, few-shot y feedback loop."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
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


class CoTOutput(BaseModel):
    chain_of_thought: list[str] = Field(description="Cuatro pasos de razonamiento breve")
    opener: str
    follow_up: str
    tone_notes: list[str]
    avoid: list[str]


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9\\s]", " ", text.lower())
    text = re.sub(r"\\s+", " ", text).strip()
    return text


def _match_gusto(texto: str, gusto: str) -> bool:
    gusto_tokens = [t for t in _normalize(gusto).split() if len(t) > 2]
    if not gusto_tokens:
        return False
    normalized_text = _normalize(texto)
    hits = sum(1 for token in gusto_tokens if token in normalized_text)
    threshold = max(1, len(gusto_tokens) // 2)
    return hits >= threshold


def evaluar_salida(perfil: dict[str, Any], salida: CoTOutput) -> dict[str, Any]:
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


def run_cot_langchain(profile: dict[str, Any] | None = None, verbose: bool = True) -> dict[str, Any]:
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
        strategy="cot_zero_shot",
    )

    if verbose:
        print("=" * 80)
        print(f"Modelo: {model}")
        print("Context packet aplicado (context engineering):")
        print(json.dumps(context_packet, ensure_ascii=False, indent=2))

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

    zero_shot_chain = zero_shot_prompt | llm_creative.with_structured_output(
        CoTOutput,
        method="function_calling",
    )
    zero_shot_result = zero_shot_chain.invoke(
        {"context_packet": json.dumps(context_packet, ensure_ascii=False, indent=2)}
    )

    if verbose:
        print("\n[Zero-shot CoT]")
        print(zero_shot_result.model_dump_json(indent=2, ensure_ascii=False))

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

    few_shot_chain = full_few_shot_prompt | llm_creative.with_structured_output(
        CoTOutput,
        method="function_calling",
    )
    few_shot_result = few_shot_chain.invoke(
        {"context_packet": json.dumps(context_packet["profile"], ensure_ascii=False, indent=2)}
    )

    if verbose:
        print("\n[Few-shot CoT]")
        print(few_shot_result.model_dump_json(indent=2, ensure_ascii=False))

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

    review_chain = review_prompt | llm_deterministic.with_structured_output(
        CoTOutput,
        method="function_calling",
    )
    reviewed_result = review_chain.invoke(
        {
            "profile": json.dumps(context_packet["profile"], ensure_ascii=False, indent=2),
            "draft": few_shot_result.model_dump_json(indent=2, ensure_ascii=False),
            "gustos_obligatorios": ", ".join(context_packet["profile"]["gustos"]),
        }
    )

    base_eval = evaluar_salida(context_packet["profile"], few_shot_result)
    refined_eval = evaluar_salida(context_packet["profile"], reviewed_result)

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
        strict_review_chain = strict_review_prompt | llm_deterministic.with_structured_output(
            CoTOutput,
            method="function_calling",
        )
        reviewed_result = strict_review_chain.invoke(
            {
                "profile": json.dumps(context_packet["profile"], ensure_ascii=False, indent=2),
                "draft": reviewed_result.model_dump_json(indent=2, ensure_ascii=False),
                "gustos_obligatorios": ", ".join(context_packet["profile"]["gustos"]),
            }
        )
        refined_eval = evaluar_salida(context_packet["profile"], reviewed_result)

    selected_result = reviewed_result
    selected_eval = refined_eval
    if refined_eval["promedio"] < base_eval["promedio"]:
        selected_result = few_shot_result
        selected_eval = base_eval

    flow_mermaid = (
        "graph TD\n"
        "A[Context Packet] --> B[Zero-shot CoT]\n"
        "A --> C[Few-shot CoT]\n"
        "C --> D[Evaluar Draft]\n"
        "D --> E[Refinar]\n"
        "E --> F[Seleccionar Mejor Version]"
    )

    payload = {
        "__model": model,
        "__context_hash": context_packet["context_hash"],
        "__flow_mermaid": flow_mermaid,
        "context_packet": context_packet,
        "zero_shot": zero_shot_result.model_dump(),
        "few_shot": few_shot_result.model_dump(),
        "reviewed": reviewed_result.model_dump(),
        "selected": selected_result.model_dump(),
        "base_eval": base_eval,
        "refined_eval": refined_eval,
        "selected_eval": selected_eval,
    }

    if verbose:
        print("\n[Feedback Loop]")
        print("Evaluacion draft:")
        print(json.dumps(base_eval, indent=2, ensure_ascii=False))
        print("\nEvaluacion refinada:")
        print(json.dumps(refined_eval, indent=2, ensure_ascii=False))
        print("\nVersion final seleccionada:")
        print(selected_result.model_dump_json(indent=2, ensure_ascii=False))
        print("\nEvaluacion version final:")
        print(json.dumps(selected_eval, indent=2, ensure_ascii=False))

        print("\n[Autocritica]")
        print("- Few-shot mejora consistencia, pero aumenta tokens y costo.")
        print("- El feedback loop mejora calidad media, pero duplica llamadas LLM.")
        print("- El contexto limpio (context packet) evita deriva por ruido narrativo.")

    return payload


if __name__ == "__main__":
    run_cot_langchain()
