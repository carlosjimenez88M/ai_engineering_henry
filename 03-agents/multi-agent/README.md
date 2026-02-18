# Multi-Agent — Coordinacion entre Agentes

Este modulo explora patrones de coordinacion entre multiples agentes especializados.

## Contenido

| Notebook | Tema | Descripcion |
|----------|------|-------------|
| `01-orquestador-workers.ipynb` | Orquestacion | Un agente descompone tareas y despacha a workers |
| `02-handoffs.ipynb` | Hand-offs | Transferencia de control entre agentes |
| `03-resolucion-conflictos.ipynb` | Conflictos | Votacion, debate y juez para resolver discrepancias |

## Scripts

- `scripts/orchestrator_workers.py` — Orquestador reutilizable
- `scripts/multi_agent_debate.py` — Sistema de debate multi-agente

## Prerequisitos

- Notebooks de `langchain/` completados
- ChromaDB con datos de comics indexados
