# Practice: LangChain Prompting

Esta carpeta convierte las estrategias de prompting del modulo anterior en componentes mantenibles con LangChain. Los 5 retos suben en complejidad: empiezas con templates y salida tipada, luego pasas a contexto reusable, CoT validado, agentes ReAct y finalmente un router hibrido que decide que estrategia conviene segun el caso.

## Objetivo

- aprender a encapsular prompts en componentes reutilizables
- tipar salidas para volverlas validables
- separar contexto reusable de contexto puntual
- elegir entre cadena, agente o sistema hibrido segun el problema
- entrenar patrones que aparecen tanto en produccion como en ejercicios de entrevista

## Orden recomendado

| Reto | Estrategia principal | Industria | Lo que entrenas |
|---|---|---|---|
| 1 | ChatPromptTemplate + Pydantic | RRHH | Templates repetibles y salidas tipadas |
| 2 | Context engineering reusable | Turismo | Paquetes de contexto consistentes |
| 3 | CoT + validator chain | Seguros | Analisis estructurado con autocritica |
| 4 | ReAct con tools | Media | Verificacion y evidencia con agentes |
| 5 | Router hibrido | Procurement | Elegir dinamicamente la mejor estrategia |

## Como trabajar los retos

1. Reutiliza ideas de `intro/01-langchain.py`, `common/context_engineering.py`, `blog_agent.py` y `fact_checker_agent.py`.
2. Define modelos Pydantic antes de escribir prompts largos.
3. Mide parse rate, exactitud y costo por ruta.
4. Registra decisiones de arquitectura: por que fue cadena, por que fue agente, por que fue router.
5. Conserva trazabilidad entre input, decisiones intermedias y respuesta final.

## Validacion transversal

- Cada salida final debe parsear contra un esquema estable.
- Los prompts deben ser reutilizables, no hardcodeados para un solo ejemplo.
- El contexto debe estar limpio, deduplicado y con presupuesto de tokens razonable.
- Las herramientas deben aportar informacion real al resultado final.
- Debe existir un fallback para baja confianza o falta de evidencia.

## Afinado con fuentes externas

Estos retos se ajustaron usando documentacion oficial y casos reales de OpenAI, Anthropic, LangChain y LangSmith. El objetivo fue que practiques patrones que hoy si aparecen en sistemas reales:

- `response_format` y salidas tipadas
- templates reutilizables en vez de prompts sueltos
- herramientas bien definidas y faciles de testear
- evaluacion offline por componentes, no solo demos manuales
- decision explicita sobre cuando usar cadena, agente o router hibrido

Revisa el detalle en `EXTERNAL_REFERENCES.md`.
