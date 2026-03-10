# Instalacion y prerequisitos

## 1. Requisitos minimos

- Python `3.10+`
- `uv`
- `git`
- API key de OpenAI para notebooks con llamadas reales
- `make` recomendado en macOS/Linux

## 2. Instalar `uv`

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 3. Clonar el repo y crear entorno

```bash
git clone <tu-fork-o-este-repo>
cd ai_engineering_henry
cp .env.example .env
uv sync --extra dev
```

Si usas `make`:

```bash
make sync
```

## 4. Configurar variables de entorno

Edita `.env` en la raiz:

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

Variables opcionales:

```bash
TVLY_API_KEY=
LANGCHAIN_API_KEY=
LANGCHAIN_TRACING_V2=
LANGCHAIN_PROJECT=henry-ai-engineering
INTENT_MIN_CONFIDENCE=0.60
MAX_HISTORY_TURNS=4
```

Si vas a usar `make doctor` dentro de `03-agents/`, copia tambien el archivo:

```bash
cp .env 03-agents/.env
```

## 5. Verificar que todo quedo bien

Desde la raiz:

```bash
make test
make lint
```

Validaciones por modulo:

```bash
make module-01
make module-02
make module-03
```

## 5.1 Instalacion por modulo

Si quieres trabajar por partes, cada modulo principal ya tiene su propio `pyproject.toml`:

```bash
cd 01-Introduction_AI_Engineering
uv sync --extra dev

cd ../02-vector_data_bases
uv sync --extra dev

cd ../03-agents
uv sync --extra dev

cd ../04-deep_learning
uv sync --extra dev
```

## 6. Comandos utiles por modulo

### Fundamentos

```bash
cd 01-Introduction_AI_Engineering
make run-ai
make test-all
```

### Vector databases

```bash
cd 02-vector_data_bases
make run-batman-module
```

### Agentes

```bash
cd 03-agents
make doctor
make run-llmops
```

### Deep Learning

```bash
cd 04-deep_learning
make doctor
make test
```

## 7. Problemas comunes

### `uv: command not found`

Abre una terminal nueva despues de instalar `uv`.

### `OPENAI_API_KEY no esta configurado`

Verifica que `.env` exista y contenga una clave valida.

### `make: command not found`

Usa los comandos equivalentes con `uv`:

```bash
uv sync --extra dev
uv run python -m pytest
uv run ruff check .
```

### Un notebook no encuentra archivos relativos

Ejecutalo desde el directorio del modulo o usa los scripts en `tools/` / `00_tools/`, que ya estan preparados para resolver rutas del curso.
