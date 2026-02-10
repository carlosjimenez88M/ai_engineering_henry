# Diseño y criterios

## 1. Responsabilidad única
Una clase debe tener una sola razón para cambiar.

## 2. API pequeña
Mientras menos métodos públicos, más fácil es usarla sin errores.

## 3. Invariantes
Define reglas que siempre deben cumplirse y asegúralas en los métodos.

## 4. Evita getters y setters innecesarios
Si solo exponen datos sin reglas, considera una dataclass.

## 5. Testea comportamiento, no implementación
Prueba el resultado esperado, no los detalles internos.
