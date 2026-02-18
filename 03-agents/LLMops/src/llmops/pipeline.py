from __future__ import annotations

from datetime import datetime, timezone

from llmops.io_utils import parse_json_object
from llmops.llm import LLMGateway
from llmops.models import LLMCallResult, MonitorEvent, Prediction, TicketExample, UsageStats
from llmops.monitoring import JsonlMonitor

VALID_ROUTES = {"billing", "technical", "account", "sales"}
VALID_PRIORITIES = {"P1", "P2", "P3"}


class TicketTriagePipeline:
    def __init__(self, gateway: LLMGateway, monitor: JsonlMonitor) -> None:
        self.gateway = gateway
        self.monitor = monitor

    def predict(self, ticket: TicketExample) -> Prediction:
        system_prompt = (
            "Eres un agente de soporte. Clasifica el ticket y redacta una respuesta en espanol.\n"
            "Devuelve SOLO JSON valido con estas claves exactas:\n"
            '{ "route": "billing|technical|account|sales", "priority": "P1|P2|P3", '
            '"answer_es": "texto" }.\n'
            "Reglas de prioridad: P1 es bloqueo severo/seguridad/cobro critico; "
            "P2 es problema importante no catastrófico; "
            "P3 es consulta comercial o solicitud no urgente."
        )
        user_prompt = f"Ticket ID: {ticket.id}\nMensaje del cliente:\n{ticket.customer_message}"

        try:
            llm_result = self.gateway.complete(system_prompt=system_prompt, user_prompt=user_prompt)
            parsed = parse_json_object(llm_result.content)
            prediction = self._prediction_from_llm(ticket, llm_result, parsed)
            status = "ok"
            error = None
        except Exception as exc:  # noqa: BLE001
            error = str(exc)
            llm_result = LLMCallResult(
                model=self.gateway.model,
                content="",
                latency_ms=0.0,
                usage=UsageStats(),
            )
            prediction = Prediction(
                ticket_id=ticket.id,
                route="technical",
                priority="P2",
                answer_es=(
                    "Estamos revisando tu caso. "
                    "Lo escalamos a soporte tecnico para analisis inmediato."
                ),
                model=self.gateway.model,
                latency_ms=0.0,
                usage=UsageStats(),
                raw_output="",
                error=error,
            )
            status = "fallback"

        self.monitor.log(
            MonitorEvent(
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
                ticket_id=ticket.id,
                model=prediction.model,
                status=status,
                latency_ms=prediction.latency_ms,
                route=prediction.route,
                priority=prediction.priority,
                input_tokens=prediction.usage.input_tokens,
                output_tokens=prediction.usage.output_tokens,
                total_tokens=prediction.usage.total_tokens,
                error=error,
            )
        )
        return prediction

    @staticmethod
    def _prediction_from_llm(
        ticket: TicketExample,
        llm_result: LLMCallResult,
        parsed: dict[str, object],
    ) -> Prediction:
        route = _normalize_route(str(parsed.get("route", "technical")))
        priority = _normalize_priority(str(parsed.get("priority", "P2")))
        answer_es = str(parsed.get("answer_es", "")).strip()
        if not answer_es:
            answer_es = "Gracias por reportarlo. Estamos procesando tu solicitud."

        return Prediction(
            ticket_id=ticket.id,
            route=route,
            priority=priority,
            answer_es=answer_es,
            model=llm_result.model,
            latency_ms=llm_result.latency_ms,
            usage=llm_result.usage,
            raw_output=llm_result.content,
        )


def _normalize_route(value: str) -> str:
    cleaned = value.strip().lower()
    mapping = {
        "tech": "technical",
        "tecnico": "technical",
        "soporte": "technical",
        "cuenta": "account",
        "facturacion": "billing",
        "ventas": "sales",
    }
    cleaned = mapping.get(cleaned, cleaned)
    if cleaned in VALID_ROUTES:
        return cleaned
    return "technical"


def _normalize_priority(value: str) -> str:
    cleaned = value.strip().upper()
    mapping = {
        "HIGH": "P1",
        "MEDIUM": "P2",
        "LOW": "P3",
        "URGENT": "P1",
    }
    cleaned = mapping.get(cleaned, cleaned)
    if cleaned in VALID_PRIORITIES:
        return cleaned
    return "P2"
