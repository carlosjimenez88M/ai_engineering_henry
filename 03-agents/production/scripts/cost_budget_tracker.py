"""
Tracker de presupuesto reutilizable.

Uso:
    from production.scripts.cost_budget_tracker import CostBudgetTracker
"""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class UsageEntry:
    """Registro de uso de una llamada."""
    timestamp: float
    label: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: float


class CostBudgetTracker:
    """Tracker de costos con presupuesto y alertas."""

    PRICING = {
        "gpt-5-mini": {"input": 0.15, "output": 0.60},
        "gpt-5": {"input": 2.00, "output": 8.00},
    }

    def __init__(
        self,
        model: str = "gpt-5-mini",
        budget_usd: float = 1.00,
        alert_threshold: float = 0.8,
    ):
        self.model = model
        self.budget_usd = budget_usd
        self.alert_threshold = alert_threshold
        self.entries: list[UsageEntry] = []
        self._alerted = False

    @property
    def total_cost(self) -> float:
        return sum(e.cost_usd for e in self.entries)

    @property
    def total_tokens(self) -> int:
        return sum(e.total_tokens for e in self.entries)

    @property
    def remaining_budget(self) -> float:
        return max(0, self.budget_usd - self.total_cost)

    def record(
        self,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float = 0.0,
        label: str = "",
    ) -> UsageEntry:
        """Registra uso y verifica presupuesto."""
        prices = self.PRICING.get(self.model, self.PRICING["gpt-5-mini"])
        cost = (
            input_tokens * prices["input"] / 1_000_000
            + output_tokens * prices["output"] / 1_000_000
        )

        entry = UsageEntry(
            timestamp=time.time(),
            label=label,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost_usd=cost,
            latency_ms=latency_ms,
        )
        self.entries.append(entry)

        # Alert check
        usage_pct = self.total_cost / self.budget_usd
        if usage_pct >= self.alert_threshold and not self._alerted:
            self._alerted = True

        return entry

    def can_proceed(self, estimated_tokens: int = 500) -> bool:
        """Verifica si hay presupuesto para una llamada estimada."""
        prices = self.PRICING.get(self.model, self.PRICING["gpt-5-mini"])
        estimated_cost = estimated_tokens * (prices["input"] + prices["output"]) / 2 / 1_000_000
        return self.total_cost + estimated_cost <= self.budget_usd

    def summary(self) -> dict:
        return {
            "total_calls": len(self.entries),
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost, 6),
            "budget_usd": self.budget_usd,
            "remaining_usd": round(self.remaining_budget, 6),
            "usage_pct": round(self.total_cost / self.budget_usd * 100, 1),
        }
