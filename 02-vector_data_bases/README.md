# Modulo 2: Vector Databases y RAG avanzado

Este modulo profundiza en representacion vectorial, retrieval y patrones de RAG con un recorrido mas tecnico que el bloque `05_rags/` del modulo principal.

## Estructura por tema

| Bloque | Enfoque | Ruta |
|---|---|---|
| 01 | Fundamentos de representacion y retrieval | `01_intro/` |
| 02 | Bases de datos vectoriales | `02_databases/` |
| 03 | Patrones de RAG | `03_rag/` |
| 04 | Caso aplicado Batman | `04_batman_vector_db_orchestration/` |

## Ruta sugerida de notebooks

### 01. Intro

| Orden sugerido | Notebook | Idea central |
|---|---|---|
| 1 | `01_intro/01_tokens.ipynb` | Como los modelos ven texto |
| 2 | `01_intro/03_transformers.ipynb` | Fundamentos de transformers |
| 3 | `01_intro/04_text_classification.ipynb` | Embeddings como representacion util |
| 4 | `01_intro/02_rag_tfidf.ipynb` | Retrieval sparse como baseline |
| 5 | `01_intro/05_rags_vectorial_databases.ipynb` | Puente entre retrieval y RAG |
| 6 | `01_intro/06_agent2agent_literario.ipynb` | Caso aplicado de cierre del bloque |

### 02. Databases

| Orden | Notebook | Idea central |
|---|---|---|
| 1 | `02_databases/01-bases-vectoriales-fundamentos.ipynb` | Embeddings, similitud y primeros stores |
| 2 | `02_databases/02-bases-vectoriales-produccion.ipynb` | Persistencia, chunking y trade-offs |
| 3 | `02_databases/03-comparacion-modelos-embeddings-rayuela.ipynb` | Comparativa aplicada de embeddings |

### 03. RAG

| Orden | Notebook | Idea central |
|---|---|---|
| 1 | `03_rag/01-rag-fundamentos.ipynb` | Pipeline completo |
| 2 | `03_rag/02-rag-avanzado.ipynb` | Multi-query, ensemble y compression |

### 04. Caso aplicado

| Orden | Notebook | Idea central |
|---|---|---|
| 1 | `04_batman_vector_db_orchestration/00_clase_de_repaso.ipynb` | Contexto y repaso |
| 2 | `04_batman_vector_db_orchestration/01_diseno_vector_db_batman.ipynb` | Diseño de vector store |
| 3 | `04_batman_vector_db_orchestration/02_rag_vs_agentic_rag_batman.ipynb` | Comparativa de enfoques |
| 4 | `04_batman_vector_db_orchestration/03_routing_orquestacion_simple.ipynb` | Routing entre dominios |
| 5 | `04_batman_vector_db_orchestration/04_ejercicio_agent2agent_batman_rag.ipynb` | Ejercicio guiado |
| 6 | `04_batman_vector_db_orchestration/05_agent2agent_roles_router_batman.ipynb` | Orquestacion especializada |

## Comandos utiles

```bash
cd 02-vector_data_bases
uv sync --extra dev
make test
make run-batman-module
```

Hoy `make test` actua como chequeo de presencia de tests. La validacion funcional principal del modulo sigue siendo ejecutar los notebooks y casos aplicados.

## Archivos de apoyo

- `pyproject.toml`: dependencias propias del modulo 2.
- `00_tools/execute_notebooks.py`: ejecuta notebooks del modulo.
- `build_review.py`: apoyo para revisiones automatizadas del material.
- `04_batman_vector_db_orchestration/scripts/`: utilidades reutilizables del caso aplicado.
