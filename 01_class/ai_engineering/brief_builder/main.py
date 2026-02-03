"""Main entry point for brief generation.

This script generates a comprehensive comparative brief on Software Engineering
vs AI Engineering using OpenAI's API. The output is structured markdown following
specific quality requirements.

Usage:
    python main.py
    python main.py --context "Fintech startup"
    python main.py --temperature 0.1 --output custom_path.md

Following principles from "AI Engineering" by Chip Huyen:
- Reproducibility: Model version, temperature, and prompts are tracked
- Modularity: Separated concerns (config, prompts, validation, metrics)
- Error handling: Specific exceptions and retry logic
- Observability: Metrics tracking for cost/latency
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime
from pathlib import Path
import sys

from openai import OpenAI

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from config import load_settings
from exceptions import APIError, ValidationError
from logger import get_logger
from metrics import BriefMetrics, calculate_cost, log_metrics, print_metrics_summary
from prompts import system_prompt, user_prompt
from retry import retry_with_backoff
from validator import (
    validate_brief_structure,
    validate_context_length,
    validate_markdown_format,
    validate_output_path,
    validate_temperature,
)


logger = get_logger()


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments.

    Returns:
        Namespace with parsed arguments:
            - output (Path): Output path for markdown file
            - context (str): Optional additional context
            - temperature (float): Model temperature (0.0-2.0)

    Examples:
        >>> import sys
        >>> sys.argv = ["main.py", "--temperature", "0.1"]
        >>> args = parse_args()
        >>> args.temperature
        0.1
    """
    parser = argparse.ArgumentParser(
        description="Genera un brief critico de Software Engineering vs AI Engineering."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("01_class/ai_engineering/briefs/software_vs_ai_engineering.md"),
        help="Ruta de salida para el markdown.",
    )
    parser.add_argument(
        "--context",
        type=str,
        default="",
        help="Contexto extra para adaptar el brief.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperatura del modelo (recomendado 0.1 a 0.3).",
    )
    args = parser.parse_args()

    # Validate temperature immediately
    try:
        validate_temperature(args.temperature)
    except ValueError as e:
        parser.error(str(e))

    return args


def generate_brief(context: str, temperature: float) -> tuple[str, BriefMetrics]:
    """Generates a brief using OpenAI API with validation and metrics.

    Makes a synchronous API call to OpenAI to generate the comparative brief.
    Uses system and user prompts to guide the model's output format and style.
    Includes input validation, retry logic, output validation, and metrics tracking.

    Args:
        context: Additional context to customize the brief (e.g., "B2B startup").
            Empty string means no additional context.
        temperature: Model temperature parameter (0.0-2.0). Lower values produce
            more deterministic outputs. Recommended range: 0.1-0.3.

    Returns:
        Tuple of (generated_brief, metrics):
            - generated_brief: Brief content as markdown string
            - metrics: BriefMetrics with usage stats and costs

    Raises:
        ValidationError: If inputs or outputs fail validation.
        APIError: If API call fails after all retry attempts.
        ConfigurationError: If OPENAI_API_KEY is not configured.

    Examples:
        >>> brief, metrics = generate_brief(context="", temperature=0.2)
        >>> "Software Engineering" in brief
        True
        >>> metrics.estimated_cost_usd > 0
        True
    """
    # Validate inputs
    validate_temperature(temperature)
    if context:
        validate_context_length(context)

    settings = load_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    logger.info("Solicitando brief al modelo: %s (temperature=%.2f)",
                settings.openai_model, temperature)

    # Start timer for latency measurement
    start_time = time.perf_counter()

    # Make API call with retry logic
    def api_call():
        return client.chat.completions.create(
            model=settings.openai_model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt()},
                {"role": "user", "content": user_prompt(extra_context=context or None)},
            ],
        )

    response = retry_with_backoff(api_call, max_attempts=3)
    latency = time.perf_counter() - start_time

    # Extract and validate content
    content = response.choices[0].message.content
    if not content:
        raise APIError("La respuesta del modelo llego vacia.")

    # Validate markdown format
    if not validate_markdown_format(content):
        logger.warning("El brief generado tiene formato markdown invalido")
        raise ValidationError("Brief tiene formato markdown invalido")

    # Validate brief structure
    structure_checks = validate_brief_structure(content)
    if not structure_checks["is_complete"]:
        missing = [k for k, v in structure_checks.items()
                   if k != "is_complete" and not v]
        logger.warning("Brief incompleto. Secciones faltantes: %s", missing)
        # Don't fail, just warn - the brief may still be usable

    # Calculate metrics
    usage = response.usage
    cost = calculate_cost(
        settings.openai_model,
        usage.prompt_tokens,
        usage.completion_tokens
    )

    metrics = BriefMetrics(
        model=settings.openai_model,
        temperature=temperature,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
        estimated_cost_usd=cost,
        latency_seconds=latency,
        timestamp=datetime.now().isoformat(),
        context=context if context else None,
    )

    logger.info(
        "Brief generado exitosamente: %d tokens, $%.6f USD, %.2fs",
        usage.total_tokens,
        cost,
        latency
    )

    return content, metrics


def save_output(markdown: str, output: Path, metrics: BriefMetrics | None = None) -> Path:
    """Saves generated brief to markdown file with optional metrics.

    Creates parent directories if they don't exist. Writes content with UTF-8
    encoding and ensures file ends with newline. If metrics provided, saves
    them to a .metrics.json file alongside the brief.

    Args:
        markdown: Brief content as markdown string.
        output: Path where to save the file.
        metrics: Optional BriefMetrics to save alongside the brief.

    Returns:
        Path where file was saved (same as output parameter).

    Raises:
        ValidationError: If output path is not writable.
        IOError: If unable to write file (permissions, disk space, etc.).

    Examples:
        >>> from pathlib import Path
        >>> path = save_output("# Test", Path("./test.md"))
        >>> path.exists()
        True
    """
    # Validate output path
    validate_output_path(output)

    # Save brief
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown.strip() + "\n", encoding="utf-8")

    # Save metrics if provided
    if metrics:
        metrics.output_path = str(output)
        log_metrics(metrics, output.parent)

    return output


def run() -> None:
    """Main execution function.

    Orchestrates the entire brief generation workflow:
    1. Parse command-line arguments (with validation)
    2. Generate brief via OpenAI API (with retry logic)
    3. Validate output quality
    4. Save output and metrics to files
    5. Print metrics summary
    6. Log completion

    This function is the entry point when running as a script.

    Raises:
        SystemExit: If argument parsing fails or uncaught exception occurs.
    """
    args = parse_args()

    try:
        # Generate brief with metrics
        brief, metrics = generate_brief(
            context=args.context,
            temperature=args.temperature
        )

        # Save brief and metrics
        output_path = save_output(
            markdown=brief,
            output=args.output,
            metrics=metrics
        )

        # Print metrics summary to console
        print_metrics_summary(metrics)

        logger.info("Brief generado en: %s", output_path)

    except ValidationError as e:
        logger.error("Error de validación: %s", e)
        sys.exit(1)
    except APIError as e:
        logger.error("Error de API: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.error("Error inesperado: %s", e)
        raise


if __name__ == "__main__":
    run()
