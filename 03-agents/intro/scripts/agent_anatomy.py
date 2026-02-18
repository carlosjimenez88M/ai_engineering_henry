"""
Agente ReAct minimo reutilizable.

Uso:
    from intro.scripts.agent_anatomy import react_agent, CostTracker

    resultado = react_agent("Cuanto es 2+2?", tools_schema, tools_registry)
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from openai import OpenAI


@dataclass
class AgentStep:
    """Registro de un paso del agente."""

    step: int
    tipo: str  # "tool_call" | "respuesta_final"
    contenido: str
    herramienta: str | None = None
    argumentos: dict | None = None
    resultado: str | None = None


@dataclass
class AgentMetrics:
    """Metricas acumuladas de una ejecucion."""

    total_steps: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    latencia_ms: float = 0.0
    costo_usd: float = 0.0


@dataclass
class AgentResult:
    """Resultado completo de una ejecucion del agente."""

    pregunta: str
    respuesta: str
    pasos: list[AgentStep] = field(default_factory=list)
    metricas: AgentMetrics = field(default_factory=AgentMetrics)


class CostTracker:
    """Rastrea costos acumulados de llamadas a OpenAI."""

    PRICING = {
        "gpt-5-mini": {"input": 0.15, "output": 0.60},
        "gpt-5": {"input": 2.00, "output": 8.00},
    }

    def __init__(self, model: str = "gpt-5-mini"):
        self.model = model
        self.calls: list[dict] = []

    def track(self, usage, latency_ms: float, label: str = "") -> dict:
        prices = self.PRICING.get(self.model, self.PRICING["gpt-5-mini"])
        costo_input = usage.prompt_tokens * prices["input"] / 1_000_000
        costo_output = usage.completion_tokens * prices["output"] / 1_000_000
        entry = {
            "label": label,
            "input_tokens": usage.prompt_tokens,
            "output_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "costo_total": costo_input + costo_output,
            "latencia_ms": latency_ms,
        }
        self.calls.append(entry)
        return entry

    @property
    def total_costo(self) -> float:
        return sum(c["costo_total"] for c in self.calls)

    @property
    def total_tokens(self) -> int:
        return sum(c["total_tokens"] for c in self.calls)


def react_agent(
    pregunta: str,
    tools_schema: list[dict],
    tools_registry: dict,
    client: OpenAI | None = None,
    model: str = "gpt-5-mini",
    max_steps: int = 5,
    system_prompt: str = "Eres un asistente util. Usa herramientas cuando sea necesario. Responde en español.",
) -> AgentResult:
    """
    Agente ReAct minimo con OpenAI API.

    Args:
        pregunta: Pregunta del usuario.
        tools_schema: Schemas de herramientas para OpenAI.
        tools_registry: Mapa nombre -> funcion callable.
        client: Cliente OpenAI (crea uno si no se provee).
        model: Modelo a usar.
        max_steps: Maximo de pasos.
        system_prompt: Prompt del sistema.

    Returns:
        AgentResult con respuesta, pasos y metricas.
    """
    if client is None:
        client = OpenAI()

    messages: list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": pregunta},
    ]

    pasos: list[AgentStep] = []
    total_input = 0
    total_output = 0
    t_start = time.time()

    for step in range(max_steps):
        kwargs: dict = {"model": model, "messages": messages}
        if tools_schema:
            kwargs["tools"] = tools_schema
            kwargs["tool_choice"] = "auto"
        response = client.chat.completions.create(**kwargs)  # type: ignore[arg-type]
        msg = response.choices[0].message
        usage = response.usage
        total_input += usage.prompt_tokens if usage else 0
        total_output += usage.completion_tokens if usage else 0

        if not msg.tool_calls:
            pasos.append(AgentStep(
                step=step + 1, tipo="respuesta_final", contenido=msg.content or "",
            ))
            break

        messages.append(msg)  # type: ignore[arg-type]
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)

            if fn_name in tools_registry:
                resultado = tools_registry[fn_name](**fn_args)
            else:
                resultado = f"Error: herramienta '{fn_name}' no encontrada"

            pasos.append(AgentStep(
                step=step + 1,
                tipo="tool_call",
                contenido="",
                herramienta=fn_name,
                argumentos=fn_args,
                resultado=resultado,
            ))

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": str(resultado),
            })

    latencia_ms = (time.time() - t_start) * 1000
    costo = total_input * 0.15 / 1_000_000 + total_output * 0.60 / 1_000_000

    return AgentResult(
        pregunta=pregunta,
        respuesta=pasos[-1].contenido if pasos else "Sin respuesta",
        pasos=pasos,
        metricas=AgentMetrics(
            total_steps=len(pasos),
            input_tokens=total_input,
            output_tokens=total_output,
            latencia_ms=round(latencia_ms, 1),
            costo_usd=round(costo, 6),
        ),
    )
