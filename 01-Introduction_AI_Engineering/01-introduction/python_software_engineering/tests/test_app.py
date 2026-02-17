from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import Ticket, classify_priority, plan_queue, score_ticket


def test_score_ticket_payment_blocker_enterprise_is_critical() -> None:
    ticket = Ticket(
        id="1",
        customer_tier="enterprise",
        channel="email",
        hours_open=2,
        has_payment_blocker=True,
        message="x",
    )
    assert score_ticket(ticket) == 75
    assert classify_priority(75) == "P0"


def test_queue_is_sorted_by_score_desc() -> None:
    tickets = [
        Ticket("a", "free", "email", 1, False, "a"),
        Ticket("b", "pro", "chat", 10, False, "b"),
    ]
    queue = plan_queue(tickets)
    assert queue[0]["id"] == "b"
    assert queue[1]["id"] == "a"
