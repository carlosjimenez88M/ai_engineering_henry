![](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)

# AI Engineering Foundation
**Henry Academy — Advanced Agentic & Deep Learning Track**

Repositorio oficial y material fundacional para la formación en **AI Engineering**. 

Este programa prescinde de aproximaciones superficiales y aborda la inteligencia artificial estocástica con el mismo rigor que la ingeniería de software clásica. Desde los fundamentos de redes neuronales y representaciones vectoriales, hasta sistemas distribuidos con múltiples agentes, RAG avanzado, telemetría y LLMops en producción.

La estructura de este repositorio prioriza el orden de estudio iterativo, posibilitando a los ingenieros moverse ágilmente entre la carga conceptual ("por qué") y la ejecución metodológica ("cómo").

---

## 1. Ruta de Estudio y Arquitectura del Curso

El material debe ser recorrido en estricta secuencia numérica. Adelantarse a las herramientas orquestadoras sin entender las fundaciones de *embeddings* limitará sustancialmente la capacidad de diagnóstico en producción.

| Orden | Módulo Académico | Objetivo Teórico-Práctico |
|:---:|---|---|
| **00** | [**Python Extra Class**](./01-Introduction_AI_Engineering/00_python_extra_class/) | Nivelación intensiva en Python avanzado enfocado a IA (Pydantic, robustez). |
| **01** | [**Introducción a AI Engineering**](./01-Introduction_AI_Engineering/) | Transición conceptual del desarrollo lineal al comportamiento emergente (*Prompting, LCEL, LangGraph base*). |
| **02** | [**Vector Databases y RAG**](./02-vector_data_bases/) | Abstracciones densas, álgebra lineal del *Retrieval*, RAG vs *Agentic RAG*. |
| **03** | [**Sistemas de Agentes y LLMops**](./03-agents/) | Tolerancia a fallos, Tool-calling, flujos de orquestación, evaluación y despliegue a producción. |
| **04** | [**Deep Learning Fundacional**](./04-deep_learning/) | Desde perceptrones hasta *Transformers* y decodificación, codificando arquitecturas "from scratch" en PyTorch. |
| **05** | [**FastAPI de Cero a Producción**](./05-fastapi/) | Despliegue de backends asíncronos para servir IA web (SQLAlchemy, JWT, endpoints). |
| **06** | [**LangGraph Integrador: Multi-Agente**](./06-langgraph/) | Cierre arquitectónico creando un sistema distribuido de ruteo y síntesis de cultura (Nolan, King, Davis). |

---

## 2. Dónde Encontrar el Material por Clase

El repositorio está estratificado para facilitar la búsqueda. Todas las lecciones cuentan con teoría y código ejecutable. Usa este índice para ubicar tu clase sin perder contexto.

<details open>
<summary>🗺️ <b>Mapa del Repositorio</b></summary>
<br>

**`01-Introduction_AI_Engineering/`**
- `00_python_extra_class/`: Clases de refuerzo para buenas prácticas y robustez.
- `01_introduction/`: Fundamentos para migrar desde el Software tradicional al AI Engineering.
- `02_prompting/`: Ingeniería de texto predictivo, cadenas (CoT) y frameworks (ReAct).
- `03_langchain_prompting/`: Abstracciones mantenibles con *LangChain*.
- `04_langchain_langgraph/`: Controladores de estado en grafos cíclicos con *LangGraph*.
- `05_rags/`: *Retrieval-Augmented Generation* introductorio.

**`02-vector_data_bases/`**
- `01_intro/`: Embeddings numéricos, tokens y distancia coseno.
- `02_databases/`: Clientes estables (*Chroma*, persistencia y filtrado Pydantic).
- `03_rag/`: Generación multi-query y ensembles.
- `04_batman_vector_db_orchestration/`: Primer laboratorio orquestador de *Agentic RAG*.

**`03-agents/`**
- `01_intro/`: Paradojas de costo, latencia y alucinación.
- `02_langchain/`: Llamado determinista de funciones dinámicas y ruteo semántico.
- `03_multi_agent/`: Sistemas orquestadores y debate sintético.
- `04_production/`: Timeouts, mallas de *fallbacks*, presupuestación en llamadas API.
- `05_llmops/`: Configuración, monitoreo, trazabilidad y evaluación automática.

**`04-deep_learning/`**
- `01_fundamentos_redes_neuronales/`: Redes estáticas construídas en PyTorch básico.
- `02_pytorch_fundamentos/`: Tensors, auto-diferenciación, y Datasets nativos.
- `03_entrenamiento_redes_profundas/`: Regularización y estabilidad estadística.
- `04_vision_por_computadora_cnns/`: Convoluciones sobre tensores espaciales.
- `05_modelado_de_secuencias/`: Ventanas viradas en el tiempo (RNN, LSTM, GRUs).
- `06_nlp_con_atencion/`: Arquitecturas de Atención paralela en NLP.
- `07_transformers_y_chatbots/`: Inferencias de chat local con *Transformers*.

**`05-fastapi/`**
- `01_fundamentos/` a `06_frontend/`: Trayecto de *APIs* nativas asíncronas para el despliegue del trabajo anterior.

**`06-langgraph/`**
- El proyecto integrador final *Cultural Intelligence System*, aplicando ruteos de estado, herramientas externas y evaluación heurística.

</details>

---

## 3. Preparación del Entorno (Qué necesitas instalar)

La madurez en AI Engineering exige reproducibilidad perfecta. Hemos abstraído la dependencia y el sistema de compilación a través de **`uv`** (el reemplazo de `pip` asíncrono en Rust) y **`make`**.

### Requisitos base:
1. Python `>=3.10` instalado en el sistema operativo.
2. [Instalar `uv`](https://github.com/astral-sh/uv).
3. Utilidad `make` (viene pre-instalada en Mac/Linux, disponible vía WSL2 en Windows).
4. Un token oficial de OpenAI API comercial o Free Tier para la experimentación.

### Procedimiento Universal (Ejecutar en la Raíz del Proyecto)

```bash
# 1. Clona el entorno a tu laptop
git clone <tu-fork-url> ai_engineering_henry
cd ai_engineering_henry

# 2. Configura los secretos
cp .env.example .env

# -> Abre el archivo .env en tu editor de texto y agrega tu OPENAI_API_KEY.

# 3. Construye todo el árbol de dependencias
make sync
```

*Nota para instructores y contribuyentes: El repositorio mantiene archivos `pyproject.toml` divididos por cada módulo, aislando el tamaño de las descargas y permitiendo entornos virtuales atómicos por carpeta.*

---

## 4. Recetas de Inspección (Ejecutar Ejemplos, Notebooks y Tests)

Los estudiantes **no deben intentar invocar notebooks o librerías internas intentando adivinar rutas relativas de PYTHONPATH**, ni utilizar `python` sobre un archivo sin activar su base respectiva.

La abstracción de *Make* permite correr cualquier bloque desde la raíz del sistema o desde cada carpeta. Utiliza `uv run` nativamente debajo de la superficie.

### Ejecución de Tests 

Asegura la trazabilidad y sanidad lógica garantizando que tu sistema levanta correctamente:

```bash
# Probar el esqueleto del Módulo 1 
make module-01

# Probar la sanidad funcional del ecosistema end-to-end de Agentes
cd 03-agents
make test

# Validar los endpoints y las dependencias de Deep Learning y NLP (Las Mil y una Noches corpus)
cd 04-deep_learning
make test
```

### Ejecutar Clases Magistrales (Notebooks) en Terminal
Si lo precisas, el sistema puede forzar corrida automatizada (Smoke tests) sobre todos los notebooks de la currícula de forma desatendida, comprobando al paso del compilador que ninguna celda rompa por dependencias externas caídas o credenciales rotas:

```bash
cd 01-Introduction_AI_Engineering
make run-notebooks-langgraph

cd ../04-deep_learning
make notebooks-smoke
```

*Nota: Recomendamos trabajar interactivamente ejecutando Visual Studio Code (con la extensión estándar de Jupyter Notebook) e indicando que utilice como Kernel el ejecutable de python que vive en el sub-directorio `.venv/bin/python` de cada módulo respectivo.*
