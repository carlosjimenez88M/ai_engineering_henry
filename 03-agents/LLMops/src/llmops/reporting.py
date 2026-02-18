from __future__ import annotations

from llmops.models import EvaluationReport


def render_markdown_report(report: EvaluationReport) -> str:
    summary = report.summary
    lines = [
        "# Evaluation Report",
        "",
        f"- Generated at: {report.generated_at_utc}",
        f"- Model: {report.model}",
        f"- Total tickets: {summary.total_tickets}",
        f"- Route accuracy: {summary.route_accuracy:.2%}",
        f"- Priority accuracy: {summary.priority_accuracy:.2%}",
        (
            f"- Avg judge score: {summary.avg_judge_score:.2f}/5"
            if summary.avg_judge_score is not None
            else "- Avg judge score: N/A"
        ),
        "",
        "## Per ticket",
        "",
    ]

    for row in report.per_ticket:
        lines.extend(
            [
                f"### {row.ticket_id}",
                f"- Route: expected `{row.route_expected}` vs predicted `{row.route_predicted}`",
                (
                    f"- Priority: expected `{row.priority_expected}` "
                    f"vs predicted `{row.priority_predicted}`"
                ),
                f"- Route correct: `{row.route_correct}`",
                f"- Priority correct: `{row.priority_correct}`",
                (
                    f"- Judge score: `{row.judge_score}` | Rationale: {row.judge_rationale}"
                    if row.judge_score is not None
                    else "- Judge score: N/A"
                ),
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"
