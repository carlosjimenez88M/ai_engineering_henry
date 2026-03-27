# Reto 1: Scorecard de entrevistas para RRHH

## Dificultad

Nivel 1 de 5.

## Estrategia principal

`ChatPromptTemplate` + `with_structured_output`.

## Industria

Recursos humanos y reclutamiento.

## Escenario

Cada entrevistador deja notas en formatos distintos. El equipo de hiring necesita un scorecard consistente para decidir a quien pasar a la siguiente ronda. Es un caso ideal para templates repetibles y salidas tipadas.

## Objetivo

Construir una cadena que transforme notas libres en un objeto `CandidateScorecard` con:

- `candidate_name`
- `role`
- `scores`
- `strengths`
- `risks`
- `follow_up_questions`
- `recommendation`

## Lo que debes construir

- Un modelo Pydantic para la salida.
- Un `ChatPromptTemplate` con variables claras.
- Un pipeline que procese al menos 12 entrevistas.

## Paso a paso

1. Define el modelo Pydantic antes de escribir el prompt.
2. Diseña un template con instrucciones estables y placeholders para notas, rol y seniority esperado.
3. Obliga a que cada riesgo y fortaleza salga de evidencia presente en las notas.
4. Usa `with_structured_output` para validar la respuesta.
5. Corre el pipeline sobre un lote y registra cuantos casos parsean sin correccion.
6. Compara esta implementacion contra una version de string libre y muestra por que la tipada es mas mantenible.

## Como validar que la salida es correcta

- El modelo debe parsear en el 100% de los casos del set.
- Ninguna fortaleza o riesgo debe inventar experiencia no mencionada.
- La recomendacion final debe ser consistente con los scores.
- Las preguntas de seguimiento deben cerrar dudas reales, no repetir lo ya respondido.

## Cuando usar esta estrategia

Usala cuando repites una misma tarea de extraccion o scoring y quieres outputs estables.

## Cuando no usarla

No la uses si necesitas consultar herramientas, navegar varias fuentes o decidir el siguiente paso dinamicamente.

## Por que se parece a produccion

Aunque el dominio aqui sea RRHH, el patron es totalmente de produccion: tomar notas desordenadas y convertirlas en un objeto typed y validable. OpenAI y LangChain empujan este enfoque con Structured Outputs y `response_format`, porque automatizar decisiones encima de texto libre sin schema suele romperse rapido.

## Senal de entrevista

En una entrevista tecnica, este reto deja ver si puedes:

- modelar bien un schema
- sostener parse rate alto
- evitar contradicciones entre scores, riesgos y recomendacion
- mostrar por que una salida tipada es mejor que un bloque de texto libre
