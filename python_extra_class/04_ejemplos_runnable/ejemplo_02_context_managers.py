"""
Ejemplos completos de Context Managers en Python.

Este módulo muestra ejemplos prácticos y ejecutables de:
- Context managers con __enter__ y __exit__
- Timer para medir tiempo de ejecución
- TemporaryState para estado temporal
- Manejo de archivos
- Simulación de conexión a base de datos con rollback
- Decorador @contextmanager

Filosofía: Código claro, ejemplos ejecutables, enfoque en el "por qué".
"""

import time
import os
from contextlib import contextmanager
from typing import Any, Optional, Generator, Dict, List
from pathlib import Path


# ============================================================================
# SECCIÓN 1: Context Manager Básico - Timer
# ============================================================================

class Timer:
    """
    Context manager para medir tiempo de ejecución.

    ¿Por qué usar context managers?
    - Garantizan que el código de limpieza se ejecute
    - Sintaxis clara con 'with'
    - Previenen fugas de recursos
    """

    def __init__(self, nombre: str = "Operación") -> None:
        """
        Inicializa el timer.

        Args:
            nombre: Nombre de la operación a medir
        """
        self.nombre = nombre
        self.inicio: Optional[float] = None
        self.fin: Optional[float] = None
        self.duracion: Optional[float] = None

    def __enter__(self) -> "Timer":
        """
        Se ejecuta al ENTRAR al bloque 'with'.

        Este método se llama automáticamente cuando haces:
        with Timer() as t:
            # código aquí
        """
        print(f"\n  [{self.nombre}] Iniciando...")
        self.inicio = time.perf_counter()
        return self  # Esto es lo que obtienes en la variable 'as'

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        exc_traceback: Optional[Any]
    ) -> bool:
        """
        Se ejecuta al SALIR del bloque 'with'.

        Parámetros:
            exc_type: Tipo de excepción si hubo error (None si todo bien)
            exc_value: La excepción en sí
            exc_traceback: Traceback de la excepción

        Returns:
            bool: True para suprimir la excepción, False para propagarla
        """
        self.fin = time.perf_counter()
        self.duracion = self.fin - self.inicio

        if exc_type is None:
            # No hubo error
            print(f"[OK] [{self.nombre}] Completado en {self.duracion:.4f} segundos")
        else:
            # Hubo un error
            print(f"[X] [{self.nombre}] Error después de {self.duracion:.4f} segundos")
            print(f"  Tipo de error: {exc_type.__name__}")
            print(f"  Mensaje: {exc_value}")

        # Retornamos False para NO suprimir la excepción
        # Si retornáramos True, la excepción se "tragaría"
        return False


def ejemplo_timer() -> None:
    """Demuestra el uso del context manager Timer."""
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Context Manager Timer (__enter__ y __exit__)")
    print("=" * 70)

    print("\nCaso 1: Operación exitosa")
    print("-" * 70)

    with Timer("Cálculo matemático") as timer:
        # Simular trabajo
        resultado = sum(i ** 2 for i in range(100000))
        print(f"  → Calculando suma de cuadrados...")
        print(f"  → Resultado: {resultado:,}")

    # Puedes acceder a la duración después
    print(f"  Info: La operación tomó {timer.duracion:.4f}s")

    print("\nCaso 2: Operación con error")
    print("-" * 70)

    try:
        with Timer("Operación que falla") as timer:
            print("  → Haciendo algo...")
            time.sleep(0.1)
            print("  → Causando un error...")
            raise ValueError("¡Algo salió mal!")
    except ValueError as e:
        print(f"  Excepción capturada fuera del context manager: {e}")

    print("\nCaso 3: Múltiples timers anidados")
    print("-" * 70)

    with Timer("Operación completa"):
        print("  → Etapa 1")
        with Timer("  Subtarea 1"):
            time.sleep(0.1)
            print("    → Procesando datos...")

        print("  → Etapa 2")
        with Timer("  Subtarea 2"):
            time.sleep(0.15)
            print("    → Guardando resultados...")


# ============================================================================
# SECCIÓN 2: TemporaryState - Restaurar Estado
# ============================================================================

class TemporaryState:
    """
    Context manager para modificar temporalmente un objeto.

    Útil para:
    - Tests (cambiar configuración temporalmente)
    - Modificaciones reversibles
    - Garantizar que el estado se restaure
    """

    def __init__(self, obj: Any, **kwargs: Any) -> None:
        """
        Inicializa el context manager.

        Args:
            obj: Objeto a modificar
            **kwargs: Atributos a cambiar temporalmente
        """
        self.obj = obj
        self.cambios = kwargs
        self.estado_original: Dict[str, Any] = {}

    def __enter__(self) -> Any:
        """Guarda el estado original y aplica cambios."""
        print("\n  → [TemporaryState] Guardando estado original...")

        # Guardar valores originales
        for key, nuevo_valor in self.cambios.items():
            if hasattr(self.obj, key):
                valor_original = getattr(self.obj, key)
                self.estado_original[key] = valor_original
                print(f"    • {key}: {valor_original} → {nuevo_valor}")
            else:
                print(f"    • {key}: (nuevo) → {nuevo_valor}")
                self.estado_original[key] = None  # Marca para eliminar después

        # Aplicar cambios
        print("  → [TemporaryState] Aplicando cambios temporales...")
        for key, valor in self.cambios.items():
            setattr(self.obj, key, valor)

        return self.obj

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        exc_traceback: Optional[Any]
    ) -> bool:
        """Restaura el estado original."""
        print("  → [TemporaryState] Restaurando estado original...")

        for key, valor_original in self.estado_original.items():
            if valor_original is None:
                # Era un atributo nuevo, eliminarlo
                if hasattr(self.obj, key):
                    delattr(self.obj, key)
                    print(f"    • {key}: eliminado")
            else:
                # Restaurar valor original
                valor_actual = getattr(self.obj, key)
                setattr(self.obj, key, valor_original)
                print(f"    • {key}: {valor_actual} → {valor_original}")

        return False


class Configuracion:
    """Clase de ejemplo para demostrar TemporaryState."""

    def __init__(self) -> None:
        self.debug = False
        self.timeout = 30
        self.max_reintentos = 3

    def __repr__(self) -> str:
        return (
            f"Configuracion(debug={self.debug}, "
            f"timeout={self.timeout}, "
            f"max_reintentos={self.max_reintentos})"
        )


def ejemplo_temporary_state() -> None:
    """Demuestra el uso de TemporaryState."""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: TemporaryState - Modificaciones Reversibles")
    print("=" * 70)

    config = Configuracion()

    print(f"\nEstado inicial: {config}")

    print("\nCaso 1: Modificación temporal para debugging")
    print("-" * 70)

    # Modificar temporalmente para debugging
    with TemporaryState(config, debug=True, timeout=5):
        print(f"\n  Estado dentro del context manager: {config}")
        print("  → Ejecutando con debug activado...")
        # Aquí harías operaciones de debugging

    print(f"\n  Estado después del context manager: {config}")
    print("  [OK] Estado restaurado automáticamente!")

    print("\nCaso 2: Múltiples modificaciones temporales")
    print("-" * 70)

    with TemporaryState(config, debug=True, max_reintentos=10, nuevo_atributo="test"):
        print(f"\n  Estado modificado: {config}")
        print(f"  Nuevo atributo: {config.nuevo_atributo}")

    print(f"\n  Estado restaurado: {config}")
    print(f"  ¿Tiene nuevo_atributo? {hasattr(config, 'nuevo_atributo')}")


# ============================================================================
# SECCIÓN 3: Manejo de Archivos
# ============================================================================

def ejemplo_file_handling() -> None:
    """
    Demuestra por qué usar context managers con archivos.

    Beneficios:
    - El archivo se cierra automáticamente
    - Incluso si hay un error
    - Código más limpio y seguro
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Manejo de Archivos con Context Managers")
    print("=" * 70)

    # Crear directorio temporal para ejemplos
    temp_dir = Path("/tmp/context_manager_examples")
    temp_dir.mkdir(exist_ok=True)
    archivo_path = temp_dir / "ejemplo.txt"

    print("\nCaso 1: Escritura de archivo (forma correcta)")
    print("-" * 70)

    print("  → Escribiendo archivo con context manager...")
    with open(archivo_path, "w", encoding="utf-8") as f:
        print(f"    • Archivo abierto: {f.name}")
        print(f"    • ¿Está cerrado? {f.closed}")
        f.write("Línea 1: Hola desde Python\n")
        f.write("Línea 2: Context managers son geniales\n")
        f.write("Línea 3: El archivo se cerrará automáticamente\n")
        print("    • Datos escritos")

    print(f"  → Después del 'with': ¿está cerrado? {f.closed}")
    print("  [OK] El archivo se cerró automáticamente!")

    print("\nCaso 2: Lectura de archivo")
    print("-" * 70)

    print("  → Leyendo archivo con context manager...")
    with open(archivo_path, "r", encoding="utf-8") as f:
        lineas = f.readlines()
        print(f"    • Se leyeron {len(lineas)} líneas:")
        for i, linea in enumerate(lineas, 1):
            print(f"      {i}. {linea.strip()}")

    print("\nCaso 3: ¿Qué pasa con errores?")
    print("-" * 70)

    print("  → Intentando operación que falla...")
    try:
        with open(archivo_path, "w", encoding="utf-8") as f:
            f.write("Escribiendo algo...\n")
            print("    • Primera escritura exitosa")
            print("    • Causando un error...")
            raise RuntimeError("¡Error simulado!")
            f.write("Esto nunca se escribirá\n")
    except RuntimeError as e:
        print(f"    [X] Error: {e}")
        print(f"    • ¿Archivo cerrado después del error? {f.closed}")
        print("    [OK] ¡El archivo se cerró a pesar del error!")

    # Verificar contenido
    with open(archivo_path, "r", encoding="utf-8") as f:
        contenido = f.read()
        print(f"\n  Contenido final del archivo:")
        print(f"    {contenido}")

    print("\nCaso 4: Múltiples archivos")
    print("-" * 70)

    archivo_entrada = temp_dir / "entrada.txt"
    archivo_salida = temp_dir / "salida.txt"

    # Crear archivo de entrada
    with open(archivo_entrada, "w", encoding="utf-8") as f:
        f.write("Python\nContext\nManagers\nSon\nIncreíbles\n")

    print("  → Procesando: entrada.txt → salida.txt")

    # Leer de uno, escribir a otro
    with open(archivo_entrada, "r", encoding="utf-8") as entrada, \
         open(archivo_salida, "w", encoding="utf-8") as salida:
        print("    • Ambos archivos abiertos")
        for i, linea in enumerate(entrada, 1):
            linea_modificada = f"{i}. {linea.strip().upper()}\n"
            salida.write(linea_modificada)
            print(f"      Procesada: {linea.strip()} → {linea_modificada.strip()}")

    print("    [OK] Ambos archivos cerrados automáticamente")

    # Limpiar archivos de ejemplo
    for archivo in [archivo_path, archivo_entrada, archivo_salida]:
        if archivo.exists():
            archivo.unlink()


# ============================================================================
# SECCIÓN 4: Simulación de Base de Datos con Rollback
# ============================================================================

class DatabaseConnection:
    """
    Simula una conexión a base de datos con transacciones.

    Características:
    - Auto-commit si todo sale bien
    - Auto-rollback si hay un error
    - Se cierra automáticamente
    """

    def __init__(self, nombre_db: str) -> None:
        """
        Inicializa la conexión a la base de datos.

        Args:
            nombre_db: Nombre de la base de datos
        """
        self.nombre_db = nombre_db
        self.conectado = False
        self.en_transaccion = False
        self.operaciones: List[str] = []
        self.datos: Dict[str, Any] = {}

    def __enter__(self) -> "DatabaseConnection":
        """Abre conexión e inicia transacción."""
        print(f"\n  → [DB] Conectando a '{self.nombre_db}'...")
        self.conectado = True
        print("  → [DB] Conexión establecida")
        print("  → [DB] Iniciando transacción...")
        self.en_transaccion = True
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        exc_traceback: Optional[Any]
    ) -> bool:
        """Cierra conexión con commit o rollback según el caso."""
        if exc_type is None:
            # No hubo error: hacer commit
            print("  → [DB] Sin errores, haciendo COMMIT...")
            self._commit()
            print("  [OK] [DB] Transacción completada exitosamente")
        else:
            # Hubo error: hacer rollback
            print(f"  → [DB] Error detectado: {exc_type.__name__}")
            print("  → [DB] Haciendo ROLLBACK...")
            self._rollback()
            print("  [X] [DB] Transacción revertida")

        print("  → [DB] Cerrando conexión...")
        self.conectado = False
        self.en_transaccion = False
        print("  [OK] [DB] Conexión cerrada")

        return False  # No suprimir la excepción

    def ejecutar(self, operacion: str) -> None:
        """Ejecuta una operación en la base de datos."""
        if not self.en_transaccion:
            raise RuntimeError("No hay transacción activa")

        print(f"    → SQL: {operacion}")
        self.operaciones.append(operacion)

    def insertar(self, tabla: str, clave: str, valor: Any) -> None:
        """Inserta un registro."""
        self.ejecutar(f"INSERT INTO {tabla} VALUES ('{clave}', '{valor}')")
        self.datos[clave] = valor

    def _commit(self) -> None:
        """Confirma la transacción (simula commit)."""
        print(f"    • {len(self.operaciones)} operaciones confirmadas")
        print(f"    • Estado final: {len(self.datos)} registros en cache")

    def _rollback(self) -> None:
        """Revierte la transacción (simula rollback)."""
        operaciones_revertidas = len(self.operaciones)
        self.operaciones.clear()
        self.datos.clear()
        print(f"    • {operaciones_revertidas} operaciones revertidas")
        print("    • Todos los cambios descartados")


def ejemplo_database_connection() -> None:
    """Demuestra el manejo de transacciones de base de datos."""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Simulación de Base de Datos con Transacciones")
    print("=" * 70)

    print("\nCaso 1: Transacción exitosa (auto-commit)")
    print("-" * 70)

    with DatabaseConnection("usuarios_db") as db:
        print("\n  Insertando usuarios:")
        db.insertar("usuarios", "user1", "Carlos")
        db.insertar("usuarios", "user2", "Ana")
        db.insertar("usuarios", "user3", "Bob")
        print(f"\n  Estado actual: {db.datos}")

    print("\n  [OK] Transacción completada y cerrada automáticamente")

    print("\nCaso 2: Transacción con error (auto-rollback)")
    print("-" * 70)

    try:
        with DatabaseConnection("productos_db") as db:
            print("\n  Insertando productos:")
            db.insertar("productos", "prod1", "Laptop")
            db.insertar("productos", "prod2", "Mouse")
            print(f"\n  Estado antes del error: {db.datos}")

            print("\n  Causando un error...")
            raise ValueError("Error de validación: precio negativo")

            # Esto nunca se ejecutará
            db.insertar("productos", "prod3", "Teclado")

    except ValueError as e:
        print(f"\n  Excepción capturada: {e}")
        print("  [OK] Rollback ejecutado automáticamente")

    print("\nCaso 3: Múltiples transacciones")
    print("-" * 70)

    print("\n  Primera transacción (exitosa):")
    with DatabaseConnection("almacen_db") as db:
        db.insertar("productos", "p1", "Mesa")
        db.insertar("productos", "p2", "Silla")

    print("\n  Segunda transacción (con error):")
    try:
        with DatabaseConnection("almacen_db") as db:
            db.insertar("productos", "p3", "Lámpara")
            raise RuntimeError("Error de red")
    except RuntimeError:
        pass

    print("\n  Tercera transacción (exitosa):")
    with DatabaseConnection("almacen_db") as db:
        db.insertar("productos", "p4", "Escritorio")

    print("\n  [OK] Cada transacción fue independiente")


# ============================================================================
# SECCIÓN 5: Decorador @contextmanager
# ============================================================================

@contextmanager
def timer_simple(nombre: str) -> Generator[Dict[str, Any], None, None]:
    """
    Context manager usando el decorador @contextmanager.

    ¿Por qué usar @contextmanager?
    - Más simple que crear una clase
    - Perfecto para casos simples
    - Usa yield para separar enter/exit

    Args:
        nombre: Nombre de la operación

    Yields:
        Dict con información del timer
    """
    print(f"\n  [{nombre}] Iniciando...")
    inicio = time.perf_counter()
    info = {"nombre": nombre, "inicio": inicio}

    try:
        # El 'yield' separa __enter__ de __exit__
        # Lo que está ANTES es el __enter__
        yield info  # Esto es lo que obtienes con 'as'
        # Lo que está DESPUÉS es el __exit__

    finally:
        # Este bloque SIEMPRE se ejecuta (como __exit__)
        fin = time.perf_counter()
        duracion = fin - inicio
        info["duracion"] = duracion
        print(f"[OK] [{nombre}] Completado en {duracion:.4f} segundos")


@contextmanager
def cambiar_directorio(nuevo_dir: str) -> Generator[Path, None, None]:
    """
    Context manager para cambiar directorio temporalmente.

    Args:
        nuevo_dir: Directorio temporal

    Yields:
        Path del nuevo directorio
    """
    original = Path.cwd()
    print(f"\n  → Cambiando: {original} → {nuevo_dir}")

    try:
        nuevo_path = Path(nuevo_dir)
        nuevo_path.mkdir(exist_ok=True)
        os.chdir(nuevo_path)
        print(f"  → Directorio actual: {Path.cwd()}")
        yield nuevo_path

    finally:
        os.chdir(original)
        print(f"  → Restaurado: {Path.cwd()}")


@contextmanager
def suprimir_excepciones(*tipos_excepcion: type) -> Generator[None, None, None]:
    """
    Context manager que suprime ciertos tipos de excepciones.

    Args:
        *tipos_excepcion: Tipos de excepciones a suprimir
    """
    print(f"\n  → Suprimiendo: {[e.__name__ for e in tipos_excepcion]}")

    try:
        yield
    except tipos_excepcion as e:
        print(f"  → Excepción suprimida: {type(e).__name__}: {e}")
        # No re-lanzamos la excepción, la "tragamos"


def ejemplo_contextmanager_decorator() -> None:
    """Demuestra el uso del decorador @contextmanager."""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Decorador @contextmanager")
    print("=" * 70)

    print("\nCaso 1: Timer simple con @contextmanager")
    print("-" * 70)

    with timer_simple("Cálculo de Fibonacci") as info:
        print(f"  → Información del timer: {info}")

        def fibonacci(n: int) -> int:
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        resultado = fibonacci(25)
        print(f"  → Fibonacci(25) = {resultado}")

    print(f"  → Duración guardada: {info['duracion']:.4f}s")

    print("\nCaso 2: Cambiar directorio temporalmente")
    print("-" * 70)

    print(f"  Directorio inicial: {Path.cwd()}")

    with cambiar_directorio("/tmp/test_context"):
        print("  → Operaciones en directorio temporal...")
        print(f"    • Directorio actual: {Path.cwd()}")
        # Aquí podrías crear archivos, etc.

    print(f"  Directorio final: {Path.cwd()}")

    print("\nCaso 3: Suprimir excepciones específicas")
    print("-" * 70)

    print("\n  Sin suprimir:")
    try:
        print("    → Causando ValueError...")
        raise ValueError("Este error NO se suprime")
    except ValueError as e:
        print(f"    [X] Excepción capturada: {e}")

    print("\n  Con supresión:")
    with suprimir_excepciones(ValueError, TypeError):
        print("    → Causando ValueError...")
        raise ValueError("Este error SÍ se suprime")
        print("    → Esta línea no se ejecutará")

    print("    [OK] Código continúa después de la excepción suprimida")

    print("\n  Excepción no suprimida:")
    try:
        with suprimir_excepciones(ValueError):
            print("    → Causando RuntimeError...")
            raise RuntimeError("Este error NO está en la lista de supresión")
    except RuntimeError as e:
        print(f"    [X] Excepción capturada fuera: {e}")


# ============================================================================
# SECCIÓN 6: Comparación de Enfoques
# ============================================================================

def ejemplo_comparacion_enfoques() -> None:
    """Compara diferentes formas de crear context managers."""
    print("\n" + "=" * 70)
    print("EJEMPLO 6: Comparación de Enfoques")
    print("=" * 70)

    print("\nEnfoque 1: Clase con __enter__ y __exit__")
    print("-" * 70)
    print("""
  Ventajas:
    • Más control y flexibilidad
    • Puede mantener estado complejo
    • Métodos adicionales disponibles

  Cuándo usar:
    • Context managers complejos
    • Necesitas mantener mucho estado
    • Múltiples métodos auxiliares

  Ejemplo:
    class MiContextManager:
        def __enter__(self):
            # setup
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            # cleanup
            return False
    """)

    print("\nEnfoque 2: Decorador @contextmanager")
    print("-" * 70)
    print("""
  Ventajas:
    • Código más simple y conciso
    • Menos boilerplate
    • Perfecto para casos simples

  Cuándo usar:
    • Context managers simples
    • Poco estado a mantener
    • Lógica directa (setup → yield → cleanup)

  Ejemplo:
    @contextmanager
    def mi_context_manager():
        # setup
        yield valor
        # cleanup
    """)

    print("\nEjemplo práctico de ambos:")
    print("-" * 70)

    # Clase
    class TempValue:
        def __init__(self, obj: Any, attr: str, temp_val: Any) -> None:
            self.obj = obj
            self.attr = attr
            self.temp_val = temp_val
            self.original = None

        def __enter__(self) -> Any:
            self.original = getattr(self.obj, self.attr)
            setattr(self.obj, self.attr, self.temp_val)
            return self.obj

        def __exit__(self, *args: Any) -> bool:
            setattr(self.obj, self.attr, self.original)
            return False

    # Decorador (equivalente)
    @contextmanager
    def temp_value(obj: Any, attr: str, temp_val: Any) -> Generator[Any, None, None]:
        original = getattr(obj, attr)
        setattr(obj, attr, temp_val)
        try:
            yield obj
        finally:
            setattr(obj, attr, original)

    # Probar ambos
    class Config:
        def __init__(self) -> None:
            self.modo = "producción"

    config = Config()

    print(f"\n  Estado inicial: modo = '{config.modo}'")

    print("\n  Usando clase:")
    with TempValue(config, "modo", "desarrollo"):
        print(f"    • Dentro: modo = '{config.modo}'")
    print(f"    • Fuera: modo = '{config.modo}'")

    print("\n  Usando decorador:")
    with temp_value(config, "modo", "testing"):
        print(f"    • Dentro: modo = '{config.modo}'")
    print(f"    • Fuera: modo = '{config.modo}'")

    print("\n  [OK] Ambos enfoques funcionan igual!")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main() -> None:
    """
    Ejecuta todos los ejemplos de context managers.

    Cada ejemplo es independiente y muestra un concepto diferente
    con salida clara para entender qué está sucediendo.
    """
    print("\n" + "=" * 70)
    print("EJEMPLOS COMPLETOS DE CONTEXT MANAGERS EN PYTHON")
    print("=" * 70)
    print("\nEstos ejemplos te mostrarán:")
    print("  1. Timer - Context manager con __enter__ y __exit__")
    print("  2. TemporaryState - Modificaciones reversibles")
    print("  3. Manejo de archivos - Por qué usar 'with'")
    print("  4. Transacciones de DB - Commit y rollback automático")
    print("  5. Decorador @contextmanager - Enfoque simplificado")
    print("  6. Comparación de enfoques")

    # Ejecutar todos los ejemplos
    ejemplo_timer()
    ejemplo_temporary_state()
    ejemplo_file_handling()
    ejemplo_database_connection()
    ejemplo_contextmanager_decorator()
    ejemplo_comparacion_enfoques()

    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN DE MEJORES PRÁCTICAS")
    print("=" * 70)
    print("""
1. USA context managers para gestión de recursos
   • Archivos: with open(...) as f:
   • Conexiones: with connect(...) as conn:
   • Locks: with lock:
   • Garantiza limpieza incluso con errores

2. CREA tus propios context managers
   • Clase (__enter__/__exit__): para casos complejos
   • @contextmanager: para casos simples
   • Usa yield para separar setup/cleanup

3. __exit__ maneja errores automáticamente
   • Recibe exc_type, exc_value, exc_traceback
   • Return True: suprime la excepción
   • Return False: propaga la excepción
   • Finally: siempre se ejecuta

4. PATRONES COMUNES
   • Timer: medir tiempo de ejecución
   • TemporaryState: cambios reversibles
   • Resource: garantizar cleanup (archivos, DBs, locks)
   • Suprimir: ignorar excepciones específicas

5. BENEFICIOS
   • Código más limpio y legible
   • Previene fugas de recursos
   • Manejo de errores automático
   • Más pythonic que try/finally manual

¿Cuándo usar cada enfoque?
  • Clase: context managers complejos, mucho estado
  • @contextmanager: casos simples, poco estado

¿Dudas? Experimenta modificando estos ejemplos. ¡La práctica es clave!
    """)


if __name__ == "__main__":
    main()
