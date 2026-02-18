# Intro — Fundamentos de Agentes

Este modulo introduce los conceptos fundamentales de agentes de IA, desde la anatomia basica hasta el analisis de costos y riesgos.

## Contenido

| Notebook | Tema | Descripcion |
|----------|------|-------------|
| `01-que-es-un-agente.ipynb` | Agente minimo | Loop ReAct con OpenAI API pura, tool calls, anatomia |
| `02-workflows-vs-agentes.ipynb` | Patrones | Workflow lineal vs agente dinamico, taxonomia Anthropic |
| `03-costo-latencia-alucinacion.ipynb` | Metricas | Token economics, latencia, alucinacion, LLM-as-judge |

## Script

- `scripts/agent_anatomy.py` — Agente ReAct minimo reutilizable como modulo

## Prerequisitos

- OpenAI API key en `.env`
- `make sync` ejecutado desde `03-agents/`
