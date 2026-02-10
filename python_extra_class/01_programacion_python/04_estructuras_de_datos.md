# Estructuras de datos

## 1. Listas
```python
nums = [1, 2, 3]
nums.append(4)
nums[0] = 10
```

Usa listas cuando el orden importa y necesitas mutar.

## 2. Tuplas
```python
point = (3, 4)
```

Usa tuplas cuando quieres inmutabilidad y claridad semántica.

## 3. Diccionarios
```python
user = {"name": "Ana", "age": 21}
user["age"] = 22
```

Diccionarios dan acceso O(1) promedio por llave.

## 4. Sets
```python
seen = set()
seen.add(3)
```

Usa sets para pertenencia rápida y eliminar duplicados.

## 5. Strings
```python
s = "python"
print(s.upper())
print(s[0:3])
```

Recuerda: los strings son inmutables.
