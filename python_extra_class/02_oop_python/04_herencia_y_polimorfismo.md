# Herencia y polimorfismo

La herencia permite reutilizar comportamiento. El polimorfismo permite tratar distintos objetos con la misma interfaz.

```python
class Animal:
    def hablar(self):
        raise NotImplementedError

class Perro(Animal):
    def hablar(self):
        return "guau"

class Gato(Animal):
    def hablar(self):
        return "miau"
```

Uso:
```python
def hacer_hablar(animal):
    return animal.hablar()
```

Por qué funciona: `hacer_hablar` solo necesita el método `hablar`; no importa la clase concreta (\"duck typing\": si camina como pato y habla como pato, sirve).
