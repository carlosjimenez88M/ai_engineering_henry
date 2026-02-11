# Excepciones Avanzadas

**Por qué importa:** El manejo adecuado de excepciones separa el código robusto del código frágil. No se trata solo de "no crashear", sino de diseñar sistemas que respondan elegantemente a situaciones inesperadas.

**Prerrequisito:** Lee primero `05_errores_y_debug.md` para conceptos básicos.

**Código ejecutable:** Ver `04_ejemplos_runnable/ejemplo_01_excepciones.py` y `ejemplo_02_context_managers.py`

---

## 1. try/except/else/finally - El Cuarteto Completo

**Por qué:** Muchos usan solo `try/except`, pero `else` y `finally` te dan control preciso sobre el flujo.

### El modelo mental

```
try:
    # Código que puede fallar
except:
    # Maneja el error
else:
    # Solo ejecuta si NO hubo error
finally:
    # Siempre ejecuta (limpieza)
```

### Cuándo usar cada uno

| Bloque | Cuándo ejecuta | Para qué |
|--------|----------------|----------|
| `try` | Siempre | Código que puede lanzar excepciones |
| `except` | Solo si hay error | Manejar el error específico |
| `else` | Solo si NO hay error | Código que depende del éxito |
| `finally` | SIEMPRE | Limpieza (cerrar archivos, conexiones) |

### Ejemplo real: Procesar archivo

```python
def process_file(filepath: str) -> dict:
    """
    Procesa archivo y retorna estadísticas.

    Invariante: El archivo siempre se cierra, haya error o no.
    """
    file = None
    try:
        file = open(filepath, 'r')
        data = file.read()
        result = parse_data(data)  # Puede fallar
    except FileNotFoundError:
        print(f"Archivo no existe: {filepath}")
        return {}
    except ValueError as e:
        print(f"Datos inválidos: {e}")
        return {}
    else:
        # Solo ejecuta si parse_data() tuvo éxito
        print(f"Archivo procesado: {len(result)} registros")
        return result
    finally:
        # Siempre cierra el archivo
        if file:
            file.close()
```

**Por qué funciona:**
- `else` asegura que el print solo ocurra si todo fue bien
- `finally` garantiza que el archivo se cierra incluso si hay error
- Sin `else`, el print estaría en `try` y podría ejecutarse antes de un error

### Caso real: Transacción de base de datos

```python
def update_user(user_id: int, data: dict) -> bool:
    """
    Actualiza usuario en BD con rollback automático.

    Complejidad: O(1) asumiendo índice en user_id
    """
    conn = None
    try:
        conn = get_db_connection()
        conn.begin_transaction()
        conn.execute("UPDATE users SET ... WHERE id = ?", user_id, data)
    except DatabaseError as e:
        print(f"Error en BD: {e}")
        if conn:
            conn.rollback()
        return False
    else:
        # Solo commit si todo fue bien
        conn.commit()
        return True
    finally:
        # Siempre cierra la conexión
        if conn:
            conn.close()
```

---

## 2. Context Managers - `with` Statement

**Por qué:** `finally` funciona, pero `with` es más elegante y menos propenso a errores. Garantiza limpieza automática.

### El patrón

```python
# Sin context manager (propenso a errores)
file = open('data.txt')
try:
    data = file.read()
finally:
    file.close()

# Con context manager (limpio, seguro)
with open('data.txt') as file:
    data = file.read()
# file.close() se llama automáticamente
```

### Cómo funciona

Un context manager implementa dos métodos:
- `__enter__()`: Se ejecuta al entrar al bloque `with`
- `__exit__()`: Se ejecuta al salir (siempre, incluso con error)

### Ejemplo: Timer personalizado

```python
import time

class Timer:
    """Context manager para medir tiempo de ejecución."""

    def __init__(self, name: str):
        self.name = name
        self.start = 0

    def __enter__(self):
        """Inicia el timer."""
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Termina el timer y muestra resultado."""
        elapsed = time.perf_counter() - self.start
        print(f"{self.name}: {elapsed:.2f}s")
        # Return False = propaga excepción si la hubo
        return False

# Uso
with Timer("Procesamiento de datos"):
    process_large_dataset()
# Imprime: "Procesamiento de datos: 2.45s"
```

### Ejemplo: Estado temporal

```python
class TemporaryState:
    """Guarda y restaura estado automáticamente."""

    def __init__(self, obj, **kwargs):
        self.obj = obj
        self.new_state = kwargs
        self.old_state = {}

    def __enter__(self):
        # Guarda estado actual
        for key in self.new_state:
            self.old_state[key] = getattr(self.obj, key)
        # Aplica nuevo estado
        for key, val in self.new_state.items():
            setattr(self.obj, key, val)
        return self.obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restaura estado original
        for key, val in self.old_state.items():
            setattr(self.obj, key, val)
        return False

# Uso
config = Config(debug=False)
with TemporaryState(config, debug=True):
    # Aquí debug=True
    run_tests()
# Aquí debug=False otra vez
```

### Atajo con `contextlib.contextmanager`

```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """Context manager simple con decorador."""
    start = time.perf_counter()
    try:
        yield  # Aquí se ejecuta el bloque with
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.2f}s")

# Uso idéntico
with timer("Carga de datos"):
    load_data()
```

**Cuándo crear un context manager:**
-  Necesitas setup + cleanup (abrir/cerrar, iniciar/detener)
-  Quieres garantizar que el cleanup ocurra
-  Tienes estado temporal que debe restaurarse

**Ver ejemplos completos:** `04_ejemplos_runnable/ejemplo_02_context_managers.py`

---

## 3. Custom Exceptions - Jerarquías de Error

**Por qué:** Las excepciones built-in (`ValueError`, `TypeError`) no siempre expresan tu dominio. Las custom exceptions documentan qué puede fallar.

### Cuándo crear excepciones personalizadas

| Situación | Usa built-in | Crea custom |
|-----------|--------------|-------------|
| Argumento inválido (tipo/valor) | `ValueError`, `TypeError` |  |
| Archivo no existe | `FileNotFoundError` |  |
| Error específico de tu dominio |  |  |
| Necesitas metadata adicional |  |  |
| Quieres catch granular |  |  |

### Patrón: Jerarquía de excepciones

```python
# Base exception para tu módulo
class APIError(Exception):
    """Excepción base para errores de API."""
    pass

# Errores específicos heredan de la base
class AuthenticationError(APIError):
    """Fallo de autenticación."""
    pass

class RateLimitError(APIError):
    """Rate limit excedido."""

    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after}s")

class ResourceNotFoundError(APIError):
    """Recurso no encontrado."""

    def __init__(self, resource_type: str, resource_id: str):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} {resource_id} not found")
```

### Por qué funciona

```python
def handle_api_call():
    try:
        result = api.get_user(user_id)
    except AuthenticationError:
        # Re-login
        api.authenticate()
        result = api.get_user(user_id)
    except RateLimitError as e:
        # Espera el tiempo indicado
        time.sleep(e.retry_after)
        result = api.get_user(user_id)
    except ResourceNotFoundError as e:
        # Log específico
        logger.warning(f"User {e.resource_id} not found")
        return None
    except APIError:
        # Catch-all para otros errores de API
        logger.error("Unexpected API error")
        raise

# Beneficio: Cada error tiene su estrategia de recovery
```

### Ejemplo real: Sistema de pagos

```python
class PaymentError(Exception):
    """Excepción base para errores de pago."""
    pass

class InsufficientFundsError(PaymentError):
    """Fondos insuficientes."""

    def __init__(self, available: float, required: float):
        self.available = available
        self.required = required
        super().__init__(
            f"Insufficient funds: ${available:.2f} < ${required:.2f}"
        )

class PaymentGatewayError(PaymentError):
    """Error del gateway de pago."""

    def __init__(self, gateway: str, code: str, message: str):
        self.gateway = gateway
        self.code = code
        super().__init__(f"{gateway} error {code}: {message}")

def process_payment(amount: float, account: Account):
    """
    Procesa pago con manejo granular de errores.

    Complejidad: O(1)
    Raises: InsufficientFundsError, PaymentGatewayError
    """
    if account.balance < amount:
        raise InsufficientFundsError(account.balance, amount)

    try:
        gateway.charge(account, amount)
    except GatewayException as e:
        raise PaymentGatewayError("Stripe", e.code, e.message) from e
```

---

## 4. Exception Chaining - `raise from`

**Por qué:** Cuando atrapas una excepción y lanzas otra, pierdes contexto. `raise from` preserva el traceback completo.

### Antipatrón: Perder contexto

```python
#  MAL: Pierde el traceback original
try:
    result = int(user_input)
except ValueError:
    raise CustomError("Invalid input")  # Traceback solo muestra esta línea
```

### Patrón correcto: Preservar contexto

```python
#  BIEN: Preserva el traceback completo
try:
    result = int(user_input)
except ValueError as e:
    raise CustomError("Invalid input") from e
    # Traceback muestra: ValueError -> CustomError (completo)
```

### Ejemplo real

```python
class ConfigurationError(Exception):
    """Error de configuración."""
    pass

def load_config(filepath: str) -> dict:
    """
    Carga configuración con contexto de error completo.

    Raises: ConfigurationError
    """
    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise ConfigurationError(
            f"Config file not found: {filepath}"
        ) from e
    except json.JSONDecodeError as e:
        raise ConfigurationError(
            f"Invalid JSON in config: {e.msg} at line {e.lineno}"
        ) from e

    return data

# Al atrapar ConfigurationError, tienes el traceback completo
# incluyendo el FileNotFoundError o JSONDecodeError original
```

### Suprimir contexto con `from None`

```python
# Si realmente NO quieres mostrar la excepción original
try:
    result = int(user_input)
except ValueError:
    raise CustomError("Invalid input") from None
    # Traceback solo muestra CustomError (sin el ValueError)
```

**Cuándo usar:**
- `raise from e`: Casi siempre (preserva debugging)
- `raise from None`: Solo cuando el error original no aporta información

---

## 5. Excepciones Específicas vs Genéricas

**Por qué:** `except Exception:` atrapa TODO, incluso errores que no deberías atrapar (KeyboardInterrupt, SystemExit).

### Tabla de decisión

```
¿Sabes qué error específico puede ocurrir?
├─ SÍ → Usa la excepción específica
│   Ejemplo: except FileNotFoundError, ValueError
└─ NO → ¿Realmente necesitas atrapar todo?
    ├─ SÍ (logging, cleanup) → except Exception: + re-raise
    └─ NO → Deja que se propague
```

### Antipatrón: Catch-all demasiado amplio

```python
#  MAL: Atrapa incluso Ctrl+C
try:
    process_data()
except:  # Atrapa BaseException (incluso SystemExit!)
    logger.error("Error")

#  TAMBIÉN MAL: Atrapa exceptions que no puedes manejar
try:
    result = api.call()
except Exception:
    return None  # Silencia errores de red, bugs, etc.
```

### Patrón correcto: Específico a genérico

```python
#  BIEN: Específico primero, genérico después
try:
    result = api.call()
except requests.ConnectionError:
    # Error específico que sé manejar
    logger.warning("Connection failed, retrying...")
    time.sleep(5)
    result = api.call()
except requests.HTTPError as e:
    # Otro error específico
    if e.status_code == 429:
        handle_rate_limit()
    else:
        raise
except Exception as e:
    # Catch-all para logging, pero re-raise
    logger.error(f"Unexpected error: {e}")
    raise  # No silencies el error
```

### Excepciones que NO debes atrapar

```python
#  Casi nunca atra pas estas:
- BaseException  # Demasiado amplio
- SystemExit     # Permite que el programa termine
- KeyboardInterrupt  # Usuario quiere cancelar
- GeneratorExit  # Control interno de generators

#  Atrapa estas si aplican:
- Exception (y sus subclases)
- Específicas: ValueError, FileNotFoundError, etc.
```

---

## 6. Error Handling Patterns - LBYL vs EAFP

**Por qué:** Python prefiere EAFP (Easier to Ask for Forgiveness than Permission), pero LBYL tiene su lugar.

### LBYL (Look Before You Leap)

```python
# Chequea antes de actuar
if 'key' in my_dict:
    value = my_dict['key']
else:
    value = default

if os.path.exists(filepath):
    with open(filepath) as f:
        data = f.read()
```

**Pros:** Explícito, fácil de leer
**Cons:** Race conditions (el archivo puede desaparecer entre check y open)

### EAFP (Easier to Ask for Forgiveness than Permission)

```python
# Intenta y maneja el error
try:
    value = my_dict['key']
except KeyError:
    value = default

try:
    with open(filepath) as f:
        data = f.read()
except FileNotFoundError:
    data = default_data
```

**Pros:** Más eficiente (un solo check), evita race conditions
**Cons:** Puede ser menos legible

### Cuándo usar cada uno

| Situación | Usa LBYL | Usa EAFP |
|-----------|----------|----------|
| Performance crítico |  |  |
| Operación esperada que falle |  |  |
| Chequeo simple de existencia |  |  |
| Evitar race conditions |  |  |
| Código más legible | Depende | Depende |

### Ejemplo: Dictionary access

```python
# LBYL (múltiples checks)
if user_id in users and 'email' in users[user_id]:
    email = users[user_id]['email']
else:
    email = 'no-email@example.com'

# EAFP (un solo try)
try:
    email = users[user_id]['email']
except (KeyError, TypeError):
    email = 'no-email@example.com'

# O mejor: usa .get()
email = users.get(user_id, {}).get('email', 'no-email@example.com')
```

---

## 7. Anti-Patterns - Qué NO Hacer

###  1. Silent failures

```python
# MAL: Silencia todos los errores
try:
    result = risky_operation()
except:
    pass  # Usuario no sabe que falló

# BIEN: Log el error o re-raise
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise
```

###  2. Usar exceptions para control de flujo

```python
# MAL: Exceptions no son if/else
try:
    user = users[user_id]
except KeyError:
    user = create_new_user()

# BIEN: Usa if
user = users.get(user_id)
if user is None:
    user = create_new_user()
```

###  3. Catch demasiado amplio sin re-raise

```python
# MAL: Atrapa pero no maneja
try:
    result = complex_operation()
except Exception:
    return None  # ¿Qué salió mal? No se sabe

# BIEN: Atrapa específico o re-raise
try:
    result = complex_operation()
except SpecificError as e:
    logger.error(f"Known issue: {e}")
    return fallback_result()
except Exception as e:
    logger.error(f"Unexpected: {e}")
    raise  # Re-lanza para debugging
```

###  4. No usar context managers

```python
# MAL: Propenso a resource leaks
file = open('data.txt')
data = file.read()
file.close()  # ¿Y si hay error antes de esta línea?

# BIEN: Usa context manager
with open('data.txt') as file:
    data = file.read()
# Cierra automáticamente
```

---

## Resumen: Cuándo Usar Qué

| Necesitas | Herramienta |
|-----------|-------------|
| Setup + cleanup | `with` statement (context manager) |
| Acción solo si no hubo error | `else` block |
| Limpieza que siempre ocurre | `finally` block |
| Errores específicos de tu dominio | Custom exceptions |
| Preservar contexto de error | `raise from` |
| Evitar race conditions | EAFP (try/except) |
| Chequeo simple de existencia | LBYL (if) |
| Log + re-raise | `except Exception` + `raise` |

**Regla de oro:** Las excepciones son para situaciones excepcionales, no para control de flujo normal.

---

**Siguiente:** Ver código ejecutable en:
- `04_ejemplos_runnable/ejemplo_01_excepciones.py`
- `04_ejemplos_runnable/ejemplo_02_context_managers.py`
