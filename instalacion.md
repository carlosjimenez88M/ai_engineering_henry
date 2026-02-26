# Guía de Instalación del Entorno (Mac y Windows)

Para solucionar problemas de compatibilidad y dependencias cruzadas, hemos unificado todas las configuraciones en un solo archivo `pyproject.toml` en la raíz del proyecto. Este archivo funciona de la misma manera que antes pero maneja la instalación centralizada para todos los módulos de clases (Introduction, Vector Databases y Agents).

A continuación se explican los pasos de instalación utilizando [`uv`](https://github.com/astral-sh/uv), el cual es el manejador de paquetes de Python recomendado en este repositorio.

---

## 🍎 Instalación en macOS

### 1. Instalar `uv`
Si aún no tienes `uv` instalado, abre tu terminal y ejecuta:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Cierra la terminal y vuelve a abrirla (o reinicia tu sesión de zsh/bash usando `source ~/.zshrc`) para que reconozca el comando.

### 2. Sincronizar el entorno (Root del repo)
Navega a la carpeta principal (`ai_engineering_henry`) donde se encuentra el nuevo `pyproject.toml` usando tu terminal:

```bash
cd /ruta/hacia/ai_engineering_henry
```

Ejecuta el siguiente comando para crear el entorno virtual (`.venv`) e instalar absolutamente todas las dependencias del curso:

```bash
uv sync --extra dev
```

Esto generará automáticamente la carpeta `.venv` y un archivo `uv.lock`.

### 3. Activar el entorno virtual (opcional)
Con `uv` puedes correr directamente los scripts pasando `uv run python script.py` (lo cual es lo recomendado), pero si prefieres activar el entorno virtual puedes hacerlo con:

```bash
source .venv/bin/activate
```

---

## 🪟 Instalación en Windows

### 1. Requisitos previos
Ten instalada al menos una versión de Python (se recomienda >= 3.10) y el intérprete integrado de Power Shell o Git Bash.

### 2. Instalar `uv`
Abre PowerShell y corre el siguiente comando:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
*(Si ya lo ejecutaste y no se reconoce uv, reinicia tu terminal PowerShell o tu computadora).*

### 3. Sincronizar el entorno (Root del repo)
Abre PowerShell y muévete a la raíz del repositorio (`ai_engineering_henry`):

```powershell
cd C:\ruta\hacia\ai_engineering_henry
```

Instala todas dependencias de manera unificada ejecutando:

```powershell
uv sync --extra dev
```

### 4. Activar el entorno virtual (opcional)
`uv` no te exige tener activo el entorno si prefijos tus comandos con `uv run` como `uv run python script.py`. Pero si necesitas activar el `.venv` tradicional, usa:

```powershell
.venv\Scripts\activate
```

---

## 🛠 Comprobación Final

Para verificar que el entorno virtual ha sido creado exitosamente tanto en Mac como Windows, puedes correr los tests de toda la estructura escribiendo:

```bash
uv run pytest
```
**(Nota sobre variables de estado):** Recordar configurar correctamente tu archivo `.env` en la raíz (donde pusiste el token de `OPENAI_API_KEY`) ya que varios ejemplos o tests podrían depender de esto.
