# Guía de Instalación y Configuración

Esta guía cubre todo lo que necesitás para dejar el entorno listo antes de la primera clase. Seguí los pasos en orden: cada uno asume que el anterior fue completado correctamente.

---

## Índice

1. [Requisitos previos](#1-requisitos-previos)
2. [Instalar uv](#2-instalar-uv)
3. [Clonar el repositorio](#3-clonar-el-repositorio)
4. [Configurar variables de entorno](#4-configurar-variables-de-entorno)
5. [Instalar dependencias](#5-instalar-dependencias)
6. [Verificar la instalación](#6-verificar-la-instalación)
7. [Trabajar módulo por módulo](#7-trabajar-módulo-por-módulo)
8. [Comandos útiles por módulo](#8-comandos-útiles-por-módulo)
9. [Problemas comunes](#9-problemas-comunes)

---

## 1. Requisitos Previos

Antes de instalar cualquier cosa, verificá que tenés lo siguiente:

| Herramienta | Versión mínima | Cómo verificar |
|---|---|---|
| Python | 3.10 (recomendado 3.13) | `python --version` o `python3 --version` |
| git | cualquier versión reciente | `git --version` |
| make | cualquier versión | `make --version` |

**Sobre `make` en Windows**: no viene instalado por defecto. Las opciones son:
- Usarlo desde WSL2 (recomendado para Windows)
- Instalarlo vía [Chocolatey](https://chocolatey.org/): `choco install make`
- Si no podés instalarlo, todos los comandos `make` tienen equivalentes con `uv` que se muestran más abajo

---

## 2. Instalar `uv`

`uv` es el gestor de entornos y dependencias que usamos en todo el curso. Es significativamente más rápido que pip y garantiza reproducibilidad completa de los entornos.

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Después de instalar, cerrá y abrí una terminal nueva para que el comando `uv` sea reconocido.

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verificar instalación

```bash
uv --version
```

Deberías ver algo como `uv 0.x.x`. Si ves "command not found", abrí una terminal nueva e intentá de nuevo.

---

## 3. Clonar el Repositorio

```bash
git clone <url-del-repositorio> ai_engineering_henry
cd ai_engineering_henry
```

Si estás trabajando con un fork propio, reemplazá la URL por la de tu fork.

---

## 4. Configurar Variables de Entorno

El archivo `.env` contiene las claves de API y configuraciones sensibles. Nunca se sube al repositorio.

```bash
# Crear tu .env a partir de la plantilla
cp .env.example .env
```

Abrí el archivo `.env` con tu editor de texto y completá los valores:

```bash
# Requerido para todos los módulos que usan LLMs
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Opcionales — déjalos vacíos si no los tenés todavía
TVLY_API_KEY=
LANGCHAIN_API_KEY=
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=henry-ai-engineering
INTENT_MIN_CONFIDENCE=0.60
MAX_HISTORY_TURNS=4
```

**Importante**: `OPENAI_API_KEY` es obligatoria para cualquier notebook que haga llamadas reales al modelo. Sin ella, esos notebooks van a fallar.

### Si trabajás en módulos profundos (03-agents)

Algunos módulos buscan el `.env` dentro de su propio directorio. Si `make doctor` falla con un error de API key, copiá el archivo:

```bash
cp .env 03-agents/.env
```

---

## 5. Instalar Dependencias

### Instalación global (todos los módulos)

Desde la raíz del repositorio:

```bash
make sync
```

Esto instala las dependencias de todos los módulos. Es la opción más simple si vas a trabajar con el curso completo.

### Instalación sin `make`

```bash
uv sync --extra dev
```

---

## 6. Verificar la Instalación

Una vez instaladas las dependencias, verificá que todo funciona:

```bash
# Correr todos los tests
make test

# Revisar el estilo del código
make lint
```

Si todos los tests pasan sin errores, el entorno está listo.

### Validación por módulo

Podés validar cada módulo individualmente:

```bash
make module-01   # Módulo 01: Python, FastAPI, Prompting
make module-02   # Módulo 02: Vector Databases, Deep Learning
make module-03   # Módulo 03: Agentes, LLMops
```

---

## 7. Trabajar Módulo por Módulo

Si preferís instalar sólo el módulo que estás usando en este momento, cada uno tiene su propio `pyproject.toml`:

```bash
# Módulo 01
cd 01-Introduction_AI_Engineering
uv sync --extra dev

# Módulo 02
cd 02-vector_data_bases
uv sync --extra dev

# Módulo 03
cd 03-agents
uv sync --extra dev
```

Esta opción es útil si tenés espacio limitado en disco o querés descargas más rápidas.

---

## 8. Comandos Útiles por Módulo

### Módulo 01 — Introducción

```bash
cd 01-Introduction_AI_Engineering
make run-ai          # Ejemplo de AI Engineering
make test-all        # Tests del módulo
make run-notebooks   # Ejecutar notebooks del módulo
```

### Módulo 02 — Vector Databases

```bash
cd 02-vector_data_bases
make run-batman-module   # Caso aplicado Batman/RAG
make test                # Tests del módulo
```

### Módulo 03 — Agentes

```bash
cd 03-agents
make doctor          # Verificar configuración del entorno
make run-llmops      # Ejecutar pipeline LLMops completo
make test            # Tests del módulo
make notebooks-intro # Notebooks de fundamentos de agentes
```

---

## 9. Problemas Comunes

### `uv: command not found`

Abrí una terminal nueva después de instalar `uv`. El instalador modifica el PATH pero sólo afecta sesiones nuevas.

### `OPENAI_API_KEY no configurada`

Verificá que el archivo `.env` exista en la raíz del repositorio y que contenga una clave válida (empieza con `sk-`). Recordá también que algunos módulos necesitan que copies el `.env` a su propio directorio.

### `make: command not found`

Usá los equivalentes directos con `uv`:

```bash
# En lugar de "make sync"
uv sync --extra dev

# En lugar de "make test"
uv run python -m pytest

# En lugar de "make lint"
uv run ruff check .
```

### Un notebook no encuentra archivos relativos

Los notebooks están diseñados para ejecutarse desde el directorio del módulo al que pertenecen, no desde la raíz. Antes de ejecutar un notebook, verificá que Jupyter esté corriendo desde el directorio correcto, o usá los scripts en `tools/` o `00_tools/` que ya resuelven las rutas automáticamente.

### Error de dependencias al cambiar de módulo

Cada módulo tiene su propio entorno. Si cambiás de módulo y algo falla, corré `uv sync --extra dev` desde el directorio del módulo al que te moviste.

### El módulo de Deep Learning tarda mucho en instalar

El módulo 02 incluye PyTorch, torchvision y otras librerías pesadas. La primera instalación puede tomar varios minutos dependiendo de la velocidad de tu conexión. Es normal.
