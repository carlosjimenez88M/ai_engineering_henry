# 02 — Agentes con LangChain

Este bloque retoma lo que construiste desde cero en el bloque anterior y lo implementa con LangChain y LangGraph. El objetivo no es simplificar el código sino entender qué abstrae el framework y por qué esas abstracciones importan cuando el sistema crece.

El caso de trabajo son cómics de Batman y Spider-Man: un corpus con el que podés probar retrieval, routing semántico y razonamiento multi-step de forma concreta.

---

## Contenido

| Notebook | Tema | Qué implementás |
|---|---|---|
| `01_tool_calling.ipynb` | Tool Calling | Decorator `@tool`, binding de herramientas al modelo, ToolNode, structured output |
| `02_routing_condicional.ipynb` | Routing Condicional | Router LLM, agentes especialistas, conditional edges en LangGraph |
| `03_validacion_salida.ipynb` | Validación de Salida | Esquemas Pydantic, retry loops automáticos, guardrails básicos |
| `04_rag_agentico.ipynb` | RAG Agéntico | RAG básico → grading de documentos → hallucination check con ChromaDB |
| `05_flujo_agentico_completo.ipynb` | Agente Completo | Agente con 4 herramientas, razonamiento multi-step, ciclo completo |

---

## Scripts Disponibles

- `scripts/tool_calling_agent.py` — Agente con tool calling listo para importar
- `scripts/routing_agent.py` — Router con especialistas reutilizable
- `scripts/agentic_rag.py` — RAG agéntico con grading y hallucination check
- `scripts/comic_knowledge_agent.py` — Agente experto en cómics completo

---

## Datos de Trabajo

Los notebooks usan el corpus en `../00_data/`:

- `batman_comics.json` — 12 narrativas del universo Batman
- `spiderman_comics.json` — 12 narrativas del universo Spider-Man
- `comics_eval.jsonl` — 10 preguntas de evaluación con respuestas esperadas

ChromaDB se inicializa en memoria dentro de cada notebook. No necesitás persistencia previa.

---

## Prerrequisitos

- Notebooks del bloque `01_intro/` completados
- `make sync` ejecutado desde `03-agents/`

---

## Criterio de Avance

Antes de pasar al bloque 03, deberías poder:

- Agregar una herramienta nueva a un agente existente y explicar cómo el modelo decide cuándo usarla
- Diseñar un router LLM con dos especialistas y describir las aristas condicionales del grafo
- Explicar por qué el RAG agéntico puede ser más confiable que el RAG clásico (y cuándo no lo es)
