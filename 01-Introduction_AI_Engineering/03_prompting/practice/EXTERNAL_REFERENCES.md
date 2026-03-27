# Referencias externas usadas para afinar los retos de `03_prompting/practice`

Este archivo resume las fuentes externas consultadas para volver los ejercicios mas cercanos a problemas reales de produccion y a take-homes tecnicos de AI engineering.

## Principios base incorporados

- **Empieza por la solucion mas simple y agrega complejidad solo si mejora resultados.**
  Inspirado por Anthropic, que recomienda encontrar la solucion mas simple posible antes de pasar a workflows o agentes.
- **Toda mejora debe medirse con datasets y evals.**
  Inspirado por OpenAI Evals y LangSmith, que enfatizan datasets representativos, referencias y evaluacion offline antes de desplegar.
- **Los agentes valen la pena cuando el camino no puede codificarse de antemano y hace falta usar herramientas.**
  Inspirado por Anthropic y OpenAI en sus guias de agentes.

## Mapeo por reto

### Reto 1

`01_reto_ecommerce_resenas.md`

- Zendesk y otras plataformas modernas de soporte operan a escala enorme y estan migrando de bots estaticos a agentes mas adaptativos.
- Viable muestra que el analisis de feedback no es solo resumir; el valor esta en extraer temas accionables y reducir ticket volume.
- OpenAI Evals recomienda usar datos representativos con etiquetas esperadas antes de iterar prompts.

## Reto 2

`02_reto_salud_checklist.md`

- OpenAI for Healthcare destaca templates reutilizables para instrucciones al paciente y workflows de discharge.
- Summer Health usa GPT para convertir observaciones medicas en notas claras y sin jerga, con revision clinica humana.
- Esto reforzo que el reto debia incluir traduccion a lenguaje paciente, checklist y paso explicito de revision/confirmacion.

## Reto 3

`03_reto_fintech_routing.md`

- Anthropic recomienda routing cuando existen categorias bien separadas con prompts especialistas.
- La guia practica de OpenAI usa `payment fraud analysis` como ejemplo de workflow donde las reglas solas se quedan cortas.
- Nubank describe un caso real donde IA ayuda a responder incidentes de fraude con mayor consistencia y calidad.

## Reto 4

`04_reto_manufactura_cot.md`

- Anthropic recomienda CoT cuando un humano tendria que pensar de forma explicita y evaluator-optimizer cuando existen criterios claros y valor real en iterar.
- ASQ trata el root cause analysis como un proceso metodico con tecnicas como 5 Whys, FMEA y control charts, muy cercano a este tipo de reto.
- A partir de esas fuentes, el reto se enfoco en evidencia vs inferencia, hipotesis rankeadas, acciones de contencion y rubrica.

## Reto 5

`05_reto_logistica_react.md`

- Anthropic describe agentes como loops de herramientas + feedback del entorno + stopping conditions.
- Su guia insiste en que las herramientas deben estar bien documentadas y ser dificiles de usar mal.
- OpenAI tambien recomienda agentes en workflows de decision compleja con datos no estructurados y multiples pasos.

## Entrevistas tecnicas

Los retos quedaron deliberadamente alineados con senales que suelen aparecer en entrevistas de AI/LLM engineering:

- diseno de taxonomias y schemas
- datasets de evaluacion con casos borde
- thresholds de confianza y fallback humano
- separacion entre evidencia, inferencia y accion
- tool design, traces, trajectory evaluation y stopping conditions

## Fuentes

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI: Working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [OpenAI: Introducing OpenAI for Healthcare](https://openai.com/index/openai-for-healthcare/)
- [OpenAI: Summer Health](https://openai.com/index/summer-health/)
- [OpenAI: Zendesk](https://openai.com/index/zendesk/)
- [OpenAI: Nubank](https://openai.com/index/nubank/)
- [OpenAI: Viable](https://openai.com/index/viable/)
- [ASQ: What is Root Cause Analysis?](https://asq.org/quality-resources/root-cause-analysis)
