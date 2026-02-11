# Pydantic para AI/ML Engineering

## Por que este tema es clave

En proyectos AI/ML, muchos bugs no vienen del modelo; vienen de datos invalidos entrando al sistema.
`pydantic` permite validar estructuras antes de inferencia, entrenamiento o serving.

## Cuando usar pydantic

Usalo cuando necesites:

- Validar payloads de API de inferencia.
- Normalizar datos de features.
- Definir contratos de entrada y salida entre componentes.
- Fallar temprano con errores explicitos.

No lo uses cuando:

- Solo guardas dos valores triviales y no hay riesgo de datos mal formados.
- El costo de validacion por item te rompe un hot path ultra-optimizado.

## Modelo base

```python
from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    prompt: str = Field(min_length=5, max_length=2000)
    max_tokens: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
```

Si llega `max_tokens="muchos"` o `temperature=3.5`, `pydantic` falla con un error estructurado.

## Validaciones personalizadas

```python
from pydantic import BaseModel, Field, field_validator


class FeatureRow(BaseModel):
    age: int = Field(ge=0, le=120)
    monthly_income_usd: float = Field(ge=0)

    @field_validator("monthly_income_usd")
    @classmethod
    def reject_unrealistic_income(cls, value: float) -> float:
        if value > 1_000_000:
            raise ValueError("monthly_income_usd parece fuera de rango realista")
        return value
```

## Contratos de salida para modelos

```python
from typing import Literal
from pydantic import BaseModel, Field


class FraudPrediction(BaseModel):
    label: Literal["fraud", "not_fraud"]
    score: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=10)
```

Con esto, si tu pipeline devuelve score fuera de [0, 1], fallas en el punto correcto.

## Patrón recomendado en AI apps

1. Parsear input externo a `pydantic model`.
2. Si falla, devolver error claro de validacion.
3. Si pasa, convertir a formato interno para inferencia.
4. Validar salida del modelo con otro `pydantic model`.

## Errores comunes

1. Usar `dict` sin contrato para datos de inferencia.
2. Validar solo frontend y confiar ciegamente en backend.
3. No validar salida del modelo antes de enviarla a usuarios/sistemas.
4. Meter logica de negocio compleja dentro de validadores (mejor separarla).

## Ejercicio recomendado

Implementa un endpoint de scoring que reciba `FeatureRow` y retorne `FraudPrediction`.
Prueba 3 casos invalidos y revisa el mensaje de error estructurado.

## Siguiente paso runnable

Ejecuta:

```bash
python 04_ejemplos_runnable/ejemplo_07_pydantic_ai.py
```
