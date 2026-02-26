# Generadores e Iteradores en Python

Los generadores son una de las características más poderosas de Python para trabajar con secuencias de datos de manera eficiente. En esta guía aprenderás cómo funcionan, cuándo usarlos y las mejores prácticas.

## 1. Protocolo de Iterador

El protocolo de iterador es la base de cómo Python maneja la iteración sobre colecciones. Consiste en dos métodos especiales:

### Componentes del Protocolo

**`__iter__()`**: Devuelve el objeto iterador (usualmente `self`).

**`__next__()`**: Devuelve el siguiente elemento o lanza `StopIteration` cuando no hay más elementos.

### Ejemplo de Iterador Personalizado

```python
class ContadorRegresivo:
    """Iterador que cuenta hacia atrás desde un número inicial."""

    def __init__(self, inicio: int) -> None:
        self.actual = inicio

    def __iter__(self) -> 'ContadorRegresivo':
        """Retorna el objeto iterador (self)."""
        return self

    def __next__(self) -> int:
        """Retorna el siguiente valor o lanza StopIteration."""
        if self.actual <= 0:
            raise StopIteration

        self.actual -= 1
        return self.actual + 1


# Uso del iterador
contador = ContadorRegresivo(5)
for numero in contador:
    print(numero)  # 5, 4, 3, 2, 1
```

### Iterador con Estado Complejo

```python
class RangoPersonalizado:
    """Implementación personalizada similar a range()."""

    def __init__(self, inicio: int, fin: int, paso: int = 1) -> None:
        self.inicio = inicio
        self.fin = fin
        self.paso = paso
        self.actual = inicio

    def __iter__(self) -> 'RangoPersonalizado':
        self.actual = self.inicio  # Reinicia el estado
        return self

    def __next__(self) -> int:
        if self.paso > 0 and self.actual >= self.fin:
            raise StopIteration
        if self.paso < 0 and self.actual <= self.fin:
            raise StopIteration

        valor = self.actual
        self.actual += self.paso
        return valor


# Uso
for num in RangoPersonalizado(0, 10, 2):
    print(num)  # 0, 2, 4, 6, 8
```

### Ventajas y Desventajas de Iteradores

**Ventajas:**
- Control total sobre el proceso de iteración
- Pueden mantener estado complejo entre llamadas
- Útiles para estructuras de datos personalizadas

**Desventajas:**
- Más código (verboso)
- Necesitas gestionar el estado manualmente
- Más propenso a errores

## 2. Funciones Generadoras (yield vs return)

Las funciones generadoras simplifican la creación de iteradores usando la palabra clave `yield`.

### Diferencia Fundamental: yield vs return

```python
def funcion_normal() -> list[int]:
    """Función normal que usa return."""
    resultado = []
    for i in range(5):
        resultado.append(i * 2)
    return resultado  # Retorna toda la lista de una vez


def funcion_generadora() -> Generator[int, None, None]:
    """Función generadora que usa yield."""
    for i in range(5):
        yield i * 2  # Pausa y retorna un valor a la vez
```

### Características Clave de yield

1. **Pausa la ejecución**: La función se detiene en `yield` y guarda su estado
2. **Reanuda desde donde se detuvo**: Al llamar `next()`, continúa después del `yield`
3. **Es perezoso (lazy)**: Solo genera valores cuando se solicitan
4. **Memoria eficiente**: No crea toda la secuencia en memoria

### Ejemplo Detallado

```python
from typing import Generator


def contador_con_mensajes(limite: int) -> Generator[int, None, None]:
    """Generador que muestra su comportamiento paso a paso."""
    print("Iniciando generador...")

    for i in range(limite):
        print(f"A punto de producir: {i}")
        yield i
        print(f"Después de producir: {i}")

    print("Generador terminado")


# Observa el comportamiento
gen = contador_con_mensajes(3)
print("Generador creado, pero no ejecutado aún")

print("\nPrimera llamada a next():")
print(next(gen))

print("\nSegunda llamada a next():")
print(next(gen))

print("\nTercera llamada a next():")
print(next(gen))

# Salida:
# Generador creado, pero no ejecutado aún
#
# Primera llamada a next():
# Iniciando generador...
# A punto de producir: 0
# 0
# Después de producir: 0
#
# Segunda llamada a next():
# A punto de producir: 1
# 1
# Después de producir: 1
#
# Tercera llamada a next():
# A punto de producir: 2
# 2
# Después de producir: 2
```

### Generador con Lógica Condicional

```python
def numeros_pares(inicio: int, fin: int) -> Generator[int, None, None]:
    """Genera solo números pares en el rango dado."""
    for num in range(inicio, fin + 1):
        if num % 2 == 0:
            yield num


# Uso
for par in numeros_pares(1, 10):
    print(par)  # 2, 4, 6, 8, 10
```

## 3. Expresiones Generadoras

Las expresiones generadoras son la versión compacta de los generadores, similar a como las list comprehensions son para listas.

### Sintaxis Básica

```python
# List comprehension (crea lista completa en memoria)
cuadrados_lista = [x ** 2 for x in range(10)]

# Generator expression (genera valores bajo demanda)
cuadrados_gen = (x ** 2 for x in range(10))

print(type(cuadrados_lista))  # <class 'list'>
print(type(cuadrados_gen))    # <class 'generator'>
```

### Ventajas de las Expresiones Generadoras

```python
# Uso eficiente con funciones que aceptan iterables
suma_total = sum(x ** 2 for x in range(1000000))  # Memoria constante
max_valor = max(x * 2 for x in range(1000) if x % 3 == 0)

# Encadenamiento eficiente
numeros = (x for x in range(100))
pares = (x for x in numeros if x % 2 == 0)
cuadrados = (x ** 2 for x in pares)

print(list(cuadrados))  # Solo se evalúa cuando se necesita
```

### Comparación: Lista vs Generador

```python
import sys

# Lista: todo en memoria
lista_grande = [x for x in range(1000000)]
print(f"Memoria de lista: {sys.getsizeof(lista_grande):,} bytes")

# Generador: tamaño constante
gen_grande = (x for x in range(1000000))
print(f"Memoria de generador: {sys.getsizeof(gen_grande):,} bytes")

# Output aproximado:
# Memoria de lista: 8,000,056 bytes
# Memoria de generador: 112 bytes
```

### Casos de Uso Comunes

```python
# Filtrado eficiente
emails_validos = (email for email in emails if '@' in email and '.' in email)

# Transformación de datos
nombres_mayusculas = (nombre.upper() for nombre in nombres)

# Procesamiento de archivos grandes
lineas_no_vacias = (linea.strip() for linea in archivo if linea.strip())
```

## 4. Cuándo Usar Generadores

Los generadores son ideales en situaciones específicas. Aquí está cuándo usarlos y cuándo no.

### Casos Perfectos para Generadores

#### 4.1 Datasets Grandes

```python
def leer_archivo_grande(ruta: str) -> Generator[str, None, None]:
    """Lee archivos grandes línea por línea sin cargar todo en memoria."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            yield linea.strip()


# Procesamiento eficiente de archivo de 10GB
for linea in leer_archivo_grande('archivo_enorme.txt'):
    procesar_linea(linea)  # Solo una línea en memoria a la vez
```

#### 4.2 Streaming de Datos

```python
from typing import Generator
import time


def stream_sensor_data() -> Generator[dict, None, None]:
    """Simula streaming de datos de sensores."""
    while True:
        # Simula lectura de sensor
        temperatura = obtener_temperatura()
        humedad = obtener_humedad()

        yield {
            'temperatura': temperatura,
            'humedad': humedad,
            'timestamp': time.time()
        }

        time.sleep(1)  # Espera entre lecturas


# Procesamiento en tiempo real
for datos in stream_sensor_data():
    if datos['temperatura'] > 30:
        activar_ventilador()

    if debe_detenerse():
        break
```

#### 4.3 Secuencias Infinitas

```python
def fibonacci() -> Generator[int, None, None]:
    """Genera la secuencia de Fibonacci infinitamente."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Toma solo los primeros 10
primeros_10 = []
for i, fib in enumerate(fibonacci()):
    if i >= 10:
        break
    primeros_10.append(fib)

print(primeros_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

#### 4.4 Pipelines de Procesamiento

```python
def leer_logs(archivo: str) -> Generator[str, None, None]:
    """Lee líneas de log."""
    with open(archivo) as f:
        for linea in f:
            yield linea


def filtrar_errores(lineas: Generator[str, None, None]) -> Generator[str, None, None]:
    """Filtra solo líneas con ERROR."""
    for linea in lineas:
        if 'ERROR' in linea:
            yield linea


def extraer_mensaje(lineas: Generator[str, None, None]) -> Generator[str, None, None]:
    """Extrae el mensaje del log."""
    for linea in lineas:
        partes = linea.split(':', 2)
        if len(partes) >= 3:
            yield partes[2].strip()


# Pipeline eficiente
logs = leer_logs('app.log')
errores = filtrar_errores(logs)
mensajes = extraer_mensaje(errores)

for mensaje in mensajes:
    print(mensaje)
```

### Cuándo NO Usar Generadores

```python
#  MAL: Necesitas acceso aleatorio
def obtener_usuarios() -> Generator[dict, None, None]:
    for usuario in usuarios_db:
        yield usuario

gen = obtener_usuarios()
# No puedes hacer: gen[5]  # Error!

#  BIEN: Usa lista
def obtener_usuarios() -> list[dict]:
    return list(usuarios_db)

usuarios = obtener_usuarios()
print(usuarios[5])  # Funciona


#  MAL: Necesitas reutilizar los datos
gen = (x * 2 for x in range(10))
lista1 = list(gen)  # Funciona
lista2 = list(gen)  # ¡Vacío! El generador se agotó

#  BIEN: Usa lista si necesitas iterar múltiples veces
datos = [x * 2 for x in range(10)]
lista1 = list(datos)  # Funciona
lista2 = list(datos)  # Funciona


#  MAL: Dataset pequeño
gen = (x for x in range(10))  # Overhead innecesario

#  BIEN: Para datasets pequeños, las listas son más simples
numeros = [x for x in range(10)]
```

### Tabla de Decisión

| Situación | Usar Generador | Usar Lista |
|-----------|---------------|------------|
| Más de 10,000 elementos |  |  |
| Streaming/datos en tiempo real |  |  |
| Necesitas `len()` |  |  |
| Necesitas indexación `[i]` |  |  |
| Iterar múltiples veces |  |  |
| Pipeline de transformaciones |  |  |
| Secuencia infinita |  |  |
| Menos de 100 elementos |  |  |

## 5. yield from (Delegación)

`yield from` permite delegar la generación de valores a otro generador, simplificando el código.

### Sin yield from (Manual)

```python
def generador1() -> Generator[int, None, None]:
    yield 1
    yield 2
    yield 3


def generador2() -> Generator[int, None, None]:
    yield 4
    yield 5
    yield 6


def combinado_manual() -> Generator[int, None, None]:
    """Combina generadores manualmente."""
    for valor in generador1():
        yield valor

    for valor in generador2():
        yield valor


for num in combinado_manual():
    print(num)  # 1, 2, 3, 4, 5, 6
```

### Con yield from (Elegante)

```python
def combinado_con_yield_from() -> Generator[int, None, None]:
    """Combina generadores con yield from."""
    yield from generador1()
    yield from generador2()


for num in combinado_con_yield_from():
    print(num)  # 1, 2, 3, 4, 5, 6
```

### Caso de Uso: Aplanar Estructuras Anidadas

```python
from typing import Generator, Any


def aplanar(items: list[Any]) -> Generator[Any, None, None]:
    """Aplana una lista anidada de cualquier profundidad."""
    for item in items:
        if isinstance(item, list):
            yield from aplanar(item)  # Recursión con yield from
        else:
            yield item


# Uso
anidada = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
plana = list(aplanar(anidada))
print(plana)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Caso de Uso: Recorrer Árbol de Directorios

```python
from pathlib import Path
from typing import Generator


def recorrer_directorio(ruta: Path) -> Generator[Path, None, None]:
    """Recorre recursivamente todos los archivos en un directorio."""
    for item in ruta.iterdir():
        if item.is_file():
            yield item
        elif item.is_dir():
            yield from recorrer_directorio(item)  # Delegación recursiva


# Uso
directorio = Path('/ruta/proyecto')
for archivo in recorrer_directorio(directorio):
    if archivo.suffix == '.py':
        print(archivo)
```

### Caso de Uso: Cadena de Responsabilidad

```python
from typing import Generator


def procesar_nivel1(datos: list[str]) -> Generator[str, None, None]:
    """Primer nivel de procesamiento."""
    for dato in datos:
        if dato.startswith('A'):
            yield f"Nivel1: {dato}"


def procesar_nivel2(datos: list[str]) -> Generator[str, None, None]:
    """Segundo nivel de procesamiento."""
    for dato in datos:
        if dato.startswith('B'):
            yield f"Nivel2: {dato}"


def procesar_nivel3(datos: list[str]) -> Generator[str, None, None]:
    """Tercer nivel de procesamiento."""
    for dato in datos:
        if dato.startswith('C'):
            yield f"Nivel3: {dato}"


def pipeline_completo(datos: list[str]) -> Generator[str, None, None]:
    """Pipeline que delega a múltiples procesadores."""
    yield from procesar_nivel1(datos)
    yield from procesar_nivel2(datos)
    yield from procesar_nivel3(datos)


# Uso
datos = ['A1', 'B2', 'C3', 'A4', 'B5']
for resultado in pipeline_completo(datos):
    print(resultado)
# Nivel1: A1
# Nivel1: A4
# Nivel2: B2
# Nivel2: B5
# Nivel3: C3
```

### Diferencia Importante: yield from vs yield en bucle

```python
# Estos NO son equivalentes cuando se usan send() o throw()

def manual_yield(gen):
    """Yield manual en bucle."""
    for valor in gen:
        yield valor  # Pierde comunicación bidireccional


def con_yield_from(gen):
    """Yield from mantiene comunicación."""
    yield from gen  # Mantiene send(), throw(), close()


# yield from es más que sintaxis: mantiene toda la funcionalidad del generador
```

## 6. Generadores vs Listas - Comparación de Rendimiento

Vamos a analizar las diferencias de memoria y velocidad entre generadores y listas.

### 6.1 Comparación de Memoria

```python
import sys
from typing import Generator


def crear_lista(n: int) -> list[int]:
    """Crea una lista con n elementos."""
    return [x * 2 for x in range(n)]


def crear_generador(n: int) -> Generator[int, None, None]:
    """Crea un generador con n elementos."""
    return (x * 2 for x in range(n))


# Comparación de memoria
tamaños = [100, 1_000, 10_000, 100_000, 1_000_000]

print("Comparación de Memoria (bytes)")
print("-" * 60)
print(f"{'Tamaño':<15} {'Lista':<20} {'Generador':<20}")
print("-" * 60)

for n in tamaños:
    lista = crear_lista(n)
    gen = crear_generador(n)

    memoria_lista = sys.getsizeof(lista)
    memoria_gen = sys.getsizeof(gen)

    print(f"{n:<15,} {memoria_lista:<20,} {memoria_gen:<20,}")

# Salida típica:
# Comparación de Memoria (bytes)
# ------------------------------------------------------------
# Tamaño          Lista                Generador
# ------------------------------------------------------------
# 100             920                  112
# 1,000           8,856                112
# 10,000          87,616               112
# 100,000         824,464              112
# 1,000,000       8,448,728            112
```

### 6.2 Comparación de Velocidad

```python
import time
from typing import Generator


def medir_tiempo_lista(n: int) -> float:
    """Mide el tiempo de crear y sumar una lista."""
    inicio = time.perf_counter()

    lista = [x * 2 for x in range(n)]
    suma = sum(lista)

    fin = time.perf_counter()
    return fin - inicio


def medir_tiempo_generador(n: int) -> float:
    """Mide el tiempo de crear y sumar un generador."""
    inicio = time.perf_counter()

    gen = (x * 2 for x in range(n))
    suma = sum(gen)

    fin = time.perf_counter()
    return fin - inicio


# Benchmark
tamaños = [10_000, 100_000, 1_000_000, 10_000_000]

print("\nComparación de Velocidad (segundos)")
print("-" * 80)
print(f"{'Tamaño':<15} {'Lista':<20} {'Generador':<20} {'Diferencia':<20}")
print("-" * 80)

for n in tamaños:
    tiempo_lista = medir_tiempo_lista(n)
    tiempo_gen = medir_tiempo_generador(n)
    diferencia = ((tiempo_lista - tiempo_gen) / tiempo_lista) * 100

    print(f"{n:<15,} {tiempo_lista:<20.6f} {tiempo_gen:<20.6f} {diferencia:>6.2f}% más rápido")
```

### 6.3 Caso Real: Procesamiento de Logs

```python
import time
from typing import Generator


def procesar_con_lista(n: int) -> int:
    """Procesa logs usando listas."""
    inicio = time.perf_counter()

    # Simula leer logs
    logs = [f"Log línea {i}: INFO mensaje" for i in range(n)]

    # Filtra solo warnings y errors
    filtrados = [log for log in logs if 'WARNING' in log or 'ERROR' in log]

    # Procesa
    procesados = [log.upper() for log in filtrados]

    resultado = len(procesados)

    fin = time.perf_counter()
    print(f"Lista: {fin - inicio:.4f}s")
    return resultado


def procesar_con_generador(n: int) -> int:
    """Procesa logs usando generadores."""
    inicio = time.perf_counter()

    # Simula leer logs
    logs = (f"Log línea {i}: INFO mensaje" for i in range(n))

    # Filtra solo warnings y errors
    filtrados = (log for log in logs if 'WARNING' in log or 'ERROR' in log)

    # Procesa
    procesados = (log.upper() for log in filtrados)

    resultado = sum(1 for _ in procesados)

    fin = time.perf_counter()
    print(f"Generador: {fin - inicio:.4f}s")
    return resultado


# Benchmark
print("\nProcesamiento de 1,000,000 de líneas de log:")
procesar_con_lista(1_000_000)
procesar_con_generador(1_000_000)
```

### 6.4 Análisis de Resultados

```python
"""
CONCLUSIONES CLAVE:

1. MEMORIA:
   - Las listas ocupan memoria proporcional a su tamaño
   - Los generadores tienen tamaño constante (~112 bytes)
   - Para 1M elementos: Lista ≈ 8MB, Generador ≈ 112 bytes (75,000x menos)

2. VELOCIDAD:
   - Para operaciones simples (sum, max, min): Similar o generadores más rápidos
   - Generadores evitan crear estructuras intermedias
   - Listas son más rápidas si necesitas acceso múltiple

3. CUANDO USAR CADA UNO:

   Usa GENERADORES cuando:
   - Trabajas con datasets grandes (>10,000 elementos)
   - Procesas streams de datos
   - Haces pipelines de transformación
   - Solo iteras una vez
   - La memoria es limitada

   Usa LISTAS cuando:
   - Dataset pequeño (<1,000 elementos)
   - Necesitas acceso aleatorio
   - Necesitas len()
   - Iteras múltiples veces
   - Necesitas slice [1:10]

4. REGLA DE ORO:
   "Si solo iteras una vez sobre datos grandes, usa generador.
    Si necesitas acceso aleatorio o múltiples iteraciones, usa lista."
"""
```

### 6.5 Ejemplo Práctico: CSV Grande

```python
from typing import Generator
import sys


def leer_csv_lista(archivo: str) -> list[dict]:
    """Lee CSV completo en memoria."""
    with open(archivo) as f:
        lineas = f.readlines()
        return [procesar_linea(linea) for linea in lineas]


def leer_csv_generador(archivo: str) -> Generator[dict, None, None]:
    """Lee CSV línea por línea."""
    with open(archivo) as f:
        for linea in f:
            yield procesar_linea(linea)


# Para un CSV de 1GB:
# Lista: 1GB+ en memoria, lento al inicio
# Generador: ~112 bytes, comienza inmediatamente

# Uso del generador
for fila in leer_csv_generador('datos_grandes.csv'):
    procesar_fila(fila)
    # Solo una fila en memoria a la vez
```

## 7. Patrones Prácticos

Veamos patrones comunes y útiles para usar generadores en el día a día.

### 7.1 Lectura de Archivos

#### Patrón Básico: Leer Líneas

```python
from typing import Generator


def leer_archivo(ruta: str) -> Generator[str, None, None]:
    """Lee un archivo línea por línea."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            yield linea.strip()


# Uso
for linea in leer_archivo('datos.txt'):
    print(linea)
```

#### Patrón: Leer en Chunks

```python
def leer_archivo_chunks(ruta: str, tamaño_chunk: int = 1024) -> Generator[str, None, None]:
    """Lee archivo en chunks de tamaño específico."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        while True:
            chunk = archivo.read(tamaño_chunk)
            if not chunk:
                break
            yield chunk


# Útil para archivos binarios o muy grandes
for chunk in leer_archivo_chunks('archivo_grande.bin', 8192):
    procesar_chunk(chunk)
```

#### Patrón: Filtrar mientras Lees

```python
def leer_lineas_no_vacias(ruta: str) -> Generator[str, None, None]:
    """Lee solo líneas no vacías."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                yield linea


def leer_sin_comentarios(ruta: str, comentario: str = '#') -> Generator[str, None, None]:
    """Lee archivo ignorando comentarios."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea and not linea.startswith(comentario):
                yield linea


# Uso en archivo de configuración
for linea in leer_sin_comentarios('config.ini'):
    clave, valor = linea.split('=')
    configurar(clave.strip(), valor.strip())
```

#### Patrón: Procesamiento de CSV

```python
import csv
from typing import Generator


def leer_csv_generador(ruta: str) -> Generator[dict, None, None]:
    """Lee CSV como diccionarios."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            yield fila


def leer_csv_filtrado(
    ruta: str,
    condicion: callable
) -> Generator[dict, None, None]:
    """Lee CSV con filtro personalizado."""
    for fila in leer_csv_generador(ruta):
        if condicion(fila):
            yield fila


# Uso: leer solo usuarios activos
usuarios_activos = leer_csv_filtrado(
    'usuarios.csv',
    lambda fila: fila['estado'] == 'activo'
)

for usuario in usuarios_activos:
    print(usuario['nombre'])
```

### 7.2 Pipelines de Datos

Los generadores son perfectos para crear pipelines de transformación.

#### Pipeline Básico

```python
from typing import Generator


def leer_numeros(ruta: str) -> Generator[int, None, None]:
    """Paso 1: Lee números de archivo."""
    with open(ruta) as f:
        for linea in f:
            yield int(linea.strip())


def filtrar_pares(numeros: Generator[int, None, None]) -> Generator[int, None, None]:
    """Paso 2: Filtra solo pares."""
    for num in numeros:
        if num % 2 == 0:
            yield num


def elevar_cuadrado(numeros: Generator[int, None, None]) -> Generator[int, None, None]:
    """Paso 3: Eleva al cuadrado."""
    for num in numeros:
        yield num ** 2


def limitar(numeros: Generator[int, None, None], limite: int) -> Generator[int, None, None]:
    """Paso 4: Limita cantidad de resultados."""
    for i, num in enumerate(numeros):
        if i >= limite:
            break
        yield num


# Pipeline completo
numeros = leer_numeros('numeros.txt')
pares = filtrar_pares(numeros)
cuadrados = elevar_cuadrado(pares)
limitados = limitar(cuadrados, 10)

for resultado in limitados:
    print(resultado)
```

#### Pipeline con Procesamiento de Texto

```python
def leer_documento(ruta: str) -> Generator[str, None, None]:
    """Lee documento línea por línea."""
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            yield linea


def limpiar_lineas(lineas: Generator[str, None, None]) -> Generator[str, None, None]:
    """Limpia espacios y líneas vacías."""
    for linea in lineas:
        linea = linea.strip()
        if linea:
            yield linea


def dividir_palabras(lineas: Generator[str, None, None]) -> Generator[str, None, None]:
    """Divide líneas en palabras."""
    for linea in lineas:
        for palabra in linea.split():
            yield palabra


def normalizar(palabras: Generator[str, None, None]) -> Generator[str, None, None]:
    """Normaliza a minúsculas y sin puntuación."""
    import string
    for palabra in palabras:
        palabra = palabra.lower().strip(string.punctuation)
        if palabra:
            yield palabra


def filtrar_palabras_cortas(
    palabras: Generator[str, None, None],
    min_longitud: int = 3
) -> Generator[str, None, None]:
    """Filtra palabras muy cortas."""
    for palabra in palabras:
        if len(palabra) >= min_longitud:
            yield palabra


# Pipeline de procesamiento de texto
lineas = leer_documento('libro.txt')
limpias = limpiar_lineas(lineas)
palabras = dividir_palabras(limpias)
normalizadas = normalizar(palabras)
filtradas = filtrar_palabras_cortas(normalizadas, 4)

# Contar palabras únicas
from collections import Counter
conteo = Counter(filtradas)
print(conteo.most_common(10))
```

#### Pipeline de ETL (Extract, Transform, Load)

```python
from typing import Generator, Dict, Any
import json


def extraer_logs(ruta: str) -> Generator[str, None, None]:
    """E: Extrae líneas del log."""
    with open(ruta) as f:
        for linea in f:
            yield linea


def parsear_json(lineas: Generator[str, None, None]) -> Generator[Dict, None, None]:
    """T: Transforma JSON strings a dicts."""
    for linea in lineas:
        try:
            yield json.loads(linea)
        except json.JSONDecodeError:
            continue  # Salta líneas mal formadas


def filtrar_errores(logs: Generator[Dict, None, None]) -> Generator[Dict, None, None]:
    """T: Filtra solo logs de error."""
    for log in logs:
        if log.get('level') == 'ERROR':
            yield log


def agregar_metadata(logs: Generator[Dict, None, None]) -> Generator[Dict, None, None]:
    """T: Agrega metadata útil."""
    for log in logs:
        log['procesado'] = True
        log['prioridad'] = calcular_prioridad(log)
        yield log


def guardar_en_db(logs: Generator[Dict, None, None]) -> None:
    """L: Carga logs en base de datos."""
    for log in logs:
        db.insertar(log)


# Pipeline ETL completo
logs = extraer_logs('app.log')
parseados = parsear_json(logs)
errores = filtrar_errores(parseados)
con_metadata = agregar_metadata(errores)
guardar_en_db(con_metadata)  # Eficiente: un item a la vez
```

### 7.3 Patrones Avanzados

#### Patrón: Batching (Agrupar en Lotes)

```python
from typing import Generator, TypeVar, Iterable

T = TypeVar('T')


def batch(iterable: Iterable[T], tamaño: int) -> Generator[list[T], None, None]:
    """Agrupa elementos en lotes de tamaño específico."""
    lote = []
    for item in iterable:
        lote.append(item)
        if len(lote) >= tamaño:
            yield lote
            lote = []

    # Yield último lote si no está vacío
    if lote:
        yield lote


# Uso: procesar 1000 items a la vez
for lote in batch(range(10000), 1000):
    procesar_lote(lote)  # Procesa 1000 items juntos
    guardar_en_db(lote)  # Insert batch más eficiente que individual
```

#### Patrón: Ventana Deslizante

```python
from typing import Generator, TypeVar, Iterable
from collections import deque

T = TypeVar('T')


def ventana_deslizante(
    iterable: Iterable[T],
    tamaño: int
) -> Generator[tuple[T, ...], None, None]:
    """Genera ventanas deslizantes de tamaño n."""
    ventana = deque(maxlen=tamaño)

    for item in iterable:
        ventana.append(item)
        if len(ventana) == tamaño:
            yield tuple(ventana)


# Uso: calcular promedios móviles
precios = [100, 102, 101, 103, 105, 104, 106]
for ventana in ventana_deslizante(precios, 3):
    promedio = sum(ventana) / len(ventana)
    print(f"Ventana: {ventana}, Promedio: {promedio:.2f}")

# Output:
# Ventana: (100, 102, 101), Promedio: 101.00
# Ventana: (102, 101, 103), Promedio: 102.00
# Ventana: (101, 103, 105), Promedio: 103.00
# Ventana: (103, 105, 104), Promedio: 104.00
# Ventana: (105, 104, 106), Promedio: 105.00
```

#### Patrón: Take While / Drop While

```python
from typing import Generator, TypeVar, Iterable, Callable

T = TypeVar('T')


def take_while(
    iterable: Iterable[T],
    predicado: Callable[[T], bool]
) -> Generator[T, None, None]:
    """Toma elementos mientras la condición sea verdadera."""
    for item in iterable:
        if not predicado(item):
            break
        yield item


def drop_while(
    iterable: Iterable[T],
    predicado: Callable[[T], bool]
) -> Generator[T, None, None]:
    """Descarta elementos mientras la condición sea verdadera."""
    iterador = iter(iterable)

    # Descarta mientras sea True
    for item in iterador:
        if not predicado(item):
            yield item
            break

    # Yield el resto
    yield from iterador


# Uso
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Toma mientras sea menor que 5
pequeños = list(take_while(numeros, lambda x: x < 5))
print(pequeños)  # [1, 2, 3, 4]

# Descarta mientras sea menor que 5
grandes = list(drop_while(numeros, lambda x: x < 5))
print(grandes)  # [5, 6, 7, 8, 9, 10]
```

#### Patrón: Merge de Streams Ordenados

```python
import heapq
from typing import Generator, Iterable


def merge_ordenado(*iterables: Iterable[int]) -> Generator[int, None, None]:
    """Merge múltiples iterables ordenados en uno solo ordenado."""
    yield from heapq.merge(*iterables)


# Uso: combinar múltiples archivos ordenados
archivo1 = [1, 3, 5, 7, 9]
archivo2 = [2, 4, 6, 8, 10]
archivo3 = [1, 2, 3, 11, 12]

for numero in merge_ordenado(archivo1, archivo2, archivo3):
    print(numero)  # 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
```

#### Patrón: Caché de Generador

```python
from typing import Generator, TypeVar, Iterable

T = TypeVar('T')


class GeneradorCacheado:
    """Cachea resultados de un generador para reutilización."""

    def __init__(self, generador: Iterable[T]) -> None:
        self.generador = iter(generador)
        self.cache: list[T] = []
        self.agotado = False

    def __iter__(self) -> Generator[T, None, None]:
        # Primero yield del cache
        yield from self.cache

        # Luego del generador, guardando en cache
        if not self.agotado:
            for item in self.generador:
                self.cache.append(item)
                yield item
            self.agotado = True


# Uso: iterar múltiples veces sobre un generador
gen = (x * 2 for x in range(5))
cacheado = GeneradorCacheado(gen)

print("Primera iteración:")
for x in cacheado:
    print(x)  # 0, 2, 4, 6, 8

print("\nSegunda iteración (desde cache):")
for x in cacheado:
    print(x)  # 0, 2, 4, 6, 8 (sin recalcular)
```

### 7.4 Mejores Prácticas

```python
"""
MEJORES PRÁCTICAS CON GENERADORES:

1. USA TYPE HINTS
    def numeros() -> Generator[int, None, None]:
    def numeros():

2. DOCUMENTA QUÉ GENERA
    '''Genera números pares del 0 al n.'''
    sin documentación

3. CIERRA RECURSOS CORRECTAMENTE
    with open(archivo) as f:
        for linea in f:
            yield linea
    f = open(archivo)
      for linea in f:
          yield linea

4. NO GENERES LISTAS COMPLETAS
    yield item
    yield lista_completa

5. USA GENERADORES PARA PIPELINES
    leer() -> filtrar() -> transformar() -> guardar()
    lista1 = leer(); lista2 = filtrar(lista1); ...

6. PREFIERE EXPRESIONES PARA CASOS SIMPLES
    (x * 2 for x in range(10))
    def gen():
         for x in range(10):
             yield x * 2

7. USA yield from PARA DELEGAR
    yield from otro_generador()
    for x in otro_generador(): yield x

8. MANEJA EXCEPCIONES APROPIADAMENTE
    try:
         yield procesar(item)
      except Error:
         log_error()
         continue
"""
```

## Resumen y Conclusiones

### Cuándo Usar Cada Herramienta

```python
# ITERADORES PERSONALIZADOS (clase con __iter__ y __next__)
# Usa cuando necesitas:
# - Estado complejo entre iteraciones
# - Lógica personalizada de iteración
# - Integración con protocolos de Python

# GENERADORES (función con yield)
# Usa cuando necesitas:
# - Secuencias grandes o infinitas
# - Pipelines de transformación
# - Lectura eficiente de archivos
# - Streaming de datos

# EXPRESIONES GENERADORAS ((x for x in iterable))
# Usa cuando necesitas:
# - Transformaciones simples
# - Filtrado rápido
# - Alternativa eficiente a list comprehension
# - Pasar a sum(), max(), min(), any(), all()

# LISTAS ([x for x in iterable])
# Usa cuando necesitas:
# - Acceso aleatorio
# - Múltiples iteraciones
# - len(), sorted(), reversed()
# - Datasets pequeños (<1000 elementos)
```

### Reglas de Oro

1. **Regla de Memoria**: Si el dataset cabe cómodamente en RAM y necesitas acceso aleatorio, usa lista. Si no, usa generador.

2. **Regla de Iteración**: Si solo iteras una vez, usa generador. Si iteras muchas veces, usa lista.

3. **Regla de Tamaño**: Más de 10,000 elementos → generador. Menos de 1,000 → lista puede ser más simple.

4. **Regla de Pipeline**: Múltiples transformaciones → cadena de generadores.

5. **Regla de Simplicidad**: Si la expresión generadora es más simple y clara, úsala. Si necesitas lógica compleja, usa función generadora.

### Checklist de Decisión

```python
"""
¿Qué usar? Responde estas preguntas:

1. ¿Cuántos elementos?
   < 1,000: Lista
   > 10,000: Generador
   Infinito: Generador

2. ¿Cuántas veces iteras?
   Una vez: Generador
   Múltiples: Lista

3. ¿Necesitas len() o indexación [i]?
   Sí: Lista
   No: Generador

4. ¿Es un pipeline de transformaciones?
   Sí: Generadores encadenados
   No: Evalúa otras preguntas

5. ¿Memoria limitada?
   Sí: Generador
   No: Puedes usar lista

6. ¿Es streaming en tiempo real?
   Sí: Generador
   No: Evalúa otras preguntas

7. ¿Lógica simple (filtro/map)?
   Sí: Expresión generadora
   No: Función generadora
"""
```

### Recursos Adicionales

Para profundizar más:

- **PEP 255**: Simple Generators
- **PEP 342**: Coroutines via Enhanced Generators
- **PEP 380**: Syntax for Delegating to a Subgenerator (yield from)
- **itertools**: Módulo estándar con herramientas para iteradores
- **more-itertools**: Biblioteca con recetas adicionales

### Ejemplo Final: Todo Junto

```python
from typing import Generator
import sys


def pipeline_completo(archivo: str) -> Generator[dict, None, None]:
    """
    Pipeline completo que demuestra todos los conceptos:
    - Lectura eficiente de archivo
    - Transformación con yield
    - Filtrado
    - yield from para delegación
    """

    def leer_lineas() -> Generator[str, None, None]:
        """Lee archivo línea por línea."""
        with open(archivo) as f:
            for linea in f:
                yield linea.strip()

    def parsear_datos(lineas: Generator[str, None, None]) -> Generator[dict, None, None]:
        """Parsea líneas a diccionarios."""
        for linea in lineas:
            if ',' in linea:
                partes = linea.split(',')
                yield {
                    'id': partes[0],
                    'nombre': partes[1],
                    'valor': int(partes[2])
                }

    def filtrar_validos(items: Generator[dict, None, None]) -> Generator[dict, None, None]:
        """Filtra items válidos."""
        for item in items:
            if item['valor'] > 0:
                yield item

    # Pipeline usando yield from
    lineas = leer_lineas()
    datos = parsear_datos(lineas)
    validos = filtrar_validos(datos)

    yield from validos


# Uso: procesa archivo gigante eficientemente
for item in pipeline_completo('datos_grandes.csv'):
    procesar(item)  # Solo un item en memoria a la vez

print(f"Memoria usada: ~112 bytes (constante)")
```

¡Ahora tienes un conocimiento completo de generadores e iteradores en Python! Úsalos sabiamente para escribir código más eficiente y elegante.
