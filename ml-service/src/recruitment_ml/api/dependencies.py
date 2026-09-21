"""Estado del modelo durante la vida del proceso.

El modelo se carga **una vez**, en el arranque, y se reutiliza en cada
peticion: entrenar o deserializar por request convertiria cada llamada en
segundos de CPU y, peor, haria que dos peticiones identicas pudieran responder
distinto.

El estado es de solo lectura tras la carga -- un pipeline de scikit-learn ya
ajustado solo se consulta -- asi que no hace falta sincronizacion. Lo que el
servicio **no** guarda es igual de importante: ni peticiones, ni predicciones,
ni nada de quien pregunta.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from recruitment_ml.serving.loader import ArtifactUnavailableError
from recruitment_ml.serving.predictor import RiskPredictor


@dataclass
class ModelState:
    """Predictor cargado, o el motivo por el que no lo esta."""

    predictor: RiskPredictor | None = None
    failure: str | None = field(default=None)

    @property
    def ready(self) -> bool:
        return self.predictor is not None

    def set_ready(self, predictor: RiskPredictor) -> None:
        self.predictor = predictor
        self.failure = None

    def set_failed(self, reason: str) -> None:
        self.predictor = None
        self.failure = reason

    def require(self) -> RiskPredictor:
        """Predictor cargado, o un error que la API traduce a 503."""
        if self.predictor is None:
            raise ArtifactUnavailableError(self.failure or "el modelo no esta cargado")
        return self.predictor
