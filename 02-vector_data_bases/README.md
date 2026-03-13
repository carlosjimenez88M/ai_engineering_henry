# Módulo 02 — Vector Databases y Deep Learning

Este módulo responde una pregunta que el módulo 01 deja abierta: ¿cómo funciona realmente la representación del lenguaje? Para poder construir sistemas RAG confiables o diagnosticar por qué un retrieval falla, necesitás entender qué hay detrás de los embeddings. Ese es el hilo conductor de este módulo.

El recorrido va desde tokens y similitud vectorial hasta redes neuronales entrenadas en PyTorch, mecanismos de atención y Transformers. Paralelamente, trabajás con bases de datos vectoriales en escenarios reales y patrones RAG más sofisticados que los del módulo anterior.

---

## Ruta de Estudio

| # | Bloque | Qué vas a aprender |
|:---:|---|---|
| 01 | [Introducción y Representación](./01_intro/) | Tokens, embeddings, retrieval TF-IDF vs vectorial, Deep Learning completo |
| 02 | [Bases de Datos Vectoriales](./02_databases/) | ChromaDB, persistencia, chunking, comparación de modelos de embeddings |
| 03 | [RAG Avanzado](./03_rag/) | Multi-query, ensemble retrievers, compresión de contexto |
| 04 | [Caso Aplicado Batman](./04_batman_vector_db_orchestration/) | Sistema RAG orquestado completo con routing entre dominios |

---

## El Bloque de Deep Learning

El sub-bloque `01_intro/07_deep_learning_attention/` es el más extenso del módulo y tiene su propio recorrido de 7 clases. Es completamente opcional si tu objetivo es sólo trabajar con bases vectoriales y RAG. Sin embargo, si querés entender de verdad por qué los embeddings funcionan como funcionan, es el camino.

El recorrido de Deep Learning cubre:

| Clase | Tema | Contenido |
|:---:|---|---|
| 01 | Fundamentos de redes neuronales | Perceptrón, MLP, funciones de activación, backpropagation desde cero |
| 02 | PyTorch para entrenamiento | Tensores, Dataset, DataLoader, training loop completo |
| 03 | Entrenamiento profundo | Inicialización, normalización por batch, regularización, diagnóstico |
| 04 | Visión por computadora (CNNs) | Convoluciones, pooling, receptive field, arquitecturas de visión |
| 05 | Modelado de secuencias | RNN, LSTM, GRU, CNN temporal, padding y packing |
| 06 | NLP con atención | Embeddings de palabras, ventanas de texto, mecanismo de atención |
| 07 | Transformers y chatbots locales | Positional embeddings, máscara causal, decoding, chat local |

Todo corre en CPU. No necesitás GPU para completar el módulo.

---

## Recorrido Recomendado de Notebooks

### Bloque 01 — Introducción

Seguí este orden para que los conceptos se construyan sobre sí mismos:

| Orden | Notebook | Por qué en este orden |
|:---:|---|---|
| 1 | `01_intro/01_tokens.ipynb` | Primero entendé cómo los modelos ven el texto |
| 2 | `01_intro/03_transformers.ipynb` | Luego la arquitectura que los procesa |
| 3 | `01_intro/04_text_classification.ipynb` | Cómo los embeddings representan significado |
| 4 | `01_intro/02_rag_tfidf.ipynb` | Retrieval sparse como punto de comparación |
| 5 | `01_intro/05_rags_vectorial_databases.ipynb` | El puente entre retrieval y RAG moderno |
| 6 | `01_intro/06_agent2agent_literario.ipynb` | Caso aplicado: cierre del bloque |

### Bloque 02 — Bases de Datos Vectoriales

| Orden | Notebook | Enfoque |
|:---:|---|---|
| 1 | `02_databases/01-bases-vectoriales-fundamentos.ipynb` | Embeddings, similitud coseno, primeras búsquedas |
| 2 | `02_databases/02-bases-vectoriales-produccion.ipynb` | Persistencia, chunking, trade-offs de configuración |
| 3 | `02_databases/03-comparacion-modelos-embeddings-rayuela.ipynb` | Comparativa aplicada sobre Rayuela de Cortázar |

### Bloque 03 — RAG Avanzado

| Orden | Notebook | Enfoque |
|:---:|---|---|
| 1 | `03_rag/01-rag-fundamentos.ipynb` | Pipeline RAG completo end-to-end |
| 2 | `03_rag/02-rag-avanzado.ipynb` | Multi-query, ensemble retrievers, compresión de contexto |

### Bloque 04 — Caso Aplicado Batman

Este bloque es el integrador del módulo. Construís un sistema RAG orquestado usando datos del universo Batman y Spider-Man.

| Orden | Notebook | Qué resuelve |
|:---:|---|---|
| 1 | `00_clase_de_repaso.ipynb` | Contexto del caso y repaso de conceptos |
| 2 | `01_diseno_vector_db_batman.ipynb` | Diseño del vector store con criterio de producción |
| 3 | `02_rag_vs_agentic_rag_batman.ipynb` | Comparativa: RAG clásico vs RAG agéntico |
| 4 | `03_routing_orquestacion_simple.ipynb` | Routing entre dominios temáticos |
| 5 | `04_ejercicio_agent2agent_batman_rag.ipynb` | Ejercicio guiado completo |
| 6 | `05_agent2agent_roles_router_batman.ipynb` | Orquestación con roles especializados |

---

## Instalación y Comandos

```bash
cd 02-vector_data_bases
uv sync --extra dev
```

Comandos principales:

```bash
make test                  # Tests del módulo
make run-batman-module     # Ejecutar el caso aplicado completo
```

---

## Archivos de Apoyo

- `pyproject.toml` — dependencias del módulo 02
- `00_tools/execute_notebooks.py` — ejecuta notebooks del módulo en batch
- `04_batman_vector_db_orchestration/scripts/` — utilidades reutilizables del caso aplicado

---

## Criterio de Avance

Estás listo para el módulo 03 cuando podás responder estas preguntas:

- ¿Por qué la similitud coseno funciona mejor que la distancia euclidiana para embeddings de texto?
- ¿Qué es el chunking y por qué el tamaño del chunk afecta la calidad del retrieval?
- ¿Cuándo tiene sentido usar multi-query retrieval?
- ¿Cuál es la diferencia entre RAG clásico y RAG agéntico?
- ¿Qué hace una red neuronal que no puede hacer una regresión lineal?
