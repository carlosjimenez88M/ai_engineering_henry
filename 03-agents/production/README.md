# Production — Hardening de Agentes

Este modulo cubre los patrones esenciales para llevar agentes de IA a produccion: resiliencia, guardrails, presupuestos y monitoreo de calidad.

## Contenido

| Notebook | Tema | Descripcion |
|----------|------|-------------|
| `01-timeouts-retries.ipynb` | Resiliencia | Timeouts, retries con backoff, circuit breaker |
| `02-fallback-guardrails.ipynb` | Guardrails | Fallback chains, input/output guardrails |
| `03-presupuesto-costos.ipynb` | Costos | TokenBudget, limites por sesion, optimizacion |
| `04-alertas-calidad.ipynb` | Monitoreo | Quality signals, alertas, tests canary |

## Scripts

- `scripts/resilient_agent.py` — Agente con resiliencia completa
- `scripts/cost_budget_tracker.py` — Tracker de presupuesto reutilizable

## Prerequisitos

- Notebooks de `langchain/` completados
- Familiaridad con patrones de `LLMops/`
