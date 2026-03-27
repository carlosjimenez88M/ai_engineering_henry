# Practice: Prompting y Workflows

Esta carpeta propone 5 retos progresivos para dominar las estrategias de `03_prompting/` en escenarios del mundo real. La dificultad sube reto a reto: empiezas con un solo prompt bien estructurado y terminas con un flujo ReAct con herramientas y validacion.

## Objetivo

- entrenar criterio para elegir la estrategia correcta
- pasar de demos sueltas a casos que se pueden medir
- practicar validacion funcional, no solo "se ve bien"
- entender cuando usar menos complejidad y cuando si vale la pena subirla

## Orden recomendado

| Reto | Estrategia principal | Industria | Lo que entrenas |
|---|---|---|---|
| 1 | Prompt estructurado de una sola llamada | E-commerce | Cuando un solo prompt bien disenado es suficiente |
| 2 | Prompt chaining | Salud | Descomponer una tarea en pasos auditables |
| 3 | Routing | Fintech | Enviar cada caso al especialista correcto |
| 4 | CoT + feedback loop | Manufactura | Razonamiento explicito y autocritica |
| 5 | ReAct | Logistica internacional | Razonar, actuar y observar con herramientas |

## Como trabajar los retos

1. Resuelve cada reto en un script o notebook nuevo dentro de esta carpeta.
2. Manten versionados tus prompts. No reemplaces todo sin comparar resultados.
3. Construye un set pequeno de evaluacion antes de iterar.
4. Mide al menos estructura, exactitud, seguridad y utilidad de negocio.
5. Anota por que elegiste esa estrategia y por que no usaste una mas compleja.

## Validacion transversal

- La estrategia elegida debe estar justificada por el tipo de problema.
- La salida debe ser parseable o facil de auditar.
- Cada campo importante debe poder rastrearse al contexto de entrada.
- Debe existir un criterio de fallback cuando la confianza sea baja.
- La solucion debe minimizar alucinaciones y evitar inventar datos faltantes.

## Recurso util

Puedes reutilizar la idea de rubricas de `../00_common/rubrica.py`, adaptando los criterios al dominio de cada reto.
