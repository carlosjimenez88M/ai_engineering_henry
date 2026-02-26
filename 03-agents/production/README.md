# Production — Hardening de Agentes

Este modulo cubre los patrones esenciales para llevar agentes de IA a produccion: resiliencia, guardrails, presupuestos y monitoreo de calidad.

## Contenido

| Notebook | Tema | Descripcion |
|----------|------|-------------|
| `01_timeouts_retries.ipynb` | Resiliencia | Timeouts, retries con backoff, circuit breaker |
| `02_fallback_guardrails.ipynb` | Guardrails | Fallback chains, input/output guardrails |
| `03_presupuesto_costos.ipynb` | Costos | TokenBudget, limites por sesion, optimizacion |
| `04_alertas_calidad.ipynb` | Monitoreo | Quality signals, alertas, tests canary |

## Scripts

- `scripts/resilient_agent.py` — Agente con resiliencia completa
- `scripts/cost_budget_tracker.py` — Tracker de presupuesto reutilizable

## Prerequisitos

- Notebooks de `02_langchain/` completados
- Familiaridad con patrones de `05_llmops/`
