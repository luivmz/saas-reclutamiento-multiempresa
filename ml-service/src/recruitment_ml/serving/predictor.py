"""Inferencia de riesgo operacional.

Dos garantias que el codigo impone, en lugar de confiar en que se recuerden:

- **el orden lo pone el artefacto, no el JSON**. El payload llega como un
  diccionario y los diccionarios tienen orden de insercion; construir la matriz
  con ese orden haria que dos peticiones equivalentes produjeran predicciones
  distintas. Aqui se reindexa siempre por `feature_order`;
- **el umbral es el congelado**, con toda su precision. Redondearlo cambia la
  clasificacion de las observaciones en la frontera.

La inferencia es *stateless*: no guarda peticiones, no persiste predicciones y
no almacena nada de quien pregunta.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd

from recruitment_ml.serving.metadata import ArtifactMetadata


class PredictionError(RuntimeError):
    """La inferencia no pudo completarse."""


@dataclass(frozen=True)
class PredictionOutcome:
    """Resultado de una prediccion, sin rastro de la peticion que la produjo."""

    risk_score: float
    risk_flag: bool
    threshold: float


@dataclass(frozen=True)
class RiskPredictor:
    """Pipeline cargado junto con los metadatos que lo identifican."""

    pipeline: Any
    metadata: ArtifactMetadata

    @property
    def feature_order(self) -> list[str]:
        return list(self.metadata.feature_order)

    @property
    def threshold(self) -> float:
        return float(self.metadata.threshold)

    def build_frame(self, features: Mapping[str, float]) -> pd.DataFrame:
        """Matriz de una fila, en el orden canonico del artefacto."""
        missing = [name for name in self.feature_order if name not in features]
        if missing:
            raise PredictionError(f"faltan features: {missing}")
        row = {name: float(features[name]) for name in self.feature_order}
        return pd.DataFrame([row], columns=self.feature_order).astype("float64")

    def predict(self, features: Mapping[str, float]) -> PredictionOutcome:
        """Probabilidad de retraso operacional y senal para revision humana."""
        frame = self.build_frame(features)
        try:
            probabilities = self.pipeline.predict_proba(frame)
        except Exception as error:  # noqa: BLE001 - sklearn no acota sus fallos
            raise PredictionError(f"la inferencia fallo: {error}") from error

        score = float(probabilities[0][1])
        threshold = self.threshold
        return PredictionOutcome(
            risk_score=score,
            # Comparacion con el umbral exacto, nunca con el redondeado.
            risk_flag=bool(score >= threshold),
            threshold=threshold,
        )
