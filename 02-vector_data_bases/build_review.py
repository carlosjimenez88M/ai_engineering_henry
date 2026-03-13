"""
build_review.py

Objetivo del script: 
Construye el notebook de repaso para los Modulos 1 y 2.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json

def md(text):
    return {\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": [text]}

def code(text):
    return {\"cell_type\": \"code\", \"execution_count\": None, \"metadata\": {}, \"outputs\": [], \"source\": [text]}

cells = []

# HEADER
cells.append(md(\"<a href=\\\"https://colab.research.google.com/github/carlosjimenez88M/ai_engineering_henry/blob/main/02-vector_data_bases/00_clase_de_repaso.ipynb\\\" target=\\\"_parent\\\"><img src=\\\"https://colab.research.google.com/assets/colab-badge.svg\\\" alt=\\\"Open In Colab\\\"/></a>\"))

cells.append(md(\"\"\"# MIT Applied AI Engineering: Clase de Repaso Exhaustiva (Módulos 01 y 02)

---

**Profesor:** El rigor académico y práctico no permite saltos de fe. Me han pedido un repaso exhaustivo, así que repasaremos **absolutamente todo** lo que se ha visto a lo largo de los dos módulos de Ingeniería en Inteligencia Artificial. No dejaremos ni una sola carpeta sin revisar. Esta libreta condensa todos los conceptos fundacionales y avanzados. 

Tomen nota de las ejecuciones, esto es la Biblia del Midterm de AI Engineering. Empezaremos desde las bases de Python y llegaremos hasta la orquestación avanzada de Bases de Datos con múltiples agentes (Batman Ejercicios).
\"\"\"))

cells.append(code(\"\"\"# %pip install -qU langchain langchain-openai langchain-community langgraph chromadb pydantic tiktoken python-dotenv rank_bm25 scikit-learn transformers sentence-transformers faiss-cpu
import os
from dotenv import load_dotenv

# Reemplaza o asegura tener el .env en tu ruta de ejecución
load_dotenv()
if not os.environ.get(\"OPENAI_API_KEY\"):
    print(\"[WARN] OPENAI_API_KEY no detectada. Las celdas LLM fallarán.\")
\"\"\"))

# M1 - 00_python_extra_class
cells.append(md(\"\"\"## 1. Módulo 01: Python y Software Engineering (Carpeta `00_python_extra_class` y `01_introduction`)
Antes de invocar LLMs, un AI Engineer debe escribir Python de producción.
### 1.1 Robustez, Validaciones y Pydantic
Los modelos devuelven strings impredecibles. `Pydantic` es el escudo de validación. Vimos manejo de errores y logging avanzado.\"\"\"))

cells.append(code(\"\"\"from pydantic import BaseModel, Field

# Validando entradas estrictas que sacariamos de un LLM
class OutputModelo(BaseModel):
    razonamiento: str = Field(description=\"Pasos lógicos\")
    accion_final: str = Field(description=\"Herramienta a usar o respuesta final\")
    confianza: float = Field(ge=0.0, le=1.0)

try:
    salida_simulada = {\"razonamiento\": \"El usuario pide X\", \"accion_final\": \"BUSCAR\", \"confianza\": 1.5}
    obj = OutputModelo(**salida_simulada)
except Exception as e:
    print(\"Error capturado correctamente de Pydantic:\", e)
\"\"\"))

# M1 - 02_prompting + 03_langchain_prompting
cells.append(md(\"\"\"## 2. Ingeniería de Prompts, LangChain Base y Paradigmas de Razonamiento (Carpetas `02_prompting` y `03_langchain_prompting`)
El núcleo de la interacción estocástica. Dejamos de tratar al modelo como una caja negra devolviendo texto plano y forzamos su formato.

### 2.1 Patrones Base y LCEL
Zero-Shot, Few-Shot, Role Prompting. En LangChain usamos el operador `|` (LCEL) para tuberías limpias.\"\"\"))

cells.append(code(\"\"\"from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model=\"gpt-4o-mini\", temperature=0)

# Few shot encadenado nativo (LCEL)
few_shot_prompt = ChatPromptTemplate.from_messages([
    (\"system\", \"Eres el Profesor del MIT. Resume el concepto central técnico.\"),
    (\"user\", \"No entiendo qué es Docker.\"),
    (\"assistant\", \"Contenedores aislados eficientes.\"),
    (\"user\", \"{pregunta}\")
])

chain_basica = few_shot_prompt | llm | StrOutputParser()
print(\"Zero/Few Shot:\", chain_basica.invoke({\"pregunta\": \"No entiendo LangChain\"}))
\"\"\"))

cells.append(md(\"\"\"### 2.2 Chain of Thought (CoT) y ReAct (Reason + Act)
En `04_cot` forzamos el *\"pensar paso a paso\"*. 
En `05_react` implementamos bucles de: **Pensamiento -> Acción -> Observación**. 
Cuando lo migramos a `03_langchain_prompting` usamos LangGraph para gestionar ese bucle.\"\"\"))

cells.append(code(\"\"\"# Simulación visual del Trace ReAct
import json
prompt_react = \"\"\"
Usa el formato: Thought -> Action -> Observation -> Final Answer.
\"\"\"
print(\"Patrón ReAct:\")
print(\"[Thought]: El usuario quiere saber del clima.\")
print(\"[Action]:  Invocar API(clima_hoy)\")
print(\"[Observation]: Soleado, 25C.\")
print(\"[Final Answer]: Hoy hace sol y 25 grados.\")
\"\"\"))

# M1 - 04_langchain_langgraph
cells.append(md(\"\"\"## 3. Orquestación Avanzada: LangGraph (Carpeta `04_langchain_langgraph`)
Las cadenas lineales se rompen con tareas heterogéneas. LangGraph introdujo Grafos Dirigidos. Revisemos los patrones:
1. **Prompt Chaining**: `A -> B -> C`.
2. **Parallelization**: Ejecutar tareas al unísono.
3. **Orchestrator-Worker**: Un jefe que divide tareas a N trabajadores.
4. **Evaluator-Optimizer**: Un bucle de mejora continua de respuestas.
5. **Routing**: Tomar decisiones de rama (`if/else` condicional en el flujo).
6. **Agent Feedback**: Intervención humana simulada o automática.

Aquí la implementación base fundamental del **Routing**:\"\"\"))

cells.append(code(\"\"\"from typing import TypedDict
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    input_text: str
    decision: str
    result: str

def classify_input(state: AgentState):
    print(\"[Node] Clasificando...\")
    # Logica simulada de un LLM: si tiene la palabra 'codigo', vamos a dev
    if \"codigo\" in state[\"input_text\"]:
        return {\"decision\": \"dev_agent\"}
    return {\"decision\": \"support_agent\"}

def build_dev(state: AgentState):
    print(\"[Node] Ejecutando Dev Agent...\")
    return {\"result\": \"def foo(): pass\"}

def build_support(state: AgentState):
    print(\"[Node] Ejecutando Support Agent...\")
    return {\"result\": \"Aquí tienes un manual.\"}

def route_decision(state: AgentState) -> str:
    return state[\"decision\"]

workflow = StateGraph(AgentState)
workflow.add_node(\"classifier\", classify_input)
workflow.add_node(\"dev_agent\", build_dev)
workflow.add_node(\"support_agent\", build_support)

workflow.set_entry_point(\"classifier\")
# Condicional Edge (El núcleo del patrón Routing)
workflow.add_conditional_edges(
    \"classifier\",
    route_decision,
    {\"dev_agent\": \"dev_agent\", \"support_agent\": \"support_agent\"}
)
workflow.add_edge(\"dev_agent\", END)
workflow.add_edge(\"support_agent\", END)

app_router = workflow.compile()
print(\"Graph Compiled. Invocando con 'codigo':\")
print(app_router.invoke({\"input_text\": \"Ayuda con el codigo Python\"})[\"result\"])
\"\"\"))


# M2 - 01_intro & 02_databases
cells.append(md(\"\"\"## 4. Fundamentos Visión Vectorial y Embeddings (Carpetas `01_intro` y `02_databases` del Módulo 2)
¿Cómo entiende una máquina el texto? A través de **Tokens** y dimensiones numéricas (Embeddings generados por *Transformers*).
Vimos enfoques léxicos (TFIDF, Bag of Words) superados por comprensión de contexto profunda.
En bases de datos (`ChromaDB`, `FAISS`) guardamos esos vectores y hacemos **Búsqueda KNN (K-Nearest Neighbors)** evaluando *Similitud Coseno*.\"\"\"))

cells.append(code(\"\"\"import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_openai import OpenAIEmbeddings

# 1. TF-IDF (Léxico superficial, de 01_intro/02_rag_tfidf)
corpus = [\"El gato come pez\", \"El felino devora salmón\", \"El coche es rojo\"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print(\"Vocabulario TF-IDF:\", vectorizer.get_feature_names_out())

# 2. Embeddings Densos (Semánticos profundos)
try:
    emb_model = OpenAIEmbeddings(model=\"text-embedding-3-small\")
    v1 = np.array(emb_model.embed_query(corpus[0]))
    v2 = np.array(emb_model.embed_query(corpus[1]))
    v3 = np.array(emb_model.embed_query(corpus[2]))
    
    def cosine_sim(a, b): return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    print(\"Similitud (Gato vs Felino):\", round(cosine_sim(v1, v2), 3))
    print(\"Similitud (Gato vs Coche):\", round(cosine_sim(v1, v3), 3))
except:
    print(\"Se necesita OPENAI_API_KEY para hacer el request real de OpenAI Embeddings.\")
\"\"\"))

cells.append(md(\"\"\"### 4.1 Chunking e Ingesta en Producción
En `02-bases-vectoriales-produccion.ipynb` el manejo de la información es exhaustivo. Usamos metadatos estructurados para aislar la búsqueda.\"\"\"))

cells.append(code(\"\"\"from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

docs = [
    Document(page_content=\"Factura A: $500\", metadata={\"tipo\": \"facturacion\", \"year\": 2024}),
    Document(page_content=\"Factura B: $1000\", metadata={\"tipo\": \"facturacion\", \"year\": 2023}),
    Document(page_content=\"Políticas vacacionales 2024\", metadata={\"tipo\": \"rrhh\"})
]

try:
    vectordb = Chroma.from_documents(docs, emb_model)
    # Filtrado por Metadatos - Criterial Crucial
    res = vectordb.similarity_search(\"Facturação\", filter={\"year\": 2024})
    print(\"Resultado filtrado metadatos:\", res[0].page_content)
except:
    print(\"No hay Chroma instanciada sin token (Fallback)\")
\"\"\"))


# M2 - 03_rag (Avanzado, Multi-Query, Ensemble RRF)
cells.append(md(\"\"\"## 5. RAG Avanzado: Combate al Recall Pobre (Carpeta `03_rag`)
El *Retrieval-Augmented Generation* falla si las palabras clave del usuario no concuerdan perfectamente con la Base Vectorial.

### 5.1 Multi-Query RAG
Uso del LLM para re-frasear la pregunta de 3 a 5 formas distintas, recuperar documentos para TODAS, y luego fusionar evitando duplicidad.

### 5.2 Ensemble Retriever con RRF (Reciprocal Rank Fusion)
Fusionamos lo semántico (`Chroma`) con lo léxico estadístico puro (`BM25Retriever`). Lo mejor de ambos mundos: encuentra sinónimos semánticos y encuentra los Acrónimos (IDs, SKUs) correctos.\"\"\"))

cells.append(code(\"\"\"from langchain_community.retrievers import BM25Retriever
from langchain_core.runnables import RunnableLambda

# Setup de datos de prueba
data_docs = [
    Document(page_content=\"El sistema de VacaTrack V3.2 está apagado.\"),
    Document(page_content=\"El módulo de licencias del personal no responde.\")
]
bm25 = BM25Retriever.from_documents(data_docs)

print(\"BM25 Buscando exactamente 'VacaTrack V3.2':\")
print(bm25.invoke(\"VacaTrack V3.2\")[0].page_content)

# En Ensemble, correríamos BM25 + Chroma, y fusionaríamos usando la fórmula RRF:
# score_RRF = 1 / (rank_lexico + k)  +  1 / (rank_semantico + k)
\"\"\"))

# M2 - 04_batman_vector_db_orchestration
cells.append(md(\"\"\"## 6. Integración Total: Orquestación de Bases Vectoriales de Batman (Carpeta `04_batman_vector_db_orchestration`)
Finalmente, la carpeta 04 nos enseñó diseño de alto nivel conectando a los Agentes. Aquí analizamos:
1. **Diseño de Vector DB**: Estructurar metadatos para Gotham.
2. **RAG vs Agentic RAG**: De pasar todo el contexto a un prompt pasivo, a **darle 'Tools' al Modelo** para que él decida si quiere buscar más contexto en la BD o ya le es suficiente.
3. **Agent 2 Agent Roles**: Ruteos donde el Batman-Agent de Análisis le delega al Batman-Agent Táctico tras consumir el VectorStore.

Este es el clímax de los dos módulos. Un agente con memoria a largo plazo vectorial.\"\"\"))

cells.append(code(\"\"\"from langchain_core.tools import tool

# Agentic RAG simplificado: RAG no como prompt, sino como una Tool ReAct
@tool
def buscar_criminologia_gotham(query: str) -> str:
    \"\"\"Busca expedientes de criminales pasados en la base de datos central de Gotham.\"\"\"
    # Aquí internamente haríamos un retriever.invoke(query)
    if \"joker\" in query.lower():
        return \"El Joker usa químicos en la planta de desechos.\"
    return \"No hay registros.\"

# El LLM (Batman) ahora tiene autonomía. No le inyectamos de golpe todo. 
# Él decide *si invocar o no* la DB Vectorial.
llm_with_tools = llm.bind_tools([buscar_criminologia_gotham])

print(\"Tool enlazada para Agentic RAG:\", list(llm_with_tools.kwargs.keys()))
\"\"\"))

cells.append(md(\"\"\"## Conclusión del MIT
Hemos ejecutado, paso a paso, cada carpeta y módulo base de la currícula 01 y 02.
- Hemos domado la fragilidad de texto con Pydantic.
- Establecimos Prompts condicionales y con roles.
- Estructuramos lógica estocástica a través de Estados en Grafo Dirigido (LangGraph).
- Convertimos strings en vectores y los medimos con coseno en bases vectoriales puras y Ensemble RRF.
- Finalmente, dotamos a nuestras máquinas de herramientas para Agentic RAG en Gotham.

Están listos para crear inteligencia asíncrona real en el **Módulo 03**.\"\"\"))

notebook_data = {
    \"cells\": cells,
    \"metadata\": {
        \"kernelspec\": {
            \"display_name\": \"Python 3\",
            \"language\": \"python\",
            \"name\": \"python3\"
        },
        \"language_info\": {
            \"name\": \"python\",
            \"version\": \"3.10.12\"
        }
    },
    \"nbformat\": 4,
    \"nbformat_minor\": 4
}

with open(\"/Users/carlosdaniel/Documents/Projects/Laborales/Henry/2026/01-introduction_ai_engineering/ai_engineering_henry/02-vector_data_bases/00_clase_de_repaso.ipynb\", \"w\") as f:
    json.dump(notebook_data, f, indent=1)

print(\"Notebook generated directly via JSON.\")
