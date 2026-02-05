# Clase 02: Prompting Aplicado (CoT + ReAct)

Esta clase está diseñada para llevarte de fundamentos a nivel medio-avanzado en prompting aplicado. El objetivo no es memorizar recetas, sino aprender a diseñar mecanismos reproducibles de razonamiento y decisión.

## Qué aprenderás

Al terminar esta clase deberías poder:

1. Diseñar prompts con estructura de ingeniería (objetivo, restricciones, formato, evaluación)
2. Distinguir cuándo usar CoT y cuándo usar ReAct
3. Implementar feedback loops que mejoren calidad de salida de forma medible
4. Pasar de pruebas manuales a ejecución validable con notebooks y scripts
5. Decidir cuándo usar JSON vs Pydantic para validación de outputs

## Conexión con Estructura Unificada de Prompts

**Antes de continuar, lee la sección "Fundamentos de Prompt Engineering" en el README principal.**

Todo lo que verás en esta clase sigue la estructura de 5 capas:

1. **ROLE**: Define quién es el agente (coach conversacional, analista, etc.)
2. **TASK**: Qué debe lograr (diseñar recomendación, auditar respeto, etc.)
3. **OUTPUT FORMAT**: Estructura JSON o Pydantic (con validación)
4. **EXAMPLES** (opcional): Few-shot para mayor consistencia
5. **CONTEXT**: Datos específicos del caso (perfil del usuario, etc.)

Los ejemplos en COT/ y ReAct/ mapean explícitamente a esta estructura en comentarios.

---

## Chain of Thought (CoT): De intuición a método

### Qué es CoT y por qué importa

Chain of Thought (CoT) no es "pedirle al modelo que piense" de forma vaga. Es un diseño de prompt donde obligamos una secuencia explícita de razonamiento antes de la respuesta final.

```
Diagrama CoT:
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Input     │───│  Paso 1:     │───│  Paso 2:     │───│  Paso 3:     │
│  Contexto   │    │  Analizar    │    │  Estrategia  │    │  Verificar   │
└─────────────┘    │  señales     │    │  de apertura │    │  riesgos     │
                   └──────────────┘    └──────────────┘    └──────────────┘
                                                                      │
                                                                      ▼
                                                          ┌──────────────────┐
                                                          │  Paso 4:         │
                                                          │  Recomendación   │
                                                          │  final           │
                                                          └──────────────────┘
```

**Valor práctico:**
- Reduce respuestas superficiales en tareas con ambigüedad
- Mejora consistencia de estilo y estructura
- Hace depurable el sistema: si falla, ubicamos en qué paso
- Transparencia: El razonamiento es visible y auditable

### Limitaciones Críticas de CoT

**1. CoT NO convierte modelos débiles en expertos**
- Si el modelo no tiene capacidad de razonamiento, CoT no la crea
- CoT amplifica la calidad del razonamiento existente
- Modelo malo + CoT = razonamiento malo explícito

**2. CoT amplifica tanto buen como mal contexto**
- **Buen contexto** (claro, estructurado, completo) + CoT = outputs mejores
- **Mal contexto** (vago, ambiguo, incompleto) + CoT = outputs peores (y más caros)
- Arregla el contexto primero, luego aplica CoT

**3. Cost/Latency Trade-off**
```
Prompt directo:  200 tokens input + 100 tokens output = 300 tokens
CoT:             200 tokens input + 300 tokens output = 500 tokens (+67%)
```
- Costo: +67% por request
- Latencia: +50-100% (más tokens generados = más tiempo)

**4. No garantiza corrección**
- El modelo puede razonar de forma plausible pero incorrecta
- Necesitas validación downstream (rúbricas, tests)
- CoT hace el error más visible, no lo previene

### Anatomía de un prompt CoT bien diseñado

Todo prompt CoT sigue las 5 capas de prompt engineering:

**1. ROLE (Quién es el agente)**
```python
"Eres un coach conversacional elegante, respetuoso y práctico."
```
- Define identidad, valores, límites éticos
- En CoT: El rol determina el estilo de razonamiento

**2. TASK (Qué debe hacer)**
```python
"Diseña una recomendación de conversación personalizada"
```
- Objetivo específico y medible
- En CoT: Incluye la descomposición en subtareas (pasos de razonamiento)

**3. OUTPUT FORMAT (Estructura requerida)**
```json
{
  "chain_of_thought": ["paso 1", "paso 2", "paso 3", "paso 4"],
  "opener": "...",
  "follow_up": "...",
  "tone_notes": [...],
  "avoid": [...]
}
```
- JSON schema (ejemplos 01, 02) o Pydantic BaseModel (ejemplos 03, 04)
- CRÍTICO: Sin formato validable, CoT queda en demo; con validación, entra en producción

**4. EXAMPLES (opcional - en Few-shot CoT)**
- 1-3 ejemplos curados de calidad
- Trade-off: +consistencia, +tokens/costo (+80% típicamente)

**5. CONTEXT (Información específica)**
```python
profile = {
  "tipo_persona": "arquitecta apasionada por fotografía urbana",
  "gustos": ["cafés tranquilos", "jazz", "viajes cortos"],
  "contexto": "match reciente, primera interacción"
}
```
- Datos estructurados, filtrados
- En CoT: El contexto alimenta cada paso de razonamiento

### Zero-shot vs Few-shot CoT: Cost Analysis

**Zero-shot CoT:**
```
Input:  200 tokens (prompt + contexto)
Output: 300 tokens (4 pasos CoT + respuesta)
Total:  500 tokens/request

Costo (gpt-4o-mini):
- Input:  200 × $0.15/1M = $0.00003
- Output: 300 × $0.60/1M = $0.00018
- Total: $0.00021/request

100,000 requests/mes = $21/mes
```

**Few-shot CoT:**
```
Input:  600 tokens (prompt + 3 ejemplos + contexto)
Output: 300 tokens (mismo razonamiento)
Total:  900 tokens/request

Costo (gpt-4o-mini):
- Input:  600 × $0.15/1M = $0.00009
- Output: 300 × $0.60/1M = $0.00018
- Total: $0.00027/request

100,000 requests/mes = $27/mes
```

**Trade-off matemático:**
- Few-shot cuesta +29% más que Zero-shot
- A cambio: +30-40% mejor consistencia (según evaluación con rubrica.py)

**Usa Zero-shot cuando:**
- Estás explorando/prototipando
- Presupuesto de tokens limitado
- Latencia crítica (menos tokens = más rápido)
- Casos de uso muy diversos (difícil curar ejemplos representativos)

**Usa Few-shot cuando:**
- Ya tienes definición de calidad clara
- Necesitas consistencia alta (producción)
- Tienes ejemplos bien curados
- Calidad > costo (ej: atención al cliente, legal)

### Cuándo NO usar CoT

**1. Tareas simples y factuales**
- Mal uso: "Extrae el email del texto [usa CoT]"
- Mejor: Regex o prompt directo sin razonamiento
- Costo evitado: 2-3x tokens

**2. Latencia crítica**
- Si necesitas <200ms de respuesta
- CoT añade +50-100% latencia (más tokens generados)
- Ejemplo: Autocompletado en tiempo real

**3. Presupuesto muy limitado**
- CoT aumenta costo 2-3x vs prompt directo
- Si estás en $50/mes, cada optimización cuenta

**4. El problema es determinístico**
- Cálculos matemáticos simples → función Python
- Validación de formato → regex
- No uses LLM (y menos CoT) si no necesitas razonamiento

**5. Contexto insuficiente**
- Si no tienes buen contexto, CoT amplifica la basura
- Arregla el contexto primero, luego considera CoT

### Implementación en este repositorio

**Scripts:**
```bash
uv run python 02-prompting/COT/Notebooks/01_zero_shot_cot_recomendador.py
uv run python 02-prompting/COT/Notebooks/02_few_shot_cot_feedback_loop.py
```

**Notebooks:**
- `02-prompting/COT/Notebooks/cot_recomendador_aplicado.ipynb`

---

## ReAct: Cómo construir agentes que razonan y actúan

### Idea central

ReAct es el puente entre "responder texto" y "operar un flujo". Si CoT organiza pensamiento interno, ReAct organiza pensamiento más ejecución de acciones con observación intermedia.

ReAct separa cada iteración en tres piezas:
- **Thought**: hipótesis o plan corto
- **Action**: qué herramienta o paso ejecutar
- **Observation**: resultado de esa acción

```
Diagrama ReAct:
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  Objetivo  │───│  Thought:  │───│  Action:   │───│Observation:│
│  Usuario   │    │  "Necesito │    │  Ejecutar  │    │  Resultado │
└────────────┘    │  analizar" │    │  tool"     │    │  parcial   │
                  └────────────┘    └────────────┘    └────────────┘
                        ▲                                     │
                        │                                     │
                        └─────────────────────────────────────┘
                             ¿Ya alcanza para responder?
                                   NO → iterar
                                   SÍ → Final Answer
```

**Diferencia crítica frente a prompting lineal:**
- No asume que el primer razonamiento es suficiente
- Obliga evidencia intermedia antes de cerrar

### CoT vs ReAct: Comparison Table

| Aspecto | CoT | ReAct |
|---------|-----|-------|
| **Propósito** | Razonamiento explícito | Razonamiento + Acción |
| **Estructura** | Pasos de pensamiento lineales | Ciclo Thought → Action → Observation |
| **Herramientas** | No (solo razonamiento) | Sí (tools críticos) |
| **Iteraciones** | 1 (una generación) | Múltiples (hasta criterio de parada) |
| **Complejidad** | Media | Alta |
| **Costo** | 2-3x prompt directo | 4-6x prompt directo |
| **Latencia** | +50-100% vs directo | +200-400% vs directo (múltiples llamadas) |
| **Debugging** | Razonamiento visible | Razonamiento + trace de tools |
| **Failure mode** | Razonamiento incorrecto | Loops infinitos, tool failures |
| **Best for** | Problemas de razonamiento puro | Problemas que requieren acciones |

### Heurística de Decisión: ¿Cuándo usar qué?

**Usa Chain of Thought (CoT) cuando:**
- El problema requiere razonamiento secuencial SIN acciones intermedias
- Puedes resolver con un solo prompt (entrada → razonamiento → salida)
- No necesitas tools/herramientas externas
- Ejemplo: "Diseña un mensaje personalizado basado en un perfil"

**Usa ReAct cuando:**
- El problema requiere ciclos de razonamiento + acción
- Necesitas tools (búsqueda, validación, API calls)
- El agente debe adaptarse según observaciones intermedias
- Necesitas guardrails (forzar protocolo, evitar agent drift)
- Ejemplo: "Analiza perfil → Genera mensaje → Audita respeto → Responde"

**Usa Prompt Directo cuando:**
- Tarea simple y factual
- No requiere razonamiento complejo
- Costo/latencia críticos
- Ejemplo: "Extrae el nombre del texto"

### Arquitectura ReAct: 3 componentes clave

**1. TOOLS (Herramientas con contratos explícitos)**

```python
def tool_analizar_perfil(profile: dict) -> dict:
    """
    INPUT: dict con tipo_persona, gustos, estilo, contexto
    OUTPUT: dict con persona, estilo_preferido, insights
    FUNCIÓN: Transforma texto de perfil en señales accionables
    """
    # Función pura: mismo input → mismo output
    # No side effects (no API calls, no estado global)
```

**Principios de Tool Design:**
- Una tool = una responsabilidad
- Input/output tipos explícitos
- Función pura cuando sea posible (idempotencia)
- Validación de input explícita
- En producción: usar Pydantic para tool I/O

**2. AGENT LOOP (Ciclo Thought → Action → Observation)**

```python
for iteration in range(max_iterations):
    step = model_next_action(client, model, state)
    action = step["action"]

    if action == "ANALIZAR_PERFIL":
        state["analysis"] = tool_analizar_perfil(state["profile"])
    elif action == "GENERAR_MENSAJE":
        state["draft_message"] = tool_generar_mensaje(...)
    elif action == "AUDITAR_RESPETO":
        state["audit"] = tool_auditar_respeto(...)
    elif action == "FINAL_ANSWER":
        return state
```

**3. GUARDRAILS (Forced protocol enforcement)**

```python
# State machine esperado: ANALIZAR → GENERAR → AUDITAR → FINAL
if state["analysis"] is None:
    expected_action = "ANALIZAR_PERFIL"
elif state["draft_message"] is None:
    expected_action = "GENERAR_MENSAJE"
elif state["audit"] is None:
    expected_action = "AUDITAR_RESPETO"
else:
    expected_action = "FINAL_ANSWER"

if action != expected_action:
    # Override: forzar protocolo
    action = expected_action
```

**¿Por qué forced protocol?**
- PROBLEMA SIN GUARDRAILS: Agent puede saltar pasos, loops infinitos, orden incorrecto
- SOLUCIÓN: State machine enforcement
- TRADE-OFF: Menos "autonomía", más predictibilidad
- En producción: predictibilidad > autonomía creativa

### Implementación en este repositorio

**Scripts:**
```bash
uv run python 02-prompting/ReAct/Notebooks/01_react_agente_coqueto.py
uv run python 02-prompting/ReAct/Notebooks/02_react_personas_feedback_loop.py
```

**Notebooks:**
- `02-prompting/ReAct/Notebooks/react_agente_aplicado.ipynb`

---

## ADVERTENCIA CRÍTICA: CoT y ReAct NO son balas de plata

Ambos:
- **Amplifican buen contexto**: Si el contexto es claro, estructurado y completo → outputs mejores
- **Amplifican mal contexto**: Si el contexto es vago, ambiguo o incompleto → outputs peores (y más caros)

**Principio fundamental**: Contexto > Técnica de prompting

Si tus outputs son malos con CoT/ReAct, el problema probable es:
1. Contexto insuficiente o mal estructurado
2. ROLE no define comportamiento claramente
3. TASK es ambigua
4. OUTPUT FORMAT no es validable

Arregla el contexto primero, optimiza la técnica después.

---

## Output Format Evolution: JSON vs Pydantic

Este curso enseña **dos approaches** para validar outputs de LLMs:

### Approach 1: JSON (Ejemplos 01, 02)

**Código típico:**
```python
response = client.chat.completions.create(
    model=model,
    messages=[...],
    response_format={"type": "json_object"},
    temperature=0.7
)

content = response.choices[0].message.content
result = json.loads(content)  # ¿Qué pasa si JSON inválido?

# Validación manual
opener = result.get("opener", "")
if not opener:
    raise ValueError("opener vacío")
```

**Ventajas:**
- Simple, directo, fácil de aprender
- Ideal para entender conceptos de CoT/ReAct
- Menos boilerplate inicial

**Problemas:**
- Stringly-typed (todo son strings sin validación)
- No validación en tiempo de definición
- No autocomplete en IDE
- Fácil olvidar validaciones críticas
- Refactoring propenso a errores

**Úsalo para**: Aprendizaje, prototipado rápido, scripts de una sola vez

### Approach 2: Pydantic (Ejemplos 03, 04)

**Código típico:**
```python
from pydantic import BaseModel, Field

class ConversationRecommendation(BaseModel):
    opener: str = Field(..., min_length=10, max_length=150)
    follow_up: str = Field(..., min_length=10, max_length=150)
    tone_notes: list[str] = Field(..., min_length=1)
    avoid: list[str] = Field(..., min_length=1)

# Uso con OpenAI structured outputs
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[...],
    response_format=ConversationRecommendation
)
result = completion.choices[0].message.parsed  # Type-safe!
```

**Ventajas:**
- Type-safe: validación automática de tipos
- Validación en definición: errores antes de ejecutar
- IDE autocomplete funciona perfectamente
- Serialización automática: JSON ↔ Python objects
- Documentación automática: schema generation
- Refactoring seguro

**Trade-offs:**
- Más código inicial (definir modelos)
- Curva de aprendizaje (conocer Pydantic)
- Dependencia extra (pero ya es estándar en Python moderno)

**Úsalo para**: Producción, trabajo en equipo, esquemas complejos (5+ campos)

### Cuándo usar qué

**Usa JSON cuando:**
- Prototipado rápido (iterando sobre ideas)
- Aprendiendo conceptos fundamentales (CoT, ReAct)
- Esquemas muy simples (2-3 campos)
- Scripts de una sola vez

**Usa Pydantic cuando:**
- Sistemas de producción (robustez > velocidad)
- Esquemas complejos (5+ campos, nested structures)
- Trabajo en equipo (contratos claros)
- Cuando importa robustez (sistemas críticos, costos altos por fallos)
- Integración con frameworks (FastAPI, Django Ninja)

### Pydantic Features en este curso

**1. Field Constraints**
```python
class ConversationRecommendation(BaseModel):
    opener: str = Field(
        ...,                # Required
        min_length=10,      # Mínimo 10 caracteres
        max_length=150,     # Máximo 150 caracteres
        description="Mensaje inicial para conversación"
    )
```

**2. Custom Validators**
```python
class ChainOfThought(BaseModel):
    chain_of_thought: list[str] = Field(..., min_length=4, max_length=4)

    @field_validator('chain_of_thought')
    @classmethod
    def validate_cot_quality(cls, v: list[str]) -> list[str]:
        """Valida que cada paso sea sustantivo."""
        for i, step in enumerate(v, 1):
            if len(step.split()) < 3:
                raise ValueError(f"Paso {i} muy corto: '{step}'")
        return v
```

**3. Nested Models (ReAct State Management)**
```python
class ReActStep(BaseModel):
    thought: str = Field(..., min_length=10)
    action: Literal["ANALIZAR_PERFIL", "GENERAR_MENSAJE", "AUDITAR_RESPETO", "FINAL_ANSWER"]
    action_input: dict[str, Any]
    observation: Optional[str] = None

class AgentState(BaseModel):
    profile: dict[str, Any]
    analysis: Optional[dict[str, Any]] = None
    draft_message: Optional[dict[str, Any]] = None
    audit: Optional[dict[str, Any]] = None
    trace: list[ReActStep] = Field(default_factory=list)
```

### Errores Comunes con Pydantic

**Error 1: Confundir `...` con `None`**
```python
# INCORRECTO: Campo "opcional" pero sin default
class Foo(BaseModel):
    bar: str  # Esto es REQUIRED

# CORRECTO: Campo opcional
class Foo(BaseModel):
    bar: Optional[str] = None
```

**Error 2: Olvidar `default_factory` para listas/dicts**
```python
# INCORRECTO: Lista compartida entre instancias (mutable default)
class Foo(BaseModel):
    items: list[str] = []  # BUG!

# CORRECTO: Usar default_factory
class Foo(BaseModel):
    items: list[str] = Field(default_factory=list)
```

**Error 3: No manejar ValidationError**
```python
# CORRECTO: Manejar ValidationError
from pydantic import ValidationError

try:
    result = ConversationRecommendation(**data)
except ValidationError as e:
    print(f"Validación falló: {e}")
```

### Performance Considerations

Pydantic es rápido (usa Rust internamente desde v2):
```
Benchmark típico:
- JSON parsing: ~10µs
- Pydantic validation: ~50µs
- Diferencia: +40µs por request

En contexto de LLM API call:
- LLM latency: 500-2000ms (500,000-2,000,000µs)
- Pydantic overhead: 50µs = 0.01% del tiempo total
```

**No optimices prematuramente.** Pydantic no es tu cuello de botella (el LLM sí lo es).

### Resumen Ejecutivo: JSON vs Pydantic

| Aspecto | JSON | Pydantic |
|---------|------|----------|
| **Complejidad inicial** | Baja | Media |
| **Type safety** | No | Sí |
| **Validación automática** | No | Sí |
| **IDE autocomplete** | No | Sí |
| **Refactoring seguro** | No | Sí |
| **Debugging** | Manual | Automático (ValidationError) |
| **Performance overhead** | 0µs | ~50µs (despreciable) |
| **Mejor para** | Prototipado, aprendizaje | Producción, equipos |

**Recomendación pedagógica:**
1. Aprende primero con JSON (ejemplos 01, 02): Enfócate en CoT/ReAct
2. Luego revisa Pydantic (ejemplos 03, 04): Enfócate en robustez

---

## Estructura del directorio

```text
02-prompting/
├── README.md                           # Este archivo
├── COT/
│   └── Notebooks/
│       ├── 01_zero_shot_cot_recomendador.py       # JSON
│       ├── 02_few_shot_cot_feedback_loop.py       # JSON
│       ├── 03_zero_shot_cot_pydantic.py           # Pydantic
│       ├── 04_few_shot_cot_pydantic.py            # Pydantic
│       ├── cot_recomendador_aplicado.ipynb        # JSON
│       └── cot_pydantic_aplicado.ipynb            # Pydantic
├── ReAct/
│   └── Notebooks/
│       ├── 01_react_agente_coqueto.py             # JSON
│       ├── 02_react_personas_feedback_loop.py     # JSON
│       ├── 03_react_agente_pydantic.py            # Pydantic
│       ├── 04_react_personas_pydantic.py          # Pydantic
│       ├── react_agente_aplicado.ipynb            # JSON
│       └── react_pydantic_aplicado.ipynb          # Pydantic
├── common/
│   ├── rubrica.py                  # Dict-based evaluation
│   └── rubrica_pydantic.py         # Type-safe evaluation
└── tools/
    └── execute_notebooks.py
```

---

## Entorno y ejecución

**Instalación con uv:**
```bash
make install-prompting
```

**Requisitos de `.env`:**
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

**Ejecutar scripts:**
```bash
# Ejemplos JSON (01, 02)
make run-cot
make run-react

# Ejemplos Pydantic (03, 04)
make run-cot-pydantic
make run-react-pydantic

# Todos los ejemplos
make run-all-prompting
```

**Ejecutar notebooks:**
```bash
make run-notebooks
```

**Artefactos generados:**
- `02-prompting/COT/Notebooks/cot_recomendador_aplicado.executed.ipynb`
- `02-prompting/ReAct/Notebooks/react_agente_aplicado.executed.ipynb`

---

## Ruta sugerida de estudio

### Semana 1: Fundamentos (JSON)
1. Lee "Fundamentos de Prompt Engineering" en README principal (estructura de 5 capas)
2. Ejecuta `01_zero_shot_cot_recomendador.py` y estudia mapeo a 5 capas
3. Ejecuta `02_few_shot_cot_feedback_loop.py` y compara consistencia/costo vs zero-shot
4. Estudia diferencias CoT vs ReAct en este README
5. Ejecuta `01_react_agente_coqueto.py` y observa ciclo Thought → Action → Observation
6. Ejecuta `02_react_personas_feedback_loop.py` con múltiples personas
7. Ejecuta notebooks con `make run-notebooks` y revisa mejora por feedback loop

### Semana 2: Producción (Pydantic - Opcional)
1. Lee sección "Output Format Evolution: JSON vs Pydantic" en este README
2. Compara `01_zero_shot_cot_recomendador.py` vs `03_zero_shot_cot_pydantic.py` lado a lado
3. Ejecuta ejemplos Pydantic: `make run-cot-pydantic && make run-react-pydantic`
4. Revisa notebooks Pydantic para ver validación en acción
5. Experimenta provocando ValidationErrors intencionales
6. Ajusta la rúbrica en `rubrica_pydantic.py` para tus propios criterios

**Si completas esta secuencia, no solo entiendes prompting: entiendes diseño de sistemas de prompting robustos y producción-ready.**

---

## Recursos adicionales

- [Pydantic Documentation](https://docs.pydantic.dev/) - Official docs
- [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs) - Integración con OpenAI
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web que usa Pydantic extensivamente

---

**Principio fundamental:**
Buen prompting no es agregar complejidad; es usar la **mínima complejidad que garantiza calidad medible**.
