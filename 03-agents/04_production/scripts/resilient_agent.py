"""
Agente con resiliencia completa: retry, circuit breaker, fallback, budget.

Uso:
    from production.scripts.resilient_agent import ResilientAgent
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class CallResult:
    """Resultado de una llamada resiliente."""
    status: str  # "ok", "fallback", "budget_exceeded", "circuit_open", "error"
    content: str
    model: str = ""
    tokens: int = 0
    latency_ms: float = 0.0
    retries: int = 0


class CircuitBreaker:
    """Circuit breaker para APIs."""

    def __init__(self, max_failures: int = 3, cooldown_seconds: float = 30.0):
        self.max_failures = max_failures
        self.cooldown_seconds = cooldown_seconds
        self.failure_count = 0
        self.state = "closed"
        self.last_failure_time = 0.0

    def can_proceed(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if time.time() - self.last_failure_time >= self.cooldown_seconds:
                self.state = "half-open"
                return True
            return False
        return True  # half-open

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = "closed"

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.max_failures:
            self.state = "open"


class TokenBudget:
    """Control de presupuesto."""

    PRICING = {"gpt-5-mini": {"input": 0.15, "output": 0.60}}

    def __init__(self, model: str = "gpt-5-mini", max_tokens: int = 50000, max_cost: float = 0.10):
        self.model = model
        self.max_tokens = max_tokens
        self.max_cost = max_cost
        self.used_tokens = 0
        self.used_cost = 0.0

    def can_proceed(self) -> bool:
        return self.used_tokens < self.max_tokens and self.used_cost < self.max_cost

    def record(self, input_tokens: int, output_tokens: int) -> None:
        prices = self.PRICING.get(self.model, self.PRICING["gpt-5-mini"])
        cost = input_tokens * prices["input"] / 1_000_000 + output_tokens * prices["output"] / 1_000_000
        self.used_tokens += input_tokens + output_tokens
        self.used_cost += cost


class ResilientAgent:
    """Agente con resiliencia completa."""

    def __init__(
        self,
        model: str = "gpt-5-mini",
        max_retries: int = 3,
        max_failures: int = 3,
        cooldown: float = 30.0,
        max_tokens: int = 50000,
        max_cost: float = 0.10,
    ):
        self.client = OpenAI()
        self.model = model
        self.max_retries = max_retries
        self.circuit = CircuitBreaker(max_failures, cooldown)
        self.budget = TokenBudget(model, max_tokens, max_cost)

    def call(self, prompt: str, system: str = "Responde en español.") -> CallResult:
        """Llamada resiliente con todas las protecciones."""
        # Budget check
        if not self.budget.can_proceed():
            return CallResult(status="budget_exceeded", content="Presupuesto agotado.")

        # Circuit breaker check
        if not self.circuit.can_proceed():
            return CallResult(status="circuit_open", content="Servicio temporalmente no disponible.")

        # Retry loop
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                t0 = time.time()
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=500,
                    timeout=15,
                )
                latency = (time.time() - t0) * 1000

                usage = response.usage
                if usage:
                    self.budget.record(usage.prompt_tokens, usage.completion_tokens)
                self.circuit.record_success()

                return CallResult(
                    status="ok",
                    content=response.choices[0].message.content or "",
                    model=self.model,
                    tokens=usage.total_tokens if usage else 0,
                    latency_ms=round(latency, 1),
                    retries=attempt,
                )
            except Exception as e:
                last_error = e
                self.circuit.record_failure()
                if attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 10))

        return CallResult(
            status="error",
            content=f"Error tras {self.max_retries} reintentos: {last_error}",
            retries=self.max_retries,
        )
