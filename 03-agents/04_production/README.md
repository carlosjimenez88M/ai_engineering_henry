# 04 — Hardening para Producción

Un agente que funciona en un notebook no necesariamente funciona en producción. Este bloque cubre los patrones que hacen la diferencia: cómo manejar fallas de la API, cómo proteger el sistema de inputs maliciosos o inesperados, cómo controlar los costos antes de que exploten, y cómo detectar degradaciones de calidad antes de que los usuarios lo noten.

El énfasis de este bloque es la modularidad: cada patrón está implementado de forma que podés incorporarlo en cualquier sistema existente sin reescribir la lógica de negocio.

---

## Contenido

| Notebook | Tema | Qué implementás |
|---|---|---|
| `01_timeouts_retries.ipynb` | Resiliencia | Timeouts configurables, retries con backoff exponencial, circuit breaker |
| `02_fallback_guardrails.ipynb` | Guardrails | Fallback chains, validación de input, filtros de output |
| `03_presupuesto_costos.ipynb` | Control de Costos | TokenBudget por sesión, límites configurables, estrategias de optimización |
| `04_alertas_calidad.ipynb` | Monitoreo de Calidad | Señales de calidad, alertas automáticas, tests canary para detección temprana |

---

## Scripts Disponibles

- `scripts/resilient_agent.py` — Agente con resiliencia completa (timeout + retry + circuit breaker)
- `scripts/cost_budget_tracker.py` — Tracker de presupuesto de tokens reutilizable

---

## Prerrequisitos

- Notebooks del bloque `02_langchain/` completados
- Es útil haber leído el bloque `05_llmops/` para entender cómo se conectan el hardening y la observabilidad

---

## Por Qué Este Bloque No Es Opcional

Los sistemas de agentes fallan de maneras que los sistemas tradicionales no fallan: el modelo puede devolver formato incorrecto, la API puede dar timeout en el peor momento, el costo puede dispararse con una sola consulta mal formulada. Ninguno de esos problemas es obvio en un prototipo.

Aprender estos patrones antes del proyecto final significa que el proyecto final va a tener una base sólida, no frágil.

---

## Criterio de Avance

Antes de pasar al bloque 05, deberías poder:

- Agregar un timeout y retry a cualquier llamada al modelo en menos de 10 líneas
- Explicar cuándo un circuit breaker es mejor que un retry infinito
- Implementar un guardrail básico de input que rechace consultas fuera del dominio del sistema
