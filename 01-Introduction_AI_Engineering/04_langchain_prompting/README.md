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

## Practica recomendada

La carpeta `practice/` propone 5 retos progresivos para llevar estas ideas a casos reales:

- `04_langchain_prompting/practice/README.md`
- `04_langchain_prompting/practice/01_reto_rrhh_scorecard.md`
- `04_langchain_prompting/practice/02_reto_turismo_contexto.md`
- `04_langchain_prompting/practice/03_reto_seguros_cot_langchain.md`
- `04_langchain_prompting/practice/04_reto_media_factcheck_react.md`
- `04_langchain_prompting/practice/05_reto_procurement_router_hibrido.md`
