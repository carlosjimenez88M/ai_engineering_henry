# Ejemplos Ejecutables - Python Extra Class

Este directorio contiene ejemplos completamente ejecutables para todos los temas avanzados del curso.

**Filosofía:** Código ejecutable > texto. Todos estos archivos se pueden correr directamente y ver el output.

---

## 📁 Archivos disponibles

### 🔴 Excepciones y Manejo de Errores

**`ejemplo_01_excepciones.py`**
- Try/except/else/finally con flujo completo
- Jerarquía de excepciones personalizadas
- Exception chaining (`raise from`)
- LBYL vs EAFP con medición de performance
- Captura específica vs genérica

**Ejecutar:**
```bash
python ejemplo_01_excepciones.py
```

**`ejemplo_02_context_managers.py`**
- Context managers con `__enter__`/`__exit__`
- TemporaryState para modificaciones reversibles
- Manejo de archivos con `with`
- Transacciones de base de datos simuladas
- Decorador `@contextmanager`

**Ejecutar:**
```bash
python ejemplo_02_context_managers.py
```

---

### 🔄 Generadores e Iteradores

**`ejemplo_03_generadores.py`**
- File reader generator para archivos grandes
- Data transformation pipeline (filter → map → reduce)
- Fibonacci infinite sequence
- Comparación de memoria: list vs generator
- Performance benchmarks

**Ejecutar:**
```bash
python ejemplo_03_generadores.py
```

---

### 📝 Logging

**`ejemplo_04_logging_basico.py`**
- Configuración básica de logger
- Los 5 niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Múltiples handlers (consola + archivo)
- Formatters con timestamp, nivel, mensaje

**Ejecutar:**
```bash
python ejemplo_04_logging_basico.py
```

**Output esperado:**
- Logs en consola con colores
- Archivo `app.log` creado con todos los logs

**`ejemplo_05_logging_avanzado.py`**
- RotatingFileHandler para rotación automática
- Structured logging (JSON format)
- Performance: lazy vs eager evaluation
- Ejemplo real: API client con logging completo

**Ejecutar:**
```bash
python ejemplo_05_logging_avanzado.py
```

**Output esperado:**
- Múltiples archivos de log rotados
- `structured.log` con formato JSON
- Mediciones de performance

---

### 🔁 List Comprehension vs For Loops

**`ejemplo_06_comprehension_performance.py`**
- Performance tests con diferentes tamaños (10, 100, 1000, 10000)
- Bytecode comparison usando `dis` module
- Memory profiling
- Ejemplos de comprehensions legibles vs ilegibles

**Ejecutar:**
```bash
python ejemplo_06_comprehension_performance.py
```

**Output esperado:**
- Tabla de comparación de tiempos
- Análisis de bytecode
- Recomendaciones basadas en datos

---

## 🚀 Cómo usar estos ejemplos

### Ejecución individual

```bash
# Navega al directorio del curso
cd python_extra_class

# Ejecuta cualquier ejemplo
python 04_ejemplos_runnable/ejemplo_01_excepciones.py
python 04_ejemplos_runnable/ejemplo_02_context_managers.py
# etc.
```

### Verificar que todos funcionan

```bash
# Ejecuta todos los ejemplos en secuencia
for file in 04_ejemplos_runnable/ejemplo_*.py; do
    echo "=== Ejecutando $file ==="
    python "$file"
    echo ""
done
```

### Testing

Algunos ejemplos tienen tests asociados:

```bash
pytest 04_ejemplos_runnable/test_ejemplos.py -v
```

---

## 📊 Qué esperar de cada ejemplo

### Nivel de output

| Archivo | Output | Archivos creados | Duración |
|---------|--------|------------------|----------|
| ejemplo_01 | ✅ Verbose, educativo | Ninguno | ~1s |
| ejemplo_02 | ✅ Verbose, educativo | `/tmp/test_*.txt` (temp) | ~2s |
| ejemplo_03 | ✅ Verbose con benchmarks | `/tmp/large_dataset.txt` (temp) | ~3s |
| ejemplo_04 | ✅ Logs en consola | `app.log`, `debug.log`, `error.log` | ~1s |
| ejemplo_05 | ✅ Logs + benchmarks | `app.log.*`, `structured.log` | ~2s |
| ejemplo_06 | ✅ Tablas de performance | Ninguno | ~5s |

### Limpieza después de ejecutar

Los ejemplos crean archivos de log temporales. Para limpiarlos:

```bash
# Desde el directorio python_extra_class
rm -f *.log *.log.* /tmp/test_*.txt /tmp/large_dataset.txt
```

---

## 🎯 Estructura de cada ejemplo

Todos los archivos siguen este patrón:

```python
"""
Título del Ejemplo
==================

Descripción breve de qué demuestra.
"""

# Imports
import logging
from typing import ...

# Definiciones de clases/funciones
class MiClase:
    """Docstring explicativo."""
    pass

def mi_funcion():
    """Docstring explicativo."""
    pass

# Sección ejecutable
if __name__ == "__main__":
    print("=" * 70)
    print("TÍTULO DEL EJEMPLO")
    print("=" * 70)

    # Ejemplo 1
    print("\nEjemplo 1: ...")
    ...

    # Ejemplo 2
    print("\nEjemplo 2: ...")
    ...

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
```

---

## 🔧 Troubleshooting

### Problema: "ModuleNotFoundError"

```bash
# Asegúrate de estar en el directorio correcto
cd python_extra_class

# O usa path absoluto
python 04_ejemplos_runnable/ejemplo_01_excepciones.py
```

### Problema: "PermissionError" al crear archivos log

```bash
# Verifica permisos del directorio
ls -la 04_ejemplos_runnable/

# O ejecuta desde otro directorio con permisos
cd /tmp
python /ruta/completa/ejemplo_04_logging_basico.py
```

### Problema: Output no se ve

Algunos ejemplos usan logging que puede no aparecer en consola. Verifica los archivos `.log` creados.

---

## 📚 Relación con el material teórico

| Ejemplo | Guía teórica |
|---------|--------------|
| ejemplo_01 | `01_programacion_python/08_excepciones_avanzadas.md` |
| ejemplo_02 | `01_programacion_python/08_excepciones_avanzadas.md` (Sección 2) |
| ejemplo_03 | `01_programacion_python/09_generadores_e_iteradores.md` |
| ejemplo_04 | `01_programacion_python/11_logging_patterns.md` |
| ejemplo_05 | `01_programacion_python/11_logging_patterns.md` (avanzado) |
| ejemplo_06 | `01_programacion_python/10_comprension_vs_loops.md` |

**Recomendación:** Lee la guía teórica primero, luego ejecuta el ejemplo correspondiente.

---

## 💡 Tips para aprovechar estos ejemplos

1. **Ejecútalos primero sin modificar** - Ve el output esperado
2. **Lee el código con comentarios** - Cada sección está documentada
3. **Modifica y experimenta** - Cambia valores, rompe cosas, aprende
4. **Compara con la teoría** - Conecta el código con los conceptos
5. **Usa como plantillas** - Copia patrones para tus proyectos

---

## ✅ Checklist de verificación

Para confirmar que todo está funcionando:

- [ ] Todos los ejemplos se ejecutan sin errores
- [ ] Los logs se crean en el directorio actual
- [ ] El output es legible y educativo
- [ ] Puedes modificar y re-ejecutar sin problemas
- [ ] Los benchmarks muestran números razonables

---

**Última actualización:** 2026-02
**Mantenedor:** Python Extra Class

Para más información, consulta el `README.md` principal del curso.
