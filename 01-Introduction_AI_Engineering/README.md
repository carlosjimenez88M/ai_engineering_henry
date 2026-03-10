# Modulo 1: Fundamentos de AI Engineering

Este modulo agrupa el tramo principal del curso. La secuencia va desde fundamentos de ingenieria aplicada a LLMs hasta un proyecto integrador con routing y RAG.

## Orden sugerido

| Orden | Tema | Ruta |
|---|---|---|
| 00 | Python extra class | `00_python_extra_class/` |
| 01 | Software Engineering vs AI Engineering | `01_introduction/` |
| 02 | Prompting aplicado | `02_prompting/` |
| 03 | LangChain prompting | `03_langchain_prompting/` |
| 04 | LangGraph workflows | `04_langchain_langgraph/` |
| 05 | RAG | `05_rags/` |
| 06 | Proyecto integrador | `06_project/` |

## Que hay en cada bloque

| Carpeta | Enfoque |
|---|---|
| `00_python_extra_class/` | Python profesional para estudiantes que necesitan nivelacion |
| `01_introduction/` | Caso comparativo entre software tradicional y AI Engineering |
| `02_prompting/` | Prompt introduction, prompt chaining, routing, CoT y ReAct |
| `03_langchain_prompting/` | Misma logica de prompting llevada a LangChain |
| `04_langchain_langgraph/` | Workflows con estado, routing, parallelization y feedback |
| `05_rags/` | Notebook base de vector stores, pipeline RAG y patrones con LangGraph |
| `06_project/` | Sistema multi-agente con routing por dominio y recuperacion de contexto |

## Comandos utiles

```bash
cd 01-Introduction_AI_Engineering
uv sync --extra dev
make test-all
make run-ai
make run-se
make run-notebooks
make run-notebooks-langchain
make run-notebooks-langgraph
make run-notebooks-rag
```

## Archivos importantes

- `pyproject.toml`: dependencias propias del modulo 1.
- `.env.example`: configuracion base para los ejemplos con OpenAI.
- `Makefile`: comandos de ejecucion, testing y notebooks.
- `03_langchain_prompting/tools/execute_notebooks.py`: ejecutor de notebooks de clase 03.
- `04_langchain_langgraph/tools/execute_notebooks.py`: ejecutor de notebooks de clase 04.
- `05_rags/tools/execute_notebooks.py`: ejecutor de notebooks de clase 05.

## Recomendacion de cursada

- Si el grupo necesita nivelacion, empieza por `00_python_extra_class/`.
- Si no, parte en `01_introduction/` y sigue el orden numerado.
- Usa los `README.md` internos de cada carpeta como guia de cada clase.
