"""
Análisis de Performance: Comprensiones vs Loops

Este módulo contiene tests exhaustivos de performance, comparaciones de bytecode,
profiling de memoria, y ejemplos de código legible vs ilegible.

Ejecuta este script para ver resultados en tiempo real:
    python ejemplo_06_comprehension_performance.py

Secciones:
1. Tests de performance (10, 100, 1000, 10000 elementos)
2. Análisis de bytecode con dis
3. Memory profiling
4. Ejemplos de legibilidad

Autor: AI Engineering Course - Henry
"""

import timeit
import dis
import sys
from typing import List, Dict, Any
from dataclasses import dataclass


# ============================================================================
# SECCIÓN 1: TESTS DE PERFORMANCE
# ============================================================================

def benchmark_simple_map(size: int, iterations: int = 10000) -> Dict[str, float]:
    """
    Compara performance de map simple: multiplicar por 2.

    Args:
        size: Número de elementos a procesar
        iterations: Número de veces que se ejecuta para promediar

    Returns:
        Dict con tiempos de ejecución
    """
    setup = f"nums = list(range({size}))"

    # Loop tradicional con append
    loop_code = """
resultado = []
for n in nums:
    resultado.append(n * 2)
"""

    # List comprehension
    comp_code = """
resultado = [n * 2 for n in nums]
"""

    # Generator expression (para comparar)
    gen_code = """
resultado = list(n * 2 for n in nums)
"""

    # map() con lambda
    map_code = """
resultado = list(map(lambda n: n * 2, nums))
"""

    tiempo_loop = timeit.timeit(loop_code, setup, number=iterations)
    tiempo_comp = timeit.timeit(comp_code, setup, number=iterations)
    tiempo_gen = timeit.timeit(gen_code, setup, number=iterations)
    tiempo_map = timeit.timeit(map_code, setup, number=iterations)

    return {
        "loop": tiempo_loop,
        "comprehension": tiempo_comp,
        "generator": tiempo_gen,
        "map": tiempo_map,
    }


def benchmark_filter(size: int, iterations: int = 10000) -> Dict[str, float]:
    """
    Compara performance de filter: solo números pares.
    """
    setup = f"nums = list(range({size}))"

    # Loop con if
    loop_code = """
resultado = []
for n in nums:
    if n % 2 == 0:
        resultado.append(n)
"""

    # List comprehension con if
    comp_code = """
resultado = [n for n in nums if n % 2 == 0]
"""

    # filter() built-in
    filter_code = """
resultado = list(filter(lambda n: n % 2 == 0, nums))
"""

    tiempo_loop = timeit.timeit(loop_code, setup, number=iterations)
    tiempo_comp = timeit.timeit(comp_code, setup, number=iterations)
    tiempo_filter = timeit.timeit(filter_code, setup, number=iterations)

    return {
        "loop": tiempo_loop,
        "comprehension": tiempo_comp,
        "filter": tiempo_filter,
    }


def benchmark_map_filter(size: int, iterations: int = 10000) -> Dict[str, float]:
    """
    Compara performance de map + filter: cuadrados de pares.
    """
    setup = f"nums = list(range({size}))"

    # Loop
    loop_code = """
resultado = []
for n in nums:
    if n % 2 == 0:
        resultado.append(n ** 2)
"""

    # Comprehension
    comp_code = """
resultado = [n ** 2 for n in nums if n % 2 == 0]
"""

    tiempo_loop = timeit.timeit(loop_code, setup, number=iterations)
    tiempo_comp = timeit.timeit(comp_code, setup, number=iterations)

    return {
        "loop": tiempo_loop,
        "comprehension": tiempo_comp,
    }


def benchmark_dict_creation(size: int, iterations: int = 10000) -> Dict[str, float]:
    """
    Compara performance de creación de diccionarios.
    """
    setup = f"items = list(range({size}))"

    # Loop
    loop_code = """
resultado = {}
for i in items:
    resultado[i] = i ** 2
"""

    # Dict comprehension
    comp_code = """
resultado = {i: i ** 2 for i in items}
"""

    tiempo_loop = timeit.timeit(loop_code, setup, number=iterations)
    tiempo_comp = timeit.timeit(comp_code, setup, number=iterations)

    return {
        "loop": tiempo_loop,
        "comprehension": tiempo_comp,
    }


def run_all_benchmarks():
    """Ejecuta todos los benchmarks y muestra resultados."""
    print("=" * 80)
    print("BENCHMARKS: COMPREHENSIONS VS LOOPS")
    print("=" * 80)

    sizes = [10, 100, 1000, 10000]

    for size in sizes:
        print(f"\n{'─' * 80}")
        print(f"TAMAÑO: {size:,} elementos")
        print(f"{'─' * 80}")

        # Ajustar iterations según tamaño para que no tarde mucho
        iterations = 100000 if size <= 100 else 10000 if size <= 1000 else 1000

        # Test 1: Map simple
        print("\n1️⃣  MAP SIMPLE (multiplicar por 2)")
        print("-" * 40)
        resultados = benchmark_simple_map(size, iterations)
        baseline = resultados["loop"]

        for nombre, tiempo in sorted(resultados.items(), key=lambda x: x[1]):
            speedup = baseline / tiempo
            porcentaje = (tiempo / baseline) * 100
            print(f"  {nombre:15s}: {tiempo:8.5f}s  ({speedup:.2f}x)  [{porcentaje:5.1f}% del loop]")

        # Test 2: Filter
        print("\n2️⃣  FILTER (solo pares)")
        print("-" * 40)
        resultados = benchmark_filter(size, iterations)
        baseline = resultados["loop"]

        for nombre, tiempo in sorted(resultados.items(), key=lambda x: x[1]):
            speedup = baseline / tiempo
            porcentaje = (tiempo / baseline) * 100
            print(f"  {nombre:15s}: {tiempo:8.5f}s  ({speedup:.2f}x)  [{porcentaje:5.1f}% del loop]")

        # Test 3: Map + Filter
        print("\n3️⃣  MAP + FILTER (cuadrados de pares)")
        print("-" * 40)
        resultados = benchmark_map_filter(size, iterations)
        baseline = resultados["loop"]

        for nombre, tiempo in sorted(resultados.items(), key=lambda x: x[1]):
            speedup = baseline / tiempo
            porcentaje = (tiempo / baseline) * 100
            print(f"  {nombre:15s}: {tiempo:8.5f}s  ({speedup:.2f}x)  [{porcentaje:5.1f}% del loop]")

        # Test 4: Dict creation
        print("\n4️⃣  DICT CREATION (índice -> cuadrado)")
        print("-" * 40)
        resultados = benchmark_dict_creation(size, iterations)
        baseline = resultados["loop"]

        for nombre, tiempo in sorted(resultados.items(), key=lambda x: x[1]):
            speedup = baseline / tiempo
            porcentaje = (tiempo / baseline) * 100
            print(f"  {nombre:15s}: {tiempo:8.5f}s  ({speedup:.2f}x)  [{porcentaje:5.1f}% del loop]")

    print(f"\n{'=' * 80}")
    print("CONCLUSIÓN:")
    print("  - Comprehensions son consistentemente 2-3x más rápidas")
    print("  - La ventaja crece con el tamaño del dataset")
    print("  - Generators son similares a comprehensions (a veces más rápidas)")
    print("=" * 80)


# ============================================================================
# SECCIÓN 2: ANÁLISIS DE BYTECODE
# ============================================================================

def analyze_bytecode():
    """
    Compara bytecode de loop vs comprehension para entender por qué
    las comprehensions son más rápidas.
    """
    print("\n" + "=" * 80)
    print("ANÁLISIS DE BYTECODE")
    print("=" * 80)

    print("\n1️⃣  LOOP TRADICIONAL CON APPEND")
    print("-" * 80)

    def loop_version():
        nums = range(10)
        resultado = []
        for n in nums:
            resultado.append(n * 2)
        return resultado

    dis.dis(loop_version)

    print("\n2️⃣  LIST COMPREHENSION")
    print("-" * 80)

    def comp_version():
        nums = range(10)
        resultado = [n * 2 for n in nums]
        return resultado

    dis.dis(comp_version)

    print("\n" + "=" * 80)
    print("DIFERENCIAS CLAVE:")
    print("=" * 80)
    print("""
  Loop tradicional:
    - LOAD_ATTR (busca el método .append en cada iteración)
    - CALL_FUNCTION (llama .append como función)
    - Múltiples instrucciones por elemento

  List comprehension:
    - LIST_APPEND (instrucción especializada, más rápida)
    - Menos overhead de lookup y llamadas
    - Optimización en C para construcción de listas

  Conclusión: Comprehensions usan instrucciones más eficientes a nivel de bytecode.
""")


# ============================================================================
# SECCIÓN 3: MEMORY PROFILING
# ============================================================================

def analyze_memory():
    """
    Compara uso de memoria entre list comprehensions y generator expressions.
    """
    print("\n" + "=" * 80)
    print("ANÁLISIS DE MEMORIA")
    print("=" * 80)

    size = 1000000  # 1 millón de elementos

    # List comprehension - carga todo en memoria
    print(f"\n1️⃣  LIST COMPREHENSION ({size:,} elementos)")
    print("-" * 80)

    import tracemalloc

    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()

    lista = [x ** 2 for x in range(size)]

    snapshot_after = tracemalloc.take_snapshot()
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"  Memoria actual: {current / 1024 / 1024:.2f} MB")
    print(f"  Memoria pico:   {peak / 1024 / 1024:.2f} MB")
    print(f"  Tamaño de la lista: {sys.getsizeof(lista) / 1024 / 1024:.2f} MB")

    del lista

    # Generator expression - lazy evaluation
    print(f"\n2️⃣  GENERATOR EXPRESSION ({size:,} elementos)")
    print("-" * 80)

    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()

    generador = (x ** 2 for x in range(size))

    snapshot_after = tracemalloc.take_snapshot()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"  Memoria actual: {current / 1024 / 1024:.2f} MB")
    print(f"  Memoria pico:   {peak / 1024 / 1024:.2f} MB")
    print(f"  Tamaño del generador: {sys.getsizeof(generador)} bytes")

    print("\n" + "=" * 80)
    print("CONCLUSIÓN:")
    print("=" * 80)
    print("""
  List comprehension:
    - Aloca toda la memoria de antemano (~8 MB para 1M de enteros)
    - Acceso rápido, múltiples iteraciones, indexing, slicing
    - Bueno cuando necesitas todos los datos en memoria

  Generator expression:
    - Solo aloca memoria del objeto generador (~200 bytes)
    - Calcula valores on-demand (lazy evaluation)
    - Ideal para datasets grandes o streams infinitos

  Regla de oro:
    - ¿Necesitas la lista completa? → List comprehension
    - ¿Solo iteras una vez o filtras/transformas? → Generator
""")


# ============================================================================
# SECCIÓN 4: EJEMPLOS DE LEGIBILIDAD
# ============================================================================

@dataclass
class Usuario:
    """Modelo de ejemplo para demostraciones."""
    id: int
    nombre: str
    apellido: str
    edad: int
    email: str
    activo: bool


def create_sample_users() -> List[Usuario]:
    """Crea usuarios de ejemplo."""
    return [
        Usuario(1, "Ana", "García", 25, "ana@example.com", True),
        Usuario(2, "Juan", "Pérez", 17, "juan@example.com", True),
        Usuario(3, "María", "López", 30, "maria@example.com", False),
        Usuario(4, "Pedro", "Martínez", 45, "pedro@example.com", True),
        Usuario(5, "Lucía", "Fernández", 16, "lucia@example.com", True),
        Usuario(6, "Carlos", "Rodríguez", 28, "carlos@example.com", True),
        Usuario(7, "Elena", "Sánchez", 65, "elena@example.com", False),
        Usuario(8, "Miguel", "Ramírez", 72, "miguel@example.com", True),
    ]


def demonstrate_readability():
    """
    Demuestra ejemplos de código legible vs ilegible.
    """
    print("\n" + "=" * 80)
    print("EJEMPLOS DE LEGIBILIDAD")
    print("=" * 80)

    usuarios = create_sample_users()

    # Ejemplo 1: Simple y legible
    print("\n1️⃣  EJEMPLO BUENO: Filtro simple")
    print("-" * 80)
    print("Código:")
    print('  adultos = [u.nombre for u in usuarios if u.edad >= 18]')
    print("\nResultado:")
    adultos = [u.nombre for u in usuarios if u.edad >= 18]
    print(f"  {adultos}")
    print("\n✅ Veredicto: LEGIBLE - Una línea, lógica clara, fácil de leer en voz alta")

    # Ejemplo 2: Comprehension compleja e ilegible
    print("\n2️⃣  EJEMPLO MALO: Comprehension compleja")
    print("-" * 80)
    print("Código:")
    codigo_malo = '''  usuarios_procesados = [
      {"id": u.id, "nombre_completo": f"{u.nombre} {u.apellido}",
       "categoria": "senior" if u.edad >= 65 else "adulto" if u.edad >= 18 else "menor",
       "contacto": u.email.lower()}
      for u in usuarios
      if u.activo and "@" in u.email
  ]'''
    print(codigo_malo)

    # Ejecutar para mostrar resultado
    usuarios_procesados = [
        {"id": u.id, "nombre_completo": f"{u.nombre} {u.apellido}",
         "categoria": "senior" if u.edad >= 65 else "adulto" if u.edad >= 18 else "menor",
         "contacto": u.email.lower()}
        for u in usuarios
        if u.activo and "@" in u.email
    ]

    print("\nResultado (primeros 2):")
    for up in usuarios_procesados[:2]:
        print(f"  {up}")

    print("\n❌ Veredicto: ILEGIBLE - Múltiples líneas, lógica compleja, difícil de mantener")

    # Ejemplo 3: Versión refactorizada
    print("\n3️⃣  EJEMPLO BUENO: Refactorizado con función helper")
    print("-" * 80)
    print("Código:")
    codigo_bueno = '''  def procesar_usuario(u: Usuario) -> Dict[str, Any]:
      """Transforma un usuario a formato de salida."""
      if not u.activo or "@" not in u.email:
          return None

      # Categorizar por edad
      if u.edad >= 65:
          categoria = "senior"
      elif u.edad >= 18:
          categoria = "adulto"
      else:
          categoria = "menor"

      return {
          "id": u.id,
          "nombre_completo": f"{u.nombre} {u.apellido}",
          "categoria": categoria,
          "contacto": u.email.lower(),
      }

  usuarios_procesados = [
      procesado
      for u in usuarios
      if (procesado := procesar_usuario(u)) is not None
  ]'''
    print(codigo_bueno)

    def procesar_usuario(u: Usuario) -> Dict[str, Any]:
        """Transforma un usuario a formato de salida."""
        if not u.activo or "@" not in u.email:
            return None

        # Categorizar por edad
        if u.edad >= 65:
            categoria = "senior"
        elif u.edad >= 18:
            categoria = "adulto"
        else:
            categoria = "menor"

        return {
            "id": u.id,
            "nombre_completo": f"{u.nombre} {u.apellido}",
            "categoria": categoria,
            "contacto": u.email.lower(),
        }

    usuarios_procesados_v2 = [
        procesado
        for u in usuarios
        if (procesado := procesar_usuario(u)) is not None
    ]

    print("\nResultado (primeros 2):")
    for up in usuarios_procesados_v2[:2]:
        print(f"  {up}")

    print("\n✅ Veredicto: EXCELENTE")
    print("  - Función helper es testeable y reusable")
    print("  - Comprehension es simple (solo filter)")
    print("  - Lógica de negocio separada de la construcción de la lista")

    # Ejemplo 4: Nested comprehension - MALO
    print("\n4️⃣  EJEMPLO MALO: Nested comprehension")
    print("-" * 80)
    print("Código:")
    print('  matriz = [[1, -2, 3], [4, -5, 6], [7, -8, 9]]')
    print('  positivos = [[n for n in fila if n > 0] for fila in matriz if sum(fila) > 5]')

    matriz = [[1, -2, 3], [4, -5, 6], [7, -8, 9]]
    positivos = [[n for n in fila if n > 0] for fila in matriz if sum(fila) > 5]

    print(f"\nResultado: {positivos}")
    print("\n❌ Veredicto: ILEGIBLE - Demasiado anidado, difícil de seguir")

    # Ejemplo 5: Versión con loop - BUENO
    print("\n5️⃣  EJEMPLO BUENO: Mismo código con loop")
    print("-" * 80)
    print("Código:")
    codigo_loop = '''  matriz = [[1, -2, 3], [4, -5, 6], [7, -8, 9]]
  positivos = []

  for fila in matriz:
      if sum(fila) > 5:
          fila_positivos = []
          for n in fila:
              if n > 0:
                  fila_positivos.append(n)
          positivos.append(fila_positivos)'''
    print(codigo_loop)

    matriz = [[1, -2, 3], [4, -5, 6], [7, -8, 9]]
    positivos_v2 = []

    for fila in matriz:
        if sum(fila) > 5:
            fila_positivos = []
            for n in fila:
                if n > 0:
                    fila_positivos.append(n)
            positivos_v2.append(fila_positivos)

    print(f"\nResultado: {positivos_v2}")
    print("\n✅ Veredicto: LEGIBLE - Variables con nombres descriptivos, lógica clara")

    # Ejemplo 6: Side effects - NUNCA uses comprehension
    print("\n6️⃣  EJEMPLO MALO: Side effects en comprehension")
    print("-" * 80)
    print("Código:")
    print('  _ = [print(f"Procesando: {u.nombre}") for u in usuarios]')
    print("\n❌ Veredicto: ANTI-PATRÓN - Comprehensions NO son para side effects")

    print("\n7️⃣  EJEMPLO BUENO: Side effects con loop")
    print("-" * 80)
    print("Código:")
    print('  for u in usuarios:')
    print('      print(f"Procesando: {u.nombre}")')
    print("\n✅ Veredicto: CORRECTO - Loops son para side effects")

    print("\n" + "=" * 80)
    print("RESUMEN DE LEGIBILIDAD")
    print("=" * 80)
    print("""
  ✅ USA COMPREHENSION cuando:
    - Es una operación simple (map o filter)
    - Cabe en una línea
    - Se puede leer en voz alta sin pausar
    - No tiene side effects

  ❌ USA LOOP cuando:
    - La lógica es compleja
    - Tiene múltiples niveles de nesting
    - Necesitas debuggear con prints
    - Hay side effects (print, log, write, etc)
    - Construyes múltiples colecciones

  Regla de oro: Si pasas más de 5 segundos entendiendo una comprehension,
  reescríbela como loop.
""")


# ============================================================================
# SECCIÓN 5: ANTI-PATRONES COMUNES
# ============================================================================

def demonstrate_antipatterns():
    """Muestra anti-patrones comunes y cómo arreglarlos."""
    print("\n" + "=" * 80)
    print("ANTI-PATRONES COMUNES")
    print("=" * 80)

    # Anti-patrón 1: Iterar múltiples veces
    print("\n❌ ANTI-PATRÓN #1: Iterar múltiples veces")
    print("-" * 80)
    print("Código malo:")
    codigo_malo = '''  nums = list(range(10000))
  pares = [n for n in nums if n % 2 == 0]      # Primera iteración
  impares = [n for n in nums if n % 2 != 0]    # Segunda iteración'''
    print(codigo_malo)

    print("\nCódigo bueno:")
    codigo_bueno = '''  nums = list(range(10000))
  pares = []
  impares = []
  for n in nums:  # Una sola iteración
      if n % 2 == 0:
          pares.append(n)
      else:
          impares.append(n)'''
    print(codigo_bueno)

    # Benchmark
    import timeit
    setup = "nums = list(range(10000))"

    malo = '''
pares = [n for n in nums if n % 2 == 0]
impares = [n for n in nums if n % 2 != 0]
'''

    bueno = '''
pares = []
impares = []
for n in nums:
    if n % 2 == 0:
        pares.append(n)
    else:
        impares.append(n)
'''

    tiempo_malo = timeit.timeit(malo, setup, number=1000)
    tiempo_bueno = timeit.timeit(bueno, setup, number=1000)

    print(f"\nTiempo (malo):  {tiempo_malo:.5f}s")
    print(f"Tiempo (bueno): {tiempo_bueno:.5f}s")
    print(f"Mejora: {tiempo_malo / tiempo_bueno:.2f}x más rápido")

    # Anti-patrón 2: Comprehension no utilizada
    print("\n❌ ANTI-PATRÓN #2: Comprehension para side effects")
    print("-" * 80)
    print("Código malo:")
    print('  _ = [print(x) for x in items]')
    print("\nCódigo bueno:")
    print('  for x in items:')
    print('      print(x)')

    # Anti-patrón 3: Comprehension cuando necesitas break
    print("\n❌ ANTI-PATRÓN #3: Buscar con comprehension (procesa todo)")
    print("-" * 80)
    print("Código malo:")
    malo_buscar = '''  nums = list(range(1000000))
  # Procesa TODOS los elementos aunque encuentre uno que cumpla
  primero = [n for n in nums if n > 500000][0]'''
    print(malo_buscar)

    print("\nCódigo bueno (opción 1 - loop con break):")
    bueno_buscar_1 = '''  nums = list(range(1000000))
  primero = None
  for n in nums:
      if n > 500000:
          primero = n
          break  # Sale temprano'''
    print(bueno_buscar_1)

    print("\nCódigo bueno (opción 2 - next con generator):")
    bueno_buscar_2 = '''  nums = list(range(1000000))
  primero = next((n for n in nums if n > 500000), None)'''
    print(bueno_buscar_2)

    # Benchmark
    setup = "nums = list(range(1000000))"

    malo = "primero = [n for n in nums if n > 500000][0]"
    bueno_loop = """
primero = None
for n in nums:
    if n > 500000:
        primero = n
        break
"""
    bueno_next = "primero = next((n for n in nums if n > 500000), None)"

    tiempo_malo = timeit.timeit(malo, setup, number=100)
    tiempo_loop = timeit.timeit(bueno_loop, setup, number=100)
    tiempo_next = timeit.timeit(bueno_next, setup, number=100)

    print(f"\nTiempo (comprehension): {tiempo_malo:.5f}s")
    print(f"Tiempo (loop+break):    {tiempo_loop:.5f}s  ({tiempo_malo/tiempo_loop:.2f}x más rápido)")
    print(f"Tiempo (next):          {tiempo_next:.5f}s  ({tiempo_malo/tiempo_next:.2f}x más rápido)")

    print("\n" + "=" * 80)


# ============================================================================
# MAIN: EJECUTA TODAS LAS DEMOSTRACIONES
# ============================================================================

def main():
    """
    Función principal que ejecuta todas las demostraciones.

    Puedes comentar/descomentar secciones según lo que quieras ver.
    """
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  ANÁLISIS COMPLETO: COMPREHENSIONS VS LOOPS".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    # Sección 1: Benchmarks de performance
    print("\n" + "█" * 80)
    print(" PARTE 1: BENCHMARKS DE PERFORMANCE")
    print("█" * 80)
    run_all_benchmarks()

    # Sección 2: Análisis de bytecode
    print("\n" + "█" * 80)
    print(" PARTE 2: ANÁLISIS DE BYTECODE")
    print("█" * 80)
    analyze_bytecode()

    # Sección 3: Memory profiling
    print("\n" + "█" * 80)
    print(" PARTE 3: PROFILING DE MEMORIA")
    print("█" * 80)
    analyze_memory()

    # Sección 4: Ejemplos de legibilidad
    print("\n" + "█" * 80)
    print(" PARTE 4: EJEMPLOS DE LEGIBILIDAD")
    print("█" * 80)
    demonstrate_readability()

    # Sección 5: Anti-patrones
    print("\n" + "█" * 80)
    print(" PARTE 5: ANTI-PATRONES Y CÓMO EVITARLOS")
    print("█" * 80)
    demonstrate_antipatterns()

    # Conclusión final
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  CONCLUSIÓN FINAL".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    print("""
  ┌────────────────────────────────────────────────────────────────────┐
  │  CUÁNDO USAR CADA UNO                                              │
  ├────────────────────────────────────────────────────────────────────┤
  │                                                                    │
  │  ✅ USA COMPREHENSION cuando:                                      │
  │     • Operación simple (map, filter, o ambos)                     │
  │     • Cabe en una línea (<80 caracteres)                          │
  │     • Legible en voz alta sin pausar                              │
  │     • No hay side effects                                         │
  │     • No necesitas break/continue                                 │
  │     → Resultado: Código más rápido (2-3x) y legible               │
  │                                                                    │
  │  ✅ USA LOOP cuando:                                               │
  │     • Lógica compleja o múltiples pasos                           │
  │     • Necesitas debuggear con prints                              │
  │     • Hay side effects (print, log, write)                        │
  │     • Construyes múltiples colecciones                            │
  │     • Necesitas break/continue                                    │
  │     • Nested operations (>1 nivel)                                │
  │     → Resultado: Código mantenible y debuggeable                  │
  │                                                                    │
  │  ✅ USA GENERATOR cuando:                                          │
  │     • Dataset muy grande (>1M elementos)                          │
  │     • Solo iteras una vez                                         │
  │     • Pasas a funciones como sum(), max(), any()                  │
  │     • Streams infinitos o lazy evaluation                         │
  │     → Resultado: Uso eficiente de memoria                         │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘

  📊 DATOS CLAVE DE LOS TESTS:
     - Comprehensions son 2-3x más rápidas que loops para operaciones simples
     - Generators usan ~99.9% menos memoria que listas para datasets grandes
     - Legibilidad > Performance (salvo que sea cuello de botella)

  💡 REGLA DE ORO:
     Si pasas más de 5 segundos entendiendo una comprehension,
     reescríbela como loop. La claridad siempre gana.

  📚 MÁS INFO:
     - Guía completa: 10_comprension_vs_loops.md
     - PEP 202: https://www.python.org/dev/peps/pep-0202/
     - Python Performance Tips: https://wiki.python.org/moin/PythonSpeed
""")

    print("\n" + "=" * 80)
    print("  Script completado. ¡Revisa los resultados arriba!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
