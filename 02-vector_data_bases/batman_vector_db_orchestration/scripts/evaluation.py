"""Evaluation and plotting helpers for RAG vs Agentic RAG."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from .common import tokenize
from .rag_pipelines import AgenticRAG, RAGResult, VanillaRAG


def groundedness_score(answer: str, contexts: Iterable[str]) -> float:
    """Token-overlap groundedness proxy in [0, 1]."""
    answer_tokens = set(tokenize(answer))
    if not answer_tokens:
        return 0.0

    context_tokens: set[str] = set()
    for context in contexts:
        context_tokens.update(tokenize(context))

    overlap = len(answer_tokens & context_tokens)
    return round(overlap / max(len(answer_tokens), 1), 4)


def build_eval_questions() -> list[str]:
    """Queries designed to stress retrieval quality and orchestration behavior."""
    return [
        "Explica como evoluciona Batman desde Year One hasta The Dark Knight Returns.",
        "Cual es la tesis filosofica central de The Killing Joke y como la refuta Gordon?",
        "Compara la estrategia de Bane en Knightfall con el enfoque de Hush.",
        "Que revela Court of Owls sobre puntos ciegos de Batman como detective?",
        "Por que Batman es clave en la Liga de la Justicia aun sin superpoderes?",
        "Resume el rol de los Robins y el aprendizaje de Bruce como mentor.",
        "Que principios morales definen a Batman y que trade-offs implican?",
        "Explica como Gotham influye en el diseno tactico de Batman.",
    ]


def _result_to_row(result: RAGResult) -> dict[str, object]:
    contexts = [str(doc.get("text", "")) for doc in result.docs]
    grounding_proxy = groundedness_score(answer=result.answer, contexts=contexts)
    return {
        "pipeline": result.pipeline,
        "query": result.query,
        "latency_seconds": result.latency_seconds,
        "retrieved_docs": len(result.docs),
        "route": result.route,
        "groundedness_proxy": grounding_proxy,
        "groundedness_internal": result.groundedness,
        "llm_provider": result.llm_provider,
        "retrieval_provider": result.retrieval_provider,
        "steps": " -> ".join(result.steps),
    }


def run_benchmark(
    vanilla: VanillaRAG,
    agentic: AgenticRAG,
    queries: list[str] | None = None,
) -> pd.DataFrame:
    """Execute both pipelines on the same query set and return tidy dataframe."""
    workload = queries or build_eval_questions()
    rows: list[dict[str, object]] = []

    for query in workload:
        vanilla_result = vanilla.run(query)
        agentic_result = agentic.run(query)
        rows.append(_result_to_row(vanilla_result))
        rows.append(_result_to_row(agentic_result))

    return pd.DataFrame(rows)


def plot_pipeline_comparison(df: pd.DataFrame, output_path: Path | str) -> pd.DataFrame:
    """Create bar chart summary for RAG vs Agentic RAG."""
    summary = (
        df.groupby("pipeline", as_index=False)
        .agg(
            latency_seconds=("latency_seconds", "mean"),
            groundedness_proxy=("groundedness_proxy", "mean"),
            retrieved_docs=("retrieved_docs", "mean"),
        )
        .round(4)
    )

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    metrics = ["latency_seconds", "groundedness_proxy", "retrieved_docs"]
    titles = ["Latencia promedio", "Groundedness promedio", "Docs recuperados promedio"]
    colors = {"vanilla_rag": "#1f77b4", "agentic_rag": "#ff7f0e"}

    for ax, metric, title in zip(axes, metrics, titles, strict=True):
        x = summary["pipeline"].tolist()
        y = summary[metric].tolist()
        bars = ax.bar(x, y, color=[colors.get(item, "#888888") for item in x])
        ax.set_title(title)
        ax.set_xlabel("Pipeline")
        ax.set_ylabel(metric)
        ax.grid(axis="y", alpha=0.3)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    fig.suptitle("Comparativa: Vanilla RAG vs Agentic RAG", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.94))

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return summary


def plot_architecture_difference(output_path: Path | str) -> None:
    """Draw a simple architecture diagram for both pipelines."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    vanilla_steps = ["User Query", "Retrieve", "Prompt + Context", "Generate"]
    agentic_steps = ["User Query", "Route", "Rewrite", "Retrieve", "Filter", "Generate", "Grounding Check"]

    for ax, title, steps in [
        (axes[0], "Vanilla RAG", vanilla_steps),
        (axes[1], "Agentic RAG", agentic_steps),
    ]:
        ax.set_title(title)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        y_positions = [0.9 - idx * (0.78 / max(len(steps) - 1, 1)) for idx in range(len(steps))]
        for idx, (step, y) in enumerate(zip(steps, y_positions, strict=True)):
            ax.text(
                0.5,
                y,
                step,
                ha="center",
                va="center",
                fontsize=10,
                bbox={"boxstyle": "round,pad=0.3", "facecolor": "#f2f2f2", "edgecolor": "#333333"},
            )
            if idx < len(steps) - 1:
                ax.annotate(
                    "",
                    xy=(0.5, y_positions[idx + 1] + 0.05),
                    xytext=(0.5, y - 0.05),
                    arrowprops={"arrowstyle": "->", "lw": 1.3, "color": "#555555"},
                )

    fig.suptitle("Flujo operacional: RAG vs Agentic RAG", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
