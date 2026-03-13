"""
state.py

Objetivo del script: 
State definitions for the Cultural Intelligence LangGraph system.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from typing import Optional

from langgraph.graph import MessagesState

from cinematic_intelligence.models import (
    CulturalResponse,
    DavisAlbumAnalysis,
    DomainEnum,
    KingBookAnalysis,
    NolanFilmAnalysis,
)


class CulturalState(MessagesState):
    """
    Main state for the Cultural Intelligence graph.

    Extends MessagesState which provides:
    - messages: Annotated[list[AnyMessage], add_messages]

    TypedDict fields cannot have default values; nodes return partial dicts
    and LangGraph merges them into the state.
    """

    domain: Optional[DomainEnum]
    routing_confidence: float
    routing_reasoning: str
    domain_result: Optional[dict]
    final_response: Optional[CulturalResponse]


class NolanSpecialistState(MessagesState):
    """State for the Nolan specialist sub-agent."""

    query: str
    analysis: Optional[NolanFilmAnalysis]
    raw_data: list[dict]


class KingSpecialistState(MessagesState):
    """State for the King specialist sub-agent."""

    query: str
    analysis: Optional[KingBookAnalysis]
    raw_data: list[dict]


class DavisSpecialistState(MessagesState):
    """State for the Davis specialist sub-agent."""

    query: str
    analysis: Optional[DavisAlbumAnalysis]
    raw_data: list[dict]
