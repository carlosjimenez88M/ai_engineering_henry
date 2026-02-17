"""
Zero-shot ReAct: Agente conversacional con herramientas y razonamiento cíclico.

DIAGRAMA: Ciclo ReAct con Tools y Guardrails
=============================================

                ┌────────────────┐
                │ Input: Perfil  │
                │ del usuario    │
                └────────┬───────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │      STATE MACHINE             │
        │  (con Guardrails enforced)     │
        └────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Thought 1  │  │  Thought 2  │  │  Thought 3  │
│  "Analizar" │  │  "Generar"  │  │  "Auditar"  │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Action:    │  │  Action:    │  │  Action:    │
│  ANALIZAR_  │  │  GENERAR_   │  │  AUDITAR_   │
│  PERFIL     │  │  MENSAJE    │  │  RESPETO    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│Observation: │  │Observation: │  │Observation: │
│ insights    │  │ draft msg   │  │ audit ok    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┴────────────────┘
                         │
                         ▼
                ┌────────────────┐
                │  FINAL_ANSWER  │
                │  con mensaje   │
                │  validado      │
                └────────────────┘

CONCEPTO FUNDAMENTAL: ReAct Pattern
====================================
ReAct = Reasoning + Acting
Un patrón donde el agente alterna entre razonar (Thought) y actuar (Action),
observando resultados (Observation) antes del siguiente ciclo.

CICLO ReAct:
1. THOUGHT → "Necesito analizar el perfil primero"
2. ACTION → Llama tool_analizar_perfil(profile)
3. OBSERVATION → {"persona": "...", "insights": [...]}
4. THOUGHT → "Ahora puedo generar mensaje basado en insights"
5. ACTION → Llama GENERAR_MENSAJE con análisis
6. OBSERVATION → {"opener": "...", "follow_up": "..."}
7. ... continúa hasta FINAL_ANSWER

¿POR QUÉ REACT? (vs CoT simple)
================================
CoT: Razonamiento lineal sin herramientas
- Input → Razonamiento visible → Output
- No puede consultar APIs, bases de datos, o hacer cómputos externos
- Limitado a conocimiento del modelo

ReAct: Razonamiento + Herramientas
- Input → [Thought → Action → Observation]* → Output
- Puede usar herramientas (APIs, DBs, validadores, etc.)
- Extiende capacidades del modelo con código/datos externos
- Cada observación informa el siguiente pensamiento

ARQUITECTURA ReAct (3 componentes clave):
==========================================

1. TOOLS (Herramientas con contratos explícitos)
   ================================================
   - tool_analizar_perfil (lines 21-30): Extrae insights de perfil
     * Input: dict con tipo_persona, gustos, estilo, contexto
     * Output: dict con persona, estilo_preferido, insights
     * Propósito: Dar al agente "comprensión" estructurada del perfil

   - tool_auditar_respeto (lines 33-41): Valida ética/respeto
     * Input: string (mensaje a auditar)
     * Output: dict con ok (bool), flags (lista), suggestion
     * Propósito: Guardrail de seguridad antes de enviar output

   PRINCIPIO DE DISEÑO DE TOOLS:
   - Función pura: mismo input → mismo output
   - No side effects (no escribe archivos, no muta estado global)
   - Validación de input explícita
   - Output estructurado (dict/Pydantic en producción)
   - Documentación clara de contrato (ver docstrings abajo)

2. AGENT LOOP (Ciclo Thought → Action → Observation)
   ===================================================
   Ver run_react_agent (lines 86-176):
   - State: dict que acumula resultados de tools
   - Loop: hasta 6 iteraciones (previene loops infinitos)
   - model_next_action: modelo decide próxima acción basado en state
   - Ejecuta action, actualiza state, repite

3. GUARDRAILS (Forced protocol enforcement)
   ==========================================
   Ver lines 101-119:
   - State machine esperado: ANALIZAR → GENERAR → AUDITAR → FINAL
   - Si agent intenta saltar pasos: override forzado
   - Trace logging de overrides para debugging
   - Propósito: Evitar agent drift (comportamiento impredecible)

GUARDRAILS RATIONALE (¿por qué forced protocol?):
==================================================
PROBLEMA SIN GUARDRAILS:
- Agent puede saltar directamente a FINAL_ANSWER sin análisis
- Agent puede auditar antes de generar mensaje (orden incorrecto)
- Agent puede entrar en loops infinitos (ej: re-analizar perpetuamente)
- Comportamiento impredecible dificulta debugging

SOLUCIÓN CON GUARDRAILS:
- Validamos que el estado actual permita la acción elegida
- Si no: sobreescribimos acción con la esperada
- Trackeamos overrides para diagnóstico (ver state["trace"])
- Logs muestran cuándo el modelo intenta desviarse

TRADE-OFF: Autonomía vs Predictibilidad
- Sin guardrails: Más "autonomía", menos predecible, difícil debuggear
- Con guardrails: Menos autonomía, más predecible, fácil mantener
- En producción: SIEMPRE elige predictibilidad > autonomía creativa

TOOL CONTRACTS (Contratos explícitos):
=======================================
Cada tool es un contrato:
- Input definido (tipos, campos requeridos)
- Output definido (estructura JSON fija)
- Comportamiento determinístico
- Sin side effects ocultos

En producción: usar Pydantic para tool I/O validation
Ver PYDANTIC_GUIDE.md y 03_react_agente_pydantic.py

CONTEXT DEPENDENCY CRÍTICO:
============================
ESTO ES ESENCIAL: Tools AMPLIFICAN la calidad del contexto.
- Profile rico → tool_analizar_perfil extrae insights valiosos → mensaje personalizado
- Profile pobre → tool extrae insights genéricos → mensaje genérico

ReAct NO convierte mal contexto en buen output.
ReAct amplifica señales. Basura in = basura out (GIGO).

CUÁNDO USAR REACT (vs CoT simple):
===================================
 Usar ReAct cuando:
- Necesitas consultar herramientas/APIs/DBs externas
- Necesitas validación/auditoría multi-paso
- Necesitas state accumulation (resultado de tool informa siguiente acción)
- Necesitas debugging granular del proceso de razonamiento

 NO usar ReAct cuando:
- Tarea resolvible con un solo LLM call (overhead innecesario)
- No tienes herramientas externas que añadan valor
- Latencia es crítica (ReAct = múltiples API calls)
- Presupuesto muy limitado (ReAct = 3-5× costo vs simple CoT)

COMPARACIÓN: CoT vs ReAct
==========================
Ver ReAct/README.md tabla completa (lines 45-60)

Resumen:
- CoT: Razonamiento visible, sin herramientas, 1-2 API calls
- ReAct: Razonamiento + herramientas + ciclo, 3-7 API calls
- CoT: Más barato, más rápido, bueno para razonamiento puro
- ReAct: Más caro, más lento, necesario cuando tools añaden valor

FAILURE MODES (y cómo diagnosticarlos):
========================================
1. Infinite loop: agent no llega a FINAL_ANSWER
   - Diagnóstico: revisar state["trace"], ver qué acción se repite
   - Fix: ajustar guardrails, añadir max_iterations (ya implementado: 6)

2. Wrong tool order: agent audita antes de generar
   - Diagnóstico: trace muestra overrides frecuentes
   - Fix: guardrails forced protocol (ya implementado: lines 101-119)

3. Tool returns unexpected format: crash en parsing
   - Diagnóstico: error en json.loads o KeyError
   - Fix: validar tool output con Pydantic (ver 03_react_agente_pydantic.py)

4. Agent ignora tool results: genera mensaje sin usar analysis
   - Diagnóstico: comparar state["analysis"] con draft_message
   - Fix: hacer analysis más explícito en prompt de GENERAR_MENSAJE

5. Tool contract violated: input mal formado
   - Diagnóstico: error en tool execution
   - Fix: validar input con Pydantic BaseModel

6. State accumulation error: state no se actualiza correctamente
   - Diagnóstico: trace muestra action pero state no cambia
   - Fix: revisar lógica de actualización de state (lines 123-158)

Ver ReAct/README.md (lines 95-130) para análisis completo de failure modes.

LIMITACIONES CRÍTICAS:
======================
1. ReAct NO es "inteligencia real" - sigue siendo LLM con tools
2. Costo 3-5× más alto que CoT simple (múltiples API calls)
3. Latencia 3-5× más alta (llamadas secuenciales, no paralelas)
4. Requiere tools bien diseñados (garbage tools = garbage output)
5. State management complejo (bugs más difíciles de diagnosticar)
6. No garantiza corrección (puede ejecutar tools en orden subóptimo)

MAPEO A ESTRUCTURA DE 5 CAPAS (ver README principal):
======================================================
1. ROLE: Lines 45-49 - Agente ReAct con acciones válidas
2. TASK: Lines 51-68 - Decidir próxima acción basado en state
3. OUTPUT FORMAT: Lines 55-61 - JSON con thought, action, action_input
4. EXAMPLES: No (este es zero-shot)
5. CONTEXT: Lines 52-53 - Estado actual del agente

Para versión tipo-segura con Pydantic: 03_react_agente_pydantic.py
Para few-shot con traces: 02_react_personas_feedback_loop.py
Para guía completa de Pydantic: ../PYDANTIC_GUIDE.md
"""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


def get_client_and_model() -> tuple[OpenAI, str]:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no está definida en el archivo .env")
    return OpenAI(api_key=api_key), os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def tool_analizar_perfil(profile: dict[str, Any]) -> dict[str, Any]:
    """
    TOOL CONTRACT: Analiza perfil y extrae insights accionables.

    PROPÓSITO:
    - Dar al agente "comprensión" estructurada del perfil
    - Extraer señales accionables que informen la generación de mensajes
    - Reducir complejidad del perfil crudo a insights digeribles

    DISEÑO ACTUAL (simplificado para pedagogía):
    - Concatena gustos → insight sobre intereses
    - Sugiere estrategia general (apertura breve + pregunta)

    PRODUCCIÓN REAL (más sofisticado):
    - Analizar correlaciones entre gustos (ej: café + jazz → probablemente bohemio)
    - Detectar keywords indicadores de personalidad (ej: "datos" → analítico)
    - Scoring de compatibilidad con estrategias conversacionales
    - Usar embeddings/ML para inferir estilo conversacional preferido

    PRINCIPIOS DE DISEÑO:
    - Función pura: mismo input → mismo output
    - No side effects (no API calls, no estado global)
    - Output estructurado (dict con campos fijos)
    - En producción: usar Pydantic ProfileAnalysis model

    CONTEXT DEPENDENCY:
    Este tool AMPLIFICA la calidad del profile.
    - Profile rico (gustos específicos, estilo claro) → insights valiosos
    - Profile pobre (genérico, vago) → insights genéricos
    - GIGO (Garbage In, Garbage Out) aplica estrictamente

    Args:
        profile: Dict con tipo_persona, gustos (lista), estilo, contexto

    Returns:
        Dict con:
        - persona: string, tipo de persona
        - estilo_preferido: string, estilo conversacional
        - insights: lista de strings con observaciones accionables

    Ver 03_react_agente_pydantic.py para versión tipo-segura.
    """
    gustos = ", ".join(profile.get("gustos", []))
    return {
        "persona": profile.get("tipo_persona", "desconocida"),
        "estilo_preferido": profile.get("estilo", "cálido"),
        "insights": [
            f"Intereses detectados: {gustos}",
            "Conviene una apertura breve con pregunta auténtica.",
        ],
    }


def tool_auditar_respeto(message: str) -> dict[str, Any]:
    """
    TOOL CONTRACT: Audita mensaje para validar respeto y ausencia de presión.

    PROPÓSITO:
    - Guardrail de seguridad antes de enviar output al usuario
    - Prevenir lenguaje inapropiado, presionante, o invasivo
    - Asegurar alineación con valores éticos (consentimiento, respeto)

    DISEÑO ACTUAL (keyword matching simplificado):
    - Lista de keywords prohibidos: ["presión", "insistir", "explícito"]
    - Busca coincidencias case-insensitive
    - Si encuentra flags: ok=False

    PRODUCCIÓN REAL (más robusto):
    - Clasificador ML entrenado en ejemplos de lenguaje inapropiado
    - Análisis semántico (no solo keywords, también contexto)
    - Scoring continuo 0-1 (no solo binario ok/not ok)
    - Integración con moderación API de OpenAI
    - Logging de casos edge para mejora continua

    LIMITACIONES DEL APPROACH ACTUAL:
    - Keyword matching es frágil (ej: "sin presión" contiene "presión")
    - No detecta sarcasmo o ironía
    - No detecta presión implícita (ej: "sería una pena si no...")
    - Lista corta de keywords (producción necesita 100+)

    MEJORAS RECOMENDADAS:
    - Usar regex para match de palabras completas (evita falsos positivos)
    - Añadir análisis de sentimiento (detectar tono agresivo)
    - Whitelist de frases seguras que contienen keywords (ej: "sin presión")
    - A/B testing para validar que auditoría mejora calidad percibida

    PRINCIPIOS DE DISEÑO:
    - Función pura: mismo input → mismo output
    - No side effects
    - Fail-safe: en caso de duda, rechazar (ok=False)
    - En producción: usar Pydantic AuditResult model

    Args:
        message: String, mensaje completo a auditar (opener + follow_up)

    Returns:
        Dict con:
        - ok: bool, True si pasa auditoría
        - flags: lista de keywords problemáticos encontrados
        - suggestion: string, sugerencia de mejora

    Ver 03_react_agente_pydantic.py para versión tipo-segura.
    """
    # LISTA DE KEYWORDS PROHIBIDOS (simplificado para pedagogía)
    # En producción: expandir a 100+ keywords + regex patterns
    banned = ["presión", "insistir", "explícito"]
    lowered = message.lower()
    flags = [token for token in banned if token in lowered]

    return {
        "ok": len(flags) == 0,
        "flags": flags,
        "suggestion": "Mantén tono amable, no invasivo y con salida elegante.",
    }


def model_next_action(client: OpenAI, model: str, state: dict[str, Any]) -> dict[str, Any]:
    system_prompt = (
        "Eres un agente ReAct. Debes decidir una acción por turno. "
        "Acciones válidas: ANALIZAR_PERFIL, GENERAR_MENSAJE, AUDITAR_RESPETO, FINAL_ANSWER. "
        "Responde SIEMPRE en JSON."
    )

    user_prompt = f"""
Estado actual del agente:
{json.dumps(state, ensure_ascii=False, indent=2)}

Devuelve JSON:
{{
  "thought": "razonamiento breve",
  "action": "ANALIZAR_PERFIL|GENERAR_MENSAJE|AUDITAR_RESPETO|FINAL_ANSWER",
  "action_input": {{...}},
  "final_answer": {{}}
}}

Reglas:
- Usa primero ANALIZAR_PERFIL.
- Luego GENERAR_MENSAJE.
- Luego AUDITAR_RESPETO.
- Si ya está auditado y está OK, usa FINAL_ANSWER.
""".strip()

    completion = client.chat.completions.create(
        model=model,
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("El modelo devolvió contenido vacío")
    return json.loads(content)


def run_react_agent(client: OpenAI, model: str, profile: dict[str, Any]) -> dict[str, Any]:
    state: dict[str, Any] = {
        "profile": profile,
        "analysis": None,
        "draft_message": None,
        "audit": None,
        "trace": [],
    }

    for _ in range(6):
        step = model_next_action(client, model, state)
        action = step.get("action")
        thought = step.get("thought", "")
        action_input = step.get("action_input", {})

        if state["analysis"] is None:
            expected_action = "ANALIZAR_PERFIL"
        elif state["draft_message"] is None:
            expected_action = "GENERAR_MENSAJE"
        elif state["audit"] is None:
            expected_action = "AUDITAR_RESPETO"
        else:
            expected_action = "FINAL_ANSWER"

        if action != expected_action:
            state["trace"].append(
                {
                    "thought": thought,
                    "action": action,
                    "action_input": action_input,
                    "override": f"Se fuerza {expected_action} para mantener el protocolo ReAct.",
                }
            )
            action = expected_action
        else:
            state["trace"].append({"thought": thought, "action": action, "action_input": action_input})

        if action == "ANALIZAR_PERFIL":
            state["analysis"] = tool_analizar_perfil(state["profile"])

        elif action == "GENERAR_MENSAJE":
            completion = client.chat.completions.create(
                model=model,
                temperature=0.7,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Genera un mensaje coqueto, respetuoso y breve. "
                            "Evita presión y frases explícitas."
                        ),
                    },
                    {
                        "role": "user",
                        "content": json.dumps(
                            {
                                "profile": state["profile"],
                                "analysis": state["analysis"],
                                "instruction": "Devuelve opener y follow_up en JSON.",
                            },
                            ensure_ascii=False,
                        ),
                    },
                ],
            )
            content = completion.choices[0].message.content
            state["draft_message"] = json.loads(content) if content else {}

        elif action == "AUDITAR_RESPETO":
            opener = (state.get("draft_message") or {}).get("opener", "")
            follow_up = (state.get("draft_message") or {}).get("follow_up", "")
            state["audit"] = tool_auditar_respeto(f"{opener} {follow_up}".strip())

        elif action == "FINAL_ANSWER":
            final_answer = step.get("final_answer") or {
                "analysis": state.get("analysis"),
                "message": state.get("draft_message"),
                "audit": state.get("audit"),
            }
            return {"final": final_answer, "trace": state["trace"]}

    return {
        "final": {
            "analysis": state.get("analysis"),
            "message": state.get("draft_message"),
            "audit": state.get("audit"),
            "note": "Se alcanzó el máximo de iteraciones.",
        },
        "trace": state["trace"],
    }


def main() -> None:
    """
    Ejecuta ejemplos de ReAct agent con perfiles diversos.

    DEMOSTRACIÓN DEL PATRÓN ReAct:
    ===============================
    Este ejemplo muestra el ciclo completo:
    1. ANALIZAR_PERFIL → extrae insights
    2. GENERAR_MENSAJE → usa insights para personalizar
    3. AUDITAR_RESPETO → valida seguridad
    4. FINAL_ANSWER → retorna resultado

    PERFILES PEDAGÓGICOS ELEGIDOS:
    ===============================
    Cada perfil demuestra cómo el contexto determina el razonamiento y las acciones.

    PERFIL 1: Neurocientífica curiosa (científica con lado artístico)
    - Señales: sueño + documentales BBC + yoga aéreo → mente analítica + busca equilibrio
    - Estilo esperado: Pregunta basada en evidencia, humor sutil
    - Demuestra: Cómo profile intelectual → opener con sustancia

    PERFIL 2: Sommelier con lado nerd (creativo ecléctico)
    - Señales: vinos naturales + cómics + speakeasy → contraste interesante
    - Estilo esperado: Lúdico, aprecia sorpresa y originalidad
    - Demuestra: Cómo profile ecléctico → opener que celebra contraste

    PERFIL 3: Data scientist aventurera (analítica + outdoor)
    - Señales: biotech + trail running + Lex Fridman → desafíos + métricas
    - Estilo esperado: Analítico pero aventurero
    - Demuestra: Cómo combinar señales aparentemente contradictorias

    OBSERVA EN OUTPUTS:
    ===================
    - ¿El trace muestra ciclo Thought → Action → Observation?
    - ¿Los insights del análisis se usan en el mensaje?
    - ¿La auditoría detecta problemas (si los hay)?
    - ¿Hubo overrides (agent intentó saltarse protocolo)?
    """
    client, model = get_client_and_model()

    # PERFIL 1: Neurocientífica especializada en sueño
    # =================================================
    # Señales accionables:
    # - "neurocientífica especializada en sueño" → mente analítica, curiosa por patrones
    # - "documentales BBC" → aprecia calidad, profundidad, evidencia
    # - "yoga aéreo" → busca equilibrio, experimenta con cuerpo/mente
    # - "cafés silenciosos para leer" → necesita espacios tranquilos, introspectiva
    # - "valora profundidad y evidencia, humor sutil" → conversación intelectual con ligereza
    # Estilo esperado: Pregunta basada en curiosidad científica, tono respetuoso e inteligente
    profile_1 = {
        "tipo_persona": "neurocientífica especializada en sueño",
        "gustos": ["documentales BBC", "yoga aéreo", "cafés silenciosos para leer"],
        "estilo": "curiosa, valora profundidad y evidencia, humor sutil",
        "contexto": "match tras leer biografía completa, ella mencionó paper tuyo",
    }

    # PERFIL 2: Sommelier con lado nerd de cómics
    # ============================================
    # Señales accionables:
    # - "sommelier" → conocimiento profundo de vinos, paladar refinado
    # - "vinos naturales" → valora autenticidad, proceso artesanal
    # - "convenciones de cómic" → nerd orgulloso, aprecia cultura pop
    # - "bares speakeasy" → disfruta experiencias únicas, algo ocultas
    # - "ecléctico, aprecia sorpresa y contraste" → celebra contradicciones interesantes
    # Estilo esperado: Lúdico, referencia al contraste vinos/cómics, invita a compartir pasiones
    profile_2 = {
        "tipo_persona": "sommelier con lado nerd de cómics vintage",
        "gustos": ["vinos naturales", "convenciones de cómic", "bares speakeasy"],
        "estilo": "ecléctico, aprecia sorpresa y contraste, conversación lúdica",
        "contexto": "second date coordinándose, ya hay rapport establecido",
    }

    # PERFIL 3: Data scientist en biotech con pasión por trail running
    # =================================================================
    # Señales accionables:
    # - "data scientist en biotech" → analítica, trabaja con datos complejos
    # - "kaggle competitions" → competitiva, disfruta desafíos intelectuales
    # - "ultra maratones" → resistencia física/mental, objetivos ambiciosos
    # - "podcasts de Lex Fridman" → curiosidad intelectual, conversaciones profundas
    # - "analítico pero aventurero, aprecia desafíos y métricas" → balance mente/cuerpo
    # Estilo esperado: Pregunta que combine analítica + aventura, métricas/objetivos
    profile_3 = {
        "tipo_persona": "data scientist en biotech con pasión por trail running",
        "gustos": ["kaggle competitions", "ultra maratones", "podcasts de Lex Fridman"],
        "estilo": "analítico pero aventurero, aprecia desafíos y métricas",
        "contexto": "ya se saludaron, buscando tema para profundizar",
    }

    # Ejecutar ReAct agent para cada perfil
    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN: ReAct Agent con ciclo Thought → Action → Observation")
    print("=" * 80)

    for i, profile in enumerate([profile_1, profile_2, profile_3], 1):
        print(f"\n{'=' * 80}")
        print(f"PERFIL {i}: {profile['tipo_persona']}")
        print(f"{'=' * 80}")
        print(f"Gustos: {', '.join(profile['gustos'])}")
        print(f"Estilo: {profile['estilo']}")
        print(f"Contexto: {profile['contexto']}")
        print(f"\n{'─' * 80}")
        print("EJECUTANDO REACT AGENT...")
        print(f"{'─' * 80}")

        result = run_react_agent(client, model, profile)

        print("\n=== RESULTADO FINAL ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    print(f"\n{'=' * 80}")
    print("ANÁLISIS PEDAGÓGICO:")
    print("=" * 80)
    print("1. ¿El trace muestra ciclo Thought → Action → Observation claramente?")
    print("2. ¿Los insights del análisis se reflejan en el mensaje generado?")
    print("3. ¿La auditoría detectó problemas? (flags debería estar vacío)")
    print("4. ¿Hubo overrides? (agent intentó saltarse el protocolo)")
    print("5. ¿El mensaje es personalizado según señales del perfil?")
    print("=" * 80)


if __name__ == "__main__":
    main()
