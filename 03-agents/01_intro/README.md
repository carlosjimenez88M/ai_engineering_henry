# 01 — Fundamentos de Agentes

Antes de usar cualquier framework, necesitás entender qué es realmente un agente. Este bloque te lleva a construir uno desde cero con la API de OpenAI, sin abstracciones, para que puedas ver exactamente qué pasa en cada paso del loop.

La pregunta central de este bloque no es "¿cómo se usa un agente?" sino "¿cuándo tiene sentido usarlo?" — y esa respuesta cambia bastante cuando entendés los costos reales.

---

## Contenido

| Notebook | Tema | Qué construís |
|---|---|---|
| `01_que_es_un_agente.ipynb` | Anatomía de un agente | Loop ReAct con OpenAI API pura, tool calls, ciclo observación-razonamiento-acción |
| `02_workflows_vs_agentes.ipynb` | Workflows vs Agentes | Workflow determinista vs agente dinámico, taxonomía de patrones de Anthropic |
| `03_costo_latencia_alucinacion.ipynb` | Métricas críticas | Token economics, latencia medida, alucinación cuantificada, LLM-as-judge |
| `04_panorama_agentes_modernos.ipynb` | Panorama actual | Puente hacia LangChain, LangGraph, memoria, sistemas multi-agente y A2A |

---

## Script Disponible

`scripts/agent_anatomy.py` — Agente ReAct mínimo listo para importar como módulo. Podés usarlo como base para experimentos propios.

---

## Prerrequisitos

- `OPENAI_API_KEY` configurada en `.env`
- `make sync` ejecutado desde `03-agents/`
- Haber completado los módulos 01 y 02 (especialmente LangGraph del módulo 01)

---

## Por Qué Empezar Aquí

Es tentador ir directo a LangGraph. No lo hagas todavía. Los notebooks de este bloque muestran cosas que los frameworks ocultan: cómo se construye el contexto de mensajes, cómo el modelo decide cuándo usar una herramienta, por qué un agente puede entrar en loop infinito, y cuánto cuesta cada llamada al modelo.

Si llegás al bloque 02 sin entender esto, vas a usar LangChain sin saber qué está haciendo por vos.

---

## Criterio de Avance

Antes de pasar al bloque 02, deberías poder responder:

- ¿Qué diferencia hay entre un workflow y un agente?
- ¿Por qué un agente puede ser más caro que un workflow para la misma tarea?
- ¿Qué es el loop ReAct y cuándo termina?
- ¿Cuándo preferirías NO usar un agente?
