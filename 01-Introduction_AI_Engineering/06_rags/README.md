# Clase 05: RAG

Este bloque introduce retrieval-augmented generation dentro del recorrido principal del curso.

## Orden recomendado

| Orden | Notebook | Tema |
|---|---|---|
| 1 | `Notebooks/01_bases_datos_vectoriales.ipynb` | Fundamentos de embeddings y vector stores |
| 2 | `Notebooks/02_rag_pipeline.ipynb` | Pipeline RAG base |
| 3 | `Notebooks/03_rag_prompt_chaining.ipynb` | RAG con prompt chaining |
| 4 | `Notebooks/04_rag_routing.ipynb` | RAG con routing por tipo de consulta |

## Estructura

- `data/`: bases de conocimiento de ejemplo.
- `Notebooks/`: secuencia principal de la clase.
- `tools/execute_notebooks.py`: ejecutor para correr la clase completa.

## Ejecucion

```bash
cd 01-Introduction_AI_Engineering
uv sync
uv run python 05_rags/tools/execute_notebooks.py
```

## Aprendizajes esperados

- entender por que RAG existe,
- diseñar chunking e indexacion,
- comparar respuestas con y sin recuperacion,
- combinar retrieval con patrones vistos en LangChain y LangGraph.
