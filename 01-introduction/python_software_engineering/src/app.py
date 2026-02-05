from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Ticket:
    id: str
    customer_tier: str
    channel: str
    hours_open: int
    has_payment_blocker: bool
    message: str


def score_ticket(ticket: Ticket) -> int:
    """
    Regla deterministica:
    - prioridad por impacto de negocio (pago bloqueado, tier)
    - prioridad por riesgo operativo (tiempo abierto)
    - sin dependencia de modelos ni prompts
    """
    score = 0

    if ticket.has_payment_blocker:
        score += 50

    if ticket.customer_tier == "enterprise":
        score += 25
    elif ticket.customer_tier == "pro":
        score += 10

    if ticket.hours_open >= 24:
        score += 15
    elif ticket.hours_open >= 8:
        score += 8

    if ticket.channel == "chat":
        score += 2

    return score


def classify_priority(score: int) -> str:
    if score >= 60:
        return "P0"
    if score >= 35:
        return "P1"
    if score >= 15:
        return "P2"
    return "P3"


def plan_queue(tickets: Iterable[Ticket]) -> list[dict[str, str | int]]:
    ranked = []
    for ticket in tickets:
        score = score_ticket(ticket)
        ranked.append(
            {
                "id": ticket.id,
                "score": score,
                "priority": classify_priority(score),
            }
        )
    return sorted(ranked, key=lambda item: item["score"], reverse=True)


def load_tickets(path: Path) -> list[Ticket]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Ticket(**item) for item in raw]


def run() -> None:
    base = Path("01_class/python_software_engineering")
    source = base / "sample_tickets.json"
    tickets = load_tickets(source)
    queue = plan_queue(tickets)

    output = base / "queue_report.json"
    output.write_text(json.dumps(queue, indent=2), encoding="utf-8")
    print(f"Queue generada en {output}")


if __name__ == "__main__":
    run()
