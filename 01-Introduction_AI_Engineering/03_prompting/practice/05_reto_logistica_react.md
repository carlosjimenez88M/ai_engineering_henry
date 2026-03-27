# Reto 5: Investigacion de retrasos en logistica internacional

## Dificultad

Nivel 5 de 5.

## Estrategia principal

ReAct.

## Industria

Logistica internacional y supply chain.

## Escenario

Un centro de control recibe preguntas como: "Por que el envio MX-2047 esta detenido y que deberiamos hacer hoy?". La respuesta no esta completa en un solo contexto. Debes consultar varias fuentes, observar resultados intermedios y decidir el siguiente paso. Ese es el terreno natural de ReAct.

## Objetivo

Construir un agente que combine razonamiento y acciones sobre herramientas simuladas o reales como:

- tracking del envio
- estado aduanero
- clima o disrupciones
- SLA del cliente

## Lo que debes construir

- Un formato de accion con `thought`, `action`, `action_input`, `observation`.
- Al menos 4 herramientas.
- Un criterio claro de parada para llegar a la respuesta final.

## Paso a paso

1. Define las herramientas como funciones simples y controladas. Empieza con stubs si hace falta.
2. Diseña un prompt que fuerce al agente a pensar, actuar, observar y decidir el siguiente paso.
3. Limita el numero maximo de iteraciones para evitar loops inutiles.
4. Exige que la respuesta final contenga diagnostico, acciones para hoy, riesgos y evidencia usada.
5. Agrega manejo de error para una herramienta caida o una observacion vacia.
6. Compara el comportamiento contra una version CoT sin herramientas y explica por que ReAct gana aqui.
7. Registra el trace completo para inspeccionar decisiones malas.

## Como validar que la salida es correcta

- Cada afirmacion importante debe estar respaldada por una observacion de una herramienta.
- El agente no debe llamar herramientas irrelevantes solo porque existen.
- Si faltan datos, la salida final debe declararlo y pedir el siguiente dato critico.
- El plan de accion debe respetar el SLA del cliente y la causa identificada.
- El trace debe permitir reconstruir por que llego a esa conclusion.

## Cuando usar esta estrategia

Usala cuando la ruta para resolver el problema no se conoce de antemano y necesitas consultar herramientas o fuentes externas.

## Cuando no usarla

No la uses si todo lo necesario ya viene en el prompt o si el problema puede resolverse con un workflow fijo.

## Extension opcional

Implementa un verificador final que revise si las acciones recomendadas realmente se derivan de las observaciones recolectadas.
