# Funciones

## 1. Definir y llamar
```python
import math

def area_circulo(r):
    return math.pi * r * r

print(area_circulo(2))
```

Por qué usar función: encapsula una idea y evita repetir código. Si mañana cambias la fórmula, la cambias en un solo lugar.

## 2. Parámetros y valores por defecto
```python
def saludar(nombre, saludo="Hola"):
    return f"{saludo} {nombre}"
```

## 3. Scope
Variables dentro de la función son locales.
```python
x = 10

def f():
    x = 5
    return x

print(f())  # 5
print(x)    # 10
```

## 4. Funciones como objetos
```python
def doble(x):
    return 2 * x

f = doble
print(f(4))
```

Sirve para pasar comportamiento a otras funciones.

## 5. Documentar
```python
def promedio(nums):
    """Retorna el promedio de una lista de números."""
    return sum(nums) / len(nums)
```

## 6. Un error clasico: defaults mutables
Esto es una fuente real de bugs:
```python
def agregar(x, xs=[]):
    xs.append(x)
    return xs
```

Por qué es peligroso: `xs` se crea una sola vez (al definir la función), no en cada llamada.

La forma correcta:
```python
def agregar(x, xs=None):
    if xs is None:
        xs = []
    xs.append(x)
    return xs
```

## 7. Funciones generadoras (yield)

**Por qué importan:** Permiten generar valores uno a la vez, sin almacenar toda la secuencia en memoria.

### Concepto básico

```python
# Función normal: retorna todo de una vez
def numeros_lista(n):
    resultado = []
    for i in range(n):
        resultado.append(i)
    return resultado  # Crea lista completa en memoria

# Función generadora: retorna valores uno a la vez
def numeros_generador(n):
    for i in range(n):
        yield i  # Pausa y retorna un valor, continúa después

# Uso
for num in numeros_generador(5):
    print(num)  # 0, 1, 2, 3, 4
```

### yield vs return

| Característica | `return` | `yield` |
|----------------|----------|---------|
| Cuántas veces | Una sola vez | Múltiples veces |
| Qué retorna | Valor final | Genera secuencia |
| Memoria | Toda la secuencia | Un valor a la vez |
| Reutilizable | Sí | No (se agota) |

### Ejemplo práctico: Leer archivo grande

```python
#  MAL: Lee todo el archivo a memoria
def leer_archivo(filepath):
    with open(filepath) as f:
        return f.readlines()  # Todo en RAM

#  BIEN: Lee línea por línea
def leer_archivo_generador(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()  # Una línea a la vez

# Uso: eficiente incluso con archivos gigantes
for linea in leer_archivo_generador('archivo_enorme.txt'):
    procesar(linea)
```

### Cuándo usar generadores

-  Datasets grandes (no caben en RAM)
-  Solo iteras una vez
-  Pipelines de datos (filtrar → transformar → procesar)
-  Necesitas acceso aleatorio (lista[5])
-  Necesitas iterar múltiples veces

**Ver guía completa:** `09_generadores_e_iteradores.md` y `04_ejemplos_runnable/ejemplo_03_generadores.py`
