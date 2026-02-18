"""
Sistema de debate multi-agente.

Uso:
    from multi_agent.scripts.multi_agent_debate import DebateSystem
"""

from __future__ import annotations

from dataclasses import dataclass, field

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field


class DebateArgument(BaseModel):
    """Argumento en un debate."""
    position: str = Field(description="Posicion defendida")
    argument: str = Field(description="Argumento principal")
    counter: str = Field(description="Contra-argumento al oponente")
    changed_mind: bool = Field(description="Si cambio de opinion")


class JudgeVerdict(BaseModel):
    """Veredicto del juez."""
    winner: str
    score_a: int = Field(ge=1, le=10)
    score_b: int = Field(ge=1, le=10)
    reasoning: str


@dataclass
class DebateRound:
    """Registro de una ronda de debate."""
    round_num: int
    agent: str
    position: str
    argument: str
    changed: bool


@dataclass
class DebateResult:
    """Resultado de un debate."""
    question: str
    strategy: str
    winner: str
    rounds: list[DebateRound] = field(default_factory=list)
    converged: bool = False


class DebateSystem:
    """Sistema de debate multi-agente."""

    def __init__(self, llm: ChatOpenAI | None = None):
        self.llm = llm or ChatOpenAI(model="gpt-5-mini", temperature=0.7)
        self.judge_llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

    def debate(
        self,
        question: str,
        position_a: str,
        position_b: str,
        max_rounds: int = 3,
    ) -> DebateResult:
        """Ejecuta un debate entre dos posiciones."""
        debate_llm = self.llm.with_structured_output(DebateArgument)
        rounds = []

        agents = {
            f"defensor_{position_a}": position_a,
            f"defensor_{position_b}": position_b,
        }

        for ronda in range(max_rounds):
            positions = []
            for agent_name, initial_pos in agents.items():
                history = "\n".join([
                    f"R{r.round_num} {r.agent}: {r.argument[:100]}"
                    for r in rounds
                ]) or "Sin historial."

                arg = debate_llm.invoke(
                    f"Defiendes a {initial_pos}.\nPregunta: {question}\n\nHistorial:\n{history}"
                )

                rounds.append(DebateRound(
                    round_num=ronda + 1,
                    agent=agent_name,
                    position=arg.position,  # type: ignore[union-attr]
                    argument=arg.argument,  # type: ignore[union-attr]
                    changed=arg.changed_mind,  # type: ignore[union-attr]
                ))
                positions.append(arg.position)  # type: ignore[union-attr]

            if len(set(positions)) == 1:
                return DebateResult(
                    question=question, strategy="debate",
                    winner=positions[0], rounds=rounds, converged=True,
                )

        return DebateResult(
            question=question, strategy="debate",
            winner="Sin consenso", rounds=rounds, converged=False,
        )

    def judge(self, question: str, position_a: str, position_b: str) -> DebateResult:
        """Resuelve usando un juez."""
        arg_a = self.llm.invoke([
            SystemMessage(content=f"Argumenta a favor de {position_a}."),
            HumanMessage(content=question),
        ])
        arg_b = self.llm.invoke([
            SystemMessage(content=f"Argumenta a favor de {position_b}."),
            HumanMessage(content=question),
        ])

        judge_llm = self.judge_llm.with_structured_output(JudgeVerdict)
        verdict = judge_llm.invoke(
            f"Pregunta: {question}\n\n"
            f"A favor de {position_a}:\n{arg_a.content}\n\n"
            f"A favor de {position_b}:\n{arg_b.content}\n\n"
            f"Evalua imparcialmente."
        )

        return DebateResult(
            question=question, strategy="juez",
            winner=verdict.winner, converged=True,  # type: ignore[union-attr]
        )
