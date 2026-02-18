from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from llmops.evaluation import ResponseJudge, run_evaluation
from llmops.io_utils import load_jsonl, write_json, write_jsonl
from llmops.llm import OpenAILLMGateway
from llmops.models import Prediction, TicketExample
from llmops.monitoring import JsonlMonitor
from llmops.pipeline import TicketTriagePipeline
from llmops.reporting import render_markdown_report

app = typer.Typer(help="LLMops pipeline runner for Module 3.")
console = Console()


@app.command()
def run(
    dataset: Annotated[
        Path,
        typer.Option(help="Path to JSONL evaluation dataset."),
    ] = Path("LLMops/data/tickets_eval.jsonl"),
    output_dir: Annotated[
        Path,
        typer.Option(help="Directory where predictions and reports are stored."),
    ] = Path("LLMops/outputs"),
    model: Annotated[
        str,
        typer.Option(envvar="OPENAI_MODEL", help="OpenAI model name."),
    ] = "gpt-5-mini",
    judge: Annotated[
        bool,
        typer.Option("--judge/--no-judge", help="Enable LLM-as-judge scoring."),
    ] = True,
) -> None:
    load_dotenv()

    if not dataset.exists():
        raise typer.BadParameter(f"Dataset does not exist: {dataset}")

    output_dir.mkdir(parents=True, exist_ok=True)

    gateway = OpenAILLMGateway(model=model)
    monitor = JsonlMonitor(output_dir / "monitoring_events.jsonl")
    pipeline = TicketTriagePipeline(gateway=gateway, monitor=monitor)

    rows = load_jsonl(dataset)
    tickets = [TicketExample.from_dict(row) for row in rows]

    predictions: list[Prediction] = []
    for ticket in tickets:
        predictions.append(pipeline.predict(ticket))

    predictions_rows = [prediction.to_dict() for prediction in predictions]
    write_jsonl(output_dir / "predictions.jsonl", predictions_rows)

    judge_component = ResponseJudge(gateway) if judge else None
    report = run_evaluation(
        dataset=tickets,
        predictions=predictions,
        model=model,
        judge=judge_component,
    )

    write_json(output_dir / "evaluation_report.json", report.to_dict())
    (output_dir / "evaluation_report.md").write_text(
        render_markdown_report(report),
        encoding="utf-8",
    )

    _print_summary(report_path=output_dir / "evaluation_report.json", report=report)


def _print_summary(*, report_path: Path, report) -> None:
    summary = report.summary
    table = Table(title="LLMops Summary")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Model", report.model)
    table.add_row("Tickets", str(summary.total_tickets))
    table.add_row("Route accuracy", f"{summary.route_accuracy:.2%}")
    table.add_row("Priority accuracy", f"{summary.priority_accuracy:.2%}")
    table.add_row(
        "Avg judge score",
        f"{summary.avg_judge_score:.2f}/5" if summary.avg_judge_score is not None else "N/A",
    )
    table.add_row("Report", str(report_path))
    console.print(table)


if __name__ == "__main__":
    app()
