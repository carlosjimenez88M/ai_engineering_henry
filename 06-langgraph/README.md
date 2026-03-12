# Módulo 06: LangGraph — Cultural Intelligence System

Sistema multi-agente construido con LangGraph que responde preguntas sobre **películas de Christopher Nolan**, **libros de Stephen King** y **álbumes de Miles Davis**.

## Estructura del Módulo

```
06-langgraph/
├── 00_datos/              # Datasets JSON (Nolan, King, Davis)
├── 01_estado_y_grafos/    # Cap 01: TypedDict, StateGraph, START/END
├── 02_mensajes_y_llm/     # Cap 02: MessagesState, LLM nodes
├── 03_herramientas/       # Cap 03: @tool, ToolNode, ReAct loop
├── 04_enrutamiento_condicional/ # Cap 04: Conditional edges, routing
├── 05_salida_estructurada/ # Cap 05: Pydantic + with_structured_output
├── 06_memoria_y_checkpointing/ # Cap 06: MemorySaver, thread_id
├── 07_paralelizacion/     # Cap 07: Send(), fan-out, parallel branches
├── 08_sistema_multiagente/ # Cap 08: Sub-graphs, streaming
├── src/cinematic_intelligence/ # Production-grade package
├── tests/                 # Unit + integration tests
└── docker/                # Dockerfile + docker-compose
```

## Setup Rápido

```bash
# 1. Instalar dependencias
cd ai_engineering_henry/06-langgraph
uv sync --extra dev

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY

# 3. Validar datos
make data-validate

# 4. Ejecutar tests
make test-unit

# 5. Iniciar API
make api-dev
```

## Curriculum

| Capítulo | Tema | Dominio | Concepto clave |
|----------|------|---------|----------------|
| 01 | Estado y Grafos | Nolan | TypedDict, StateGraph, START/END |
| 02 | Mensajes y LLM | King | MessagesState, add_messages |
| 03 | Herramientas | Davis | @tool, ToolNode, ReAct loop |
| 04 | Enrutamiento | Los 3 | add_conditional_edges, routing LLM |
| 05 | Salida Estructurada | Nolan | with_structured_output, Pydantic |
| 06 | Memoria | King | MemorySaver, thread_id, checkpointing |
| 07 | Paralelización | Davis | Send(), fan-out, benchmark |
| 08 | Multi-agente | Los 3 | Sub-graphs, streaming, xray |

## API Endpoints

```
GET  /                          → Health check
GET  /domains                   → ["nolan", "king", "davis"]
POST /chat/{thread_id}          → Consulta completa
POST /chat/{thread_id}/stream   → Respuesta streaming SSE
DELETE /chat/{thread_id}        → 501 (usar PostgreSQL en producción)
```

### Ejemplo de uso

```bash
# Consulta simple
curl -X POST http://localhost:8006/chat/mi_sesion \
  -H "Content-Type: application/json" \
  -d '{"message": "Explica la técnica narrativa de Inception"}'

# Streaming
curl -X POST http://localhost:8006/chat/mi_sesion/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son los temas recurrentes de Stephen King?"}'
```

## Arquitectura del Sistema

```
CulturalState (MessagesState)
      │
      ▼
 node_router        ← LLM clasifica domain con structured output
      │
 cultural_route()   ← función pura lee state["domain"]
      │
 ┌────┴────────────┬─────────────┐
 ▼                 ▼             ▼
nolan_specialist king_specialist davis_specialist
 └────────────────┴─────────────┘
                  │
                  ▼
            node_synthesizer   ← formatea respuesta final
                  │
                 END
```

## Notas de Producción

- **MemorySaver** es in-memory, no persiste entre reinicios. Para producción, usar `langgraph-checkpoint-postgres`.
- **OPENAI_MODEL** es configurable via `.env`. Por defecto usa `gpt-4o-mini`.
- Para activar LangSmith tracing: `LANGCHAIN_TRACING_V2=true` + `LANGCHAIN_API_KEY=...`

## Tests

```bash
make test-unit        # Tests sin API real (~rápidos)
make test-integration # Tests de grafo e integración (mocked)
make test             # Todos
```

## Docker

```bash
make api-docker       # Build + start en background
make api-docker-down  # Stop

# Con Jupyter Lab (perfil dev)
docker compose -f docker/docker-compose.yml --profile dev up
```
