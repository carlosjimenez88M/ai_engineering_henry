# Ejercicios guiados (fundamentos)

## 1. Suma de pares
Enunciado: dada una lista, suma solo los números pares.

Pista mental: filtrar por `n % 2 == 0` y acumular.

Código:
```python
def suma_pares(nums):
    total = 0
    for n in nums:
        if n % 2 == 0:
            total += n
    return total
```

Por qué funciona: `total` siempre representa la suma de pares vistos.

## 2. Contar vocales
Enunciado: cuenta cuántas vocales tiene un string.

Código:
```python
def contar_vocales(s):
    vocales = set("aeiou")
    c = 0
    for ch in s.lower():
        if ch in vocales:
            c += 1
    return c
```

Por qué `set`: la verificación `in` es O(1) promedio.

## 3. Máximo en lista
Enunciado: retorna el mayor número de una lista no vacía.

Código:
```python
def maximo(nums):
    best = nums[0]
    for n in nums[1:]:
        if n > best:
            best = n
    return best
```

Invariante: `best` es el mayor valor visto hasta ahora.
