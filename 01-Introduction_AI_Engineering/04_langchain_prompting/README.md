# Clase 03: LangChain Prompting

Esta clase toma los ejercicios de `02_prompting/` y los transforma en componentes mas reutilizables usando LangChain.

## Objetivo

- estructurar prompts con templates,
- tipar salidas,
- reutilizar contexto,
- pasar de demos aisladas a piezas mas mantenibles.

## Orden recomendado

| Orden | Recurso | Objetivo |
|---|---|---|
| 1 | `COT_LangChain/Notebooks/cot_langchain_aplicado.ipynb` | Llevar CoT a LangChain |
| 2 | `ReAct_LangChain/Notebooks/react_langchain_aplicado.ipynb` | Llevar ReAct a LangChain |
| 3 | `COT_LangChain/Notebooks/02_cot_langgraph.ipynb` | Ver el puente hacia grafos |
| 4 | `ReAct_LangChain/Notebooks/02_react_langgraph.ipynb` | Integrar ReAct con flujos mas complejos |

## Estructura

- `COT_LangChain/`: ejemplos de chain-of-thought con LangChain.
- `ReAct_LangChain/`: agentes ReAct con tools y salida estructurada.
- `common/context_engineering.py`: utilidades para construir contexto reusable.
- `tools/execute_notebooks.py`: ejecuta y valida las notebooks de la clase.

## Ejecucion

```bash
cd 01-Introduction_AI_Engineering
uv sync
uv run python 03_langchain_prompting/tools/execute_notebooks.py
```

## Prerrequisitos

- Haber trabajado `02_prompting/`.
- Tener `OPENAI_API_KEY` configurada.
