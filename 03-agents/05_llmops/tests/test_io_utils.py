from __future__ import annotations

from llmops.io_utils import parse_json_object


def test_parse_json_object_supports_code_fence() -> None:
    raw = """```json
{"route":"sales","priority":"P3","answer_es":"Te contacto ventas."}
```"""
    parsed = parse_json_object(raw)
    assert parsed["route"] == "sales"
