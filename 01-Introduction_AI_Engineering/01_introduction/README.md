# Clase 01: Software Engineering vs AI Engineering

Esta clase compara ambos enfoques con ejemplos ejecutables y una guía práctica de decisión. El proyecto incluye un caso de estudio funcional (`brief_builder`) que demuestra principios de AI Engineering aplicados en una arquitectura modular, observable y resiliente.

## Inicio Rápido

### 1. Preparar el entorno

Primero, crea un archivo `.env` en la raíz del repositorio:

```bash
cp .env.example .env
# Edita .env y agrega tu clave de OpenAI:
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4o-mini  # opcional
```

### 2. Instalar dependencias

```bash
uv sync  # O usa: make install
```

Esto instala todas las dependencias definidas en `pyproject.toml`, incluyendo OpenAI SDK, pytest, coverage y herramientas de linting.

### 3. Verificar instalación

```bash
make test-se   # Prueba el ejemplo de Software Engineering
make test-ai   # Prueba el módulo de AI Engineering
```

## Comandos disponibles

Ejecutar desde la raíz del repo:

```bash
# Instalar dependencias
make install

# Ejecutar ejemplos
make run-se                                      # Ejecuta el ejemplo SE
make run-ai                                      # Ejecuta brief_builder con config por defecto
make run-ai-context CONTEXT="Startup B2B, 24/7" # Brief con contexto personalizado
make run-ai-model MODEL=gpt-4o                  # Usa modelo diferente

# Testing y cobertura
make test-se                                     # Tests del ejemplo SE
make test-ai                                     # Tests de brief_builder con salida verbose
make test-ai-cov                                 # Tests con reporte HTML de cobertura
make test-all                                    # Todos los tests

# Calidad de código
make lint                                        # Ruff check
make format                                      # Ruff format
make check                                       # Compilación de módulos
make clean                                       # Limpiar __pycache__
```

## Diferencias clave entre SE y AI Engineering

| Dimension | Software Engineering | AI Engineering | En brief_builder |
|---|---|---|---|
| Naturaleza del sistema | Determinista: misma entrada, misma salida | Probabilístico: misma entrada puede variar | `temperature=0.2` configurable, prompts versionados |
| Activo principal | Código y reglas | Código, datos, prompts, evaluaciones y modelo | `main.py`, `prompts.py`, `config.py`, métricas |
| Testing | Unit/integration tests con asserts exactos | Tests + evaluación semántica y métricas de calidad | `test_validator.py`, `test_config.py`, `test_main.py` |
| Fallas típicas | Bugs lógicos o de integración | Alucinaciones, drift, regresión de calidad, costo alto | `validate_brief_structure()`, `metrics.py` |
| Deployment | Release por versiones de código | Release + guardrails + monitoreo de calidad/costo | `retry.py`, `metrics.py`, `.metrics.json` |
| Operación | SRE clásico (latencia, errores, disponibilidad) | SRE + eval continua de outputs y riesgo de negocio | Logs coloreados, tokens/costo/latencia por request |
| Mantenibilidad | Refactor de código | Refactor de código, prompts, datasets y políticas | Git versionado, prompts en `prompts.py`, config en `.env` |

## Cosas en común

| Aspecto compartido | En ambos enfoques |
|---|---|
| Diseño de arquitectura | Se definen componentes, contratos y límites claros |
| Buenas prácticas | Versionado, code review, CI/CD, observabilidad |
| Enfoque en negocio | Se prioriza impacto, costo y tiempos de entrega |
| Calidad | Se requieren criterios de aceptación y verificación |
| Operación en producción | Necesitan monitoreo, alertas y respuesta a incidentes |
| Trabajo en equipo | Colaboración entre producto, ingeniería y operaciones |

---

## Setup: Paso a paso

### Crear archivo .env

El archivo `.env` contiene configuración sensible que no debe versionarse:

```bash
# .env (NO COMMITAR ESTE ARCHIVO)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini  # opcional, por defecto es gpt-4o-mini
```

El módulo `config.py` carga automáticamente este archivo usando `python-dotenv`.

### Obtener clave de OpenAI API

1. Ir a https://platform.openai.com/api-keys
2. Crear una nueva API key
3. Copiarla inmediatamente (no se mostrará nuevamente)
4. Pegarla en tu `.env`: `OPENAI_API_KEY=sk-...`

**Importante**: Nunca comitas tu clave. Git está configurado para ignorar `.env`.

### Instalar dependencias con uv

`uv` es un gestor de paquetes Python ultrarrápido:

```bash
# En macOS o Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# En Windows
powershell -ExecutionPolicy BypassUser -c "irm https://astral.sh/uv/install.ps1 | iex"

# Luego instala el proyecto
uv sync
```

Esto crea un `venv` aislado e instala todas las dependencias listadas en `pyproject.toml`.

### Verificar instalación

```bash
make test-se  # Ejecuta tests del módulo SE (no necesita API key)
```

Si ves `PASSED`, estás listo para usar AI Engineering:

```bash
make test-ai  # Ejecuta tests de brief_builder (necesita mock + API key)
```

---

## Arquitectura de brief_builder

El módulo `brief_builder` demuestra cómo construir un sistema de AI Engineering robusto, observable y resiliente.

### Estructura modular

```
ai_engineering/
├── brief_builder/
│   ├── main.py              # Entrada y orquestación
│   ├── config.py            # Carga de config desde .env
│   ├── prompts.py           # Prompts versionados en Git
│   ├── validator.py         # Validación de inputs/outputs
│   ├── exceptions.py        # Excepciones específicas
│   ├── retry.py             # Reintentos con backoff exponencial
│   ├── metrics.py           # Tracking de tokens/costo/latencia
│   └── logger.py            # Logs coloreados para debugging
└── tests/
    ├── test_config.py       # Valida carga de config
    ├── test_validator.py    # Valida inputs/outputs
    └── test_main.py         # Integración end-to-end (con mocks)
```

### Flujo de datos

```
Argumentos de CLI
    ↓
validate_temperature() ← Rechaza si no está en [0.0, 2.0]
validate_context_length() ← Rechaza si contexto > 4000 tokens
    ↓
load_settings() ← Lee OPENAI_API_KEY de .env
    ↓
client.chat.completions.create() ← Llamada a OpenAI
    ↓ (con retry_with_backoff)
    ↓ (exponential backoff + jitter en caso de rate limit)
    ↓
validate_brief_structure() ← Verifica secciones requeridas
validate_markdown_format() ← Verifica sintaxis markdown
    ↓
calculate_cost() ← Estima costo basado en tokens
BriefMetrics ← Empaqueta tokens, costo, latencia
    ↓
save_output() → brief.md + brief.metrics.json
```

### Principios de AI Engineering aplicados

Basados en "AI Engineering" por Chip Huyen:

**1. Reproducibilidad**
- Versión de modelo en Git: `gpt-4o-mini` (config.py)
- Temperatura configurable: `0.2` por defecto, modificable por CLI
- Prompts versionados: `prompts.py` en Git, no hardcoded en código
- Timestamps y métricas guardadas en `.metrics.json`

**2. Modularidad**
- `config.py`: responsabilidad única de configuración
- `prompts.py`: prompts separados de lógica
- `validator.py`: validación centralizada (inputs y outputs)
- `retry.py`: lógica de reintentos reutilizable
- `exceptions.py`: jerarquía clara de errores
- `metrics.py`: observabilidad separada del core

**3. Testing exhaustivo**
- `test_config.py`: 13 tests de carga de config (casos normales y edge)
- `test_validator.py`: 18 tests de validación (inputs/outputs)
- `test_main.py`: 9 tests de integración con mocks de API
- Cobertura objetivo: 85%+
- Usa pytest con markers (`@pytest.mark.unit`)

**4. Manejo de errores**
- Excepciones específicas: `APIError`, `ValidationError`, `ConfigurationError`
- Retry logic: exponential backoff + jitter (evita thundering herd)
- Logging granular: DEBUG, INFO, WARNING, ERROR con colores
- Diferencia entre errores recuperables (API) y no recuperables

**5. Observabilidad**
- Logging en tiempo real: qué modelo, temperatura, tokens, costo
- Métricas guardadas: `brief.metrics.json` junto a cada output
- Latencia medida: `time.perf_counter()` para precisión
- Costo estimado: basado en pricing oficial de OpenAI (enero 2025)

**6. Diseño defensivo**
- Valida inputs antes de llamar API (ahorra dinero)
- Valida outputs después de generar (evita guardar basura)
- Paths relativos convertidos a absolutos (evita bugs de contexto)
- Archivos parent directories creados automáticamente

---

## Testing

### Ejecutar tests

```bash
# Tests con salida detallada
make test-ai

# Tests con cobertura HTML (abre htmlcov/index.html)
make test-ai-cov

# Todos los tests del repo
make test-all
```

### Qué validan los tests

**test_config.py** (13 tests)
- Carga de API key desde `.env`
- Manejo de variables faltantes
- Valores por defecto (model = gpt-4o-mini)
- Stripped whitespace
- Immutabilidad de Settings (frozen dataclass)

**test_validator.py** (18 tests)
- `validate_temperature()`: rango [0.0, 2.0]
- `validate_context_length()`: límite de ~4000 tokens
- `validate_output_path()`: permisos de escritura
- `validate_brief_structure()`: presencia de secciones requeridas
- `validate_markdown_format()`: sintaxis markdown válida

**test_main.py** (9 tests)
- Parsing de argumentos CLI
- Integración: args → validation → (mocked API) → metrics → save
- Manejo de excepciones
- Creación de directorios
- Guardado de métricas JSON

### Cobertura

El proyecto apunta a **85%+ de cobertura**. Para ver el reporte:

```bash
make test-ai-cov
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

Las áreas de menor cobertura son:
- Manejo de IO errors (difícil de mockear)
- Casos edge de logging
- Partes del código que dependen de OpenAI SDK internamente

---

## Principios de AI Engineering (Chip Huyen)

### Reproducibilidad

**Por qué importa**: Un brief generado hoy con `gpt-4o-mini` + `temperature=0.2` debe poder regenerarse exactamente igual en 6 meses.

**Cómo lo implementamos**:
- Modelo y temperatura en `.env` (versionable)
- Prompts en `prompts.py` (versionados en Git)
- Timestamp de generación en `brief.metrics.json`
- Hash del prompt en logs (futuro)

**Verificar**:
```bash
# Generar brief
make run-ai --context "Startup"
# Regenerar con mismos parámetros
make run-ai --context "Startup"
# Las métricas (tokens, cost) deberían ser ~iguales
cat 01-introduction/ai_engineering/briefs/brief.metrics.json
```

### Modularidad

**Por qué importa**: Cambiar prompt, retry logic o métricas no debe romper el resto del código.

**Cómo lo implementamos**:
- Cada módulo tiene responsabilidad única
- Contratos claros (args/returns bien tipados)
- Excepciones específicas por failure mode
- Tests aislados por funcionalidad

**Verificar**:
```bash
# Cambiar prompt sin tocar main.py
nano 01-introduction/ai_engineering/brief_builder/prompts.py
# Cambiar retry logic sin tocar API call
nano 01-introduction/ai_engineering/brief_builder/retry.py
# Tests aún pasan
make test-ai
```

### Testing

**Por qué importa**: Un prompt que genera alucinaciones el 10% del tiempo no es deplorable en producción sin evaluación automática.

**Cómo lo implementamos**:
- Unit tests: config, validators, formato markdown
- Integration tests: orquestación end-to-end (con mocks)
- Propios tests de output: `validate_brief_structure()` verifica secciones

**Verificar**:
```bash
make test-ai  # 40 tests
make test-ai-cov  # Cobertura HTML
# Nota: mocks de OpenAI previenen gastar dinero en testing
```

**Limitación**: Los tests actuales no evalúan "calidad semántica" del brief (eso requeriría otra LLM como judge). Es un área donde AI Engineering difiere de SE.

### Error Handling

**Por qué importa**: Una API rate-limited puede recuperarse con reintentos. Una config faltante no.

**Cómo lo implementamos**:
- Excepciones específicas: `APIError` (recuperable), `ConfigurationError` (no recuperable)
- Retry con backoff exponencial: 1s, 2s, 4s con jitter
- Logging detallado de cada reintento
- Diferenciación de error (API vs validación vs config)

**Verificar**:
```bash
# Simular rate limit (comentar en main.py, descomentar error)
# make run-ai  # Verás reintentos en logs
# Ver estructura de excepciones
cat 01-introduction/ai_engineering/brief_builder/exceptions.py
```

### Observabilidad

**Por qué importa**: "Lo que no se mide, no se mejora". Necesitas saber tokens, costo y latencia de cada request.

**Cómo lo implementamos**:
- Logging con colores (DEBUG=cian, INFO=verde, WARNING=amarillo, ERROR=rojo)
- Métricas JSON por cada ejecución
- Cálculo de costo basado en pricing actual
- Latencia medida con precisión nanosegundos (`time.perf_counter()`)

**Verificar**:
```bash
make run-ai  # Ver logs coloreados
cat 01-introduction/ai_engineering/briefs/brief.metrics.json  # Ver métricas JSON
# Busca: "tokens", "cost_usd", "latency_seconds"
```

**Ejemplo de métrica**:
```json
{
  "model": "gpt-4o-mini",
  "temperature": 0.2,
  "prompt_tokens": 1243,
  "completion_tokens": 876,
  "total_tokens": 2119,
  "estimated_cost_usd": 0.000655,
  "latency_seconds": 2.34,
  "timestamp": "2025-02-03T14:30:00"
}
```

### Referencias

- **AI Engineering** por Chip Huyen
  - Cap. 2: Foundational Components (ML Systems)
  - Cap. 3: Data Engineering Fundamentals
  - Cap. 4: Model Development
  - Cap. 5: Building Resilient Systems (Retry logic)
  - Cap. 7: Monitoring and Observability
- **The Twelve-Factor App**: Configuración desde environment

---

## Troubleshooting

### "OPENAI_API_KEY no configurado"

**Síntoma**: `RuntimeError: OPENAI_API_KEY no esta configurado.`

**Causa**: El archivo `.env` no existe o está vacío.

**Solución**:
```bash
# 1. Crear .env en la raíz del repo
echo "OPENAI_API_KEY=sk-..." > .env
# 2. Reemplazar sk-... con tu clave real
# 3. Verificar que la raíz sea correcta (misma carpeta que pyproject.toml)
ls -la .env
# 4. Reintentar
make run-ai
```

### "Rate limit exceeded" (Error 429)

**Síntoma**: Ves logs con "Attempt 1/3 failed" varias veces, luego `APIError: Rate limit exceeded`.

**Causa**: OpenAI throttling (demasiadas requests o cuota excedida).

**Solución**:
- La retry logic ya maneja esto automáticamente (espera 1s, 2s, 4s)
- Si sigue fallando después de 3 intentos:
  - Espera 5-10 minutos antes de reintentar
  - Verifica tu cuota en https://platform.openai.com/account/usage/overview
  - Si es cuota, agrega créditos o reduce temperatura (menos tokens = más rápido)

### "Brief tiene formato markdown invalido"

**Síntoma**: El brief se genera pero los logs muestran `ValidationError: Brief tiene formato markdown invalido`.

**Causa**: El modelo generó markdown malformado (ej: ``` sin cerrar).

**Solución**:
- Baja temperatura a `0.1` (más determinístico, menos creatividad):
  ```bash
  make run-ai --temperature 0.1
  ```
- Revisa el prompt en `prompts.py` para ser más explícito
- Si persiste, quizás `gpt-4o-mini` necesita un upgrade a `gpt-4o`:
  ```bash
  echo "OPENAI_MODEL=gpt-4o" >> .env
  ```

### "Brief incompleto. Secciones faltantes"

**Síntoma**: Logs muestran `[has_recommendations=False]` u otra sección faltante.

**Causa**: El modelo no incluyó todas las secciones requeridas (ver `prompts.py`).

**Solución**:
- Usa `gpt-4o` (mejor calidad) en lugar de `gpt-4o-mini`
- Reduce temperatura a `0.2` o menos
- Agrega contexto especificando el dominio:
  ```bash
  make run-ai-context CONTEXT="Para una startup fintech"
  ```

### "AttributeError: module 'openai' has no attribute..."

**Síntoma**: Error durante `import openai` o `from openai import...`.

**Causa**: Versión vieja de openai SDK o instalación incompleta.

**Solución**:
```bash
# Reinstalar dependencias
rm -rf .venv
uv sync
make test-ai  # Verificar que funcionan tests
```

### Tests fallan con "ModuleNotFoundError: No module named 'brief_builder'"

**Síntoma**: Ves `ModuleNotFoundError` al ejecutar `make test-ai`.

**Causa**: Python path no configurado correctamente.

**Solución**:
```bash
# Verificar que tests usan sys.path insert correctamente
head -20 01-introduction/ai_engineering/tests/test_config.py
# Si falta, el conftest.py debería inyectarlo
cd /Users/carlosdaniel/Desktop/ai_engineering_henry
make test-ai -v  # Con verbose
```

---

## Métricas y Costos

### Leer archivo .metrics.json

Cada vez que ejecutas `make run-ai`, se guarda `brief.metrics.json`:

```bash
cat 01-introduction/ai_engineering/briefs/brief.metrics.json | jq .
```

Campos principales:

| Campo | Significado | Unidad |
|---|---|---|
| `model` | Modelo usado (ej: gpt-4o-mini) | string |
| `temperature` | Parámetro de aleatoriedad | 0.0-2.0 |
| `prompt_tokens` | Tokens en la pregunta | número |
| `completion_tokens` | Tokens en la respuesta | número |
| `total_tokens` | Suma de ambos | número |
| `estimated_cost_usd` | Costo estimado | USD |
| `latency_seconds` | Tiempo de ejecución | segundos |
| `timestamp` | Cuándo se ejecutó | ISO 8601 |

### Estimar costos antes de ejecutar

**Pricing actual (enero 2025)**:

| Modelo | Entrada | Salida |
|---|---|---|
| gpt-4o-mini | $0.15 / 1M tokens | $0.60 / 1M tokens |
| gpt-4o | $2.50 / 1M tokens | $10.00 / 1M tokens |
| gpt-4 | $30 / 1M tokens | $60 / 1M tokens |

**Ejemplo de cálculo**:
```
Prompt: 1,000 tokens
Completion: 800 tokens (típico para un brief)
Modelo: gpt-4o-mini

Costo = (1000 * 0.15 + 800 * 0.60) / 1,000,000
       = (150 + 480) / 1,000,000
       = 630 / 1,000,000
       = $0.00063  (menos de 1 centavo!)
```

**Presupuesto recomendado para estudiantes**:
- 100 briefs con gpt-4o-mini: ~$0.06
- Experimentar con parámetros: $0.10-0.50/día
- Mejor empezar con $5-10 de créditos

### Tips para controlar costos

1. **Usa gpt-4o-mini por defecto** (10x más barato que gpt-4o)
2. **Monitorea tokens**:
   ```bash
   # Resumen rápido
   grep "completion_tokens" 01-introduction/ai_engineering/briefs/brief.metrics.json
   ```
3. **Reduce contexto si es muy largo**:
   ```bash
   # [OK] Bien: contexto específico
   make run-ai-context CONTEXT="Startup B2B"
   # [X] Evitar: contexto de 5 páginas
   make run-ai-context CONTEXT="..."  # miles de tokens
   ```
4. **Aumenta temperatura solo si necesitas creatividad**:
   - `temperature=0.1`: determinístico (menor costo de tokens)
   - `temperature=1.0`: balanceado (default en muchos modelos)
   - `temperature=2.0`: creativo (más tokens para mayor variabilidad)
5. **Usa logs para debugging, no para trace completo**:
   - Los logs se guardan en stderr (no impacta tokens de salida)
   - Ver logs: `make run-ai 2>&1 | grep "tokens"`

### Dashboard de uso (manual)

Si corres varios briefs, crea un pequeño script para agregar:

```bash
# Ejemplo: suma de todos los costos
find 01-introduction/ai_engineering/briefs -name "*.metrics.json" -exec \
  jq '.estimated_cost_usd' {} \; | \
  awk '{sum+=$1} END {print "Total: $" sum}'
```

---

## Estructura del repositorio

```
01-introduction/
├── README.md                          # Tú estás aquí
├── python_software_engineering/       # Enfoque clásico (determinista)
│   ├── src/
│   │   └── app.py                    # Ejemplo simple: generador de briefs determinista
│   └── tests/
│       └── test_app.py
├── ai_engineering/                    # Enfoque AI (probabilístico, observable)
│   ├── brief_builder/                 # Caso de estudio principal
│   │   ├── main.py                   # Orquestación del flujo
│   │   ├── config.py                 # Carga de variables de ambiente
│   │   ├── prompts.py                # Prompts versionados en Git
│   │   ├── validator.py              # Validación de inputs/outputs
│   │   ├── exceptions.py             # Excepciones personalizadas
│   │   ├── retry.py                  # Retry logic con backoff exponencial
│   │   ├── metrics.py                # Tracking de costo/tokens/latencia
│   │   ├── logger.py                 # Logging con colores
│   │   └── __init__.py
│   ├── briefs/                        # Output de ejecuciones
│   │   ├── software_vs_ai_engineering.md
│   │   └── brief.metrics.json
│   ├── tests/                         # Suite de tests
│   │   ├── test_config.py            # 13 tests de configuración
│   │   ├── test_validator.py         # 18 tests de validación
│   │   ├── test_main.py              # 9 tests de integración
│   │   ├── conftest.py               # Fixtures de pytest
│   │   └── __init__.py
│   └── __init__.py
└── slides/                            # Materiales de clase
```

---

## Próximos pasos

1. **Ejecuta los ejemplos**:
   ```bash
   make run-se   # Ver diferencias clave
   make run-ai   # Ver AI Engineering en acción
   ```

2. **Lee el código**:
   - Empieza por `main.py` (flujo principal)
   - Entiende `prompts.py` (qué pedimos al modelo)
   - Revisa `retry.py` (cómo manejamos fallos)
   - Explora `metrics.py` (cómo medimos éxito)

3. **Experimenta**:
   ```bash
   make run-ai-context CONTEXT="Tu contexto"
   make run-ai --temperature 0.1  # Menos creativo
   OPENAI_MODEL=gpt-4o make run-ai  # Mejor calidad
   ```

4. **Modifica y aprende**:
   - Cambia un prompt en `prompts.py`
   - Agrega una nueva sección en `validator.py`
   - Experimenta con retry delays en `retry.py`
   - Entiende por qué SE y AI Engineering requieren diferentes estrategias

5. **Lee la bibliografía**:
   - "AI Engineering" - Chip Huyen (capítulos 2-7)
   - Papers sobre prompt engineering y evaluación de LLMs
   - Documentación de OpenAI API

---

**Nota para instructores**: Este proyecto es una plantilla viva. Siéntete libre de:
- Agregar más secciones al brief
- Crear nuevos validadores
- Experimentar con otros modelos (Claude, Llama, etc.)
- Implementar evaluadores semánticos
- Extender a un dashboard de costos

**Última actualización**: Febrero 2025
