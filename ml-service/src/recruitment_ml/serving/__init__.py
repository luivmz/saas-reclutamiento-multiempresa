"""Capa de servicio del modelo congelado en la Fase 15B.

Separa dos responsabilidades que conviene no mezclar:

- `build_artifact` **reconstruye** el modelo a partir del protocolo congelado,
  de forma reproducible y sin versionar binarios;
- `loader` y `predictor` **sirven** ese artefacto, verificando antes que
  corresponde exactamente al freeze que la fase aprobo.

Nada de esto autoriza despliegue: el servicio es experimental y no tiene
validacion institucional. `GAP-01` quedo resuelto tecnicamente en la Fase 16
(`vacancies.target_completion_at`); eso no cambia su caracter experimental.
"""

from recruitment_ml.serving.metadata import ArtifactMetadata, ServiceMetadata
from recruitment_ml.serving.predictor import PredictionOutcome, RiskPredictor

__all__ = [
    "ArtifactMetadata",
    "ServiceMetadata",
    "PredictionOutcome",
    "RiskPredictor",
]
