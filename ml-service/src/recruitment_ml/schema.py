"""Contrato de columnas del dataset sintetico.

Implementa `docs/v1.1/ml/feature-contract.md`. Es la unica fuente de verdad
sobre que columna es feature, cual es metadato, cual es auxiliar y cual esta
prohibida. Los validadores y las pruebas leen de aqui, no de listas duplicadas.
"""

from __future__ import annotations

from typing import Final

#: ML-FEAT-01, 03..06, 08, 09, 11..13, 15..18. Nucleo aprobado y computable hoy
#: en Laravel.
CORE_FEATURES: Final[tuple[str, ...]] = (
    "elapsed_days_since_publication",
    "application_window_days",
    "positions_count",
    "applications_received_count",
    "configured_criteria_count",
    "evaluations_scheduled_count",
    "evaluations_completed_count",
    "evaluations_overdue_pending_count",
    "interviews_scheduled_count",
    "interviews_completed_count",
    "interviews_overdue_pending_count",
    "stage_transition_count",
    "days_since_last_operational_event",
    "concurrent_open_vacancies_count",
)

#: ML-FEAT-02. Aprobada para el dataset sintetico porque `target_completion_at`
#: se genera explicitamente. NO es computable en Laravel mientras GAP-01 siga
#: abierta.
CONDITIONAL_FEATURES: Final[tuple[str, ...]] = ("days_remaining_to_target",)

#: ML-FEAT-07. Cardinalidad maxima 3 por el CHECK del esquema real. Se genera,
#: pero queda fuera del conjunto model-ready: solo se estudia como ablation.
ABLATION_FEATURES: Final[tuple[str, ...]] = ("configured_stage_count",)

#: ML-FEAT-10 y ML-FEAT-14. Combinacion lineal exacta de dos features ya
#: incluidas. Se conservan para validar invariantes, nunca como features.
AUXILIARY_COLUMNS: Final[tuple[str, ...]] = (
    "evaluations_pending_count",
    "interviews_pending_count",
)

#: Identificadores y linaje. Nunca entran en X.
METADATA_COLUMNS: Final[tuple[str, ...]] = (
    "vacancy_id",
    "organization_id",
    "checkpoint_at",
    "observation_status",
    "dataset_version",
)

TARGET_COLUMN: Final[str] = "delayed"

#: Factores latentes del generador. Existen solo en memoria durante la
#: simulacion y no pueden alcanzar ningun frame exportado.
LATENT_FACTORS: Final[tuple[str, ...]] = (
    "operational_capacity",
    "coordination_friction",
    "workload_pressure",
    "random_shock",
    "period_effect",
)

#: Columnas prohibidas por nombre exacto (`feature-contract.md` seccion 3).
FORBIDDEN_COLUMNS: Final[tuple[str, ...]] = (
    "candidate_id",
    "user_id",
    "evaluator_id",
    "scheduled_by",
    "changed_by",
    "job_request_id",
    "selected_application_id",
    "decided_by",
    "decided_at",
    "closed_at",
    "closed_by",
    "closure_type",
    "closure_notes",
    "status",
    "total_duration_days",
    "selected_score",
    "selected_position",
    "ranked_candidates",
    "outcome",
    "score",
    "ranking",
    "observations",
    "justification",
    "required_by",
    "target_completion_at",
)

#: Fragmentos prohibidos: cualquier columna que los contenga delata identidad,
#: atributo sensible, proxy socioeconomico, contenido textual o resultado sobre
#: una persona.
FORBIDDEN_TOKENS: Final[tuple[str, ...]] = (
    "nombre",
    "apellido",
    "name",
    "dni",
    "email",
    "correo",
    "phone",
    "telefono",
    "address",
    "direccion",
    "photo",
    "foto",
    "age",
    "edad",
    "birth",
    "nacimiento",
    "gender",
    "genero",
    "sexo",
    "nationality",
    "nacionalidad",
    "marital",
    "civil",
    "race",
    "raza",
    "ethnic",
    "etnia",
    "religion",
    "sexual",
    "health",
    "salud",
    "disab",
    "discapacidad",
    "ideolog",
    "union",
    "sindical",
    "biometric",
    "biometr",
    "university",
    "universidad",
    "school",
    "cv",
    "resume",
    "embedding",
    "comment",
    "comentario",
    "text",
    "candidate",
    "postulante",
    "selected",
    "seleccion",
    "decision",
    # Resultados sobre personas y datos posteriores al checkpoint. Van como
    # fragmento y no solo como nombre exacto: `evaluation_score` o
    # `vacancy_closed_at` deben quedar bloqueados igual que `score` o
    # `closed_at`.
    "score",
    "puntaje",
    "rank",
    "outcome",
    "closed",
    "closure",
    "justification",
    "justificacion",
    "observation",
    "observacion",
)

#: Columnas que forman la matriz X del modelo.
MODEL_READY_FEATURES: Final[tuple[str, ...]] = CORE_FEATURES + CONDITIONAL_FEATURES

#: Orden canonico de columnas del dataset exportado.
DATASET_COLUMNS: Final[tuple[str, ...]] = (
    METADATA_COLUMNS
    + MODEL_READY_FEATURES
    + ABLATION_FEATURES
    + AUXILIARY_COLUMNS
    + (TARGET_COLUMN,)
)

#: Tipo esperado de cada columna no temporal. Todas las features son enteros no
#: negativos: son conteos y diferencias de dias.
INTEGER_COLUMNS: Final[tuple[str, ...]] = (
    MODEL_READY_FEATURES + ABLATION_FEATURES + AUXILIARY_COLUMNS
)

#: Estados posibles de una observacion.
STATUS_COMPLETED: Final[str] = "completed"
STATUS_CENSORED: Final[str] = "censored"


def is_forbidden_column(column: str) -> bool:
    """True si el nombre de columna viola el contrato de features.

    La comprobacion es por nombre exacto y por fragmento, porque una columna
    prohibida puede colarse con un nombre derivado.
    """
    lowered = column.lower()
    if lowered in {c.lower() for c in FORBIDDEN_COLUMNS}:
        return True
    # `days_remaining_to_target` es legitima aunque contenga "target": es una
    # diferencia de dias conocida en el checkpoint, no el plazo en si.
    if lowered in {c.lower() for c in DATASET_COLUMNS}:
        return False
    return any(token in lowered for token in FORBIDDEN_TOKENS)
