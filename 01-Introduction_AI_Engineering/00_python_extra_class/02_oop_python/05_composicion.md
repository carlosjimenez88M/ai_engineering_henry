# Composición

Preferir composición sobre herencia cuando una clase "tiene" otras, no "es" otra.

```python
class Motor:
    def encender(self):
        return "motor encendido"

class Auto:
    def __init__(self):
        self.motor = Motor()

    def arrancar(self):
        return self.motor.encender()
```

Por qué es mejor aquí: un auto no es un motor, pero contiene uno.
