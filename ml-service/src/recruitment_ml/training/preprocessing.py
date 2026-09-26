"""Conjuntos de features y preprocesamiento reproducible.

El preprocesamiento vive dentro de un `Pipeline` de scikit-learn, de modo que
el escalado se ajusta **solo con train** y validation y test unicamente se
transforman. Es la forma estructural de impedir la fuga, no una convencion que
haya que recordar.
"""

from __future__ import annotations

from typing import Final

import pandas as pd

from recruitment_ml.schema import (
    METADATA_COLUMNS,
    MODEL_READY_FEATURES,
    TARGET_COLUMN,
    is_forbidden_column,
)

#: Conjunto principal: las 15 features model-ready del contrato.
FEATURE_SET_CORE: Final[str] = "core"

#: Ablations obligatorias declaradas por la auditoria de 15A.
FEATURE_SET_NO_CONCURRENCY: Final[str] = "core_without_concurrency"
FEATURE_SET_NO_ELAPSED: Final[str] = "core_without_elapsed"
FEATURE_SET_WITH_STAGE_COUNT: Final[str] = "core_plus_configured_stage_count"

FEATURE_SETS: Final[dict[str, tuple[str, ...]]] = {
    FEATURE_SET_CORE: MODEL_READY_FEATURES,
    FEATURE_SET_NO_CONCURRENCY: tuple(
        column for column in MODEL_READY_FEATURES if column != "concurrent_open_vacancies_count"
    ),
    FEATURE_SET_NO_ELAPSED: tuple(
        column for column in MODEL_READY_FEATURES if column != "elapsed_days_since_publication"
    ),
    FEATURE_SET_WITH_STAGE_COUNT: MODEL_READY_FEATURES + ("configured_stage_count",),
}

#: Columnas que jamas pueden entrar en X, aunque esten en el frame.
NEVER_IN_X: Final[tuple[str, ...]] = METADATA_COLUMNS + (TARGET_COLUMN,)


def feature_columns(feature_set: str) -> tuple[str, ...]:
    """Columnas de un conjunto de features declarado."""
    if feature_set not in FEATURE_SETS:
        raise ValueError(f"conjunto de features desconocido: {feature_set!r}")
    return FEATURE_SETS[feature_set]


def assert_feature_set_is_clean(feature_set: str) -> None:
    """Falla si un conjunto de features contiene algo prohibido.

    Se comprueba antes de entrenar: un identificador, un metadato o el propio
    target dentro de X invalidaria el experimento entero.
    """
    for column in feature_columns(feature_set):
        if column in NEVER_IN_X:
            raise ValueError(f"{column!r} es metadato o target y no puede entrar en X")
        if is_forbidden_column(column):
            raise ValueError(f"{column!r} viola el contrato de features")


def build_matrix(frame: pd.DataFrame, feature_set: str) -> pd.DataFrame:
    """Matriz X de una particion, en el orden canonico del conjunto."""
    assert_feature_set_is_clean(feature_set)
    columns = list(feature_columns(feature_set))
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"faltan columnas en el frame: {missing}")
    return frame[columns].astype("float64")


def build_target(frame: pd.DataFrame) -> pd.Series:
    """Vector y de una particion, como enteros 0/1."""
    target = frame[TARGET_COLUMN]
    if target.isna().any():
        raise ValueError("hay filas sin etiqueta; los censurados no deben llegar aqui")
    return target.astype("int64")
