# Reto 2: Checklist preoperatorio para pacientes

## Dificultad

Nivel 2 de 5.

## Estrategia principal

Prompt chaining.

## Industria

Clinicas, hospitales y operacion asistencial.

## Escenario

Un hospital recibe indicaciones preoperatorias escritas por distintos medicos. El lenguaje suele ser tecnico, incompleto y poco amigable para pacientes. Necesitas convertir esa informacion en una checklist clara sin perder alertas clinicas relevantes.

## Objetivo

Construir un workflow de 4 pasos:

1. extraer datos clinicos clave
2. traducirlos a lenguaje simple
3. generar una checklist accionable
4. verificar omisiones o contradicciones

## Lo que debes construir

- Un paso extractor con salida estructurada.
- Un paso traductor a lenguaje paciente.
- Un paso generador de checklist.
- Un paso verificador que revise consistencia.

## Paso a paso

1. Reune 10 instrucciones medicas ficticias pero realistas con variaciones de calidad.
2. Diseña un primer prompt que extraiga: procedimiento, fecha, medicacion relevante, restricciones, signos de alarma y dudas pendientes.
3. Diseña un segundo prompt que convierta el contenido tecnico en frases claras, sin diagnosticar ni cambiar la indicacion.
4. Diseña un tercer prompt que produzca una checklist separada en `antes`, `que llevar`, `que suspender`, `cuando llamar`.
5. Diseña un cuarto prompt validador que compare la checklist contra la extraccion inicial y marque campos faltantes como `NECESITA_CONFIRMACION`.
6. Guarda la salida intermedia de cada paso para poder depurar errores.
7. Mide donde falla el flujo: extraccion, simplificacion o validacion.

## Como validar que la salida es correcta

- Cada medicamento mencionado en la entrada debe aparecer en la extraccion o quedar explicitamente marcado como dudoso.
- La checklist final no debe agregar instrucciones nuevas que no esten en el texto original.
- Toda recomendacion ambigua debe terminar en una bandera de confirmacion, no en una afirmacion inventada.
- Un profesional no tecnico debe poder entender la version paciente en una sola lectura.
- Si cambias un paso del workflow, debes poder detectar exactamente cual mejoro o empeoro.

## Cuando usar esta estrategia

Usala cuando una sola llamada mezcle demasiadas subtareas y quieras auditar cada transformacion.

## Cuando no usarla

No la uses si solo necesitas clasificar o resumir algo corto y estable.

## Extension opcional

Agrega un quinto paso que adapte el tono de la checklist segun edad o nivel de alfabetizacion del paciente.
