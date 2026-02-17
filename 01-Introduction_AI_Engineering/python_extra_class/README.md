# Python Extra Class

Curso intensivo de Python desde base, con foco en uso profesional para AI/ML engineering.

Si ya sabes Python basico, usa la ruta de AI/ML engineer mas abajo para ir directo a lo que importa.

## Que vas a aprender

- Fundamentos de Python hasta robustez: errores, logging, generadores, Pydantic
- OOP aplicada: modelar wrappers, orquestadores y servicios de inferencia
- Pensamiento algoritmico con ejercicios tipo LeetCode
- Validacion de contratos de datos (critico para pipelines de AI/ML)
- Entorno reproducible con `make` + `uv`

## Estructura

| Modulo | Contenido | Para que sirve |
|--------|-----------|----------------|
| `00_setup/` | Instalacion de `make`, `uv`, flujo diario | Eliminar fricciones de entorno |
| `01_programacion_python/` | Fundamentos hasta Pydantic | Base solida de Python |
| `02_oop_python/` | Modelado y diseno orientado a objetos | Software mantenible para AI/ML |
| `03_ejercicios_leetcode/` | Ejercicios algoritmicos con rubrica | Pensamiento estructurado |
| `04_ejemplos_runnable/` | Demostraciones ejecutables de temas clave | Teoria aplicada a codigo real |
| `GUIA_DE_DECISIONES.md` | Marco para elegir herramientas segun contexto | Criterio profesional |

## Notebooks interactivas

Cada modulo incluye notebooks para experimentar con el codigo paso a paso:

| Notebook | Modulo | Temas |
|----------|--------|-------|
| `01_programacion_python/Notebooks/01_fundamentos_y_estructuras.ipynb` | Programacion | Tipos, control de flujo, estructuras de datos, performance |
| `01_programacion_python/Notebooks/02_funciones_y_modularidad.ipynb` | Programacion | Funciones, scope, closures, modulos, buenas practicas |
| `01_programacion_python/Notebooks/03_robustez_y_validacion.ipynb` | Programacion | Excepciones, generadores, logging, Pydantic |
| `02_oop_python/Notebooks/01_oop_aplicada.ipynb` | OOP | Clases, encapsulamiento, herencia, composicion, dataclasses |
| `03_ejercicios_leetcode/Notebooks/01_algoritmos_interactivos.ipynb` | Algoritmos | Two Sum, Palindrome, Binary Search, Sliding Window, DP |
| `04_ejemplos_runnable/Notebooks/01_pydantic_pipeline_ai.ipynb` | Ejemplos | Pipeline completo con Pydantic, dict vs Pydantic |
| `04_ejemplos_runnable/Notebooks/02_patrones_produccion.ipynb` | Ejemplos | Context managers, generadores, logging, pipelines |

Las notebooks no requieren API keys ni dependencias externas mas alla de `pydantic`.

## Ruta recomendada (principiante)

1. `00_setup/README.md` - Configurar entorno reproducible
2. `01_programacion_python/README.md` - Fundamentos de Python
3. `04_ejemplos_runnable/README.md` - Ver los conceptos en accion
4. `02_oop_python/README.md` - OOP aplicada
5. `03_ejercicios_leetcode/README.md` - Practica algoritmica
6. `GUIA_DE_DECISIONES.md` - Criterio para elegir herramientas

## Ruta recomendada (AI/ML engineer)

Si ya manejas Python basico, ve directo a lo que impacta en AI/ML:

1. `00_setup/README.md` - Setup con `uv` (no saltear)
2. `01_programacion_python/06_modulos_y_archivos.md` - Imports y estructura
3. `01_programacion_python/08_excepciones_avanzadas.md` - Error handling robusto
4. `01_programacion_python/09_generadores_e_iteradores.md` - Procesamiento lazy
5. `01_programacion_python/11_logging_patterns.md` - Observabilidad
6. `01_programacion_python/12_pydantic.md` - Validacion de contratos de datos
7. `02_oop_python/05_composicion.md` - Composicion para wrappers y servicios
8. `02_oop_python/07_diseno_y_criterios.md` - Criterios de diseno

## Comandos

Desde `python_extra_class/`:

```bash
make help           # Ver todos los targets disponibles
make venv           # Crear entorno virtual
make sync           # Sincronizar dependencias
make test           # Ejecutar tests
make run-pydantic   # Ejecutar ejemplo de Pydantic para AI
```

## Criterio de exito

Al terminar deberias poder:

1. Escribir funciones y clases legibles, con validacion clara de inputs
2. Explicar decisiones tecnicas (no solo que funciona, sino por que)
3. Ejecutar tests y ejemplos sin pasos manuales fragiles
4. Evitar errores silenciosos en flujos de datos para AI/ML

## Validacion rapida

```bash
cd python_extra_class
make test
make run-pydantic
```

Si ambos comandos pasan, el entorno y la base curricular estan listos.
