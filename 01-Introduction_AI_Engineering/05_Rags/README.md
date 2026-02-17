# Clase 05: RAG (Retrieval-Augmented Generation) y Bases de Datos Vectoriales

Esta clase cierra el ciclo de AI Engineering aplicado. Hasta ahora construiste prompts (Clase 02), los integraste con LangChain (Clase 03), los orquestaste con LangGraph (Clase 04) y viste un proyecto multi-agente (05_project). Ahora atacamos **el problema mas critico en produccion**: como darle a un LLM acceso a conocimiento que no tiene.

## Que aprenderas

Al terminar esta clase deberias poder:

1. Explicar por que RAG existe y que problema resuelve (no es opcional, es necesidad)
2. Disenar un pipeline RAG completo: chunking → embedding → indexacion → retrieval → generacion
3. Elegir la base de datos vectorial correcta para tu caso de uso
4. Implementar RAG con agentes usando **prompt chaining** y **routing** con LangGraph
5. Identificar cuando RAG **no** es la solucion correcta

## Conexion con clases anteriores

```
Clase 02: Prompting        → Aprendiste a hablar con el LLM
Clase 03: LangChain        → Aprendiste a estructurar la conversacion
Clase 04: LangGraph        → Aprendiste a orquestar flujos de decision
Clase 05: RAG              → Aprendiste a darle memoria y conocimiento externo
                              ↓
                     Agente que razona + sabe + decide
```

---

## 1. El Problema Fundamental: Por que RAG?

Los LLMs tienen tres limitaciones criticas que ningun prompt puede resolver:

### Limitacion 1: Conocimiento congelado

Un modelo entrenado en enero 2024 no sabe nada de lo que paso despues. Si tu empresa lanzo un producto en marzo, el modelo no lo conoce. Punto. No importa cuanto prompt engineering hagas.

### Limitacion 2: Alucinaciones con confianza

Cuando un LLM no sabe algo, no dice "no se". Inventa una respuesta coherente y la presenta con la misma confianza que un hecho verificado. Esto es **peligroso en produccion**.

### Limitacion 3: Sin acceso a datos privados

Tu base de conocimiento interna, tus documentos de HR, tu runbook tecnico — nada de eso existe para el modelo. El LLM solo conoce su corpus de entrenamiento.

```
┌─────────────────────────────────────────────────────────────┐
│                    SIN RAG                                  │
│                                                             │
│  Usuario: "Cual es la politica de vacaciones?"              │
│                                                             │
│  LLM: "Generalmente las empresas ofrecen 15 dias..."       │
│        ↑ ALUCINACION: inventa una respuesta generica       │
│        ↑ No tiene acceso a TU manual de RRHH               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CON RAG                                  │
│                                                             │
│  Usuario: "Cual es la politica de vacaciones?"              │
│                                                             │
│  [1] Busca en tu base de conocimiento → encuentra chunk     │
│  [2] Pasa el chunk como contexto al LLM                     │
│  [3] LLM responde BASADO en evidencia real                  │
│                                                             │
│  LLM: "Segun el manual de RRHH (seccion 3.2), la empresa   │
│        ofrece 20 dias habiles para empleados full-time..."  │
│        ↑ VERIFICABLE: cita fuente real                      │
└─────────────────────────────────────────────────────────────┘
```

**RAG no es un "nice to have". Es la diferencia entre un chatbot de juguete y un sistema de produccion.**

Referencia: Chip Huyen, *AI Engineering*, Cap. 10 — "RAG is the most impactful pattern for grounding LLM outputs in factual, domain-specific knowledge."

---

## 2. Que es RAG (Retrieval-Augmented Generation)

RAG es un patron de arquitectura que combina dos capacidades:

1. **Retrieval (Recuperacion)**: Buscar informacion relevante en una base de conocimiento externa
2. **Generation (Generacion)**: Usar esa informacion como contexto para que el LLM genere una respuesta fundamentada

El termino fue introducido por Lewis et al. (2020) en el paper *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"* (Facebook AI Research).

### La idea central

En lugar de pedirle al LLM que "sepa" todo, le damos un mecanismo para "buscar" lo que necesita antes de responder. Es como la diferencia entre un examen a libro cerrado vs libro abierto.

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Query   │────→│  Retriever   │────→│   Context    │────→│  Generator   │
│ (usuario)│     │ (busca docs) │     │ (docs rels.) │     │   (LLM)      │
└──────────┘     └──────────────┘     └──────────────┘     └──────┬───────┘
                                                                   │
                                                                   ▼
                                                          ┌──────────────┐
                                                          │  Respuesta   │
                                                          │ fundamentada │
                                                          └──────────────┘
```

---

## 3. Arquitectura Completa de un Sistema RAG

Un sistema RAG tiene dos fases principales:

### Fase 1: Indexacion (offline, se hace una vez)

```
┌───────────┐    ┌───────────┐    ┌───────────┐    ┌────────────────┐
│ Documentos│───→│ Chunking  │───→│ Embedding │───→│  Vector Store  │
│  (raw)    │    │ (partir)  │    │ (vectores)│    │  (almacenar)   │
└───────────┘    └───────────┘    └───────────┘    └────────────────┘

Ejemplo:
  manual_rrhh.md → [chunk_1, chunk_2, ...] → [vec_1, vec_2, ...] → ChromaDB
```

### Fase 2: Consulta (online, cada request)

```
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌──────────┐
│  Query   │───→│ Embedding │───→│ Similarity│───→│  Top-K    │───→│   LLM    │
│ (texto)  │    │ (vector)  │    │  Search   │    │  chunks   │    │ Generate │
└──────────┘    └───────────┘    └───────────┘    └───────────┘    └──────────┘
```

### Codigo: Pipeline RAG minimo

```python
from openai import OpenAI
import chromadb

client = OpenAI()
db = chromadb.Client()
collection = db.create_collection("mi_conocimiento")

# --- Fase 1: Indexacion ---
documentos = [
    "La empresa ofrece 20 dias de vacaciones al ano.",
    "El proceso de onboarding dura 30 dias.",
    "Las evaluaciones de desempeno son trimestrales.",
]

collection.add(
    documents=documentos,
    ids=[f"doc_{i}" for i in range(len(documentos))],
)

# --- Fase 2: Consulta ---
query = "Cuantos dias de vacaciones tengo?"
resultados = collection.query(query_texts=[query], n_results=2)

# Construir contexto
contexto = "\n".join(resultados["documents"][0])

# Generar respuesta fundamentada
respuesta = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Responde SOLO con base en este contexto:\n{contexto}"},
        {"role": "user", "content": query},
    ],
)
print(respuesta.choices[0].message.content)
```

**Observacion critica**: Este pipeline minimo funciona, pero tiene problemas graves en produccion. Los resolveremos progresivamente en las notebooks.

---

## 4. Embeddings: La Representacion del Conocimiento

### Que es un embedding?

Un embedding es una representacion numerica (vector) de un texto en un espacio de alta dimensionalidad. Textos con significado similar tienen vectores cercanos.

```
"vacaciones"          → [0.12, -0.34, 0.56, ..., 0.78]   (1536 dims)
"dias libres"         → [0.11, -0.33, 0.55, ..., 0.77]   ← MUY CERCANO
"deploy en kubernetes"→ [0.89, 0.12, -0.67, ..., 0.03]   ← MUY LEJANO
```

### Modelos de embedding populares

| Modelo | Dimensiones | Contexto | Costo (1M tokens) | Mejor para |
|--------|-------------|----------|--------------------|------------|
| `text-embedding-3-small` (OpenAI) | 1536 | 8191 tokens | $0.02 | Uso general, bajo costo |
| `text-embedding-3-large` (OpenAI) | 3072 | 8191 tokens | $0.13 | Alta precision |
| `text-embedding-ada-002` (OpenAI) | 1536 | 8191 tokens | $0.10 | Legacy, aun popular |
| Cohere `embed-v3` | 1024 | 512 tokens | $0.10 | Multilingue |
| Sentence-BERT (open source) | 768 | 512 tokens | Gratis | Sin dependencia de API |
| BGE-M3 (BAAI, open source) | 1024 | 8192 tokens | Gratis | Multilingue + codigo |

### Codigo: Crear embeddings

```python
from openai import OpenAI

client = OpenAI()

respuesta = client.embeddings.create(
    model="text-embedding-3-small",
    input=["vacaciones de la empresa", "deploy en produccion"]
)

vec_vacaciones = respuesta.data[0].embedding  # [0.12, -0.34, ...]
vec_deploy = respuesta.data[1].embedding       # [0.89, 0.12, ...]

print(f"Dimensiones: {len(vec_vacaciones)}")  # 1536
```

### Intuicion geometrica

Los embeddings mapean texto a puntos en un espacio vectorial. La "distancia" entre puntos refleja similitud semantica:

```
Espacio de embeddings (simplificado a 2D):

    ▲ dimension_2
    │
    │   ● "politica de vacaciones"
    │   ● "dias libres anuales"          ← cluster RRHH
    │   ● "licencia por enfermedad"
    │
    │
    │                    ● "deploy en k8s"
    │                    ● "rotacion de secretos"   ← cluster TECH
    │                    ● "CI/CD pipeline"
    │
    └──────────────────────────────────────→ dimension_1
```

**Critica importante**: Los embeddings NO son perfectos. Capturan similitud semantica superficial, no razonamiento profundo. "El gato come raton" y "El raton come gato" tendran embeddings MUY similares a pesar de significar cosas opuestas. Esto importa en retrieval.

---

## 5. Bases de Datos Vectoriales

### Que es una base de datos vectorial?

Una base de datos optimizada para almacenar, indexar y buscar vectores de alta dimensionalidad. A diferencia de una base de datos relacional (que busca por igualdad exacta), una vector DB busca por **similitud aproximada**.

```
Base de datos relacional:        Base de datos vectorial:
SELECT * FROM docs               SELECT * FROM docs
WHERE id = 123                   ORDER BY distance(query_vec, doc_vec)
                                 LIMIT 5
↑ Busqueda exacta                ↑ Busqueda por similitud (ANN)
```

### Metricas de similitud

Las tres metricas mas usadas para medir "cercania" entre vectores:

**1. Similitud Coseno** (la mas comun)
```
              A · B
cos(θ) = ─────────────
          ||A|| × ||B||

Rango: [-1, 1]  (1 = identicos, 0 = ortogonales, -1 = opuestos)

Ventaja:  Invariante a la magnitud del vector
Cuando:   Uso general, embeddings de texto
```

**2. Distancia Euclidiana (L2)**
```
d(A,B) = √(Σ(ai - bi)²)

Rango: [0, ∞)  (0 = identicos, mayor = mas lejanos)

Ventaja:  Intuitiva geometricamente
Cuando:   Embeddings normalizados, clustering
```

**3. Producto Punto (Dot Product)**
```
A · B = Σ(ai × bi)

Rango: (-∞, ∞)  (mayor = mas similares)

Ventaja:  Rapido de computar
Cuando:   Embeddings normalizados (equivale a coseno)
```

**Regla practica**: Si no sabes cual usar, usa **similitud coseno**. Es la mas robusta para embeddings de texto.

### Algoritmos de indexacion (como buscan rapido)

Buscar el vector mas cercano entre millones no puede ser fuerza bruta (O(n)). Las vector DBs usan algoritmos de Approximate Nearest Neighbors (ANN):

| Algoritmo | Como funciona | Trade-off |
|-----------|---------------|-----------|
| **HNSW** (Hierarchical Navigable Small World) | Grafo multi-capa que navega de nodos generales a especificos | Mejor recall, mas RAM |
| **IVF** (Inverted File Index) | Agrupa vectores en clusters, busca solo en clusters cercanos | Menor RAM, menor recall |
| **PQ** (Product Quantization) | Comprime vectores en sub-vectores | Minima RAM, menor precision |
| **Flat** (fuerza bruta) | Compara contra todos | Perfecto recall, O(n) lento |

**Para prototipo y aprendizaje**: Flat o HNSW (ChromaDB usa HNSW por default).
**Para produccion con millones de docs**: HNSW o IVF+PQ.

### Comparativa de bases de datos vectoriales

| Base de datos | Tipo | Mejor para | Hosting | Precio |
|---------------|------|------------|---------|--------|
| **ChromaDB** | Open source, embebida | Prototipos, desarrollo local | Local/Docker | Gratis |
| **FAISS** (Meta) | Libreria open source | Investigacion, alto rendimiento | Self-hosted | Gratis |
| **Pinecone** | Managed cloud | Produccion sin ops, escala automatica | Cloud | $$$, desde $70/mes |
| **Weaviate** | Open source + cloud | Busqueda hibrida, multimodal | Local/Cloud | Gratis (OSS) |
| **Qdrant** | Open source + cloud | Alto rendimiento, filtrado avanzado | Local/Cloud | Gratis (OSS) |
| **pgvector** | Extension PostgreSQL | Equipos que ya usan PostgreSQL | Donde sea | Gratis |
| **Milvus** | Open source distribuido | Escala masiva (billones de vectores) | Self-hosted | Gratis |

### Cuando usar cual

```
¿Prototipando o aprendiendo?
  └──→ ChromaDB (0 config, embebida, perfecto para notebooks)

¿Produccion con equipo chico?
  └──→ pgvector (si ya usas PostgreSQL)
  └──→ Qdrant/Weaviate (si quieres especializado)

¿Produccion a escala con presupuesto?
  └──→ Pinecone (managed, 0 ops)

¿Millones/billones de vectores?
  └──→ Milvus o FAISS con IVF+PQ
```

### Codigo: ChromaDB basico

```python
import chromadb

# Crear cliente (en memoria para desarrollo)
client = chromadb.Client()

# Crear coleccion (equivale a una "tabla")
collection = client.create_collection(
    name="base_conocimiento",
    metadata={"hnsw:space": "cosine"}  # metrica de distancia
)

# Insertar documentos (ChromaDB genera embeddings automaticamente)
collection.add(
    documents=[
        "La empresa ofrece 20 dias de vacaciones al ano.",
        "El onboarding incluye 3 sesiones de mentoria.",
        "Los deploys se hacen con Kubernetes y ArgoCD.",
    ],
    metadatas=[
        {"dominio": "rrhh", "seccion": "vacaciones"},
        {"dominio": "rrhh", "seccion": "onboarding"},
        {"dominio": "tech", "seccion": "infraestructura"},
    ],
    ids=["doc_1", "doc_2", "doc_3"],
)

# Buscar por similitud semantica
resultados = collection.query(
    query_texts=["cuantos dias libres tengo?"],
    n_results=2,
    where={"dominio": "rrhh"},  # filtro por metadata
)

print(resultados["documents"])
# [['La empresa ofrece 20 dias de vacaciones al ano.',
#   'El onboarding incluye 3 sesiones de mentoria.']]
```

---

## 6. Estrategias de Chunking

El chunking es **el factor mas critico y subestimado** de un sistema RAG. Un mal chunking arruina todo el pipeline, sin importar que tan bueno sea tu modelo de embedding o tu LLM.

### Por que importa el chunking?

```
Documento completo (5000 tokens)
  │
  ├── Chunk demasiado grande (2000 tokens):
  │     → Diluye la senal, mete ruido irrelevante en el contexto
  │     → Gasta tokens del LLM en informacion innecesaria
  │
  ├── Chunk demasiado pequeno (50 tokens):
  │     → Pierde contexto, la frase suelta no tiene sentido
  │     → "20 dias" sin saber que habla de vacaciones
  │
  └── Chunk optimo (200-500 tokens):
        → Suficiente contexto para ser autonomo
        → Suficientemente especifico para ser relevante
```

### Estrategias principales

#### 1. Fixed-Size Chunking (el mas simple)

```python
def fixed_size_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Divide texto en chunks de tamano fijo con overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # overlap para no cortar ideas
    return chunks
```

**Ventaja**: Simple, predecible.
**Desventaja**: Corta en medio de oraciones/ideas. El overlap mitiga pero no resuelve.

#### 2. Recursive Character Splitting (LangChain default)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],  # orden de prioridad
)

chunks = splitter.split_text(documento)
```

**Ventaja**: Respeta estructura del documento (parrafos > oraciones > palabras).
**Desventaja**: Aun puede cortar ideas semanticas.

#### 3. Semantic Chunking

Agrupa texto por similitud semantica en lugar de tamano fijo:

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

chunker = SemanticChunker(
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    breakpoint_threshold_type="percentile",
)

chunks = chunker.split_text(documento)
```

**Ventaja**: Chunks semanticamente coherentes.
**Desventaja**: Mas lento, mas caro (requiere embeddings para chunking), tamano variable.

#### 4. Document-Structure Chunking

Usa la estructura del documento (headers, secciones) para dividir:

```python
from langchain.text_splitter import MarkdownTextSplitter

splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(documento_markdown)
```

**Ventaja**: Respeta la organizacion del autor.
**Desventaja**: Requiere documentos bien estructurados.

### Tabla comparativa de chunking

| Estrategia | Complejidad | Costo | Calidad chunks | Mejor para |
|------------|-------------|-------|----------------|------------|
| Fixed-size | Baja | Gratis | Media | Prototipado rapido |
| Recursive | Baja | Gratis | Buena | **Default recomendado** |
| Semantic | Alta | $$ (embeddings) | Muy buena | Docs heterogeneos |
| Document-structure | Media | Gratis | Muy buena | Docs bien formateados |

**Recomendacion**: Empieza con **Recursive**, mide calidad de retrieval, y solo mueve a Semantic si Recursive no es suficiente.

---

## 7. Estrategias de Retrieval

### Retrieval Denso (Dense Retrieval)

Usa embeddings para buscar por similitud semantica. Es lo que hemos visto hasta ahora.

```python
# El query se convierte en vector y se busca por similitud
resultados = collection.query(
    query_texts=["como roto secretos en kubernetes"],
    n_results=5,
)
```

**Fortaleza**: Entiende sinonimos y parafraseo ("dias libres" ≈ "vacaciones").
**Debilidad**: Puede fallar con terminos tecnicos exactos (IDs, nombres propios, codigos).

### Retrieval Disperso (Sparse Retrieval)

Usa metodos clasicos como BM25/TF-IDF que buscan por coincidencia de palabras clave.

```python
# BM25 busca por overlap de tokens exactos
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_documents(docs, k=5)
resultados = bm25_retriever.invoke("error ERR_K8S_SECRET_ROTATION_FAIL")
```

**Fortaleza**: Excelente para terminos exactos, codigos, IDs.
**Debilidad**: No entiende sinonimos ("vacaciones" ≠ "dias libres").

### Retrieval Hibrido (la mejor opcion en produccion)

Combina denso + disperso con un merge strategy:

```python
from langchain.retrievers import EnsembleRetriever

hibrido = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.6, 0.4],  # 60% semantico, 40% keyword
)

resultados = hibrido.invoke("error en rotacion de secretos kubernetes")
# Captura TANTO la semantica como los terminos exactos
```

**Esto es lo que deberias usar en produccion.** Dense solo es suficiente para prototipos.

### Re-ranking (post-retrieval refinement)

Despues de recuperar los top-K documentos, un modelo de re-ranking los reordena por relevancia mas fina:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

reranker = CohereRerank(model="rerank-v3.5", top_n=3)
retriever_con_rerank = ContextualCompressionRetriever(
    base_retriever=hibrido,
    base_compressor=reranker,
)
```

**Por que re-ranking?** El retriever inicial es rapido pero impreciso (ANN). El re-ranker es lento pero preciso. Usas el primero para filtrar y el segundo para refinar.

```
1000 docs → Retriever (ANN, rapido) → 20 candidatos → Re-ranker (preciso) → 5 mejores
```

---

## 8. Tecnicas Avanzadas de RAG

### 8.1 Query Transformation

El query del usuario suele ser ambiguo o incompleto. Transformarlo antes de buscar mejora el retrieval:

**Multi-Query**: Genera variaciones del query original

```python
# Query original: "vacaciones"
# Queries generadas:
# - "politica de dias libres anuales para empleados"
# - "cuantos dias de vacaciones corresponden por ano"
# - "proceso para solicitar vacaciones"
# Se busca con TODOS y se deduplicar resultados
```

**HyDE (Hypothetical Document Embeddings)**: Genera un documento hipotetico que responderia la pregunta, y usa ESE embedding para buscar

```python
# Query: "vacaciones"
# HyDE genera: "La empresa ofrece 20 dias de vacaciones anuales para
#               empleados full-time, con posibilidad de acumular hasta
#               5 dias para el siguiente periodo..."
# Se busca con el embedding de ESTE texto hipotetico
# → Mejor match porque el embedding es mas cercano al documento real
```

**Step-back Prompting**: Genera una pregunta mas general antes de buscar

```python
# Query: "puedo tomar vacaciones en mi primer mes?"
# Step-back: "cuales son las politicas de vacaciones y periodos de prueba?"
# → Recupera informacion mas completa
```

### 8.2 Self-RAG (RAG con autocritica)

El sistema evalua la calidad de su propio retrieval y generacion:

```
┌──────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Query│───→│ Retrieve  │───→│ Grade    │───→│ Generate │
└──────┘    │ docs      │    │ relevance│    │ answer   │
            └──────────┘    └────┬─────┘    └────┬─────┘
                                 │                │
                          ┌──────▼──────┐   ┌────▼──────┐
                          │ Irrelevant? │   │ Hallucin? │
                          │ → Re-query  │   │ → Re-gen  │
                          └─────────────┘   └───────────┘
```

Esta arquitectura la implementaremos con **prompt chaining** en la Notebook 03.

### 8.3 RAG con Routing Multi-Dominio

Cuando tienes multiples bases de conocimiento (RRHH, Tech, Legal), un router clasifica la intencion y dirige al retriever especializado:

```
                         ┌─────────────┐
                         │  Classifier │
                         │  (intent)   │
                         └──────┬──────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
              ┌─────▼────┐ ┌───▼─────┐ ┌───▼──────┐
              │ HR RAG   │ │Tech RAG │ │ Fallback │
              │ Agent    │ │ Agent   │ │ Agent    │
              └─────┬────┘ └───┬─────┘ └───┬──────┘
                    │          │           │
                    └──────────┼───────────┘
                               │
                         ┌─────▼──────┐
                         │  Response  │
                         │  Envelope  │
                         └────────────┘
```

Esta arquitectura la implementaremos con **routing** en la Notebook 04.

---

## 9. RAG + Agentes: Dos Enfoques

### Enfoque 1: Prompt Chaining

Cadena secuencial donde cada paso refina el anterior:

```
Query Analysis → Retrieval → Context Grading → Generation → Answer Validation
     │                              │                              │
     │                        ¿Contexto                      ¿Respuesta
     │                        relevante?                     fiel al contexto?
     │                          │    │                          │    │
     │                         SI   NO──→ Re-query             SI   NO──→ Re-generate
     │                          │                               │
     │                          ▼                               ▼
     └────────────────── Flujo continua ───────────────── Respuesta final
```

**Cuando usar prompt chaining para RAG**:
- Necesitas control de calidad en cada etapa
- El costo de una respuesta incorrecta es alto
- Quieres trazabilidad de por que fallo
- Ejemplo: chatbot medico, asesor legal, soporte critico

**Cuando NO usar**:
- Queries simples con retrieval directo
- Latencia es critica (< 2s)
- El costo de tokens es prioridad absoluta

### Enfoque 2: Routing

Decision condicional que dirige al agente especializado:

**Cuando usar routing para RAG**:
- Multiples dominios con bases de conocimiento distintas
- Cada dominio requiere estrategia de retrieval o generacion diferente
- Quieres escalar anadiendo nuevos dominios sin refactorear
- Ejemplo: helpdesk corporativo (RRHH + IT + Legal + Finanzas)

**Cuando NO usar**:
- Un solo dominio de conocimiento
- Las categorias no son distinguibles
- El costo del clasificador no compensa

### Comparacion directa

| Aspecto | Prompt Chaining | Routing |
|---------|----------------|---------|
| **Estructura** | Secuencial (A→B→C→D) | Condicional (A→{B\|C\|D}) |
| **Foco** | Calidad de una respuesta | Especializacion por dominio |
| **Latencia** | Mayor (mas pasos) | Menor (solo un branch) |
| **Costo tokens** | Mayor (evaluaciones intermedias) | Menor (clasificacion + 1 branch) |
| **Complejidad** | Media-alta | Media |
| **Mejor para** | RAG critico con autocorreccion | RAG multi-dominio |

**En la practica, se combinan**: Routing selecciona el dominio, y dentro de cada dominio el agente usa prompt chaining para asegurar calidad.

---

## 10. RAG vs Fine-tuning: Cuando Usar Cada Uno

Esta es una de las preguntas mas frecuentes. La respuesta no es "uno u otro" — son herramientas complementarias con objetivos distintos.

| Criterio | RAG | Fine-tuning |
|----------|-----|-------------|
| **Que resuelve** | Acceso a conocimiento externo/actualizado | Adaptar comportamiento/estilo del modelo |
| **Datos necesarios** | Documentos (no etiquetados) | Dataset curado de pares input/output |
| **Actualizacion** | Instantanea (cambias docs) | Re-entrenamiento (horas/dias) |
| **Costo inicial** | Bajo (API + vector DB) | Alto (GPU, dataset, iteracion) |
| **Costo por query** | Medio (embedding + retrieval + generation) | Bajo (solo generation) |
| **Alucinaciones** | Reducidas (cita fuentes) | Puede empeorar si datos son malos |
| **Trazabilidad** | Alta (puedes auditar chunks usados) | Baja (caja negra) |

### Matriz de decision

```
¿Necesitas que el modelo SEPA datos nuevos/privados?
  └──→ RAG

¿Necesitas que el modelo SE COMPORTE de forma diferente?
  └──→ Fine-tuning

¿Necesitas ambos?
  └──→ Fine-tuning para estilo + RAG para conocimiento
       (ej: modelo fine-tuned para responder como tu marca + RAG para datos del producto)
```

**Critica honesta**: En 2024-2025, con la ventana de contexto creciendo (128K→1M tokens), hay quien argumenta que "solo mete todo en el context window". Esto funciona para prototipos pero **NO escala**: costo O(n) por query, latencia proporcional al contexto, y no resuelve actualizacion continua.

---

## 11. Cuando NO Usar RAG

RAG no es la solucion universal. No lo uses cuando:

1. **El conocimiento ya esta en el modelo**: Si preguntas cosas de conocimiento general, RAG agrega costo sin valor
2. **No tienes documentos de calidad**: Garbage in, garbage out. RAG sobre documentos mal escritos produce respuestas mal fundamentadas
3. **La tarea es creativa**: Si quieres que el LLM genere poesia o brainstorm, no necesita "evidencia"
4. **Latencia sub-segundo es critica**: Retrieval agrega 200-500ms tipicamente
5. **El volumen de datos es trivial**: Si tienes 3 paginas de documentos, metelos en el system prompt directamente

---

## 12. Estructura del Modulo

```text
05_Rags/
  README.md                                          ← Este documento
  data/
    base_conocimiento_productos.md                   ← KB de productos (para demos)
    base_conocimiento_tecnica.md                     ← KB tecnica (para demos)
  Notebooks/
    01_bases_datos_vectoriales.ipynb                  ← Embeddings + ChromaDB desde cero
    02_rag_pipeline.ipynb                             ← Pipeline RAG completo paso a paso
    03_rag_prompt_chaining.ipynb                      ← RAG + agente con prompt chaining
    04_rag_routing.ipynb                              ← RAG + agente con routing multi-dominio
```

### Ruta de aprendizaje recomendada

```
Notebook 01 (fundamentos)
    ↓
Notebook 02 (pipeline completo)
    ↓
  ┌─────────────────────┐
  │ Elige segun tu caso │
  └───────┬─────────────┘
          │
    ┌─────┴──────┐
    ↓            ↓
Notebook 03   Notebook 04
(chaining)    (routing)
```

## 13. Setup

### Dependencias adicionales

Este modulo requiere dependencias que no estan en el `pyproject.toml` base:

```bash
# Desde la raiz del proyecto
uv pip install chromadb langchain-community scikit-learn matplotlib numpy
```

O si prefieres agregarlas al pyproject.toml:

```toml
# Agregar a dependencies en pyproject.toml
"chromadb>=0.5.0",
"langchain-community>=0.3.0",
"scikit-learn>=1.3.0",
"matplotlib>=3.8.0",
"numpy>=1.26.0",
```

### Variables de entorno

```bash
cp .env.example .env
```

Configura:
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### Ejecucion

```bash
# Desde la raiz del proyecto
cd 05_Rags

# Opcion 1: Ejecutar notebooks interactivamente
jupyter notebook Notebooks/01_bases_datos_vectoriales.ipynb

# Opcion 2: Ejecutar todas las notebooks (validacion)
uv run python ../tools/execute_notebooks.py 05_Rags/Notebooks/
```

---

## 14. Referencias

1. Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS.
2. Chip Huyen (2024). *AI Engineering: Building Applications with Foundation Models*. O'Reilly. Cap. 10.
3. Gao, Y. et al. (2024). *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv:2312.10997.
4. Asai, A. et al. (2023). *Self-RAG: Learning to Retrieve, Generate, and Critique*. arXiv:2310.11511.
5. LangChain Documentation. *RAG Techniques*. https://python.langchain.com/docs/tutorials/rag/
6. ChromaDB Documentation. https://docs.trychroma.com/

---

## Critica tecnica (honesta)

- RAG es poderoso pero **no es magia**. La calidad depende de: (1) calidad de los documentos fuente, (2) estrategia de chunking, (3) modelo de embeddings, (4) estrategia de retrieval. En ese orden de importancia.
- El 80% de los problemas de RAG en produccion son problemas de **datos**, no de arquitectura.
- Si no mides recall@k, precision@k y faithfulness, estas construyendo a ciegas.
- Un retriever hibrido (dense + sparse) con re-ranking supera a un retriever dense solo en casi todos los benchmarks. El costo adicional casi siempre vale la pena.
- Las vector DBs managed (Pinecone) son convenientes pero crean vendor lock-in. Evalua si pgvector o Qdrant cubren tu caso antes de comprometerte.

**La regla de oro**: Mide antes de optimizar. Un RAG naive bien medido es mejor que un RAG sofisticado sin metricas.
