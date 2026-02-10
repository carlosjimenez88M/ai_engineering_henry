# Logging Patterns

**Por qué importa:** En producción, `print()` no sirve. Los logs son tu única visibilidad sobre qué está pasando en sistemas reales. Dominar logging es la diferencia entre debuggear por horas o encontrar el problema en minutos.

**Código ejecutable:** Ver `04_ejemplos_runnable/ejemplo_04_logging_basico.py` y `ejemplo_05_logging_avanzado.py`

---

## 1. Por qué logging (no print) - Necesidades de producción

### El problema con print()

```python
# ❌ Código con prints (amateur)
def procesar_pedido(pedido_id: int) -> bool:
    print(f"Procesando pedido {pedido_id}")

    if not validar_stock(pedido_id):
        print("Error: sin stock")  # ¿Dónde va este mensaje?
        return False

    print("Pedido procesado")  # ¿Cómo lo desactivas en producción?
    return True
```

**Problemas:**
- ❌ No puedes desactivar prints sin eliminar código
- ❌ No puedes guardar en archivo
- ❌ No puedes filtrar por severidad
- ❌ No incluye timestamp automático
- ❌ No puedes enviar a sistemas de monitoreo
- ❌ Se mezcla con output real del programa

### La solución: logging

```python
# ✅ Código con logging (profesional)
import logging

logger = logging.getLogger(__name__)

def procesar_pedido(pedido_id: int) -> bool:
    logger.info(f"Procesando pedido {pedido_id}")

    if not validar_stock(pedido_id):
        logger.error(f"Pedido {pedido_id}: sin stock")
        return False

    logger.info(f"Pedido {pedido_id} procesado exitosamente")
    return True
```

**Ventajas:**
- ✅ Controlas nivel de detalle (DEBUG, INFO, ERROR)
- ✅ Guardas automáticamente en archivos
- ✅ Incluye timestamp, módulo, línea
- ✅ Puedes enviar a Sentry, CloudWatch, etc.
- ✅ No interfiere con output del programa

### Decisión: ¿Cuándo usar qué?

| Contexto | Herramienta | Por qué |
|----------|-------------|---------|
| Script de una sola vez | `print()` | Simple, rápido, temporal |
| Debugging local | `print()` con "DEBUG:" | Fácil de encontrar y eliminar |
| Aplicación en desarrollo | `logging.DEBUG` | Puedes desactivar sin eliminar |
| Aplicación en producción | `logging.INFO/ERROR` | Monitoreo, auditoría, debugging remoto |
| Biblioteca/módulo | `logging.getLogger(__name__)` | El usuario controla los logs |

---

## 2. Basic Setup - Logger vs Root Logger

### Root Logger (Simple pero limitado)

```python
import logging

# Configuración global (afecta todo el programa)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Usa el root logger
logging.info("Aplicación iniciada")  # ✅ Funciona
logging.debug("Cargando config")     # ❌ No se muestra (nivel = INFO)
```

**Cuándo usar:**
- Scripts simples
- Prototipado rápido
- Aplicaciones de un solo archivo

**Limitaciones:**
- Solo puedes configurar una vez
- No puedes tener diferentes niveles por módulo
- Difícil de controlar en aplicaciones grandes

### Named Logger (Profesional y flexible)

```python
import logging

# Cada módulo tiene su propio logger
logger = logging.getLogger(__name__)  # __name__ = nombre del módulo

def procesar_datos(datos: list[int]) -> int:
    logger.debug(f"Entrada: {datos}")  # Control fino por módulo
    resultado = sum(datos)
    logger.info(f"Procesados {len(datos)} elementos")
    return resultado
```

**Por qué `__name__`:**
- `__name__` = `"mi_modulo"` → logger se llama `"mi_modulo"`
- Jerárquico: `"api.usuarios"` hereda config de `"api"`
- Puedes controlar nivel por módulo:
  ```python
  logging.getLogger("api.usuarios").setLevel(logging.DEBUG)
  logging.getLogger("api.pedidos").setLevel(logging.INFO)
  ```

### Patrón recomendado

```python
# mi_modulo.py
import logging

# SIEMPRE al inicio del módulo
logger = logging.getLogger(__name__)

def funcion():
    logger.info("Haciendo algo")  # ✅ Usa el logger del módulo
```

**Regla de oro:** Usa `getLogger(__name__)` en TODAS tus aplicaciones serias. Es el estándar de la industria.

---

## 3. Log Levels - CUÁNDO usar cada uno

### Los 5 niveles (de menos a más severo)

| Nivel | Valor numérico | Cuándo usar | Visible en producción |
|-------|----------------|-------------|----------------------|
| `DEBUG` | 10 | Información detallada para debugging | ❌ NO |
| `INFO` | 20 | Confirmación de que todo funciona | ✅ SÍ |
| `WARNING` | 30 | Algo inesperado pero no crítico | ✅ SÍ |
| `ERROR` | 40 | Error que impide una operación | ✅ SÍ |
| `CRITICAL` | 50 | Error que puede detener la aplicación | ✅ SÍ |

### Tabla de decisión: ¿Qué nivel usar?

```
┌─────────────────────────────────────────────────────────────────────┐
│ ¿La operación falló?                                                │
│ ├─ NO → ¿Es información de diagnóstico detallada?                  │
│ │   ├─ SÍ → DEBUG                                                   │
│ │   └─ NO → ¿Es un evento normal del flujo?                        │
│ │       ├─ SÍ → INFO                                                │
│ │       └─ NO → ¿Es algo inusual pero no rompe nada?              │
│ │           └─ SÍ → WARNING                                         │
│ └─ SÍ → ¿El programa puede continuar?                              │
│     ├─ SÍ → ERROR                                                   │
│     └─ NO → CRITICAL                                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Ejemplos de cada nivel

#### DEBUG - Información de diagnóstico

```python
logger.debug(f"Variables: x={x}, y={y}, resultado={resultado}")
logger.debug(f"Query SQL: {query}")
logger.debug(f"Headers HTTP: {headers}")
logger.debug(f"Entrando a función procesar() con args={args}")
```

**Cuándo:** Variables intermedias, estado interno, flujo de ejecución detallado.

**Por qué DEBUG no ERROR:** Esta información NO indica un problema, solo ayuda a entender el flujo.

#### INFO - Eventos normales del negocio

```python
logger.info(f"Usuario {user_id} inició sesión")
logger.info(f"Procesados {n} pedidos en {elapsed}s")
logger.info(f"Servidor escuchando en puerto {port}")
logger.info(f"Backup completado: {backup_path}")
```

**Cuándo:** Confirmación de operaciones exitosas, métricas, eventos del negocio.

**Por qué INFO no DEBUG:** Esto es información valiosa incluso en producción.

#### WARNING - Problemas no críticos

```python
logger.warning(f"API respondió lento: {elapsed}s (límite: 2s)")
logger.warning(f"Cache miss para key={key}, consultando BD")
logger.warning(f"Parámetro obsoleto '{old_param}', usa '{new_param}'")
logger.warning(f"Disco al 85% de capacidad")
```

**Cuándo:**
- Operación exitosa pero subóptima
- Configuración obsoleta pero funcional
- Recursos cerca del límite

**Por qué WARNING no ERROR:** El programa FUNCIONA, solo advierte de algo.

#### ERROR - Operación falló

```python
logger.error(f"No se pudo conectar a BD: {e}")
logger.error(f"Archivo no encontrado: {filepath}")
logger.error(f"Validación falló para usuario {user_id}: {validation_errors}")
logger.error(f"Timeout en API externa después de {retries} reintentos")
```

**Cuándo:**
- Una operación específica falló
- Se puede recuperar o continuar con otras tareas
- El error debe investigarse

**Por qué ERROR no CRITICAL:** El sistema SIGUE funcionando para otras operaciones.

#### CRITICAL - Sistema comprometido

```python
logger.critical("No hay espacio en disco, deteniendo escrituras")
logger.critical("Memoria al 98%, posible crash inminente")
logger.critical(f"BD principal inalcanzable: {e}")
logger.critical("Corrupción detectada en archivo de configuración")
```

**Cuándo:**
- El sistema completo está comprometido
- Requiere intervención inmediata
- Puede resultar en shutdown

**Por qué CRITICAL no ERROR:** No es una operación que falló, es el SISTEMA que está en peligro.

### Ejemplo completo con todos los niveles

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def procesar_pago(user_id: int, monto: float) -> Optional[str]:
    """
    Procesa un pago y retorna transaction_id o None si falla.
    """
    logger.debug(f"procesar_pago() llamado con user_id={user_id}, monto={monto}")

    # Validación
    if monto <= 0:
        logger.error(f"Monto inválido: {monto} para user_id={user_id}")
        return None

    logger.info(f"Procesando pago de ${monto} para usuario {user_id}")

    try:
        # Verificar saldo
        saldo = get_saldo(user_id)
        logger.debug(f"Saldo actual: ${saldo}")

        if saldo < monto:
            logger.warning(f"Saldo insuficiente para user_id={user_id}: {saldo} < {monto}")
            return None

        # Llamar API de pago
        transaction_id = payment_api.charge(user_id, monto)
        logger.info(f"Pago exitoso: transaction_id={transaction_id}, user_id={user_id}")

        return transaction_id

    except PaymentAPITimeout as e:
        logger.error(f"Timeout en API de pagos: {e}")
        return None

    except DatabaseConnectionError as e:
        logger.critical(f"BD de pagos inalcanzable: {e}")
        raise  # Re-raise porque es crítico
```

---

## 4. Formatters - Timestamp, Module, Level, Message

### Formato básico

```python
import logging

logging.basicConfig(
    format='%(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Hola")
# Output: INFO - Hola
```

### Atributos de formato disponibles

| Atributo | Descripción | Ejemplo |
|----------|-------------|---------|
| `%(asctime)s` | Timestamp | `2026-02-10 14:30:15,234` |
| `%(levelname)s` | Nivel (INFO, ERROR) | `ERROR` |
| `%(name)s` | Nombre del logger | `api.usuarios` |
| `%(module)s` | Módulo Python | `usuarios` |
| `%(funcName)s` | Nombre de función | `procesar_pedido` |
| `%(lineno)d` | Línea de código | `42` |
| `%(message)s` | Mensaje del log | `Usuario creado` |
| `%(pathname)s` | Path completo del archivo | `/app/api/usuarios.py` |
| `%(process)d` | Process ID | `12345` |
| `%(thread)d` | Thread ID | `67890` |

### Formatos recomendados por contexto

#### Desarrollo (verbose, fácil de leer)

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Output:
# 2026-02-10 14:30:15 - api.usuarios - INFO - Usuario 123 creado
```

#### Producción (incluye módulo y línea para debugging)

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Output:
# 2026-02-10 14:30:15 | INFO     | api.usuarios:42 | Usuario 123 creado
```

**Nota:** `%(levelname)-8s` alinea a la izquierda con 8 caracteres (para que quede `INFO    ` y `ERROR   `).

#### Microservicios (incluye process/thread para concurrencia)

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(process)d | %(thread)d | %(levelname)s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Output:
# 2026-02-10 14:30:15 | 12345 | 67890 | INFO | api.usuarios | Request procesado
```

### Personalización avanzada: Formatters custom

```python
import logging

class ColoredFormatter(logging.Formatter):
    """Formatter con colores para desarrollo."""

    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

# Uso
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
logger.addHandler(handler)
```

---

## 5. Handlers - Console, File, RotatingFileHandler

### ¿Qué son los Handlers?

Un **handler** determina DÓNDE van los logs (consola, archivo, red, etc).

**Regla:** Puedes tener múltiples handlers en el mismo logger.

### Console Handler (para desarrollo)

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logger.addHandler(console_handler)

logger.info("Esto va a la consola")
```

### File Handler (para producción)

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler para archivo
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s'
))

logger.addHandler(file_handler)

logger.info("Esto va al archivo app.log")
```

### RotatingFileHandler (evita archivos enormes)

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

# Archivo rota cuando llega a 10MB, mantiene 5 backups
handler = RotatingFileHandler(
    'app.log',
    maxBytes=10_000_000,  # 10 MB
    backupCount=5          # app.log.1, app.log.2, ..., app.log.5
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s'
))

logger.addHandler(handler)

# Cuando app.log llega a 10MB:
# 1. app.log → app.log.1
# 2. Nuevo app.log se crea
# 3. app.log.5 se elimina (solo mantiene 5)
```

**Cuándo usar:** SIEMPRE en producción. Sin esto, el archivo crece indefinidamente.

### TimedRotatingFileHandler (rota por fecha)

```python
import logging
from logging.handlers import TimedRotatingFileHandler

# Rota cada día a medianoche, mantiene 30 días
handler = TimedRotatingFileHandler(
    'app.log',
    when='midnight',
    interval=1,
    backupCount=30
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s'
))

logger.addHandler(handler)

# Archivos generados:
# - app.log (hoy)
# - app.log.2026-02-09
# - app.log.2026-02-08
# - ...
```

**Opciones de `when`:**
- `'S'` - Segundos
- `'M'` - Minutos
- `'H'` - Horas
- `'D'` - Días
- `'midnight'` - A medianoche
- `'W0'-'W6'` - Día de la semana (0=Lunes)

### Patrón: Múltiples handlers (consola + archivo)

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    """Configura logger con consola (DEBUG) y archivo (INFO)."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Handler 1: Consola (todo)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    ))

    # Handler 2: Archivo (solo INFO+)
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=10_000_000,
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
    ))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Uso
logger = setup_logger(__name__)
logger.debug("Esto solo va a consola")     # Solo consola
logger.info("Esto va a consola Y archivo") # Ambos
```

**Por qué funciona:** Desarrollo ve todo (DEBUG en consola), producción solo guarda lo importante (INFO+ en archivo).

---

## 6. Configuration Patterns - Dict Config, File Config, Code

### Opción 1: Código (simple, limitado)

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

**Pros:** Simple, rápido.
**Contras:** No puedes cambiar sin reiniciar, difícil de mantener.

### Opción 2: Archivo INI (legado, poco usado)

```ini
# logging.ini
[loggers]
keys=root,api

[handlers]
keys=console,file

[formatters]
keys=simple,detailed

[logger_root]
level=INFO
handlers=console,file

[logger_api]
level=DEBUG
handlers=console
qualname=api
propagate=0

[handler_console]
class=StreamHandler
level=DEBUG
formatter=simple
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=INFO
formatter=detailed
args=('app.log', 'a')

[formatter_simple]
format=%(levelname)s - %(message)s

[formatter_detailed]
format=%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s
```

```python
import logging.config

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)
```

**Pros:** Configuración externa.
**Contras:** Sintaxis verbosa, poco flexible.

### Opción 3: Dict Config (RECOMENDADO)

```python
import logging.config
from typing import Dict, Any

LOGGING_CONFIG: Dict[str, Any] = {
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
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': 'app.log',
            'maxBytes': 10_000_000,
            'backupCount': 5
        }
    },

    'loggers': {
        'api': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    },

    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

# Aplicar configuración
logging.config.dictConfig(LOGGING_CONFIG)

# Uso
logger = logging.getLogger('api')
logger.info("Configuración aplicada")
```

**Pros:**
- ✅ Estructura clara (Python dict)
- ✅ Fácil de versionar (código)
- ✅ Puedes cargar desde JSON/YAML
- ✅ Flexible y potente

### Opción 4: YAML Config (MEJOR para producción)

```yaml
# logging.yaml
version: 1
disable_existing_loggers: false

formatters:
  simple:
    format: '%(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'

handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: detailed
    filename: app.log
    maxBytes: 10000000
    backupCount: 5

loggers:
  api:
    level: DEBUG
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console, file]
```

```python
import logging.config
import yaml

with open('logging.yaml', 'r') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
```

**Pros:**
- ✅ Más legible que INI
- ✅ Puedes cambiar sin tocar código
- ✅ Fácil de mantener

**Contras:**
- ❌ Requiere PyYAML (`pip install pyyaml`)

### Patrón recomendado: Config por entorno

```python
import logging.config
import os
from typing import Dict, Any

def get_logging_config(env: str = 'development') -> Dict[str, Any]:
    """Retorna configuración de logging según entorno."""

    base_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
            }
        }
    }

    if env == 'development':
        base_config['handlers'] = {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple'
            }
        }
        base_config['root'] = {
            'level': 'DEBUG',
            'handlers': ['console']
        }

    elif env == 'production':
        base_config['handlers'] = {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': '/var/log/app/app.log',
                'maxBytes': 50_000_000,
                'backupCount': 10
            }
        }
        base_config['root'] = {
            'level': 'INFO',
            'handlers': ['file']
        }

    return base_config

# Uso
env = os.getenv('ENV', 'development')
logging.config.dictConfig(get_logging_config(env))
logger = logging.getLogger(__name__)
```

---

## 7. Structured Logging - JSON Logs

### Por qué JSON logs

**Problema con logs de texto:**
```
2026-02-10 14:30:15 | INFO | Usuario 123 inició sesión desde IP 192.168.1.1
```

Para buscar "todos los logins del usuario 123" necesitas regex. Para agregaciones (¿cuántos logins por hora?) necesitas parsear texto.

**Solución: JSON logs**
```json
{
  "timestamp": "2026-02-10T14:30:15.234Z",
  "level": "INFO",
  "logger": "api.auth",
  "message": "Usuario inició sesión",
  "user_id": 123,
  "ip": "192.168.1.1",
  "session_duration_ms": 450
}
```

Ahora puedes:
- Buscar: `user_id == 123`
- Agregar: `SELECT COUNT(*) GROUP BY hour(timestamp)`
- Alertar: `ip NOT IN whitelist`

### Implementación con python-json-logger

```bash
pip install python-json-logger
```

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)

# Handler con JSON formatter
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(timestamp)s %(level)s %(name)s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Logs simples
logger.info("Usuario creado")
# Output: {"timestamp": "2026-02-10T14:30:15.234Z", "level": "INFO", ...}

# Logs con datos estructurados
logger.info(
    "Pago procesado",
    extra={
        'user_id': 123,
        'amount': 99.99,
        'currency': 'USD',
        'transaction_id': 'tx_abc123'
    }
)
# Output: {..., "user_id": 123, "amount": 99.99, ...}
```

### Implementación manual (sin dependencias)

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any

class JSONFormatter(logging.Formatter):
    """Formatter que convierte logs a JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Agregar campos extra
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id

        # Incluir exception si existe
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data)

# Uso
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Log con campos custom
logger.info("Pedido creado", extra={'user_id': 123, 'order_id': 456})
```

### Patrón: Context logger (para requests)

```python
import logging
from typing import Optional
from contextvars import ContextVar

# Variable de contexto para request_id
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)

class RequestContextFilter(logging.Filter):
    """Agrega request_id a todos los logs."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get() or 'no-request'
        return True

# Setup
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
handler.addFilter(RequestContextFilter())
logger.addHandler(handler)

# Uso en request handler
def handle_request(request):
    request_id = request.headers.get('X-Request-ID', generate_id())
    request_id_var.set(request_id)

    logger.info("Request iniciado")  # Incluye request_id automáticamente
    process_request(request)
    logger.info("Request completado")  # Incluye el mismo request_id
```

### Cuándo usar JSON logs

| Contexto | JSON? | Por qué |
|----------|-------|---------|
| Desarrollo local | ❌ NO | Texto es más fácil de leer |
| Scripts simples | ❌ NO | Overhead innecesario |
| Producción con ELK/Splunk | ✅ SÍ | Permite búsquedas y agregaciones |
| Microservicios | ✅ SÍ | Permite tracing distribuido |
| Aplicaciones con métricas | ✅ SÍ | Fácil extraer datos |

---

## 8. Performance - Lazy Evaluation con %

### El problema: String formatting costoso

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ❌ MAL: Se ejecuta incluso si DEBUG está desactivado
logger.debug(f"Datos: {expensive_function()}")
# expensive_function() SE EJECUTA SIEMPRE, aunque el log no se muestre

# ❌ MAL: Se construye el string siempre
logger.debug(f"Usuario: {user.to_dict()}")
# user.to_dict() se ejecuta incluso si DEBUG está off
```

**Problema:** El f-string se evalúa ANTES de que logging decida si mostrar el mensaje.

### La solución: Lazy evaluation con %

```python
# ✅ BIEN: Solo se evalúa si el log va a mostrarse
logger.debug("Datos: %s", expensive_function())
# expensive_function() SOLO se ejecuta si DEBUG está activo

# ✅ BIEN: Lazy evaluation
logger.debug("Usuario: %s", user.to_dict())
# user.to_dict() solo se llama si DEBUG está activo
```

**Cómo funciona:**
1. logging recibe: `"Datos: %s"` y `expensive_function` (sin ejecutar)
2. logging verifica: ¿DEBUG está activo?
3. Si NO → descarta sin ejecutar `expensive_function()`
4. Si SÍ → ejecuta `expensive_function()` y formatea

### Benchmark de performance

```python
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # DEBUG desactivado

def slow_operation():
    time.sleep(0.1)
    return "resultado"

# Test 1: f-string (MALO)
start = time.time()
for _ in range(100):
    logger.debug(f"Resultado: {slow_operation()}")  # ❌ 10 segundos
print(f"f-string: {time.time() - start:.2f}s")

# Test 2: lazy % (BUENO)
start = time.time()
for _ in range(100):
    logger.debug("Resultado: %s", slow_operation())  # ✅ ~0 segundos
print(f"lazy %: {time.time() - start:.2f}s")
```

**Resultado:**
- f-string: 10 segundos (ejecuta slow_operation() 100 veces)
- lazy %: ~0 segundos (no ejecuta slow_operation() porque DEBUG está off)

### Reglas de performance

| Caso | Usa | Ejemplo |
|------|-----|---------|
| Variables simples | Cualquiera | `logger.info(f"x={x}")` está ok |
| Función costosa | `%` o `lazy=True` | `logger.debug("Data: %s", expensive())` |
| Conversión (dict, json) | `%` | `logger.debug("User: %s", user.to_dict())` |
| Nivel INFO+ en prod | Cualquiera | Siempre se ejecuta de todos modos |

### Caso especial: isEnabledFor()

```python
# Cuando tienes MUCHA lógica de debug
if logger.isEnabledFor(logging.DEBUG):
    # Solo ejecuta este bloque si DEBUG está activo
    data = expensive_computation()
    formatted = complex_formatting(data)
    logger.debug(f"Resultado complejo: {formatted}")
```

**Cuándo usar:** Solo si el formateo en sí es costoso (bucles, conversiones pesadas).

---

## 9. Anti-patterns - Qué evitar

### ❌ Anti-pattern 1: Logging dentro de loops

```python
# ❌ MAL: 10,000 logs
for i in range(10000):
    logger.debug(f"Procesando item {i}")
    process_item(i)

# ✅ BIEN: Log por batch
logger.info(f"Procesando {len(items)} items...")
for i, item in enumerate(items):
    process_item(item)
    if i % 1000 == 0:
        logger.info(f"Progreso: {i}/{len(items)}")
logger.info("Procesamiento completado")
```

### ❌ Anti-pattern 2: Logging información sensible

```python
# ❌ MAL: Expone credenciales
logger.info(f"Conectando con user={user}, password={password}")

# ❌ MAL: Expone PII (Personally Identifiable Information)
logger.info(f"Usuario: {user.email}, SSN: {user.ssn}")

# ✅ BIEN: Sanitiza datos sensibles
logger.info(f"Conectando con user={user}")
logger.info(f"Usuario: {user.id}, email={mask_email(user.email)}")
```

### ❌ Anti-pattern 3: Exception swallowing

```python
# ❌ MAL: Captura y solo logguea
try:
    critical_operation()
except Exception as e:
    logger.error(f"Error: {e}")
    # ¡No hace nada más!

# ✅ BIEN: Logguea Y re-raise si es crítico
try:
    critical_operation()
except ValueError as e:
    logger.warning(f"Input inválido: {e}")
    return None  # Esperado, maneja gracefully
except Exception as e:
    logger.error(f"Error crítico: {e}", exc_info=True)
    raise  # Re-lanza para que el caller maneje
```

**Nota:** `exc_info=True` incluye el traceback completo en el log.

### ❌ Anti-pattern 4: Logging sin contexto

```python
# ❌ MAL: ¿Qué falló?
logger.error("Error en validación")

# ✅ BIEN: Contexto completo
logger.error(
    f"Validación falló para usuario {user_id}: {validation_errors}",
    extra={'user_id': user_id, 'errors': validation_errors}
)
```

### ❌ Anti-pattern 5: Level incorrecto

```python
# ❌ MAL: Usar ERROR para algo que no es error
if cache_miss:
    logger.error("Cache miss")  # No es error, es normal

# ✅ BIEN: Usa el nivel apropiado
if cache_miss:
    logger.debug("Cache miss, consultando BD")
```

### ❌ Anti-pattern 6: Logging + print

```python
# ❌ MAL: Mezcla logging y print
logger.info("Iniciando proceso")
print("Procesando...")  # ¿Por qué?
logger.info("Proceso completado")

# ✅ BIEN: Solo logging
logger.info("Iniciando proceso")
logger.info("Procesando...")
logger.info("Proceso completado")
```

### ❌ Anti-pattern 7: No configurar nivel

```python
# ❌ MAL: No configuras nivel, defaults a WARNING
logger = logging.getLogger(__name__)
logger.info("Esto no se muestra")  # ¡No verás nada!

# ✅ BIEN: Siempre configura nivel
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # O usa logging.basicConfig()
logger.info("Esto sí se muestra")
```

### ❌ Anti-pattern 8: Logging en hot path

```python
# ❌ MAL: Logging en función llamada millones de veces
def calculate_distance(x1, y1, x2, y2):
    logger.debug(f"Calculando distancia: ({x1},{y1}) -> ({x2},{y2})")
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

# ✅ BIEN: Solo loggea resumen
def process_points(points):
    logger.info(f"Calculando distancias para {len(points)} puntos")
    distances = [calculate_distance(*p) for p in points]
    logger.info(f"Distancia promedio: {sum(distances)/len(distances):.2f}")
    return distances
```

---

## Tabla de decisión: Logging vs Print vs Raise

```
┌─────────────────────────────────────────────────────────────────────┐
│ ¿Es parte de la funcionalidad del programa (output esperado)?      │
│ ├─ SÍ → print() o return (no es log)                               │
│ │   Ejemplo: Script que imprime resultados, CLI output             │
│ │                                                                    │
│ └─ NO → ¿Es para debugging o monitoreo?                            │
│     ├─ SÍ → ¿Estás en una aplicación seria?                        │
│     │   ├─ SÍ → logging                                             │
│     │   └─ NO → print("DEBUG: ...")                                │
│     │                                                                │
│     └─ NO → ¿Algo salió mal?                                       │
│         ├─ ¿Es un error que el caller debe manejar?               │
│         │   └─ SÍ → raise Exception()                              │
│         │                                                            │
│         └─ ¿Es un error que puedes recuperar?                     │
│             ├─ SÍ → logger.warning() y continúa                    │
│             └─ NO → logger.error() y raise o return None          │
└─────────────────────────────────────────────────────────────────────┘
```

### Flowchart visual

```
START: Quiero comunicar algo
│
├─ ¿Es output del programa? (resultado del script, respuesta API)
│  └─ SÍ → print() o return
│
├─ ¿Es información de diagnóstico? (debugging, monitoreo)
│  └─ SÍ → ¿Es aplicación seria (producción, librería)?
│     ├─ SÍ → logging.debug()/info()
│     └─ NO → print("DEBUG: ...")
│
└─ ¿Es un error?
   ├─ ¿Puedes manejarlo aquí?
   │  ├─ SÍ → logger.warning() + return valor_por_defecto
   │  └─ NO → logger.error() + raise
   │
   └─ ¿Es crítico para el sistema?
      └─ SÍ → logger.critical() + raise o exit()
```

### Ejemplos concretos

#### Caso 1: Script que calcula estadísticas

```python
# ✅ CORRECTO
def main():
    logger.info("Cargando datos...")  # Logging (diagnóstico)
    data = load_data()

    logger.debug(f"Datos cargados: {len(data)} registros")  # Logging
    stats = calculate_stats(data)

    print(json.dumps(stats, indent=2))  # Print (output esperado)

# Output:
# (stderr) 2026-02-10 14:30:15 - INFO - Cargando datos...
# (stdout) {"mean": 42.5, "median": 40, ...}
```

#### Caso 2: Validación de input

```python
# ✅ CORRECTO
def procesar_pedido(pedido_id: int) -> Optional[dict]:
    logger.info(f"Procesando pedido {pedido_id}")  # Logging (monitoreo)

    if not validar_pedido(pedido_id):
        logger.warning(f"Pedido {pedido_id} inválido")  # Logging
        return None  # Return (no es excepcional, es esperado)

    return ejecutar_pedido(pedido_id)
```

#### Caso 3: Error fatal

```python
# ✅ CORRECTO
def conectar_bd(config: dict) -> Connection:
    logger.info("Conectando a BD...")  # Logging

    try:
        conn = create_connection(config)
        return conn
    except ConnectionError as e:
        logger.critical(f"No se puede conectar a BD: {e}")  # Logging
        raise  # Raise (caller DEBE saber que falló)
```

---

## Resumen: Guía rápida de decisiones

### ¿Qué nivel usar?

```python
logger.debug("Variable x=%s", x)           # Solo desarrollo, detalles
logger.info("Pedido %s procesado", id)     # Eventos normales del negocio
logger.warning("API lenta: %ss", time)     # Problema no crítico
logger.error("Validación falló: %s", err)  # Operación falló
logger.critical("BD inalcanzable")         # Sistema comprometido
```

### ¿Qué configuración usar?

```python
# Desarrollo
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

# Producción
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('app.log', maxBytes=10_000_000, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s'))
logger.addHandler(handler)
```

### ¿Cuándo usar qué?

| Necesidad | Herramienta |
|-----------|-------------|
| Script simple | `print("DEBUG: ...")` |
| Aplicación seria | `logging.getLogger(__name__)` |
| Output del programa | `print()` o `return` |
| Error recoverable | `logger.warning()` + `return None` |
| Error fatal | `logger.error()` + `raise` |
| Performance crítica | `logger.debug("msg: %s", expensive())` |
| Producción | RotatingFileHandler + JSON logs |

---

**Siguiente:**
- **Código ejecutable:** `04_ejemplos_runnable/ejemplo_04_logging_basico.py`
- **Código ejecutable:** `04_ejemplos_runnable/ejemplo_05_logging_avanzado.py`
- **Temas relacionados:** `05_errores_y_debug.md`, `08_excepciones_avanzadas.md`
