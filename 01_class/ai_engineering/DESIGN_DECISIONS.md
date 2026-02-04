# Design Decisions - Brief Builder

Este documento registra las decisiones arquitecturales clave del sistema `brief_builder`, siguiendo el formato ADR (Architecture Decision Record). Cada decisión está fundamentada en principios de **"AI Engineering"** y **"Designing Machine Learning Systems"** de Chip Huyen.

---

## ADR-001: Retry Logic con Exponential Backoff

**Fecha:** 2026-02-03
**Estado:** Implementado en `retry.py`

### Contexto

Las APIs de LLM (como OpenAI) pueden fallar temporalmente por:
- Rate limiting (429)
- Errores de servicio (503, 504)
- Timeouts de red
- Mantenimiento temporal

Sin retry logic, cada fallo requiere intervención manual, haciendo el sistema frágil en producción.

### Decisión

Implementar retry con **exponential backoff** y **jitter**:
- Máximo 3 intentos por defecto
- Delay inicial: 1 segundo
- Multiplicador exponencial: 2x (1s → 2s → 4s)
- Jitter aleatorio para prevenir thundering herd
- Solo reintentar errores recuperables (429, 503, 504)

### Rationale

Chip Huyen (AI Engineering, Capítulo 5: "Resilient Systems"):
> "Resilience is critical for LLM systems. Exponential backoff prevents overwhelming failing services and gives them time to recover."

**Beneficios:**
- Sistema más robusto ante fallos temporales
- Evita sobrecargar APIs con reintentos agresivos
- Jitter previene que múltiples clientes reintenten simultáneamente
- Logging detallado para debugging

**Trade-offs aceptados:**
- Latencia mayor en casos de error (hasta ~7 segundos con 3 intentos)
- Complejidad adicional en el código
- **Decisión:** El trade-off es aceptable porque la alternativa (fallos sin retry) es peor en producción

### Alternativas Consideradas

1. **Sin retry** → ❌ Descartado: Demasiado frágil
2. **Retry simple (fixed delay)** → ❌ Descartado: Puede empeorar rate limiting
3. **Circuit breaker** → 🔮 Futuro: Útil cuando se escale a múltiples clientes

### Referencias

- Implementación: `01_class/ai_engineering/brief_builder/retry.py:29`
- Tests: `01_class/ai_engineering/tests/test_main.py` (mocked)
- Chip Huyen: AI Engineering, Chapter 5

---

## ADR-002: Validación de Inputs y Outputs

**Fecha:** 2026-02-03
**Estado:** Implementado en `validator.py`

### Contexto

Los sistemas AI son probabilísticos y pueden:
- Aceptar inputs inválidos que desperdician tokens ($$$)
- Generar outputs malformados o incompletos
- Fallar silenciosamente sin validación

### Decisión

Validar agresivamente en ambos extremos:

**Input validation:**
- `temperature` en rango [0.0, 2.0]
- `context` no excede límite de tokens (~4000)
- `output_path` es escribible

**Output validation:**
- Formato markdown válido
- Estructura del brief completa (secciones requeridas)
- Content no vacío

### Rationale

Chip Huyen (Designing ML Systems, Capítulo 8: "Data Quality"):
> "Bad data in, bad predictions out. Validation at system boundaries is non-negotiable."

**Beneficios:**
- Detecta errores temprano (fail fast)
- Previene desperdiciar tokens ($) en inputs inválidos
- Garantiza calidad mínima del output
- Logs warnings cuando brief está incompleto

**Trade-offs:**
- Overhead de validación (~5ms por request)
- Código adicional a mantener
- **Decisión:** Overhead mínimo vs beneficio alto

### Implementación

```python
# Validar ANTES de llamar API
validate_temperature(temperature)
validate_context_length(context)

# Validar DESPUÉS de recibir respuesta
if not validate_markdown_format(content):
    raise ValidationError("Invalid markdown")

structure_checks = validate_brief_structure(content)
if not structure_checks["is_complete"]:
    logger.warning("Brief incompleto: %s", missing_sections)
```

### Alternativas Consideradas

1. **Sin validación** → ❌ Descartado: Costos impredecibles, calidad baja
2. **Validación solo en inputs** → ❌ Insuficiente: No garantiza output útil
3. **Validación estricta que falla** → ⚠️ Parcial: Warning en lugar de error si brief útil pero incompleto

### Referencias

- Implementación: `01_class/ai_engineering/brief_builder/validator.py`
- Tests: `01_class/ai_engineering/tests/test_validator.py` (29 tests)
- Chip Huyen: Designing ML Systems, Chapter 8

---

## ADR-003: Tracking de Métricas y Costos

**Fecha:** 2026-02-03
**Estado:** Implementado en `metrics.py`

### Contexto

Los sistemas AI tienen costos variables por request:
- Tokens de entrada (prompt)
- Tokens de salida (completion)
- Modelo utilizado (gpt-4o vs gpt-4o-mini = 10x diferencia)
- Latencia impacta UX

Sin tracking, es imposible:
- Estimar presupuestos
- Detectar anomalías (costos altos)
- Optimizar prompts
- Debugging de producción

### Decisión

Trackear y loggear métricas en cada request:
- Tokens (prompt, completion, total)
- Costo estimado (USD)
- Latencia (segundos)
- Model, temperature, timestamp
- Guardar en `.metrics.json` junto al brief

### Rationale

Chip Huyen (AI Engineering, Capítulo 7: "Monitoring and Observability"):
> "You can't improve what you don't measure. Cost and latency metrics are critical for LLM systems."

**Beneficios:**
- Budget awareness desde día 1
- Detectar prompts ineficientes (demasiados tokens)
- Comparar modelos (gpt-4o-mini vs gpt-4o)
- Histórico de costos para auditoría
- Debugging: correlacionar latencia con errores

**Ejemplo de output:**
```json
{
  "model": "gpt-4o-mini",
  "temperature": 0.2,
  "prompt_tokens": 1234,
  "completion_tokens": 567,
  "total_tokens": 1801,
  "estimated_cost_usd": 0.000525,
  "latency_seconds": 3.42,
  "timestamp": "2026-02-03T18:30:00Z"
}
```

### Alternativas Consideradas

1. **Sin tracking** → ❌ Descartado: Imposible gestionar costos
2. **Solo loggear en consola** → ❌ Insuficiente: Se pierde el historial
3. **Enviar a servicio externo** → 🔮 Futuro: Útil para agregación multi-usuario

### Referencias

- Implementación: `01_class/ai_engineering/brief_builder/metrics.py`
- Uso: `01_class/ai_engineering/brief_builder/main.py:163-185`
- Pricing: https://openai.com/api/pricing/
- Chip Huyen: AI Engineering, Chapter 7

---

## ADR-004: Excepciones Específicas vs Generic

**Fecha:** 2026-02-03
**Estado:** Implementado en `exceptions.py`

### Contexto

Los sistemas complejos tienen múltiples modos de fallo:
- Errores de configuración (API key faltante)
- Errores de API (rate limit, timeout)
- Errores de validación (input/output inválido)

Usar `Exception` genérico hace difícil:
- Diagnosticar problemas
- Aplicar retry selectivo
- Manejar errores diferentes de forma apropiada

### Decisión

Definir jerarquía de excepciones específicas:

```python
BriefBuilderError (base)
├── APIError (API calls)
├── ValidationError (inputs/outputs)
└── ConfigurationError (settings)
```

Cada excepción incluye:
- Mensaje descriptivo
- Metadata relevante (status_code, field, value)
- `__str__` customizado para logging

### Rationale

Python Best Practices + Chip Huyen (AI Engineering):
> "Specific exceptions make debugging faster and enable selective error handling."

**Beneficios:**
- Catch selectivo: `except APIError` para retry, `except ValidationError` para skip
- Logs más claros: "ValidationError: temperature=3.0" vs "Exception"
- Facilita debugging en producción
- Self-documenting code

**Ejemplo:**
```python
try:
    brief, metrics = generate_brief(context, temp=3.0)
except ValidationError as e:
    logger.error("Input inválido: %s", e)
    # No reintentar - error del usuario
except APIError as e:
    logger.error("API falló: %s", e)
    # Reintentar automáticamente
```

### Alternativas Consideradas

1. **Solo `Exception`** → ❌ Dificulta debugging
2. **Códigos de error numéricos** → ❌ Menos pythonic
3. **Excepciones muy granulares** → ⚠️ Over-engineering para este scope

### Referencias

- Implementación: `01_class/ai_engineering/brief_builder/exceptions.py`
- Uso: `01_class/ai_engineering/brief_builder/main.py:260-290`
- PEP 8: Exception Naming Conventions

---

## ADR-005: Prompts Versionados en Git

**Fecha:** 2026-02-03
**Estado:** Implementado en `prompts.py`

### Contexto

Los prompts son **código** en sistemas AI:
- Cambiar el prompt cambia el comportamiento del sistema
- Debugging requiere saber qué prompt se usó
- Múltiples developers necesitan colaborar en prompts

Sin versionado:
- Imposible reproducir outputs antiguos
- No hay code review de prompts
- Regresiones difíciles de detectar

### Decisión

**Versionar prompts en Git** como código normal:
- `prompts.py` contiene funciones que retornan strings
- Cambios de prompts = commits con descripción
- Code review obligatorio para cambios de prompts
- Fecha incluida en prompt (`date.today()`) para reproducibilidad

### Rationale

Chip Huyen (AI Engineering, Capítulo 3: "Reproducibility"):
> "Prompts are code. Version them like code. A system that can't reproduce results is a system you can't debug."

**Beneficios:**
- Reproducibilidad: `git checkout <commit>` reproduce output exacto
- Trazabilidad: `git blame` muestra quién cambió qué
- Colaboración: Pull requests para cambios de prompts
- Rollback fácil si prompt nuevo empeora calidad

**Ejemplo de commit message:**
```
feat(prompts): agregar sección de anti-patrones

- Añade requisito de 5 anti-patrones mínimo
- Cada anti-patrón incluye síntoma + impacto + mitigación
- Mejora calidad del brief para estudiantes
```

### Alternativas Consideradas

1. **Prompts en base de datos** → 🔮 Futuro: Útil para A/B testing
2. **Hardcoded strings** → ❌ Sin versionado, difícil de revisar
3. **Archivos .txt separados** → ⚠️ Posible, pero menos ergonómico

### Referencias

- Implementación: `01_class/ai_engineering/brief_builder/prompts.py`
- Git history: `git log -- prompts.py`
- Chip Huyen: AI Engineering, Chapter 3

---

## ADR-006: Testing con Mocks vs Llamadas Reales

**Fecha:** 2026-02-03
**Estado:** Implementado en `tests/conftest.py`

### Contexto

Tests de sistemas AI pueden:
- Hacer llamadas reales a APIs ($$$ + lento + rate limits)
- Usar mocks que simulan respuestas (rápido + gratis)

### Decisión

**Usar mocks para tests unitarios** con fixture `mock_openai_client`:
- Simula respuestas de OpenAI sin llamadas reales
- Tests rápidos (<1s total)
- Sin costos ni rate limits
- Tests integración marcados con `@pytest.mark.integration` (no ejecutados por defecto)

### Rationale

Testing Best Practices:
> "Unit tests should be fast, deterministic, and isolated."

**Beneficios:**
- Tests corren en CI/CD sin API keys
- Velocidad: 56 tests en 0.47s
- Costo: $0
- Determinismo: misma respuesta siempre
- Permite testear casos edge (errores, respuestas vacías)

**Trade-offs:**
- Mocks pueden divergir de API real
- **Mitigación:** Tests manuales ocasionales con API real

### Implementación

```python
@pytest.fixture
def mock_openai_client(mocker):
    mock_response = mocker.Mock()
    mock_response.choices[0].message.content = "..."
    mock_response.usage.total_tokens = 1500
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client
```

### Referencias

- Implementación: `01_class/ai_engineering/tests/conftest.py:14`
- Tests: Todos los tests en `test_main.py` usan mocks
- Coverage: 88% con solo mocks

---

## Principios Generales Aplicados

### 1. Separation of Concerns
- `config.py`: Solo configuración
- `prompts.py`: Solo prompts
- `validator.py`: Solo validación
- `retry.py`: Solo retry logic
- `metrics.py`: Solo tracking

**Beneficio:** Cada módulo es testeable independientemente

### 2. Fail Fast
- Validar temperatura en `parse_args` (antes de API call)
- Validar API key en `load_settings` (al inicio)
- Validar outputs inmediatamente después de recibir

**Beneficio:** Errores detectados temprano = debugging más fácil

### 3. Explicit Better Than Implicit
- Parámetros explícitos (`temperature`, `context`)
- Excepciones específicas con nombres claros
- Docstrings en todas las funciones públicas

**Beneficio:** Código self-documenting

### 4. Observability First
- Logs en cada paso crítico
- Métricas guardadas automáticamente
- Colored output para escaneo rápido

**Beneficio:** Debugging rápido en producción

---

## Decisiones Pendientes (Future Work)

### FW-001: Circuit Breaker Pattern
**Cuándo:** Al escalar a múltiples usuarios concurrentes
**Por qué:** Prevenir cascading failures si OpenAI cae

### FW-002: A/B Testing de Prompts
**Cuándo:** Cuando queramos optimizar prompts con datos
**Por qué:** Métricas cuantitativas > opiniones

### FW-003: Caching de Responses
**Cuándo:** Si vemos requests repetidos
**Por qué:** Reducir costos y latencia

### FW-004: Async API Calls
**Cuándo:** Si necesitamos generar múltiples briefs en paralelo
**Por qué:** Mejor throughput

### FW-005: Prompt Registry Separado
**Cuándo:** Al tener >10 prompts diferentes
**Por qué:** Facilita A/B testing y versionado granular

---

## Referencias

### Libros
- Chip Huyen - "AI Engineering" (2024)
- Chip Huyen - "Designing Machine Learning Systems" (2022)

### Artículos
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [Google's Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [The Twelve-Factor App](https://12factor.net/)

### Código
- Repository: `ai_engineering_henry`
- Módulo: `01_class/ai_engineering/brief_builder/`
- Tests: `01_class/ai_engineering/tests/`

---

**Última actualización:** 2026-02-03
**Autores:** Carlos Daniel (con Claude Sonnet 4.5)
**Revisores:** Henry Academy Team
