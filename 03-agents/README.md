# Modulo 3: Agentes

Este modulo organiza el contenido de agentes de menor a mayor complejidad: primero fundamentos, luego frameworks, despues coordinacion multi-agente y finalmente hardening y LLMops.

## Estructura por tema

| Orden | Bloque | Ruta |
|---|---|---|
| 01 | Fundamentos | `01_intro/` |
| 02 | Agentes con LangChain/LangGraph | `02_langchain/` |
| 03 | Coordinacion multi-agente | `03_multi_agent/` |
| 04 | Produccion | `04_production/` |
| 05 | LLMops aplicado | `05_llmops/` |

## Recorrido recomendado

1. `01_intro/` para entender que es un agente y cuando no usarlo.
2. `01_intro/04_panorama_agentes_modernos.ipynb` como notebook puente antes de entrar a frameworks.
3. `02_langchain/` para tool calling, routing, validacion y RAG agentico.
4. `03_multi_agent/` para orquestacion y handoffs.
5. `04_production/` para resiliencia, guardrails y control de costos.
6. `05_llmops/` para ver un pipeline completo con evaluacion y monitoreo.

## Datos y soporte

- `00_data/`: corpus de Batman y Spider-Man para notebooks y scripts.
- `99_tests/`: tests unitarios del modulo de agentes.
- `05_llmops/00_data/`: dataset del caso de triage de tickets.
- `05_llmops/outputs/`: artefactos generados al correr el pipeline.

## Comandos utiles

```bash
cd 03-agents
uv sync --extra dev
make test
make doctor
make run-llmops
make notebooks-intro
make notebooks-langchain
make notebooks-multi
make notebooks-prod
```

## Modelos por defecto

- `gpt-5-mini` en el caso `05_llmops/`
- OpenAI API key requerida para ejemplos que llaman al modelo real

## Instalacion del modulo

- `pyproject.toml` en la raiz del modulo permite instalar todo `03-agents/` con `uv sync --extra dev`.
- `05_llmops/` sigue expuesto como paquete instalable dentro del modulo.

## Readmes por bloque

- [01_intro/README.md](./01_intro/README.md)
- [02_langchain/README.md](./02_langchain/README.md)
- [03_multi_agent/README.md](./03_multi_agent/README.md)
- [04_production/README.md](./04_production/README.md)
- [05_llmops/README.md](./05_llmops/README.md)
