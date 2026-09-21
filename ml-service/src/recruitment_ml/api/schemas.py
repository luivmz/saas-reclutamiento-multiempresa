"""Esquemas de la API.

Dos decisiones que conviene justificar:

- **`extra="forbid"`**. Un campo de mas no es un descuido inocente: es la via
  por la que entrarian `candidate_id`, `vacancy_id` o cualquier atributo
  personal. Rechazar lo desconocido convierte el contrato de features en una
  frontera efectiva y no en una recomendacion.
- **`strict=True`**. En modo laxo Pydantic convertiria `"12"` en `12` y `3.5`
  en `3`. Las features son conteos y diferencias de dias enteras; aceptar una
  cadena o un decimal silenciaria un error del cliente.

Los limites provienen del contrato sintetico aprobado, no de supuestos
institucionales: todas las features son enteros no negativos y
`days_remaining_to_target` es estrictamente positiva porque el plazo es
posterior al checkpoint. El tope de los campos en dias sale del periodo maximo
que admite `SyntheticConfig` (180 meses).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from recruitment_ml.schema import MODEL_READY_FEATURES

#: Tope de los campos medidos en dias. `SyntheticConfig.months` admite como
#: maximo 180 meses; por encima de eso el valor no pertenece a ningun dataset
#: que este contrato pueda haber producido.
MAX_DAYS = 180 * 31

_COUNT = Field(ge=0, description="Conteo operacional no negativo.")


class PredictionRequest(BaseModel):
    """Features operacionales de **un** proceso de vacante en un checkpoint.

    No incluye identificadores, ni datos de personas, ni resultados del
    proceso. El servicio no sabria que hacer con ellos y los rechaza.
    """

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        json_schema_extra={
            "example": {
                "elapsed_days_since_publication": 34,
                "application_window_days": 21,
                "positions_count": 2,
                "applications_received_count": 18,
                "configured_criteria_count": 5,
                "evaluations_scheduled_count": 12,
                "evaluations_completed_count": 7,
                "evaluations_overdue_pending_count": 2,
                "interviews_scheduled_count": 6,
                "interviews_completed_count": 3,
                "interviews_overdue_pending_count": 1,
                "stage_transition_count": 9,
                "days_since_last_operational_event": 4,
                "concurrent_open_vacancies_count": 5,
                "days_remaining_to_target": 12,
            }
        },
    )

    elapsed_days_since_publication: int = Field(
        ge=0, le=MAX_DAYS, description="Dias transcurridos desde la publicacion de la vacante."
    )
    application_window_days: int = Field(
        ge=0, le=MAX_DAYS, description="Duracion de la ventana de postulacion, en dias."
    )
    positions_count: int = _COUNT
    applications_received_count: int = _COUNT
    configured_criteria_count: int = _COUNT
    evaluations_scheduled_count: int = _COUNT
    evaluations_completed_count: int = _COUNT
    evaluations_overdue_pending_count: int = _COUNT
    interviews_scheduled_count: int = _COUNT
    interviews_completed_count: int = _COUNT
    interviews_overdue_pending_count: int = _COUNT
    stage_transition_count: int = _COUNT
    days_since_last_operational_event: int = Field(
        ge=0, le=MAX_DAYS, description="Dias desde el ultimo evento operacional registrado."
    )
    concurrent_open_vacancies_count: int = _COUNT
    days_remaining_to_target: int = Field(
        ge=1,
        le=MAX_DAYS,
        description=(
            "Dias que faltan para el plazo objetivo. Estrictamente positiva por contrato. "
            "GAP-01: Laravel todavia no puede producirla."
        ),
    )

    def as_features(self) -> dict[str, float]:
        """Features como numeros, sin asumir el orden del JSON."""
        return {name: float(value) for name, value in self.model_dump().items()}


class PredictionResponse(BaseModel):
    """Riesgo operacional estimado y senal para revision humana."""

    # `model_version`, `model_ready` y `model_family` chocan con el espacio
    # protegido `model_` de Pydantic. Son los nombres del contrato publico de
    # la API, asi que se desactiva el espacio en lugar de renombrarlos.
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    risk_score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Probabilidad estimada de retraso operacional del proceso. "
            "No evalua, puntua ni clasifica personas."
        ),
    )
    risk_flag: bool = Field(
        description=(
            "risk_score >= threshold. Senal para revision humana: no es una decision, "
            "ni una recomendacion, ni un descarte, ni un ranking."
        )
    )
    threshold: float = Field(description="Umbral congelado en la Fase 15B, con precision completa.")
    model_version: str = Field(description="Identificador del experimento que produjo el modelo.")
    freeze_fingerprint: str = Field(description="Huella del protocolo congelado.")
    status: str = Field(description="Estado del servicio: experimental, no desplegable.")


class HealthResponse(BaseModel):
    """Estado del proceso y del modelo, por separado."""

    # Ver la nota de PredictionResponse sobre `protected_namespaces`.
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    status: str = Field(description="Estado del proceso del servicio.")
    model_ready: bool = Field(description="True si hay un artefacto cargado y verificado.")
    version: str = Field(description="Version del componente Python.")
    detail: str | None = Field(
        default=None,
        description="Motivo generico de que el modelo no este listo. Sin rutas ni trazas.",
    )


class ModelInfoResponse(BaseModel):
    """Metadatos tecnicos del modelo servido. Ningun dato de entrenamiento."""

    # Ver la nota de PredictionResponse sobre `protected_namespaces`.
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    model_family: str
    experiment_id: str
    freeze_fingerprint: str
    threshold: float
    feature_order: list[str]
    verdict: str
    deployment_status: str
    gap_01_open: bool
    gap_01_note: str
    risk_score_meaning: str
    risk_flag_meaning: str
    artifact_schema_version: str
    library_versions: dict[str, str]


class ErrorResponse(BaseModel):
    """Respuesta de error, deliberadamente escueta para el cliente."""

    model_config = ConfigDict(extra="forbid")

    error: str
    detail: str


def expected_feature_names() -> tuple[str, ...]:
    """Nombres que el contrato de 15B declara como features model-ready."""
    return MODEL_READY_FEATURES


def assert_schema_matches_contract() -> None:
    """El esquema de la API no puede divergir del contrato de features.

    Se comprueba al importar el modulo de la aplicacion: si alguien anade o
    quita un campo, el servicio falla al arrancar en lugar de servir un modelo
    con una matriz distinta de la que se entreno.
    """
    declared = tuple(PredictionRequest.model_fields)
    expected = expected_feature_names()
    if set(declared) != set(expected):
        missing = sorted(set(expected) - set(declared))
        extra: list[str] = sorted(set(declared) - set(expected))
        raise RuntimeError(
            "PredictionRequest no coincide con el contrato de features "
            f"(faltan {missing}, sobran {extra})"
        )


def json_schema_example() -> dict[str, Any]:
    """Ejemplo ficticio publicado en OpenAPI."""
    extra = PredictionRequest.model_config.get("json_schema_extra") or {}
    return dict(extra.get("example", {}))  # type: ignore[union-attr]
