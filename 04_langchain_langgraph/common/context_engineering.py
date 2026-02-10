"""Context engineering utilities for LangGraph architecture demos."""

from __future__ import annotations

import hashlib
from typing import Any


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        normalized = item.strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(item.strip())
    return out


def build_context_packet(
    *,
    profile: dict[str, Any],
    architecture: str,
    module: str = "04_langchain_langgraph",
    max_gustos: int = 5,
) -> dict[str, Any]:
    """Create a compact and traceable context packet for LangGraph runs."""
    tipo_persona = str(profile.get("tipo_persona", "desconocida")).strip()
    estilo = str(profile.get("estilo", "calido y respetuoso")).strip()
    contexto = str(profile.get("contexto", "sin contexto adicional")).strip()
    gustos = _dedupe_keep_order([str(g).strip() for g in profile.get("gustos", [])])[:max_gustos]

    packet = {
        "module": module,
        "architecture": architecture,
        "profile": {
            "tipo_persona": tipo_persona,
            "gustos": gustos,
            "estilo": estilo,
            "contexto": contexto,
        },
        "constraints": {
            "respect": "No manipulacion, no presion, no lenguaje explicito.",
            "token_budget_hint": "Mantener contexto <= 300 tokens.",
            "must_reference_min_gustos": 2,
        },
        "design_notes": {
            "filters": [
                "dedupe_gustos",
                f"max_gustos={max_gustos}",
                "drop_empty_fields",
            ]
        },
    }

    digest = hashlib.sha256(str(packet).encode("utf-8")).hexdigest()[:12]
    packet["context_hash"] = digest
    return packet
