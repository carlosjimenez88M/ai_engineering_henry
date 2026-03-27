# Reto 5: Copiloto hibrido para procurement

## Dificultad

Nivel 5 de 5.

## Estrategia principal

Router hibrido entre cadena tipada, CoT y ReAct.

## Industria

Procurement, compras empresariales y vendor management.

## Escenario

El equipo de compras recibe solicitudes muy distintas:

- "Resume este cuestionario de proveedor"
- "Disena una estrategia de negociacion para renovar contrato"
- "Investiga si este proveedor tiene riesgo reputacional reciente"

Un solo flujo es mala idea. Necesitas un router que decida que estrategia conviene segun el trabajo.

## Objetivo

Construir un sistema con 3 rutas:

- ruta A: resumen estructurado con template
- ruta B: analisis CoT para negociacion
- ruta C: agente ReAct para investigacion externa

y una salida final unificada llamada `ProcurementDecision`.

## Lo que debes construir

- Un router con `intent`, `confidence` y `reason`.
- Tres subcomponentes con responsabilidades claras.
- Un esquema comun de salida para no exponer complejidad interna al usuario final.

## Paso a paso

1. Define un conjunto mixto de 30 a 45 casos repartidos entre las tres rutas.
2. Diseña el router para que elija una ruta y escale a humano si la confianza es baja.
3. Implementa la ruta de resumen con `ChatPromptTemplate` + salida tipada.
4. Implementa la ruta de negociacion con CoT y criterios de evaluacion.
5. Implementa la ruta de investigacion con herramientas y evidencia trazable.
6. Normaliza las tres respuestas a un solo modelo final.
7. Mide precision del router, parse rate por ruta, latencia y costo aproximado.
8. Documenta por que cada solicitud pertenece a esa ruta y no a otra.

## Como validar que la salida es correcta

- El router debe superar 85% de acierto en el set mixto.
- La ruta de resumen no debe usar herramientas innecesarias.
- La ruta de investigacion no debe responder sin evidencia externa.
- La ruta de negociacion debe mostrar razonamiento util y accionable.
- La salida final debe verse uniforme aunque venga de caminos distintos.
- Los casos ambiguos deben ir a revision humana si la confianza cae bajo tu threshold.

## Cuando usar esta estrategia

Usala cuando conviven tareas heterogeneas y el costo de usar siempre la estrategia mas compleja es demasiado alto.

## Cuando no usarla

No la uses si casi todos los casos pertenecen al mismo tipo de problema o si el router introduce mas errores que valor.

## Extension opcional

Agrega trazas por ruta y un dashboard simple para comparar costo, latencia y calidad entre estrategias.

## Por que se parece a produccion

OpenAI usa ejemplos como fraude, vendor security reviews y claims para mostrar que no todos los workflows merecen el mismo nivel de autonomia. Ironclad muestra casos donde se necesitan cambios minimos y controlados; Hebbia, en cambio, muestra tareas donde si compensa una investigacion multi-step. Este reto toma esa realidad y te obliga a elegir arquitectura por tipo de trabajo, no por moda.

## Senal de entrevista

En una entrevista tecnica, este suele ser el capstone ideal para ver si puedes:

- justificar arquitectura con trade-offs reales
- unificar salidas de rutas distintas
- evaluar router, response quality y costo por camino
- demostrar criterio para no usar siempre la opcion mas compleja
