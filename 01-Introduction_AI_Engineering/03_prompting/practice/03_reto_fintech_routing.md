# Reto 3: Routing de incidentes en fintech

## Dificultad

Nivel 3 de 5.

## Estrategia principal

Routing hacia especialistas.

## Industria

Fintech, operaciones de pago y fraude.

## Escenario

Una fintech recibe tickets mezclados: pagos rechazados, disputas, onboarding KYC y sospechas de fraude. Un prompt unico produce respuestas mediocres porque cada problema exige politicas y tono distintos. Necesitas un router que envie cada caso al especialista correcto.

## Objetivo

Construir un sistema con:

- un router inicial
- 4 prompts especialistas
- una politica de fallback para baja confianza

## Lo que debes construir

- Un clasificador que retorne `intent`, `confidence` y `reason`.
- Especialistas para `PAGO_RECHAZADO`, `DISPUTA`, `KYC`, `FRAUDE`.
- Un formato unificado de salida para que soporte no reciba respuestas inconsistentes.

## Paso a paso

1. Prepara un dataset de al menos 24 tickets, 6 por categoria.
2. Diseña el router para que responda solo con una categoria valida, un score de confianza y una breve justificacion.
3. Define un threshold de seguridad, por ejemplo 0.70. Todo caso por debajo debe ir a revision humana.
4. Crea prompts especialistas con instrucciones, tono y limites propios de cada flujo.
5. Unifica la salida final en campos como `intent`, `priority`, `next_action`, `customer_message`, `needs_human_review`.
6. Corre una matriz de confusion para detectar las categorias mas confundidas.
7. Ajusta el router con ejemplos solo si puedes demostrar mejora medible.

## Como validar que la salida es correcta

- El routing debe acertar al menos 85% de los casos del set de evaluacion.
- Los casos de baja confianza deben escalarse, no resolverse con seguridad falsa.
- El especialista de fraude nunca debe prometer desbloqueos inmediatos.
- El especialista de KYC debe pedir documentos faltantes concretos, no mensajes genericos.
- Todas las respuestas finales deben compartir el mismo formato de salida.

## Cuando usar esta estrategia

Usala cuando tengas familias de problemas distintas, con politicas distintas y prompts especialistas claramente mejores que uno generalista.

## Cuando no usarla

No la uses si las categorias son artificiales, se solapan demasiado o el costo del router supera el beneficio.

## Extension opcional

Agrega una categoria `UNKNOWN` y mide si reduce errores graves en tickets ambiguos.
