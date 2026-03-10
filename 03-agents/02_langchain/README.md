# LangChain — Agentes con Framework

Este modulo implementa agentes progresivamente mas complejos usando LangChain y LangGraph, culminando en un sistema RAG agentico completo con comics de Batman y Spider-Man.

## Contenido

| Notebook | Tema | Descripcion |
|----------|------|-------------|
| `01_tool_calling.ipynb` | Tools | `@tool` decorator, binding, ToolNode, structured output |
| `02_routing_condicional.ipynb` | 03_routing | Router LLM, especialistas, conditional edges |
| `03_validacion_salida.ipynb` | Validacion | Pydantic schemas, retry loops, guardrails |
| `04_rag_agentico.ipynb` | **RAG** | RAG basico → grading → hallucination check (ChromaDB) |
| `05_flujo_agentico_completo.ipynb` | **Agente** | Agente completo con 4 tools, multi-step reasoning |

## Scripts

- `scripts/tool_calling_agent.py` — Agente con tool calling reutilizable
- `scripts/routing_agent.py` — Router con especialistas
- `scripts/agentic_rag.py` — RAG agentico con grading y hallucination check
- `scripts/comic_knowledge_agent.py` — Agente experto en comics completo

## Datos

Los notebooks usan los datos de `../00_data/`:
- `batman_comics.json` — 12 narrativas de Batman
- `spiderman_comics.json` — 12 narrativas de Spider-Man
- `comics_eval.jsonl` — 10 preguntas de evaluacion

## Prerequisitos

- Notebooks de `01_intro/` completados
- `make sync` ejecutado desde `03-agents/`
- ChromaDB se inicializa in-memory en cada notebook
