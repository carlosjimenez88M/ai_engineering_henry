# AI Engineering (detalle operativo)

## Que cambia frente a software tradicional
- El core no es solo codigo: tambien datos, evaluaciones y comportamiento probabilistico.
- El "bug" frecuente no es un `traceback`, es degradacion de calidad o aumento de alucinaciones.
- El deployment no termina en release: exige evaluacion continua por drift de datos y cambios de modelo.

## Arquitectura recomendada (asistente ecommerce)
1. Ingestion: solicitud del usuario + metadata (canal, idioma, tipo de cliente).
2. Orquestacion:
   - clasificador de intencion (reglas o modelo ligero)
   - retrieval de politicas/documentacion (RAG)
   - decision de ruta (respuesta automatica vs escalar a humano)
3. Generacion: LLM con prompt versionado y guardrails.
4. Post-proceso:
   - validaciones (PII, toxicidad, formato)
   - score de confianza
5. Observabilidad:
   - calidad de respuesta
   - tasa de escalamiento
   - costo por ticket

## Ciclo de vida tipo ML Systems
- Discovery: definir metrica norte (resolucion automatica util) y metrica de riesgo (errores criticos).
- Build: versionar prompt, dataset de evaluacion y politicas.
- Test: combinar tests deterministas + evaluaciones basadas en casos.
- Deploy: rollout gradual por segmentos de usuarios.
- Operacion: monitoreo diario de calidad, costo y regresiones por version.
