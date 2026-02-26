# Ejercicios guiados (OOP)

## 1. Clase Temporizador
Requerimiento: iniciar, pausar, reiniciar, y leer tiempo total.

Idea: guarda `start_time`, `elapsed`, y un flag `running`. La clave es usar un reloj monotónico (no depende de cambios de hora del sistema).

Código (implementación completa):
```python
import time

class Temporizador:
    def __init__(self):
        self._running = False
        self._start = 0.0
        self._elapsed = 0.0

    def iniciar(self) -> None:
        if self._running:
            return
        self._running = True
        self._start = time.monotonic()

    def pausar(self) -> None:
        if not self._running:
            return
        now = time.monotonic()
        self._elapsed += now - self._start
        self._running = False

    def reiniciar(self) -> None:
        self._running = False
        self._start = 0.0
        self._elapsed = 0.0

    def tiempo_total(self) -> float:
        if not self._running:
            return self._elapsed
        return self._elapsed + (time.monotonic() - self._start)
```

Por qué funciona:
- Invariante: `_elapsed` siempre guarda el tiempo acumulado de periodos ya pausados.
- Si está corriendo, sumas el tramo actual (`now - _start`) sin modificar `_elapsed` (lectura sin efectos colaterales).

## 2. Clase Inventario
Requerimiento: agregar items, quitar items, y contar stock por id.

Por qué clase: concentra reglas de negocio (no dejar stock negativo) y centraliza la estructura de datos.

Código (simple y suficiente):
```python
class Inventario:
    def __init__(self):
        self._stock = {}  # item_id -> cantidad

    def agregar(self, item_id: str, cantidad: int = 1) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self._stock[item_id] = self._stock.get(item_id, 0) + cantidad

    def quitar(self, item_id: str, cantidad: int = 1) -> bool:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        actual = self._stock.get(item_id, 0)
        if cantidad > actual:
            return False
        nuevo = actual - cantidad
        if nuevo == 0:
            self._stock.pop(item_id, None)
        else:
            self._stock[item_id] = nuevo
        return True

    def stock(self, item_id: str) -> int:
        return self._stock.get(item_id, 0)
```

Por qué `dict`: lookup y actualización son O(1) promedio por `item_id`.

## 3. Clase Cola con prioridad
Requerimiento: insertar y extraer el item de mayor prioridad.

Enfoque: usa `heapq` (min-heap) y guarda prioridad negativa, o almacena tuplas `(-prioridad, item)`.

## 4. Composicion: Biblioteca y Libro
`Biblioteca` tiene muchos `Libro`.
Métodos: `agregar`, `prestar`, `devolver`.

Justificación: un libro existe fuera de la biblioteca, por eso composición.
