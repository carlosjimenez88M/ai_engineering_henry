# Fundamentos

## 1. Variables y tipos
Una variable es un nombre que apunta a un valor. El tipo describe qué operaciones son válidas.

Ejemplo:
```python
x = 3          # int
pi = 3.14      # float
name = "Ada"   # str
is_ok = True   # bool
```

Por qué importa el tipo:
- No puedes sumar un string con un int.
- Un bool en Python es un int disfrazado (True == 1, False == 0).
 - El tipo te dice qué puedes asumir: si algo es `list`, puedes mutarlo; si es `tuple`, no.

## 2. Operadores
- Aritméticos: `+ - * / // % **`
- Comparación: `== != < > <= >=`
- Lógicos: `and or not`

Ejemplo:
```python
n = 7
is_even = (n % 2) == 0
```

Explicación: `n % 2` da el residuo al dividir por 2. Si es 0, entonces es par.

## 3. Entrada y salida
```python
name = input("Tu nombre: ")
print("Hola", name)
```

`input` siempre devuelve string. Si necesitas número:
```python
age = int(input("Edad: "))
```

## 4. Conversiones útiles
```python
int("42")
float("3.5")
str(100)
list("abc")  # ['a', 'b', 'c']
```

## 5. Inmutabilidad vs mutabilidad
- Inmutables: int, float, str, tuple
- Mutables: list, dict, set

Por qué importa: una lista puede cambiar sin crear otra; un string no.

## 6. Comprobar tipos (sin obsesionarse)
```python
x = 10
print(type(x))              # <class 'int'>
print(isinstance(x, int))   # True
```

La idea no es llenar el código de `isinstance`, sino entender qué espera tu función y fallar temprano si el input es inválido.
