"""
__init__.py

Objetivo del script: 
Utilities for the Batman vector DB and agentic orchestration module.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from scripts.common import chunk_comic_records, load_comic_records
from scripts.evaluation import (
    build_eval_questions,
    groundedness_score,
    plot_architecture_difference,
    plot_pipeline_comparison,
    run_benchmark,
)
from scripts.rag_pipelines import AgenticRAG, HeroRouterOrchestrator, VanillaRAG
from scripts.vector_store_lab import ComicsVectorDB

__all__ = [
    "AgenticRAG",
    "ComicsVectorDB",
    "HeroRouterOrchestrator",
    "VanillaRAG",
    "build_eval_questions",
    "chunk_comic_records",
    "groundedness_score",
    "load_comic_records",
    "plot_architecture_difference",
    "plot_pipeline_comparison",
    "run_benchmark",
]
