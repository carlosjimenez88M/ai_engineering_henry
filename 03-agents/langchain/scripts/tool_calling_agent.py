"""
Agente con tool calling reutilizable.

Uso:
    from langchain.scripts.tool_calling_agent import ToolCallingAgent
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class ToolCallingAgent:
    """Agente generico con tool calling via LangGraph."""

    def __init__(
        self,
        tools: list[BaseTool],
        model: str = "gpt-5-mini",
        system_prompt: str = "Eres un asistente util. Responde en español.",
    ):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.tools = tools
        self.system_prompt = system_prompt
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.app = self._build_graph()

    def _build_graph(self):
        """Construye el grafo del agente."""

        def call_model(state: AgentState) -> dict:
            messages = [SystemMessage(content=self.system_prompt)] + state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}

        def should_continue(state: AgentState) -> str:
            last = state["messages"][-1]
            if hasattr(last, "tool_calls") and last.tool_calls:
                return "tools"
            return END

        graph = StateGraph(AgentState)
        graph.add_node("agent", call_model)
        graph.add_node("tools", ToolNode(self.tools))

        graph.add_edge(START, "agent")
        graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
        graph.add_edge("tools", "agent")

        return graph.compile()

    def invoke(self, query: str) -> str:
        """Ejecuta una query y retorna la respuesta."""
        result = self.app.invoke({"messages": [HumanMessage(content=query)]})
        last_msg = result["messages"][-1]
        return last_msg.content if hasattr(last_msg, "content") else str(last_msg)
