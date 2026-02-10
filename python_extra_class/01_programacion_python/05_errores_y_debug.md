# Errores y debug

**Por qué importa:** El 90% del tiempo programando es debugging. Saber leer errores y debuggear eficientemente te hace 10x más productivo.

**Para temas avanzados:** Lee `08_excepciones_avanzadas.md` después de dominar estos conceptos básicos.

---

## 1. Errores comunes en Python

### 1.1 SyntaxError - Error de sintaxis

**Qué es:** Python no puede parsear tu código.

```python
# ❌ Error: falta paréntesis de cierre
def suma(a, b:
    return a + b

# ❌ Error: falta dos puntos
if x > 5
    print(x)

# ✅ Correcto
def suma(a, b):
    return a + b

if x > 5:
    print(x)
```

**Cómo arreglarlo:** El error te dice la línea exacta. Busca paréntesis/corchetes sin cerrar, dos puntos faltantes, comillas sin cerrar.

### 1.2 NameError - Variable no definida

**Qué es:** Usas una variable que no existe.

```python
# ❌ Error: 'resultado' no está definido
print(resultado)

# ✅ Correcto: define antes de usar
resultado = 42
print(resultado)
```

**Cómo arreglarlo:** Define la variable antes de usarla, o verifica typos en el nombre.

### 1.3 TypeError - Tipo incorrecto

**Qué es:** Operación inválida para ese tipo.

```python
# ❌ Error: no puedes sumar string + int
x = "5" + 3

# ✅ Correcto: convierte tipos
x = int("5") + 3  # → 8
y = "5" + str(3)  # → "53"
```

**Cómo arreglarlo:** Verifica los tipos con `print(type(x))` y convierte según necesites.

### 1.4 IndexError - Índice fuera de rango

**Qué es:** Intentas acceder a índice que no existe.

```python
arr = [1, 2, 3]

# ❌ Error: solo hay índices 0, 1, 2
print(arr[3])

# ✅ Correcto: verifica longitud
if len(arr) > 3:
    print(arr[3])
else:
    print("Índice fuera de rango")
```

### 1.5 KeyError - Clave no existe en diccionario

**Qué es:** Intentas acceder a key que no existe.

```python
usuario = {"nombre": "Ana", "edad": 25}

# ❌ Error: 'email' no existe
print(usuario["email"])

# ✅ Correcto: usa .get() con default
print(usuario.get("email", "No especificado"))

# O verifica antes
if "email" in usuario:
    print(usuario["email"])
```

### 1.6 AttributeError - Atributo no existe

**Qué es:** El objeto no tiene ese atributo/método.

```python
texto = "Hola"

# ❌ Error: strings no tienen .append()
texto.append("!")

# ✅ Correcto: strings usan +
texto = texto + "!"
```

### 1.7 IndentationError - Indentación incorrecta

**Qué es:** La indentación (espacios/tabs) está mal.

```python
# ❌ Error: el return no está indentado
def suma(a, b):
return a + b

# ✅ Correcto: 4 espacios de indentación
def suma(a, b):
    return a + b
```

---

## 2. try / except - Manejo de errores

**Por qué usarlo:** Protege el flujo normal y te deja manejar casos esperados (input inválido, archivo no existe, etc).

### Patrón básico

```python
try:
    x = int("abc")  # Esto lanzará ValueError
except ValueError:
    print("No es un número válido")
    x = 0  # Valor por defecto
```

### Regla de oro: Captura específico, nunca genérico

```python
# ❌ MAL: Captura TODO, incluso errores que no esperas
try:
    resultado = operacion_compleja()
except:
    print("Error")

# ✅ BIEN: Captura solo el error que esperas
try:
    resultado = int(user_input)
except ValueError:
    print("Debes ingresar un número")
    resultado = 0
```

### Múltiples excepciones

```python
try:
    archivo = open("datos.txt")
    contenido = archivo.read()
    numero = int(contenido)
except FileNotFoundError:
    print("Archivo no existe")
except ValueError:
    print("El archivo no contiene un número válido")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    # Siempre se ejecuta, haya error o no
    if 'archivo' in locals():
        archivo.close()
```

**Ver ejemplos avanzados:** `08_excepciones_avanzadas.md` y `04_ejemplos_runnable/ejemplo_01_excepciones.py`

---

## 3. Workflow de debugging

### 3.1 Debug con prints (La herramienta más usada)

```python
def buscar_maximo(nums):
    print(f"DEBUG: nums = {nums}")  # Ver input
    best = nums[0]
    for i, n in enumerate(nums):
        print(f"DEBUG: i={i}, n={n}, best={best}")  # Ver cada paso
        if n > best:
            best = n
    print(f"DEBUG: resultado final = {best}")  # Ver output
    return best
```

**Por qué funciona:** Ver el estado en cada paso te muestra dónde está el problema.

**Tip:** Usa un prefijo como "DEBUG:" para encontrar y eliminar los prints fácilmente después.

### 3.2 Debug con assert

```python
def calcular_promedio(nums):
    assert len(nums) > 0, "La lista no puede estar vacía"
    total = sum(nums)
    promedio = total / len(nums)
    assert 0 <= promedio <= 100, f"Promedio inválido: {promedio}"
    return promedio
```

**Por qué funciona:** `assert` detiene el programa si la condición es False. Úsalo para verificar invariantes.

### 3.3 Debug con type hints y herramientas

```python
# Los type hints ayudan a detectar errores ANTES de ejecutar
def procesar(datos: list[int]) -> int:
    return sum(datos)

# Herramientas como mypy o pyright detectan:
procesar("123")  # ❌ Error: espera list[int], recibe str
```

### 3.4 Estrategia de debugging paso a paso

1. **Reproduce el error:** Crea un caso mínimo que falle
2. **Lee el traceback:** Última línea = tipo de error y ubicación
3. **Agrega prints:** Antes y después de la línea con error
4. **Verifica invariantes:** ¿Qué debería ser cierto en cada paso?
5. **Divide el problema:** Comenta secciones para aislar el bug
6. **Testa casos límite:** ¿Funciona con lista vacía? ¿Con 1 elemento?

---

## 4. Leer el traceback (stack trace)

**Regla de oro:** Lee el traceback de **abajo hacia arriba**.

### Ejemplo de traceback

```
Traceback (most recent call last):
  File "main.py", line 15, in <module>
    resultado = procesar_datos(usuarios)
  File "main.py", line 8, in procesar_datos
    return calcular(datos["edad"])
  File "main.py", line 3, in calcular
    return valor / 0
ZeroDivisionError: division by zero
```

### Cómo leerlo

1. **Última línea:** `ZeroDivisionError: division by zero`
   - Tipo de error: División por cero
   - Mensaje: "division by zero"

2. **Penúltima sección:** `File "main.py", line 3, in calcular`
   - Archivo: main.py
   - Línea: 3
   - Función: calcular
   - Código: `return valor / 0` → ¡Aquí está el problema!

3. **Secciones anteriores:** La cadena de llamadas
   - main.py:15 llamó a procesar_datos()
   - procesar_datos() llamó a calcular()
   - calcular() causó el error

### Tipos de error más comunes y cómo arreglarlos

| Error | Causa | Solución |
|-------|-------|----------|
| `NameError: name 'x' is not defined` | Variable no existe | Define `x` antes de usarla |
| `TypeError: unsupported operand type(s)` | Operación entre tipos incompatibles | Convierte tipos: `int()`, `str()` |
| `IndexError: list index out of range` | Índice no existe | Verifica `len(lista)` antes de acceder |
| `KeyError: 'key'` | Clave no existe en dict | Usa `.get('key', default)` |
| `AttributeError: 'X' has no attribute 'Y'` | Atributo no existe | Verifica documentación del objeto |
| `ZeroDivisionError` | División por cero | Verifica `if divisor != 0:` antes |
| `FileNotFoundError` | Archivo no existe | Verifica path o usa try/except |

---

## 5. Pensamiento de invariantes

**Qué son:** Condiciones que DEBEN ser ciertas en cada paso del algoritmo.

### Ejemplo: Buscar máximo

```python
def buscar_maximo(nums):
    """
    Invariante: best siempre contiene el máximo de los elementos vistos hasta ahora.
    """
    best = nums[0]  # Invariante: best = max(nums[0:1])
    for i in range(1, len(nums)):
        # Invariante al inicio: best = max(nums[0:i])
        if nums[i] > best:
            best = nums[i]
        # Invariante al final: best = max(nums[0:i+1])
    return best  # Invariante final: best = max(nums)
```

### Ejemplo: Búsqueda binaria

```python
def binary_search(nums, target):
    """
    Invariante: Si target está en nums, está en nums[lo:hi+1].
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        # Invariante: target está en nums[lo:hi+1] si está en nums
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1  # Descarta mitad izquierda
        else:
            hi = mid - 1  # Descarta mitad derecha
        # Invariante se mantiene
    return -1
```

**Por qué importa:** Si identificas el invariante, puedes verificar con `assert` en cada paso y encontrar bugs rápidamente.

---

## 6. Herramientas de debugging

### 6.1 pdb - Python Debugger (built-in)

```python
import pdb

def funcion_compleja(x, y):
    resultado = x * 2
    pdb.set_trace()  # Pausa ejecución aquí
    resultado = resultado + y
    return resultado

# Al ejecutar, entra en modo interactivo:
# (Pdb) print(resultado)  → 10
# (Pdb) print(y)          → 5
# (Pdb) n                 → Siguiente línea
# (Pdb) c                 → Continuar ejecución
```

### 6.2 logging - Mejor que print para producción

```python
import logging

logging.basicConfig(level=logging.DEBUG)

def procesar(datos):
    logging.debug(f"Entrada: {datos}")  # Solo en desarrollo
    resultado = datos * 2
    logging.info(f"Procesado: {resultado}")  # Info general
    return resultado
```

**Por qué mejor que print:**
- Puedes desactivar logs sin eliminar código
- Puedes guardar logs en archivo
- Niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Ver más:** `11_logging_patterns.md`

---

## 7. Consejos prácticos

### ✅ DO: Haz esto

1. **Lee el error completo** - No adivines, lee el mensaje
2. **Reproduce el error** - Crea un caso mínimo
3. **Usa prints liberalmente** - No es "sucio", es eficiente
4. **Verifica tipos** - `print(type(x))` es tu amigo
5. **Testa casos límite** - Vacío, un elemento, muchos elementos
6. **Declara invariantes** - Escribe qué debe ser cierto
7. **Lee código en voz alta** - Ayuda a encontrar errores lógicos

### ❌ DON'T: Evita esto

1. **No uses `except:` sin especificar** - Atrapa todo, incluso bugs
2. **No ignores warnings** - Son errores esperando suceder
3. **No copies código sin entender** - Entender > copiar
4. **No debuggees con cambios aleatorios** - Entiende el problema primero
5. **No asumas tipos** - Verifica con `type()` o `isinstance()`

---

## Resumen: Tu flujo de debugging

```
¿Hay error?
├─ SÍ → Lee el traceback (última línea primero)
│   ├─ ¿Entiendes el error?
│   │   ├─ SÍ → Arréglalo
│   │   └─ NO → Agrega prints alrededor del error
│   └─ ¿Sigues sin entender?
│       └─ Reproduce con caso mínimo + verifica invariantes
└─ NO (funciona pero resultado incorrecto)
    ├─ Agrega prints en cada paso
    ├─ Verifica invariantes con assert
    └─ Testa casos límite (vacío, 1 elemento, etc)
```

---

**Siguiente:**
- **Temas avanzados:** `08_excepciones_avanzadas.md`
- **Código ejecutable:** `04_ejemplos_runnable/ejemplo_01_excepciones.py`
- **Logging para producción:** `11_logging_patterns.md`
