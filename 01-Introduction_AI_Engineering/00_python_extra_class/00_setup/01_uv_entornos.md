# Crear y usar entornos con uv

`uv` simplifica manejo de entorno virtual y dependencias.

## 1. Instalar uv

### macOS y Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

## 2. Verificar instalacion

```bash
uv --version
```

## 3. Crear entorno virtual del modulo

Desde `python_extra_class/`:

```bash
uv venv
```

Esto crea `.venv/` local.

## 4. Activar entorno (opcional)

No es obligatorio si usas `uv run`, pero sirve para debug manual.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

## 5. Instalar dependencias

Con `pyproject.toml`:

```bash
uv sync
```

Compatibilidad legacy con `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

## 6. Ejecutar comandos sin activar entorno

```bash
uv run pytest -q
uv run python 04_ejemplos_runnable/ejemplo_07_pydantic_ai.py
```

`uv run` usa el entorno del proyecto automaticamente.
