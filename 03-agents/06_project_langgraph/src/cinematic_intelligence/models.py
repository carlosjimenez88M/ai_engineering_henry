"""
models.py

Objetivo del script: 
Pydantic models for the Cultural Intelligence system.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DomainEnum(str, Enum):
    """Supported cultural domains."""

    NOLAN = "nolan"
    KING = "king"
    DAVIS = "davis"
    GENERAL = "general"


class DomainRoute(BaseModel):
    """Structured output for domain routing decisions."""

    domain: DomainEnum = Field(
        description="The cultural domain most relevant to the user's query"
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score for the routing decision (0-1)",
    )
    reasoning: str = Field(
        default="",
        description="Brief explanation for the routing decision",
    )


class NolanFilmAnalysis(BaseModel):
    """Structured analysis of a Christopher Nolan film."""

    film_title: str = Field(description="Title of the analyzed film")
    year: Optional[int] = Field(default=None, description="Year of release")
    main_themes: list[str] = Field(
        default_factory=list,
        description="Primary thematic elements of the film",
    )
    narrative_technique: str = Field(
        default="",
        description="Key narrative or cinematographic technique used",
    )
    analysis: str = Field(
        description="Detailed analysis response to the user's query"
    )
    connections: list[str] = Field(
        default_factory=list,
        description="Thematic connections to other Nolan films",
    )


class KingBookAnalysis(BaseModel):
    """Structured analysis of a Stephen King book."""

    book_title: str = Field(description="Title of the analyzed book")
    year: Optional[int] = Field(default=None, description="Year of publication")
    horror_elements: list[str] = Field(
        default_factory=list,
        description="Horror and supernatural elements present",
    )
    psychological_themes: list[str] = Field(
        default_factory=list,
        description="Psychological and social themes explored",
    )
    analysis: str = Field(
        description="Detailed analysis response to the user's query"
    )
    setting: str = Field(default="", description="Primary setting/location")


class DavisAlbumAnalysis(BaseModel):
    """Structured analysis of a Miles Davis album."""

    album_title: str = Field(description="Title of the analyzed album")
    year: Optional[int] = Field(default=None, description="Year of release")
    era: list[str] = Field(
        default_factory=list,
        description="Jazz era/period classification",
    )
    techniques: list[str] = Field(
        default_factory=list,
        description="Musical techniques and innovations",
    )
    analysis: str = Field(
        description="Detailed analysis response to the user's query"
    )
    historical_significance: str = Field(
        default="",
        description="Historical importance in jazz history",
    )


class CulturalResponse(BaseModel):
    """Final synthesized response from the Cultural Intelligence system."""

    domain: DomainEnum = Field(description="The cultural domain that handled this query")
    query: str = Field(description="The original user query")
    final_answer: str = Field(description="The synthesized response to the user")
    sources_consulted: list[str] = Field(
        default_factory=list,
        description="Data sources or works referenced in the response",
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Overall confidence in the response",
    )
