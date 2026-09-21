"""Servicio FastAPI experimental de riesgo operacional (Fase 15C).

Cadena completa prevista:

    React/Inertia -> Laravel -> HTTP interno -> FastAPI -> scikit-learn

**En 15C solo existe el tramo `FastAPI -> scikit-learn`.** Laravel no consume
este servicio todavia; eso es Fase 16. Y aunque lo consumiera, `GAP-01` sigue
abierto: `target_completion_at` no existe en Laravel, asi que
`days_remaining_to_target` no es computable en produccion. El servicio es
**experimental** y no esta autorizado para despliegue.

Lo que el servicio no hace, y no debe hacer: no toca la base de datos de
Laravel, no autentica usuarios, no ordena candidatos, no decide nada y no
almacena peticiones ni predicciones.

Arranque local:

    uvicorn recruitment_ml.api.app:app --host 127.0.0.1 --port 8001
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import Depends, FastAPI, Request

from recruitment_ml.api.dependencies import ModelState
from recruitment_ml.api.errors import register_error_handlers
from recruitment_ml.api.schemas import (
    ErrorResponse,
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
    assert_schema_matches_contract,
)
from recruitment_ml.serving.loader import ArtifactUnavailableError, load_predictor
from recruitment_ml.serving.metadata import DEPLOYMENT_STATUS, ServiceMetadata
from recruitment_ml.serving.predictor import RiskPredictor

LOGGER = logging.getLogger("recruitment_ml.api")

#: Version del componente Python que se sirve. No es la version del modelo.
SERVICE_VERSION = "0.1.0"

TITLE = "Servicio experimental de riesgo operacional"
DESCRIPTION = (
    "Estima la probabilidad de retraso operacional de un proceso de vacante. "
    "No evalua, puntua ni clasifica personas, y ninguna respuesta constituye una "
    "decision: la decision final es humana (RF-23). Servicio EXPERIMENTAL, sin "
    "autorizacion de despliegue mientras GAP-01 siga abierto. No debe exponerse "
    "fuera de localhost o de la red interna."
)

# Si alguien anade o quita un campo del esquema, el servicio falla al
# importarse en lugar de servir una matriz distinta de la entrenada.
assert_schema_matches_contract()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Carga el artefacto al arrancar, una sola vez.

    Un fallo aqui **no** tumba el proceso: el servicio sigue vivo y lo declara
    en `/health` con `model_ready=false`, que es mas util para diagnosticar que
    un contenedor en bucle de reinicio. Las rutas que necesitan el modelo
    responden 503.
    """
    state: ModelState = app.state.model_state
    try:
        state.set_ready(load_predictor())
        LOGGER.info("modelo cargado: %s", state.require().metadata.experiment_id)
    except ArtifactUnavailableError as error:
        state.set_failed(str(error))
        LOGGER.error("el modelo no pudo cargarse: %s", error)
    yield


def create_app() -> FastAPI:
    """Construye la aplicacion. Sin CORS: el consumidor sera Laravel, no un navegador."""
    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        version=SERVICE_VERSION,
        lifespan=lifespan,
    )
    app.state.model_state = ModelState()
    register_error_handlers(app)
    _register_routes(app)
    return app


def get_state(request: Request) -> ModelState:
    return request.app.state.model_state


def get_predictor(state: ModelState = Depends(get_state)) -> RiskPredictor:
    """Predictor cargado; si no lo hay, la excepcion se traduce a 503."""
    return state.require()


def _register_routes(app: FastAPI) -> None:
    @app.get(
        "/health",
        response_model=HealthResponse,
        summary="Estado del proceso y del modelo",
        tags=["operacion"],
    )
    def health(state: ModelState = Depends(get_state)) -> HealthResponse:
        """Distingue **proceso vivo** de **modelo listo**: no son lo mismo.

        Si el artefacto falta, el proceso sigue respondiendo y lo dice. El
        motivo es generico: ni rutas locales ni trazas.
        """
        return HealthResponse(
            status="ok",
            model_ready=state.ready,
            version=SERVICE_VERSION,
            detail=None if state.ready else "modelo no cargado",
        )

    @app.get(
        "/v1/model-info",
        response_model=ModelInfoResponse,
        responses={503: {"model": ErrorResponse}},
        summary="Metadatos tecnicos del modelo servido",
        tags=["modelo"],
    )
    def model_info(predictor: RiskPredictor = Depends(get_predictor)) -> ModelInfoResponse:
        """Que modelo se esta sirviendo y con que limitaciones.

        Informacion tecnica del experimento: ni datos de entrenamiento, ni
        filas individuales, ni rutas locales.
        """
        metadata = ServiceMetadata.from_artifact(predictor.metadata)
        return ModelInfoResponse(**metadata.to_dict())

    @app.post(
        "/v1/predict",
        response_model=PredictionResponse,
        responses={503: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
        summary="Riesgo operacional de un proceso de vacante",
        tags=["modelo"],
    )
    def predict(
        payload: PredictionRequest, predictor: RiskPredictor = Depends(get_predictor)
    ) -> PredictionResponse:
        """Probabilidad de retraso del **proceso**, no de ninguna persona.

        `risk_flag` es `risk_score >= threshold` con el umbral congelado: una
        senal para que alguien revise, nunca una decision.
        """
        outcome = predictor.predict(payload.as_features())
        return PredictionResponse(
            risk_score=outcome.risk_score,
            risk_flag=outcome.risk_flag,
            threshold=outcome.threshold,
            model_version=predictor.metadata.experiment_id,
            freeze_fingerprint=predictor.metadata.freeze_fingerprint,
            status=DEPLOYMENT_STATUS,
        )


app = create_app()
