# 06 — Proyecto Final: Cultural Intelligence System

Este es el proyecto que integra todo lo que aprendiste en el programa. Construís un sistema multi-agente completo con LangGraph que responde preguntas sobre tres dominios culturales: **películas de Christopher Nolan**, **libros de Stephen King** y **álbumes de Miles Davis**.

No es un proyecto de demostración. Tiene estado persistente, herramientas externas reales, evaluación automática, API REST con streaming, tests unitarios e integración, y despliegue en Docker. Es el tipo de sistema que presentarías en un portafolio profesional.

---

## Cómo está Organizado

El proyecto está dividido en 8 capítulos progresivos, cada uno un notebook, donde construís el sistema de menor a mayor complejidad. Los capítulos no son independientes: cada uno extiende el anterior.

```
06_project_langgraph/
├── 00_datos/                    # Datasets JSON: Nolan, King, Davis
├── 01_estado_y_grafos/          # Cap 01: TypedDict, StateGraph, START/END
├── 02_mensajes_y_llm/           # Cap 02: MessagesState, nodos LLM
├── 03_herramientas/             # Cap 03: @tool, ToolNode, loop ReAct
├── 04_enrutamiento_condicional/ # Cap 04: conditional edges, routing LLM
├── 05_salida_estructurada/      # Cap 05: Pydantic + with_structured_output
├── 06_memoria_y_checkpointing/  # Cap 06: MemorySaver, thread_id
├── 07_paralelizacion/           # Cap 07: Send(), fan-out, ramas paralelas
├── 08_sistema_multiagente/      # Cap 08: sub-grafos, streaming, xray
├── src/                         # Paquete de producción (cinematic_intelligence)
├── tests/                       # Tests unitarios e integración
└── docker/                      # Dockerfile + docker-compose
```

---

## Currículo del Proyecto

| Capítulo | Tema | Dominio de trabajo | Concepto central |
|:---:|---|---|---|
| 01 | Estado y Grafos | Nolan | TypedDict, StateGraph, START/END |
| 02 | Mensajes y LLM | King | MessagesState, add_messages, nodos LLM |
| 03 | Herramientas | Davis | @tool, ToolNode, loop ReAct completo |
| 04 | Enrutamiento Condicional | Los 3 | add_conditional_edges, routing semántico |
| 05 | Salida Estructurada | Nolan | with_structured_output, validación Pydantic |
| 06 | Memoria y Checkpointing | King | MemorySaver, thread_id, persistencia de sesión |
| 07 | Paralelización | Davis | Send(), fan-out, benchmark de rendimiento |
| 08 | Sistema Multi-agente | Los 3 | Sub-grafos, streaming SSE, xray de estado |

---

## Arquitectura del Sistema

El flujo de una consulta a través del sistema:

```
CulturalState (MessagesState)
      │
      ▼
 node_router        ← LLM clasifica el dominio con structured output
      │
 cultural_route()   ← función pura que lee state["domain"]
      │
 ┌────┴─────────────┬─────────────┐
 ▼                  ▼             ▼
nolan_specialist  king_specialist  davis_specialist
 └─────────────────┴─────────────┘
                   │
                   ▼
             node_synthesizer   ← formatea la respuesta final
                   │
                  END
```

Cada especialista tiene acceso a su propio dataset JSON y está optimizado para responder preguntas dentro de su dominio. El router decide a qué especialista enviar la consulta antes de que ninguno de ellos sea invocado.

---

## Setup del Proyecto

```bash
# Desde la raíz del proyecto (03-agents/)
cd 06_project_langgraph

# 1. Instalar dependencias
uv sync --extra dev

# 2. Configurar variables de entorno
cp .env.example .env
# Completar OPENAI_API_KEY en .env

# 3. Validar que los datasets están presentes
make data-validate

# 4. Correr los tests unitarios
make test-unit

# 5. Levantar la API en modo desarrollo
make api-dev
```

---

## API del Sistema

Una vez levantada la API, podés interactuar con el sistema via HTTP:

```
GET  /                          → Health check
GET  /domains                   → Lista de dominios disponibles
POST /chat/{thread_id}          → Consulta completa (respuesta al finalizar)
POST /chat/{thread_id}/stream   → Respuesta en streaming (SSE)
DELETE /chat/{thread_id}        → Limpiar sesión (requiere PostgreSQL en prod)
```

Ejemplo de consulta:

```bash
# Pregunta simple
curl -X POST http://localhost:8006/chat/mi_sesion \
  -H "Content-Type: application/json" \
  -d '{"message": "Explicá la técnica narrativa de Inception"}'

# Streaming
curl -X POST http://localhost:8006/chat/mi_sesion/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son los temas recurrentes de Stephen King?"}'
```

---

## Tests

```bash
make test-unit        # Tests unitarios (sin llamadas reales a la API)
make test-integration # Tests de integración (con mocks del grafo)
make test             # Suite completa
```

---

## Docker

```bash
make api-docker       # Build + levantar en background
make api-docker-down  # Detener

# Con Jupyter Lab (perfil de desarrollo)
docker compose -f docker/docker-compose.yml --profile dev up
```

---

## Notas de Producción

**Memoria**: `MemorySaver` almacena el estado en memoria RAM. Si la API se reinicia, el historial se pierde. Para persistencia real en producción, reemplazarlo por `langgraph-checkpoint-postgres`.

**Modelo**: `OPENAI_MODEL` es configurable en `.env`. Por defecto usa `gpt-4o-mini`. Podés cambiarlo a `gpt-4o` si necesitás mayor capacidad de razonamiento.

**Trazabilidad**: para activar LangSmith tracing, configurá `LANGCHAIN_TRACING_V2=true` y `LANGCHAIN_API_KEY` en `.env`. Cada invocación del grafo quedará trazada en el dashboard de LangSmith.

---

## Criterio de Entrega

El proyecto está completo cuando:

- Los 8 capítulos de notebooks corren sin errores de principio a fin
- `make test` pasa sin fallos
- La API responde correctamente a consultas de los tres dominios
- La API funciona desde Docker con `make api-docker`
