"""
main.py

Objetivo del script: 
FastAPI application for the Cultural Intelligence system.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import json
from typing import Any, AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from cinematic_intelligence.api.db import CheckpointerDep, lifespan
from cinematic_intelligence.graph import make_cultural_graph
from cinematic_intelligence.models import DomainEnum

app = FastAPI(
    title="Cultural Intelligence API",
    description="Multi-agent LangGraph system for Nolan films, King books, and Davis albums",
    version="1.0.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    """Request body for chat endpoints."""

    message: str


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


@app.get("/domains")
async def list_domains() -> list[str]:
    """List available cultural domains."""
    return [d.value for d in DomainEnum if d != DomainEnum.GENERAL]


@app.post("/chat/{thread_id}")
async def chat(
    thread_id: str,
    request: ChatRequest,
    checkpointer: CheckpointerDep,
) -> dict[str, Any]:
    """
    Send a message and get a complete response.

    The thread_id maintains conversation history across requests.
    """
    graph = make_cultural_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": thread_id}}

    result = graph.invoke(
        {"messages": [HumanMessage(content=request.message)]},
        config=config,
    )

    final_response = result.get("final_response")
    if final_response is None:
        raise HTTPException(status_code=500, detail="No response generated")

    return final_response.model_dump()


@app.post("/chat/{thread_id}/stream")
async def chat_stream(
    thread_id: str,
    request: ChatRequest,
    checkpointer: CheckpointerDep,
) -> StreamingResponse:
    """
    Send a message and receive a streaming SSE response.

    Returns text/event-stream with JSON chunks.
    """
    graph = make_cultural_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": thread_id}}

    async def generate() -> AsyncGenerator[str, None]:
        for chunk in graph.stream(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
            stream_mode="updates",
        ):
            yield f"data: {json.dumps(chunk, default=str)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.delete("/chat/{thread_id}")
async def delete_thread(thread_id: str) -> dict[str, str]:
    """
    Delete a conversation thread.

    Note: MemorySaver doesn't support deletion.
    In production, use a PostgreSQL-backed checkpointer.
    """
    raise HTTPException(
        status_code=501,
        detail=(
            "Thread deletion not implemented with MemorySaver. "
            "Use a PostgreSQL checkpointer in production."
        ),
    )
