# Clase 04: LangGraph Workflows

Esta clase organiza los patrones de orquestacion mas utiles para sistemas LLM: cadenas, paralelizacion, routers, orchestrator-worker, evaluator-optimizer y loops de feedback.

## Orden recomendado

| Orden | Notebook | Tema |
|---|---|---|
| 1 | `01_prompt_chaining/Notebooks/prompt_chaining_langgraph.ipynb` | Secuencias simples |
| 2 | `02_parallelization/Notebooks/parallelization_langgraph.ipynb` | Subtareas independientes |
| 3 | `05_routing/Notebooks/routing_langgraph.ipynb` | Decisiones por rama |
| 4 | `03_orchestrator_worker/Notebooks/orchestrator_worker_langgraph.ipynb` | Descomposicion dinamica |
| 5 | `04_evaluator_optimizer/Notebooks/evaluator_optimizer_langgraph.ipynb` | Mejora iterativa |
| 6 | `06_agent_feedback/Notebooks/agent_feedback_langgraph.ipynb` | Agente con control de calidad |

## Estructura

- `common/context_engineering.py`: helpers de contexto compartido.
- `tools/execute_notebooks.py`: ejecutor de notebooks del modulo.
- `01_prompt_chaining/` a `06_agent_feedback/`: una arquitectura por carpeta.

## Ejecucion

```bash
cd 01-Introduction_AI_Engineering
uv sync
uv run python 04_langchain_langgraph/tools/execute_notebooks.py
```

## Criterio pedagogico

No todas las arquitecturas deben usarse siempre. La clase esta ordenada desde el patron mas liviano al mas costoso de mantener, para que el estudiante aprenda a elegir la minima arquitectura que resuelve el problema.
