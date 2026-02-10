# Logging en Clases

**Por qué importa:** Las clases representan entidades complejas que necesitan logging para debuggear y monitorear. Saber dónde y cómo loggear en OOP es crucial.

**Prerrequisitos:**
- `01_programacion_python/11_logging_patterns.md` - Conceptos básicos de logging
- `02_oop_python/01_clases_y_objetos.md` - Conceptos básicos de OOP

---

## 1. Logger por Clase - El Patrón Estándar

**Por qué:** Cada clase debería tener su propio logger para saber qué clase generó cada log.

### Patrón básico

```python
import logging

class Usuario:
    """
    Clase con logging propio.

    Invariante: self.logger siempre está configurado.
    """

    def __init__(self, nombre: str, edad: int):
        # Logger con el nombre de la clase
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Creando usuario: {nombre}")

        self.nombre = nombre
        self.edad = edad

    def actualizar_edad(self, nueva_edad: int) -> None:
        """Actualiza edad con logging."""
        self.logger.debug(f"Actualizando edad de {self.nombre}: {self.edad} -> {nueva_edad}")

        if nueva_edad < 0:
            self.logger.error(f"Edad inválida: {nueva_edad}")
            raise ValueError("Edad no puede ser negativa")

        self.edad = nueva_edad
        self.logger.info(f"Edad de {self.nombre} actualizada a {nueva_edad}")
```

**Beneficio:** Los logs muestran `Usuario - Creando usuario: carlos` en vez de un log genérico.

### Logger a nivel de módulo (alternativa común)

```python
import logging

# Logger compartido por todas las clases del módulo
logger = logging.getLogger(__name__)

class Usuario:
    def __init__(self, nombre: str):
        logger.info(f"Creando usuario: {nombre}")
        self.nombre = nombre

class Administrador:
    def __init__(self, nombre: str):
        logger.info(f"Creando admin: {nombre}")
        self.nombre = nombre

# Los logs mostrarán: mymodule.Usuario - ...
```

**Trade-off:**
- Logger por instancia: Más flexible, pero más memoria si tienes miles de objetos
- Logger por módulo: Menos memoria, pero menos granular

**Recomendación:** Usa logger por módulo (`__name__`) para la mayoría de casos.

---

## 2. Logging del Ciclo de Vida

**Por qué:** Los eventos importantes del ciclo de vida (crear, modificar, destruir) deben loggearse para auditoría y debugging.

### Patrón completo

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ConexionDB:
    """
    Conexión a base de datos con logging completo del ciclo de vida.

    Invariante: Si self.conectada es True, self._conn no es None.
    """

    def __init__(self, host: str, port: int):
        logger.info(f"Inicializando conexión a {host}:{port}")
        self.host = host
        self.port = port
        self._conn = None
        self.conectada = False

    def conectar(self) -> None:
        """Establece conexión."""
        logger.debug(f"Intentando conectar a {self.host}:{port}")

        try:
            self._conn = self._establecer_conexion()
            self.conectada = True
            logger.info(f"✓ Conectado a {self.host}:{self.port}")
        except ConnectionError as e:
            logger.error(f"✗ Falló conexión a {self.host}:{self.port}: {e}")
            raise

    def desconectar(self) -> None:
        """Cierra conexión."""
        if not self.conectada:
            logger.warning("Intento de desconectar cuando no hay conexión activa")
            return

        logger.debug(f"Desconectando de {self.host}:{self.port}")
        self._conn.close()
        self.conectada = False
        logger.info(f"Desconectado de {self.host}:{self.port}")

    def __del__(self):
        """Destructor con cleanup y logging."""
        if self.conectada:
            logger.warning(f"Conexión a {self.host}:{self.port} no fue cerrada explícitamente")
            self.desconectar()
        logger.debug(f"ConexionDB a {self.host}:{self.port} destruida")
```

### Eventos a loggear

| Evento | Nivel | Ejemplo |
|--------|-------|---------|
| `__init__` (inicio) | `INFO` | "Inicializando Usuario con id=123" |
| Operación exitosa | `INFO` | "Usuario 123 actualizado" |
| Operación fallida | `ERROR` | "Falló actualización de Usuario 123" |
| Estado inconsistente | `WARNING` | "Usuario en estado inválido" |
| `__del__` (cleanup) | `DEBUG` | "Usuario 123 destruido" |
| Cleanup no hecho | `WARNING` | "Recurso no liberado explícitamente" |

---

## 3. Logging + Exceptions - Cuándo Log vs Raise

**Por qué:** No todo error necesita log Y excepción. Saber cuándo usar qué evita spam en logs.

### Árbol de decisión

```
¿Es un error?
├─ SÍ → ¿Puedes recuperarte?
│   ├─ SÍ → Log WARNING + maneja (NO raises)
│   └─ NO → ¿El caller puede manejarlo?
│       ├─ SÍ → Log ERROR + raise
│       └─ NO → Solo raise (caller loggeará)
└─ NO → ¿Es información útil?
    ├─ SÍ → Log INFO
    └─ NO → No loggees
```

### Ejemplos

#### ✅ BIEN: Log + raise para errores no recuperables

```python
class Validador:
    def validar_email(self, email: str) -> bool:
        """
        Valida formato de email.

        Raises: ValueError si formato inválido
        """
        if '@' not in email:
            logger.error(f"Email inválido: {email}")
            raise ValueError(f"Email debe contener '@': {email}")

        logger.debug(f"Email válido: {email}")
        return True
```

#### ✅ BIEN: Log warning + recupera (NO raise)

```python
class Cache:
    def obtener(self, key: str) -> Optional[str]:
        """
        Obtiene valor del cache.

        Returns: Valor o None si no existe (no lanza excepción).
        """
        try:
            valor = self._cache[key]
            logger.debug(f"Cache hit: {key}")
            return valor
        except KeyError:
            logger.warning(f"Cache miss: {key}")
            return None  # No raise, esto es esperado
```

#### ❌ MAL: Log + raise para errores esperados

```python
class Calculadora:
    def dividir(self, a: float, b: float) -> float:
        if b == 0:
            # ❌ MAL: No loggees + raises para errores esperados
            logger.error(f"División por cero: {a}/{b}")
            raise ValueError("División por cero")

        # ✅ BIEN: Solo raise, el caller decide si loggear
        if b == 0:
            raise ValueError("División por cero")

        return a / b
```

### Reglas de oro

1. **Error esperado que caller puede manejar** → Solo `raise` (sin log)
2. **Error inesperado o crítico** → `logger.error()` + `raise`
3. **Error del que te recuperas** → `logger.warning()` (sin raise)
4. **Debugging de flujo** → `logger.debug()`
5. **Nunca** → `logger.error()` sin `raise` si el error rompe la operación

---

## 4. Logger Hierarchy en Herencia

**Por qué:** Cuando usas herencia, necesitas decidir si cada clase tiene su logger o heredan.

### Opción 1: Logger por clase (recomendado)

```python
import logging

class Animal:
    def __init__(self, nombre: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Creando {self.__class__.__name__}: {nombre}")
        self.nombre = nombre

class Perro(Animal):
    def ladrar(self):
        self.logger.info(f"{self.nombre} está ladrando")

class Gato(Animal):
    def maullar(self):
        self.logger.info(f"{self.nombre} está maullando")

# Logs:
# Animal - Creando Animal: Max  (❌ no queremos esto)
# Perro - Creando Perro: Max    (✅ queremos esto)
# Perro - Max está ladrando

perro = Perro("Max")
perro.ladrar()
# INFO - Perro - Max está ladrando
```

**Por qué funciona:** `self.__class__.__name__` se resuelve a la clase concreta (`Perro`), no a la base (`Animal`).

### Opción 2: Logger por módulo (más simple)

```python
import logging

logger = logging.getLogger(__name__)

class Animal:
    def __init__(self, nombre: str):
        logger.info(f"Creando animal: {nombre}")
        self.nombre = nombre

class Perro(Animal):
    def ladrar(self):
        logger.info(f"{self.nombre} ({self.__class__.__name__}) ladra")

# Logs:
# mymodule - Creando animal: Max
# mymodule - Max (Perro) ladra
```

**Trade-off:**
- Logger por clase: Más granular, fácil de filtrar
- Logger por módulo: Más simple, menos overhead

---

## 5. Testing con Logging - caplog en pytest

**Por qué:** Necesitas verificar que tu código loggea correctamente. Pytest provee `caplog` para esto.

### Patrón de test

```python
import logging
import pytest

class Servicio:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def procesar(self, valor: int) -> int:
        if valor < 0:
            self.logger.warning(f"Valor negativo: {valor}")
            return 0

        self.logger.info(f"Procesando: {valor}")
        return valor * 2


def test_servicio_loggea_warning_con_negativo(caplog):
    """Test que verifica logging de warning."""
    servicio = Servicio()

    with caplog.at_level(logging.WARNING):
        resultado = servicio.procesar(-5)

    # Verifica el resultado
    assert resultado == 0

    # Verifica que hubo un warning
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert "Valor negativo: -5" in caplog.records[0].message


def test_servicio_loggea_info_con_positivo(caplog):
    """Test que verifica logging de info."""
    servicio = Servicio()

    with caplog.at_level(logging.INFO):
        resultado = servicio.procesar(10)

    assert resultado == 20
    assert any("Procesando: 10" in record.message for record in caplog.records)


def test_servicio_sin_errores(caplog):
    """Test que verifica que NO hay errores loggeados."""
    servicio = Servicio()

    with caplog.at_level(logging.ERROR):
        servicio.procesar(5)

    # No debe haber logs de nivel ERROR
    assert len(caplog.records) == 0
```

### Métodos útiles de caplog

```python
# Verificar que hubo logs
assert len(caplog.records) > 0

# Verificar nivel específico
assert caplog.records[0].levelname == "ERROR"

# Verificar mensaje contiene texto
assert "usuario no encontrado" in caplog.text

# Verificar múltiples logs
assert len([r for r in caplog.records if r.levelname == "WARNING"]) == 2

# Limpiar logs entre tests
caplog.clear()
```

---

## 6. Patrones Avanzados

### Pattern 1: Contexto en cada log

```python
class Usuario:
    def __init__(self, user_id: int, nombre: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.user_id = user_id
        self.nombre = nombre

    def _log(self, level: int, mensaje: str) -> None:
        """Helper que agrega contexto automáticamente."""
        self.logger.log(
            level,
            f"[Usuario {self.user_id}] {mensaje}"
        )

    def actualizar(self, datos: dict) -> None:
        self._log(logging.INFO, f"Actualizando con {len(datos)} campos")
        # ... lógica de actualización
        self._log(logging.INFO, "Actualización completada")

# Todos los logs tendrán: [Usuario 123] ...
```

### Pattern 2: Logger como dependency injection

```python
class Servicio:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Acepta logger externo para testing.

        Args:
            logger: Logger personalizado, o None para usar el default
        """
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def procesar(self, datos):
        self.logger.info("Procesando datos")
        # ...

# En producción
servicio = Servicio()

# En tests (con logger mock)
logger_mock = logging.getLogger("test")
servicio = Servicio(logger=logger_mock)
```

---

## Resumen: Checklist de Logging en OOP

Cuando escribes una clase, pregúntate:

- [ ] ¿Tiene logger? → `self.logger = logging.getLogger(__name__)`
- [ ] ¿Loggeo __init__? → `logger.info(f"Creando {self.__class__.__name__}")`
- [ ] ¿Loggeo operaciones importantes? → `logger.info("Operación X completada")`
- [ ] ¿Loggeo errores antes de raise? → `logger.error(...)` + `raise`
- [ ] ¿Tengo tests de logging? → Usa `caplog` en pytest
- [ ] ¿Hay cleanup en __del__? → `logger.debug("Destruyendo...")`
- [ ] ¿Evito log spam? → Solo loggeo eventos útiles

---

**Ver también:**
- `01_programacion_python/11_logging_patterns.md` - Logging patterns completos
- `04_ejemplos_runnable/ejemplo_04_logging_basico.py` - Ejemplos ejecutables
- `GUIA_DE_DECISIONES.md` - Cuándo usar qué nivel de log
