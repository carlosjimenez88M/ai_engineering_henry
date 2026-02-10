# Ejercicios (10 básicos + 2 intermedios)

Antes de mirar una solución, usa este guion mental:
1. Reescribe el enunciado con tus palabras (y define inputs/outputs).
2. Piensa en un enfoque bruto (aunque sea O(n^2)). Te da un punto de partida correcto.
3. Pregunta: ¿dónde se repite trabajo? Ahí aparece el `dict`, el `set`, el ordenamiento o una DP.
4. Declara un invariante simple (qué debe ser cierto en cada paso).
5. Calcula complejidad (tiempo/espacio) y prueba con 2 casos límite.

## Básico 1: Two Sum
Patrón: hash map (diccionario).

Enunciado: dado un arreglo y un objetivo, retorna los índices de dos números que sumen el objetivo.

Idea: usar un diccionario para recordar lo ya visto.

Paso a paso:
1. Recorre el arreglo.
2. Calcula `faltante = target - n`.
3. Si `faltante` ya está en el diccionario, encontraste la pareja.
4. Si no, guarda el número actual con su índice.

Por qué funciona: cuando llegas al índice `i`, ya has registrado todos los elementos anteriores. Si existe el complemento, se detecta en O(1) promedio.

Complejidad: O(n) tiempo, O(n) espacio.

Código:
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i
```

### Casos de prueba
```python
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]
```

### Casos límite
- Array vacío: `two_sum([], 0)` → retorna `None`
- Un solo elemento: `two_sum([1], 5)` → retorna `None`
- Sin solución: `two_sum([1, 2], 10)` → retorna `None`
- Números negativos y ceros: `two_sum([-1, 0, 1], 0)` → debe manejar correctamente

### Preguntas de seguimiento (entrevista)
1. **"¿Qué pasa si el array no está ordenado?"**
   → La solución con hash map funciona igual, no requiere que esté ordenado. Complejidad O(n).

2. **"¿Y si el array está ordenado? ¿Hay mejor solución?"**
   → Sí, puedes usar dos punteros (left, right) desde extremos. Si suma < target, avanza left; si suma > target, retrocede right. También O(n) pero con O(1) espacio.

3. **"¿Cómo manejarías múltiples soluciones o devolver todos los pares?"**
   → En vez de retornar inmediatamente, acumula todas las parejas encontradas en una lista. Debes evitar duplicados usando un set o verificando que i < j.

### Solución alternativa (dos punteros, requiere array ordenado)
```python
def two_sum_sorted(nums, target):
    # Crear lista de (valor, índice_original) y ordenar
    indexed = [(n, i) for i, n in enumerate(nums)]
    indexed.sort()

    left, right = 0, len(indexed) - 1
    while left < right:
        suma = indexed[left][0] + indexed[right][0]
        if suma == target:
            return sorted([indexed[left][1], indexed[right][1]])
        elif suma < target:
            left += 1
        else:
            right -= 1
    return None
```

**Trade-offs:**
- Tiempo: Hash map O(n) vs Dos punteros O(n log n) por ordenamiento
- Espacio: Hash map O(n) vs Dos punteros O(n) para índices + O(1) si ya está ordenado
- Aplicabilidad: Hash map para no ordenado; dos punteros si ya está ordenado o espacio es crítico

### Errores comunes en entrevistas
1. ❌ Usar dos bucles anidados (O(n²)) sin considerar optimización
2. ❌ Olvidar verificar que los dos índices sean diferentes (cuando hay duplicados)
3. ❌ No manejar casos límite (array vacío, sin solución)

## Básico 2: Valid Palindrome
Patrón: dos punteros.

Enunciado: verifica si un string es palíndromo ignorando mayúsculas y caracteres no alfanuméricos.

Idea: dos punteros desde extremos.

Paso a paso:
1. `i` al inicio, `j` al final.
2. Avanza `i` si no es alfanumérico.
3. Retrocede `j` si no es alfanumérico.
4. Compara en minúsculas.

Por qué funciona: siempre comparas los caracteres relevantes en orden espejo; lo que ignoras no afecta el resultado.

Complejidad: O(n) tiempo, O(1) espacio.

Código:
```python
def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True
```

### Casos de prueba
```python
assert is_palindrome("A man, a plan, a canal: Panama") == True
assert is_palindrome("race a car") == False
assert is_palindrome("") == True
assert is_palindrome("Aa") == True
```

### Casos límite
- String vacío: `is_palindrome("")` → `True` (considerado palíndromo)
- Un solo carácter: `is_palindrome("a")` → `True`
- Solo espacios/puntuación: `is_palindrome("   ")` → `True`
- Solo caracteres no alfanuméricos: `is_palindrome("!!!")` → `True`

### Preguntas de seguimiento (entrevista)
1. **"¿Cómo lo harías si no puedes usar espacio extra?"**
   → La solución con dos punteros ya es O(1) espacio, es óptima.

2. **"¿Y si quisieras considerar también los espacios?"**
   → Elimina la verificación `isalnum()` y compara todos los caracteres después de normalizarlos a minúsculas.

3. **"¿Cómo optimizarías para strings muy largos con muchos caracteres no alfanuméricos?"**
   → Podrías preprocesar el string una vez (filtrar y convertir a minúsculas) y luego comparar, pero usaría O(n) espacio. Trade-off: espacio por simplicidad.

### Solución alternativa (con preprocesamiento)
```python
def is_palindrome_preprocess(s):
    # Filtrar y normalizar de una vez
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```

**Trade-offs:**
- Tiempo: Ambas O(n), pero preprocesamiento hace dos pasadas
- Espacio: Dos punteros O(1) vs Preprocesamiento O(n)
- Aplicabilidad: Dos punteros para espacio limitado; preprocesamiento si vas a verificar múltiples veces el mismo string

### Errores comunes en entrevistas
1. ❌ Olvidar normalizar mayúsculas/minúsculas antes de comparar
2. ❌ No saltar correctamente caracteres no alfanuméricos (comparar índices fuera de rango)
3. ❌ Crear un nuevo string filtrado sin considerar el espacio O(n) que consumes

## Básico 3: Reverse Linked List
Patrón: iteración + reasignación de punteros.

Enunciado: invierte una lista enlazada simple.

Idea: ir revirtiendo punteros con tres referencias.

Paso a paso:
1. `prev = None`, `cur = head`.
2. Guarda `nxt = cur.next` (el resto de la lista).
3. Apunta `cur.next` a `prev`.
4. Avanza `prev` y `cur`.

Por qué funciona: al final, `prev` es la nueva cabeza, porque cada nodo ya apunta hacia atrás.

Complejidad: O(n) tiempo, O(1) espacio.

Código:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```

### Casos de prueba
```python
# Lista: 1 -> 2 -> 3 -> 4 -> 5
assert linked_list_to_list(reverse_list(list_to_linked_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
assert linked_list_to_list(reverse_list(list_to_linked_list([1]))) == [1]
assert linked_list_to_list(reverse_list(list_to_linked_list([]))) == []
assert linked_list_to_list(reverse_list(list_to_linked_list([1, 2]))) == [2, 1]
```

### Casos límite
- Lista vacía: `reverse_list(None)` → `None`
- Un solo nodo: `reverse_list(ListNode(1))` → mismo nodo
- Dos nodos: lista mínima para verificar el swap correcto
- Lista larga: verificar que no hay pérdida de referencias

### Preguntas de seguimiento (entrevista)
1. **"¿Cómo lo harías de forma recursiva?"**
   → Base: si `head` es None o `head.next` es None, retorna `head`. Recursión: reversa el resto, luego `head.next.next = head` y `head.next = None`.

2. **"¿Cómo revertirías solo una parte de la lista (del nodo m al n)?"**
   → Guarda referencia al nodo antes de m, reversa la sublista usando la técnica estándar, y reconecta los extremos.

3. **"¿Qué complejidad tendría una solución con stack?"**
   → O(n) tiempo y O(n) espacio. Push todos los nodos, luego pop para reconstruir. Menos eficiente que la solución iterativa.

### Solución alternativa (recursiva)
```python
def reverse_list_recursive(head):
    # Caso base
    if not head or not head.next:
        return head

    # Reversa el resto de la lista
    new_head = reverse_list_recursive(head.next)

    # Reconecta: el siguiente de head ahora apunta a head
    head.next.next = head
    head.next = None

    return new_head
```

**Trade-offs:**
- Tiempo: Ambas O(n)
- Espacio: Iterativa O(1) vs Recursiva O(n) por call stack
- Aplicabilidad: Iterativa siempre mejor para listas muy largas (evita stack overflow); recursiva más elegante pero menos práctica

### Errores comunes en entrevistas
1. ❌ Perder la referencia al resto de la lista (olvidar guardar `nxt = cur.next`)
2. ❌ No actualizar correctamente `prev` antes de avanzar `cur`
3. ❌ Retornar `head` en vez de `prev` al final (la nueva cabeza es el último nodo procesado)

## Básico 4: Climbing Stairs
Patrón: programación dinámica (DP) lineal.

Enunciado: ¿cuántas formas hay de subir `n` escalones, si puedes subir 1 o 2?

Idea: DP con Fibonacci.

Paso a paso:
1. `ways[i] = ways[i-1] + ways[i-2]`.
2. Solo necesitas las dos últimas; por eso se puede usar dos variables en vez de un arreglo.

Por qué funciona: la última acción es subir 1 o 2 escalones; por eso `ways[n] = ways[n-1] + ways[n-2]`.

Complejidad: O(n) tiempo, O(1) espacio.

Código:
```python
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```

### Casos de prueba
```python
assert climb_stairs(1) == 1
assert climb_stairs(2) == 2
assert climb_stairs(3) == 3
assert climb_stairs(5) == 8
```

### Casos límite
- n = 1: solo una forma (un escalón)
- n = 2: dos formas (1+1, o 2)
- n grande (ej. n = 45): verificar que no haya overflow y sea eficiente
- n = 0: depende del problema, pero generalmente 1 forma (no hacer nada)

### Preguntas de seguimiento (entrevista)
1. **"¿Qué pasa si puedes subir 1, 2 o 3 escalones?"**
   → Cambias la fórmula a `ways[i] = ways[i-1] + ways[i-2] + ways[i-3]`. Necesitas 3 variables (a, b, c) en vez de 2.

2. **"¿Cómo optimizarías para consultas múltiples de diferentes valores de n?"**
   → Precalcula hasta el n máximo en un array. Luego cada consulta es O(1).

3. **"¿Puedes explicar por qué es Fibonacci?"**
   → Para llegar al escalón n, el último paso fue de 1 o 2 escalones. Por tanto: `f(n) = f(n-1) + f(n-2)`, que es la definición de Fibonacci.

### Solución alternativa (memoización con recursión)
```python
def climb_stairs_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 2:
        return n

    memo[n] = climb_stairs_memo(n-1, memo) + climb_stairs_memo(n-2, memo)
    return memo[n]
```

**Trade-offs:**
- Tiempo: Ambas O(n)
- Espacio: Iterativa O(1) vs Recursiva con memo O(n) (stack + diccionario)
- Aplicabilidad: Iterativa más eficiente; recursiva útil si tienes múltiples casos base complejos

### Errores comunes en entrevistas
1. ❌ Intentar recursión sin memoización (O(2^n), demasiado lento)
2. ❌ No reconocer el patrón de Fibonacci y complicar innecesariamente
3. ❌ Olvidar los casos base (n=1, n=2) y causar errores de índice

## Básico 5: Majority Element
Patrón: Boyer-Moore voting.

Enunciado: retorna el elemento que aparece más de n/2 veces.

Idea: algoritmo de Boyer-Moore.

Paso a paso:
1. Mantiene un candidato y un conteo.
2. Si conteo es 0, cambia candidato.
3. Si mismo valor, suma; si diferente, resta.

Por qué funciona: el elemento mayoritario no puede ser cancelado por completo por los no-mayoritarios; al final queda como candidato.

Complejidad: O(n) tiempo, O(1) espacio.

Código:
```python
def majority_element(nums):
    cand = None
    count = 0
    for n in nums:
        if count == 0:
            cand = n
        count += 1 if n == cand else -1
    return cand
```

### Casos de prueba
```python
assert majority_element([3, 2, 3]) == 3
assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2
assert majority_element([1]) == 1
assert majority_element([5, 5, 5, 5]) == 5
```

### Casos límite
- Un solo elemento: `majority_element([1])` → `1`
- Todos iguales: `majority_element([7, 7, 7])` → `7`
- Mayoría al final: verificar que el algoritmo no depende del orden
- Array grande con mayoría justa (n/2 + 1): caso límite de la definición

### Preguntas de seguimiento (entrevista)
1. **"¿Qué pasa si no hay elemento mayoritario?"**
   → El algoritmo de Boyer-Moore aún retorna un candidato, pero sería incorrecto. Necesitas una segunda pasada para verificar que el candidato realmente aparece > n/2 veces.

2. **"¿Cómo encontrarías todos los elementos que aparecen más de n/3 veces?"**
   → Versión extendida de Boyer-Moore con 2 candidatos. Puedes tener máximo 2 elementos con frecuencia > n/3.

3. **"¿Por qué funciona Boyer-Moore?"**
   → Si hay un elemento mayoritario (>n/2), no puede ser "cancelado" por completo. Los otros elementos juntos son < n/2, así que el contador nunca elimina permanentemente al mayoritario.

### Solución alternativa (usando hash map)
```python
def majority_element_hashmap(nums):
    counts = {}
    majority_threshold = len(nums) // 2

    for n in nums:
        counts[n] = counts.get(n, 0) + 1
        if counts[n] > majority_threshold:
            return n
```

**Trade-offs:**
- Tiempo: Ambas O(n)
- Espacio: Boyer-Moore O(1) vs Hash map O(n)
- Aplicabilidad: Boyer-Moore óptimo cuando se garantiza mayoría; hash map más versátil (puede contar todas las frecuencias)

### Errores comunes en entrevistas
1. ❌ Olvidar que Boyer-Moore asume que SÍ existe elemento mayoritario (no verifica)
2. ❌ No entender por qué funciona (pregunta común de seguimiento)
3. ❌ Usar sorting O(n log n) cuando existe O(n) con O(1) espacio

## Básico 6: Intersection of Two Arrays II
Patrón: conteo de frecuencias (hash map).

Enunciado: retorna la intersección con conteo.

Idea: contar frecuencias en un diccionario.

Paso a paso:
1. Cuenta elementos de `nums1`.
2. Recorre `nums2` y agrega si hay stock.

Por qué funciona: cada número se usa tantas veces como aparece en ambos; el conteo se reduce a medida que lo consumes.

Complejidad: O(n+m) tiempo, O(n) espacio.

Código:
```python
def intersect(nums1, nums2):
    counts = {}
    for n in nums1:
        counts[n] = counts.get(n, 0) + 1
    out = []
    for n in nums2:
        if counts.get(n, 0) > 0:
            out.append(n)
            counts[n] -= 1
    return out
```

### Casos de prueba
```python
assert sorted(intersect([1, 2, 2, 1], [2, 2])) == [2, 2]
assert sorted(intersect([4, 9, 5], [9, 4, 9, 8, 4])) == [4, 9]
assert intersect([1, 2], [3, 4]) == []
assert sorted(intersect([1, 1, 1], [1, 1])) == [1, 1]
```

### Casos límite
- Arrays vacíos: `intersect([], [])` → `[]`
- Un array vacío: `intersect([1], [])` → `[]`
- Sin intersección: `intersect([1, 2], [3, 4])` → `[]`
- Todos duplicados: `intersect([1, 1, 1], [1, 1])` → respeta frecuencias

### Preguntas de seguimiento (entrevista)
1. **"¿Qué harías si los arrays están ordenados?"**
   → Usa dos punteros. Compara elementos: si iguales, agrega e incrementa ambos; si diferentes, avanza el menor. O(n+m) tiempo, O(1) espacio extra.

2. **"¿Y si nums1 es mucho más pequeño que nums2?"**
   → Construye el hash map del array más pequeño (nums1) para minimizar espacio. La solución actual ya lo hace correctamente.

3. **"¿Cómo manejarías si los arrays no caben en memoria?"**
   → Divide en chunks, procesa por bloques. O usa external sorting si están ordenados y aplica dos punteros por streams.

### Solución alternativa (dos punteros, arrays ordenados)
```python
def intersect_sorted(nums1, nums2):
    nums1.sort()
    nums2.sort()
    i, j = 0, 0
    result = []

    while i < len(nums1) and j < len(nums2):
        if nums1[i] == nums2[j]:
            result.append(nums1[i])
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1

    return result
```

**Trade-offs:**
- Tiempo: Hash map O(n+m) vs Dos punteros O(n log n + m log m) por sorting
- Espacio: Hash map O(min(n,m)) vs Dos punteros O(1) si ya ordenados, O(log n) del sort en Python
- Aplicabilidad: Hash map general; dos punteros si ya ordenados o espacio crítico

### Errores comunes en entrevistas
1. ❌ Usar sets (perdería información de frecuencias, solo contaría una vez)
2. ❌ No decrementar el contador después de usar un elemento
3. ❌ No considerar que el resultado puede tener duplicados válidos

## Básico 7: Single Number
Patrón: bit manipulation (XOR).

Enunciado: todos aparecen dos veces excepto uno; retorna el único.

Idea: XOR cancela pares.

Paso a paso:
1. Inicializa `x = 0`.
2. `x ^= n` para cada elemento.

Por qué funciona: `a ^ a = 0`, y `0 ^ b = b` (los pares se cancelan).

Complejidad: O(n) tiempo, O(1) espacio.

Código:
```python
def single_number(nums):
    x = 0
    for n in nums:
        x ^= n
    return x
```

### Casos de prueba
```python
assert single_number([2, 2, 1]) == 1
assert single_number([4, 1, 2, 1, 2]) == 4
assert single_number([1]) == 1
assert single_number([-1, -1, -2]) == -2
```

### Casos límite
- Un solo elemento: `single_number([1])` → `1`
- Números negativos: `single_number([-1, -1, -2])` → `-2` (XOR funciona con negativos)
- Cero en el array: `single_number([0, 1, 0])` → `1`
- Número único al principio o al final: verificar que el orden no importa

### Preguntas de seguimiento (entrevista)
1. **"¿Qué pasa si hay dos números únicos (todos los demás aparecen dos veces)?"**
   → XOR de todos da `a ^ b`. Usa cualquier bit set en ese resultado para dividir los números en dos grupos, y aplica XOR a cada grupo.

2. **"¿Y si todos aparecen tres veces excepto uno?"**
   → Cuenta bits en cada posición. Si el conteo % 3 != 0, ese bit pertenece al número único. Reconstruyes el número bit por bit.

3. **"¿Por qué funciona XOR?"**
   → Propiedades: `a ^ a = 0`, `0 ^ b = b`, y XOR es conmutativo/asociativo. Los pares se cancelan, solo queda el único.

### Solución alternativa (usando hash set)
```python
def single_number_set(nums):
    seen = set()
    for n in nums:
        if n in seen:
            seen.remove(n)
        else:
            seen.add(n)
    return seen.pop()
```

**Trade-offs:**
- Tiempo: Ambas O(n)
- Espacio: XOR O(1) vs Set O(n)
- Aplicabilidad: XOR óptimo y elegante; set más intuitivo pero menos eficiente en espacio

### Errores comunes en entrevistas
1. ❌ No conocer la técnica de XOR (intentar hash map o sorting innecesariamente)
2. ❌ Pensar que XOR no funciona con números negativos (sí funciona, opera a nivel de bits)
3. ❌ Olvidar inicializar el acumulador en 0

## Básico 8: Move Zeroes
Patrón: dos punteros (escritura compacta).

Enunciado: mueve todos los ceros al final, manteniendo el orden.

Idea: dos punteros, escribe los no-ceros y luego completa con ceros.

Paso a paso:
1. `k` es la posición de escritura.
2. Copia cada número no-cero a `nums[k]` y suma `k`.
3. Rellena con ceros desde `k`.

Por qué funciona: los no-ceros se reescriben en orden; el resto, por definición, debe ser cero.

Complejidad: O(n) tiempo, O(1) espacio.

Código:
```python
def move_zeroes(nums):
    # Modifica `nums` in-place y retorna None.
    k = 0
    for n in nums:
        if n != 0:
            nums[k] = n
            k += 1
    for i in range(k, len(nums)):
        nums[i] = 0
```

### Casos de prueba
```python
nums = [0, 1, 0, 3, 12]
move_zeroes(nums)
assert nums == [1, 3, 12, 0, 0]

nums = [0]
move_zeroes(nums)
assert nums == [0]

nums = [1, 2, 3]
move_zeroes(nums)
assert nums == [1, 2, 3]
```

### Casos límite
- Un solo cero: `[0]` → `[0]`
- Sin ceros: `[1, 2, 3]` → `[1, 2, 3]`
- Todos ceros: `[0, 0, 0]` → `[0, 0, 0]`
- Ceros ya al final: `[1, 2, 0, 0]` → `[1, 2, 0, 0]` (sin cambios)

### Preguntas de seguimiento (entrevista)
1. **"¿Cómo minimizarías el número de escrituras?"**
   → En vez de copiar no-ceros y luego rellenar, usa swap solo cuando sea necesario. Dos punteros: uno para no-ceros, otro que recorre todo.

2. **"¿Puedes hacerlo con una sola pasada?"**
   → Sí, con swap inteligente. Cuando encuentras un no-cero, intercambialo con la posición `k` solo si `k != i`.

3. **"¿Qué pasa si quieres mover otros valores además de ceros?"**
   → Generaliza: en vez de `n != 0`, usa `n != target_value`. La lógica es la misma.

### Solución alternativa (swap en una pasada)
```python
def move_zeroes_swap(nums):
    k = 0  # posición para el próximo no-cero
    for i in range(len(nums)):
        if nums[i] != 0:
            # Swap solo si es necesario
            nums[k], nums[i] = nums[i], nums[k]
            k += 1
```

**Trade-offs:**
- Tiempo: Ambas O(n)
- Espacio: Ambas O(1)
- Aplicabilidad: Primera solución más clara (dos pasadas); swap más eficiente (una pasada, menos escrituras)

### Errores comunes en entrevistas
1. ❌ Crear un array nuevo en vez de modificar in-place (viola el requisito)
2. ❌ Perder el orden relativo de los elementos no-cero
3. ❌ Olvidar rellenar con ceros después de copiar los no-ceros

## Básico 9: Roman to Integer
Patrón: recorrido lineal con lookahead.

Enunciado: convierte un número romano a entero.

Idea: sumar valores, pero restar cuando un símbolo menor está antes de uno mayor.

Paso a paso:
1. Recorre el string.
2. Si el valor actual es menor que el siguiente, resta.
3. Si no, suma.

Por qué funciona: los casos especiales (IV, IX, etc) son exactamente los casos donde una letra menor va antes de una mayor.

Complejidad: O(n) tiempo, O(1) espacio.

Código:
```python
def roman_to_int(s):
    val = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}
    total = 0
    for i in range(len(s)):
        if i + 1 < len(s) and val[s[i]] < val[s[i+1]]:
            total -= val[s[i]]
        else:
            total += val[s[i]]
    return total
```

### Casos de prueba
```python
assert roman_to_int("III") == 3
assert roman_to_int("IV") == 4
assert roman_to_int("LVIII") == 58
assert roman_to_int("MCMXCIV") == 1994
```

### Casos límite
- Un solo carácter: `roman_to_int("I")` → `1`
- Valor máximo: `roman_to_int("MMMCMXCIX")` → `3999`
- Todos casos especiales: `roman_to_int("MCMXC")` → `1990` (CM=900, XC=90)
- Sin casos especiales: `roman_to_int("MMXX")` → `2020`

### Preguntas de seguimiento (entrevista)
1. **"¿Cómo convertirías de entero a romano (problema inverso)?"**
   → Usa una lista de pares (valor, símbolo) ordenada descendente. Mientras el número sea >= valor, resta y agrega símbolo. Incluye pares especiales (900:"CM", 400:"CD", etc).

2. **"¿Cómo validarías que un string romano es válido?"**
   → Verifica reglas: no más de 3 consecutivos para I,X,C,M; no más de 1 para V,L,D; solo combinaciones válidas de resta (IV, IX, XL, XC, CD, CM).

3. **"¿Se puede hacer en una pasada de derecha a izquierda?"**
   → Sí, mantén el valor anterior. Si el actual < anterior, resta; si no, suma. Es más elegante que lookahead.

### Solución alternativa (recorrido derecha a izquierda)
```python
def roman_to_int_reverse(s):
    val = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}
    total = 0
    prev_value = 0

    for ch in reversed(s):
        current = val[ch]
        if current < prev_value:
            total -= current
        else:
            total += current
        prev_value = current

    return total
```

**Trade-offs:**
- Tiempo: Ambas O(n)
- Espacio: Ambas O(1)
- Aplicabilidad: Lookahead más intuitivo; reverse más elegante (sin chequear índices)

### Errores comunes en entrevistas
1. ❌ Olvidar los casos especiales (IV, IX, XL, XC, CD, CM) y solo sumar valores
2. ❌ No manejar correctamente el lookahead (acceder fuera de rango)
3. ❌ Hardcodear casos especiales en vez de usar la regla general (menor antes de mayor = resta)

## Básico 10: Binary Search
Patrón: búsqueda binaria.

Enunciado: busca un valor en un arreglo ordenado.

Idea: dividir en mitades.

Paso a paso:
1. `lo` y `hi` delimitan el rango.
2. Calcula `mid`.
3. Ajusta límites según comparación.

Por qué funciona: cada paso descarta la mitad que no puede contener el valor.

Complejidad: O(log n) tiempo, O(1) espacio.

Código:
```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### Casos de prueba
```python
assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
assert binary_search([5], 5) == 0
assert binary_search([5], 3) == -1
```

### Casos límite
- Array vacío: `binary_search([], 1)` → `-1`
- Un elemento (encontrado): `binary_search([5], 5)` → `0`
- Un elemento (no encontrado): `binary_search([5], 3)` → `-1`
- Elemento al principio: `binary_search([1, 2, 3], 1)` → `0`
- Elemento al final: `binary_search([1, 2, 3], 3)` → `2`

### Preguntas de seguimiento (entrevista)
1. **"¿Cómo buscarías el primer/último índice si hay duplicados?"**
   → Modifica la condición: cuando encuentras el target, no retornes. Si buscas el primero, haz `hi = mid - 1`; si el último, `lo = mid + 1`. Al final, verifica el índice.

2. **"¿Cómo evitar overflow al calcular mid en otros lenguajes?"**
   → En vez de `mid = (lo + hi) // 2`, usa `mid = lo + (hi - lo) // 2`. En Python no hay overflow de enteros, pero es buena práctica.

3. **"¿Cómo buscarías en un array rotado (ej: [4,5,6,7,0,1,2])?"**
   → Primero determina qué mitad está ordenada. Luego verifica si el target está en ese rango ordenado. Ajusta lo/hi según corresponda. O(log n).

### Solución alternativa (buscar primer índice con duplicados)
```python
def binary_search_first(nums, target):
    lo, hi = 0, len(nums) - 1
    result = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            result = mid
            hi = mid - 1  # Sigue buscando a la izquierda
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return result
```

**Trade-offs:**
- Tiempo: Ambas O(log n)
- Espacio: Ambas O(1)
- Aplicabilidad: Clásica para elementos únicos; variante para duplicados o búsqueda de rangos

### Errores comunes en entrevistas
1. ❌ Usar `lo < hi` en vez de `lo <= hi` (pierde el caso cuando lo==hi)
2. ❌ No actualizar correctamente lo/hi (usar `mid` en vez de `mid+1` o `mid-1` causa loops infinitos)
3. ❌ Olvidar que el array debe estar ordenado (si no lo está, binary search no funciona)

---

## Intermedio 1: Group Anagrams
Patrón: hashing por firma (conteo de letras).

Enunciado: agrupa palabras que son anagramas.

Idea: usar la cuenta de letras como clave.

Paso a paso:
1. Para cada palabra, cuenta letras (26 posiciones).
2. Usa la tupla de conteos como llave.
3. Agrega la palabra al grupo.

Por qué funciona: anagramas tienen exactamente la misma cuenta de letras.

Complejidad: O(n * k) tiempo, O(n * k) espacio, donde k es longitud promedio.

Código:
```python
def group_anagrams(strs):
    groups = {}
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        key = tuple(count)
        groups.setdefault(key, []).append(s)
    return list(groups.values())
```

### Casos de prueba
```python
result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
# Resultado: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
assert len(result) == 3

assert group_anagrams([""]) == [[""]]
assert group_anagrams(["a"]) == [["a"]]
result = group_anagrams(["abc", "bca", "cab"])
assert len(result) == 1 and len(result[0]) == 3
```

### Casos límite
- String vacío: `group_anagrams([""])` → `[[""]]`
- Un solo string: `group_anagrams(["a"])` → `[["a"]]`
- Sin anagramas: todos los grupos tienen tamaño 1
- Todos anagramas: un solo grupo con todos los strings

### Preguntas de seguimiento (entrevista)
1. **"¿Qué pasa si hay caracteres no alfabéticos o mayúsculas?"**
   → Normaliza a minúsculas y expande el array de conteo para incluir todos los caracteres necesarios, o usa un diccionario en vez de array de 26.

2. **"¿Es la solución con sorting más simple? ¿Cuándo la usarías?"**
   → Sí: `key = ''.join(sorted(s))`. Más simple pero O(n * k log k) por el sort. Úsala si k (longitud) es muy pequeño o simplicidad es prioridad.

3. **"¿Cómo optimizarías para muchos strings muy largos?"**
   → La solución de conteo es mejor (O(n*k) vs O(n*k log k)). También podrías usar hashing más sofisticado (hash de primos por frecuencia).

### Solución alternativa (usando sorting)
```python
def group_anagrams_sorted(strs):
    groups = {}
    for s in strs:
        key = ''.join(sorted(s))
        groups.setdefault(key, []).append(s)
    return list(groups.values())
```

**Trade-offs:**
- Tiempo: Conteo O(n*k) vs Sorting O(n*k log k)
- Espacio: Ambas O(n*k) para almacenar grupos
- Aplicabilidad: Conteo mejor performance; sorting más simple y legible

### Errores comunes en entrevistas
1. ❌ Intentar comparar strings directamente sin normalizar (no detecta anagramas)
2. ❌ Olvidar que la clave del diccionario debe ser hashable (usar lista en vez de tupla)
3. ❌ No considerar la complejidad del sorting al analizar el tiempo total

## Intermedio 2: Longest Substring Without Repeating Characters
Patrón: ventana deslizante (sliding window) + mapa de última posición.

Enunciado: longitud máxima de substring sin repetir caracteres.

Idea: ventana deslizante con mapa de última posición.

Paso a paso:
1. `left` marca inicio de la ventana.
2. Recorre con `right`.
3. Si el carácter ya se vio y está dentro de la ventana, mueve `left`.
4. Actualiza respuesta con el tamaño actual.

Por qué funciona: la ventana siempre mantiene caracteres únicos; cuando aparece un repetido, recortas por la izquierda lo mínimo necesario.

Complejidad: O(n) tiempo, O(min(n, alfabeto)) espacio.

Código:
```python
def length_of_longest_substring(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

### Casos de prueba
```python
assert length_of_longest_substring("abcabcbb") == 3  # "abc"
assert length_of_longest_substring("bbbbb") == 1     # "b"
assert length_of_longest_substring("pwwkew") == 3    # "wke"
assert length_of_longest_substring("") == 0
```

### Casos límite
- String vacío: `length_of_longest_substring("")` → `0`
- Un carácter: `length_of_longest_substring("a")` → `1`
- Todos únicos: `length_of_longest_substring("abcdef")` → `6`
- Todos iguales: `length_of_longest_substring("aaaa")` → `1`

### Preguntas de seguimiento (entrevista)
1. **"¿Cómo devolverías el substring en vez de solo su longitud?"**
   → Además de `best`, guarda `best_start` y `best_end`. Cuando actualizas `best`, también actualiza estas posiciones. Al final retorna `s[best_start:best_end+1]`.

2. **"¿Qué pasa si quieres permitir hasta k caracteres repetidos?"**
   → Usa ventana deslizante con contador de frecuencias. Expande right; si repeticiones > k, contrae left hasta que sea válido nuevamente.

3. **"¿Por qué necesitas verificar `last[ch] >= left`?"**
   → Porque el carácter puede haber aparecido antes, pero fuera de la ventana actual. Solo importa si su última posición está dentro de la ventana.

### Solución alternativa (usando set para caracteres)
```python
def length_of_longest_substring_set(s):
    chars = set()
    left = 0
    best = 0

    for right in range(len(s)):
        # Contrae ventana hasta que no haya duplicado
        while s[right] in chars:
            chars.remove(s[left])
            left += 1

        chars.add(s[right])
        best = max(best, right - left + 1)

    return best
```

**Trade-offs:**
- Tiempo: Diccionario O(n) vs Set O(n), pero set puede hacer más operaciones en el worst case
- Espacio: Ambas O(min(n, alfabeto))
- Aplicabilidad: Diccionario más eficiente (salto directo); set más intuitivo para principiantes

### Errores comunes en entrevistas
1. ❌ No verificar `last[ch] >= left` (considerar caracteres fuera de la ventana actual)
2. ❌ Intentar fuerza bruta O(n³) o O(n²) sin reconocer el patrón de ventana deslizante
3. ❌ Olvidar actualizar `last[ch]` incluso cuando el carácter causa un ajuste de ventana
