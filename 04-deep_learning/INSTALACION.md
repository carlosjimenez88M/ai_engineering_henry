# Instalacion del modulo Deep Learning

## Objetivo

Dejar un entorno que funcione en macOS, Linux y Windows usando `uv`, con una ruta reproducible en CPU y una validacion real de notebooks.

## Python recomendado

- Soportado: `3.10`, `3.11`, `3.12`
- No recomendado por ahora: `3.13+`

La razon es practica: el stack de Deep Learning suele estabilizarse mas tarde que el resto del ecosistema.

## Dependencias del modulo

Se instalan desde [pyproject.toml](./pyproject.toml) e incluyen:

- `torch` y `torchvision`
- `transformers` y `sentencepiece`
- `numpy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`
- herramientas de notebooks (`jupyterlab`, `nbclient`, `nbformat`, `nbconvert`)
- testing y lint (`pytest`, `ruff`) en el extra `dev`

## Instalacion con uv

### macOS y Linux

```bash
cd 04-deep_learning
uv sync --extra dev
make doctor
make test
make corpus-check
make notebooks-smoke
```

### Windows PowerShell

```powershell
cd 04-deep_learning
uv sync --extra dev
uv run python scripts/doctor.py
uv run python -m pytest
uv run python -m tools.text_corpus
$env:HENRY_DL_SMOKE="1"
$env:HENRY_DL_ONLINE_MODE="0"
uv run python tools/execute_notebooks.py all --smoke --timeout 1200
```

## Por que la ruta base es CPU

Porque es la unica ruta que podemos asumir para una cohorte completa sin depender de:

- la misma GPU,
- la misma version de CUDA,
- los mismos drivers,
- el mismo sistema operativo.

Primero se aprende con una base estable. Luego se acelera.

## Modo smoke

Las notebooks leen `HENRY_DL_SMOKE=1` al inicio y reducen:

- epocas,
- pasos de entrenamiento,
- tamanos de batch,
- volumen de datos cuando aplica.

Ese modo existe para validar la reproducibilidad del modulo. No reemplaza la exploracion completa en clase.

## Modo online opcional

Las celdas que descargan un modelo pequeno estan protegidas por `HENRY_DL_ONLINE_MODE=1`.

- Por defecto estan desactivadas.
- No forman parte de la validacion oficial del modulo.
- Sirven para contrastar un modelo local pequeno con un modelo preentrenado mas fuerte.

## Aceleracion opcional

### macOS con Apple Silicon

PyTorch puede usar `MPS` si esta disponible:

```bash
uv run python scripts/doctor.py
```

### Windows o Linux con NVIDIA

La recomendacion docente es:

1. instalar primero la ruta base con `uv sync --extra dev`,
2. verificar que todo corre en CPU,
3. recien despues instalar la variante de PyTorch compatible con tu CUDA desde el selector oficial de PyTorch.

Asi se separan los problemas del modulo de los problemas del stack GPU.

## Problemas frecuentes

### `uv` no existe

Instalar `uv` y abrir una terminal nueva.

### `make` no existe en Windows

No es un error del modulo. En Windows la ruta oficial usa `uv run python ...`.

### `torch` no detecta GPU

La configuracion base es CPU-first. No hace falta GPU para completar el modulo.

### La instalacion tarda mucho

Es normal. `torch`, `torchvision` y `transformers` son paquetes pesados. La primera instalacion es la mas lenta.
