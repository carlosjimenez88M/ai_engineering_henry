# Clase 04: LangChain + LangGraph Workflows y Agents (aplicado)

Esta clase evoluciona `03_langchain_prompting` hacia arquitecturas de orquestacion con **LangGraph**, usando el enfoque oficial de workflows/agents de LangChain.

Referencia base (fuente primaria):
- [LangGraph Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

## Objetivo pedagogico

Pasar de "un buen prompt" a "un sistema de decision". En produccion, el valor no esta en un prompt aislado, sino en:

- flujo de estados reproducible,
- control de rutas,
- paralelizacion cuando aplica,
- ciclos de mejora con criterio,
- agentes con herramientas y feedback.

## Arquitecturas cubiertas

Este modulo implementa 6 arquitecturas del material oficial y las aterriza al caso que ya venimos trabajando (recomendaciones conversacionales personalizadas):

1. Prompt chaining
2. Parallelization
3. Routing
4. Orchestrator-worker
5. Evaluator-optimizer
6. Agent con feedback

## Cuando usar cada arquitectura

| Arquitectura | Cuando usarla | Señal de que **no** debes usarla |
|---|---|---|
| Prompt chaining | Tarea secuencial donde cada paso depende del anterior (analizar -> generar -> refinar). | Si todo se resuelve bien en una sola llamada estable. |
| Parallelization | Subtareas independientes que se pueden ejecutar en paralelo y luego agregar. | Si las subtareas dependen fuertemente una de otra. |
| Routing | Tienes tipos de input claramente distintos que requieren estrategias especializadas. | Si las ramas no son distinguibles o el router no agrega valor. |
| Orchestrator-worker | Necesitas descomponer dinamicamente en N subtareas (N variable) y sintetizar resultados. | Si N siempre es 1 o 2 fijo y la complejidad extra no compensa. |
| Evaluator-optimizer | La calidad importa mas que latencia y necesitas ciclo de mejora guiado por criterios. | Si tu SLA de latencia es estricto o costo es prioridad absoluta. |
| Agent con feedback | Necesitas herramientas + razonamiento iterativo + control de calidad en loop. | Si no hay tools reales o el problema es deterministico de bajo riesgo. |

## Estructura del modulo

- `04_langchain_langgraph/01_prompt_chaining/Notebooks`
- `04_langchain_langgraph/02_parallelization/Notebooks`
- `04_langchain_langgraph/03_orchestrator_worker/Notebooks`
- `04_langchain_langgraph/04_evaluator_optimizer/Notebooks`
- `04_langchain_langgraph/05_routing/Notebooks`
- `04_langchain_langgraph/06_agent_feedback/Notebooks`
- `04_langchain_langgraph/common/context_engineering.py`
- `04_langchain_langgraph/tools/execute_notebooks.py`

Cada arquitectura incluye:
- script `.py` ejecutable,
- notebook `.ipynb`,
- notebook `.executed.ipynb` generado por validacion.

## Context engineering (criterio transversal)

Todo ejemplo usa `context packet` con:
- campos estructurados,
- deduplicacion de senales,
- budget de contexto,
- hash de trazabilidad (`context_hash`).

Esto permite comparar salidas entre arquitecturas sin contaminar por ruido de contexto.

## Ejecucion

```bash
uv sync
uv run python 04_langchain_langgraph/tools/execute_notebooks.py
```

## Critica tecnica (honesta)

- Estas arquitecturas no son gratis: agregan costo cognitivo, tokens y mantenimiento.
- LangGraph no reemplaza evaluacion offline; solo organiza mejor el flujo.
- Sin contratos de estado bien definidos, el grafo se vuelve fragil.
- Si no mides calidad/costo/latencia, estas sobre-ingenierizando.

La regla de oro: **elige la arquitectura minima que cubra tu riesgo principal**.
