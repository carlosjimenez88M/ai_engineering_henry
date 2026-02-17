# Encapsulamiento

Encapsular es limitar el acceso directo al estado interno.
En Python usamos una convención: `_atributo` indica uso interno.

```python
class Termometro:
    def __init__(self, celsius: float):
        self.celsius = celsius  # reusa la validación del setter

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, c: float) -> None:
        if c < -273.15:
            raise ValueError("Temperatura inválida")
        self._celsius = float(c)
```

Por qué usar un setter: así impones reglas de validez antes de cambiar el estado, y mantienes el invariante (temperatura >= cero absoluto).
