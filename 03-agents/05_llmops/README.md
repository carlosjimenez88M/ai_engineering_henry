# LLMops: Ejemplo End-to-End

Caso aplicado: triage de tickets de soporte con `gpt-5-mini`.

## Que incluye

1. Pipeline de inferencia (routing + prioridad + respuesta sugerida).
2. Monitoring por request (latencia, tokens, errores, salida).
3. Evaluacion offline:
- Exactitud de `route`.
- Exactitud de `priority`.
- Juez LLM opcional (score 1-5 de calidad de respuesta).
4. Reportes en JSON y Markdown.

## Ejecutar

```bash
cd 03-agents
uv sync
cp ../.env .env
make doctor
make run-llmops
```

Modo sin juez LLM (mas rapido y barato):

```bash
make run-llmops-nojudge
```

## Artefactos

- `05_llmops/outputs/predictions.jsonl`
- `05_llmops/outputs/monitoring_events.jsonl`
- `05_llmops/outputs/evaluation_report.json`
- `05_llmops/outputs/evaluation_report.md`

## Criterio tecnico

La precision de clasificacion no basta para produccion. Se miden tambien:

1. Estabilidad de formato.
2. Coste por ticket.
3. Tasa de fallback.
4. Calidad util de la respuesta para usuario final.
