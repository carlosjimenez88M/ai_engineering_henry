#!/usr/bin/env python3
"""
Ejemplo 04: Logging Básico
===========================

Demuestra:
1. Setup básico de logger
2. Los 5 niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
3. Múltiples handlers (consola + archivo)
4. Formatters diferentes por handler
5. Logging vs Print vs Raise

Prerrequisito: Lee 11_logging_patterns.md

Ejecuta: python ejemplo_04_logging_basico.py
"""

import logging
import sys
from pathlib import Path
from typing import Optional


# ============================================================================
# PARTE 1: Setup básico de logging
# ============================================================================

def setup_basic_logger() -> logging.Logger:
    """
    Configura logger básico con consola.

    Returns:
        Logger configurado con nivel DEBUG
    """
    # Crea logger con nombre del módulo
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Nivel más bajo = ve todo

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Formatter simple para desarrollo
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)-8s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def demo_basic_logging():
    """Demuestra uso básico de logging."""
    print("\n" + "="*70)
    print("DEMO 1: Logging básico")
    print("="*70)

    logger = setup_basic_logger()

    logger.debug("Este es un mensaje DEBUG")
    logger.info("Este es un mensaje INFO")
    logger.warning("Este es un mensaje WARNING")
    logger.error("Este es un mensaje ERROR")
    logger.critical("Este es un mensaje CRITICAL")


# ============================================================================
# PARTE 2: Los 5 niveles - Cuándo usar cada uno
# ============================================================================

def demo_log_levels():
    """Demuestra cuándo usar cada nivel de log."""
    print("\n" + "="*70)
    print("DEMO 2: Los 5 niveles de log")
    print("="*70)

    logger = setup_basic_logger()

    print("\n--- DEBUG: Variables intermedias, flujo de ejecución ---")
    x = 10
    y = 20
    logger.debug(f"Variables: x={x}, y={y}")
    resultado = x + y
    logger.debug(f"Resultado calculado: {resultado}")

    print("\n--- INFO: Eventos normales del negocio ---")
    user_id = 123
    logger.info(f"Usuario {user_id} inició sesión")
    logger.info(f"Procesando pedido para usuario {user_id}")
    logger.info("Pedido procesado exitosamente")

    print("\n--- WARNING: Problemas no críticos ---")
    logger.warning("API respondió lento: 2.5s (límite: 2s)")
    logger.warning("Cache miss, consultando base de datos")
    logger.warning("Disco al 85% de capacidad")

    print("\n--- ERROR: Operación falló ---")
    logger.error("No se pudo conectar a la base de datos")
    logger.error("Archivo no encontrado: datos.csv")
    logger.error("Validación falló: email inválido")

    print("\n--- CRITICAL: Sistema comprometido ---")
    logger.critical("Memoria al 98%, posible crash inminente")
    logger.critical("Base de datos principal inalcanzable")


# ============================================================================
# PARTE 3: Múltiples handlers (consola + archivo)
# ============================================================================

def setup_multi_handler_logger() -> logging.Logger:
    """
    Configura logger con múltiples handlers:
    - Consola: muestra DEBUG+ con formato simple
    - Archivo: guarda INFO+ con formato detallado

    Returns:
        Logger configurado con 2 handlers
    """
    logger = logging.getLogger("multi_handler")
    logger.setLevel(logging.DEBUG)

    # Handler 1: Consola (todo)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Handler 2: Archivo (solo INFO+)
    log_file = Path(__file__).parent / "ejemplo_04_output.log"
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger, log_file


def demo_multiple_handlers():
    """Demuestra logger con múltiples handlers."""
    print("\n" + "="*70)
    print("DEMO 3: Múltiples handlers (consola + archivo)")
    print("="*70)

    logger, log_file = setup_multi_handler_logger()

    print("\n>>> Generando logs con múltiples destinos...\n")

    logger.debug("Mensaje DEBUG - solo en consola")
    logger.info("Mensaje INFO - en consola Y archivo")
    logger.warning("Mensaje WARNING - en consola Y archivo")
    logger.error("Mensaje ERROR - en consola Y archivo")

    print(f"\n>>> Logs guardados en: {log_file}")
    print(">>> Contenido del archivo:\n")

    with open(log_file, 'r') as f:
        for line in f:
            print(f"    {line.rstrip()}")


# ============================================================================
# PARTE 4: Logging vs Print vs Raise
# ============================================================================

def demo_logging_vs_print_vs_raise():
    """Demuestra cuándo usar logging, print, o raise."""
    print("\n" + "="*70)
    print("DEMO 4: Logging vs Print vs Raise")
    print("="*70)

    logger = setup_basic_logger()

    # Caso 1: Print para output esperado
    print("\n--- Caso 1: print() para output del programa ---")
    stats = {"mean": 42.5, "count": 100}
    logger.info("Calculando estadísticas...")  # Logging = diagnóstico
    print(f"Resultado: {stats}")  # Print = output esperado

    # Caso 2: Logging para monitoreo
    print("\n--- Caso 2: logging para monitoreo ---")

    def procesar_pedido(pedido_id: int) -> Optional[dict]:
        """Procesa un pedido."""
        logger.info(f"Procesando pedido {pedido_id}")  # Monitoreo

        # Simulación de validación
        if pedido_id < 0:
            logger.warning(f"Pedido {pedido_id} inválido")  # Warning
            return None

        logger.info(f"Pedido {pedido_id} procesado")
        return {"status": "ok", "pedido_id": pedido_id}

    resultado = procesar_pedido(123)
    print(f"Resultado: {resultado}")

    resultado_invalido = procesar_pedido(-1)
    print(f"Resultado inválido: {resultado_invalido}")

    # Caso 3: Raise para errores fatales
    print("\n--- Caso 3: raise para errores fatales ---")

    def conectar_bd(host: str) -> bool:
        """Conecta a base de datos."""
        logger.info(f"Conectando a {host}...")

        if host == "localhost":
            logger.info("Conexión exitosa")
            return True
        else:
            logger.critical(f"No se puede conectar a {host}")
            raise ConnectionError(f"BD inalcanzable: {host}")

    # Conexión exitosa
    conectar_bd("localhost")

    # Conexión fallida (comentado para no crashear el ejemplo)
    # try:
    #     conectar_bd("invalid_host")
    # except ConnectionError as e:
    #     logger.error(f"Capturado error: {e}")


# ============================================================================
# PARTE 5: Ejemplo real - Procesador de datos
# ============================================================================

def procesar_datos(numeros: list[int], logger: logging.Logger) -> dict[str, float]:
    """
    Procesa lista de números y retorna estadísticas.

    Demuestra uso de diferentes niveles de log en contexto real.

    Args:
        numeros: Lista de números a procesar
        logger: Logger para registrar eventos

    Returns:
        Dict con estadísticas (mean, min, max)

    Raises:
        ValueError: Si la lista está vacía
    """
    logger.info(f"Iniciando procesamiento de {len(numeros)} números")
    logger.debug(f"Input: {numeros}")

    # Validación
    if not numeros:
        logger.error("Lista vacía recibida")
        raise ValueError("La lista no puede estar vacía")

    # Verificar anomalías
    if len(numeros) < 3:
        logger.warning(f"Muestra pequeña: {len(numeros)} elementos")

    # Procesamiento
    logger.debug("Calculando estadísticas...")
    stats = {
        'mean': sum(numeros) / len(numeros),
        'min': min(numeros),
        'max': max(numeros),
        'count': len(numeros)
    }

    logger.debug(f"Estadísticas calculadas: {stats}")
    logger.info("Procesamiento completado exitosamente")

    return stats


def demo_ejemplo_real():
    """Demuestra uso de logging en ejemplo real."""
    print("\n" + "="*70)
    print("DEMO 5: Ejemplo real - Procesador de datos")
    print("="*70)

    logger = setup_basic_logger()

    print("\n--- Caso exitoso ---")
    datos = [10, 20, 30, 40, 50]
    resultado = procesar_datos(datos, logger)
    print(f"Resultado: {resultado}")

    print("\n--- Caso con warning (muestra pequeña) ---")
    datos_pequenos = [5, 10]
    resultado_pequeno = procesar_datos(datos_pequenos, logger)
    print(f"Resultado: {resultado_pequeno}")

    print("\n--- Caso con error (lista vacía) ---")
    try:
        procesar_datos([], logger)
    except ValueError as e:
        logger.error(f"Error capturado: {e}")
        print(f"Error esperado: {e}")


# ============================================================================
# PARTE 6: Comparación de performance - lazy evaluation
# ============================================================================

def demo_lazy_evaluation():
    """Demuestra lazy evaluation con % vs f-strings."""
    print("\n" + "="*70)
    print("DEMO 6: Performance - Lazy evaluation")
    print("="*70)

    logger = setup_basic_logger()

    # Configurar logger para que DEBUG esté desactivado
    logger.setLevel(logging.INFO)

    print("\n>>> Logger configurado con nivel INFO (DEBUG desactivado)\n")

    # Función "costosa"
    call_count = 0

    def expensive_function() -> str:
        """Simula operación costosa."""
        nonlocal call_count
        call_count += 1
        return f"resultado_{call_count}"

    # Test 1: f-string (se ejecuta siempre)
    print("--- Test 1: f-string (MALO para performance) ---")
    call_count = 0
    logger.debug(f"Resultado: {expensive_function()}")
    print(f"expensive_function() llamada {call_count} vez(ces)")
    print("^ Se ejecutó aunque DEBUG está desactivado!\n")

    # Test 2: lazy % (solo se ejecuta si es necesario)
    print("--- Test 2: lazy % (BUENO para performance) ---")
    call_count = 0
    logger.debug("Resultado: %s", expensive_function())
    print(f"expensive_function() llamada {call_count} vez(ces)")
    print("^ NO se ejecutó porque DEBUG está desactivado!\n")

    # Test 3: Con DEBUG activo (ambos se ejecutan)
    print("--- Test 3: Con DEBUG activo ---")
    logger.setLevel(logging.DEBUG)

    call_count = 0
    logger.debug(f"f-string: {expensive_function()}")
    print(f"f-string: llamadas = {call_count}")

    call_count = 0
    logger.debug("lazy %%: %s", expensive_function())
    print(f"lazy %: llamadas = {call_count}")

    print("\n>>> Conclusión: Usa % en DEBUG para evitar ejecutar código innecesario")


# ============================================================================
# PARTE 7: Tabla de decisión
# ============================================================================

def print_decision_table():
    """Imprime tabla de decisión para logging vs print vs raise."""
    print("\n" + "="*70)
    print("TABLA DE DECISIÓN: Logging vs Print vs Raise")
    print("="*70)

    table = """
┌────────────────────────────────────────────────────────────────┐
│ ¿Qué herramienta usar?                                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. ¿Es OUTPUT del programa? (resultado, respuesta)            │
│    └─> print() o return                                        │
│                                                                 │
│ 2. ¿Es información de DIAGNÓSTICO? (debugging, monitoreo)     │
│    ├─> Aplicación seria? → logging.debug()/info()             │
│    └─> Script simple? → print("DEBUG: ...")                   │
│                                                                 │
│ 3. ¿Es un ERROR?                                               │
│    ├─> ¿Puedes manejarlo aquí?                                │
│    │   ├─> SÍ → logger.warning() + return default             │
│    │   └─> NO → logger.error() + raise                        │
│    └─> ¿Es crítico para el sistema?                           │
│        └─> SÍ → logger.critical() + raise/exit()              │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│ NIVELES DE LOG:                                                │
│                                                                 │
│ DEBUG    → Variables, flujo interno (solo desarrollo)         │
│ INFO     → Eventos normales del negocio (producción)          │
│ WARNING  → Problema no crítico (funciona pero subóptimo)      │
│ ERROR    → Operación falló (recuperable)                      │
│ CRITICAL → Sistema comprometido (requiere acción inmediata)   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

EJEMPLOS:

✅ print()
   - Script que imprime resultados
   - CLI que muestra output al usuario
   - Respuesta de API (vía return, no print directo)

✅ logging.debug()
   - Valores de variables intermedias
   - Flujo de ejecución detallado
   - Query SQL generada

✅ logging.info()
   - "Usuario 123 inició sesión"
   - "Procesados 1000 registros en 2.5s"
   - "Servidor escuchando en puerto 8000"

✅ logging.warning()
   - "API respondió lento: 3s"
   - "Cache miss, consultando BD"
   - "Parámetro obsoleto usado"

✅ logging.error()
   - "No se pudo conectar a BD"
   - "Archivo no encontrado"
   - "Validación falló"

✅ logging.critical()
   - "Disco lleno"
   - "Memoria al 98%"
   - "BD principal inalcanzable"

✅ raise Exception()
   - Error que el caller DEBE manejar
   - Sistema no puede continuar
   - Después de logger.error() o logger.critical()
"""
    print(table)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta todas las demos."""
    print("\n" + "="*70)
    print(" "*15 + "EJEMPLO 04: LOGGING BÁSICO")
    print("="*70)

    # Ejecutar todas las demos
    demo_basic_logging()
    demo_log_levels()
    demo_multiple_handlers()
    demo_logging_vs_print_vs_raise()
    demo_ejemplo_real()
    demo_lazy_evaluation()
    print_decision_table()

    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print("""
✅ Has aprendido:
   1. Setup básico de logger con getLogger(__name__)
   2. Los 5 niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
   3. Múltiples handlers (consola + archivo)
   4. Formatters diferentes por handler
   5. Cuándo usar logging vs print vs raise
   6. Lazy evaluation con % para performance
   7. Tabla de decisión para elegir nivel correcto

📚 Próximo paso:
   - Ver ejemplo_05_logging_avanzado.py para:
     * RotatingFileHandler (evita archivos gigantes)
     * JSON logging (para ELK, Splunk)
     * Performance comparison (benchmarks)
     * Context managers para logging

📖 Documentación:
   - Lee 11_logging_patterns.md para más patrones
    """)


if __name__ == "__main__":
    main()
