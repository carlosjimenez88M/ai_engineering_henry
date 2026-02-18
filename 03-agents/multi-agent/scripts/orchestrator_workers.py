"""
Orquestador-Workers reutilizable.

Uso:
    from multi_agent.scripts.orchestrator_workers import Orchestrator
"""

from __future__ import annotations

from dataclasses import dataclass, field

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field


class SubtaskPlan(BaseModel):
    """Subtarea generada por el orquestador."""
    description: str = Field(description="Lo que debe investigar el worker")
    worker: str = Field(description="Tipo de worker asignado")


class OrchestrationPlan(BaseModel):
    """Plan de descomposicion."""
    subtasks: list[SubtaskPlan]
    strategy: str = Field(description="Estrategia de descomposicion")


@dataclass
class WorkerResult:
    """Resultado de un worker."""
    worker_type: str
    subtask: str
    result: str
    tokens_used: int = 0


@dataclass
class OrchestratorResult:
    """Resultado completo del orquestador."""
    query: str
    plan: OrchestrationPlan
    worker_results: list[WorkerResult] = field(default_factory=list)
    final_answer: str = ""


class Orchestrator:
    """Patron orquestador-workers generico."""

    def __init__(
        self,
        llm: ChatOpenAI | None = None,
        worker_types: list[str] | None = None,
    ):
        self.llm = llm or ChatOpenAI(model="gpt-5-mini", temperature=0)
        self.worker_types = worker_types or ["general"]
        self._planner = self.llm.with_structured_output(OrchestrationPlan)

    def plan(self, query: str) -> OrchestrationPlan:
        """Descompone la query en subtareas."""
        workers_desc = ", ".join(self.worker_types)
        return self._planner.invoke(  # type: ignore[return-value]
            f"Descompone esta tarea en subtareas para workers de tipo: {workers_desc}\n\n{query}"
        )

    def execute_worker(self, subtask: str, worker_type: str, context: str = "") -> WorkerResult:
        """Ejecuta un worker individual."""
        prompt = f"Eres un worker especializado en {worker_type}."
        if context:
            prompt += f"\n\nContexto:\n{context}"

        response = self.llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=subtask),
        ])

        return WorkerResult(
            worker_type=worker_type,
            subtask=subtask,
            result=str(response.content),
        )

    def synthesize(self, query: str, results: list[WorkerResult]) -> str:
        """Sintetiza resultados de workers."""
        results_text = "\n\n".join([
            f"Worker ({r.worker_type}): {r.result}" for r in results
        ])

        response = self.llm.invoke([
            SystemMessage(content="Sintetiza los resultados en una respuesta coherente."),
            HumanMessage(content=f"Pregunta: {query}\n\nResultados:\n{results_text}"),
        ])

        return str(response.content)

    def run(self, query: str, context_fn=None) -> OrchestratorResult:
        """Ejecuta el flujo completo."""
        plan = self.plan(query)

        results = []
        for subtask in plan.subtasks:
            context = context_fn(subtask.worker, subtask.description) if context_fn else ""
            result = self.execute_worker(subtask.description, subtask.worker, context)
            results.append(result)

        answer = self.synthesize(query, results)

        return OrchestratorResult(
            query=query,
            plan=plan,
            worker_results=results,
            final_answer=answer,
        )
