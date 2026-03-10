from __future__ import annotations

import json
from pathlib import Path

from llmops.models import LLMCallResult, TicketExample, UsageStats
from llmops.monitoring import JsonlMonitor
from llmops.pipeline import TicketTriagePipeline


class FakeGateway:
    def __init__(self, content: str) -> None:
        self.model = "gpt-5-mini"
        self._content = content

    def complete(self, *, system_prompt: str, user_prompt: str) -> LLMCallResult:  # noqa: ARG002
        return LLMCallResult(
            model=self.model,
            content=self._content,
            latency_ms=123.0,
            usage=UsageStats(input_tokens=100, output_tokens=50, total_tokens=150),
        )


def test_pipeline_parses_valid_json_and_logs_event(tmp_path: Path) -> None:
    monitor = JsonlMonitor(tmp_path / "monitoring_events.jsonl")
    gateway = FakeGateway(
        '{"route":"billing","priority":"P1","answer_es":"Revertimos el cobro y abrimos caso."}'
    )
    pipeline = TicketTriagePipeline(gateway=gateway, monitor=monitor)
    ticket = TicketExample(
        id="T-001",
        customer_message="Me cobraron doble.",
        expected_route="billing",
        expected_priority="P1",
    )

    prediction = pipeline.predict(ticket)

    assert prediction.route == "billing"
    assert prediction.priority == "P1"
    assert prediction.usage.total_tokens == 150

    lines = (tmp_path / "monitoring_events.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["ticket_id"] == "T-001"
    assert event["status"] == "ok"
    assert event["total_tokens"] == 150


def test_pipeline_uses_fallback_when_output_is_not_json(tmp_path: Path) -> None:
    monitor = JsonlMonitor(tmp_path / "monitoring_events.jsonl")
    gateway = FakeGateway("not-json-output")
    pipeline = TicketTriagePipeline(gateway=gateway, monitor=monitor)
    ticket = TicketExample(
        id="T-099",
        customer_message="La app no funciona.",
        expected_route="technical",
        expected_priority="P2",
    )

    prediction = pipeline.predict(ticket)

    assert prediction.route == "technical"
    assert prediction.priority == "P2"
    assert prediction.error is not None

    lines = (tmp_path / "monitoring_events.jsonl").read_text(encoding="utf-8").strip().splitlines()
    event = json.loads(lines[0])
    assert event["status"] == "fallback"
