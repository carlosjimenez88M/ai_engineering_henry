# Reto 3: Triage de siniestros en seguros

## Dificultad

Nivel 3 de 5.

## Estrategia principal

CoT con LangChain + validator chain.

## Industria

Seguros patrimoniales y claims operations.

## Escenario

Una aseguradora recibe reportes de siniestro con fotos resumidas, notas del ajustador y extractos de poliza. El analista necesita priorizar el caso, detectar documentos faltantes y senales de fraude leve sin negar coberturas de forma apresurada.

## Objetivo

Construir una cadena de analisis y una cadena validadora que generen un `ClaimAssessment` con:

- `severity`
- `coverage_risk`
- `missing_documents`
- `fraud_signals`
- `recommended_next_step`
- `analysis_steps`

## Lo que debes construir

- Un modelo Pydantic para el analisis.
- Un `ChatPromptTemplate` de razonamiento estructurado.
- Una segunda cadena que critique cumplimiento de poliza y suficiencia de evidencia.

## Paso a paso

1. Define un esquema de salida claro y limitado.
2. Diseña una primera cadena CoT que separe hechos observados, dudas y recomendacion operativa.
3. Diseña una segunda cadena evaluadora que revise si el analisis invento condiciones de poliza o salto a conclusiones.
4. Si la validacion falla, regenera una vez con feedback concreto.
5. Crea un set de 10 siniestros con diferentes combinaciones de evidencia suficiente e insuficiente.
6. Registra parse rate, numero de reintentos y mejoras tras la validacion.

## Como validar que la salida es correcta

- Ninguna exclusion de cobertura puede aparecer si no esta en el extracto de poliza.
- `missing_documents` debe ser accionable y especifico.
- Los `fraud_signals` deben ser prudentes y no equivaler a acusaciones.
- Los casos con evidencia incompleta deben terminar en recoleccion de datos, no en cierre apresurado.
- El segundo paso debe mejorar o corregir errores reales, no solo reescribir por estilo.

## Cuando usar esta estrategia

Usala cuando el razonamiento importa, la salida debe ser tipada y ademas quieres una capa de control de calidad.

## Cuando no usarla

No la uses si la tarea solo necesita una extraccion deterministica o si debes consultar herramientas externas en tiempo real.

## Por que se parece a produccion

La guia practica de OpenAI usa `home insurance claim` como ejemplo de workflow donde reglas fijas no bastan. Oscar describe un claims assistant real que navega trazas complejas y acelera la resolucion de escalaciones. Por eso este reto combina CoT, salida tipada y una cadena validadora: es mucho mas cercano a operations real que a una demo de notebook.

## Senal de entrevista

En una entrevista tecnica, este reto muestra si puedes:

- separar hechos, dudas y recomendacion
- validar contra poliza o evidencia, no solo por estilo
- instrumentar reintentos con feedback concreto
- medir parse rate, accuracy y ganancia del segundo paso
