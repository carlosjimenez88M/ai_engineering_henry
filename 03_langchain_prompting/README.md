# Clase 03: LangChain Prompting Avanzado (CoT + ReAct + Context Engineering)

Esta clase toma la lógica de `02-prompting` y la evoluciona a un patrón de ingeniería más cercano a producción con **LangChain**.

## Qué vas a dominar en esta clase

1. Qué es LangChain y cuándo sí vale la pena usarlo (y cuándo no).
2. Cómo traducir la estructura de 5 capas (ROLE, TASK, OUTPUT, EXAMPLES, CONTEXT) a componentes de LangChain.
3. Cómo llevar **CoT** y **ReAct** desde prompts directos a pipelines trazables y validados.
4. Cómo diseñar **context engineering** para reducir alucinaciones, costo y deriva de comportamiento.
5. Cómo auditar y refinar respuestas con feedback loop medible.

---

## ¿Qué es LangChain ?

LangChain es una librería para construir sistemas LLM con piezas componibles: prompts, modelos, parsers, herramientas y memoria/contexto.

En vez de tener un string gigante con prompt + llamada API, LangChain te permite:

- Definir prompts estructurados (`ChatPromptTemplate`).
- Encadenar pasos (`prompt | model | parser`).
- Forzar formato de salida tipado (`with_structured_output`).
- Conectar herramientas (tools) para agentes ReAct.
- Inspeccionar trazas de ejecución para debugging.

### Regla pragmática

- Si tu problema se resuelve en 1 llamada simple y estable, `openai` directo suele bastar.
- Si necesitas orquestación multi-paso, tools, validación de output y reusabilidad, LangChain te da ventaja de ingeniería.

---

## Mapeo de Clase 02 -> Clase 03

| Capa de Prompting | Clase 02 (direct API) | Clase 03 (LangChain) |
|---|---|---|
| ROLE | `system_prompt` string | `ChatPromptTemplate.from_messages` |
| TASK | instrucciones dentro del user prompt | template parametrizable + subcadenas |
| OUTPUT FORMAT | `response_format={"type":"json_object"}` | `with_structured_output(PydanticModel)` |
| EXAMPLES | few-shot en texto | `FewShotChatMessagePromptTemplate` |
| CONTEXT | dict serializado manualmente | `context packet` diseñado y validado |

---

## Context Engineering (la capa que más impacta calidad)

No es "poner más contexto". Es diseñar **contexto útil, mínimo y trazable**.

### Patrón recomendado

1. **Context contract**: define campos obligatorios del contexto.
2. **Filtrado**: elimina ruido que no cambia la decisión.
3. **Priorización**: ordena señales por impacto en la tarea.
4. **Budget de tokens**: impón límites para evitar latencia/costo descontrolado.
5. **Traceabilidad**: conserva `context_hash` para reproducibilidad.

### Errores comunes

- Contexto narrativo largo sin estructura.
- Mezclar hechos, inferencias y suposiciones sin etiquetado.
- No versionar el contexto ni su esquema.
- Usar ReAct con tools pobres y esperar milagros.

---

## Estructura del módulo

- `03_langchain_prompting/COT_LangChain/Notebooks/cot_langchain_aplicado.ipynb`
  - Evoluciona los ejemplos CoT de `02-prompting/COT` a LangChain.
  - Incluye zero-shot, few-shot y feedback loop con rúbrica.

- `03_langchain_prompting/ReAct_LangChain/Notebooks/react_langchain_aplicado.ipynb`
  - Evoluciona los ejemplos ReAct de `02-prompting/ReAct` a LangChain.
  - Incluye tools, loop ReAct, guardrails y context engineering explícito.

- `03_langchain_prompting/common/context_engineering.py`
  - Utilidades para construir `context packets` limpios y trazables.

- `03_langchain_prompting/tools/execute_notebooks.py`
  - Ejecuta notebooks y guarda artefactos `.executed.ipynb`.

---

## Ejecución

1. Instala dependencias:

```bash
uv sync
```

2. Ejecuta notebooks de la clase:

```bash
uv run python 03_langchain_prompting/tools/execute_notebooks.py
```

