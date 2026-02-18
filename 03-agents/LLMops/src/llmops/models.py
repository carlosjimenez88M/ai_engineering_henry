from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class UsageStats:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    def to_dict(self) -> dict[str, int | None]:
        return asdict(self)


@dataclass
class LLMCallResult:
    model: str
    content: str
    latency_ms: float
    usage: UsageStats


@dataclass
class TicketExample:
    id: str
    customer_message: str
    expected_route: str
    expected_priority: str

    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "TicketExample":
        return cls(
            id=row["id"],
            customer_message=row["customer_message"],
            expected_route=row["expected_route"],
            expected_priority=row["expected_priority"],
        )


@dataclass
class Prediction:
    ticket_id: str
    route: str
    priority: str
    answer_es: str
    model: str
    latency_ms: float
    usage: UsageStats
    raw_output: str
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["usage"] = self.usage.to_dict()
        return data


@dataclass
class MonitorEvent:
    timestamp_utc: str
    ticket_id: str
    model: str
    status: str
    latency_ms: float
    route: str | None = None
    priority: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class JudgeResult:
    score: int
    rationale: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class TicketEvaluation:
    ticket_id: str
    route_expected: str
    route_predicted: str
    priority_expected: str
    priority_predicted: str
    route_correct: bool
    priority_correct: bool
    judge_score: int | None = None
    judge_rationale: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class EvaluationSummary:
    total_tickets: int
    route_accuracy: float
    priority_accuracy: float
    avg_judge_score: float | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class EvaluationReport:
    generated_at_utc: str
    model: str
    summary: EvaluationSummary
    per_ticket: list[TicketEvaluation]

    def to_dict(self) -> dict[str, object]:
        return {
            "generated_at_utc": self.generated_at_utc,
            "model": self.model,
            "summary": self.summary.to_dict(),
            "per_ticket": [row.to_dict() for row in self.per_ticket],
        }
