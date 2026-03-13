# Módulo 03 — Sistemas de Agentes y LLMops

Este es el módulo de cierre del programa y el más exigente. Integra todo lo aprendido en los módulos anteriores y lo lleva a un nivel de complejidad y realismo que se acerca a lo que enfrentás en producción.

La progresión está diseñada deliberadamente: no vas a usar frameworks complejos hasta que entiendas qué problema resuelven. Primero construís un agente desde cero con la API de OpenAI, después incorporás LangChain y LangGraph, luego coordinás múltiples agentes, después aprendés a blindar el sistema para producción, y finalmente cerrás con el proyecto final.

---

## Ruta de Estudio

| # | Bloque | Qué vas a aprender |
|:---:|---|---|
| 01 | [Fundamentos de Agentes](./01_intro/) | Qué es un agente, anatomía básica, cuándo NO usar agentes, costos y alucinaciones |
| 02 | [Agentes con LangChain](./02_langchain/) | Tool calling, routing condicional, validación de salida, RAG agéntico |
| 03 | [Multi-agente](./03_multi_agent/) | Orquestador-workers, handoffs, resolución de conflictos entre agentes |
| 04 | [Producción](./04_production/) | Timeouts, retries, fallbacks, guardrails, presupuesto de tokens |
| 05 | [LLMops](./05_llmops/) | Trazabilidad, monitoreo, evaluación automática, reportes |
| 06 | [Proyecto Final](./06_project_langgraph/) | Cultural Intelligence System: sistema multi-dominio completo con LangGraph + FastAPI |

---

## Por Qué Este Orden Importa

**No saltes al bloque 03 sin el bloque 01.** La razón es concreta: los errores que cometen los sistemas multi-agente (loops infinitos, handoffs rotos, costos descontrolados) son exactamente los que entendés cuando construís un agente mínimo desde cero. Sin esa base, los frameworks te ocultan los problemas hasta que aparecen en producción.

El bloque 04 tampoco es opcional. Cualquier sistema que valga la pena necesita timeouts, fallbacks y control de costos. Aprenderlo antes del proyecto final evita que el proyecto final sea frágil.

---

## Descripción de Cada Bloque

### 01 — Fundamentos de Agentes

El bloque más corto pero conceptualmente el más importante. Construís un agente ReAct con la API de OpenAI directamente, sin frameworks, para entender qué es realmente un loop agéntico. También analizás el costo real de usar agentes (tokens, latencia, alucinaciones) y entendés cuándo es mejor no usarlos.

Cierra con un notebook de panorama que sirve de puente hacia LangChain y LangGraph.

### 02 — Agentes con LangChain

Implementación progresiva de agentes más complejos: tool calling con el decorator `@tool`, routing semántico entre especialistas, validación de salida con Pydantic, y un sistema RAG agéntico completo con ChromaDB. Los datos de trabajo son cómics de Batman y Spider-Man.

### 03 — Coordinación Multi-agente

Patrones de coordinación entre agentes: orquestador que descompone tareas y despacha a workers especializados, handoffs para transferencia de control entre agentes, y mecanismos de resolución de conflictos (votación, debate, juez LLM).

### 04 — Hardening para Producción

Los patrones que hacen la diferencia entre un prototipo y un sistema confiable: timeouts con backoff exponencial, circuit breakers, fallback chains, guardrails de input/output, y control de presupuesto de tokens por sesión. Todo implementado de forma modular y reutilizable.

### 05 — LLMops Aplicado

Pipeline end-to-end de triage de tickets de soporte: inferencia, monitoreo por request (latencia, tokens, errores), evaluación offline (exactitud de routing, exactitud de priorización, juez LLM de calidad), y reportes en JSON y Markdown. Es un caso de uso realista que muestra lo que diferencia un sistema observable de uno opaco.

### 06 — Proyecto Final: Cultural Intelligence System

El proyecto integrador del curso. Es un sistema multi-agente que responde preguntas sobre tres dominios culturales (películas de Nolan, libros de Stephen King, álbumes de Miles Davis). Construido en 8 capítulos progresivos con LangGraph, con API FastAPI, tests unitarios e integración, y despliegue en Docker.

---

## Instalación y Comandos

```bash
cd 03-agents
uv sync --extra dev

# Si usás make doctor (verificación de entorno):
cp ../.env .env
```

Comandos principales:

```bash
make doctor             # Verificar configuración del entorno
make test               # Tests del módulo completo
make run-llmops         # Ejecutar pipeline LLMops
make run-llmops-nojudge # Pipeline sin juez LLM (más rápido y barato)
make notebooks-intro    # Notebooks del bloque 01
make notebooks-langchain # Notebooks del bloque 02
make notebooks-multi    # Notebooks del bloque 03
make notebooks-prod     # Notebooks del bloque 04
```

---

## Datos y Recursos

- `00_data/` — corpus de Batman y Spider-Man usado en los bloques 02 y 03
- `05_llmops/00_data/` — dataset de tickets de soporte para el bloque 05
- `05_llmops/outputs/` — artefactos generados al correr el pipeline LLMops
- `99_tests/` — tests unitarios del módulo

---

## READMEs por Bloque

Cada bloque tiene su propio README con la lista de notebooks, scripts disponibles, prerrequisitos y criterios de avance:

- [01_intro/README.md](./01_intro/README.md)
- [02_langchain/README.md](./02_langchain/README.md)
- [03_multi_agent/README.md](./03_multi_agent/README.md)
- [04_production/README.md](./04_production/README.md)
- [05_llmops/README.md](./05_llmops/README.md)
- [06_project_langgraph/README.md](./06_project_langgraph/README.md)

---

## Criterio de Avance

Al cerrar este módulo deberías poder:

- Diseñar un sistema multi-agente describiendo los nodos, aristas y condiciones de routing antes de escribir una línea de código
- Identificar qué patrones de producción son necesarios para un sistema dado y justificar por qué
- Leer las métricas de un reporte LLMops y sacar conclusiones accionables
- Desplegar el proyecto final con Docker y hacer una consulta via API
