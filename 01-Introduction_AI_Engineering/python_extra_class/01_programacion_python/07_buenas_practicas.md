# Buenas prácticas

## 1. Nombres claros
- `total_price` es mejor que `tp`.
- Verbo para funciones: `calcular_total`.

## 2. Funciones pequeñas
Una función debe hacer una cosa bien. Si necesita "y", tal vez es muy grande.

## 3. No repetir código
Si copias y pegas algo dos veces, considera una función.

## 4. Complejidad
Antes de optimizar, mide o piensa el orden de crecimiento.

## 5. Tests mentales
Prueba con casos extremos:
- lista vacía
- un solo elemento
- valores negativos

## 6. Estilo
Sigue PEP8 para consistencia. La consistencia reduce errores.

## 7. Logging en producción

**Por qué importa:** `print()` no funciona en producción. Los logs son tu ventana al comportamiento de la aplicación en vivo.

### Usa logger, no print

```python
#  MAL: print en código de producción
def procesar_pedido(pedido_id):
    print(f"Procesando pedido {pedido_id}")  # Nadie ve esto en producción
    # ...

#  BIEN: logger configurado
import logging

logger = logging.getLogger(__name__)

def procesar_pedido(pedido_id):
    logger.info(f"Procesando pedido {pedido_id}")  # Va a archivo, monitoreo, etc.
    # ...
```

### Usa el nivel correcto

- `logger.debug()` → Solo desarrollo (detalles internos)
- `logger.info()` → Operaciones normales
- `logger.warning()` → Algo raro pero no crítico
- `logger.error()` → Error que afecta la operación
- `logger.critical()` → Error que puede parar el sistema

### No loggees información sensible

```python
#  MAL: Contraseñas en logs
logger.info(f"Usuario login: {username}, password: {password}")

#  BIEN: Solo info no sensible
logger.info(f"Usuario login exitoso: {username}")
```

### Lazy formatting con %

```python
#  BIEN: Lazy evaluation (mejor performance)
logger.debug("Procesando usuario %s con items %s", user_id, items)

#  Menos eficiente: f-strings siempre evalúan, incluso si nivel desactivado
logger.debug(f"Procesando usuario {user_id} con items {items}")
```

**Ver guía completa:** `11_logging_patterns.md`
