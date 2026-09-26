"""Errores de la API.

Regla: **el cliente recibe la categoria, los registros internos reciben el
detalle**. Una traza o una ruta local en la respuesta convierte un fallo en
informacion util para quien no deberia tenerla; a la vez, ocultarla tambien en
los logs haria imposible diagnosticar nada.
"""

from __future__ import annotations

import logging

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from recruitment_ml.serving.loader import ArtifactUnavailableError
from recruitment_ml.serving.predictor import PredictionError

LOGGER = logging.getLogger("recruitment_ml.api")

#: El modelo no esta disponible o no es compatible. No es culpa del cliente.
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_INTERNAL_ERROR = 500
HTTP_UNPROCESSABLE = 422

MODEL_UNAVAILABLE_MESSAGE = (
    "El modelo no esta disponible. Reconstruye el artefacto con "
    "'python -m recruitment_ml.serving.build_artifact'."
)
INFERENCE_FAILED_MESSAGE = "La inferencia no pudo completarse."


def safe_validation_errors(errors: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Errores de validacion sin devolver al cliente lo que envio.

    El manejador por omision de FastAPI incluye el valor recibido en `input`.
    Eso tiene dos problemas. Uno practico: un `NaN` o un `Infinity` en el
    payload no es serializable a JSON, y la respuesta de error reventaria al
    codificarse. Otro de criterio: si alguien manda por error un dato personal
    en un campo prohibido, devolverselo en el cuerpo del 422 lo copia a los
    logs del cliente y a cualquier intermediario.

    Se conservan `loc`, `msg` y `type`, que es lo que permite corregir la
    peticion.
    """
    safe: list[dict[str, str]] = []
    for error in errors:
        safe.append(
            {
                "field": ".".join(str(part) for part in error.get("loc", ()) if part != "body"),
                "message": str(error.get("msg", "valor invalido")),
                "type": str(error.get("type", "value_error")),
            }
        )
    return safe


def register_error_handlers(app: FastAPI) -> None:
    """Conecta las excepciones del dominio con respuestas seguras."""

    @app.exception_handler(RequestValidationError)
    async def _validation_failed(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_UNPROCESSABLE,
            content={
                "error": "validation_error",
                "detail": "El payload no cumple el contrato de features.",
                "errors": safe_validation_errors(list(exc.errors())),
            },
        )

    @app.exception_handler(ArtifactUnavailableError)
    async def _artifact_unavailable(
        request: Request, exc: ArtifactUnavailableError
    ) -> JSONResponse:
        LOGGER.error("artefacto no disponible en %s: %s", request.url.path, exc)
        return JSONResponse(
            status_code=HTTP_SERVICE_UNAVAILABLE,
            content={"error": "model_unavailable", "detail": MODEL_UNAVAILABLE_MESSAGE},
        )

    @app.exception_handler(PredictionError)
    async def _prediction_failed(request: Request, exc: PredictionError) -> JSONResponse:
        LOGGER.error("fallo de inferencia en %s: %s", request.url.path, exc)
        return JSONResponse(
            status_code=HTTP_INTERNAL_ERROR,
            content={"error": "inference_failed", "detail": INFERENCE_FAILED_MESSAGE},
        )
