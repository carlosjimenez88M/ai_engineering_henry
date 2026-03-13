"""
schemas.py

Objetivo del script: 
Pydantic schemas for intent routing and RAG outputs.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class IntentLabel(str, Enum):
    HR = "HR"
    TECH = "TECH"
    UNKNOWN = "UNKNOWN"


class IntentClassification(BaseModel):
    intent: IntentLabel
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str


class RAGAnswer(BaseModel):
    answer: str
    citations: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    follow_up_question: str
    retrieval_hits: int = Field(ge=0, default=0)
    evidence_notes: list[str] = Field(default_factory=list)


class RoutedResponse(BaseModel):
    intent: IntentLabel
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str
    answer: str
    citations: list[str]
    follow_up_question: str
    route_used: str
    conversation_id: str
    processing_ms: int = Field(ge=0)
    retrieval_hits: int = Field(ge=0)
    debug: dict = Field(default_factory=dict)
