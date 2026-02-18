# Evaluation Report

- Generated at: 2026-02-18T15:54:57.966830+00:00
- Model: gpt-5-mini
- Total tickets: 8
- Route accuracy: 87.50%
- Priority accuracy: 87.50%
- Avg judge score: 4.88/5

## Per ticket

### T-001
- Route: expected `billing` vs predicted `billing`
- Priority: expected `P1` vs predicted `P1`
- Route correct: `True`
- Priority correct: `True`
- Judge score: `5` | Rationale: Respuesta clara y profesional: ofrece disculpa, ticket y acciones concretas (qué enviar y siguientes pasos), pide información útil y establece un plazo razonable; no contiene promesas irreales. Podría mejorarse indicando el canal seguro para enviar el recibo.

### T-002
- Route: expected `account` vs predicted `account`
- Priority: expected `P1` vs predicted `P1`
- Route correct: `True`
- Priority correct: `True`
- Judge score: `4` | Rationale: Clara, útil y con pasos concretos y tono profesional; sin embargo incluye una promesa de resolución en "menos de 4 horas" (potencial promesa falsa) y solicita datos sensibles sin indicar un canal seguro.

### T-003
- Route: expected `technical` vs predicted `billing`
- Priority: expected `P1` vs predicted `P1`
- Route correct: `False`
- Priority correct: `True`
- Judge score: `5` | Rationale: Respuesta clara y profesional; solicita información precisa y reproducible, ofrece acciones concretas para mitigar y diagnosticar, y escaló el incidente. La promesa de actualización en 1 hora es razonable y no induce expectativas irreales.

### T-004
- Route: expected `sales` vs predicted `sales`
- Priority: expected `P3` vs predicted `P3`
- Route correct: `True`
- Priority correct: `True`
- Judge score: `5` | Rationale: Respuesta clara y profesional: confirma SSO y contrato anual, detalla protocolos soportados y servicios incluidos, pide información concreta para preparar propuesta y ofrece pasos siguientes; no contiene promesas infundadas.

### T-005
- Route: expected `billing` vs predicted `billing`
- Priority: expected `P2` vs predicted `P2`
- Route correct: `True`
- Priority correct: `True`
- Judge score: `5` | Rationale: Respuesta clara y profesional: proporciona pasos concretos para actualizar la tarjeta, advierte sobre seguridad y ofrece asistencia si hay problemas; no contiene promesas falsas.

### T-006
- Route: expected `technical` vs predicted `technical`
- Priority: expected `P2` vs predicted `P1`
- Route correct: `True`
- Priority correct: `False`
- Judge score: `5` | Rationale: Respuesta clara y profesional: solicita la información necesaria, ofrece pasos concretos de diagnóstico y soluciones temporales, y comunica escalado sin hacer promesas irreales.

### T-007
- Route: expected `account` vs predicted `account`
- Priority: expected `P1` vs predicted `P1`
- Route correct: `True`
- Priority correct: `True`
- Judge score: `5` | Rationale: Clara y útil: solicita información concreta para verificar identidad, ofrece alternativa de canal seguro, da acciones inmediatas y tono profesional. No contiene promesas problemáticas.

### T-008
- Route: expected `sales` vs predicted `sales`
- Priority: expected `P3` vs predicted `P3`
- Route correct: `True`
- Priority correct: `True`
- Judge score: `5` | Rationale: Respuesta clara y profesional: solicita la información necesaria, propone pasos concretos (demo, presupuesto, trial/PoC), pide disponibilidad para agendar y no incluye promesas falsas.
