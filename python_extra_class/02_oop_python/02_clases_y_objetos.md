# Clases y objetos

```python
class Cuenta:
    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("El balance inicial no puede ser negativo")
        self.owner = owner
        self._balance = float(balance)

    @property
    def balance(self) -> float:
        return self._balance

    def depositar(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("El depósito debe ser positivo")
        self._balance += amount

    def retirar(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("El retiro debe ser positivo")
        if amount > self._balance:
            return False
        self._balance -= amount
        return True
```

Por qué funciona:
- `__init__` construye el estado inicial.
- `depositar` y `retirar` son la API pública.
- Protegemos invariantes: balance inicial >= 0 y balance nunca puede volverse negativo.
- Exponemos `balance` como propiedad de solo lectura: puedes observar el estado sin poder romperlo desde afuera.

Uso:
```python
c = Cuenta("Luis", 100)
ok = c.retirar(30)
print(c.balance)
```
