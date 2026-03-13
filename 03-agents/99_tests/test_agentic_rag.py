"""
test_agentic_rag.py

Objetivo del script: 
Tests for 02_langchain/scripts/agentic_rag.py

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from conftest import load_module
from pydantic import ValidationError

mod = load_module("02_langchain/scripts/agentic_rag.py")
GradeDocument = mod.GradeDocument
HallucinationCheck = mod.HallucinationCheck


class TestAgenticRAGState:
    """Test RAG state structures."""

    def test_grade_document_model(self):
        grade = GradeDocument(es_relevante="si")
        assert grade.es_relevante == "si"

        grade_no = GradeDocument(es_relevante="no")
        assert grade_no.es_relevante == "no"

    def test_hallucination_check_model(self):
        check = HallucinationCheck(esta_fundamentada="si", score=4)
        assert check.esta_fundamentada == "si"
        assert check.score == 4

    def test_hallucination_check_score_bounds(self):
        import pytest

        with pytest.raises(ValidationError):
            HallucinationCheck(esta_fundamentada="si", score=0)

        with pytest.raises(ValidationError):
            HallucinationCheck(esta_fundamentada="si", score=6)
