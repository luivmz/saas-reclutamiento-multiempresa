"""Contrato de columnas del dataset sintetico.

Implementa `docs/v1.1/ml/feature-contract.md`. Es la unica fuente de verdad
sobre que columna es feature, cual es metadato, cual es auxiliar y cual esta
prohibida. Los validadores y las pruebas leen de aqui, no de listas duplicadas.
"""

from __future__ import annotations

import re
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
#: se genera explicitamente. Laravel la calcula desde la Fase 16 a partir de
#: `vacancies.target_completion_at` (GAP-01 resuelto tecnicamente).
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

#: Palabras prohibidas, comparadas **por token** y no por subcadena.
#:
#: La distincion importa: buscar la subcadena "age" bloquearia `coverage_ratio`
#: y `management_latency`, y buscar "name" bloquearia `filename`. Tokenizando
#: por separadores y comparando palabras completas, `evaluation_score` queda
#: bloqueada por el token "score" mientras `coverage_ratio` pasa.
FORBIDDEN_WORDS: Final[frozenset[str]] = frozenset(
    {
        # Identidad y contacto
        "nombre",
        "nombres",
        "apellido",
        "apellidos",
        "name",
        "names",
        "fullname",
        "firstname",
        "lastname",
        "dni",
        "email",
        "correo",
        "mail",
        "phone",
        "telefono",
        "address",
        "direccion",
        "photo",
        "foto",
        # Atributos demograficos y sensibles
        "age",
        "edad",
        "birth",
        "birthdate",
        "nacimiento",
        "gender",
        "genero",
        "sexo",
        "sex",
        "nationality",
        "nacionalidad",
        "marital",
        "race",
        "raza",
        "ethnic",
        "ethnicity",
        "etnia",
        "religion",
        "sexual",
        "health",
        "salud",
        "disability",
        "discapacidad",
        "ideology",
        "ideologia",
        "sindical",
        "biometric",
        "biometrico",
        # Proxies socioeconomicos
        "university",
        "universidad",
        "school",
        "colegio",
        # Contenido textual
        "cv",
        "resume",
        "curriculum",
        "embedding",
        "embeddings",
        "comment",
        "comentario",
        "observations",
        "observaciones",
        "justification",
        "justificacion",
        "text",
        "texto",
        # Personas y resultados sobre personas
        "candidate",
        "candidato",
        "postulante",
        "applicant",
        "evaluator",
        "user",
        "selected",
        "selection",
        "seleccion",
        "seleccionado",
        "decision",
        "score",
        "scores",
        "puntaje",
        "rank",
        "ranking",
        "outcome",
        "result",
        "results",
        "resultado",
        "final",
        "finalist",
        # Datos posteriores al checkpoint
        "closed",
        "closure",
        "cierre",
        "duration",
        "duracion",
        "document",
        "documento",
    }
)

#: Prefijos/sufijos legitimos que nunca deben tokenizarse como prohibidos.
#: `days_remaining_to_target` contiene "target" y es una feature valida: una
#: diferencia de dias conocida en el checkpoint, no el plazo en si.
ALLOWED_WORDS: Final[frozenset[str]] = frozenset({"target", "status", "count", "days"})

#: Columnas que forman la matriz X del modelo.
MODEL_READY_FEATURES: Final[tuple[str, ...]] = CORE_FEATURES + CONDITIONAL_FEATURES

#: Features que se conservan en X pero cuya contribucion **debe** compararse en
#: 15B entrenando con y sin ellas.
#:
#: `concurrent_open_vacancies_count` crece con el calendario porque los procesos
#: estancados permanecen abiertos indefinidamente, fiel al dominio real donde no
#: existe cancelacion (A-22). Es informativa, pero 15B tiene que demostrar que
#: el modelo no esta aprendiendo simplemente el paso del tiempo.
#: `elapsed_days_since_publication` y `application_window_days` quedan casi
#: colineales por construccion del checkpoint: al definirse como `closes_at + 1`,
#: el tiempo transcurrido desde la publicacion es la ventana mas el desfase entre
#: publicar y abrir postulaciones. La identidad exacta se elimino generando ese
#: desfase, pero la correlacion residual sigue siendo alta y es una propiedad del
#: diseno aprobado, no un defecto del generador.
ABLATION_REQUIRED_IN_15B: Final[tuple[str, ...]] = (
    "concurrent_open_vacancies_count",
    "configured_stage_count",
    "elapsed_days_since_publication",
)

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


def tokenize_column(column: str) -> list[str]:
    """Descompone un nombre de columna en palabras comparables.

    Separa por guiones, guiones bajos, puntos, espacios y por los limites de
    camelCase, y normaliza a minusculas. `candidateEmail`, `candidate_email` y
    `Candidate.Email` producen los mismos tokens.
    """
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", column)
    return [token for token in re.split(r"[^A-Za-z0-9]+", spaced) if token]


def _is_forbidden_word(token: str) -> bool:
    """True si el token es una palabra prohibida, admitiendo plural simple."""
    lowered = token.lower()
    if lowered in ALLOWED_WORDS:
        return False
    if lowered in FORBIDDEN_WORDS:
        return True
    # Plural regular: `scores` -> `score`, `candidates` -> `candidate`.
    if len(lowered) > 3 and lowered.endswith("s") and lowered[:-1] in FORBIDDEN_WORDS:
        return True
    return False


def is_forbidden_column(column: str) -> bool:
    """True si el nombre de columna viola el contrato de features.

    Se comprueba por nombre exacto y por **token completo**, no por subcadena:
    `coverage_ratio`, `management_latency` y `filename` son nombres
    operacionales legitimos que una busqueda de subcadenas bloquearia por
    contener "age" o "name".
    """
    lowered = column.lower()
    if lowered in {c.lower() for c in FORBIDDEN_COLUMNS}:
        return True
    if lowered in {c.lower() for c in DATASET_COLUMNS}:
        return False
    return any(_is_forbidden_word(token) for token in tokenize_column(column))
