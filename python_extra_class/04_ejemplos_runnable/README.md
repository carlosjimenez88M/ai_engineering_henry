# 04 - Ejemplos Ejecutables

Este directorio contiene ejemplos 100% ejecutables para convertir teoria en practica.

## Critica del estado inicial (y mejora aplicada)

Problema detectado:
- Habia buenos ejemplos, pero faltaba una pieza clave para AI engineering: validacion de contratos de datos.

Mejora aplicada:
- Se agrego `ejemplo_07_pydantic_ai.py`.
- Se alineo la ejecucion con `make` + `uv` para flujo reproducible.

## Archivos disponibles

### Excepciones y manejo de errores

- `ejemplo_01_excepciones.py`
- `ejemplo_02_context_managers.py`

### Generadores e iteradores

- `ejemplo_03_generadores.py`

### Logging

- `ejemplo_04_logging_basico.py`
- `ejemplo_05_logging_avanzado.py`

### Comprension vs loops

- `ejemplo_06_comprehension_performance.py`

### Contratos de datos para AI/ML

- `ejemplo_07_pydantic_ai.py`

## Ejecutar

Desde `python_extra_class/`:

```bash
make run-examples
```

O ejecutar uno puntual:

```bash
make run-pydantic
```

## Testing

```bash
make test
```

## Relacion con teoria

| Ejemplo | Documento recomendado |
|---|---|
| ejemplo_01 | `01_programacion_python/08_excepciones_avanzadas.md` |
| ejemplo_02 | `01_programacion_python/08_excepciones_avanzadas.md` |
| ejemplo_03 | `01_programacion_python/09_generadores_e_iteradores.md` |
| ejemplo_04 | `01_programacion_python/11_logging_patterns.md` |
| ejemplo_05 | `01_programacion_python/11_logging_patterns.md` |
| ejemplo_06 | `01_programacion_python/10_comprension_vs_loops.md` |
| ejemplo_07 | `01_programacion_python/12_pydantic.md` |

## Criterio de salida del modulo

- Todos los ejemplos ejecutan sin error.
- Puedes explicar que trade-off demuestra cada ejemplo.
- Puedes adaptar al menos 2 ejemplos a un caso de AI/ML real.
