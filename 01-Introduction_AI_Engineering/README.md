# Módulo 01 — Introducción a AI Engineering

Este módulo es el punto de partida del programa. La idea no es aprender herramientas: es entender el cambio de paradigma que implica construir software basado en modelos de lenguaje. Arrancamos desde Python profesional, construimos una API web con FastAPI, y progresivamente incorporamos prompting, orquestación con LangChain y LangGraph, hasta cerrar con un sistema RAG funcional.

---

## Ruta de Estudio

El contenido debe recorrerse en orden. Cada bloque construye sobre el anterior.

| # | Bloque | Qué vas a aprender |
|:---:|---|---|
| 00 | [Python Extra Class](./00_python_extra_class/) | Python robusto para AI/ML: Pydantic, OOP, error handling, entornos reproducibles |
| 01 | [FastAPI](./01_fastapi/) | Construcción de APIs web asíncronas para exponer sistemas de IA |
| 02 | [Introducción](./02_introduction/) | La diferencia entre Software Engineering clásico y AI Engineering |
| 03 | [Prompting](./03_prompting/) | Técnicas de prompting: introducción, chaining, routing, CoT y ReAct |
| 04 | [LangChain Prompting](./04_langchain_prompting/) | Las mismas técnicas de prompting implementadas con LangChain |
| 05 | [LangGraph Workflows](./05_langchain_langgraph/) | Workflows con estado, routing, paralelización y feedback loops |
| 06 | [RAG](./06_rags/) | Retrieval-Augmented Generation: vector stores, pipeline completo y patrones |
| 07 | [Proyecto Integrador](./07_project/) | Sistema con routing semántico, RAG y exposición via FastAPI |

> **Sobre el bloque 00**: si ya manejás Python intermedio, podés saltear `00_python_extra_class/` e ir directo al bloque 01. Igualmente, no saltees el `00_setup/` dentro de ese bloque: la configuración del entorno con `uv` se usa en todo el curso.

---

## Qué Construís en Este Módulo

Al finalizar el bloque 07 tenés un sistema funcional que:

- Recibe una pregunta del usuario via API HTTP
- Clasifica la pregunta y la enruta al agente especialista correcto
- Busca contexto relevante en una base vectorial
- Genera una respuesta coherente usando un LLM
- Expone todo esto como un endpoint documentado en FastAPI

Es un sistema pequeño pero completo, y es la base arquitectural de todo lo que viene en los módulos 02 y 03.

---

## Descripción de Cada Bloque

### 00 — Python Extra Class

Nivelación intensiva para estudiantes que necesitan reforzar Python antes de entrar al curso. Si ya sabés Python básico, podés ir directo al setup y después saltar al bloque 01. Si nunca trabajaste con Pydantic, OOP aplicada o manejo robusto de errores, este bloque vale la pena.

Incluye notebooks ejecutables, ejercicios tipo LeetCode y una guía de decisiones técnicas. Nada requiere API keys.

### 01 — FastAPI

Construcción progresiva de una API web completa: desde endpoints básicos hasta autenticación JWT, base de datos con SQLAlchemy 2.0, migraciones con Alembic, tests con pytest y frontend con Jinja2. Seis secciones con comandos individuales para levantar y probar cada parte.

### 02 — Introducción a AI Engineering

El bloque conceptual del módulo. Compara el flujo de trabajo del Software Engineering tradicional contra el AI Engineering, identificando qué cambia cuando el comportamiento del sistema es estocástico. Es una clase de contexto, no de código, pero es fundamental para entender las decisiones de diseño del resto del curso.

### 03 — Prompting

Ingeniería de prompts aplicada: no es un listado de "tips", es una sistemática. Cubre prompt introduction, prompt chaining, routing condicional, Chain of Thought y ReAct. Todos los patrones están implementados con la API de OpenAI directamente, sin frameworks, para que quede claro qué hace cada uno.

### 04 — LangChain Prompting

Los mismos patrones del bloque anterior, ahora implementados con LangChain. El objetivo es entender qué abstrae el framework y por qué eso importa para mantener el código a largo plazo.

### 05 — LangGraph Workflows

Introducción a los grafos de estado como primitiva de orquestación. Cubre workflows de chaining, paralelización, orchestrator-worker, evaluator-optimizer, routing y agent feedback. Es el primer contacto con el paradigma que se desarrolla completamente en el módulo 03.

### 06 — RAG (Retrieval-Augmented Generation)

Pipeline completo de RAG: carga de documentos, chunking, generación de embeddings, almacenamiento en vector store, recuperación y síntesis de respuesta. También incluye patrones avanzados como multi-query y ensemble retrievers.

### 07 — Proyecto Integrador

El consolidador del módulo. Integra FastAPI, routing semántico, RAG y LangGraph en un sistema cohesivo. Es el proyecto que entregás al cerrar el módulo 01.

---

## Instalación y Comandos

```bash
cd 01-Introduction_AI_Engineering
uv sync --extra dev
```

Comandos principales:

```bash
make test-all              # Correr todos los tests del módulo
make run-ai                # Ejemplo de AI Engineering
make run-se                # Ejemplo de Software Engineering (comparativo)
make run-notebooks         # Ejecutar notebooks del módulo
make run-notebooks-langchain    # Notebooks de LangChain
make run-notebooks-langgraph    # Notebooks de LangGraph
make run-notebooks-rag          # Notebooks de RAG
```

---

## Archivos Importantes

- `pyproject.toml` — dependencias propias del módulo 01
- `.env.example` — configuración base para los ejemplos con OpenAI
- `Makefile` — todos los comandos disponibles (`make help` para verlos)

---

## Criterio de Avance

Estás listo para el módulo 02 cuando podás responder estas preguntas sin mirar el código:

- ¿Qué diferencia hay entre un workflow y un agente?
- ¿Cuándo tiene sentido usar prompt chaining en lugar de un solo prompt?
- ¿Qué problema resuelve el RAG y cuándo NO lo usarías?
- ¿Qué es un grafo de estado y para qué sirve en LangGraph?
