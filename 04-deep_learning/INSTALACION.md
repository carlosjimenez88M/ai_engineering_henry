# Instalacion del modulo Deep Learning

## Objetivo

Dejar un entorno que funcione en macOS, Linux y Windows usando `uv`, con una ruta reproducible en CPU y una validacion real de notebooks.

## Python recomendado

- Soportado: `3.11`, `3.12`, `3.13`
- Minimo requerido: `3.11`

PyTorch 2.5+ incluye wheels oficiales para Python 3.11, 3.12 y 3.13.

## Dependencias del modulo

Se instalan desde [pyproject.toml](./pyproject.toml) e incluyen:

- `torch>=2.5.0` y `torchvision>=0.20.0`
- `transformers` y `sentencepiece`
- `numpy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`
- herramientas de notebooks (`jupyterlab`, `nbclient`, `nbformat`, `nbconvert`)
- testing y lint (`pytest`, `ruff`) en el extra `dev`

## Instalacion con uv

### macOS y Linux

```bash
cd 04-deep_learning
make sync
```

`make sync` hace tres cosas en orden:
1. Instala todas las dependencias con `uv sync --extra dev`
2. Instala el paquete `tools` en modo editable (necesario para que los notebooks importen `from tools.notebook_utils import ...`)
3. Registra el kernel `henry-deep-learning` en Jupyter con `ipykernel install --user`

Luego verificar que todo funciona:

```bash
make doctor
make test
make corpus-check
make notebooks-smoke
```

### Verificar que el kernel aparece en JupyterLab

Despues de `make sync`, el kernel debe aparecer como **"Henry Deep Learning"** en la barra de seleccion de kernel de JupyterLab.

Para confirmar desde la terminal:

```bash
jupyter kernelspec list
```

Debe aparecer una linea como:

```
henry-deep-learning   /Users/<tu-usuario>/Library/Jupyter/kernels/henry-deep-learning
```

Si ya tienes JupyterLab abierto cuando corres `make sync`, **reinicia el servidor de JupyterLab** para que detecte el nuevo kernel.

Si el kernel no aparece despues de reiniciar, ejecuta:

```bash
make kernel
```

Eso re-registra el kernel sin reinstalar las dependencias.

### Windows PowerShell

```powershell
cd 04-deep_learning
uv sync --extra dev
.venv\Scripts\python -m ipykernel install --user --name henry-deep-learning --display-name "Henry Deep Learning"
```

Verificar:

```powershell
jupyter kernelspec list
uv run python scripts/doctor.py
uv run python -m pytest
uv run python -m tools.text_corpus
$env:HENRY_DL_SMOKE="1"
$env:HENRY_DL_ONLINE_MODE="0"
uv run python tools/execute_notebooks.py all --smoke --timeout 1200
```

## Como funciona el kernel

`ipykernel install --user` crea un spec en:

- macOS: `~/Library/Jupyter/kernels/henry-deep-learning/`
- Linux: `~/.local/share/jupyter/kernels/henry-deep-learning/`
- Windows: `%APPDATA%\jupyter\kernels\henry-deep-learning\`

El archivo `kernel.json` dentro apunta al Python del `.venv` local, por lo que
JupyterLab usa exactamente el entorno instalado con `uv`, sin importar desde donde
se abra el servidor.

## Por que no hay `sys.path.append` en las notebooks

El paquete `tools` se instala como parte del proyecto cuando ejecutas `make sync`.
Con `package = true` en `pyproject.toml`, uv instala el proyecto en modo editable,
por lo que `from tools.notebook_utils import ...` funciona directamente sin
manipular `sys.path`.

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

PyTorch detecta MPS automaticamente. Para verificar:

```bash
make doctor
```

### Windows o Linux con NVIDIA

La recomendacion docente es:

1. instalar primero la ruta base con `make sync`,
2. verificar que todo corre en CPU con `make doctor`,
3. recien despues instalar la variante de PyTorch compatible con tu CUDA desde el selector oficial de PyTorch.

Asi se separan los problemas del modulo de los problemas del stack GPU.

## Problemas frecuentes

### El kernel "Henry Deep Learning" no aparece en JupyterLab

1. Verificar que `make sync` termino sin errores
2. Ejecutar `jupyter kernelspec list` para confirmar que el kernel esta registrado
3. Si esta registrado pero no aparece: reiniciar el servidor de JupyterLab
4. Si no esta registrado: correr `make kernel`

### `uv` no existe

Instalar `uv` y abrir una terminal nueva:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### `make` no existe en Windows

No es un error del modulo. En Windows la ruta oficial usa los comandos de `uv run python ...` listados en la seccion de Windows.

### `torch` no detecta GPU

La configuracion base es CPU-first. No hace falta GPU para completar el modulo.

### La instalacion tarda mucho

Es normal. `torch`, `torchvision` y `transformers` son paquetes pesados. La primera instalacion es la mas lenta.
