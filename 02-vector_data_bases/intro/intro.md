# De Texto Completo a Agentic RAG: Busqueda Semantica sobre Don Quijote

## Por que bases de datos vectoriales?

Los LLMs tienen ventanas de contexto limitadas y costos proporcionales al numero de tokens. Pasar un corpus completo como contexto (**context stuffing**) funciona para textos cortos, pero no escala:

- **Costo**: ~20K tokens por query = ~$0.003/query. A 1000 queries/dia = $90/mes solo en contexto.
- **Latencia**: Mas tokens = mas tiempo de procesamiento.
- **"Lost in the middle"**: Los LLMs pierden informacion en la mitad de contextos largos (Liu et al., 2023).

Las **bases de datos vectoriales** resuelven esto: convierten texto en vectores numericos y permiten buscar **solo los fragmentos relevantes**, reduciendo tokens ~40x.

## Contenido de la notebook

La notebook `01_rag_tfidf.ipynb` implementa y compara 3 enfoques progresivos sobre un corpus real (~15K palabras de Don Quijote, capitulos I-VIII):

### Seccion 1: Context Stuffing

Pasar TODO el texto como contexto al LLM. Sirve como **baseline** para medir cuanto mejoran los otros enfoques.

- Medicion real de tokens, costo y latencia con `tiktoken`.
- Proyeccion de costos mensuales.

### Seccion 2: TF-IDF -- De Texto a Numeros

Explicacion completa de TF-IDF con formula, calculo manual y visualizacion:

- **Intuicion**: palabra importante = frecuente en documento + rara en corpus.
- **Calculo manual** con `collections.Counter` y comparacion con `TfidfVectorizer`.
- **Heatmap** de la matriz TF-IDF.
- **Limitacion clave**: TF-IDF no entiende semantica ("rocin flaco" vs "caballo delgado" = score 0).

### Seccion 3: ChromaDB -- Vector DB Real

Transicion a embeddings densos con **ChromaDB** y **OpenAI embeddings** (`text-embedding-3-small`):

- Chunking con `RecursiveCharacterTextSplitter` (500 chars, 50 overlap).
- Creacion de coleccion ChromaDB con embeddings de OpenAI.
- Comparacion side-by-side TF-IDF vs ChromaDB para las mismas queries.
- Heatmap dual: similitud sparse vs dense.

### Seccion 4: Simple RAG

Pipeline: Query -> Embed -> ChromaDB -> Top-3 chunks (~500 tokens) -> LLM.

- ~40x reduccion en tokens de contexto vs context stuffing.
- Comparacion directa de tokens, costo y latencia.

### Seccion 5: Agentic RAG con LangGraph

StateGraph con 7 nodos y conditional edges:

1. **analyze_query**: analiza y opcionalmente reformula la query.
2. **retrieve**: busca en ChromaDB con embeddings densos.
3. **grade_context**: evalua relevancia con structured output (`ContextGrade`).
4. **generate**: genera respuesta con el LLM.
5. **grade_answer**: evalua si la respuesta tiene alucinaciones (`AnswerGrade`).

Loops: contexto irrelevante -> re-query; alucinacion -> re-generate. Maximo 2 retries.

### Seccion 6: Evaluacion Comparativa

6 preguntas con ground truth keywords spanning capitulos I-VIII:

- Keyword recall como precision proxy.
- Bar chart 3-panel: tokens, precision, latencia.
- Proyeccion de costos mensuales (log scale).

## Tabla comparativa

| Dimension | Context Stuffing | Simple RAG | Agentic RAG |
|-----------|-----------------|------------|-------------|
| Tokens de contexto | ~20,000 | ~500 | ~500-1,500 |
| Costo por query | ~$0.003 | ~$0.0001 | ~$0.0005 |
| Autocorreccion | No | No | Si (grading loops) |
| Latencia | Media | Baja | Alta (multiples LLM calls) |
| Mejor para | Textos cortos, prototipos | Corpus medianos, produccion | Queries complejas |

## Prerequisitos y reproducibilidad

```bash
cd 02-vector_data_bases
uv sync                        # instala dependencias en .venv/
```

Configurar `OPENAI_API_KEY` en `.env` (la notebook usa `find_dotenv()` para localizarlo). Ver `.env.example` como referencia.

Ejecucion:

```bash
# Interactiva (VS Code apunta al venv via .vscode/settings.json)
# Abrir intro/01_rag_tfidf.ipynb y ejecutar todas las celdas

# Headless
make run-notebook
```

Todas las visualizaciones se generan inline con `plt.show()`. No se generan archivos externos.

## Lectura critica

### Fortalezas

- Corpus real (~15K palabras), no un parrafo de juguete.
- ChromaDB como vector store real con embeddings de OpenAI.
- Metricas cuantitativas: tokens, costo, latencia y precision por enfoque.
- Agentic RAG con reasoning loops reales (grading + re-query).

### Limitaciones

- Keyword recall no es una metrica robusta (produccion requiere RAGAS, ARES, o evaluacion humana).
- Corpus unico (Don Quijote). Generalizar requiere multiples corpus.
- ChromaDB in-memory: no persiste entre ejecuciones.
- Self-grading circular: el mismo LLM genera y evalua.

### Roadmap a produccion

1. Vector DB escalable (FAISS, Pinecone, Qdrant).
2. Golden dataset de evaluacion con scorecards humanas.
3. Observabilidad de trazas y costos (LangSmith, Phoenix).
4. Guardrails de seguridad, validacion de fuentes.
5. Experimentar con semantic chunking y agentic chunking.

## Referencias

- Chip Huyen (2024). *AI Engineering: Building Applications with Foundation Models*. O'Reilly.
- Asai, A., Wu, Z., Wang, Y., Sil, A., & Hajishirzi, H. (2023). *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*. arXiv:2310.11511.
- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). *Lost in the Middle: How Language Models Use Long Contexts*. arXiv:2307.03172.
