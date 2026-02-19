"""Utilities for the Batman vector DB and agentic orchestration module."""

from .common import chunk_comic_records, load_comic_records
from .evaluation import (
    build_eval_questions,
    groundedness_score,
    plot_architecture_difference,
    plot_pipeline_comparison,
    run_benchmark,
)
from .rag_pipelines import AgenticRAG, HeroRouterOrchestrator, VanillaRAG
from .vector_store_lab import ComicsVectorDB

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
