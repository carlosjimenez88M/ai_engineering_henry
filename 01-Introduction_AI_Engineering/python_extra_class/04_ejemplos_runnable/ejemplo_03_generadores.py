"""
Ejemplos Prácticos de Generadores e Iteradores

Este módulo contiene ejemplos ejecutables que demuestran:
1. Iteradores personalizados
2. Funciones generadoras
3. Generador de lectura de archivos
4. Pipeline de transformación de datos
5. Secuencia de Fibonacci
6. Comparación de memoria (sys.getsizeof)
7. Benchmarks de rendimiento

Autor: Henry AI Engineering Course
Fecha: 2026
"""

import sys
import time
import tempfile
import csv
from pathlib import Path
from typing import Generator, Iterator, TypeVar, Iterable, Callable
from collections import deque
from dataclasses import dataclass


# ============================================================================
# 1. ITERADORES PERSONALIZADOS
# ============================================================================

class ContadorRegresivo:
    """Iterador que cuenta hacia atrás desde un número inicial."""

    def __init__(self, inicio: int) -> None:
        """
        Inicializa el contador.

        Args:
            inicio: Número desde donde empezar a contar hacia atrás
        """
        self.inicio = inicio
        self.actual = inicio

    def __iter__(self) -> Iterator[int]:
        """Retorna el objeto iterador."""
        self.actual = self.inicio  # Reinicia el estado
        return self

    def __next__(self) -> int:
        """Retorna el siguiente valor o lanza StopIteration."""
        if self.actual <= 0:
            raise StopIteration

        valor = self.actual
        self.actual -= 1
        return valor


class RangoPersonalizado:
    """Implementación personalizada similar a range()."""

    def __init__(self, inicio: int, fin: int, paso: int = 1) -> None:
        """
        Crea un rango personalizado.

        Args:
            inicio: Valor inicial
            fin: Valor final (no inclusive)
            paso: Incremento entre valores
        """
        self.inicio = inicio
        self.fin = fin
        self.paso = paso

    def __iter__(self) -> Iterator[int]:
        """Retorna un nuevo iterador."""
        actual = self.inicio
        while (self.paso > 0 and actual < self.fin) or \
              (self.paso < 0 and actual > self.fin):
            yield actual
            actual += self.paso


def ejemplos_iteradores() -> None:
    """Demuestra el uso de iteradores personalizados."""
    print("=" * 70)
    print("ITERADORES PERSONALIZADOS")
    print("=" * 70)

    print("\n1. ContadorRegresivo:")
    contador = ContadorRegresivo(5)
    for num in contador:
        print(f"  {num}", end=" ")
    print()

    print("\n2. RangoPersonalizado (0 a 10, paso 2):")
    for num in RangoPersonalizado(0, 10, 2):
        print(f"  {num}", end=" ")
    print()

    print("\n3. RangoPersonalizado regresivo (10 a 0, paso -2):")
    for num in RangoPersonalizado(10, 0, -2):
        print(f"  {num}", end=" ")
    print("\n")


# ============================================================================
# 2. FUNCIONES GENERADORAS
# ============================================================================

def numeros_pares(inicio: int, fin: int) -> Generator[int, None, None]:
    """
    Genera números pares en un rango.

    Args:
        inicio: Número inicial
        fin: Número final (inclusive)

    Yields:
        Números pares en el rango
    """
    for num in range(inicio, fin + 1):
        if num % 2 == 0:
            yield num


def contador_con_estado(limite: int) -> Generator[dict[str, int], None, None]:
    """
    Generador que mantiene estado y produce diccionarios.

    Args:
        limite: Cantidad de valores a generar

    Yields:
        Diccionario con contador y cuadrado
    """
    for i in range(limite):
        yield {
            'contador': i,
            'cuadrado': i ** 2,
            'cubo': i ** 3
        }


def ejemplos_generadores_basicos() -> None:
    """Demuestra funciones generadoras básicas."""
    print("=" * 70)
    print("FUNCIONES GENERADORAS BÁSICAS")
    print("=" * 70)

    print("\n1. Números pares (1 a 20):")
    pares = numeros_pares(1, 20)
    print(f"  {list(pares)}")

    print("\n2. Generador con estado:")
    for item in contador_con_estado(5):
        print(f"  {item}")
    print()


# ============================================================================
# 3. GENERADOR DE LECTURA DE ARCHIVOS
# ============================================================================

def leer_archivo_lineas(ruta: Path) -> Generator[str, None, None]:
    """
    Lee un archivo línea por línea de manera eficiente.

    Args:
        ruta: Path al archivo

    Yields:
        Cada línea del archivo (sin espacios al inicio/fin)
    """
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:  # Solo líneas no vacías
                yield linea


def leer_archivo_chunks(ruta: Path, tamaño_chunk: int = 1024) -> Generator[str, None, None]:
    """
    Lee un archivo en chunks de tamaño específico.

    Args:
        ruta: Path al archivo
        tamaño_chunk: Tamaño de cada chunk en bytes

    Yields:
        Chunks del archivo
    """
    with open(ruta, 'r', encoding='utf-8') as archivo:
        while True:
            chunk = archivo.read(tamaño_chunk)
            if not chunk:
                break
            yield chunk


def leer_csv_generador(ruta: Path) -> Generator[dict[str, str], None, None]:
    """
    Lee un archivo CSV como generador de diccionarios.

    Args:
        ruta: Path al archivo CSV

    Yields:
        Cada fila como diccionario
    """
    with open(ruta, 'r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            yield fila


def ejemplos_lectura_archivos() -> None:
    """Demuestra lectura de archivos con generadores."""
    print("=" * 70)
    print("LECTURA DE ARCHIVOS CON GENERADORES")
    print("=" * 70)

    # Crear archivo temporal de texto
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_txt = Path(f.name)
        f.write("Primera línea\n")
        f.write("Segunda línea\n")
        f.write("\n")  # Línea vacía
        f.write("Tercera línea\n")
        f.write("Cuarta línea\n")

    # Crear archivo temporal CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        temp_csv = Path(f.name)
        writer = csv.DictWriter(f, fieldnames=['nombre', 'edad', 'ciudad'])
        writer.writeheader()
        writer.writerow({'nombre': 'Ana', 'edad': '25', 'ciudad': 'Madrid'})
        writer.writerow({'nombre': 'Luis', 'edad': '30', 'ciudad': 'Barcelona'})
        writer.writerow({'nombre': 'María', 'edad': '28', 'ciudad': 'Valencia'})

    try:
        print("\n1. Leer archivo línea por línea:")
        for i, linea in enumerate(leer_archivo_lineas(temp_txt), 1):
            print(f"  Línea {i}: {linea}")

        print("\n2. Leer archivo en chunks:")
        for i, chunk in enumerate(leer_archivo_chunks(temp_txt, 20), 1):
            print(f"  Chunk {i}: {repr(chunk[:50])}")

        print("\n3. Leer CSV como diccionarios:")
        for persona in leer_csv_generador(temp_csv):
            print(f"  {persona['nombre']}: {persona['edad']} años, {persona['ciudad']}")
        print()

    finally:
        # Limpieza
        temp_txt.unlink()
        temp_csv.unlink()


# ============================================================================
# 4. PIPELINE DE TRANSFORMACIÓN DE DATOS
# ============================================================================

T = TypeVar('T')


def filtrar(
    iterable: Iterable[T],
    predicado: Callable[[T], bool]
) -> Generator[T, None, None]:
    """
    Filtra elementos según un predicado.

    Args:
        iterable: Secuencia de entrada
        predicado: Función que retorna True para elementos a mantener

    Yields:
        Elementos que cumplen el predicado
    """
    for item in iterable:
        if predicado(item):
            yield item


def mapear(
    iterable: Iterable[T],
    funcion: Callable[[T], T]
) -> Generator[T, None, None]:
    """
    Transforma cada elemento usando una función.

    Args:
        iterable: Secuencia de entrada
        funcion: Función de transformación

    Yields:
        Elementos transformados
    """
    for item in iterable:
        yield funcion(item)


def take(iterable: Iterable[T], n: int) -> Generator[T, None, None]:
    """
    Toma los primeros n elementos.

    Args:
        iterable: Secuencia de entrada
        n: Cantidad de elementos a tomar

    Yields:
        Los primeros n elementos
    """
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item


def batch(iterable: Iterable[T], tamaño: int) -> Generator[list[T], None, None]:
    """
    Agrupa elementos en lotes de tamaño específico.

    Args:
        iterable: Secuencia de entrada
        tamaño: Tamaño de cada lote

    Yields:
        Lotes de elementos
    """
    lote = []
    for item in iterable:
        lote.append(item)
        if len(lote) >= tamaño:
            yield lote
            lote = []

    if lote:  # Último lote parcial
        yield lote


def ventana_deslizante(
    iterable: Iterable[T],
    tamaño: int
) -> Generator[tuple[T, ...], None, None]:
    """
    Genera ventanas deslizantes de tamaño n.

    Args:
        iterable: Secuencia de entrada
        tamaño: Tamaño de la ventana

    Yields:
        Tuplas con ventanas deslizantes
    """
    ventana = deque(maxlen=tamaño)
    for item in iterable:
        ventana.append(item)
        if len(ventana) == tamaño:
            yield tuple(ventana)


@dataclass
class Transaccion:
    """Representa una transacción financiera."""
    id: int
    monto: float
    tipo: str
    valida: bool


def ejemplos_pipelines() -> None:
    """Demuestra pipelines de transformación de datos."""
    print("=" * 70)
    print("PIPELINES DE TRANSFORMACIÓN")
    print("=" * 70)

    # Pipeline 1: Números
    print("\n1. Pipeline de números:")
    numeros = range(1, 21)
    pares = filtrar(numeros, lambda x: x % 2 == 0)
    cuadrados = mapear(pares, lambda x: x ** 2)
    primeros_5 = take(cuadrados, 5)
    resultado = list(primeros_5)
    print(f"  Primeros 5 cuadrados de pares: {resultado}")

    # Pipeline 2: Strings
    print("\n2. Pipeline de strings:")
    palabras = ["hola", "mundo", "python", "generador", "x", "y"]
    largas = filtrar(palabras, lambda p: len(p) > 3)
    mayusculas = mapear(largas, lambda p: p.upper())
    resultado = list(mayusculas)
    print(f"  Palabras largas en mayúsculas: {resultado}")

    # Pipeline 3: Batching
    print("\n3. Agrupación en lotes:")
    numeros = range(1, 11)
    lotes = batch(numeros, 3)
    for i, lote in enumerate(lotes, 1):
        print(f"  Lote {i}: {lote}")

    # Pipeline 4: Ventana deslizante
    print("\n4. Ventanas deslizantes (promedios móviles):")
    precios = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109]
    for ventana in ventana_deslizante(precios, 3):
        promedio = sum(ventana) / len(ventana)
        print(f"  Ventana {ventana}: promedio = {promedio:.2f}")

    # Pipeline 5: Procesamiento complejo
    print("\n5. Pipeline complejo (transacciones):")
    transacciones = [
        Transaccion(1, 100.50, "compra", True),
        Transaccion(2, -50.00, "devolucion", True),
        Transaccion(3, 200.00, "compra", False),
        Transaccion(4, 150.75, "compra", True),
        Transaccion(5, -25.00, "devolucion", True),
        Transaccion(6, 300.00, "compra", True),
    ]

    # Pipeline: válidas -> compras -> mayores a 100
    validas = filtrar(transacciones, lambda t: t.valida)
    compras = filtrar(validas, lambda t: t.tipo == "compra")
    grandes = filtrar(compras, lambda t: t.monto > 100)

    total = sum(t.monto for t in grandes)
    print(f"  Total de compras válidas > $100: ${total:.2f}")
    print()


# ============================================================================
# 5. SECUENCIA DE FIBONACCI
# ============================================================================

def fibonacci_generador(limite: int | None = None) -> Generator[int, None, None]:
    """
    Genera la secuencia de Fibonacci.

    Args:
        limite: Cantidad máxima de números (None = infinito)

    Yields:
        Números de Fibonacci
    """
    a, b = 0, 1
    contador = 0

    while limite is None or contador < limite:
        yield a
        a, b = b, a + b
        contador += 1


def fibonacci_hasta(max_valor: int) -> Generator[int, None, None]:
    """
    Genera Fibonacci hasta un valor máximo.

    Args:
        max_valor: Valor máximo permitido

    Yields:
        Números de Fibonacci menores o iguales a max_valor
    """
    a, b = 0, 1
    while a <= max_valor:
        yield a
        a, b = b, a + b


def ejemplos_fibonacci() -> None:
    """Demuestra generadores de Fibonacci."""
    print("=" * 70)
    print("SECUENCIA DE FIBONACCI")
    print("=" * 70)

    print("\n1. Primeros 15 números de Fibonacci:")
    fib = list(fibonacci_generador(15))
    print(f"  {fib}")

    print("\n2. Fibonacci hasta 1000:")
    fib = list(fibonacci_hasta(1000))
    print(f"  {fib}")

    print("\n3. Suma de los primeros 10 números de Fibonacci:")
    suma = sum(fibonacci_generador(10))
    print(f"  Suma: {suma}")

    print("\n4. Generación bajo demanda (infinito):")
    print("  Primeros 20 números (de secuencia infinita):")
    gen = fibonacci_generador()  # Infinito
    primeros_20 = [next(gen) for _ in range(20)]
    print(f"  {primeros_20}")
    print()


# ============================================================================
# 6. COMPARACIÓN DE MEMORIA
# ============================================================================

def crear_lista(n: int) -> list[int]:
    """Crea una lista con n elementos."""
    return [x * 2 for x in range(n)]


def crear_generador(n: int) -> Generator[int, None, None]:
    """Crea un generador con n elementos."""
    return (x * 2 for x in range(n))


def comparacion_memoria() -> None:
    """Compara el uso de memoria entre listas y generadores."""
    print("=" * 70)
    print("COMPARACIÓN DE MEMORIA: LISTAS VS GENERADORES")
    print("=" * 70)

    tamaños = [100, 1_000, 10_000, 100_000, 1_000_000]

    print(f"\n{'Tamaño':<15} {'Lista (bytes)':<20} {'Generador (bytes)':<20} {'Ratio':<10}")
    print("-" * 70)

    for n in tamaños:
        lista = crear_lista(n)
        gen = crear_generador(n)

        memoria_lista = sys.getsizeof(lista)
        memoria_gen = sys.getsizeof(gen)
        ratio = memoria_lista / memoria_gen

        print(f"{n:<15,} {memoria_lista:<20,} {memoria_gen:<20,} {ratio:<10.1f}x")

    # Ejemplo adicional: contenido en memoria
    print("\n" + "=" * 70)
    print("Tamaño en memoria de diferentes estructuras:")
    print("=" * 70)

    ejemplos = [
        ("Lista vacía", []),
        ("Lista [1,2,3]", [1, 2, 3]),
        ("Lista 100 elementos", list(range(100))),
        ("Generador vacío", (x for x in [])),
        ("Generador range(100)", (x for x in range(100))),
        ("Generador range(1000000)", (x for x in range(1_000_000))),
        ("Tupla (1,2,3)", (1, 2, 3)),
        ("Set {1,2,3}", {1, 2, 3}),
        ("Dict {'a':1}", {'a': 1}),
    ]

    for nombre, estructura in ejemplos:
        tamaño = sys.getsizeof(estructura)
        print(f"  {nombre:<30} {tamaño:>10,} bytes")
    print()


# ============================================================================
# 7. BENCHMARKS DE RENDIMIENTO
# ============================================================================

def benchmark_suma_lista(n: int) -> tuple[float, int]:
    """Mide el rendimiento de suma con lista."""
    inicio = time.perf_counter()

    lista = [x * 2 for x in range(n)]
    resultado = sum(lista)

    fin = time.perf_counter()
    return fin - inicio, resultado


def benchmark_suma_generador(n: int) -> tuple[float, int]:
    """Mide el rendimiento de suma con generador."""
    inicio = time.perf_counter()

    gen = (x * 2 for x in range(n))
    resultado = sum(gen)

    fin = time.perf_counter()
    return fin - inicio, resultado


def benchmark_filtrado_lista(n: int) -> tuple[float, int]:
    """Mide el rendimiento de filtrado con lista."""
    inicio = time.perf_counter()

    numeros = [x for x in range(n)]
    pares = [x for x in numeros if x % 2 == 0]
    cuadrados = [x ** 2 for x in pares]
    resultado = sum(cuadrados)

    fin = time.perf_counter()
    return fin - inicio, resultado


def benchmark_filtrado_generador(n: int) -> tuple[float, int]:
    """Mide el rendimiento de filtrado con generador."""
    inicio = time.perf_counter()

    numeros = (x for x in range(n))
    pares = (x for x in numeros if x % 2 == 0)
    cuadrados = (x ** 2 for x in pares)
    resultado = sum(cuadrados)

    fin = time.perf_counter()
    return fin - inicio, resultado


def benchmarks_rendimiento() -> None:
    """Ejecuta benchmarks comparando listas y generadores."""
    print("=" * 70)
    print("BENCHMARKS DE RENDIMIENTO")
    print("=" * 70)

    tamaños = [10_000, 100_000, 1_000_000]

    # Benchmark 1: Suma simple
    print("\n1. Suma de elementos (x * 2 para x in range(n)):")
    print(f"{'Tamaño':<15} {'Lista (s)':<15} {'Generador (s)':<15} {'Más rápido':<15}")
    print("-" * 70)

    for n in tamaños:
        tiempo_lista, _ = benchmark_suma_lista(n)
        tiempo_gen, _ = benchmark_suma_generador(n)

        if tiempo_gen < tiempo_lista:
            ganador = f"Gen {((tiempo_lista/tiempo_gen - 1) * 100):.1f}%"
        else:
            ganador = f"List {((tiempo_gen/tiempo_lista - 1) * 100):.1f}%"

        print(f"{n:<15,} {tiempo_lista:<15.6f} {tiempo_gen:<15.6f} {ganador:<15}")

    # Benchmark 2: Filtrado y transformación
    print("\n2. Pipeline (filtrar pares -> cuadrados -> suma):")
    print(f"{'Tamaño':<15} {'Lista (s)':<15} {'Generador (s)':<15} {'Más rápido':<15}")
    print("-" * 70)

    for n in tamaños:
        tiempo_lista, _ = benchmark_filtrado_lista(n)
        tiempo_gen, _ = benchmark_filtrado_generador(n)

        if tiempo_gen < tiempo_lista:
            ganador = f"Gen {((tiempo_lista/tiempo_gen - 1) * 100):.1f}%"
        else:
            ganador = f"List {((tiempo_gen/tiempo_lista - 1) * 100):.1f}%"

        print(f"{n:<15,} {tiempo_lista:<15.6f} {tiempo_gen:<15.6f} {ganador:<15}")

    # Benchmark 3: Iteración múltiple
    print("\n3. Iteración múltiple (3 veces):")
    print("  Lista: Rápido (datos ya en memoria)")
    print("  Generador: Lento (debe regenerar cada vez)")
    print()

    n = 100_000

    # Lista: crear una vez, iterar 3 veces
    inicio = time.perf_counter()
    lista = [x * 2 for x in range(n)]
    for _ in range(3):
        sum(lista)
    tiempo_lista = time.perf_counter() - inicio

    # Generador: debe crear 3 veces
    inicio = time.perf_counter()
    for _ in range(3):
        gen = (x * 2 for x in range(n))
        sum(gen)
    tiempo_gen = time.perf_counter() - inicio

    print(f"  Lista (3 iteraciones): {tiempo_lista:.6f}s")
    print(f"  Generador (3 regeneraciones): {tiempo_gen:.6f}s")
    print(f"  Lista es {(tiempo_gen/tiempo_lista):.1f}x más rápida para múltiples iteraciones")
    print()


# ============================================================================
# 8. CASOS DE USO PRÁCTICOS
# ============================================================================

def procesar_log_file_eficiente(ruta: Path) -> dict[str, int]:
    """
    Procesa un archivo de log grande de manera eficiente.

    Args:
        ruta: Path al archivo de log

    Returns:
        Diccionario con conteo de niveles de log
    """
    conteo = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0}

    # Generador para leer líneas
    lineas = leer_archivo_lineas(ruta)

    # Generador para parsear y contar
    for linea in lineas:
        for nivel in conteo.keys():
            if nivel in linea:
                conteo[nivel] += 1
                break

    return conteo


def calcular_estadisticas_streaming(
    numeros: Generator[float, None, None]
) -> dict[str, float]:
    """
    Calcula estadísticas de un stream de números sin cargar todos en memoria.

    Args:
        numeros: Generador de números

    Returns:
        Diccionario con estadísticas
    """
    count = 0
    suma = 0.0
    suma_cuadrados = 0.0
    minimo = float('inf')
    maximo = float('-inf')

    for num in numeros:
        count += 1
        suma += num
        suma_cuadrados += num ** 2
        minimo = min(minimo, num)
        maximo = max(maximo, num)

    promedio = suma / count if count > 0 else 0
    varianza = (suma_cuadrados / count - promedio ** 2) if count > 0 else 0

    return {
        'count': count,
        'suma': suma,
        'promedio': promedio,
        'minimo': minimo,
        'maximo': maximo,
        'varianza': varianza,
    }


def ejemplos_casos_practicos() -> None:
    """Demuestra casos de uso prácticos."""
    print("=" * 70)
    print("CASOS DE USO PRÁCTICOS")
    print("=" * 70)

    # Caso 1: Procesar log file
    print("\n1. Procesamiento eficiente de log file:")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        temp_log = Path(f.name)
        for i in range(1000):
            nivel = ['INFO', 'WARNING', 'ERROR', 'DEBUG'][i % 4]
            f.write(f"2026-02-10 12:00:{i:02d} [{nivel}] Mensaje {i}\n")

    try:
        conteo = procesar_log_file_eficiente(temp_log)
        print(f"  Conteo de niveles:")
        for nivel, cantidad in conteo.items():
            print(f"    {nivel}: {cantidad}")
    finally:
        temp_log.unlink()

    # Caso 2: Estadísticas streaming
    print("\n2. Estadísticas en streaming (sin cargar todo en memoria):")
    # Generador de 1 millón de números
    numeros = (x * 0.5 for x in range(1_000_000))
    stats = calcular_estadisticas_streaming(numeros)
    print(f"  Procesados: {stats['count']:,} números")
    print(f"  Suma: {stats['suma']:,.2f}")
    print(f"  Promedio: {stats['promedio']:,.2f}")
    print(f"  Mínimo: {stats['minimo']:,.2f}")
    print(f"  Máximo: {stats['maximo']:,.2f}")
    print(f"  Varianza: {stats['varianza']:,.2f}")

    # Caso 3: Pipeline de procesamiento de datos
    print("\n3. Pipeline de procesamiento de datos:")
    # Simula datos de sensores
    def generar_lecturas_sensor(cantidad: int) -> Generator[dict, None, None]:
        """Genera lecturas simuladas de sensor."""
        import random
        for i in range(cantidad):
            yield {
                'id': i,
                'temperatura': 20 + random.uniform(-5, 15),
                'humedad': 50 + random.uniform(-20, 30),
            }

    # Pipeline
    lecturas = generar_lecturas_sensor(1000)
    altas_temp = filtrar(lecturas, lambda l: l['temperatura'] > 30)
    alertas = mapear(altas_temp, lambda l: f"ALERTA: Sensor {l['id']}: {l['temperatura']:.1f}°C")
    primeras_5 = take(alertas, 5)

    print("  Primeras 5 alertas de temperatura alta:")
    for alerta in primeras_5:
        print(f"    {alerta}")

    print()


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main() -> None:
    """Ejecuta todos los ejemplos."""
    print("\n" + "=" * 70)
    print("EJEMPLOS COMPLETOS: GENERADORES E ITERADORES")
    print("=" * 70)
    print()

    ejemplos_iteradores()
    ejemplos_generadores_basicos()
    ejemplos_lectura_archivos()
    ejemplos_pipelines()
    ejemplos_fibonacci()
    comparacion_memoria()
    benchmarks_rendimiento()
    ejemplos_casos_practicos()

    print("=" * 70)
    print("RESUMEN DE CONCLUSIONES")
    print("=" * 70)
    print("""
    1. MEMORIA:
       - Generadores usan memoria constante (~112 bytes)
       - Listas crecen linealmente con el tamaño
       - Para 1M elementos: Lista ~8MB vs Generador ~112 bytes

    2. RENDIMIENTO:
       - Generadores son más rápidos para pipelines
       - Listas son mejores para acceso múltiple
       - Generadores permiten procesamiento lazy

    3. CUANDO USAR:
       - Generadores: Datasets grandes, streaming, pipelines
       - Listas: Acceso aleatorio, múltiples iteraciones, datasets pequeños

    4. BEST PRACTICES:
       - Usa generadores para archivos grandes
       - Encadena generadores para pipelines eficientes
       - Usa list() solo cuando realmente necesitas la lista completa
       - Prefiere expresiones generadoras para transformaciones simples
    """)
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
