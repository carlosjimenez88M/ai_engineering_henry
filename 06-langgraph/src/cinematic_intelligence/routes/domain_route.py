"""Conditional edge function for cultural domain routing."""

from __future__ import annotations

from typing import Literal

from cinematic_intelligence.models import DomainEnum
from cinematic_intelligence.state import CulturalState


def cultural_route(
    state: CulturalState,
) -> Literal["nolan_specialist", "king_specialist", "davis_specialist", "general_fallback"]:
    """
    Pure function that reads state["domain"] and returns the next node name.

    Used as the condition function in add_conditional_edges().
    """
    domain = state.get("domain")

    if domain == DomainEnum.NOLAN:
        return "nolan_specialist"
    elif domain == DomainEnum.KING:
        return "king_specialist"
    elif domain == DomainEnum.DAVIS:
        return "davis_specialist"
    else:
        return "general_fallback"
