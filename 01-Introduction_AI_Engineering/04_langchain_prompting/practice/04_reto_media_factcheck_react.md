# Reto 4: Fact-check de noticias con agente ReAct

## Dificultad

Nivel 4 de 5.

## Estrategia principal

ReAct con `StructuredTool` y salida tipada.

## Industria

Media, newsroom y public affairs.

## Escenario

Antes de publicar una nota, la redaccion debe verificar afirmaciones que pueden requerir busqueda, comparacion de fuentes y decision sobre evidencia insuficiente. Es un caso donde el camino no es fijo y las herramientas importan tanto como el prompt.

## Objetivo

Construir un agente inspirado en `fact_checker_agent.py` que produzca:

- `claim`
- `verdict`
- `confidence`
- `evidence`
- `sources`
- `open_questions`

## Lo que debes construir

- Herramientas para extraer afirmaciones, buscar evidencia y sintetizar veredictos.
- Un agente que decida la siguiente accion por iteracion.
- Un modelo Pydantic para la salida final.

## Paso a paso

1. Define herramientas pequenas y observables. No empieces con una herramienta gigante.
2. Diseña el estado minimo del agente: afirmaciones, evidencia, trace y veredicto parcial.
3. Usa `StructuredTool.from_function` o `@tool` para registrar las herramientas.
4. Fuerza un orden razonable del flujo o agrega guardrails si el agente se desvia.
5. Obliga a que el veredicto final distinga entre `VERDADERO`, `FALSO`, `PARCIAL` e `INCIERTO`.
6. Evalua el sistema con afirmaciones faciles, ambiguas y deliberadamente imposibles de verificar.

## Como validar que la salida es correcta

- Cada veredicto debe apoyarse en evidencia citada.
- Debe haber diversidad minima de fuentes cuando el caso lo permita.
- Si no hay evidencia suficiente, el sistema debe decir `INCIERTO`, no inventar.
- El trace debe mostrar por que el agente uso cada herramienta.
- La salida final debe parsear y mantener consistencia entre veredicto, confianza y evidencia.

## Cuando usar esta estrategia

Usala cuando resolver la tarea exige buscar o actuar sobre fuentes externas y el siguiente paso depende de lo ya observado.

## Cuando no usarla

No la uses si todo el conocimiento ya esta en el contexto local o si un pipeline fijo resuelve mejor el problema.
