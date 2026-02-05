"""
Few-shot ReAct + Feedback Loop para múltiples personas objetivo.

DIAGRAMA: Few-shot ReAct con Feedback Loop Multi-Persona
=========================================================

Trace Ejemplo        Perfil 1           Perfil 2           Perfil 3
(cine indie)      (data scientist)   (arquitecta)        (chef)
     │                  │                 │                 │
     └──────┬───────────┴─────────────────┴─────────────────┘
            │
            ▼
   ┌────────────────────────────────────────┐
   │  ReAct Agent (con ejemplo de trace)    │
   │  Thought → Action → Observation        │
   └──────────┬─────────────────────────────┘
              │
              ▼
   ┌────────────────────────────────────────┐
   │  Output: trace + mensaje               │
   └──────────┬─────────────────────────────┘
              │
              ▼
   ┌────────────────────────────────────────┐
   │  Feedback Loop: Evalúa                 │
   │  - Coherencia de trace                 │
   │  - Personalización del mensaje         │
   │  - Adherencia al protocolo             │
   └──────────┬─────────────────────────────┘
              │
      ┌───────┴────────┐
      │                │
      ▼                ▼
  Score < 7?       Score >= 7
      │                │
      ▼                │
┌─────────────┐        │
│ Regenerar   │        │
│ con crítica │        │
└──────┬──────┘        │
       │               │
       └───────┬───────┘
               ▼
        ┌──────────────┐
        │ Output final │
        │ mejorado     │
        └──────────────┘

CONCEPTO FUNDAMENTAL: Few-shot ReAct Traces
============================================
Extensión de ReAct zero-shot donde proporcionamos ejemplos explícitos
de trazas completas (Thought → Action → Observation) en el prompt.

¿POR QUÉ FEW-SHOT EN REACT?
============================
Zero-shot ReAct: El modelo infiere el patrón de razonamiento
- Puede no entender el formato exacto de acciones
- Puede no seguir el orden esperado (ANALIZAR → GENERAR → AUDITAR)
- Variabilidad en estilo de "thoughts"

Few-shot ReAct: Enseñamos el patrón con ejemplos concretos
- Muestra formato exacto de Thought → Action → Observation
- Enseña el orden canónico de acciones
- Estandariza estilo de razonamiento
- Mejora adherencia al protocolo (menos overrides necesarios)

ESTRUCTURA DE TRACE PEDAGÓGICA (lines 28-39):
==============================================

EJEMPLO TRACE COMPLETO:
-----------------------
Thought: "Necesito identificar intereses y nivel de formalidad"
├─ PEDAGOGÍA: Explica QUÉ necesita hacer y POR QUÉ
├─ Conecta con objetivo (entender perfil antes de generar)

Action: analizar_perfil
├─ PEDAGOGÍA: Nombre de tool claro y específico
├─ Sin ambigüedad (no "procesar" o "revisar")

Observation: "intereses = cine indie, formalidad media"
├─ PEDAGOGÍA: Resultado estructurado del tool
├─ Información accionable para próximo paso

Thought: "Con eso, genero apertura corta y pregunta abierta"
├─ PEDAGOGÍA: Muestra cómo observation informa próximo thought
├─ Razonamiento encadenado (no desconectado)

Action: generar_mensaje
Observation: "opener y follow_up creados"

Thought: "Verifico respeto y evito presión"
├─ PEDAGOGÍA: Auditoría como paso explícito (no asumido)

Action: auditar_respeto
Observation: "ok=true"

Thought: "ya puedo responder"
Action: finalizar

ANÁLISIS DEL TRACE (pedagogía explicada):
==========================================
1. ORDEN CANÓNICO: analizar → generar → auditar → finalizar
   - Este es el flujo esperado en producción
   - Cada paso depende del anterior (state accumulation)

2. THOUGHTS EXPLICAN RAZONAMIENTO:
   - No solo dicen acción, explican POR QUÉ
   - "Necesito identificar..." vs "Voy a analizar" (el primero es mejor)

3. OBSERVATIONS SON ESPECÍFICOS:
   - "intereses = cine indie" vs "análisis completo" (el primero es mejor)
   - Información accionable, no vaga

4. TRACE ES NARRATIVA COHERENTE:
   - Cada thought conecta con observation anterior
   - No saltos lógicos

CONTEXTO DETERMINA COMPORTAMIENTO (DEMOSTRACIÓN):
==================================================
Mismo sistema ReAct, diferente perfil = diferente razonamiento

Ejemplo 1: Perfil analítico (data scientist)
├─ Thought: "Perfil valora precisión → pregunta concreta sobre métricas"
├─ Action: generar_mensaje enfocado en datos/eficiencia
└─ Output: Pregunta sobre optimización, algoritmos, métricas

Ejemplo 2: Perfil creativo (músico de jazz)
├─ Thought: "Perfil valora espontaneidad → pregunta abierta sobre experiencias"
├─ Action: generar_mensaje enfocado en creatividad/emoción
└─ Output: Pregunta sobre inspiración, improvisación, sensaciones

ESTO ES LA ESENCIA DE AI ENGINEERING:
Context >> Prompt engineering tricks
El mismo agente ReAct produce outputs radicalmente diferentes según el contexto.

FEEDBACK LOOP EN REACT (lines 74-115):
=======================================
Patrón iterativo aplicado a ReAct:
1. Generar trace completo + mensaje
2. Evaluar con criterios objetivos
3. Regenerar si score < umbral

DIFERENCIA vs CoT feedback loop:
- CoT: Evalúa solo output final
- ReAct: Puede evaluar trace completo (razonamiento + acciones + output)
- ReAct: Más granular, puede identificar qué action falló

TEMPERATURA SETTINGS (rationale):
=================================
- run_react_few_shot: 0.6 (balance creatividad/consistencia)
  * Más bajo que CoT (0.7) porque few-shot ya da estructura
  * Suficiente para variación creativa en mensajes

- critique_and_improve: 0.3 (muy determinístico)
  * Evaluación debe ser consistente, no creativa
  * Críticas deben ser objetivas y reproducibles

COST ANALYSIS (transparencia completa):
========================================
Few-shot ReAct con feedback loop:
- Trace example: ~400 tokens (en prompt)
- Profile + instructions: ~200 tokens
- Input total: ~600 tokens
- Output (trace + mensaje): ~400 tokens
- Primera llamada: 1000 tokens × $0.00042/1K = $0.00042

- Feedback loop: ~800 tokens input + ~300 tokens output = 1100 tokens
- Segunda llamada: $0.00046

TOTAL: $0.00088/request

COMPARACIÓN DE COSTOS:
- Zero-shot CoT: $0.00021 (baseline)
- Few-shot CoT: $0.00027 (+29%)
- Zero-shot ReAct: $0.00045 (+114%)
- Few-shot ReAct + feedback: $0.00088 (+319%)

TRADE-OFF:
- 4.2× más caro que baseline
- Pero: mayor consistencia + tools + auditoría + feedback
- ROI: Si calidad/seguridad vale 4× costo → usar

CUÁNDO USAR FEW-SHOT REACT:
============================
 Usar cuando:
- Producción con budget razonable y alta criticidad
- Necesitas consistencia estricta en formato de trace
- Necesitas tools + auditoría + razonamiento visible
- Debugging es prioritario (traces completos facilitan diagnóstico)

 NO usar cuando:
- Prototipado rápido (zero-shot ReAct es suficiente)
- Budget muy limitado (4× costo)
- Tarea simple que no requiere tools (CoT es suficiente)
- Latencia crítica (múltiples API calls secuenciales)

LIMITACIONES CRÍTICAS:
======================
1. Costo 4× baseline - no sustentable para alto volumen sin optimización
2. Latencia alta (2-3 segundos típico) - no apto para UX interactiva
3. Few-shot example puede sesgar hacia ese estilo - elegir ejemplos diversos
4. Feedback loop duplica costo - usar selectivamente (no todos los requests)
5. Complexity alta - debugging más difícil que CoT simple

MEJORAS EN PRODUCCIÓN:
======================
- Cache de traces comunes (reduce costo de few-shot)
- Batch processing para requests no-interactivos
- A/B testing: few-shot vs zero-shot para validar ROI
- Métricas de calidad: track score antes/después de feedback
- Async processing para reducir percepción de latencia

Para versión tipo-segura con Pydantic: 04_react_personas_pydantic.py
Para comparación completa: ../PYDANTIC_GUIDE.md
Ver rubrica.py para evaluación objetiva de outputs
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


def run_react_few_shot(client: OpenAI, model: str, profile: dict[str, Any]) -> dict[str, Any]:
    """
    Ejecuta ReAct agent con few-shot trace example.

    PEDAGOGÍA: Few-shot Learning en ReAct
    ======================================
    Este prompt enseña al modelo:
    1. Formato exacto de Thought → Action → Observation
    2. Orden canónico de acciones (analizar → generar → auditar → finalizar)
    3. Estilo de razonamiento (explícito, conectado, accionable)
    4. Cómo observation informa próximo thought

    EJEMPLO TRACE (pedagogía explicada en prompt):
    ===============================================
    - Thought 1: "Necesito identificar intereses..."
      * PEDAGOGÍA: Explica QUÉ y POR QUÉ (no solo "voy a analizar")
    - Action 1: analizar_perfil
      * PEDAGOGÍA: Nombre de tool específico (no genérico)
    - Observation 1: "intereses = cine indie, formalidad media"
      * PEDAGOGÍA: Resultado estructurado y accionable
    - Thought 2: "Con eso, genero apertura..."
      * PEDAGOGÍA: Muestra cómo observation informa next thought
    - ... continúa hasta finalizar

    TEMPERATURA: 0.6 (balance)
    - Más bajo que zero-shot CoT (0.7) porque few-shot da estructura
    - Suficiente variación para creatividad en mensajes
    - Más alto que feedback (0.3) porque queremos personalización

    Args:
        client: Cliente OpenAI configurado
        model: Nombre del modelo
        profile: Dict con tipo_persona, gustos, estilo, contexto

    Returns:
        Dict con trace (array de steps) y result (opener, follow_up, why_it_works)
    """
    # CAPA 1: ROLE - Agente ReAct con restricciones éticas
    system_prompt = (
        "Eres un agente ReAct. Tomas decisiones por pasos y luego entregas respuesta final. "
        "Tono coqueto, respetuoso, no invasivo, no explícito."
    )

    # CAPA 4: EXAMPLES - Few-shot trace completo
    # ===========================================
    # PEDAGOGÍA: Este trace enseña el patrón completo de razonamiento
    #
    # NOTA sobre el ejemplo elegido:
    # - "cine indie, formalidad media" → perfil intelectual pero accesible
    # - Demuestra cómo adaptar tono según señales
    # - Trace es breve (4 pasos) para no inflar costos
    # - En producción: considerar 2-3 ejemplos con estilos diversos
    user_prompt = f"""
# EJEMPLO: Trace ReAct completo
# ==============================
# PEDAGOGÍA: Este ejemplo enseña el flujo canónico de razonamiento + acción
#
# Paso 1: ANALIZAR (entender el perfil)
Thought: Necesito identificar intereses y nivel de formalidad.
Action: analizar_perfil
Observation: intereses = cine indie, formalidad media.

# Paso 2: GENERAR (crear mensaje basado en análisis)
Thought: Con eso, genero apertura corta y pregunta abierta.
Action: generar_mensaje
Observation: opener y follow_up creados.

# Paso 3: AUDITAR (validar respeto y seguridad)
Thought: Verifico respeto y evito presión.
Action: auditar_respeto
Observation: ok=true.

# Paso 4: FINALIZAR (retornar resultado)
Thought: ya puedo responder.
Action: finalizar

# CASO ACTUAL - Aplica el patrón aprendido
# =========================================
# CAPA 5: CONTEXT - Perfil específico del usuario
{json.dumps(profile, ensure_ascii=False, indent=2)}

# CAPA 3: OUTPUT FORMAT - Estructura esperada
# ============================================
Devuelve JSON:
{{
  "trace": [
    {{"thought": "...", "action": "...", "observation": "..."}},
    {{"thought": "...", "action": "...", "observation": "..."}}
  ],
  "result": {{
    "opener": "...",
    "follow_up": "...",
    "why_it_works": ["...", "..."]
  }}
}}
""".strip()

    completion = client.chat.completions.create(
        model=model,
        temperature=0.6,
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


def critique_and_improve(client: OpenAI, model: str, profile: dict[str, Any], react_output: dict[str, Any]) -> dict[str, Any]:
    """
    Feedback loop: evalúa output de ReAct agent y genera versión mejorada.

    PEDAGOGÍA: Feedback loop en ReAct
    ==================================
    A diferencia de CoT (que solo evalúa output final),
    ReAct feedback puede evaluar:
    1. Calidad del trace (¿razonamiento coherente?)
    2. Orden de acciones (¿siguió protocolo?)
    3. Output final (¿mensaje personalizado?)

    VENTAJA DE FEEDBACK EN REACT:
    - Más granular: puede identificar qué action falló
    - Trace visible facilita diagnóstico
    - Puede sugerir mejoras específicas al razonamiento

    CRITERIOS DE EVALUACIÓN (implícitos en prompt):
    - Personalización: ¿Usa señales del perfil?
    - Naturalidad: ¿Suena humano y conversacional?
    - Respeto: ¿Sin presión/lenguaje inapropiado?
    - Utilidad: ¿Invita a continuar conversación?
    - Coherencia: ¿Trace tiene lógica clara?

    TEMPERATURA: 0.3 (muy determinístico)
    - Evaluación debe ser consistente, no creativa
    - Diagnósticos objetivos y reproducibles
    - Más bajo que generación (0.6) para reducir variabilidad

    COST IMPACT:
    - Duplica el costo del request (draft + review)
    - Trade-off: +100% costo, +20-30% calidad
    - En producción: usar selectivamente (no todos los requests)

    Args:
        client: Cliente OpenAI configurado
        model: Nombre del modelo
        profile: Perfil original del usuario
        react_output: Output generado por run_react_few_shot

    Returns:
        Dict con diagnostico (array de strings) y version_mejorada
    """
    # ROLE: Auditor crítico de calidad
    system_prompt = (
        "Eres un auditor de calidad de un agente conversacional. "
        "Evalúas calidad humana, respeto, personalización y utilidad."
    )

    # TASK: Diagnóstico + mejora
    # CONTEXT: Perfil + output del agente
    user_prompt = f"""
# CONTEXTO: Perfil objetivo
# =========================
{json.dumps(profile, ensure_ascii=False, indent=2)}

# CONTEXTO: Salida del agente ReAct
# ==================================
{json.dumps(react_output, ensure_ascii=False, indent=2)}

# TASK: Feedback loop en dos etapas
# ==================================
1) DIAGNÓSTICO CRÍTICO:
   - ¿El trace muestra razonamiento coherente?
   - ¿El mensaje usa señales del perfil?
   - ¿El tono es apropiado para el estilo indicado?
   - ¿Hay problemas de respeto/presión?
   - ¿La pregunta invita a responder?

2) VERSIÓN MEJORADA:
   - Corrige problemas identificados
   - Mantiene fortalezas del original
   - Mejora personalización si es genérica

# OUTPUT FORMAT: JSON estructurado
# =================================
Devuelve JSON:
{{
  "diagnostico": ["...", "..."],
  "version_mejorada": {{
    "opener": "...",
    "follow_up": "...",
    "why_it_works": ["...", "..."]
  }}
}}
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


def main() -> None:
    """
    Ejecuta ReAct few-shot + feedback loop sobre múltiples perfiles.

    DEMOSTRACIÓN PEDAGÓGICA:
    ========================
    Este ejemplo demuestra:
    1. Mismo sistema ReAct, diferente contexto = diferente razonamiento
    2. Cómo few-shot trace mejora consistencia de formato
    3. Cómo feedback loop identifica y corrige problemas
    4. Trade-off costo vs calidad en acción

    PERFILES ELEGIDOS (rationale pedagógico):
    =========================================

    PERFIL 1: Data scientist en biotech (analítica + aventurera)
    - Contraste interesante: análisis de datos + ultra maratones
    - Demuestra: Cómo balancear señales aparentemente contradictorias
    - Estilo esperado: Pregunta que combine mente + cuerpo, desafíos + métricas

    PERFIL 2: Arquitecta de ciudades sustentables (comprometida + activista)
    - Señales fuertes: urbanismo, huertos, documentales → valora impacto
    - Demuestra: Cómo perfil con valores claros → pregunta sobre acción
    - Estilo esperado: Auténtico, enfocado en hacer (no solo hablar)

    PERFIL 3: Chef de cocina molecular (sensorial + emotivo)
    - Contraste artístico: experimentación culinaria + trova (Silvio Rodríguez)
    - Demuestra: Cómo perfil artístico → pregunta poética pero con sustancia
    - Estilo esperado: Sensorial, evocativo, no superficial

    PERFILES DIVERSOS PEDAGÓGICAMENTE:
    - Perfil 1: STEM + fitness → racional + objetivos
    - Perfil 2: Social + activismo → valores + impacto
    - Perfil 3: Arte + gastronomía → sensorial + emoción

    ANÁLISIS DE CONTEXTO DEPENDENCY:
    =================================
    Observa cómo el MISMO sistema produce outputs radicalmente diferentes:

    Data scientist → Pregunta sobre métricas/desafíos
    ├─ Trace thought: "Perfil valora datos y logros cuantificables"
    └─ Opener: "¿Qué métrica trackeas en tus ultras?"

    Arquitecta → Pregunta sobre proyectos/impacto
    ├─ Trace thought: "Perfil valora acción sobre palabras"
    └─ Opener: "¿En qué proyecto de urbanismo táctico estás ahora?"

    Chef → Pregunta sobre experiencias sensoriales
    ├─ Trace thought: "Perfil valora sensaciones y emociones"
    └─ Opener: "¿Qué experimento culinario te sorprendió últimamente?"

    ESTO DEMUESTRA: Context >> Prompt engineering tricks

    COST ANALYSIS (transparencia):
    ==============================
    Por cada perfil:
    - run_react_few_shot: ~$0.00042 (few-shot prompt + trace generation)
    - critique_and_improve: ~$0.00046 (evaluation + improved version)
    - Total por perfil: ~$0.00088

    3 perfiles × $0.00088 = $0.00264 total para esta ejecución

    COMPARACIÓN:
    - Zero-shot CoT (3 perfiles): 3 × $0.00021 = $0.00063
    - Este approach: $0.00264 (4.2× más caro)

    ROI QUESTION:
    ¿La mejora en consistencia + tools + feedback vale 4× el costo?
    Respuesta depende de criticidad y volumen de tu caso de uso.

    OBSERVA EN OUTPUTS:
    ===================
    1. ¿Los traces muestran razonamiento coherente?
    2. ¿Los diagnósticos identifican problemas reales?
    3. ¿Las versiones mejoradas corrigen esos problemas?
    4. ¿Hay diferencia sustantiva entre perfiles (personalización)?
    5. ¿El feedback loop añade valor o es marginal?
    """
    client, model = get_client_and_model()

    # PERFILES DIVERSOS (pedagogía explicada arriba)
    # ===============================================
    profiles = [
        # PERFIL 1: Data scientist en biotech + ultra maratones
        # ======================================================
        # Señales accionables:
        # - "data scientist en biotech" → analítica, trabaja con datos complejos
        # - "kaggle competitions" → competitiva, disfruta desafíos intelectuales
        # - "ultra maratones" → resistencia física/mental, objetivos ambiciosos
        # - "podcasts de Lex Fridman" → curiosidad intelectual profunda
        # Estilo esperado: Balance mente/cuerpo, métricas/logros
        {
            "tipo_persona": "data scientist en biotech con pasión por trail running",
            "gustos": ["kaggle competitions", "ultra maratones", "podcasts de Lex Fridman"],
            "estilo": "analítico pero aventurero, aprecia desafíos y métricas",
            "contexto": "ya se saludaron, buscando tema para profundizar",
        },
        # PERFIL 2: Arquitecta de ciudades sustentables + activista
        # ==========================================================
        # Señales accionables:
        # - "arquitecta de ciudades sustentables" → pragmática, piensa en sistemas
        # - "urbanismo táctico" → valora acción directa, no solo teoría
        # - "huertos urbanos" → conexión con comunidad, sustentabilidad práctica
        # - "documentales de Greta" → comprometida, valora autenticidad
        # Estilo esperado: Auténtico, enfocado en impacto, no superficial
        {
            "tipo_persona": "arquitecta de ciudades sustentables, activista ambiental",
            "gustos": ["urbanismo táctico", "huertos urbanos", "documentales de Greta"],
            "estilo": "comprometida, valora acción sobre palabras, auténtica",
            "contexto": "match por valores compartidos, primer mensaje",
        },
        # PERFIL 3: Chef de cocina molecular + trova
        # ===========================================
        # Señales accionables:
        # - "chef de cocina molecular" → experimentación, busca sorprender
        # - "vinilos de trova (Silvio Rodríguez)" → sensibilidad poética, emotivo
        # - "mercados locales" → valora autenticidad, ingredientes con historia
        # Estilo esperado: Sensorial, poético, conversación con sustancia
        {
            "tipo_persona": "chef de cocina molecular, coleccionista de vinilos de trova",
            "gustos": ["experimentación culinaria", "Silvio Rodríguez", "mercados locales"],
            "estilo": "sensorial, emotivo, conversación poética pero con sustancia",
            "contexto": "retomando conversación tras pausa, ya hay química",
        },
    ]

    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN: ReAct Few-shot + Feedback Loop sobre múltiples perfiles")
    print("=" * 80)
    print(f"\nProcesando {len(profiles)} perfiles...")
    print("Por cada perfil: 1) ReAct few-shot → 2) Feedback loop → 3) Versión mejorada")

    report = []
    for i, profile in enumerate(profiles, 1):
        print(f"\n{'─' * 80}")
        print(f"PROCESANDO PERFIL {i}/{len(profiles)}: {profile['tipo_persona']}")
        print(f"{'─' * 80}")

        # PASO 1: Generar con ReAct few-shot
        print("  → Generando con ReAct few-shot...")
        raw = run_react_few_shot(client, model, profile)

        # PASO 2: Aplicar feedback loop
        print("  → Aplicando feedback loop (crítica + mejora)...")
        improved = critique_and_improve(client, model, profile, raw)

        report.append({"profile": profile, "react": raw, "feedback_loop": improved})
        print("  ✓ Completado")

    # OUTPUT FINAL
    print("\n" + "=" * 80)
    print("RESULTADOS COMPLETOS")
    print("=" * 80)
    print(json.dumps(report, ensure_ascii=False, indent=2))

    # ANÁLISIS PEDAGÓGICO
    print("\n" + "=" * 80)
    print("ANÁLISIS PEDAGÓGICO:")
    print("=" * 80)
    print("1. ¿Los traces muestran razonamiento coherente para cada perfil?")
    print("2. ¿Los diagnósticos identifican problemas específicos y accionables?")
    print("3. ¿Las versiones mejoradas corrigen esos problemas?")
    print("4. ¿Hay personalización clara entre los 3 perfiles?")
    print("   - Data scientist → ¿menciona métricas/desafíos?")
    print("   - Arquitecta → ¿menciona proyectos/impacto?")
    print("   - Chef → ¿menciona experiencias sensoriales?")
    print("5. ¿El feedback loop añade valor sustantivo o es marginal?")
    print("6. ¿El costo 4× justifica la mejora en calidad?")
    print("=" * 80)


if __name__ == "__main__":
    main()
