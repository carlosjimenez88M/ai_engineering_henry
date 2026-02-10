# Módulos y archivos

## 1. Importar
```python
import math
print(math.sqrt(16))
```

Usa módulos para no reescribir código probado.

## 2. Crear tu módulo
Archivo `utils.py`:
```python
def clamp(x, lo, hi):
    return max(lo, min(hi, x))
```

Uso:
```python
from utils import clamp
print(clamp(10, 0, 5))
```

## 3. Lectura de archivos
```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

`with` asegura que el archivo se cierre incluso si hay error.

## 4. Escritura de archivos
```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("Hola\n")
```

## 5. Un archivo puede ser modulo y script
Esto evita ejecutar código al importar:
```python
def main():
    print("Ejecutando como script")

if __name__ == "__main__":
    main()
```
