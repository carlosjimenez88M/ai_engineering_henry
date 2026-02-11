# Comprensiones vs Loops: Guía Definitiva

**Por qué importa:** Las comprensiones pueden hacer tu código más rápido y legible, pero usadas mal lo vuelven imposible de entender. Esta guía te enseña cuándo usar cada herramienta.

**TL;DR:**
- Comprensiones simples → Más rápido y legible
- Comprensiones complejas → Usa loop explícito
- Cuando dudes → Usa loop (siempre puedes refactorizar después)

---

## 1. Comparación de Performance

### 1.1 ¿Por qué las comprensiones son más rápidas?

Las comprensiones están **optimizadas en bytecode**. Python sabe de antemano que estás construyendo una lista, por lo que pre-aloca memoria y evita llamadas a métodos.

### 1.2 Resultados de timeit (elementos promedio)

```python
import timeit

# Caso 1: Lista simple (1000 elementos)
setup = "nums = range(1000)"

# Loop tradicional
loop_code = """
result = []
for n in nums:
    result.append(n * 2)
"""

# List comprehension
comp_code = """
result = [n * 2 for n in nums]
"""

print(f"Loop:          {timeit.timeit(loop_code, setup, number=10000):.4f}s")
print(f"Comprehension: {timeit.timeit(comp_code, setup, number=10000):.4f}s")

# Resultado típico:
# Loop:          0.8500s
# Comprehension: 0.3200s
# → Comprehension es ~2.6x más rápida
```

### 1.3 Ventajas de performance

| Estructura | Tiempo (10k elementos) | Razón |
|------------|------------------------|-------|
| `for` + `.append()` | 100% (baseline) | Llamada a método en cada iteración |
| List comprehension | ~38% | Optimizada en bytecode |
| Generator expression | ~35% | No aloca memoria por adelantado |
| `map()` + `lambda` | ~45% | Overhead de llamadas a función |

**Golden Rule #1:** Para operaciones simples (map, filter), usa comprehensions. Son más rápidas y más legibles.

### 1.4 Comparación con datos reales

```python
# Escenario: Filtrar y transformar usuarios
usuarios = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Juan", "edad": 17},
    {"nombre": "María", "edad": 30},
    # ... 10,000 usuarios
]

# Loop tradicional: ~120ms
adultos = []
for u in usuarios:
    if u["edad"] >= 18:
        adultos.append(u["nombre"].upper())

# Comprehension: ~45ms (2.6x más rápido)
adultos = [u["nombre"].upper() for u in usuarios if u["edad"] >= 18]
```

**Ver código ejecutable:** `04_ejemplos_runnable/ejemplo_06_comprehension_performance.py`

---

## 2. Reglas de Legibilidad

### 2.1 La Regla de la Línea Única

**Golden Rule #2:** Si cabe en una línea (<80 caracteres) y es fácil de leer en voz alta, usa comprehension. Si no, usa loop.

####  BUENAS comprensiones (una línea, fácil de leer)

```python
# Map simple
cuadrados = [x**2 for x in range(10)]

# Filter simple
pares = [x for x in nums if x % 2 == 0]

# Map + filter simple
adultos_mayores = [u["nombre"] for u in usuarios if u["edad"] >= 65]

# Transformación simple
nombres_upper = [n.upper() for n in nombres]
```

####  MALAS comprensiones (complejas, difíciles de leer)

```python
#  Múltiples condiciones (demasiado denso)
resultado = [x * y for x in range(10) for y in range(10)
             if x > 5 if y < 3 if x + y != 8]

#  Lógica compleja dentro del map
usuarios_procesados = [
    {**u, "nombre_completo": f"{u['nombre']} {u['apellido']}",
     "es_mayor": u["edad"] >= 18, "categoria": "senior" if u["edad"] >= 65 else "adulto"}
    for u in usuarios
    if u.get("activo", True) and u["edad"] > 0
]

#  Comprensión anidada (imposible de leer)
matriz_filtrada = [[y for y in fila if y > 0] for fila in matriz if sum(fila) > 10]
```

### 2.2 Test de Legibilidad

Pregúntate:

1. **¿Puedes leerlo en voz alta sin pausar?** → Sí = comprehension, No = loop
2. **¿Cabe en una línea sin scrolling horizontal?** → Sí = comprehension, No = loop
3. **¿Tiene más de un `if` o `for` anidado?** → Sí = loop, No = puede ser comprehension
4. **¿Necesitarás debuggearlo con prints?** → Sí = loop, No = comprehension

**Golden Rule #3:** Si pasas más de 5 segundos entendiendo una comprehension, reescríbela como loop.

---

## 3. Árbol de Decisión

### 3.1 Flowchart: ¿Comprehension o Loop?

```
¿Necesitas construir una lista/set/dict?
│
├─ NO → Usa loop normal (no necesitas comprensión)
│
└─ SÍ → ¿Es una operación simple (map o filter)?
    │
    ├─ NO → ¿Necesitas múltiples pasos o lógica compleja?
    │   │
    │   ├─ SÍ → Usa loop explícito
    │   │        Razón: Legibilidad > Performance
    │   │
    │   └─ NO → ¿Necesitas debuggear con prints?
    │       │
    │       ├─ SÍ → Usa loop explícito
    │       │        Razón: Puedes agregar prints entre pasos
    │       │
    │       └─ NO → ¿La comprehension tiene más de 1 línea?
    │           │
    │           ├─ SÍ → Usa loop explícito
    │           │        Razón: Si necesitas múltiples líneas, es muy compleja
    │           │
    │           └─ NO →  USA COMPREHENSION
    │                    Razón: Simple, legible, rápida
    │
    └─ SÍ → ¿Necesitas el resultado inmediatamente?
        │
        ├─ NO → Usa generator expression (lazy evaluation)
        │        Ejemplo: sum(x**2 for x in range(10000))
        │
        └─ SÍ → ¿Cabe en una línea (<80 chars)?
            │
            ├─ SÍ →  USA COMPREHENSION
            │
            └─ NO → Usa loop explícito
```

### 3.2 Casos especiales

| Caso | Usa | Razón |
|------|-----|-------|
| Procesamiento de archivos grandes | Generator | No carga todo en memoria |
| Cálculos matemáticos simples | Comprehension | Más rápida, más clara |
| Necesitas `break` o `continue` complejo | Loop | Comprehensions no soportan break |
| Necesitas `else` en el loop | Loop | Comprehensions no soportan else |
| Efectos secundarios (print, logging) | Loop | Comprehensions son para transformar, no side effects |
| Múltiples estructuras (lista Y dict) | Loop | Una comprehension = una estructura |

---

## 4. 10 Ejemplos Side-by-Side

### Ejemplo 1: Map simple - Duplicar valores

```python
#  BUENA comprehension
nums = [1, 2, 3, 4, 5]
dobles = [n * 2 for n in nums]

#  BUENA loop (más verbosa pero clara)
nums = [1, 2, 3, 4, 5]
dobles = []
for n in nums:
    dobles.append(n * 2)

# Veredicto: Usa comprehension (simple, legible, rápida)
```

### Ejemplo 2: Filter simple - Solo pares

```python
#  BUENA comprehension
nums = [1, 2, 3, 4, 5, 6, 7, 8]
pares = [n for n in nums if n % 2 == 0]

#  BUENA loop
nums = [1, 2, 3, 4, 5, 6, 7, 8]
pares = []
for n in nums:
    if n % 2 == 0:
        pares.append(n)

# Veredicto: Usa comprehension (más concisa, igualmente clara)
```

### Ejemplo 3: Map + Filter - Cuadrados de pares

```python
#  BUENA comprehension
nums = [1, 2, 3, 4, 5, 6]
cuadrados_pares = [n**2 for n in nums if n % 2 == 0]

#  BUENA loop
nums = [1, 2, 3, 4, 5, 6]
cuadrados_pares = []
for n in nums:
    if n % 2 == 0:
        cuadrados_pares.append(n**2)

# Veredicto: Usa comprehension (todavía legible)
```

### Ejemplo 4: Lógica compleja - Categorizar usuarios

```python
#  MALA comprehension (demasiado compleja)
categorias = [
    "niño" if u["edad"] < 18 else "adulto" if u["edad"] < 65 else "senior"
    for u in usuarios
    if u.get("activo", True)
]

#  BUENO: Loop con función helper
def categorizar_usuario(usuario):
    if not usuario.get("activo", True):
        return None
    if usuario["edad"] < 18:
        return "niño"
    elif usuario["edad"] < 65:
        return "adulto"
    else:
        return "senior"

categorias = []
for u in usuarios:
    cat = categorizar_usuario(u)
    if cat is not None:
        categorias.append(cat)

# Veredicto: Usa loop + función (más claro y testeable)
```

### Ejemplo 5: Nested loops - Producto cartesiano

```python
#  MALA comprehension (difícil de leer)
pares = [(x, y) for x in range(5) for y in range(5) if x != y]

#  BUENO: Loop explícito
pares = []
for x in range(5):
    for y in range(5):
        if x != y:
            pares.append((x, y))

# Veredicto: Usa loop (más fácil de seguir la lógica anidada)
```

### Ejemplo 6: Diccionarios - Invertir clave-valor

```python
#  BUENA dict comprehension
original = {"a": 1, "b": 2, "c": 3}
invertido = {v: k for k, v in original.items()}

#  BUENA loop
original = {"a": 1, "b": 2, "c": 3}
invertido = {}
for k, v in original.items():
    invertido[v] = k

# Veredicto: Usa comprehension (operación simple, muy común)
```

### Ejemplo 7: Sets - Valores únicos

```python
#  BUENA set comprehension
usuarios = [{"id": 1, "role": "admin"}, {"id": 2, "role": "user"}, {"id": 3, "role": "admin"}]
roles_unicos = {u["role"] for u in usuarios}

#  BUENA loop
usuarios = [{"id": 1, "role": "admin"}, {"id": 2, "role": "user"}, {"id": 3, "role": "admin"}]
roles_unicos = set()
for u in usuarios:
    roles_unicos.add(u["role"])

# Veredicto: Usa comprehension (extracción simple)
```

### Ejemplo 8: Efectos secundarios - Logging

```python
#  MAL: NO uses comprehension para side effects
# (funciona pero es un anti-patrón)
_ = [print(f"Procesando {item}") for item in items]

#  BUENO: Loop para side effects
for item in items:
    print(f"Procesando {item}")

# Veredicto: SIEMPRE usa loop para efectos secundarios
```

### Ejemplo 9: Early exit - Buscar primero que cumple condición

```python
#  NO PUEDES: Comprehension no soporta break
# resultado = [x for x in nums if x > 10]  # procesa TODO

#  BUENO: Loop con break
resultado = None
for x in nums:
    if x > 10:
        resultado = x
        break  # Sale temprano, no procesa el resto

#  MEJOR: Usa next() con generator
resultado = next((x for x in nums if x > 10), None)

# Veredicto: Loop con break o next() con generator
```

### Ejemplo 10: Múltiples colecciones - Separar pares e impares

```python
#  NO PUEDES: Comprehension solo construye UNA estructura
# pares = [n for n in nums if n % 2 == 0]
# impares = [n for n in nums if n % 2 != 0]  # ¡Itera DOS veces!

#  BUENO: Loop que construye ambas
pares = []
impares = []
for n in nums:
    if n % 2 == 0:
        pares.append(n)
    else:
        impares.append(n)

# Veredicto: Usa loop (más eficiente, itera una sola vez)
```

---

## 5. Implicaciones de Memoria

### 5.1 List Comprehension vs Generator Expression

```python
# List comprehension - Aloca TODA la memoria de antemano
nums_list = [x**2 for x in range(1000000)]  # ~8 MB en memoria

# Generator expression - Lazy evaluation (calcula on-demand)
nums_gen = (x**2 for x in range(1000000))   # ~200 bytes en memoria

# Ejemplo práctico
#  MAL: Carga 10 GB en memoria
grandes = [procesar_archivo(f) for f in archivos_10GB]

#  BUENO: Procesa uno a la vez
grandes = (procesar_archivo(f) for f in archivos_10GB)
for resultado in grandes:
    hacer_algo(resultado)
```

### 5.2 Cuándo usar cada una

| Situación | Usa | Razón |
|-----------|-----|-------|
| Necesitas iterar múltiples veces | List comp | Generators se agotan después de una iteración |
| Necesitas len(), indexing, slicing | List comp | Generators no soportan estas operaciones |
| Procesando millones de items | Generator | No carga todo en memoria |
| Pasando a sum(), max(), any() | Generator | Estas funciones consumen iterables |
| Necesitas ver resultado para debug | List comp | Generators son "cajas negras" hasta consumirlos |

### 5.3 Ejemplo real: Procesamiento de logs

```python
#  MAL: Carga 1 GB de logs en memoria
with open("app.log") as f:
    errores = [line for line in f if "ERROR" in line]
    print(f"Total errores: {len(errores)}")

#  BUENO: Procesa línea por línea
with open("app.log") as f:
    errores = (line for line in f if "ERROR" in line)
    count = sum(1 for _ in errores)
    print(f"Total errores: {count}")

#  MEJOR: Si necesitas contar, no materialices
with open("app.log") as f:
    count = sum(1 for line in f if "ERROR" in line)
    print(f"Total errores: {count}")
```

**Golden Rule #4:** Si no necesitas la lista completa en memoria, usa generator expression.

---

## 6. Consideraciones de Debugging

### 6.1 Por qué los loops son más fáciles de debuggear

```python
# Comprehension - No puedes agregar prints entre pasos
resultado = [procesar(x) for x in data if validar(x)]

# Loop - Puedes inspeccionar cada paso
resultado = []
for x in data:
    print(f"DEBUG: Procesando {x}")
    if validar(x):
        print(f"DEBUG: {x} es válido")
        procesado = procesar(x)
        print(f"DEBUG: Resultado = {procesado}")
        resultado.append(procesado)
```

### 6.2 Estrategia: Empieza con loop, luego refactoriza

```python
# Paso 1: Escribe como loop (fácil de debuggear)
usuarios_adultos = []
for u in usuarios:
    print(f"DEBUG: usuario = {u}")  # Puedes ver qué está pasando
    if u["edad"] >= 18:
        usuarios_adultos.append(u["nombre"])

# Paso 2: Una vez que funciona, refactoriza a comprehension
usuarios_adultos = [u["nombre"] for u in usuarios if u["edad"] >= 18]
```

### 6.3 Debugging de comprehensions con walrus operator

```python
# Python 3.8+: Puedes usar := para "espiar" valores intermedios
#  Sin walrus: No puedes ver valores intermedios
resultado = [procesar(x) for x in data if validar(x)]

#  Con walrus: Puedes imprimir/guardar valores intermedios
debug_values = []
resultado = [
    procesado
    for x in data
    if validar(x)
    if (procesado := procesar(x)) or True  # Truco: guardar en variable
]

# Pero esto ya es demasiado complejo → mejor usa loop
```

**Golden Rule #5:** Si necesitas debuggear, escribe como loop primero. Refactoriza después.

---

## 7. Code Review Red Flags

### 7.1 Red Flags en comprehensions

 **Red Flag #1: Múltiples líneas**

```python
#  MAL
resultado = [
    procesar(x, y, z)
    for x in range(10)
    for y in range(10)
    for z in range(10)
    if x > y
    if y > z
    if validar(x, y, z)
]

#  MEJOR: Si necesitas múltiples líneas, usa loop
```

 **Red Flag #2: Lógica compleja en el map**

```python
#  MAL
resultado = [
    {"id": u["id"], "nombre": f"{u['first']} {u['last']}",
     "email": u["email"].lower(), "activo": u.get("status") == "active"}
    for u in usuarios
]

#  MEJOR: Función helper
def transformar_usuario(u):
    return {
        "id": u["id"],
        "nombre": f"{u['first']} {u['last']}",
        "email": u["email"].lower(),
        "activo": u.get("status") == "active"
    }

resultado = [transformar_usuario(u) for u in usuarios]
```

 **Red Flag #3: Side effects en comprehensions**

```python
#  MAL: Comprehension con side effects
_ = [log_procesamiento(x) for x in items]  # NO uses comprehension para side effects

#  MEJOR: Loop explícito
for x in items:
    log_procesamiento(x)
```

 **Red Flag #4: Nested comprehensions**

```python
#  MAL: Demasiado anidado
matriz_procesada = [
    [procesar(y) for y in fila if y > 0]
    for fila in matriz
    if sum(fila) > 10
]

#  MEJOR: Loop con nombre de variables descriptivos
matriz_procesada = []
for fila in matriz:
    if sum(fila) > 10:
        fila_procesada = []
        for valor in fila:
            if valor > 0:
                fila_procesada.append(procesar(valor))
        matriz_procesada.append(fila_procesada)
```

 **Red Flag #5: Comprehension que nadie usa**

```python
#  MAL: Crea lista pero no la usa (solo quiere side effects)
[print(x) for x in items]

#  MEJOR: Loop explícito
for x in items:
    print(x)
```

### 7.2 Red Flags en loops

 **Red Flag #1: Loop simple que debería ser comprehension**

```python
#  SUBÓPTIMO: Loop para operación trivial
cuadrados = []
for x in range(10):
    cuadrados.append(x**2)

#  MEJOR: Comprehension
cuadrados = [x**2 for x in range(10)]
```

 **Red Flag #2: .append() en loop sin lógica adicional**

```python
#  SUBÓPTIMO
pares = []
for n in nums:
    if n % 2 == 0:
        pares.append(n)

#  MEJOR
pares = [n for n in nums if n % 2 == 0]
```

 **Red Flag #3: Iterar múltiples veces cuando puedes hacerlo en una**

```python
#  SUBÓPTIMO: Dos iteraciones
pares = [n for n in nums if n % 2 == 0]
impares = [n for n in nums if n % 2 != 0]

#  MEJOR: Una sola iteración
pares = []
impares = []
for n in nums:
    if n % 2 == 0:
        pares.append(n)
    else:
        impares.append(n)
```

---

## Golden Rules: Resumen Ejecutivo

### Las 7 Reglas de Oro

**Rule #1: Performance**
- Comprehensions simples son ~2-3x más rápidas que loops
- Para operaciones triviales (map/filter), usa comprehension

**Rule #2: Legibilidad**
- Si cabe en una línea (<80 chars) y se lee fácil → comprehension
- Si no → loop

**Rule #3: Tiempo de comprensión**
- Si pasas >5 segundos entendiendo una comprehension → reescríbela como loop

**Rule #4: Memoria**
- Si no necesitas la lista completa → usa generator expression
- Archivos grandes, streams, datos infinitos → generators

**Rule #5: Debugging**
- Necesitas debuggear → empieza con loop
- Funciona → refactoriza a comprehension si es simple

**Rule #6: Side effects**
- NUNCA uses comprehensions para side effects (print, logging, writes)
- Comprehensions son para transformar datos, no para ejecutar acciones

**Rule #7: Complejidad**
- Una condición simple → comprehension OK
- Múltiples condiciones o lógica compleja → loop

### Decisión rápida

```python
# ¿Tu operación es...?
#
#  [n*2 for n in nums]                    → Simple map
#  [n for n in nums if n > 0]             → Simple filter
#  [n*2 for n in nums if n > 0]           → Simple map + filter
#  {k: v for k, v in items}               → Dict construction
#  {item for item in items}               → Set construction
#
#  Múltiples líneas                        → Loop
#  Lógica compleja (if/elif/else)         → Loop
#  Nested loops                            → Loop
#  Side effects (print, log, write)       → Loop
#  Necesitas break/continue                → Loop
#  Construyes múltiples colecciones        → Loop
```

---

## Checklist de Code Review

### Para comprehensions

- [ ] ¿Cabe en una línea (<80 caracteres)?
- [ ] ¿Se puede leer en voz alta sin pausar?
- [ ] ¿Es más rápida que un loop? (casi siempre sí)
- [ ] ¿No tiene side effects?
- [ ] ¿No está anidada >1 nivel?
- [ ] ¿No tiene lógica compleja (múltiples if/else)?

### Para loops

- [ ] ¿Realmente necesitas la flexibilidad del loop?
- [ ] ¿Podrías reemplazarlo con comprehension simple?
- [ ] ¿Estás construyendo múltiples colecciones? (entonces sí, loop)
- [ ] ¿Necesitas break/continue complejo? (entonces sí, loop)
- [ ] ¿Hay side effects? (entonces sí, loop)

---

## Ejercicios

### Ejercicio 1: Convierte estos loops a comprehensions (solo si mejora legibilidad)

```python
# 1.
numeros = []
for i in range(10):
    numeros.append(i * 3)

# 2.
mayores = []
for persona in personas:
    if persona["edad"] >= 18:
        mayores.append(persona["nombre"])

# 3.
resultado = {}
for clave, valor in datos.items():
    if valor > 0:
        resultado[clave] = valor * 2
```

### Ejercicio 2: Convierte estas comprehensions a loops (porque son muy complejas)

```python
# 1.
resultado = [x*y for x in range(10) for y in range(10) if x > y if (x+y) % 2 == 0]

# 2.
usuarios_filtrados = [
    {**u, "nombre_completo": f"{u['nombre']} {u['apellido']}", "mayor": u["edad"] >= 18}
    for u in usuarios
    if u.get("activo") and u["email"] and "@" in u["email"]
]
```

### Ejercicio 3: Identifica los red flags

```python
# ¿Qué está mal con este código?
_ = [print(f"Procesando: {item}") for item in items]

# ¿Qué está mal aquí?
pares = [n for n in range(10000000) if n % 2 == 0]  # 10 millones
impares = [n for n in range(10000000) if n % 2 != 0]
```

---

**Siguiente:**
- **Código ejecutable:** `04_ejemplos_runnable/ejemplo_06_comprehension_performance.py`
- **Temas relacionados:** `09_iteradores_y_generators.md`
- **Patrones avanzados:** `12_functional_programming_patterns.md`
