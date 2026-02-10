# Python Extra Class 🐍

**Una clase intensiva de Python para developers que quieren dominar el lenguaje y prepararse para entrevistas técnicas.**

Este material está pensado como una clase extra intensiva. **Filosofía:** teoría mínima, código claro, explicar el _porqué_ de cada decisión. No es un libro; es un mapa práctico con código 100% ejecutable.

---

## 📚 Estructura completa

### Módulo 1: Programación Python (`01_programacion_python/`)

**Fundamentos:**
1. Variables y tipos de datos
2. Control de flujo (if, for, while, comprehensions)
3. Funciones
4. Estructuras de datos (list, dict, set, tuple)

**Manejo de errores:**
5. Errores y debug (básico)
6. Buenas prácticas
7. **[NUEVO]** Testing básico con pytest

**Avanzado:**
8. **[NUEVO]** Excepciones avanzadas (try/except/else/finally, custom exceptions, context managers)
9. **[NUEVO]** Generadores e iteradores (yield, generator expressions, memory efficiency)
10. **[NUEVO]** Comprensión vs loops (cuándo usar qué, performance, readability)
11. **[NUEVO]** Logging patterns (niveles, handlers, formatters, structured logging)

---

### Módulo 2: OOP Python (`02_oop_python/`)

1. Clases y objetos
2. Herencia
3. Métodos especiales
4. Properties
5. Dataclasses
6. Composición vs herencia
7. Patrones de diseño básicos
8. **[NUEVO]** Logging en clases (logger por clase, lifecycle logging, testing con caplog)

---

### Módulo 3: Ejercicios LeetCode (`03_ejercicios_leetcode/`)

**10 básicos + 2 intermedios** con soluciones detalladas:

**Básicos:**
1. Two Sum (hash map)
2. Valid Palindrome (two pointers)
3. Reverse Linked List (iteración)
4. Climbing Stairs (DP)
5. Majority Element (Boyer-Moore)
6. Intersection of Two Arrays II (hash map)
7. Single Number (XOR)
8. Move Zeroes (two pointers)
9. Roman to Integer (lookahead)
10. Binary Search

**Intermedios:**
11. Group Anagrams (hashing)
12. Longest Substring Without Repeating Characters (sliding window)

**Incluye:**
- ✅ Explicación paso a paso
- ✅ Invariantes y complejidad
- ✅ **[NUEVO]** Código ejecutable (`leetcode_runnable.py`)
- ✅ **[NUEVO]** Tests completos (`test_leetcode.py` con 67 tests)
- ✅ **[NUEVO]** Casos límite y casos de prueba
- ✅ **[NUEVO]** Preguntas de seguimiento para entrevistas
- ✅ **[NUEVO]** Soluciones alternativas con trade-offs
- ✅ **[NUEVO]** Errores comunes en entrevistas

---

### Módulo 4: Ejemplos Ejecutables (`04_ejemplos_runnable/`) **[NUEVO]**

**Todo el código es 100% ejecutable.** Corre los ejemplos para ver los conceptos en acción:

- `ejemplo_01_excepciones.py` - Try/except/else/finally, custom exceptions, LBYL vs EAFP
- `ejemplo_02_context_managers.py` - `__enter__`/`__exit__`, @contextmanager, transacciones
- `ejemplo_03_generadores.py` - Generators, yield, memory comparison, pipelines
- `ejemplo_04_logging_basico.py` - Configuración, niveles, handlers, formatters
- `ejemplo_05_logging_avanzado.py` - RotatingFileHandler, JSON logging, performance
- `ejemplo_06_comprehension_performance.py` - Benchmarks, bytecode, memory profiling

Ver `04_ejemplos_runnable/README.md` para detalles.

---

### Guía de Decisiones (`GUIA_DE_DECISIONES.md`) **[NUEVO]**

**La herramienta más importante del curso.** Árboles de decisión para saber **CUÁNDO** usar cada herramienta:

1. Exception handling - ¿Cómo manejar errores?
2. Logging vs Print vs Raise - ¿Cómo reportar problemas?
3. List comprehension vs For loop - ¿Cómo iterar?
4. Generators vs Lists - ¿Cómo almacenar secuencias?
5. Data structures - ¿Qué estructura usar?
6. Custom exceptions vs Built-in - ¿Crear excepciones propias?
7. Logging levels - ¿Qué nivel de log usar?
8. Context managers - ¿Cuándo crear uno?
9. Dataclass vs Regular class - ¿Cómo definir clases?
10. Resumen visual - Mapa mental completo

**Lee este documento cuando no estés seguro qué herramienta usar.**

---

## 🎯 Cómo usar este material

### Opción 1: Path rápido (Weekend Intensivo - 2 días)

**Objetivo:** Conocimientos esenciales para entrevistas.

**Día 1 (Sábado - 8 horas):**
- ✅ Lee `GUIA_DE_DECISIONES.md` completo (1h)
- ✅ Revisa `01_programacion_python/02_control_de_flujo.md` (0.5h)
- ✅ Lee `01_programacion_python/10_comprension_vs_loops.md` (0.5h)
- ✅ Ejecuta `04_ejemplos_runnable/ejemplo_06_comprehension_performance.py` (0.5h)
- ✅ Resuelve LeetCode 1-5 (Básicos) sin mirar soluciones (2h)
- ✅ Revisa soluciones y lee las alternativas (1.5h)
- ✅ Ejecuta `python 03_ejercicios_leetcode/leetcode_runnable.py` (0.5h)
- ✅ Lee `01_programacion_python/08_excepciones_avanzadas.md` (1.5h)

**Día 2 (Domingo - 8 horas):**
- ✅ Resuelve LeetCode 6-10 (Básicos) (2.5h)
- ✅ Resuelve LeetCode 11-12 (Intermedios) (2.5h)
- ✅ Lee `02_oop_python/01_clases_y_objetos.md` y `05_dataclasses.md` (1h)
- ✅ Ejecuta todos los ejemplos en `04_ejemplos_runnable/` (1h)
- ✅ Repasa `GUIA_DE_DECISIONES.md` haciendo resumen mental (1h)

**Resultado:** Listo para entrevistas básicas/intermedias.

---

### Opción 2: Path completo (2 semanas)

**Objetivo:** Dominio profundo de Python + preparación completa para entrevistas.

**Semana 1: Fundamentos + Avanzado**

| Día | Tema | Tiempo | Actividad |
|-----|------|--------|-----------|
| Lun | Setup + Fundamentos | 2h | `01_programacion_python/01-04` |
| Mar | Errores y debug | 2h | `05_errores_y_debug.md` + `08_excepciones_avanzadas.md` |
| Mié | Generators | 2h | `09_generadores_e_iteradores.md` + `ejemplo_03_generadores.py` |
| Jue | Comprehensions | 2h | `10_comprension_vs_loops.md` + `ejemplo_06_comprehension_performance.py` |
| Vie | Logging | 2h | `11_logging_patterns.md` + `ejemplo_04_logging_basico.py` |
| Sáb | OOP Completo | 4h | Todo `02_oop_python/` |
| Dom | Repaso + Guía | 2h | `GUIA_DE_DECISIONES.md` + revisar conceptos confusos |

**Semana 2: Algoritmos + Entrevistas**

| Día | Tema | Tiempo | Actividad |
|-----|------|--------|-----------|
| Lun-Mar | LeetCode 1-5 | 4h | Resolver + revisar alternativas |
| Mié-Jue | LeetCode 6-10 | 4h | Resolver + revisar alternativas |
| Vie | LeetCode 11-12 | 3h | Resolver + revisar alternativas |
| Sáb | Mock interviews | 4h | Resolver 5 problemas random en 2h, sin mirar soluciones |
| Dom | Repaso final | 2h | `pytest -v`, revisar guías, hacer resumen personal |

**Resultado:** Listo para entrevistas senior + código de producción.

---

### Opción 3: Path entrevista (Foco algoritmos - 1 semana)

**Objetivo:** Máxima preparación para entrevistas técnicas.

**Día 1-2:** Teoría esencial
- ✅ `GUIA_DE_DECISIONES.md` completo
- ✅ `01_programacion_python/04_estructuras_de_datos.md`
- ✅ Ejecuta `pytest 03_ejercicios_leetcode/test_leetcode.py -v`

**Día 3-5:** Algoritmos básicos
- ✅ Resuelve LeetCode 1-10 (uno por uno, sin mirar soluciones)
- ✅ Tiempo límite: 30 min por problema
- ✅ Después de resolver (o rendirte), lee la solución + alternativas
- ✅ Anota patrones comunes (hash map, two pointers, etc.)

**Día 6-7:** Algoritmos intermedios + repaso
- ✅ Resuelve LeetCode 11-12
- ✅ Re-resuelve los 5 problemas que más te costaron
- ✅ Mock interview: 3 problemas random en 90 minutos

**Resultado:** Confianza para entrevistas de coding.

---

## ✅ Verificar que todo funciona

### Opción 1: Tests completos (recomendado)

```bash
cd python_extra_class

# Tests de LeetCode (67 tests)
pytest 03_ejercicios_leetcode/test_leetcode.py -v

# Tests de ejemplos
pytest 04_ejemplos_runnable/test_ejemplos.py -v

# Todos los tests
pytest -v
```

**Output esperado:**
```
============================== 67 passed in 0.14s ==============================
```

### Opción 2: Ejecutar ejemplos individuales

```bash
# Excepciones
python 04_ejemplos_runnable/ejemplo_01_excepciones.py
python 04_ejemplos_runnable/ejemplo_02_context_managers.py

# Generators
python 04_ejemplos_runnable/ejemplo_03_generadores.py

# Logging
python 04_ejemplos_runnable/ejemplo_04_logging_basico.py
python 04_ejemplos_runnable/ejemplo_05_logging_avanzado.py

# Comprehensions
python 04_ejemplos_runnable/ejemplo_06_comprehension_performance.py
```

### Opción 3: Ejecutar LeetCode problems

```bash
python 03_ejercicios_leetcode/leetcode_runnable.py
```

**Output esperado:**
```
======================================================================
✓ TODOS LOS 12 PROBLEMAS PASARON
======================================================================
```

---

## 🎓 Filosofía del curso

### 1. Código ejecutable
**Todo snippet debe poder correrse.** No hay fragmentos con `...` o código incompleto.

### 2. Por qué antes que qué
Cada concepto explica **por qué importa** antes de mostrar el código.

### 3. Invariantes
Cada algoritmo declara sus invariantes. **Invariante = condición que debe ser cierta en cada paso.**

### 4. Complejidad siempre
Todos los algoritmos incluyen análisis de complejidad tiempo/espacio.

### 5. Práctica real
Ejemplos de situaciones reales, no toy problems desconectados de la realidad.

### 6. Tests incluidos
Si no tiene tests, no está completo. Todos los problemas y ejemplos tienen tests.

---

## 📊 Nivel objetivo

### Entrada (prerequisitos)
- ✅ Python básico: variables, funciones, if/for
- ✅ Saber usar terminal/command line
- ✅ Editor de texto o IDE instalado
- ✅ Python 3.8+ instalado

### Salida (qué lograrás)
- ✅ Listo para entrevistas intermediate+ en empresas tech
- ✅ Escribes código de producción con manejo robusto de errores
- ✅ Entiendes CUÁNDO usar cada herramienta, no solo CÓMO
- ✅ Puedes explicar complejidad y trade-offs de tus decisiones
- ✅ Dominas patrones de algoritmos comunes (hash map, two pointers, DP básico)

---

## 🔧 Setup

### Instalación

```bash
# Clonar o descargar el repositorio
cd python_extra_class

# Instalar dependencias (solo pytest)
pip install -r requirements.txt

# Verificar que funciona
pytest -v
```

### Estructura de archivos

```
python_extra_class/
├── README.md                          ← Estás aquí
├── GUIA_DE_DECISIONES.md             ← Árbol de decisiones
├── requirements.txt                   ← Dependencias (pytest)
├── pytest.ini                         ← Configuración de tests
│
├── 01_programacion_python/            ← Módulo 1
│   ├── 01_variables_y_tipos.md
│   ├── ...
│   ├── 08_excepciones_avanzadas.md   ← NUEVO
│   ├── 09_generadores_e_iteradores.md ← NUEVO
│   ├── 10_comprension_vs_loops.md    ← NUEVO
│   └── 11_logging_patterns.md         ← NUEVO
│
├── 02_oop_python/                     ← Módulo 2
│   ├── 01_clases_y_objetos.md
│   ├── ...
│   └── 08_logging_en_clases.md        ← NUEVO
│
├── 03_ejercicios_leetcode/            ← Módulo 3
│   ├── ejercicios.md                  ← 12 problemas explicados
│   ├── leetcode_runnable.py           ← NUEVO: Código ejecutable
│   └── test_leetcode.py               ← NUEVO: 67 tests
│
└── 04_ejemplos_runnable/              ← Módulo 4 (NUEVO)
    ├── README.md                       ← Guía de ejemplos
    ├── ejemplo_01_excepciones.py
    ├── ejemplo_02_context_managers.py
    ├── ejemplo_03_generadores.py
    ├── ejemplo_04_logging_basico.py
    ├── ejemplo_05_logging_avanzado.py
    ├── ejemplo_06_comprehension_performance.py
    └── test_ejemplos.py                ← Tests de ejemplos
```

---

## 💡 Tips para aprender

1. **No leas pasivamente** - Ejecuta cada ejemplo
2. **Modifica el código** - Rompe cosas para entender cómo funcionan
3. **Resuelve antes de mirar** - En LeetCode, intenta 20-30 min antes de ver la solución
4. **Usa la guía de decisiones** - Cuando dudes, consulta `GUIA_DE_DECISIONES.md`
5. **Escribe tus propios tests** - Agrega casos límite a los problemas
6. **Explica en voz alta** - Si puedes explicarlo, lo entiendes
7. **Revisa patrones** - Después de 5 problemas, anota qué patrones se repiten

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pytest'"

```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError" al ejecutar ejemplos

```bash
# Asegúrate de estar en el directorio correcto
cd python_extra_class
python 04_ejemplos_runnable/ejemplo_01_excepciones.py
```

### Tests fallan

```bash
# Verifica la versión de Python (necesitas 3.8+)
python --version

# Reinstala dependencias
pip install --upgrade pytest pytest-cov

# Ejecuta con más info
pytest -vv --tb=long
```

---

## 📈 Progress Tracker

Marca tu progreso:

**Módulo 1: Programación Python**
- [ ] 01-04: Fundamentos
- [ ] 05-07: Errores y buenas prácticas
- [ ] 08: Excepciones avanzadas
- [ ] 09: Generadores
- [ ] 10: Comprehensions vs loops
- [ ] 11: Logging patterns

**Módulo 2: OOP Python**
- [ ] 01-07: OOP básico
- [ ] 08: Logging en clases

**Módulo 3: LeetCode**
- [ ] Básico 1-5
- [ ] Básico 6-10
- [ ] Intermedio 11-12
- [ ] Todos los tests pasan: `pytest 03_ejercicios_leetcode/test_leetcode.py -v`

**Módulo 4: Ejemplos**
- [ ] Todos los ejemplos ejecutados
- [ ] Código modificado y experimentado

**Guía de Decisiones**
- [ ] Leída completa
- [ ] Consultada cuando necesario
- [ ] Puedo explicar cada árbol de decisión

---

## 🚀 Siguiente paso

1. **Nuevo en Python?** → Empieza con `01_programacion_python/01_variables_y_tipos.md`
2. **Sabes Python básico?** → Lee `GUIA_DE_DECISIONES.md` y elige un path de aprendizaje arriba
3. **Solo quieres practicar algoritmos?** → Ve directo a `03_ejercicios_leetcode/`
4. **Preparación para entrevista urgente?** → Sigue el "Path rápido" (2 días)

---

**Última actualización:** 2026-02
**Nivel:** Intermedio a Avanzado
**Tiempo estimado:** 2 días (rápido) a 2 semanas (completo)

---

**Feedback:** Si encuentras errores, conceptos confusos, o tienes sugerencias, son bienvenidos. Este es un documento vivo.

**Licencia:** Material educativo de uso libre. Úsalo, modifícalo, compártelo.
