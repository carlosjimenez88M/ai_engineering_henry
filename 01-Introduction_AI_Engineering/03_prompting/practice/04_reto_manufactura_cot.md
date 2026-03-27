# Reto 4: Analisis de defectos en manufactura

## Dificultad

Nivel 4 de 5.

## Estrategia principal

Chain of Thought con feedback loop.

## Industria

Manufactura y quality assurance.

## Escenario

Una planta recibe reportes de defectos con datos de sensores, notas de operario, lote, turno y fallas historicas. El equipo necesita una hipotesis de causa raiz y un plan de contencion. Aqui ya no basta con clasificar: hace falta razonamiento explicito, comparacion de evidencias y autocorreccion.

## Objetivo

Diseñar un flujo CoT que produzca:

- `evidence_signals`
- `hypotheses_ranked`
- `root_cause_candidate`
- `containment_actions`
- `missing_data`
- `self_check`

## Lo que debes construir

- Un prompt CoT zero-shot.
- Una rubrica de evaluacion del analisis.
- Un feedback loop que regenere si la calidad cae bajo tu threshold.

## Paso a paso

1. Crea 8 casos de defecto con causa raiz conocida o consensuada por ti.
2. Define los pasos de razonamiento que esperas: leer senales, conectar patrones, rankear hipotesis, revisar contradicciones y proponer accion.
3. Obliga a separar evidencia observada de inferencia. Esa frontera es clave.
4. Ejecuta un baseline sin CoT y compara contra una version con pasos explicitos.
5. Implementa una rubrica con criterios como trazabilidad, coherencia causal, utilidad operativa y prudencia.
6. Si el score total cae bajo tu threshold, reintenta con feedback concreto del evaluador.
7. Documenta el costo adicional en tokens y en latencia, y justifica si vale la pena.

## Como validar que la salida es correcta

- Cada hipotesis debe apoyarse en senales reales del caso.
- La causa raiz propuesta debe coincidir con tu etiqueta esperada en la mayoria de casos de evaluacion.
- `containment_actions` debe ser util hoy, no una lista vaga de buenas practicas.
- El modelo debe reconocer datos faltantes cuando la evidencia no alcance.
- El feedback loop debe mejorar al menos un criterio de la rubrica en los casos rechazados.

## Cuando usar esta estrategia

Usala cuando el problema sea ambiguo, de varias senales, y te convenga ver el razonamiento para auditar o mejorar.

## Cuando no usarla

No la uses si la respuesta puede salir de una regla fija, una consulta SQL o una funcion deterministica.

## Extension opcional

Convierte tu CoT zero-shot en few-shot y compara consistencia, costo y latencia.

## Por que se parece a produccion

Este reto es una inferencia informada por dos familias de fuentes. Anthropic recomienda CoT para problemas donde un humano realmente tendria que pensar paso a paso y evaluator-optimizer cuando existen criterios claros y valor real en iterar. Por su lado, ASQ trata el root cause analysis como un proceso metodico con tecnicas como 5 Whys, FMEA y control charts. El resultado es un ejercicio muy cercano a analisis de calidad y operaciones en plantas reales.

## Senal de entrevista

En una entrevista tecnica, este reto revela si puedes:

- separar evidencia observada de inferencia
- construir una rubrica util, no solo subjetiva
- cerrar el loop entre generacion, evaluacion y mejora
- medir si la segunda iteracion realmente sube la calidad
