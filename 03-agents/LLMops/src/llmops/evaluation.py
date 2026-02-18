from __future__ import annotations

from datetime import datetime, timezone

from llmops.io_utils import parse_json_object
from llmops.llm import LLMGateway
from llmops.models import (
    EvaluationReport,
    EvaluationSummary,
    JudgeResult,
    Prediction,
    TicketEvaluation,
    TicketExample,
)


class ResponseJudge:
    def __init__(self, gateway: LLMGateway) -> None:
        self.gateway = gateway

    def score(self, ticket: TicketExample, prediction: Prediction) -> JudgeResult:
        system_prompt = (
            "Eres un evaluador de calidad de soporte. Puntua la respuesta de 1 a 5.\n"
            "Devuelve SOLO JSON valido: {\"score\": <int 1-5>, \"rationale\": \"texto breve\" }."
        )
        user_prompt = (
            f"Ticket:\n{ticket.customer_message}\n\n"
            f"Respuesta del agente:\n{prediction.answer_es}\n\n"
            "Criterios: utilidad, accion concreta, tono profesional, ausencia de promesas falsas."
        )
        result = self.gateway.complete(system_prompt=system_prompt, user_prompt=user_prompt)
        payload = parse_json_object(result.content)
        raw_score = int(payload.get("score", 1))
        score = max(1, min(5, raw_score))
        rationale = str(payload.get("rationale", "")).strip() or "Sin justificacion."
        return JudgeResult(score=score, rationale=rationale)


def run_evaluation(
    *,
    dataset: list[TicketExample],
    predictions: list[Prediction],
    model: str,
    judge: ResponseJudge | None,
) -> EvaluationReport:
    dataset_by_id = {ticket.id: ticket for ticket in dataset}

    rows: list[TicketEvaluation] = []
    judge_scores: list[int] = []

    for prediction in predictions:
        ticket = dataset_by_id[prediction.ticket_id]
        route_correct = prediction.route == ticket.expected_route
        priority_correct = prediction.priority == ticket.expected_priority

        judge_score = None
        judge_rationale = None
        if judge is not None:
            try:
                judge_result = judge.score(ticket=ticket, prediction=prediction)
                judge_score = judge_result.score
                judge_rationale = judge_result.rationale
                judge_scores.append(judge_score)
            except Exception as exc:  # noqa: BLE001
                judge_score = None
                judge_rationale = f"judge_error: {exc}"

        rows.append(
            TicketEvaluation(
                ticket_id=ticket.id,
                route_expected=ticket.expected_route,
                route_predicted=prediction.route,
                priority_expected=ticket.expected_priority,
                priority_predicted=prediction.priority,
                route_correct=route_correct,
                priority_correct=priority_correct,
                judge_score=judge_score,
                judge_rationale=judge_rationale,
            )
        )

    total = len(rows)
    route_hits = sum(1 for row in rows if row.route_correct)
    priority_hits = sum(1 for row in rows if row.priority_correct)

    summary = EvaluationSummary(
        total_tickets=total,
        route_accuracy=(route_hits / total if total else 0.0),
        priority_accuracy=(priority_hits / total if total else 0.0),
        avg_judge_score=(sum(judge_scores) / len(judge_scores) if judge_scores else None),
    )

    return EvaluationReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        model=model,
        summary=summary,
        per_ticket=rows,
    )
