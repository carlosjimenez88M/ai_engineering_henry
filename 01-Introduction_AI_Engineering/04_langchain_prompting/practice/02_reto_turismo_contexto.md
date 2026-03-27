# Reto 2: Concierge de viajes con contexto reusable

## Dificultad

Nivel 2 de 5.

## Estrategia principal

Context engineering reusable con LangChain.

## Industria

Turismo, hospitalidad y travel design.

## Escenario

Una agencia boutique arma itinerarios personalizados para viajeros frecuentes. El perfil del cliente se reutiliza en varias interacciones y no conviene reconstruirlo desde cero cada vez. Necesitas un paquete de contexto compacto, limpio y trazable.

## Objetivo

Crear un helper estilo `build_context_packet(...)` y una cadena que genere un itinerario de 2 dias usando:

- perfil del viajero
- presupuesto
- restricciones alimentarias
- ritmo del viaje
- preferencias culturales

## Lo que debes construir

- Una funcion de contexto reusable.
- Un hash o identificador del contexto generado.
- Un `ChatPromptTemplate` que consuma ese contexto sin duplicar informacion.

## Paso a paso

1. Define que campos del perfil son reutilizables y cuales solo aplican a una consulta puntual.
2. Implementa limpieza minima: dedupe de intereses, truncado de listas, normalizacion de presupuesto y eliminacion de vacios.
3. Agrega un `context_hash` para poder rastrear cambios entre versiones del contexto.
4. Diseña un template que use el paquete ya limpio y no vuelva a pedir al modelo que reorganice datos ruidosos.
5. Genera 5 perfiles distintos y evalua si el sistema responde de forma realmente personalizada.
6. Mide el tamano aproximado del contexto y ajusta un presupuesto maximo de tokens.

## Como validar que la salida es correcta

- El contexto debe ser deterministico: misma entrada, mismo `context_hash`.
- El paquete no debe contener gustos duplicados ni campos vacios.
- El itinerario debe respetar presupuesto, ritmo y restricciones.
- Al menos 2 decisiones del itinerario deben poder explicarse por senales concretas del perfil.

## Cuando usar esta estrategia

Usala cuando el mismo perfil o contexto base se reutiliza en multiples prompts o workflows.

## Cuando no usarla

No la uses si el contexto cambia por completo en cada request y el costo de encapsularlo no compensa.

## Por que se parece a produccion

OpenAI recomienda usar prompt templates y variables antes de saltar a arquitecturas mas complejas. En casos reales como Lowe’s, la calidad depende mucho de entender intencion y contexto: el usuario no llega con un SKU exacto, sino con un problema o proyecto. Este reto entrena exactamente eso, pero en formato de contexto reusable.

## Senal de entrevista

En una entrevista tecnica, aqui suelen mirar si sabes:

- separar contexto estable de contexto puntual
- controlar presupuesto de tokens
- deduplicar y normalizar informacion antes de pasarsela al modelo
- dejar trazabilidad entre perfil, contexto generado y salida final
