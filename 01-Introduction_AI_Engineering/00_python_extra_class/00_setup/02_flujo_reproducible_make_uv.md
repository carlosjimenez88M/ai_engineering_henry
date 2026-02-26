# Flujo reproducible con Makefile + uv

Este proyecto incluye un `Makefile` en `python_extra_class/`.

## 1. Comandos disponibles

```bash
cd python_extra_class
make help
```

## 2. Setup inicial (una vez)

```bash
make venv
make sync
```

## 3. Ciclo diario

```bash
make test
make run-pydantic
```

## 4. Ejecutar ejemplos completos

```bash
make run-examples
```

## 5. Limpiar entorno

```bash
make clean
```

## 6. Errores frecuentes y solucion

### Error: `uv no esta instalado`

Solucion: instalar uv y reabrir la terminal.

### Error: `make: command not found`

Solucion: completar modulo `00_instalar_make.md`.

### Error: dependencias faltantes

Solucion:

```bash
make sync
```

### Error en Windows por politica de PowerShell

Ejecutar PowerShell como admin y permitir scripts locales:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 7. Criterio de salida del modulo

Tu entorno esta correcto si estos comandos pasan sin errores:

```bash
make test
make run-pydantic
```
