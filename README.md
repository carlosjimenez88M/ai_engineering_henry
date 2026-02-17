![](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)

# AI Engineering - Henry

Curso practico de AI Engineering. Vas de cero a construir sistemas AI que funcionan en produccion, no solo demos.

Basado en los principios de **Chip Huyen** (*AI Engineering* y *Designing Machine Learning Systems*).

## Que vas a aprender

- Cuando usar AI vs software tradicional (y cuando combinarlos)
- Prompting aplicado: CoT, ReAct, feedback loops
- Orquestacion con LangChain y LangGraph
- RAG: darle memoria y conocimiento externo a un LLM
- Proyecto integrador: sistema multi-agente con routing y RAG

## Estructura del Curso

### Clase 1: Software vs AI Engineering
Comparacion critica entre desarrollo tradicional y AI Engineering. Ejemplo practico: sistema de brief generation con OpenAI, testing, metricas y observabilidad.

**Ubicacion:** `01-introduction/`

### Clase 2: Prompting Aplicado (CoT + ReAct)
Estrategias Chain of Thought (zero-shot y few-shot), ReAct con herramientas, feedback loops con rubrica. Notebooks ejecutables con OpenAI API.

**Ubicacion:** `02-prompting/`

### Clase 3: LangChain Prompting Avanzado
Migracion de tecnicas de Clase 2 a LangChain: `ChatPromptTemplate`, `FewShot`, salida estructurada. ReAct con tools, guardrails y context engineering aplicado.

**Ubicacion:** `03_langchain_prompting/`

### Clase 4: LangGraph Workflows y Agents
Workflows de LangGraph: prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer. Agent con tools y feedback loop de calidad.

**Ubicacion:** `04_langchain_langgraph/`

### Clase 5: RAG y Bases de Datos Vectoriales
Retrieval-Augmented Generation: chunking, embeddings, vector stores, retrieval hibrido, re-ranking. RAG con agentes usando prompt chaining y routing.

**Ubicacion:** `05_Rags/`

### Proyecto: Multi-Agent Router + Domain RAG
Sistema multi-agente con clasificacion de intencion, routing condicional por dominio (HR/Tech), agentes RAG especializados, memoria de conversacion y trazabilidad.

**Ubicacion:** `06_project/`

### Material Complementario: Python Extra Class
Curso intensivo de Python desde base, con foco en uso profesional para AI/ML. Incluye fundamentos, OOP, ejercicios tipo LeetCode, Pydantic y ejemplos ejecutables.

**Ubicacion:** `python_extra_class/`

## Comenzando

### Requisitos

- **Python 3.12+**
- **uv** ([instalacion](https://github.com/astral-sh/uv))
- **API key de OpenAI** ([obtener aqui](https://platform.openai.com/api-keys))

### Instalacion

```bash
git clone https://github.com/yourusername/ai_engineering_henry.git
cd ai_engineering_henry

# Instalar dependencias
make install

# Configurar API key
cp .env.example .env
# Edita .env y agrega tu OPENAI_API_KEY

# Verificar que todo funciona
make test-se
```

### Primer comando

```bash
make run-ai
```

Genera un brief comparativo en `01-introduction/ai_engineering/briefs/`. Con contexto personalizado:

```bash
make run-ai-context CONTEXT="Startup de fintech B2B"
```

## Como sacarle el maximo a este curso

1. **Ejecuta antes de leer.** Corre el notebook o ejemplo primero. Despues lee la teoria. Entender el "que hace" antes del "por que" acelera el aprendizaje.
2. **Rompe cosas a proposito.** Cambia un prompt, quita un guardrail, baja la temperature a 0. Observa que pasa. Los errores ensenian mas que los ejemplos felices.
3. **Sigue el orden.** Cada clase construye sobre la anterior. Saltarte una te deja con huecos que se acumulan.
4. **Lee el codigo, no solo la documentacion.** Los READMEs explican el "que" y el "por que". El codigo muestra el "como". Ambos importan.
5. **Mide.** Tokens, latencia, costos, calidad. Si no lo mides, no lo entiendes. Este curso insiste en metricas porque la industria las exige.

## Distribucion del Repositorio

```
ai_engineering_henry/
├── 01-introduction/                        # Clase 1: Software vs AI Engineering
│   ├── ai_engineering/                     # Ejemplo AI Engineering
│   │   ├── brief_builder/                  # Sistema de generacion de briefs
│   │   ├── tests/                          # Tests del sistema AI
│   │   └── briefs/                         # Briefs generados
│   ├── python_software_engineering/        # Ejemplo Software tradicional
│   │   ├── src/                            # Logica de negocio determinista
│   │   └── tests/                          # Tests unitarios
│   └── sildes/                             # Slides de la clase
│
├── 02-prompting/                           # Clase 2: CoT + ReAct
│   ├── COT/Notebooks/                      # Notebooks Chain of Thought
│   ├── ReAct/Notebooks/                    # Notebooks ReAct
│   ├── Prompt_Introduction/                # Introduccion a prompting
│   ├── Prompt_chaining/                    # Prompt chaining
│   ├── Routing/                            # Routing basico
│   ├── common/                             # Utilidades compartidas
│   └── tools/                              # Herramientas de ejecucion
│
├── 03_langchain_prompting/                 # Clase 3: LangChain avanzado
│   ├── COT_LangChain/Notebooks/            # CoT con LangChain
│   ├── ReAct_LangChain/Notebooks/          # ReAct con LangChain
│   ├── common/                             # Utilidades compartidas
│   └── tools/                              # Herramientas de ejecucion
│
├── 04_langchain_langgraph/                 # Clase 4: LangGraph
│   ├── 01_prompt_chaining/Notebooks/       # Prompt chaining
│   ├── 02_parallelization/Notebooks/       # Parallelization
│   ├── 03_orchestrator_worker/Notebooks/   # Orchestrator-worker
│   ├── 04_evaluator_optimizer/Notebooks/   # Evaluator-optimizer
│   ├── 05_routing/Notebooks/               # Routing
│   ├── 06_agent_feedback/Notebooks/        # Agent feedback loop
│   ├── common/                             # Utilidades compartidas
│   └── tools/                              # Herramientas de ejecucion
│
├── 05_Rags/                                # Clase 5: RAG
│   ├── data/                               # Bases de conocimiento de ejemplo
│   └── Notebooks/                          # Notebooks RAG
│
├── 06_project/                             # Proyecto: Multi-Agent Router
│   ├── data/                               # Documentos HR y Tech
│   │   ├── hr/                             # Manual RRHH
│   │   └── tech/                           # Runbook tecnico
│   ├── src/multi_agent_system/             # Codigo fuente del sistema
│   └── tests/                              # Tests de routing
│
├── python_extra_class/                     # Material complementario: Python
│   ├── 00_setup/                           # Entorno reproducible
│   ├── 01_programacion_python/             # Fundamentos hasta Pydantic
│   ├── 02_oop_python/                      # OOP para AI/ML
│   ├── 03_ejercicios_leetcode/             # Pensamiento algoritmico
│   └── 04_ejemplos_runnable/               # Ejemplos ejecutables
│
├── Makefile                                # Comandos de desarrollo
├── pyproject.toml                          # Dependencias y configuracion
├── .env.example                            # Template de variables de entorno
└── README.md                               # Este archivo
```

## Comandos Disponibles

### Ejecucion

```bash
# Clase 1
make run-ai                                 # Generar brief basico
make run-ai-context CONTEXT="texto"         # Brief con contexto personalizado
make run-se                                 # Ejemplo de software clasico

# Clase 2
make run-cot                                # Ejemplos CoT (JSON)
make run-react                              # Ejemplos ReAct (JSON)
make run-cot-pydantic                       # CoT con Pydantic (type-safe)
make run-react-pydantic                     # ReAct con Pydantic (type-safe)
make run-all-prompting                      # Todos los ejemplos de prompting
make run-notebooks                          # Ejecutar notebooks Clase 02

# Clase 3
make run-cot-langchain                      # CoT con LangChain
make run-react-langchain                    # ReAct con LangChain
make run-notebooks-langchain                # Ejecutar notebooks Clase 03

# Clase 4
make run-langgraph-architectures            # Todas las arquitecturas LangGraph
make run-notebooks-langgraph                # Ejecutar notebooks Clase 04

# Proyecto
make run-project QUERY="tu consulta"        # Ejecutar sistema multi-agente
```

### Testing

```bash
make test-se                                # Tests software engineering
make test-ai                                # Tests AI engineering
make test-ai-cov                            # Tests AI con cobertura
make test-project                           # Tests del proyecto
make test-all                               # Todos los tests
```

### Utilidades

```bash
make install                                # Instalar dependencias
make lint                                   # Verificar estilo (ruff)
make format                                 # Formatear codigo (ruff)
make check                                  # Verificar sintaxis Python
make clean                                  # Limpiar artefactos
```

## Recursos

### Libros
- **"AI Engineering"** - Chip Huyen (O'Reilly)
- **"Designing Machine Learning Systems"** - Chip Huyen

### Referencias
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) - Google

## Notas de Seguridad

**Nunca subas secretos a Git.** El `.gitignore` ya previene esto, pero:

1. Usa `.env` para secrets (nunca hardcodees API keys)
2. Rota API keys si sospechas exposicion
3. Limita permisos de API keys
4. Monitorea uso en el dashboard de OpenAI
5. Configura spending limits en tu cuenta

Si expones un secret: revoca la key inmediatamente en OpenAI dashboard, genera una nueva, y actualiza tu `.env`.

## Contribuyendo

Si encuentras bugs, documentacion poco clara, o ideas para mejorar: abre un issue o pull request.

## Licencia

Material propiedad de Henry Academy. Disponible para estudiantes del programa. No redistribuir sin autorizacion.


