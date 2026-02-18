# LangChain — Agentes con Framework

Este modulo implementa agentes progresivamente mas complejos usando LangChain y LangGraph, culminando en un sistema RAG agentico completo con comics de Batman y Spider-Man.

## Contenido

| Notebook | Tema | Descripcion |
|----------|------|-------------|
| `01-tool-calling.ipynb` | Tools | `@tool` decorator, binding, ToolNode, structured output |
| `02-routing-condicional.ipynb` | Routing | Router LLM, especialistas, conditional edges |
| `03-validacion-salida.ipynb` | Validacion | Pydantic schemas, retry loops, guardrails |
| `04-rag-agentico.ipynb` | **RAG** | RAG basico → grading → hallucination check (ChromaDB) |
| `05-flujo-agentico-completo.ipynb` | **Agente** | Agente completo con 4 tools, multi-step reasoning |

## Scripts

- `scripts/tool_calling_agent.py` — Agente con tool calling reutilizable
- `scripts/routing_agent.py` — Router con especialistas
- `scripts/agentic_rag.py` — RAG agentico con grading y hallucination check
- `scripts/comic_knowledge_agent.py` — Agente experto en comics completo

## Datos

Los notebooks usan los datos de `../data/`:
- `batman_comics.json` — 12 narrativas de Batman
- `spiderman_comics.json` — 12 narrativas de Spider-Man
- `comics_eval.jsonl` — 10 preguntas de evaluacion

## Prerequisitos

- Notebooks de `intro/` completados
- `make sync` ejecutado desde `03-agents/`
- ChromaDB se inicializa in-memory en cada notebook
