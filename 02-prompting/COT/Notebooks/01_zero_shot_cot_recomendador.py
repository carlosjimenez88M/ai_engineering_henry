"""
Zero-shot Chain of Thought (CoT) aplicado a recomendador de conversaciones.

DIAGRAMA: Flujo Chain of Thought
=================================

┌─────────────────┐
│ Input: Perfil   │
│ del usuario     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Paso 1:         │───▶│ Paso 2:         │───▶│ Paso 3:         │───▶│ Paso 4:         │
│ Señales clave   │    │ Estrategia      │    │ Riesgos a       │    │ Recomendación   │
│ del perfil      │    │ de apertura     │    │ evitar          │    │ final           │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                                                                │
                                                                                ▼
                                                                      ┌──────────────────┐
                                                                      │ Output: JSON     │
                                                                      │ - chain_of_thought│
                                                                      │ - opener         │
                                                                      │ - follow_up      │
                                                                      │ - tone_notes     │
                                                                      │ - avoid          │
                                                                      └──────────────────┘

CONCEPTO FUNDAMENTAL: Chain of Thought
======================================
CoT es una técnica de prompting donde obligamos al modelo a explicitar su razonamiento
en pasos visibles ANTES de generar la respuesta final.

¿Por qué CoT?
- Reduce respuestas superficiales o genéricas
- Hace el razonamiento depurable (si falla, vemos dónde)
- Mejora consistencia de estilo y estructura

ZERO-SHOT vs FEW-SHOT:
- Zero-shot: Sin ejemplos en el prompt (este archivo)
  - Ventajas: Menos tokens (más barato), más rápido de implementar
  - Desventajas: Mayor variación de estilo entre ejecuciones
- Few-shot: Con ejemplos (ver 02_few_shot_cot_feedback_loop.py)
  - Ventajas: Mayor consistencia, mejor adherencia al formato
  - Desventajas: +80% tokens (más caro), requiere curar ejemplos

TRADE-OFF ECONÓMICO (ver README.md para detalles):
- Este approach: ~500 tokens/request = $0.00021/request (gpt-4o-mini)
- Few-shot: ~900 tokens/request = $0.00027/request (+29% costo)
- Prompt directo sin CoT: ~300 tokens/request (baseline reference)

LIMITACIÓN CRÍTICA:
CoT NO convierte modelos débiles en expertos. CoT amplifica la calidad del razonamiento
y el contexto que le des. Mal contexto + CoT = razonamiento malo (y más caro).

MAPEO A ESTRUCTURA DE 5 CAPAS (ver README principal):
1. ROLE: Líneas 96-105 - Define identidad y valores del agente
2. TASK: Líneas 107-127 - Qué debe hacer (incluye descomposición en 4 pasos)
3. OUTPUT FORMAT: Líneas 129-156 - JSON schema estricto
4. EXAMPLES: No (este es zero-shot)
5. CONTEXT: Líneas 194-229 - Perfil específico del usuario

Para versión tipo-segura con Pydantic, ver: 03_zero_shot_cot_pydantic.py
Para comparison JSON vs Pydantic, lee README.md sección "Output Format Evolution"
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

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return OpenAI(api_key=api_key), model


def run_zero_shot_cot(client: OpenAI, model: str, profile: dict[str, Any]) -> dict[str, Any]:
    """
    Ejecuta Chain of Thought zero-shot (sin ejemplos en el prompt).

    VENTAJAS:
    - Rápido de implementar (no requiere curar ejemplos)
    - Menor uso de tokens (~500 vs ~900 con few-shot)
    - Flexible a casos diversos (no se limita a estilo de ejemplos)

    DESVENTAJAS:
    - Mayor variabilidad en estilo entre ejecuciones
    - Puede derivar del formato esperado (menos que con few-shot)
    - Requiere más iteraciones de prueba/error para afinar

    CUÁNDO USAR:
    - Prototipado rápido
    - Presupuesto de tokens limitado
    - Casos de uso muy diversos (difícil curar ejemplos representativos)

    CUÁNDO NO USAR:
    - Necesitas consistencia muy alta (→ usa few-shot)
    - Producción con volumen alto (considera afinar con ejemplos)

    Ver 02_few_shot_cot_feedback_loop.py para alternativa con mayor consistencia.
    Ver ../PYDANTIC_GUIDE.md para alternativa tipo-segura.

    Args:
        client: Cliente OpenAI configurado
        model: Nombre del modelo (ej: "gpt-4o-mini")
        profile: Dict con tipo_persona, gustos, estilo, contexto

    Returns:
        Dict con chain_of_thought, opener, follow_up, tone_notes, avoid
    """
    # CAPA 1: ROLE - Define quién es el agente
    # =========================================
    # - Identidad: "coach conversacional"
    # - Valores: "elegante, respetuoso, práctico"
    # - Restricciones éticas: "sin presión, sin lenguaje explícito, prioriza consentimiento"
    system_prompt = (
        "Eres un coach conversacional elegante, respetuoso y práctico. "
        "Tu objetivo es ayudar a iniciar conversaciones con calidez, sin presión y sin lenguaje explícito. "
        "Siempre prioriza consentimiento, autenticidad y respeto."
    )

    # CAPA 2: TASK - Qué debe hacer el agente
    # =========================================
    # - Objetivo: "Diseña una recomendación personalizada"
    # - Descomposición: 4 pasos de razonamiento (señales, estrategia, riesgos, recomendación)
    # - Alcance: "personalizada" (usa señales del perfil, no genérica)

    # CAPA 5: CONTEXT - Información específica
    # =========================================
    # - Datos estructurados del perfil del usuario
    # - Sin ruido, solo señales accionables

    user_prompt = f"""
Diseña una recomendación de conversación personalizada para el siguiente perfil:
{json.dumps(profile, ensure_ascii=False, indent=2)}

Usa Chain of Thought visible en 4 pasos breves:
1) Señales clave del perfil.
2) Estrategia de apertura.
3) Riesgos a evitar.
4) Recomendación final.

# CAPA 3: OUTPUT FORMAT - Estructura requerida
# ==============================================
# - JSON validable (response_format enforces esto)
# - Campos específicos con tipos implícitos
# - chain_of_thought: array de exactamente 4 strings
# - opener/follow_up: strings de longitud razonable (10-150 chars)
# - tone_notes/avoid: arrays de strings

Devuelve JSON con esta estructura exacta:
{{
  "chain_of_thought": ["...", "...", "...", "..."],
  "opener": "mensaje inicial corto",
  "follow_up": "pregunta natural de seguimiento",
  "tone_notes": ["...", "..."],
  "avoid": ["...", "..."]
}}

# ANTI-PATTERNS (qué NO hacer):
#  Opener genérico sin personalización: "Hola, ¿cómo estás?"
#  Opener demasiado directo/presión: "Hola, me gustas. ¿Salimos?"
#  Lenguaje explícito o inapropiado para primera interacción
#  Ignorar señales del perfil (no usar gustos/estilo/contexto)

# PATTERNS (qué sí hacer):
#  Opener que referencia gustos: "¿Qué cafés de Palermo recomendarías para escuchar jazz en vivo?"
#  Pregunta abierta que invita a hablar de su pasión
#  Tono coherente con estilo del perfil (ej: intelectual → pregunta reflexiva)
#  Follow-up que profundiza naturalmente en el tema
""".strip()

    completion = client.chat.completions.create(
        model=model,
        temperature=0.7,
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
    Ejecuta ejemplos de Zero-shot CoT con perfiles diversos.

    PERFILES PEDAGÓGICOS:
    - Diseñados para mostrar cómo el contexto determina el output
    - Cada perfil tiene señales accionables distintas
    - Demuestra que el mismo sistema produce outputs personalizados según contexto
    """
    client, model = get_client_and_model()

    # PERFIL 1: Profesional analítica con intereses culturales
    # ==========================================================
    # Señales accionables:
    # - "cirujana cardiovascular" → valora precisión, disciplina
    # - "ballet clásico" → aprecia arte, elegancia
    # - "vinos biodinámicos" → interés en sustentabilidad, conocimiento profundo
    # - "alpinismo de altura" → aventurera, desafiante
    # Estilo esperado: Intelectual, preciso, con sustancia
    profile_1 = {
        "tipo_persona": "cirujana cardiovascular con pasión por ballet clásico",
        "gustos": ["teatro de cámara", "vinos biodinámicos", "alpinismo de altura"],
        "estilo": "valora precisión, elegancia y conversación intelectual profunda",
        "contexto": "match con perfil verificado, ella envió like primero",
    }

    # PERFIL 2: Creativo ecléctico con contraste interesante
    # =======================================================
    # Señales accionables:
    # - "productor musical de jazz" → creativo, sensibilidad auditiva
    # - "vinilos de Coltrane" → conocimiento profundo, coleccionista
    # - "cocina japonesa izakaya" → aprecia autenticidad, experiencias sensoriales
    # - "fotografía analógica" → valora proceso, no solo resultado
    # Estilo esperado: Creativo, referencias culturales, conversación lúdica
    profile_2 = {
        "tipo_persona": "productor musical de jazz contemporáneo",
        "gustos": ["vinilos de Coltrane", "cocina japonesa izakaya", "fotografía analógica"],
        "estilo": "creativo, espontáneo, aprecia referencias culturales sutiles",
        "contexto": "conversación retomada tras 3 días de silencio",
    }

    # PERFIL 3: Científica con lado artístico
    # ========================================
    # Señales accionables:
    # - "neurocientífica especializada en sueño" → mente analítica, curiosa
    # - "documentales BBC" → aprecia calidad, profundidad
    # - "yoga aéreo" → busca equilibrio, experimenta
    # - "cafés silenciosos para leer" → necesita espacios tranquilos
    # Estilo esperado: Curiosa, valora evidencia, humor sutil
    profile_3 = {
        "tipo_persona": "neurocientífica especializada en sueño",
        "gustos": ["documentales BBC", "yoga aéreo", "cafés silenciosos para leer"],
        "estilo": "curiosa, valora profundidad y evidencia, humor sutil",
        "contexto": "match tras leer biografía completa, ella mencionó paper tuyo",
    }

    # Ejecutar CoT para cada perfil
    print("\n" + "=" * 70)
    print("DEMOSTRACIÓN: Mismo sistema, diferente contexto = diferente output")
    print("=" * 70)

    for i, profile in enumerate([profile_1, profile_2, profile_3], 1):
        print(f"\n{'=' * 70}")
        print(f"PERFIL {i}: {profile['tipo_persona']}")
        print(f"{'=' * 70}")
        print(f"Gustos: {', '.join(profile['gustos'])}")
        print(f"Estilo: {profile['estilo']}")
        print(f"Contexto: {profile['contexto']}")
        print(f"\n{'─' * 70}")
        print("RECOMENDACIÓN GENERADA:")
        print(f"{'─' * 70}")

        result = run_zero_shot_cot(client, model, profile)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    print(f"\n{'=' * 70}")
    print("OBSERVA:")
    print("- ¿El opener referencia gustos específicos del perfil?")
    print("- ¿El tono coincide con el estilo esperado?")
    print("- ¿El razonamiento (chain_of_thought) es coherente?")
    print("- ¿Hay variación creativa entre los 3 outputs?")
    print("=" * 70)


if __name__ == "__main__":
    main()
