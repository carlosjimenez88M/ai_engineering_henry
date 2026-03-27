# Reto 1: Triage de resenas en e-commerce

## Dificultad

Nivel 1 de 5.

## Estrategia principal

Prompt estructurado de una sola llamada.

## Industria

E-commerce y customer support.

## Escenario

Un marketplace recibe cientos de resenas al dia. El equipo de operaciones necesita transformar cada resena en un ticket util para soporte sin pasar por un flujo complejo. Aqui el objetivo es demostrar que un solo prompt bien disenado puede resolver una tarea acotada y repetitiva.

## Objetivo

Convertir una resena libre y algunos metadatos de la orden en un JSON con:

- `sentiment`
- `issue_type`
- `urgency`
- `one_line_summary`
- `draft_reply`

## Lo que debes construir

- Un prompt con las 5 capas: role, task, output format, examples opcionales y context.
- Un esquema de salida estable.
- Un set de evaluacion de al menos 15 resenas con etiquetas esperadas.

## Paso a paso

1. Define 4 categorias de problema utiles para negocio, por ejemplo `LOGISTICA`, `CALIDAD_PRODUCTO`, `COBRO`, `RIESGO_REPUTACIONAL`.
2. Diseña un `system_prompt` que deje claro el rol del agente, sus limites y el formato exacto de salida.
3. Incluye en el `user_prompt` solo el contexto necesario: texto de la resena, pais, categoria del producto y estado de la orden.
4. Obliga al modelo a responder en JSON y deja claro que no debe inventar politicas ni compensaciones.
5. Ejecuta un baseline con un prompt vago y comparalo contra tu prompt estructurado.
6. Agrega 3 casos borde: sarcasmo, cliente agresivo y comentario ambiguo.
7. Documenta por que no necesitas chaining ni routing en este problema.

## Como validar que la salida es correcta

- El JSON debe parsear en el 100% de los casos.
- `issue_type` debe coincidir con tu etiqueta esperada en al menos 85% del set.
- `urgency` debe subir a `HIGH` en casos con fraude, insultos publicos o producto riesgoso.
- `one_line_summary` debe capturar el problema principal en maximo 20 palabras.
- `draft_reply` no debe prometer reembolsos, cupones o acciones no mencionadas en politicas.
- En resenas negativas, la respuesta debe incluir empatia y un siguiente paso concreto.

## Cuando usar esta estrategia

Usala cuando la tarea sea estable, el contexto sea pequeno y la salida final pueda generarse de una vez.

## Cuando no usarla

No la uses si necesitas consultar fuentes externas, aplicar especialistas distintos o depurar razonamiento paso a paso.

## Extension opcional

Agrega una segunda salida llamada `needs_human_review` y evalua si mejora la seguridad operacional.

## Por que se parece a produccion

Este reto fue afinado pensando en equipos reales de soporte y customer insights. OpenAI muestra casos como Zendesk, donde la atencion al cliente opera a escala enorme, y Viable, donde el valor no esta solo en resumir texto sino en convertir feedback libre en temas y acciones utiles para negocio.

## Senal de entrevista

En una entrevista tecnica, aqui suelen mirar si sabes:

- disenar una taxonomia util y no arbitraria
- exigir salida estructurada estable
- crear un set de evaluacion con etiquetas esperadas
- definir cuando escalar a humano en vez de responder con exceso de confianza
