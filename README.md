<div align="center">

# AI Engineering Foundation
### Henry Academy — Advanced Agentic & Deep Learning Track

*Construye sistemas de inteligencia artificial desde los fundamentos hasta producción.*

</div>

---

## ¿De qué trata este programa?

Este repositorio es el material oficial del curso de **AI Engineering** de Henry Academy. No es una colección de tutoriales sueltos: es un programa diseñado como una ingeniería progresiva, donde cada módulo construye sobre el anterior.

La premisa es simple: un buen AI Engineer no es alguien que sabe usar APIs de OpenAI. Es alguien que entiende cómo funcionan los modelos, diseña sistemas confiables alrededor de ellos, los lleva a producción y los mantiene. Este programa te lleva exactamente ahí.

Al finalizar los tres módulos habrás construido un sistema multi-agente completo con estado persistente, herramientas externas, evaluación automática y despliegue en Docker, todo desde cero.

---

## Mapa del Programa

El programa está dividido en tres módulos que deben cursarse en orden. Saltear módulos sin la base del anterior genera puntos ciegos difíciles de diagnosticar más adelante.

| # | Módulo | Enfoque central | Proyecto integrador |
|:---:|---|---|---|
| **01** | [Introducción a AI Engineering](./01-Introduction_AI_Engineering/) | Python profesional, FastAPI, Prompting, LangChain, LangGraph, RAG | Sistema de routing semántico con FastAPI |
| **02** | [Vector Databases y Deep Learning](./02-vector_data_bases/) | Embeddings, bases vectoriales, RAG avanzado, redes neuronales desde cero | Sistema RAG orquestado con datos reales |
| **03** | [Sistemas de Agentes y LLMops](./03-agents/) | Agentes autónomos, multi-agente, producción, observabilidad, evaluación | Cultural Intelligence System con LangGraph |

---

## ¿Qué vas a aprender en cada módulo?

### Módulo 01 — Introducción a AI Engineering

Empezás por los fundamentos que un AI Engineer necesita dominar antes de tocar cualquier framework: Python robusto, APIs web con FastAPI, y las técnicas de prompting que determinan la calidad de cualquier sistema LLM. Después incorporás LangChain y LangGraph para construir workflows con estado, y cerrás con tu primer sistema RAG funcional.

Lo importante de este módulo es que no se trata de aprender herramientas: se trata de entender *por qué* cada capa existe y cuándo usarla.

### Módulo 02 — Vector Databases y Deep Learning

Acá profundizás en la representación matemática del lenguaje. Partís desde cómo los modelos procesan texto (tokens, embeddings, similitud vectorial), pasás por bases de datos vectoriales en producción, y llegás al recorrido completo de Deep Learning: redes neuronales desde cero en PyTorch, CNNs, RNNs, mecanismos de atención y Transformers.

Este módulo te da el "por qué" detrás de las herramientas que usás en el módulo 1 y el módulo 3.

### Módulo 03 — Sistemas de Agentes y LLMops

El módulo más denso y el que integra todo lo anterior. Arrancás con la anatomía de un agente (qué es, cuándo usarlo, cuándo no), avanzás hacia sistemas multi-agente con coordinación y handoffs, implementás patrones de producción (timeouts, fallbacks, control de costos), y cerrás con el **proyecto final**: un sistema multi-dominio construido sobre LangGraph con API FastAPI, tests, Docker y evaluación automática.

---

## Antes de Empezar

### Requisitos del sistema

- Python `3.10` o superior (recomendado `3.13`)
- `git` instalado
- Acceso a internet para la API de OpenAI
- 4 GB de RAM disponibles (8 GB recomendados para el módulo de Deep Learning)

### Herramientas que vas a usar

- **`uv`**: gestor de entornos y dependencias Python (reemplaza pip + venv)
- **`make`**: automatización de comandos repetitivos
- **`OpenAI API`**: necesitás una clave activa para los ejemplos con LLMs
- **`Docker`** (opcional): para el proyecto final del módulo 03

### Guía de instalación completa

Todos los pasos de instalación están documentados en [`instalacion.md`](./instalacion.md). Leé ese archivo antes de correr cualquier comando del repositorio.

---

## Inicio Rápido

Si ya tenés `uv` y `git` instalados:

```bash
# 1. Clonar el repositorio
git clone <url-del-repo> ai_engineering_henry
cd ai_engineering_henry

# 2. Copiar el archivo de configuración
cp .env.example .env
# Abrí .env y completá tu OPENAI_API_KEY

# 3. Instalar todas las dependencias
make sync

# 4. Verificar que todo funciona
make test
```

Si algún paso falla, consultá la sección de [troubleshooting en instalacion.md](./instalacion.md#problemas-comunes).

---

## Validación por Módulo

Podés verificar que el entorno de cada módulo está configurado correctamente con:

```bash
make module-01   # Valida el módulo de Introducción
make module-02   # Valida bases vectoriales y Deep Learning
make module-03   # Valida el ecosistema de agentes
```

Cada comando corre los tests del módulo y reporta si el entorno está listo para trabajar.

---

## Estructura del Repositorio

```
ai_engineering_henry/
├── 01-Introduction_AI_Engineering/   # Módulo 01
│   ├── 00_python_extra_class/        # Nivelación Python (opcional)
│   ├── 01_fastapi/                   # APIs web con FastAPI
│   ├── 02_introduction/              # Software Engineering → AI Engineering
│   ├── 03_prompting/                 # Técnicas de prompting
│   ├── 04_langchain_prompting/       # Prompting con LangChain
│   ├── 05_langchain_langgraph/       # Workflows con estado en LangGraph
│   ├── 06_rags/                      # Retrieval-Augmented Generation
│   └── 07_project/                   # Proyecto integrador del módulo
│
├── 02-vector_data_bases/             # Módulo 02
│   ├── 01_intro/                     # Tokens, embeddings, retrieval
│   │   └── 07_deep_learning_attention/  # Deep Learning completo (PyTorch)
│   ├── 02_databases/                 # Bases vectoriales en producción
│   ├── 03_rag/                       # RAG avanzado
│   └── 04_batman_vector_db_orchestration/  # Caso aplicado
│
├── 03-agents/                        # Módulo 03
│   ├── 01_intro/                     # Fundamentos de agentes
│   ├── 02_langchain/                 # Agentes con LangChain/LangGraph
│   ├── 03_multi_agent/               # Coordinación multi-agente
│   ├── 04_production/                # Hardening para producción
│   ├── 05_llmops/                    # Observabilidad y evaluación
│   └── 06_project_langgraph/         # Proyecto final del curso
│
├── instalacion.md                    # Guía de instalación detallada
├── .env.example                      # Plantilla de variables de entorno
└── Makefile                          # Comandos de automatización
```

---

## Convenciones del Repositorio

Algunas cosas que se repiten en todos los módulos y vale la pena conocer desde el principio:

**Numeración de carpetas**: el prefijo numérico (`01_`, `02_`, etc.) define el orden de estudio. Seguí ese orden.

**`pyproject.toml` por módulo**: cada módulo tiene sus propias dependencias. Podés instalar sólo el módulo en el que estás trabajando con `uv sync --extra dev` desde su directorio.

**`Makefile` por módulo**: cada módulo tiene sus propios comandos. Corré `make help` dentro de cualquier módulo para ver las opciones disponibles.

**`.env` compartido**: el archivo `.env` de la raíz sirve para todos los módulos. Si trabajás en módulos más profundos, puede que necesites copiarlo: `cp .env 03-agents/.env`.

**Notebooks ejecutables**: todos los notebooks fueron diseñados para correr de principio a fin sin errores. Si un notebook falla, es probable que sea un problema de entorno, no del código.

---

## Soporte y Comunidad

Si encontrás un error en el material, podés abrir un issue en el repositorio describiendo el problema y el contexto.

Si tenés dudas sobre el contenido del curso, usá los canales de comunicación de Henry Academy.

---

<div align="center">

*Este material fue construido para que lo uses, lo rompas y lo entiendas. La mejor forma de aprender ingeniería es haciendo ingeniería.*

</div>
