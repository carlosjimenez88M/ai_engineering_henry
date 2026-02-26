# Modulo 3: Agents

Este modulo cubre el ciclo completo de agentes de IA: desde fundamentos teoricos hasta produccion, pasando por frameworks (LangChain/LangGraph), RAG agentico con ChromaDB, coordinacion multi-agente, y hardening operativo.

## Objetivo academico

Un agente en produccion no se evalua por "demo bonita", sino por:

1. **Calidad** de salida bajo distribucion real
2. **Trazabilidad** — que hizo, cuando, con que costo
3. **Evaluacion** reproducible
4. **Resiliencia** — fallo controlado, fallback, presupuestos

## Estructura

```
03-agents/
├── 01_intro/              # Fundamentos: agente minimo, workflows vs agentes, metricas
├── 02_langchain/          # LangChain/LangGraph: tools, routing, RAG agentico, agente completo
├── 03_multi_agent/        # Coordinacion: orquestador-workers, handoffs, resolucion de conflictos
├── 04_production/         # Hardening: retries, guardrails, presupuestos, alertas de calidad
├── 05_llmops/             # Ejemplo aplicado completo (triage de tickets)
├── 00_data/               # Corpus de comics Batman y Spider-Man
└── 99_tests/              # Tests unitarios para scripts
```

## Setup

```bash
cd 03-agents
uv sync --extra dev
cp ../.env .env  # Debe contener OPENAI_API_KEY
```

## Comandos

```bash
make test              # Ejecutar tests
make lint              # Linting con ruff
make doctor            # Verificar .env + DNS + conectividad OpenAI
make run-llmops        # Pipeline LLMops completo
make notebooks-all     # Ejecutar todos los notebooks
make notebooks-intro   # Solo notebooks de intro
make notebooks-langchain  # Solo notebooks de langchain
```

## Datos

El corpus usa narrativas originales de comics:

- `00_data/batman_comics.json` — 12 narrativas (~12,000 palabras)
- `00_data/spiderman_comics.json` — 12 narrativas (~12,000 palabras)
- `00_data/comics_eval.jsonl` — 10 preguntas de evaluacion con keywords

## Recorrido sugerido

1. **01_intro/** — Entender que es un agente, cuando usarlo, cuanto cuesta
2. **02_langchain/** — Implementar agentes con framework, culminando en RAG agentico
3. **03_multi_agent/** — Coordinar multiples agentes
4. **04_production/** — Preparar agentes para produccion
5. **05_llmops/** — Ver un pipeline completo en accion

## Modelo

Todos los notebooks usan `gpt-5-mini` por defecto. Configurar en `.env`.
