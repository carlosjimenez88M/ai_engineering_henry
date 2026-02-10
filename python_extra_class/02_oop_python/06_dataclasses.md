# Dataclasses

Cuando una clase es solo datos con pocas reglas, una dataclass es ideal.

```python
from dataclasses import dataclass

@dataclass
class Punto:
    x: float
    y: float
```

Beneficios:
- `__init__` automático
- `__repr__` legible

Si necesitas validaciones complejas, vuelve a una clase normal.

Tip: si quieres inmutabilidad (como una tupla con nombres):
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Punto:
    x: float
    y: float
```
