# 03 — Coordinación Multi-agente

Cuando un solo agente ya no es suficiente porque la tarea es demasiado amplia, demasiado especializada, o requiere perspectivas independientes, entrás en territorio multi-agente. Este bloque cubre los tres patrones fundamentales de coordinación: orquestación, handoffs y resolución de conflictos.

La diferencia con el bloque anterior no es de herramientas sino de arquitectura: acá diseñás sistemas donde varios agentes interactúan, se pasan el control y pueden llegar a resultados distintos que necesitan reconciliarse.

---

## Contenido

| Notebook | Tema | Qué construís |
|---|---|---|
| `01_orquestador_workers.ipynb` | Patrón Orquestador-Workers | Un agente descompone la tarea en subtareas y despacha a agentes especializados |
| `02_handoffs.ipynb` | Handoffs | Transferencia explícita de control entre agentes, con contexto compartido |
| `03_resolucion_conflictos.ipynb` | Resolución de Conflictos | Votación entre agentes, debate sintético, y juez LLM para arbitrar discrepancias |

---

## Scripts Disponibles

- `scripts/orchestrator_workers.py` — Orquestador genérico reutilizable
- `scripts/multi_agent_debate.py` — Sistema de debate multi-agente configurable

---

## Prerrequisitos

- Notebooks del bloque `02_langchain/` completados
- ChromaDB con datos de cómics indexados (se inicializa en los notebooks del bloque 02)

---

## Nota sobre Complejidad

Los sistemas multi-agente son más difíciles de depurar que los de un solo agente porque los errores pueden originarse en la coordinación entre agentes, no en ninguno de ellos individualmente. Antes de hacer cualquier bloque de este módulo más complejo, asegurate de entender bien el flujo de datos entre los nodos del grafo.

---

## Criterio de Avance

Antes de pasar al bloque 04, deberías poder:

- Describir cuándo elegirías el patrón orquestador-workers sobre un solo agente complejo
- Explicar qué información necesita pasar en un handoff para que el agente receptor tenga suficiente contexto
- Identificar los casos donde el debate entre agentes mejora la calidad y donde sólo agrega latencia
