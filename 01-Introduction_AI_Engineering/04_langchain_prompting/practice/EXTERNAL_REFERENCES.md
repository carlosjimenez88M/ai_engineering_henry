# Referencias externas usadas para afinar los retos de `04_langchain_prompting/practice`

Este archivo resume las fuentes consultadas para volver los retos de LangChain mas parecidos a implementaciones de produccion y a take-homes tecnicos donde importa arquitectura, evaluacion y mantenibilidad.

## Principios base incorporados

- **Schema-first cuando sea posible.**
  OpenAI Structured Outputs y LangChain `response_format` empujan hacia salidas tipadas y validables.
- **Prompt templates y contexto reusable antes de saltar a arquitecturas complejas.**
  La guia practica de OpenAI recomienda maximizar primero las capacidades de un solo agente y usar templates para mantener el sistema.
- **Herramientas con contratos claros.**
  Anthropic y LangChain coinciden en que los tools deben tener inputs y outputs definidos, buena documentacion y pruebas.
- **Evaluacion por componentes.**
  LangSmith recomienda separar final response, trajectory y single-step evals.

## Mapeo por reto

### Reto 1

`01_reto_rrhh_scorecard.md`

- Las fuentes de OpenAI y LangChain sobre structured output justifican que el primer reto se centre en schemas, parse rate y consistencia.
- Se mantuvo un caso de scorecard porque es un patron muy comun en entrevistas: convertir notas desordenadas en un objeto typed y evaluable.

### Reto 2

`02_reto_turismo_contexto.md`

- La guia practica de OpenAI recomienda prompt templates para manejar complejidad sin saltar demasiado pronto a sistemas multiagente.
- El caso de Lowe’s refuerza la importancia de contexto e intencion: usuarios describen proyectos o necesidades, no productos exactos.
- El reto se enfoco en construir paquetes de contexto limpios, reutilizables y trazables.

### Reto 3

`03_reto_seguros_cot_langchain.md`

- OpenAI menciona `home insurance claim` como ejemplo de workflow donde la automatizacion determinista falla.
- Oscar describe un claims assistant real que navega trazas complejas de reclamos y acelera escalaciones.
- LangSmith aporta el enfoque de evaluar pasos aislados y calidad final.

### Reto 4

`04_reto_media_factcheck_react.md`

- Anthropic y OpenAI describen agentes como loops de herramientas y feedback del entorno.
- Hebbia muestra que la investigacion multi-step sobre documentos y fuentes es ya un caso real de trabajo de alto valor.
- LangChain tools y structured output permiten bajar esa logica a un agente observable y tipado.

### Reto 5

`05_reto_procurement_router_hibrido.md`

- OpenAI usa fraude, vendor security reviews y claims como ejemplos de workflows donde diferentes niveles de complejidad conviven.
- Ironclad muestra un caso donde a veces se necesitan cambios minimos y controlados, no una reescritura total.
- Hebbia muestra que para research complejo si vale la pena orquestar varias capacidades.
- Anthropic insiste en que la complejidad debe justificarse con mejora medible; de ahi el router hibrido.

## Entrevistas tecnicas

Estos retos quedaron alineados con senales muy utiles en entrevistas:

- uso correcto de Pydantic o schemas equivalentes
- templates reutilizables y parametrizables
- tool design y docstrings utiles para el modelo
- datasets offline y evaluadores por componente
- comparacion explicita entre opciones arquitectonicas

## Fuentes

- [OpenAI: Structured outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [OpenAI: Working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [OpenAI: Lowe’s](https://openai.com/index/lowes/)
- [OpenAI: Oscar](https://openai.com/index/oscar/)
- [OpenAI: Ironclad](https://openai.com/index/ironclad/)
- [OpenAI: Hebbia](https://openai.com/index/hebbia/)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [LangChain: Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)
- [LangChain: Tools](https://docs.langchain.com/oss/python/langchain/tools)
- [LangSmith: Evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- [LangSmith: Evaluate a complex agent](https://docs.langchain.com/langsmith/evaluate-complex-agent)
