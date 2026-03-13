![](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)

# AI Engineering Foundation
**Henry Academy — Advanced Agentic & Deep Learning Track**

Repositorio oficial y material fundacional para la formación en **AI Engineering**. 

Este programa prescinde de aproximaciones superficiales y aborda la inteligencia artificial estocástica con el mismo rigor que la ingeniería de software clásica. Desde los fundamentos de redes neuronales y representaciones vectoriales, hasta sistemas distribuidos con múltiples agentes, RAG avanzado, telemetría y LLMops en producción.

La estructura de este repositorio prioriza el orden de estudio iterativo, posibilitando a los ingenieros moverse ágilmente entre la carga conceptual ("por qué") y la ejecución metodológica ("cómo"). **Diseñado nativamente para Python 3.13**.

---

## 1. Ruta de Estudio y Arquitectura del Curso

El material debe ser recorrido en estricta secuencia numérica. Adelantarse a las herramientas orquestadoras sin entender las fundaciones de *embeddings* limitará sustancialmente la capacidad de diagnóstico en producción. Hemos unificado todo el contenido en 3 grandes Módulos Base estructurales:

| Orden | Módulo Académico | Objetivo Teórico-Práctico |
|:---:|---|---|
| **01** | [**Introducción a AI Engineering y APIs**](./01-Introduction_AI_Engineering/) | Nivelación en Python 3.13, despliegue de backends nativos (FastAPI) y fundamentos base sobre Prompting y transiciones del Software al IA. |
| **02** | [**Vector Databases, Retrieval y Deep Learning**](./02-vector_data_bases/) | Abstracciones algebraicas del *Retrieval*, fundamentos duros "from scratch" en PyTorch hasta lograr redes neuronales, *Attention* local y simulación visual de *Self-Attention*. |
| **03** | [**Sistemas de Agentes y LLMops Integrador**](./03-agents/) | Tolerancia a fallos, flujos de orquestación, *LangGraph*, sistemas autónomos que compiten en *datasets* semánticos (Películas, Libros, Discos) y evaluación ciega en producción. |

---

## 2. Dónde Encontrar el Material por Clase

El repositorio está fuertemente estratificado.

<details open>
<summary>🗺️ <b>Mapa del Repositorio Actualizado</b></summary>
<br>

**`01-Introduction_AI_Engineering/`**
- `00_python_extra_class/`: Nivelación intensiva en Python avanzado (Pydantic, robustez).
- `01_fastapi/`: Construcción y exposición de APIs asíncronas para servir IA web.
- `02_introduction/`: Fundamentos para migrar desde el Software tradicional al AI Engineering.
- `03_prompting/`: Ingeniería de texto predictivo, cadenas (CoT) y frameworks (ReAct).
- `04_langchain_prompting/`: Abstracciones mantenibles con *LangChain*.
- `05_langchain_langgraph/`: Controladores de estado en grafos cíclicos elementales.
- `06_rags/`: *Retrieval-Augmented Generation* introductorio.
- `07_project/`: El primer consolidado ruteador base en FastAPI.

**`02-vector_data_bases/`**
- `01_intro/`: Entendimiento numérico. Incluye un recorrido teórico robusto que finaliza incrustándose en *Deep Learning*:
  - **`07_deep_learning_attention/`**: El camino completo desde cero en PyTorch, arquitecturas estáticas de visión, modelos de lenguaje natural secuenciales, y reconstrucción algorítmica de la base de una red recurrente y de Mecanismos de *Attention*.
- `02_databases/`: Clientes estables (*Chroma*, persistencia y filtrado Pydantic).
- `03_rag/`: Generación multi-query y ensembles.
- `04_batman_vector_db_orchestration/`: Laboratorio vectorizado aplicado tipo *Agentic RAG*.

**`03-agents/`**
- `01_intro/`: Paradojas de costo, latencia y alucinación.
- `02_langchain/`: Llamado determinista de funciones dinámicas y ruteo semántico.
- `03_multi_agent/`: Sistemas orquestadores y debate sintético.
- `04_production/`: Timeouts, mallas de *fallbacks*, presupuestación en llamadas API.
- `05_llmops/`: Configuración, monitoreo, trazabilidad y evaluación automática.
- `06_project_langgraph/`: **[Proyecto Final del Curso]** El *Cultural Intelligence System*, aplicando todos los ruteos de estado mutables, herramientas externas complejas, evaluación heurística multi-agente en una app asíncrona completa.

</details>

---

## 3. Preparación del Entorno (Python 3.13)

La madurez en AI Engineering exige reproducibilidad perfecta. Hemos abstraído la dependencia y el sistema de compilación a través de **`uv`** garantizando candados absolutos en las versiones usadas.

### Requisitos base:
1. Python `>=3.13` instalado en el sistema operativo.
2. [Instalar `uv`](https://github.com/astral-sh/uv).
3. Utilidad `make` (viene pre-instalada en Mac/Linux, disponible vía WSL2 en Windows).
4. Un token oficial de OpenAI API comercial o Free Tier para la experimentación.

### Procedimiento Universal (Ejecutable desde la Raíz)

```bash
# 1. Clona el entorno a tu laptop
git clone <tu-fork-url> ai_engineering_henry
cd ai_engineering_henry

# 2. Configura los secretos
cp .env.example .env

# -> Abre el archivo .env en tu editor de texto y agrega tu OPENAI_API_KEY.

# 3. Construye todo el árbol de dependencias global
make sync
```

*Nota para instructores: El repositorio mantiene archivos `pyproject.toml` divididos por cada módulo, aislando el tamaño de las descargas en entornos atómicos si así lo requieres.*

---

## 4. Recetas de Inspección (Pruebas unitarias Automáticas)

Los estudiantes pueden validar interactivamente que todo su código opera localmente gracias al encapsulamiento en las reglas de compilación *Make* con *uv*:

```bash
# Probar el Módulo 1 (Python, FastAPI, Intro)
make module-01

# Probar bases vectoriales (y sanidad teórica profunda de Deep Learning)
make module-02

# Probar la sanidad del ecosistema Agentic / LangGraph en la ruta definitiva
make module-03
```

*Nota: Recomendamos trabajar interactivamente ejecutando Visual Studio Code (con la extensión estándar de Jupyter Notebook) e indicando que utilice como Kernel el ejecutable de Python 3.13 que vive en el sub-directorio `.venv/bin/python` de la carpeta en labor.*
