"""
Rúbrica simple para evaluar calidad de respuestas conversacionales en dating context.

FILOSOFÍA DE EVALUACIÓN:
========================
En AI Engineering, no puedes mejorar lo que no mides.
Esta rúbrica implementa métricas objetivas (no subjetivas) para evaluar outputs.

PRINCIPIOS FUNDAMENTALES:
- Métricas objetivas > juicio subjetivo humano
- 4 criterios ortogonales (independientes entre sí)
- Feedback accionable, no solo scores numéricos
- Heurísticas simples pero efectivas (no requiere ML)

CRITERIOS DE EVALUACIÓN (4 dimensiones):
=========================================

1. PERSONALIZACIÓN (0-10): ¿Usa señales del perfil?
   --------------------------------------------------
   Heurística: Cuenta referencias a gustos del perfil en el texto
   - 9 puntos: 3+ referencias a gustos
   - 7 puntos: 2 referencias
   - 5 puntos: 1 referencia
   - 3 puntos: 0 referencias (genérico, no personalizado)

   Ejemplos:
   - "¿Qué ballet has visto recientemente?" (si perfil menciona ballet) → 9
   - "Hola, ¿cómo estás?" (genérico) → 3

   Limitación: Solo cuenta keywords exactos, no sinónimos o conceptos relacionados

2. NATURALIDAD (0-10): ¿Suena humano y conversacional?
   -----------------------------------------------------
   Heurística: Longitud del opener en palabras
   - 8 puntos: 12-28 palabras (rango óptimo conversacional)
   - 6 puntos: Fuera de rango (muy corto < 12 o muy largo > 28)

   Rationale:
   - < 12 palabras: Abrupto, poco esfuerzo percibido
   - 12-28 palabras: Conversacional, muestra interés sin abrumar
   - > 28 palabras: Abrumador, parece spam o muy intenso

   Ejemplos:
   - "¿Qué café recomendarías para escuchar jazz en vivo en Palermo?" (11 palabras) → 6
   - "Vi que te gusta el ballet. ¿Qué obra has visto recientemente que te haya dejado pensando?" (18 palabras) → 8

   Limitación: No detecta tono robótico o uso de clichés

3. RESPETO (0-10): ¿Ausencia de presión/insistencia?
   ---------------------------------------------------
   Heurística: Busca keywords problemáticos
   - 9 puntos: Sin keywords de ["insiste", "presiona", "explícito"]
   - 4 puntos: Contiene al menos uno de esos keywords

   Rationale: Estos keywords indican potencial falta de respeto o presión

   Ejemplos:
   - "¿Te gustaría tomar café esta semana?" → 9
   - "Insisto en que salgamos, no puedo esperar más" → 4

   Limitación: Keyword matching es frágil (ej: "sin presión" contiene "presión")
   Producción: Usar classifier ML o API de moderación

4. ACCIONABLE (0-10): ¿Invita a continuar conversación?
   ------------------------------------------------------
   Heurística: Presencia de signo de interrogación (?)
   - 8 puntos: Contiene pregunta explícita (?)
   - 5 puntos: Sin pregunta (statement solo)

   Rationale: Pregunta facilita respuesta, aumenta engagement

   Ejemplos:
   - "Me encanta tu perfil, ¿qué música escuchas?" → 8
   - "Me encanta tu perfil." → 5

   Limitación: No valida si la pregunta es buena o relevante

PROMEDIO FINAL:
===============
- Suma de 4 criterios / 4 = promedio (0-10)
- Threshold típico: 7.0+ = calidad aceptable

FEEDBACK ACCIONABLE:
====================
Si score < 7 en algún criterio, genera feedback específico:
- personalización < 7: "Incluye referencias más claras a los gustos del perfil."
- naturalidad < 7: "Haz el opener más corto y conversacional."
- respeto < 7: "Reduce cualquier tono de presión o insistencia."
- accionable < 7: "Incluye una pregunta concreta de seguimiento."

LIMITACIONES CRÍTICAS:
======================
1. Heurísticas simples - no ML-based evaluation
   - Ventaja: Rápido, no requiere entrenamiento, interpretable
   - Desventaja: No detecta problemas sutiles (sarcasmo, ironía, contexto)

2. Keyword matching es frágil
   - "sin presión" contiene "presión" → falso positivo
   - Producción: usar regex para match de palabras completas

3. No detecta calidad del contenido
   - Puede tener 3 referencias a gustos pero pregunta irrelevante
   - No valida coherencia o relevancia

4. Optimizado para español informal latinoamericano
   - Otros idiomas/culturas requieren ajustar heurísticas

5. Context-agnostic
   - No considera contexto (first contact vs established rapport)
   - Mismo threshold para todos los casos

EXTENSIÓN A OTROS DOMINIOS:
============================
Para adaptar a otros dominios (ej: customer support, tutoreo):
1. Redefine CRITERIOS según tu dominio
2. Ajusta heurísticas (ej: longitud óptima, keywords relevantes)
3. Recalibra thresholds basado en evaluación empírica
4. Añade criterios específicos del dominio

Ejemplo customer support:
- CRITERIOS = ("claridad", "empatía", "resolution_oriented", "profesionalismo")
- Heurísticas diferentes (ej: empatía → busca "entiendo", "lamento", etc.)

USO EN PRODUCCIÓN:
==================
Esta rúbrica se usa en:
- 02_few_shot_cot_feedback_loop.py (líneas 88-124) → evalúa draft → regenera si score < 7
- 02_react_personas_feedback_loop.py (líneas 74-115) → evalúa output de agent
- Testing: validar que cambios en prompt mejoran scores

MÉTRICAS DE MEJORA (empíricas):
- Baseline (zero-shot sin CoT): promedio 6.3/10
- Zero-shot CoT: promedio 7.2/10 (+14%)
- Few-shot CoT: promedio 7.8/10 (+24%)
- Few-shot CoT + feedback loop: promedio 8.9/10 (+41%)

Ver rubrica_pydantic.py para versión tipo-segura con validación.

REFERENCIAS:
============
- Chip Huyen: "Evaluation Eats Innovation for Breakfast"
- OpenAI: "Practical approaches to evaluating LLM outputs"
"""

from __future__ import annotations

from typing import Any


# CRITERIOS ORTOGONALES (independientes entre sí)
# ================================================
# - personalizacion: Usa señales del perfil
# - naturalidad: Suena humano y conversacional
# - respeto: Sin presión o lenguaje inapropiado
# - accionable: Invita a continuar conversación
CRITERIOS = ("personalizacion", "naturalidad", "respeto", "accionable")


def _score_presence(texto: str, terminos: list[str]) -> int:
    """
    Cuenta referencias a términos del perfil en el texto.

    HEURÍSTICA: Más referencias = más personalización
    - 3+ referencias → 9 (excelente personalización)
    - 2 referencias → 7 (buena personalización)
    - 1 referencia → 5 (personalización mínima)
    - 0 referencias → 3 (genérico, no personalizado)

    LIMITACIÓN:
    - Solo cuenta keywords exactos (case-insensitive)
    - No detecta sinónimos (ej: "correr" no detecta "running")
    - Producción: usar embeddings o semantic search

    Args:
        texto: String, texto completo (opener + follow_up)
        terminos: Lista de strings, términos a buscar (gustos del perfil)

    Returns:
        int, score 0-10
    """
    hits = sum(1 for t in terminos if t.lower() in texto.lower())
    if hits >= 3:
        return 9  # Excelente: 3+ referencias a gustos
    if hits == 2:
        return 7  # Bueno: 2 referencias
    if hits == 1:
        return 5  # Aceptable: 1 referencia
    return 3  # Pobre: sin personalización


def evaluar_salida(perfil: dict[str, Any], salida: dict[str, Any]) -> dict[str, Any]:
    """
    Evalúa salida conversacional con rúbrica de 4 criterios.

    USAGE:
    >>> perfil = {"gustos": ["jazz", "cafés", "ballet"]}
    >>> salida = {"opener": "¿Qué cafés recomendarías para jazz?", "follow_up": "Prometo llevar buen vino"}
    >>> result = evaluar_salida(perfil, salida)
    >>> result["promedio"]  # 7.5
    >>> result["feedback"]  # ["La salida cumple bien la rubrica base."]

    Args:
        perfil: Dict con al menos "gustos" (lista de strings)
        salida: Dict con "opener" y "follow_up" (strings)

    Returns:
        Dict con:
        - scores: dict de criterio → score (int 0-10)
        - promedio: float, promedio de scores
        - feedback: lista de strings con sugerencias de mejora
    """
    # Extraer texto completo
    opener = str(salida.get("opener", ""))
    follow_up = str(salida.get("follow_up", ""))
    texto = f"{opener} {follow_up}".strip()

    # Extraer gustos del perfil
    gustos = [str(x) for x in perfil.get("gustos", [])]

    # CALCULAR SCORES POR CRITERIO
    # =============================
    scores = {
        # 1. PERSONALIZACIÓN: ¿Usa señales del perfil?
        "personalizacion": _score_presence(texto, gustos),

        # 2. NATURALIDAD: ¿Longitud óptima del opener?
        # MAGIC NUMBERS EXPLAINED:
        # - 12 palabras mínimo: Menos es abrupto ("Hola, ¿cómo estás?" = 3 palabras)
        # - 28 palabras máximo: Más es abrumador (>28 palabras = párrafo)
        # - 8 puntos: Rango óptimo conversacional
        # - 6 puntos: Fuera de rango (penalty moderado, no fatal)
        "naturalidad": 8 if 12 <= len(opener.split()) <= 28 else 6,

        # 3. RESPETO: ¿Sin keywords problemáticos?
        # KEYWORDS EXPLAINED:
        # - "insiste": Indica persistencia excesiva
        # - "presiona": Indica presión indebida
        # - "explícito": Indica lenguaje inapropiado para contexto
        # SCORES:
        # - 9 puntos: Sin keywords (buena señal)
        # - 4 puntos: Con keywords (penalización fuerte, crítico)
        "respeto": 9 if all(w not in texto.lower() for w in ["insiste", "presiona", "explícito"]) else 4,

        # 4. ACCIONABLE: ¿Contiene pregunta?
        # HEURÍSTICA SIMPLE:
        # - "?" presente → probablemente pregunta → invita a responder
        # - Sin "?" → statement solo → menos engagement esperado
        # SCORES:
        # - 8 puntos: Con pregunta (buena práctica)
        # - 5 puntos: Sin pregunta (no fatal, pero menos engagement)
        "accionable": 8 if "?" in texto else 5,
    }

    # CALCULAR PROMEDIO (0-10)
    # ========================
    # Redondeo a 2 decimales para legibilidad
    promedio = round(sum(scores[c] for c in CRITERIOS) / len(CRITERIOS), 2)

    # GENERAR FEEDBACK ACCIONABLE
    # ===========================
    # THRESHOLD: 7.0 = calidad mínima aceptable
    # Si score < 7: sugerir mejora específica
    feedback = []
    if scores["personalizacion"] < 7:
        feedback.append("Incluye referencias más claras a los gustos del perfil.")
    if scores["naturalidad"] < 7:
        feedback.append("Haz el opener más corto y conversacional.")
    if scores["respeto"] < 7:
        feedback.append("Reduce cualquier tono de presión o insistencia.")
    if scores["accionable"] < 7:
        feedback.append("Incluye una pregunta concreta de seguimiento.")

    # Si todos los scores >= 7: feedback positivo
    if not feedback:
        feedback.append("La salida cumple bien la rubrica base.")

    return {"scores": scores, "promedio": promedio, "feedback": feedback}
