"""Unit tests for LangGraph state definitions."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage

from cinematic_intelligence.models import DomainEnum
from cinematic_intelligence.state import (
    CulturalState,
    DavisSpecialistState,
    KingSpecialistState,
    NolanSpecialistState,
)


class TestCulturalState:
    def test_messages_field_exists(self):
        """CulturalState inherits messages from MessagesState."""
        state = CulturalState(messages=[HumanMessage(content="Hello")])
        assert len(state["messages"]) == 1

    def test_optional_fields_absent_by_default(self):
        """Domain and result fields are not present until set by nodes."""
        state = CulturalState(messages=[])
        assert state.get("domain") is None
        assert state.get("domain_result") is None
        assert state.get("final_response") is None

    def test_domain_field_accepts_enum(self):
        state = CulturalState(messages=[], domain=DomainEnum.NOLAN)
        assert state["domain"] == DomainEnum.NOLAN

    def test_add_messages_accumulates(self):
        """The add_messages reducer should accumulate, not replace."""
        state = CulturalState(messages=[HumanMessage(content="First")])
        # Simulate what LangGraph does when a node returns new messages
        from langgraph.graph.message import add_messages
        updated: list = list(add_messages(state["messages"], [AIMessage(content="Response")]))
        assert len(updated) == 2
        assert updated[1].content == "Response"


class TestSpecialistStates:
    def test_nolan_state(self):
        state = NolanSpecialistState(messages=[], query="Tell me about Inception")
        assert state["query"] == "Tell me about Inception"
        assert state.get("analysis") is None

    def test_king_state(self):
        state = KingSpecialistState(messages=[], query="What is The Shining about?")
        assert state["query"] == "What is The Shining about?"

    def test_davis_state(self):
        state = DavisSpecialistState(messages=[], query="Describe Kind of Blue")
        assert state["query"] == "Describe Kind of Blue"
