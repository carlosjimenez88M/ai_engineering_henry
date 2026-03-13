"""
test_models.py

Objetivo del script: 
Unit tests for Pydantic models in cinematic_intelligence.models.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from cinematic_intelligence.models import (
    CulturalResponse,
    DavisAlbumAnalysis,
    DomainEnum,
    DomainRoute,
    KingBookAnalysis,
    NolanFilmAnalysis,
)


class TestDomainEnum:
    def test_valid_values(self):
        assert DomainEnum.NOLAN == "nolan"
        assert DomainEnum.KING == "king"
        assert DomainEnum.DAVIS == "davis"
        assert DomainEnum.GENERAL == "general"

    def test_from_string(self):
        assert DomainEnum("nolan") == DomainEnum.NOLAN
        assert DomainEnum("king") == DomainEnum.KING

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            DomainEnum("invalid_domain")


class TestDomainRoute:
    def test_required_fields(self):
        route = DomainRoute(domain=DomainEnum.NOLAN)
        assert route.domain == DomainEnum.NOLAN
        assert route.confidence == 1.0
        assert route.reasoning == ""

    def test_confidence_bounds(self):
        route = DomainRoute(domain=DomainEnum.KING, confidence=0.85)
        assert route.confidence == 0.85

    def test_confidence_out_of_range(self):
        with pytest.raises(ValidationError):
            DomainRoute(domain=DomainEnum.NOLAN, confidence=1.5)

    def test_with_all_fields(self):
        route = DomainRoute(
            domain=DomainEnum.DAVIS,
            confidence=0.95,
            reasoning="User asked about Kind of Blue",
        )
        assert route.domain == DomainEnum.DAVIS
        assert route.reasoning == "User asked about Kind of Blue"


class TestNolanFilmAnalysis:
    def test_required_fields(self):
        analysis = NolanFilmAnalysis(
            film_title="Inception",
            analysis="A film about dreams within dreams.",
        )
        assert analysis.film_title == "Inception"
        assert analysis.year is None
        assert analysis.main_themes == []
        assert analysis.connections == []

    def test_full_model(self):
        analysis = NolanFilmAnalysis(
            film_title="Memento",
            year=2000,
            main_themes=["memoria", "identidad"],
            narrative_technique="narración inversa",
            analysis="Un thriller sobre la memoria fragmentada.",
            connections=["Inception", "The Prestige"],
        )
        assert analysis.year == 2000
        assert len(analysis.main_themes) == 2


class TestKingBookAnalysis:
    def test_defaults(self):
        analysis = KingBookAnalysis(
            book_title="It",
            analysis="A horror novel about a clown.",
        )
        assert analysis.horror_elements == []
        assert analysis.psychological_themes == []
        assert analysis.setting == ""

    def test_serialization(self):
        analysis = KingBookAnalysis(
            book_title="The Shining",
            year=1977,
            horror_elements=["hotel fantasma", "posesión"],
            analysis="Un hotel que enloquece a su guardian.",
        )
        data = analysis.model_dump()
        assert data["book_title"] == "The Shining"
        assert "horror_elements" in data


class TestDavisAlbumAnalysis:
    def test_defaults(self):
        analysis = DavisAlbumAnalysis(
            album_title="Kind of Blue",
            analysis="The most influential jazz album.",
        )
        assert analysis.era == []
        assert analysis.techniques == []
        assert analysis.historical_significance == ""

    def test_with_era(self):
        analysis = DavisAlbumAnalysis(
            album_title="Bitches Brew",
            year=1970,
            era=["jazz-rock", "fusion"],
            analysis="Defined jazz fusion.",
        )
        assert len(analysis.era) == 2


class TestCulturalResponse:
    def test_required_fields(self):
        resp = CulturalResponse(
            domain=DomainEnum.NOLAN,
            query="Tell me about Inception",
            final_answer="Inception is a 2010 film...",
        )
        assert resp.domain == DomainEnum.NOLAN
        assert resp.sources_consulted == []
        assert resp.confidence == 1.0

    def test_serialization_roundtrip(self):
        resp = CulturalResponse(
            domain=DomainEnum.DAVIS,
            query="Kind of Blue?",
            final_answer="It is the best jazz album.",
            sources_consulted=["Kind of Blue (1959)"],
            confidence=0.9,
        )
        data = resp.model_dump()
        restored = CulturalResponse(**data)
        assert restored.final_answer == resp.final_answer
