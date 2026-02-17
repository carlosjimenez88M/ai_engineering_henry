"""Context engineering helpers for LangChain prompting notebooks."""

from __future__ import annotations

import hashlib
from typing import Any


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item.strip())
    return result


def build_context_packet(
    *,
    profile: dict[str, Any],
    module: str,
    strategy: str,
    max_gustos: int = 4,
) -> dict[str, Any]:
    """Builds a compact, reproducible context packet for prompting.

    Args:
        profile: Raw profile dictionary.
        module: Course module label (for traceability).
        strategy: Prompt strategy label (e.g. "cot_zero_shot", "react").
        max_gustos: Max number of preferences included.

    Returns:
        A cleaned and traceable context packet.
    """
    tipo_persona = str(profile.get("tipo_persona", "desconocida")).strip()
    estilo = str(profile.get("estilo", "cálido y respetuoso")).strip()
    contexto = str(profile.get("contexto", "sin contexto adicional")).strip()

    gustos_raw = [str(g).strip() for g in profile.get("gustos", []) if str(g).strip()]
    gustos = _dedupe_keep_order(gustos_raw)[:max_gustos]

    packet = {
        "module": module,
        "strategy": strategy,
        "profile": {
            "tipo_persona": tipo_persona,
            "gustos": gustos,
            "estilo": estilo,
            "contexto": contexto,
        },
        "design_notes": {
            "applied_filters": [
                "dedupe_gustos",
                f"max_gustos={max_gustos}",
                "drop_empty_fields",
            ],
            "token_budget_hint": "Mantener el contexto <= 250 tokens.",
        },
    }

    digest = hashlib.sha256(str(packet).encode("utf-8")).hexdigest()[:12]
    packet["context_hash"] = digest
    return packet
