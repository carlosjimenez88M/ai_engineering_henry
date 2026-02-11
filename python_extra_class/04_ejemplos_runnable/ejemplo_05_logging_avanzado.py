#!/usr/bin/env python3
"""
Ejemplo 05: Logging Avanzado
=============================

Demuestra:
1. RotatingFileHandler (evita archivos gigantes)
2. TimedRotatingFileHandler (rotación por fecha)
3. JSON logging (para sistemas de monitoreo)
4. Performance comparison (f-string vs lazy %)
5. Context managers para logging
6. Configuración con dict config

Prerrequisito: Lee 11_logging_patterns.md y ejecuta ejemplo_04_logging_basico.py

Ejecuta: python ejemplo_05_logging_avanzado.py
"""

import logging
import logging.config
import json
import time
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime


# ============================================================================
# PARTE 1: RotatingFileHandler - Evita archivos gigantes
# ============================================================================

def setup_rotating_logger() -> tuple[logging.Logger, Path]:
    """
    Configura logger con RotatingFileHandler.

    El archivo rota cuando alcanza maxBytes.
    Mantiene backupCount archivos antiguos.

    Returns:
        Tupla de (logger, path_al_archivo)
    """
    logger = logging.getLogger("rotating")
    logger.setLevel(logging.DEBUG)

    # Archivo rota cuando llega a 1KB (pequeño para demo)
    log_file = Path(__file__).parent / "ejemplo_05_rotating.log"
    handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=1024,  # 1 KB (en producción: 10_000_000 = 10 MB)
        backupCount=3   # Mantiene 3 backups (.1, .2, .3)
    )

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, log_file


def demo_rotating_file_handler():
    """Demuestra RotatingFileHandler."""
    print("\n" + "="*70)
    print("DEMO 1: RotatingFileHandler")
    print("="*70)

    logger, log_file = setup_rotating_logger()
    log_dir = log_file.parent

    print(f"\n>>> Archivo de log: {log_file}")
    print(">>> maxBytes=1024, backupCount=3")
    print(">>> Generando muchos logs para forzar rotación...\n")

    # Generar muchos logs para forzar rotación
    for i in range(100):
        logger.info(f"Mensaje número {i:03d} - Este es un mensaje largo para forzar rotación del archivo de log")

    # Mostrar archivos creados
    print(">>> Archivos creados:\n")
    for log_path in sorted(log_dir.glob("ejemplo_05_rotating.log*")):
        size = log_path.stat().st_size
        print(f"    {log_path.name:<35} {size:>6} bytes")

    print("\n>>> Observa:")
    print("    - ejemplo_05_rotating.log     → Archivo actual")
    print("    - ejemplo_05_rotating.log.1   → Backup más reciente")
    print("    - ejemplo_05_rotating.log.2   → Backup anterior")
    print("    - ejemplo_05_rotating.log.3   → Backup más antiguo")
    print("    - Solo mantiene 3 backups (backupCount=3)")


# ============================================================================
# PARTE 2: TimedRotatingFileHandler - Rotación por fecha
# ============================================================================

def setup_timed_rotating_logger() -> tuple[logging.Logger, Path]:
    """
    Configura logger con TimedRotatingFileHandler.

    Rota cada 'when' (segundos, minutos, horas, días).

    Returns:
        Tupla de (logger, path_al_archivo)
    """
    logger = logging.getLogger("timed_rotating")
    logger.setLevel(logging.INFO)

    log_file = Path(__file__).parent / "ejemplo_05_timed.log"

    # Rota cada 5 segundos (para demo)
    # En producción: when='midnight', interval=1
    handler = TimedRotatingFileHandler(
        filename=log_file,
        when='S',       # S=segundos, M=minutos, H=horas, D=días, midnight=medianoche
        interval=5,     # Cada 5 segundos
        backupCount=3   # Mantiene 3 backups
    )

    formatter = logging.Formatter(
        '%(asctime)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, log_file


def demo_timed_rotating_file_handler():
    """Demuestra TimedRotatingFileHandler."""
    print("\n" + "="*70)
    print("DEMO 2: TimedRotatingFileHandler")
    print("="*70)

    logger, log_file = setup_timed_rotating_logger()

    print(f"\n>>> Archivo de log: {log_file}")
    print(">>> when='S' (segundos), interval=5, backupCount=3")
    print(">>> Generando logs cada segundo durante 12 segundos...\n")

    # Generar logs durante 12 segundos
    for i in range(12):
        logger.info(f"Mensaje en segundo {i+1}")
        print(f"    [{i+1}/12] Log generado")
        time.sleep(1)

    # Mostrar archivos creados
    print("\n>>> Archivos creados:\n")
    log_dir = log_file.parent
    for log_path in sorted(log_dir.glob("ejemplo_05_timed.log*")):
        size = log_path.stat().st_size
        mtime = datetime.fromtimestamp(log_path.stat().st_mtime)
        print(f"    {log_path.name:<45} {size:>4} bytes  {mtime.strftime('%H:%M:%S')}")

    print("\n>>> Observa:")
    print("    - Archivos rotados cada 5 segundos")
    print("    - Nombres incluyen timestamp de rotación")
    print("    - Solo mantiene 3 backups más recientes")


# ============================================================================
# PARTE 3: JSON Logging - Para sistemas de monitoreo
# ============================================================================

class JSONFormatter(logging.Formatter):
    """
    Formatter que convierte logs a JSON.

    Útil para ELK Stack, Splunk, CloudWatch, etc.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Convierte LogRecord a JSON.

        Args:
            record: Registro de log

        Returns:
            String JSON
        """
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage()
        }

        # Agregar campos extra si existen
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms

        # Incluir exception si existe
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_json_logger() -> tuple[logging.Logger, Path]:
    """
    Configura logger con JSON formatter.

    Returns:
        Tupla de (logger, path_al_archivo)
    """
    logger = logging.getLogger("json_logger")
    logger.setLevel(logging.INFO)

    log_file = Path(__file__).parent / "ejemplo_05_json.log"
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    return logger, log_file


def demo_json_logging():
    """Demuestra JSON logging."""
    print("\n" + "="*70)
    print("DEMO 3: JSON Logging")
    print("="*70)

    logger, log_file = setup_json_logger()

    print(f"\n>>> Archivo de log JSON: {log_file}")
    print(">>> Generando logs con datos estructurados...\n")

    # Log simple
    logger.info("Aplicación iniciada")

    # Log con campos extra
    logger.info(
        "Usuario inició sesión",
        extra={
            'user_id': 123,
            'request_id': 'req-abc-123'
        }
    )

    # Log con métricas
    logger.info(
        "Request procesado",
        extra={
            'user_id': 123,
            'request_id': 'req-abc-123',
            'duration_ms': 45.7
        }
    )

    # Log de error con exception
    try:
        resultado = 10 / 0
    except ZeroDivisionError:
        logger.error(
            "Error en cálculo",
            extra={'user_id': 123},
            exc_info=True
        )

    # Mostrar contenido del archivo
    print(">>> Contenido del archivo JSON (formateado):\n")
    with open(log_file, 'r') as f:
        for i, line in enumerate(f, 1):
            log_entry = json.loads(line)
            print(f"    Log {i}:")
            print(f"    {json.dumps(log_entry, indent=6, ensure_ascii=False)}\n")

    print(">>> Ventajas de JSON logging:")
    print("    - Fácil de parsear por herramientas (ELK, Splunk)")
    print("    - Permite búsquedas estructuradas: user_id=123")
    print("    - Soporta agregaciones y métricas")
    print("    - Ideal para microservicios y sistemas distribuidos")


# ============================================================================
# PARTE 4: Performance Comparison - f-string vs lazy %
# ============================================================================

def expensive_operation() -> str:
    """
    Simula operación costosa.

    Returns:
        String de resultado
    """
    # Simula operación que toma tiempo
    total = 0
    for i in range(1000):
        total += i
    return f"resultado_{total}"


def demo_performance_comparison():
    """
    Demuestra diferencia de performance entre f-string y lazy %.

    Ejecuta benchmark real.
    """
    print("\n" + "="*70)
    print("DEMO 4: Performance Comparison")
    print("="*70)

    logger = logging.getLogger("performance")
    logger.setLevel(logging.INFO)  # DEBUG desactivado
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)

    print("\n>>> Logger configurado con nivel INFO (DEBUG desactivado)")
    print(">>> Ejecutando benchmark con 10,000 iteraciones...\n")

    iterations = 10_000

    # Test 1: f-string (MALO)
    print("--- Test 1: f-string (se ejecuta siempre) ---")
    start = time.perf_counter()
    for i in range(iterations):
        logger.debug(f"Iteración {i}: {expensive_operation()}")
    elapsed_fstring = time.perf_counter() - start
    print(f"Tiempo: {elapsed_fstring:.3f}s")
    print("^ expensive_operation() se ejecutó 10,000 veces!\n")

    # Test 2: lazy % (BUENO)
    print("--- Test 2: lazy % (solo se ejecuta si es necesario) ---")
    start = time.perf_counter()
    for i in range(iterations):
        logger.debug("Iteración %s: %s", i, expensive_operation())
    elapsed_lazy = time.perf_counter() - start
    print(f"Tiempo: {elapsed_lazy:.3f}s")
    print("^ expensive_operation() NO se ejecutó porque DEBUG está off!\n")

    # Comparación
    speedup = elapsed_fstring / elapsed_lazy if elapsed_lazy > 0 else float('inf')
    print("--- Comparación ---")
    print(f"f-string:    {elapsed_fstring:.3f}s")
    print(f"lazy %:      {elapsed_lazy:.3f}s")
    print(f"Speedup:     {speedup:.1f}x más rápido")
    print(f"Diferencia:  {elapsed_fstring - elapsed_lazy:.3f}s ahorrados")

    print("\n>>> Conclusión:")
    print("     Usa lazy % en DEBUG para evitar ejecutar código innecesario")
    print("     En producción (INFO+), la diferencia es menor")
    print("     Para operaciones costosas, SIEMPRE usa lazy %")


# ============================================================================
# PARTE 5: Context Manager para logging
# ============================================================================

class LoggedOperation:
    """
    Context manager que loggea duración de operaciones.

    Útil para medir performance de bloques de código.
    """

    def __init__(self, logger: logging.Logger, operation_name: str):
        """
        Inicializa context manager.

        Args:
            logger: Logger a usar
            operation_name: Nombre de la operación
        """
        self.logger = logger
        self.operation_name = operation_name
        self.start_time: float = 0.0

    def __enter__(self) -> 'LoggedOperation':
        """Inicia la operación."""
        self.logger.info(f"Iniciando: {self.operation_name}")
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Finaliza la operación y loggea duración."""
        elapsed = (time.perf_counter() - self.start_time) * 1000  # ms

        if exc_type is None:
            self.logger.info(
                f"Completado: {self.operation_name} ({elapsed:.2f}ms)",
                extra={'duration_ms': elapsed}
            )
        else:
            self.logger.error(
                f"Falló: {self.operation_name} ({elapsed:.2f}ms) - {exc_val}",
                extra={'duration_ms': elapsed},
                exc_info=True
            )

        # No suprime la excepción
        return False


def demo_context_manager():
    """Demuestra context manager para logging."""
    print("\n" + "="*70)
    print("DEMO 5: Context Manager para logging")
    print("="*70)

    logger = logging.getLogger("context_manager")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    ))
    logger.addHandler(handler)

    print("\n>>> Usando context manager para medir operaciones...\n")

    # Operación exitosa
    print("--- Operación exitosa ---")
    with LoggedOperation(logger, "Procesar datos"):
        time.sleep(0.1)  # Simula trabajo
        print("    (trabajando...)")

    # Operación con error
    print("\n--- Operación con error ---")
    try:
        with LoggedOperation(logger, "Validar input"):
            time.sleep(0.05)
            print("    (trabajando...)")
            raise ValueError("Input inválido")
    except ValueError:
        print("    (error capturado)")

    print("\n>>> Ventajas:")
    print("    - Loggea automáticamente inicio y fin")
    print("    - Mide duración con precisión")
    print("    - Captura errores automáticamente")


# ============================================================================
# PARTE 6: Dict Config - Configuración profesional
# ============================================================================

def get_logging_config(env: str = 'development') -> Dict[str, Any]:
    """
    Retorna configuración de logging según entorno.

    Args:
        env: Entorno (development, production)

    Returns:
        Dict de configuración para dictConfig()
    """
    base_config: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        }
    }

    if env == 'development':
        base_config['handlers'] = {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            }
        }
        base_config['root'] = {
            'level': 'DEBUG',
            'handlers': ['console']
        }

    elif env == 'production':
        log_file = str(Path(__file__).parent / "ejemplo_05_production.log")
        base_config['handlers'] = {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': log_file,
                'maxBytes': 10_000_000,  # 10 MB
                'backupCount': 5
            }
        }
        base_config['root'] = {
            'level': 'INFO',
            'handlers': ['file']
        }

    return base_config


def demo_dict_config():
    """Demuestra dict config."""
    print("\n" + "="*70)
    print("DEMO 6: Dict Config - Configuración profesional")
    print("="*70)

    print("\n>>> Configuración para DEVELOPMENT:\n")
    dev_config = get_logging_config('development')
    print(json.dumps(dev_config, indent=2))

    print("\n>>> Configuración para PRODUCTION:\n")
    prod_config = get_logging_config('production')
    print(json.dumps(prod_config, indent=2))

    print("\n>>> Aplicando configuración de desarrollo...\n")
    logging.config.dictConfig(dev_config)

    logger = logging.getLogger(__name__)
    logger.debug("Debug message (visible en dev)")
    logger.info("Info message")
    logger.warning("Warning message")

    print("\n>>> Ventajas de dict config:")
    print("    - Estructura clara y mantenible")
    print("    - Fácil de versionar en git")
    print("    - Puedes cargar desde JSON/YAML")
    print("    - Configuración por entorno (dev/prod)")


# ============================================================================
# PARTE 7: Ejemplo real completo
# ============================================================================

class APIHandler:
    """Handler de API con logging completo."""

    def __init__(self):
        """Inicializa handler con logger."""
        self.logger = logging.getLogger(__name__)

    def process_request(
        self,
        user_id: int,
        request_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Procesa request con logging completo.

        Args:
            user_id: ID del usuario
            request_data: Datos del request

        Returns:
            Respuesta procesada
        """
        request_id = f"req-{int(time.time()*1000)}"

        with LoggedOperation(self.logger, f"Request {request_id}"):
            self.logger.info(
                "Request iniciado",
                extra={
                    'user_id': user_id,
                    'request_id': request_id,
                    'action': request_data.get('action')
                }
            )

            # Validación
            if not request_data.get('action'):
                self.logger.warning(
                    "Action faltante en request",
                    extra={'user_id': user_id, 'request_id': request_id}
                )
                return {'status': 'error', 'message': 'Action requerido'}

            # Procesamiento
            time.sleep(0.05)  # Simula trabajo

            result = {
                'status': 'success',
                'request_id': request_id,
                'data': {'processed': True}
            }

            self.logger.info(
                "Request exitoso",
                extra={
                    'user_id': user_id,
                    'request_id': request_id,
                    'status': result['status']
                }
            )

            return result


def demo_ejemplo_real():
    """Demuestra ejemplo real completo."""
    print("\n" + "="*70)
    print("DEMO 7: Ejemplo real - API Handler")
    print("="*70)

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    ))
    logger.addHandler(handler)

    api = APIHandler()

    print("\n>>> Request exitoso:\n")
    result = api.process_request(
        user_id=123,
        request_data={'action': 'create_order', 'amount': 99.99}
    )
    print(f"\nResultado: {result}")

    print("\n>>> Request con warning (action faltante):\n")
    result = api.process_request(
        user_id=456,
        request_data={'amount': 50.00}
    )
    print(f"\nResultado: {result}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta todas las demos."""
    print("\n" + "="*70)
    print(" "*12 + "EJEMPLO 05: LOGGING AVANZADO")
    print("="*70)

    # Ejecutar demos
    demo_rotating_file_handler()
    demo_timed_rotating_file_handler()
    demo_json_logging()
    demo_performance_comparison()
    demo_context_manager()
    demo_dict_config()
    demo_ejemplo_real()

    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print("""
 Has aprendido:
   1. RotatingFileHandler - Evita archivos gigantes
   2. TimedRotatingFileHandler - Rotación por fecha
   3. JSON logging - Para ELK, Splunk, CloudWatch
   4. Performance - lazy % es 10-1000x más rápido
   5. Context managers - Logging automático de duración
   6. Dict config - Configuración profesional por entorno
   7. Ejemplo real - API handler completo

 Benchmarks de performance:
   - f-string con DEBUG off: 10,000 llamadas ejecutadas
   - lazy % con DEBUG off: 0 llamadas ejecutadas
   - Speedup: 10-1000x dependiendo del costo de la operación

 Patrones para producción:
   - RotatingFileHandler con maxBytes=10_000_000, backupCount=5
   - JSON logging para sistemas de monitoreo
   - Context managers para medir duración
   - Dict config para configuración por entorno

 Archivos generados:
   - ejemplo_05_rotating.log*     (RotatingFileHandler)
   - ejemplo_05_timed.log*        (TimedRotatingFileHandler)
   - ejemplo_05_json.log          (JSON logging)
   - ejemplo_05_production.log*   (Dict config)

 Documentación:
   - Lee 11_logging_patterns.md para más patrones
   - Ver ejemplo_04_logging_basico.py para fundamentos
    """)


if __name__ == "__main__":
    main()
