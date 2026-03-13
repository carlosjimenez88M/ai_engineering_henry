"""
db.py

Objetivo del script: 
Database and checkpointer management for the Cultural Intelligence API.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from langgraph.checkpoint.memory import MemorySaver

_checkpointer: MemorySaver | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and clean up application resources."""
    global _checkpointer
    _checkpointer = MemorySaver()
    yield
    _checkpointer = None


def get_checkpointer() -> MemorySaver:
    """Dependency that returns the global MemorySaver instance."""
    if _checkpointer is None:
        raise RuntimeError("Checkpointer not initialized. Did lifespan run?")
    return _checkpointer


CheckpointerDep = Annotated[MemorySaver, Depends(get_checkpointer)]
