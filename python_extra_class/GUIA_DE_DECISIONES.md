# Guía de Decisiones - Python Extra Class

**Por qué existe esta guía:** Python te da muchas formas de hacer lo mismo. Esta guía te dice CUÁNDO usar cada herramienta, no solo CÓMO usarla.

**Cómo usarla:** Encuentra tu situación → sigue el árbol de decisión → aplica la recomendación.

---

## Tabla de contenidos

1. [Exception Handling - ¿Cómo manejar errores?](#1-exception-handling)
2. [Logging vs Print vs Raise - ¿Cómo reportar problemas?](#2-logging-vs-print-vs-raise)
3. [List Comprehension vs For Loop - ¿Cómo iterar?](#3-list-comprehension-vs-for-loop)
4. [Generators vs Lists - ¿Cómo almacenar secuencias?](#4-generators-vs-lists)
5. [Data Structures - ¿Qué estructura usar?](#5-data-structures)
6. [Custom Exceptions vs Built-in - ¿Crear excepciones propias?](#6-custom-exceptions-vs-built-in)
7. [Logging Levels - ¿Qué nivel de log usar?](#7-logging-levels)
8. [Context Managers - ¿Cuándo crear uno?](#8-context-managers)
9. [Dataclass vs Regular Class - ¿Cómo definir clases?](#9-dataclass-vs-regular-class)
10. [Resumen Visual](#10-resumen-visual)

---

## 1. Exception Handling

### Árbol de decisión

```
¿Puede fallar esta operación?
├─ NO → No uses try/except
└─ SÍ → ¿Sabes qué error específico puede ocurrir?
    ├─ SÍ → ¿Puedes recuperarte del error?
    │   ├─ SÍ → try/except específico + manejo
    │   └─ NO → Deja que se propague o usa try/except + re-raise
    └─ NO → ¿Es para logging/cleanup solamente?
        ├─ SÍ → try/except Exception as e + log + re-raise
        └─ NO → Deja que se propague
```

### Tabla de estrategias

| Situación | Estrategia | Ejemplo |
|-----------|------------|---------|
| Error esperado y recuperable | Catch específico + handle | `except FileNotFoundError: create_file()` |
| Error esperado, no recuperable | Catch específico + log + re-raise | `except ValueError as e: logger.error(e); raise` |
| Necesitas cleanup siempre | `finally` o context manager | `finally: file.close()` o `with open()` |
| Solo para logging | Catch `Exception` + log + re-raise | `except Exception as e: logger.error(e); raise` |
| Error no esperado | No catches, deja propagar | (sin try/except) |

### Ejemplos

#### ✅ BIEN: Error esperado y recuperable

```python
def cargar_config(filepath):
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        # Error esperado, uso config por defecto
        return DEFAULT_CONFIG
    except json.JSONDecodeError as e:
        # Error esperado, informo al usuario
        raise ConfigError(f"JSON inválido: {e}") from e
```

#### ❌ MAL: Catch demasiado amplio

```python
def procesar_datos(datos):
    try:
        resultado = operacion_compleja(datos)
        return resultado
    except:  # ¿Qué error? ¿Por qué falló?
        return None  # Silencia TODOS los errores
```

---

## 2. Logging vs Print vs Raise

### Árbol de decisión

```
¿Es para desarrollo local (tú debuggeando)?
├─ SÍ → print() está bien
└─ NO → ¿Es un error que rompe la ejecución?
    ├─ SÍ → raise Exception (+ logger.error antes si necesario)
    └─ NO → ¿Necesitan verlo ops/producción?
        ├─ SÍ → ¿Qué tan importante es?
        │   ├─ Información normal → logger.info()
        │   ├─ Algo inesperado pero no crítico → logger.warning()
        │   ├─ Error que afecta operación → logger.error()
        │   └─ Error crítico del sistema → logger.critical()
        └─ NO → No logues nada (evita spam en logs)
```

### Tabla de decisión

| Situación | Usa | Razón |
|-----------|-----|-------|
| Debuggear localmente | `print()` | Rápido, simple, no necesitas configuración |
| Logs en producción | `logger.info/warning/error()` | Control de niveles, archivos, rotación |
| Error que rompe ejecución | `raise ExceptionType()` | Detiene flujo, fuerza manejo |
| Error + necesitas log | `logger.error(); raise` | Log para ops, raise para detener |
| Información de progreso | `logger.info()` | Trackear operaciones normales |
| Algo raro pero no fatal | `logger.warning()` | Atención pero no detiene |
| Error crítico del sistema | `logger.critical()` | Máxima prioridad, puede requerir alerta |

### Ejemplos lado a lado

#### Escenario 1: Procesando archivo

```python
# ✅ BIEN: Desarrollo local
def procesar_archivo_dev(filepath):
    print(f"Procesando {filepath}")
    data = leer_archivo(filepath)
    print(f"Leídos {len(data)} bytes")
    return data

# ✅ BIEN: Producción
def procesar_archivo_prod(filepath):
    logger.info(f"Iniciando procesamiento de {filepath}")
    try:
        data = leer_archivo(filepath)
        logger.info(f"Archivo procesado: {len(data)} bytes")
        return data
    except IOError as e:
        logger.error(f"Error al leer archivo {filepath}: {e}")
        raise
```

#### Escenario 2: API rate limit

```python
# ✅ BIEN: Warning, no raise (no es fatal)
def llamar_api(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 429:
        logger.warning(
            f"Rate limit alcanzado en {endpoint}. "
            f"Retry-After: {response.headers.get('Retry-After')}"
        )
        time.sleep(int(response.headers.get('Retry-After', 60)))
        return llamar_api(endpoint)
    return response.json()

# ❌ MAL: Print en producción
def llamar_api_mal(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 429:
        print("Rate limited!")  # Nadie ve esto en producción
    return response.json()
```

---

## 3. List Comprehension vs For Loop

### Árbol de decisión

```
¿La lógica cabe en UNA línea clara y legible?
├─ SÍ → ¿Es una transformación simple (map) o filtro?
│   ├─ SÍ → List comprehension ✓
│   │   Ejemplo: [x*2 for x in nums]
│   │   Ejemplo: [x for x in nums if x > 0]
│   └─ NO → ¿Tiene lógica compleja con múltiples if?
│       └─ SÍ → For loop
│           Ejemplo: for x in nums: if x > 0 and validate(x): ...
└─ NO → ¿Necesitas break, continue, o try-except?
    ├─ SÍ → For loop (comprehensions no soportan esto)
    └─ NO → ¿Son más de 2 niveles de nesting?
        ├─ SÍ → For loop (ilegible como comprehension)
        └─ NO → ¿Necesitas print/debug statements?
            ├─ SÍ → For loop
            └─ NO → List comprehension probablemente esté bien
```

### Reglas de oro

1. **Una línea clara** → Comprehension
2. **Lógica compleja** → For loop
3. **Necesitas debugging** → For loop
4. **Más de 2 niveles nested** → For loop
5. **Dataset grande y solo iteras una vez** → Generator expression

### Tabla de comparación

| Feature | List Comprehension | For Loop |
|---------|-------------------|----------|
| Performance | ~30-50% más rápido | Más lento |
| Legibilidad (simple) | ✅ Excelente | ❌ Verbose |
| Legibilidad (complejo) | ❌ Ilegible | ✅ Clara |
| break/continue | ❌ No soportado | ✅ Soportado |
| try/except | ❌ No soportado | ✅ Soportado |
| Debugging | ❌ Difícil | ✅ Fácil (prints) |
| Memoria (grande) | ❌ Toda en RAM | ❌ Toda en RAM |
| Memoria (generator) | ✅ `()` en vez de `[]` | N/A |

### Ejemplos lado a lado

#### ✅ BIEN: Comprehension (simple, claro)

```python
# Transformación simple
squares = [x**2 for x in range(10)]

# Filtro simple
evens = [x for x in nums if x % 2 == 0]

# Transformación + filtro
positive_doubles = [x*2 for x in nums if x > 0]

# Map sobre diccionario
names = [user['name'] for user in users]
```

#### ✅ BIEN: For loop (lógica compleja)

```python
# Múltiples condiciones y validaciones
result = []
for x in nums:
    if x > 0 and x < 100:
        validated = validate_complex(x)
        if validated:
            result.append(transform(validated))

# Con try-except
result = []
for x in nums:
    try:
        processed = complex_function(x)
        result.append(processed)
    except ValueError:
        logger.warning("Skipping %s", x)
        continue

# Con break
result = []
for x in nums:
    if x > threshold:
        break
    result.append(x*2)
```

#### ❌ MAL: Comprehension ilegible

```python
# NO HAGAS ESTO - muy complejo para una línea
result = [transform(x) for x in nums if x > 0 and x < 100 and validate(x) and check(x)]

# NO HAGAS ESTO - nested difícil de leer
matrix = [[[z for z in range(i)] for y in range(j)] for i in range(10) for j in range(5)]

# Mejor como for loop con nombres claros
matrix = []
for i in range(10):
    layer = []
    for j in range(5):
        row = list(range(i))
        layer.append(row)
    matrix.append(layer)
```

---

## 4. Generators vs Lists

### Árbol de decisión

```
¿Necesitas toda la secuencia en memoria?
├─ SÍ (acceso aleatorio, múltiples iteraciones) → List
└─ NO → ¿Cuál es el tamaño del dataset?
    ├─ Pequeño (< 1000 items) → List (más simple)
    └─ Grande (> 1000 items) → ¿Solo iteras una vez?
        ├─ SÍ → Generator ✓
        └─ NO → ¿Cabe en RAM?
            ├─ SÍ → List
            └─ NO → Generator (obligatorio)
```

### Tabla de comparación

| Feature | List | Generator |
|---------|------|-----------|
| Memoria | O(n) - toda en RAM | O(1) - item a la vez |
| Velocidad (crear) | Lenta (crea todo) | Rápida (lazy) |
| Velocidad (iterar) | Rápida | Similar |
| Acceso aleatorio | ✅ `list[i]` | ❌ No soportado |
| Múltiples iteraciones | ✅ Reutilizable | ❌ Una sola vez |
| len() | ✅ Soportado | ❌ No soportado |
| Sintaxis | `[x for x in ...]` | `(x for x in ...)` |

### Ejemplos

#### ✅ BIEN: List (necesitas acceso aleatorio)

```python
# Necesitas índices
usuarios = [get_user(id) for id in user_ids]
primer_usuario = usuarios[0]
ultimo_usuario = usuarios[-1]

# Necesitas iterar múltiples veces
numeros = [x for x in range(100)]
suma = sum(numeros)
promedio = sum(numeros) / len(numeros)  # Iteras 2 veces
```

#### ✅ BIEN: Generator (dataset grande, una iteración)

```python
# Archivo grande
def leer_archivo_grande(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()

# Solo iteras una vez
for linea in leer_archivo_grande('big_file.txt'):
    procesar(linea)

# Pipeline de datos
def numeros_pares(n):
    return (x for x in range(n) if x % 2 == 0)

def cuadrados(nums):
    return (x**2 for x in nums)

# Todo lazy, sin crear listas intermedias
resultado = sum(cuadrados(numeros_pares(1000000)))
```

#### Comparación de memoria

```python
import sys

# List: 8MB para 1 millón de números
lista = [x for x in range(1000000)]
print(sys.getsizeof(lista))  # ~8,000,000 bytes

# Generator: solo 200 bytes
generador = (x for x in range(1000000))
print(sys.getsizeof(generador))  # ~200 bytes
```

---

## 5. Data Structures

### Árbol de decisión

```
¿Qué operaciones necesitas?

Búsqueda rápida por clave → dict
│
Orden de inserción + sin duplicados → set
│
Orden de inserción + acceso por índice → list
│
Extremos rápidos (push/pop en ambos lados) → deque
│
Siempre ordenado → SortedList (no built-in, usa bisect + list)
│
Datos tabulares → DataFrame (pandas) o list[dict]
│
Conteo de elementos → Counter (collections)
│
Valor por defecto automático → defaultdict (collections)
```

### Tabla de complejidad

| Estructura | Acceso | Búsqueda | Inserción | Eliminación | Uso |
|------------|--------|----------|-----------|-------------|-----|
| `list` | O(1) | O(n) | O(1) final, O(n) medio | O(n) | Secuencia ordenada |
| `dict` | O(1) | O(1) | O(1) | O(1) | Key-value, lookup rápido |
| `set` | N/A | O(1) | O(1) | O(1) | Sin duplicados, membership |
| `tuple` | O(1) | O(n) | N/A (inmutable) | N/A | Datos inmutables |
| `deque` | O(1) extremos | O(n) | O(1) extremos | O(1) extremos | Cola, stack, buffer |

### Ejemplos de decisión

#### Escenario 1: Necesito buscar si un elemento existe

```python
# ❌ MAL: List O(n)
usuarios_list = [u1, u2, u3, ...]
if 'carlos' in usuarios_list:  # O(n) - lento

# ✅ BIEN: Set O(1)
usuarios_set = {u1, u2, u3, ...}
if 'carlos' in usuarios_set:  # O(1) - rápido
```

#### Escenario 2: Necesito acceso por clave

```python
# ❌ MAL: List de listas
usuarios = [['carlos', 25], ['ana', 30]]
for nombre, edad in usuarios:
    if nombre == 'carlos':  # O(n)
        print(edad)

# ✅ BIEN: Dict
usuarios = {'carlos': 25, 'ana': 30}
print(usuarios['carlos'])  # O(1)
```

#### Escenario 3: Necesito contar frecuencias

```python
from collections import Counter

# ❌ MAL: Dict manual
palabras = ['a', 'b', 'a', 'c', 'b', 'a']
conteo = {}
for p in palabras:
    conteo[p] = conteo.get(p, 0) + 1

# ✅ BIEN: Counter
conteo = Counter(palabras)
print(conteo['a'])  # 3
print(conteo.most_common(2))  # [('a', 3), ('b', 2)]
```

---

## 6. Custom Exceptions vs Built-in

### Árbol de decisión

```
¿El error encaja perfectamente en una excepción built-in?
├─ SÍ → Usa built-in
│   ValueError: Valor inválido
│   TypeError: Tipo incorrecto
│   KeyError: Clave no existe
│   FileNotFoundError: Archivo no existe
│   etc.
└─ NO → ¿Es específico de tu dominio?
    ├─ SÍ → ¿Necesitas metadata adicional?
    │   ├─ SÍ → Custom exception con __init__
    │   └─ NO → Custom exception simple
    └─ NO → Usa built-in más cercana
```

### Cuándo crear custom exceptions

| Situación | Usa built-in | Crea custom |
|-----------|--------------|-------------|
| Argumento inválido (tipo/valor) | `ValueError`, `TypeError` | ❌ |
| Archivo no existe | `FileNotFoundError` | ❌ |
| Operación no soportada | `NotImplementedError` | ❌ |
| Error específico de tu API/dominio | ❌ | ✅ |
| Necesitas campos adicionales | ❌ | ✅ |
| Quieres catch granular | ❌ | ✅ |
| Error de autenticación | ❌ | ✅ `AuthError` |
| Error de negocio | ❌ | ✅ `BusinessRuleError` |

### Ejemplos

#### ✅ BIEN: Usa built-in cuando encaja

```python
def dividir(a, b):
    if not isinstance(a, (int, float)):
        raise TypeError("a debe ser número")
    if b == 0:
        raise ValueError("b no puede ser cero")
    return a / b
```

#### ✅ BIEN: Custom cuando es específico de dominio

```python
class PaymentError(Exception):
    """Error base de pagos."""
    pass

class InsufficientFundsError(PaymentError):
    def __init__(self, balance, required):
        self.balance = balance
        self.required = required
        super().__init__(f"Fondos insuficientes: ${balance} < ${required}")

class PaymentGatewayError(PaymentError):
    def __init__(self, gateway, code):
        self.gateway = gateway
        self.code = code
        super().__init__(f"{gateway} error: {code}")

# Uso
try:
    procesar_pago(100, cuenta)
except InsufficientFundsError as e:
    notificar_usuario(f"Necesitas ${e.required - e.balance} más")
except PaymentGatewayError as e:
    logger.error(f"Gateway {e.gateway} falló: {e.code}")
```

---

## 7. Logging Levels

### Tabla de decisión

| Nivel | Cuándo usarlo | Ejemplo | En producción |
|-------|---------------|---------|---------------|
| `DEBUG` | Información detallada para debugging | `logger.debug("user_id=%s, params=%s", uid, params)` | ❌ Desactivado |
| `INFO` | Eventos normales del flujo | `logger.info("User %s logged in", username)` | ✅ Activado |
| `WARNING` | Algo inesperado pero no crítico | `logger.warning("Cache miss para key=%s", key)` | ✅ Activado |
| `ERROR` | Error que afecta operación actual | `logger.error("Failed to save: %s", error)` | ✅ Activado |
| `CRITICAL` | Error que puede detener la app | `logger.critical("DB pool exhausted")` | ✅ Activado + alerta |

### Flowchart de decisión

```
¿Es para debugging/desarrollo?
├─ SÍ → logger.debug()
└─ NO → ¿Es parte del flujo normal?
    ├─ SÍ → logger.info()
    └─ NO → ¿Es un problema?
        ├─ NO (solo advertencia) → logger.warning()
        └─ SÍ → ¿Rompe la operación actual?
            ├─ SÍ → ¿Rompe toda la aplicación?
            │   ├─ SÍ → logger.critical()
            │   └─ NO → logger.error()
            └─ NO → logger.warning()
```

### Ejemplos reales

```python
import logging

logger = logging.getLogger(__name__)

def procesar_pedido(pedido_id):
    # DEBUG: Detalles de desarrollo
    logger.debug("Procesando pedido %s con items: %s",
                 pedido_id, pedido.items)

    # INFO: Flujo normal
    logger.info("Pedido %s iniciado por usuario %s",
                pedido_id, pedido.user_id)

    # WARNING: Algo raro pero no crítico
    if pedido.total < 10:
        logger.warning("Pedido %s tiene total bajo: $%s",
                       pedido_id, pedido.total)

    try:
        procesar_pago(pedido)
        logger.info("Pedido %s completado", pedido_id)
    except InsufficientFundsError as e:
        # ERROR: Falla esta operación, pero la app sigue
        logger.error("Pedido %s falló: fondos insuficientes",
                     pedido_id)
        return False
    except DatabaseError as e:
        # CRITICAL: Problema sistémico
        logger.critical("DB error al procesar pedido %s: %s",
                        pedido_id, e)
        raise
```

---

## 8. Context Managers

### Árbol de decisión

```
¿Necesitas garantizar cleanup (cerrar, liberar, restaurar)?
├─ NO → No necesitas context manager
└─ SÍ → ¿Existe un context manager built-in?
    ├─ SÍ → Úsalo (open(), lock.acquire(), etc)
    └─ NO → ¿Es código simple?
        ├─ SÍ → @contextmanager decorator
        └─ NO (lógica compleja) → Clase con __enter__/__exit__
```

### Cuándo crear uno

| Situación | Solución |
|-----------|----------|
| Abrir/cerrar archivo | Built-in: `with open()` |
| Adquirir/liberar lock | Built-in: `with lock:` |
| Transacción DB | Custom: `with transaction():` |
| Timing de operación | Custom: `with timer():` |
| Estado temporal | Custom: `with temporary_state():` |
| Suprimir excepciones | Built-in: `with suppress(ValueError):` |
| Cambiar directorio temporalmente | Custom: `with cd(path):` |

### Ejemplos

#### Usa built-in cuando existe

```python
# ✅ Archivo
with open('data.txt') as f:
    data = f.read()

# ✅ Lock
import threading
lock = threading.Lock()
with lock:
    critical_section()

# ✅ Suprimir errores
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove('archivo_opcional.txt')
```

#### Crea custom cuando no existe

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    """Mide tiempo de ejecución."""
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{name}: {elapsed:.2f}s")

# Uso
with timer("Procesamiento"):
    procesar_datos()
```

---

## 9. Dataclass vs Regular Class

### Árbol de decisión

```
¿La clase es principalmente datos (attributes)?
├─ SÍ → ¿Necesitas métodos complejos?
│   ├─ NO → Dataclass ✓
│   └─ SÍ → ¿Los métodos son complejos?
│       ├─ SÍ → Regular class
│       └─ NO → Dataclass (puedes agregar métodos)
└─ NO (lógica compleja) → Regular class
```

### Tabla de comparación

| Feature | Dataclass | Regular Class |
|---------|-----------|---------------|
| __init__ automático | ✅ | ❌ Manual |
| __repr__ automático | ✅ | ❌ Manual |
| __eq__ automático | ✅ | ❌ Manual |
| Type hints requeridos | ✅ | ❌ Opcional |
| Inmutabilidad | ✅ `frozen=True` | ❌ Manual con properties |
| Herencia | ✅ | ✅ |
| Métodos personalizados | ✅ | ✅ |
| Boilerplate | ❌ Mínimo | ✅ Mucho |

### Ejemplos

#### ✅ BIEN: Dataclass (principalmente datos)

```python
from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    edad: int
    email: str
    activo: bool = True

    def es_mayor_de_edad(self) -> bool:
        return self.edad >= 18

# Sin dataclass necesitarías ~15 líneas de __init__, __repr__, __eq__
```

#### ✅ BIEN: Regular class (lógica compleja)

```python
class DatabaseConnection:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self._connection = None
        self._setup_connection(user, password)

    def _setup_connection(self, user, password):
        # Lógica compleja de conexión
        ...

    def query(self, sql):
        # Lógica de queries
        ...

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
```

---

## 10. Resumen Visual

### Mapa mental de decisiones rápidas

```
ITERACIÓN
├─ Simple → List comprehension
├─ Complejo → For loop
└─ Grande → Generator

ERRORES
├─ Esperado + recuperable → try/except + handle
├─ Esperado + no recuperable → try/except + log + raise
└─ No esperado → Propagar

LOGGING
├─ Desarrollo → print()
├─ Producción info → logger.info()
├─ Producción warning → logger.warning()
└─ Producción error → logger.error()

DATOS
├─ Búsqueda rápida → dict/set
├─ Orden + índices → list
├─ Inmutable → tuple
└─ Conteo → Counter

MEMORIA
├─ < 1000 items → List
├─ Una iteración → Generator
└─ > 100k items → Generator obligatorio
```

### Checklist rápido

Antes de escribir código, pregúntate:

- [ ] ¿Puede fallar? → Necesito try/except?
- [ ] ¿Es para producción? → Necesito logger en vez de print?
- [ ] ¿Es iteración simple? → Puedo usar comprehension?
- [ ] ¿Dataset grande? → Debería usar generator?
- [ ] ¿Necesito lookup rápido? → Debería usar dict/set?
- [ ] ¿Necesito cleanup? → Debería usar context manager?
- [ ] ¿Es solo datos? → Debería usar dataclass?

---

## Referencias

- **Excepciones:** `01_programacion_python/08_excepciones_avanzadas.md`
- **Logging:** `01_programacion_python/11_logging_patterns.md`
- **Generators:** `01_programacion_python/09_generadores_e_iteradores.md`
- **Comprehensions:** `01_programacion_python/10_comprension_vs_loops.md`
- **Ejemplos ejecutables:** `04_ejemplos_runnable/`

---

**Última actualización:** 2026-02

**Contribuciones:** Este es un documento vivo. Si encuentras un caso no cubierto, agrégalo.
