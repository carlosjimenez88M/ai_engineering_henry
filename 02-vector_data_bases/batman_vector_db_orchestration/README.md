# Batman Vector DB + RAG + Agentic Orchestration Module

Este submodulo extiende el **modulo 2** con un enfoque aplicado y detallado sobre:

1. Diseno de una base de datos vectorial desde cero.
2. Construccion de un pipeline **Vanilla RAG**.
3. Construccion de un pipeline **Agentic RAG** con routing, reescritura y grounding check.
4. Ejemplo simple de **orquestacion por routing** entre dominios (Batman vs Spider-Man).
5. Ejercicio simple de **agent2agent** con Batman + RAG.
6. Ejercicio **agent2agent especializado por roles** con router interno.

El tono y la estructura estan pensados para clase avanzada de AI Engineering aplicada.

## Estructura

- `01_diseno_vector_db_batman.ipynb`: diseno de schema, chunking, metadata strategy e indexado.
- `02_rag_vs_agentic_rag_batman.ipynb`: implementacion comparativa y graficas de diferencias.
- `03_routing_orquestacion_simple.ipynb`: routing/orquestacion simple entre retrievers tematicos.
- `04_ejercicio_agent2agent_batman_rag.ipynb`: ejercicio guiado agent2agent con retriever agent + synthesizer agent.
- `05_agent2agent_roles_router_batman.ipynb`: agent2agent con router semantico y agentes especializados (`timeline`, `villains`, `strategy`, `general`).
- `scripts/`: utilidades reutilizables para DB, pipelines y evaluacion.
- `data/`: datasets de comics (Batman y Spider-Man).
- `outputs/`: artefactos generados por notebooks (graficas y tablas).

## Modelos usados

- LLM: `gpt-5-mini`.
- Embeddings: `text-embedding-3-small`.
- Vector DB: `ChromaDB`.

Si `OPENAI_API_KEY` esta configurada y hay conectividad, los notebooks usan OpenAI.
Si no, activan fallback local deterministico para que el flujo se ejecute igual.

## Como ejecutar (desde `02-vector_data_bases`)

```bash
make run-batman-module
```

Esto ejecuta los 5 notebooks y genera versiones `*.executed.ipynb`.

## Variables recomendadas

```bash
export OPENAI_API_KEY="tu_clave"
```
