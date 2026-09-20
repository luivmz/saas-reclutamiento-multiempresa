"""Ausencia de fuga en el entrenamiento.

Tres garantias distintas: el preprocesamiento no ve validation ni test, la
matriz X no contiene metadatos ni columnas prohibidas, y el conjunto de prueba
no se puede abrir antes de congelar el experimento.
"""

from __future__ import annotations

import numpy as np
import pytest

from recruitment_ml.schema import METADATA_COLUMNS, TARGET_COLUMN, is_forbidden_column
from recruitment_ml.training.preprocessing import (
    FEATURE_SET_CORE,
    FEATURE_SETS,
    NEVER_IN_X,
    assert_feature_set_is_clean,
    build_matrix,
    build_target,
    feature_columns,
)
from recruitment_ml.training.split import SealedTestSetError


def test_scaler_is_fitted_only_with_train(temporal_split) -> None:
    """La media del escalador debe ser la de train, no la del conjunto completo."""
    from recruitment_ml.training.models import build_pipeline

    train, validation = temporal_split.train, temporal_split.validation
    X_train = build_matrix(train, FEATURE_SET_CORE)
    y_train = build_target(train)

    pipeline = build_pipeline("logistic_regression", {"C": 1.0, "class_weight": None})
    pipeline.fit(X_train, y_train)
    scaler = pipeline.named_steps["scaler"]

    np.testing.assert_allclose(scaler.mean_, X_train.mean().to_numpy(), rtol=1e-9)

    combined = build_matrix(
        __import__("pandas").concat([train, validation], ignore_index=True), FEATURE_SET_CORE
    )
    assert not np.allclose(scaler.mean_, combined.mean().to_numpy())


def test_validation_is_only_transformed_never_refitted(temporal_split) -> None:
    from recruitment_ml.training.models import build_pipeline

    X_train = build_matrix(temporal_split.train, FEATURE_SET_CORE)
    y_train = build_target(temporal_split.train)
    X_validation = build_matrix(temporal_split.validation, FEATURE_SET_CORE)

    pipeline = build_pipeline("logistic_regression", {"C": 1.0, "class_weight": None})
    pipeline.fit(X_train, y_train)
    before = pipeline.named_steps["scaler"].mean_.copy()

    pipeline.predict_proba(X_validation)

    np.testing.assert_array_equal(pipeline.named_steps["scaler"].mean_, before)


def test_sealed_test_cannot_be_opened_without_a_freeze(temporal_split) -> None:
    with pytest.raises(SealedTestSetError):
        temporal_split.sealed_test.reveal(None)

    class NotFrozen:
        is_frozen = False

    with pytest.raises(SealedTestSetError):
        temporal_split.sealed_test.reveal(NotFrozen())


def test_describing_the_test_partition_does_not_count_as_opening_it(temporal_split) -> None:
    """Documentar la particion es legitimo; entrenar con ella no."""
    before = temporal_split.sealed_test.reveal_count
    description = temporal_split.sealed_test.describe()

    assert description["n"] > 0
    assert temporal_split.sealed_test.reveal_count == before


@pytest.mark.parametrize("feature_set", list(FEATURE_SETS))
def test_no_feature_set_contains_metadata_or_target(feature_set: str) -> None:
    assert_feature_set_is_clean(feature_set)
    for column in feature_columns(feature_set):
        assert column not in NEVER_IN_X
        assert column not in METADATA_COLUMNS
        assert column != TARGET_COLUMN


@pytest.mark.parametrize("feature_set", list(FEATURE_SETS))
def test_no_feature_set_contains_a_forbidden_column(feature_set: str) -> None:
    for column in feature_columns(feature_set):
        assert not is_forbidden_column(column)


def test_identifiers_never_reach_the_matrix(temporal_split) -> None:
    X = build_matrix(temporal_split.train, FEATURE_SET_CORE)

    for identifier in ("vacancy_id", "organization_id", "checkpoint_at", "observation_status"):
        assert identifier not in X.columns
    assert TARGET_COLUMN not in X.columns


def test_raw_timestamps_are_not_used_as_features() -> None:
    for feature_set in FEATURE_SETS:
        for column in feature_columns(feature_set):
            assert not column.endswith("_at"), f"{column} parece un timestamp crudo"


def test_unknown_feature_set_is_rejected() -> None:
    with pytest.raises(ValueError):
        feature_columns("inventado")
    with pytest.raises(ValueError):
        assert_feature_set_is_clean("inventado")


def test_building_the_target_rejects_unlabelled_rows(temporal_split) -> None:
    corrupted = temporal_split.train.copy()
    corrupted.loc[0, TARGET_COLUMN] = None

    with pytest.raises(ValueError):
        build_target(corrupted)


def test_missing_feature_columns_are_reported(temporal_split) -> None:
    incomplete = temporal_split.train.drop(columns=["positions_count"])

    with pytest.raises(ValueError, match="faltan columnas"):
        build_matrix(incomplete, FEATURE_SET_CORE)
