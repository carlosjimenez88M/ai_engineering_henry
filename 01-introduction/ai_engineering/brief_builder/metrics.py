"""Metrics tracking and cost calculation for brief generation.

This module provides observability into LLM system performance following
principles from "AI Engineering" by Chip Huyen (Chapter 7: Monitoring and Observability).

Key metrics tracked:
- Token usage (prompt, completion, total)
- Cost estimation based on model pricing
- Latency (end-to-end time)
- Model configuration (model name, temperature)

This data is essential for:
- Budget management
- Performance optimization
- Debugging production issues
- Understanding usage patterns
"""

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

# OpenAI pricing as of January 2025 (USD per 1M tokens)
# Source: https://openai.com/api/pricing/
MODEL_PRICING = {
    "gpt-4o": {
        "prompt": 2.50,
        "completion": 10.00,
    },
    "gpt-4o-mini": {
        "prompt": 0.150,
        "completion": 0.600,
    },
    "gpt-4": {
        "prompt": 30.00,
        "completion": 60.00,
    },
    "gpt-3.5-turbo": {
        "prompt": 0.50,
        "completion": 1.50,
    },
}


@dataclass
class BriefMetrics:
    """Metrics captured during brief generation.

    Attributes:
        model: OpenAI model name (e.g., "gpt-4o-mini").
        temperature: Temperature parameter used.
        prompt_tokens: Number of tokens in the prompt.
        completion_tokens: Number of tokens in the completion.
        total_tokens: Total tokens (prompt + completion).
        estimated_cost_usd: Estimated cost in USD based on model pricing.
        latency_seconds: Time taken to generate the brief (seconds).
        timestamp: ISO 8601 timestamp of generation.
        context: Optional context string provided by user.
        output_path: Path where brief was saved.
    """

    model: str
    temperature: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    latency_seconds: float
    timestamp: str
    context: str | None = None
    output_path: str | None = None


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculates estimated cost based on OpenAI pricing.

    Args:
        model: OpenAI model name (e.g., "gpt-4o-mini").
        prompt_tokens: Number of tokens in the prompt.
        completion_tokens: Number of tokens in the completion.

    Returns:
        Estimated cost in USD. Returns 0.0 if model pricing is unknown.

    Examples:
        >>> cost = calculate_cost("gpt-4o-mini", 1000, 500)
        >>> cost
        0.00045
        >>> # (1000 * 0.150 + 500 * 0.600) / 1_000_000
    """
    if model not in MODEL_PRICING:
        logger.warning(
            f"Unknown model '{model}', cannot estimate cost. "
            f"Known models: {list(MODEL_PRICING.keys())}"
        )
        return 0.0

    pricing = MODEL_PRICING[model]
    prompt_cost = (prompt_tokens * pricing["prompt"]) / 1_000_000
    completion_cost = (completion_tokens * pricing["completion"]) / 1_000_000
    total_cost = prompt_cost + completion_cost

    logger.debug(
        f"Cost calculation for {model}: "
        f"prompt={prompt_tokens} tokens (${prompt_cost:.6f}), "
        f"completion={completion_tokens} tokens (${completion_cost:.6f}), "
        f"total=${total_cost:.6f}"
    )

    return total_cost


def log_metrics(metrics: BriefMetrics, output_dir: Path) -> None:
    """Saves metrics to JSON file alongside the generated brief.

    Creates a .metrics.json file with the same base name as the brief.
    This allows easy correlation between briefs and their generation metrics.

    Args:
        metrics: The BriefMetrics object to save.
        output_dir: Directory where the brief was saved.

    Raises:
        IOError: If unable to write metrics file.

    Examples:
        >>> metrics = BriefMetrics(
        ...     model="gpt-4o-mini",
        ...     temperature=0.2,
        ...     prompt_tokens=1000,
        ...     completion_tokens=500,
        ...     total_tokens=1500,
        ...     estimated_cost_usd=0.00045,
        ...     latency_seconds=3.5,
        ...     timestamp="2025-01-15T10:30:00Z",
        ... )
        >>> log_metrics(metrics, Path("./output"))
        # Creates ./output/brief.metrics.json
    """
    metrics_path = output_dir / "brief.metrics.json"

    try:
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2, ensure_ascii=False)

        logger.info(f"Metrics saved to {metrics_path}")

    except IOError as e:
        logger.error(f"Failed to save metrics to {metrics_path}: {e}")
        raise


def print_metrics_summary(metrics: BriefMetrics) -> None:
    """Prints a human-readable summary of metrics to console.

    Args:
        metrics: The BriefMetrics object to summarize.

    Examples:
        >>> metrics = BriefMetrics(...)
        >>> print_metrics_summary(metrics)
        # Outputs formatted summary to console
    """
    print("\n" + "=" * 60)
    print(" BRIEF GENERATION METRICS")
    print("=" * 60)
    print(f"Model:              {metrics.model}")
    print(f"Temperature:        {metrics.temperature}")
    print(f"Prompt tokens:      {metrics.prompt_tokens:,}")
    print(f"Completion tokens:  {metrics.completion_tokens:,}")
    print(f"Total tokens:       {metrics.total_tokens:,}")
    print(f"Estimated cost:     ${metrics.estimated_cost_usd:.6f} USD")
    print(f"Latency:            {metrics.latency_seconds:.2f}s")
    print(f"Timestamp:          {metrics.timestamp}")
    if metrics.context:
        print(f"Context:            {metrics.context}")
    if metrics.output_path:
        print(f"Output:             {metrics.output_path}")
    print("=" * 60 + "\n")
