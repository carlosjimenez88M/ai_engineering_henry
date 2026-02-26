"""
Ejemplo 07: Pydantic aplicado a AI/ML
======================================

Demuestra validacion de:
1. Request de inferencia
2. Fila de features
3. Salida de modelo

Ejecutar:
    python ejemplo_07_pydantic_ai.py
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator


class InferenceRequest(BaseModel):
    prompt: str = Field(min_length=5, max_length=2000)
    max_tokens: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class FeatureRow(BaseModel):
    age: int = Field(ge=0, le=120)
    monthly_income_usd: float = Field(ge=0)
    tenure_months: int = Field(ge=0)

    @field_validator("monthly_income_usd")
    @classmethod
    def reject_unrealistic_income(cls, value: float) -> float:
        if value > 1_000_000:
            raise ValueError("monthly_income_usd parece fuera de rango realista")
        return value


class FraudPrediction(BaseModel):
    label: Literal["fraud", "not_fraud"]
    score: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=10)


def fake_model_predict(features: FeatureRow) -> FraudPrediction:
    """Modelo simplificado solo para demo educativa."""
    if features.monthly_income_usd < 1000 and features.tenure_months < 3:
        return FraudPrediction(
            label="fraud",
            score=0.81,
            rationale="Patron de riesgo: bajo ingreso y poca antiguedad.",
        )

    return FraudPrediction(
        label="not_fraud",
        score=0.22,
        rationale="No se observan senales fuertes de fraude en las features.",
    )


def demo_inference_request_validation() -> None:
    print("\n[1] Validacion de request de inferencia")

    valid_payload = {
        "prompt": "Explica en 3 puntos por que MLOps necesita validacion de datos.",
        "max_tokens": 300,
        "temperature": 0.3,
    }
    request = InferenceRequest(**valid_payload)
    print("Request valido:", request.model_dump())

    invalid_payload = {
        "prompt": "hola",
        "max_tokens": "muchos",
        "temperature": 4.2,
    }

    try:
        InferenceRequest(**invalid_payload)
    except ValidationError as exc:
        print("Request invalido (errores estructurados):")
        for err in exc.errors():
            print(" -", err["loc"], err["msg"])


def demo_feature_row_and_prediction() -> None:
    print("\n[2] Validacion de features y salida de modelo")

    raw_features = {
        "age": 29,
        "monthly_income_usd": 820.5,
        "tenure_months": 1,
    }
    features = FeatureRow(**raw_features)
    prediction = fake_model_predict(features)
    print("Features validadas:", features.model_dump())
    print("Prediccion validada:", prediction.model_dump())

    invalid_features = {
        "age": 31,
        "monthly_income_usd": 2_500_000,
        "tenure_months": 4,
    }

    try:
        FeatureRow(**invalid_features)
    except ValidationError as exc:
        print("Features invalidas:")
        for err in exc.errors():
            print(" -", err["loc"], err["msg"])


def main() -> None:
    print("=" * 72)
    print("EJEMPLO 07 - PYDANTIC PARA AI/ML")
    print("=" * 72)

    demo_inference_request_validation()
    demo_feature_row_and_prediction()

    print("\nResumen:")
    print("1. Pydantic valida contratos de entrada y salida.")
    print("2. Reduce bugs silenciosos en pipelines de AI/ML.")
    print("3. Errores de validacion vienen estructurados y accionables.")


if __name__ == "__main__":
    main()
