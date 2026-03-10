![](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)

# AI Engineering - Henry

Repositorio docente para el curso de AI Engineering de Henry. El material esta organizado por modulo, luego por tema, y finalmente por notebooks o proyectos aplicados. La prioridad de esta estructura es que un estudiante nuevo pueda entender rapido:

1. que estudiar primero,
2. donde esta cada clase,
3. que necesita instalar,
4. como ejecutar ejemplos, notebooks y tests sin adivinar rutas.

## Recorrido recomendado

| Orden | Modulo | Objetivo | Ruta |
|---|---|---|---|
| 0 | Python extra class | Nivelar Python profesional para AI/ML | `01-Introduction_AI_Engineering/00_python_extra_class/` |
| 1 | Introduccion a AI Engineering | Entender AI vs software tradicional | `01-Introduction_AI_Engineering/01_introduction/` |
| 2 | Prompting aplicado | CoT, ReAct, routing y feedback loops | `01-Introduction_AI_Engineering/02_prompting/` |
| 3 | LangChain prompting | Llevar prompting a patrones mas mantenibles | `01-Introduction_AI_Engineering/03_langchain_prompting/` |
| 4 | LangGraph workflows | Diseñar flujos, routers y agentes con estado | `01-Introduction_AI_Engineering/04_langchain_langgraph/` |
| 5 | RAG | Retrieval, vector stores y pipelines con contexto externo | `01-Introduction_AI_Engineering/05_rags/` |
| 6 | Proyecto integrador | Router multi-agente con RAG por dominio | `01-Introduction_AI_Engineering/06_project/` |
| 7 | Vector databases en profundidad | Fundamentos, produccion y casos aplicados | `02-vector_data_bases/` |
| 8 | Agentes | Fundamentos, frameworks, multi-agent y produccion | `03-agents/` |
| 9 | Deep Learning | Redes neuronales, PyTorch, CNNs, secuencias y transformers | `04-deep_learning/` |

## Requisitos

- Python `3.10+` recomendado `3.11` o `3.12`
- [`uv`](https://github.com/astral-sh/uv) para dependencias y ejecucion
- `git`
- API key de OpenAI para notebooks que usan LLMs
- `make` opcional pero recomendado en macOS/Linux

## Instalacion rapida

```bash
git clone <tu-fork-o-este-repo>
cd ai_engineering_henry
cp .env.example .env
make sync
make test
```

Cada modulo principal tambien tiene su propio `pyproject.toml`, asi que puedes instalarlo por separado:

```bash
cd 01-Introduction_AI_Engineering && uv sync --extra dev
cd 02-vector_data_bases && uv sync --extra dev
cd 03-agents && uv sync --extra dev
```

Si vas a trabajar dentro de `03-agents/` con `make doctor`, copia tambien el `.env` a esa carpeta:

```bash
cp .env 03-agents/.env
```

La guia detallada de setup, prerequisitos por sistema operativo y troubleshooting esta en [instalacion.md](./instalacion.md).

## Comandos principales

Desde la raiz:

```bash
make help
make sync
make test
make lint
make format
make module-01
make module-02
make module-03
```

## Estructura academica

### Modulo 1: Fundamentos de AI Engineering

Ruta base: `01-Introduction_AI_Engineering/`

| Clase | Tema | Carpeta |
|---|---|---|
| 00 | Python extra class | `00_python_extra_class/` |
| 01 | Software Engineering vs AI Engineering | `01_introduction/` |
| 02 | Prompting aplicado | `02_prompting/` |
| 03 | LangChain prompting | `03_langchain_prompting/` |
| 04 | LangGraph workflows | `04_langchain_langgraph/` |
| 05 | RAG | `05_rags/` |
| 06 | Proyecto integrador | `06_project/` |

Resumen ampliado: [01-Introduction_AI_Engineering/README.md](./01-Introduction_AI_Engineering/README.md)

### Modulo 2: Vector Databases y RAG avanzado

Ruta base: `02-vector_data_bases/`

| Bloque | Tema | Ruta |
|---|---|---|
| 01 | Representacion, retrieval y embeddings | `01_intro/` |
| 02 | Bases de datos vectoriales | `02_databases/` |
| 03 | RAG | `03_rag/` |
| 04 | Caso aplicado Batman | `04_batman_vector_db_orchestration/` |

Resumen ampliado: [02-vector_data_bases/README.md](./02-vector_data_bases/README.md)

### Modulo 3: Agentes

Ruta base: `03-agents/`

| Bloque | Tema | Ruta |
|---|---|---|
| 01 | Fundamentos de agentes | `01_intro/` |
| 02 | Agentes con LangChain/LangGraph | `02_langchain/` |
| 03 | Coordinacion multi-agente | `03_multi_agent/` |
| 04 | Hardening para produccion | `04_production/` |
| 05 | Caso end-to-end de LLMops | `05_llmops/` |

Resumen ampliado: [03-agents/README.md](./03-agents/README.md)

### Modulo 4: Deep Learning

Ruta base: `04-deep_learning/`

| Bloque | Tema | Ruta |
|---|---|---|
| 01 | Fundamentos de redes neuronales | `01_fundamentos_redes_neuronales/` |
| 02 | PyTorch | `02_pytorch_fundamentos/` |
| 03 | Entrenamiento profundo | `03_entrenamiento_redes_profundas/` |
| 04 | CNNs | `04_vision_por_computadora_cnns/` |
| 05 | Secuencias | `05_modelado_de_secuencias/` |
| 06 | NLP con atencion | `06_nlp_con_atencion/` |
| 07 | Transformers | `07_transformers_y_chatbots/` |

Resumen ampliado: [04-deep_learning/README.md](./04-deep_learning/README.md)

## Convenciones del repositorio

- Las carpetas numeradas marcan el orden de cursada.
- `data/` o `00_data/` guarda datasets y bases de conocimiento.
- `tools/` o `00_tools/` contiene utilidades para ejecutar notebooks.
- `scripts/` contiene versiones reutilizables de la logica vista en notebooks.
- `tests/`, `99_tests/` o `05_llmops/tests/` contiene validaciones automatizadas.
- Los artefactos generados (`outputs/`, `*.executed.ipynb`, caches) quedan fuera del flujo principal del estudiante.

## Estructura general

```text
ai_engineering_henry/
├── .env.example
├── Makefile
├── README.md
├── instalacion.md
├── pyproject.toml
├── 01-Introduction_AI_Engineering/
│   ├── 00_python_extra_class/
│   ├── 01_introduction/
│   ├── 02_prompting/
│   ├── 03_langchain_prompting/
│   ├── 04_langchain_langgraph/
│   ├── 05_rags/
│   └── 06_project/
├── 02-vector_data_bases/
│   ├── 01_intro/
│   ├── 02_databases/
│   ├── 03_rag/
│   └── 04_batman_vector_db_orchestration/
├── 03-agents/
│   ├── 00_data/
│   ├── 01_intro/
│   ├── 02_langchain/
│   ├── 03_multi_agent/
│   ├── 04_production/
│   ├── 05_llmops/
│   └── 99_tests/
└── 04-deep_learning/
    ├── 01_fundamentos_redes_neuronales/
    ├── 02_pytorch_fundamentos/
    ├── 03_entrenamiento_redes_profundas/
    ├── 04_vision_por_computadora_cnns/
    ├── 05_modelado_de_secuencias/
    ├── 06_nlp_con_atencion/
    ├── 07_transformers_y_chatbots/
    ├── scripts/
    └── tests/
```

## Recomendacion para estudiantes

- No recorras el repo por orden alfabetico; sigue el orden numerado.
- Empieza cada modulo por su `README.md`.
- Ejecuta primero los notebooks base y luego los casos aplicados.
- Usa `make test` o los `Makefile` por modulo para validar que el entorno quedo bien.
