# 05 — LLMops Aplicado

Este bloque presenta un pipeline completo de LLMops aplicado a un caso concreto: triage automático de tickets de soporte con `gpt-4o-mini`. No es un ejercicio teórico — es el tipo de sistema que encontrás en equipos reales que usan LLMs en producción.

La diferencia entre un sistema de inferencia y un sistema observable está en la instrumentación. Acá aprendés a instrumentar, medir y evaluar.

---

## Qué Incluye el Pipeline

El pipeline tiene cuatro capas que se ejecutan de principio a fin:

**1. Inferencia**: cada ticket pasa por tres nodos — clasificación de dominio (routing), asignación de prioridad, y generación de respuesta sugerida.

**2. Monitoring por request**: por cada ticket se registra latencia, tokens consumidos, errores encontrados y salida generada.

**3. Evaluación offline**: comparación contra etiquetas ground truth para exactitud de routing, exactitud de priorización, y evaluación de calidad de respuesta con un juez LLM (score 1-5).

**4. Reportes**: los resultados se exportan en JSON (para ingesta automatizada) y Markdown (para revisión humana).

---

## Cómo Ejecutar

```bash
cd 03-agents
uv sync
cp ../.env .env
make doctor          # Verificar que el entorno esté configurado
make run-llmops      # Pipeline completo con juez LLM
```

Si querés una ejecución más rápida y barata (sin el juez LLM):

```bash
make run-llmops-nojudge
```

---

## Artefactos Generados

Después de correr el pipeline, encontrás estos archivos en `outputs/`:

- `predictions.jsonl` — predicciones del modelo por ticket
- `monitoring_events.jsonl` — eventos de monitoreo (latencia, tokens, errores)
- `evaluation_report.json` — reporte completo en formato estructurado
- `evaluation_report.md` — reporte legible para revisión humana

---

## Lo que Este Bloque Enseña sobre Evaluación

La precisión de clasificación es una métrica necesaria pero no suficiente para producción. Un sistema puede clasificar bien el 90% de los tickets pero ser inutilizable si: los formatos de salida son inestables, el costo por ticket es prohibitivo, la tasa de fallback es alta, o las respuestas sugeridas no son útiles para el agente humano que las recibe.

Este bloque mide las cuatro dimensiones juntas porque en producción las cuatro importan.

---

## Prerrequisitos

- `OPENAI_API_KEY` configurada en `.env`
- `make doctor` corrido sin errores desde `03-agents/`
