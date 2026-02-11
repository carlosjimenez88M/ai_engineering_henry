# 01 - Programacion en Python

Meta de este modulo: que puedas escribir codigo Python correcto, legible y util para pipelines de AI/ML.

## Critica del estado inicial (y mejora aplicada)

Problema detectado:
- La ruta estaba bien para sintaxis, pero faltaba puente explicito hacia casos AI/ML.
- Faltaba un cierre practico sobre contratos de datos.

Mejora aplicada:
- Se agrego `12_pydantic.md` para validacion de entradas/salidas en sistemas de inferencia.
- Se dejo una secuencia de aprendizaje por niveles (base -> robustez -> AI/ML).

## Ruta sugerida

1. `01_fundamentos.md`
2. `02_control_de_flujo.md`
3. `03_funciones.md`
4. `04_estructuras_de_datos.md`
5. `05_errores_y_debug.md`
6. `06_modulos_y_archivos.md`
7. `07_buenas_practicas.md`
8. `08_excepciones_avanzadas.md`
9. `09_generadores_e_iteradores.md`
10. `10_comprension_vs_loops.md`
11. `11_logging_patterns.md`
12. `12_pydantic.md`
13. `ejercicios_guided.md`

## Resultado de salida del modulo

Al terminar deberias poder:

- Explicar por que una estructura de datos es mejor que otra para un caso dado.
- Identificar errores comunes y agregar manejo robusto sin esconder bugs.
- Diseñar funciones modulares y testeables.
- Validar payloads con `pydantic` antes de pasar datos a un modelo.

Regla de oro: si no puedes explicar en una frase por que existe una linea, todavia no la dominas.
