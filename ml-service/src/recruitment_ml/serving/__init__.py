"""Capa de servicio del modelo congelado en la Fase 15B.

Separa dos responsabilidades que conviene no mezclar:

- `build_artifact` **reconstruye** el modelo a partir del protocolo congelado,
  de forma reproducible y sin versionar binarios;
- `loader` y `predictor` **sirven** ese artefacto, verificando antes que
  corresponde exactamente al freeze que la fase aprobo.

Nada de esto autoriza despliegue: `GAP-01` sigue abierto y el servicio es
experimental.
"""

from recruitment_ml.serving.metadata import ArtifactMetadata, ServiceMetadata
from recruitment_ml.serving.predictor import PredictionOutcome, RiskPredictor

__all__ = [
    "ArtifactMetadata",
    "ServiceMetadata",
    "PredictionOutcome",
    "RiskPredictor",
]
