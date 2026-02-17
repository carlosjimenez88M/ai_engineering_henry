# Control de flujo

## 1. if / elif / else
```python
x = 10
if x > 0:
    print("positivo")
elif x == 0:
    print("cero")
else:
    print("negativo")
```

Por qué funciona: la primera condición verdadera corta el resto.

## 2. for
```python
for i in range(5):
    print(i)
```

`range(5)` produce 0..4. Usamos `for` cuando sabemos el número de iteraciones.

Tip: si necesitas índice y valor a la vez:
```python
for i, x in enumerate(["a", "b", "c"]):
    print(i, x)
```

## 3. while
```python
n = 3
while n > 0:
    print(n)
    n -= 1
```

Usamos `while` cuando la condición es más importante que la cantidad de vueltas.

## 4. break / continue
- `break` corta el loop.
- `continue` salta a la siguiente vuelta.

Ejemplo:
```python
for x in [1, 2, 3, 4, 5]:
    if x == 3:
        continue
    if x == 5:
        break
    print(x)
```

## 5. Comprensiones (listas)

**Por qué importan:** Son más rápidas y expresivas que un for loop para transformaciones simples.

### Sintaxis básica

```python
# Transformación simple
squares = [x * x for x in range(5)]
# [0, 1, 4, 9, 16]

# Con filtro
pares = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Transformación + filtro
cuadrados_pares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

### Equivalente con for loop

```python
# List comprehension
cuadrados = [x**2 for x in range(5)]

# For loop equivalente
cuadrados = []
for x in range(5):
    cuadrados.append(x**2)
```

### Cuándo usar comprehension vs for loop

| Usa comprehension | Usa for loop |
|-------------------|--------------|
|  Transformación simple |  Lógica compleja |
|  Una línea legible |  Múltiples condiciones |
|  No necesitas print/debug |  Necesitas debugging |
|  Sin break/continue |  Necesitas break/continue |

### Ejemplos

```python
#  BIEN: comprehension simple y clara
nombres_mayusculas = [nombre.upper() for nombre in nombres]
numeros_positivos = [n for n in numeros if n > 0]

#  MAL: comprehension muy compleja (usa for loop)
resultado = [transform(x) for x in datos if x > 0 and validate(x) and check(x)]

#  BIEN: for loop para lógica compleja
resultado = []
for x in datos:
    if x > 0 and validate(x):
        if check(x):
            resultado.append(transform(x))
```

**Ver guía completa:** `10_comprension_vs_loops.md` con benchmarks, patrones y cuándo usar qué.
