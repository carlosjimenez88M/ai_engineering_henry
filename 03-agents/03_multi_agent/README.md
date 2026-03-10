# Multi-Agent — Coordinacion entre Agentes

Este modulo explora patrones de coordinacion entre multiples agentes especializados.

## Contenido

| Notebook | Tema | Descripcion |
|----------|------|-------------|
| `01_orquestador_workers.ipynb` | Orquestacion | Un agente descompone tareas y despacha a workers |
| `02_handoffs.ipynb` | Hand-offs | Transferencia de control entre agentes |
| `03_resolucion_conflictos.ipynb` | Conflictos | Votacion, debate y juez para resolver discrepancias |

## Scripts

- `scripts/orchestrator_workers.py` — Orquestador reutilizable
- `scripts/multi_agent_debate.py` — Sistema de debate multi-agente

## Prerequisitos

- Notebooks de `02_langchain/` completados
- ChromaDB con datos de comics indexados
