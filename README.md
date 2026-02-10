![](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)

# AI Engineering - Henry 

Bienvenido al curso de AI Engineering de Henry. Este repositorio contiene material práctico diseñado para estudiantes que quieren entender las diferencias fundamentales entre Software Engineering tradicional y AI Engineering moderno, siguiendo los principios de **Chip Huyen** ("Designing Machine Learning Systems" y "AI Engineering").

## ¿Por qué este curso?

En la industria tech actual, no basta con saber usar un LLM API. Los mejores AI Engineers entienden:
- Cómo diseñar sistemas que sean **reproducibles, testeables y observables**
- Cuándo usar AI vs software tradicional (y cuándo combinarlos)
- Cómo medir costos, latencia y calidad en sistemas AI
- Patrones de producción que separan prototipos de sistemas reales

Este curso te prepara para construir sistemas AI que escalan en producción, no solo demos que funcionan una vez.

## Estructura del Curso

El curso se divide en 4 clases progresivas:

### **Clase 1: Software vs AI Engineering** 
**Estado:** Completa y lista para usar

Contenido:
- Comparación crítica: ¿Cuándo usar qué?
- Ejemplo práctico: Sistema de brief generation con OpenAI
- Testing, validación, métricas y observabilidad
- Trade-offs y anti-patrones comunes

**Ubicación:** `01_class/`

### **Clase 2: Prompting aplicado (CoT + ReAct)** 
**Estado:** Completa y lista para usar

Contenido:
- Estrategias Chain of Thought: Zero-shot y Few-shot
- Estrategias ReAct: razonamiento + acción con herramientas
- Feedback loop y auto-crítica con rúbrica
- Notebooks ejecutables con OpenAI API

**Ubicación:** `02-prompting/`

### **Clase 3: LangChain Prompting Avanzado (CoT + ReAct + Context Engineering)** 
**Estado:** Completa y lista para usar

Contenido:
- Qué es LangChain y cuándo usarlo en problemas reales
- Migración de técnicas de `02-prompting` a `ChatPromptTemplate`, `FewShot` y salida estructurada
- ReAct con tools, guardrails y trazabilidad de estado
- Context engineering aplicado para mejorar calidad/costo/latencia
- Notebooks ejecutables con validación automática

**Ubicación:** `03_langchain_prompting/`

### **Clase 4: LangGraph Workflows y Agents** 
**Estado:** Completa y lista para usar

Contenido:
- Workflows oficiales de LangGraph aplicados: prompt chaining, parallelization, routing
- Arquitecturas avanzadas: orchestrator-worker y evaluator-optimizer
- Agent con tools y feedback loop de calidad
- Notebooks ejecutables por arquitectura

**Ubicación:** `04_langchain_langgraph/`

## Comenzando

### Requisitos Previos

- **Python 3.10 o superior**
- **Cuenta de OpenAI** con API key activa ([obtener aquí](https://platform.openai.com/api-keys))
- **uv** instalado ([instrucciones de instalación](https://github.com/astral-sh/uv))
- Conocimientos básicos de:
  - Python (funciones, clases, imports)
  - Terminal/CLI
  - Git (opcional pero recomendado)

### Instalación Paso a Paso

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/yourusername/ai_engineering_henry.git
   cd ai_engineering_henry
   ```

2. **Instala dependencias con uv:**
   ```bash
   make install
   # o directamente: uv sync
   ```

3. **Configura tu API key de OpenAI:**

   Crea un archivo `.env` en la raíz del proyecto:
   ```bash
   cp .env.example .env
   ```

   Edita `.env` y agrega tu API key:
   ```
   OPENAI_API_KEY=sk-proj-tu-api-key-aqui
   OPENAI_MODEL=gpt-4o-mini  # opcional, default: gpt-4o-mini
   ```

4. **Verifica la instalación:**
   ```bash
   make test-se
   ```

   Si ves tests pasando, ¡estás listo! 

### Primer Comando

Genera tu primer brief comparativo:
```bash
make run-ai
```

El brief se guardará en `01_class/ai_engineering/briefs/software_vs_ai_engineering.md`.

Con contexto personalizado:
```bash
make run-ai-context CONTEXT="Startup de fintech B2B"
```

## Filosofía del Curso

Este curso sigue los principios de **Chip Huyen** sobre sistemas AI en producción:

### 1. **Reproducibilidad**
- Versionamos prompts en Git
- Trackeamos model version, temperature y parámetros
- Logs detallados para debugging

### 2. **Modularidad**
- Separación clara de concerns (config, prompts, validation, metrics)
- Componentes reusables y testeables
- No "God functions" que hacen todo

### 3. **Testing Riguroso**
- Tests unitarios para lógica de negocio
- Tests de integración con mocks de APIs
- Validación de inputs y outputs
- Target: 85%+ code coverage

### 4. **Observabilidad**
- Métricas de costo por request
- Latency tracking
- Quality checks automatizados
- Error logging estructurado

### 5. **Error Handling Resiliente**
- Retry logic con exponential backoff
- Excepciones específicas (no "catch all")
- Graceful degradation cuando sea posible

### 6. **Budget Awareness**
- Estimación de costos antes de ejecutar
- Logs de tokens y USD por operación
- Alertas cuando se exceden thresholds

## Fundamentos de Prompt Engineering

### Premisa Central: Los Agentes Dependen del Contexto

**Principio fundamental**: La calidad del razonamiento de un agente es directamente proporcional a la claridad y completitud del contexto que recibe.

- **Agente** = Sistema LLM + Herramientas + Contexto + Ciclo de retroalimentación
- **Buen contexto** = comportamiento consistente, predecible, eficiente en costos
- **Contexto vago** = alucinaciones, inconsistencia, explosión de costos

**Ejemplo:**
-  Contexto débil: "Aquí hay info del usuario"
-  Contexto fuerte: "Usuario: 28 años, preferencias: [jazz, fotografía], estilo conversacional: inteligente y ligero, contexto: primer mensaje tras match"

### Anatomía de un Prompt de Producción

Todo prompt efectivo sigue esta estructura de 5 capas:

**1. ROLE (Quién es el agente)**
```
"Eres un coach conversacional elegante, respetuoso y práctico."
```
- Define identidad, expertise, valores
- Establece tono y límites éticos
- Siempre explícito, nunca implícito

**2. TASK (Qué debe hacer)**
```
"Diseña una recomendación de conversación personalizada basada en el perfil del usuario."
```
- Objetivo específico y medible
- Sin ambigüedad en el alcance
- Descomponer tareas complejas en subtareas

**3. OUTPUT FORMAT (Estructura requerida)**
```json
{
  "opener": "mensaje inicial",
  "follow_up": "pregunta de seguimiento",
  "tone_notes": ["observación 1", "observación 2"]
}
```
- JSON schema o Pydantic BaseModel
- Valida automáticamente
- Facilita integración downstream

**4. EXAMPLES (Comportamiento esperado - opcional)**
```
"Ejemplo de buen opener: '¿Qué cafés de Palermo recomendarías para...?'"
```
- Few-shot learning: 1-3 ejemplos de calidad
- Trade-off: +consistencia, +tokens/costo
- Usar cuando calidad > costo

**5. CONTEXT (Información específica)**
```python
profile = {
  "tipo_persona": "arquitecta apasionada por fotografía urbana",
  "gustos": ["cafés tranquilos", "jazz", "viajes cortos"],
  "contexto": "match reciente, primera interacción"
}
```
- Datos estructurados, no narrativos
- Incluir meta-información (fuente, confianza)
- Filtrar ruido, priorizar señales

**Aplicación en este curso:**
- **Clase 1**: brief_builder usa ROLE + TASK + FORMAT implícitamente
- **Clase 2**: COT añade razonamiento explícito; ReAct añade herramientas y ciclos
- **Clase 3**: LangChain formaliza prompts, tools y salida estructurada
- **Clase 4**: LangGraph lleva esta estructura a arquitecturas de orquestación

### Mejores Prácticas de AI Engineering

**1. Instrucciones Claras y No Ambiguas**
- Usa lenguaje imperativo: "Devuelve", "Analiza", "Genera"
- Evita lenguaje condicional vago: "tal vez", "podría"
- Especifica límites: longitud máxima, formato exacto, restricciones

**2. Siempre Define el Rol del Agente**
- Sin rol = agente asume personalidad genérica
- Rol explícito = comportamiento consistente
- Incluye valores éticos en el rol (respeto, consentimiento)

**3. Divide Tareas Complejas en Subtareas**
- Una tarea = una responsabilidad
- Cadena subtareas con estado explícito
- Ejemplo: ANALIZAR → GENERAR → AUDITAR → RESPONDER

**4. Especifica Formato de Salida Estrictamente**
- JSON schema con campos requeridos
- Pydantic BaseModel con validación (producción)
- Incluye tipos de datos y rangos permitidos

**5. Seguridad y Restricciones Éticas**
- Restricciones upfront en ROLE y TASK
- Auditoría automática de salidas (ver ReAct/audit)
- Nunca asumas que el modelo "sabe" ética implícitamente

**6. Proceso Iterativo con Evaluación**
- Primera versión → Evaluación con rúbrica → Feedback → Regeneración
- Métricas objetivas (ver rubrica.py)
- Itera hasta alcanzar umbral de calidad

### Errores Comunes y Diagnóstico

**Error 1: Ambigüedad en Instrucciones**
-  Problema: "Genera un mensaje simpático"
-  Solución: "Genera un mensaje de 15-25 palabras que incluya una pregunta sobre [tema del perfil]"
- **Impacto**: Inconsistencia, outputs impredecibles, debugging difícil

**Error 2: Contradicciones en el Prompt**
-  Problema: "Sé breve" + "Explica detalladamente"
-  Solución: Prioriza explícitamente o separa en dos llamadas
- **Impacto**: Modelo elige arbitrariamente, resultados varían por ejecución

**Error 3: Asumir que el LLM "Lee la Mente"**
-  Problema: "El usuario quiere algo interesante"
-  Solución: Proporciona gustos explícitos del perfil como contexto estructurado
- **Impacto**: Alucinaciones, outputs genéricos, baja personalización

**Error 4: Falta de Validación de Salidas**
-  Problema: Asumir que la API siempre devuelve formato correcto
-  Solución: Valida con JSON schema o Pydantic antes de usar
- **Impacto**: Errores en sistemas downstream, fallos silenciosos

**Error 5: Prompt Injection**
-  Problema: Concatenar input del usuario directamente en prompts
-  Solución: Sanitiza inputs, usa delimitadores claros, valida antes de insertar
- **Impacto**: Usuarios maliciosos pueden alterar comportamiento del agente

**Error 6: Explosión de Contexto**
-  Problema: Meter documentos completos sin procesar
-  Solución: Resume, extrae hechos clave, estructura jerárquicamente
- **Impacto**: Costos inmanejables, timeouts, degradación de calidad

**Error 7: Temperatura Incorrecta**
-  Problema: Usar temperature=1.5 para tareas determinísticas
-  Solución: 0.1-0.3 para consistencia, 0.7+ para creatividad
- **Impacto**: Variabilidad impredecible, costos más altos por reintentos

**Error 8: No Estimar Costos Antes de Producción**
-  Problema: Desplegar sin calcular tokens/request típico
-  Solución: Calcula (input_tokens + output_tokens) × precio × volumen_esperado
- **Impacto**: Sobrecostos, necesidad de rediseño de emergencia

### Conexión con Clases del Curso

Esta estructura se aplica progresivamente:

- **Clase 1** (brief_builder): Prompt simple con ROLE + TASK + FORMAT
- **Clase 2** (CoT/ReAct): Añade razonamiento explícito y herramientas
  - COT: Descompone razonamiento en pasos visibles
  - ReAct: Añade ciclo Thought → Action → Observation
- **Clase 3** (LangChain): Orquestación con templates, tools y context engineering
- **Clase 4** (LangGraph): Patrones de workflows y agents para sistemas compuestos

Ver `02-prompting/`, `03_langchain_prompting/` y `04_langchain_langgraph/` para aplicación práctica de estos conceptos.

## Distribución del Repositorio

```
ai_engineering_henry/
├── 01_class/                    # Clase 1: Software vs AI Engineering
│   ├── ai_engineering/          # Ejemplo de AI Engineering
│   │   ├── brief_builder/       # Sistema de generación de briefs
│   │   │   ├── main.py         # Entry point con CLI
│   │   │   ├── config.py       # Configuración y secrets
│   │   │   ├── prompts.py      # Prompts versionados
│   │   │   ├── validator.py    # Validación de inputs/outputs
│   │   │   ├── exceptions.py   # Excepciones específicas
│   │   │   ├── retry.py        # Retry logic con backoff
│   │   │   ├── metrics.py      # Tracking de costos/latencia
│   │   │   └── logger.py       # Logging estructurado
│   │   ├── tests/              # Tests del sistema AI
│   │   ├── briefs/             # Briefs generados
│   │   └── README.md           # Guía detallada de Clase 1
│   │
│   └── python_software_engineering/  # Ejemplo de Software tradicional
│       ├── src/app.py          # Lógica de negocio determinista
│       └── tests/test_app.py   # Tests unitarios
│
├── Makefile                    # Comandos para desarrollo
├── pyproject.toml             # Dependencias y configuración
├── .env.example               # Template para variables de entorno
└── README.md                  # Este archivo
```

## Comandos Disponibles

### Desarrollo
```bash
make install        # Instalar dependencias
make install-prompting  # Instalar entorno de Clase 02 con uv
make run-ai         # Generar brief básico
make run-ai-context CONTEXT="texto"  # Brief con contexto
make run-se         # Ejecutar ejemplo de software clásico
make run-cot        # Ejecutar ejemplos CoT
make run-react      # Ejecutar ejemplos ReAct
make run-notebooks  # Ejecutar notebooks de Clase 02
```

### Testing
```bash
make test-se        # Tests de software engineering
make test-ai        # Tests de AI engineering
make test-all       # Todos los tests
make test-ai-cov    # Tests con reporte de cobertura
```

### Utilidades
```bash
make check          # Verificar sintaxis Python
make clean          # Limpiar artefactos
```

## Recursos Adicionales

### Libros Recomendados
- 📚 **"Designing Machine Learning Systems"** - Chip Huyen
  - Capítulos clave: 5 (Model Development), 7 (Monitoring), 8 (Data Distribution Shifts)
- 📚 **"AI Engineering"** - Chip Huyen
  - Especialmente: Resilient Systems, Evaluation, Production Patterns

### Artículos y Referencias
- [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) - Google
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [The Twelve-Factor App](https://12factor.net/) - Metodología para aplicaciones modernas

### Comunidad Henry
- 💬 **Slack:** Canal #ai-engineering
- 📧 **Email:** ai-support@soyhenry.com
-  **Office Hours:** Consulta el calendario interno

## Notas de Seguridad

###  IMPORTANTE: Nunca subas secretos a Git

El `.gitignore` está configurado para prevenir:
-  Claves API (`.env`, archivos `secrets.*`)
-  Certificados y llaves privadas (`.pem`, `.key`)
-  Entornos virtuales (`.venv/`, `venv/`)
-  Artefactos de desarrollo (`__pycache__`, `.pytest_cache`)

### Buenas Prácticas

1. **Usa `.env` para secrets** (nunca hardcodees API keys)
2. **Rotate API keys** si sospechas exposición
3. **Limita permisos** de API keys (solo los necesarios)
4. **Monitorea uso** en el dashboard de OpenAI
5. **Set spending limits** en tu cuenta de OpenAI

### ¿Qué hacer si expones un secret?

1. **Inmediatamente:** Revoca la API key en OpenAI dashboard
2. **Genera nueva key** y actualiza tu `.env`
3. **Reporta** al equipo si fue en repo compartido
4. **Aprende:** Usa `git-secrets` o pre-commit hooks

## Contribuyendo

Este es un curso en evolución. Si encuentras:
- 🐛 Bugs o errores
- 📝 Documentación poco clara
- 💡 Ideas para mejorar
- 🎯 Ejemplos adicionales que ayudarían

Por favor abre un issue o pull request. Todas las contribuciones son bienvenidas.

## Licencia

Este material es propiedad de Henry Academy y está disponible para estudiantes del programa. No redistribuir sin autorización.

---

## Próximos Pasos

1.  Completa la **Clase 1** siguiendo `01_class/README.md`
2. 🧪 Experimenta con diferentes valores de `temperature` y observa los resultados
3.  Revisa los archivos `.metrics.json` para entender costos
4. 🧐 Lee el brief generado y compáralo con el prompt
5. 🔍 Explora el código en `brief_builder/` para ver los patrones

**¿Listo para empezar?** → Ve a `01_class/README.md`

---

**Made with ❤️ by Henry Academy**

*"The best way to predict the future is to build it."* - Alan Kay
