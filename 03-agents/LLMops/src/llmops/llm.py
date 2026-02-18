from __future__ import annotations

import time
from dataclasses import asdict
from typing import Any, Protocol

from openai import OpenAI

from llmops.models import LLMCallResult, UsageStats


class LLMGateway(Protocol):
    model: str

    def complete(self, *, system_prompt: str, user_prompt: str) -> LLMCallResult:
        """Call the underlying LLM and return normalized metadata."""


class OpenAILLMGateway:
    def __init__(self, model: str = "gpt-5-mini", api_key: str | None = None) -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key, max_retries=0, timeout=20.0)

    def complete(self, *, system_prompt: str, user_prompt: str) -> LLMCallResult:
        start = time.perf_counter()
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        latency_ms = (time.perf_counter() - start) * 1000

        content = getattr(response, "output_text", "") or _extract_content(response)
        usage = _extract_usage(getattr(response, "usage", None))

        return LLMCallResult(
            model=self.model,
            content=content,
            latency_ms=latency_ms,
            usage=usage,
        )


def _extract_content(response: Any) -> str:
    output = getattr(response, "output", None)
    if not output:
        return ""

    text_chunks: list[str] = []
    for item in output:
        content_items = getattr(item, "content", None) or []
        for content_item in content_items:
            text_value = getattr(content_item, "text", None)
            if text_value:
                text_chunks.append(str(text_value))
    return "\n".join(text_chunks).strip()


def _extract_usage(raw_usage: Any) -> UsageStats:
    if raw_usage is None:
        return UsageStats()

    if hasattr(raw_usage, "model_dump"):
        payload = raw_usage.model_dump()
    elif isinstance(raw_usage, dict):
        payload = raw_usage
    else:
        payload = asdict(raw_usage) if hasattr(raw_usage, "__dataclass_fields__") else {}

    input_tokens = payload.get("input_tokens") or payload.get("prompt_tokens")
    output_tokens = payload.get("output_tokens") or payload.get("completion_tokens")
    total_tokens = payload.get("total_tokens")

    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    return UsageStats(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )
