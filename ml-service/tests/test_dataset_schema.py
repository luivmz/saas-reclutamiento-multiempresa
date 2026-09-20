"""Contrato de columnas y prohibiciones.

Validaciones 3, 4, 5, 10, 11, 17, 18 y 19. Estas pruebas son la barrera que
impide que una variable personal, un identificador o un factor latente acabe
dentro de la matriz X.
"""

from __future__ import annotations

import pandas as pd
import pytest

from recruitment_ml.schema import (
    ABLATION_FEATURES,
    AUXILIARY_COLUMNS,
    CORE_FEATURES,
    DATASET_COLUMNS,
    INTEGER_COLUMNS,
    LATENT_FACTORS,
    METADATA_COLUMNS,
    MODEL_READY_FEATURES,
    STATUS_CENSORED,
    STATUS_COMPLETED,
    TARGET_COLUMN,
    is_forbidden_column,
)
from recruitment_ml.synthetic.validators import check_columns, check_ranges, check_uniqueness


def test_columns_match_the_contract_exactly(frame: pd.DataFrame) -> None:
    assert list(frame.columns) == list(DATASET_COLUMNS)
    assert check_columns(frame) == []


def test_no_forbidden_column_is_present(frame: pd.DataFrame) -> None:
    offenders = [column for column in frame.columns if is_forbidden_column(column)]
    assert offenders == []


def test_no_latent_factor_is_exported(frame: pd.DataFrame) -> None:
    """Los latentes causan la covariacion; exportarlos seria regalar el target."""
    leaked = [factor for factor in LATENT_FACTORS if factor in frame.columns]
    assert leaked == []


@pytest.mark.parametrize(
    "column",
    [
        "candidate_id",
        "user_id",
        "organization_name",
        "candidate_email",
        "cv_text",
        "interview_outcome",
        "evaluation_score",
        "selected_application_id",
        "closed_at",
        "closure_type",
        "universidad",
        "fecha_nacimiento",
        "genero",
        "required_by",
        "target_completion_at",
    ],
)
def test_known_offenders_are_detected(column: str) -> None:
    assert is_forbidden_column(column)


@pytest.mark.parametrize("column", list(DATASET_COLUMNS))
def test_contract_columns_are_not_flagged(column: str) -> None:
    """Ninguna columna legitima puede quedar marcada como prohibida.

    `days_remaining_to_target` contiene la palabra "target" y debe pasar: es
    una diferencia de dias conocida en el checkpoint, no el plazo en si.
    """
    assert not is_forbidden_column(column)


def test_identifiers_exist_only_as_metadata() -> None:
    for identifier in ("vacancy_id", "organization_id"):
        assert identifier in METADATA_COLUMNS
        assert identifier not in MODEL_READY_FEATURES


def test_linear_combination_columns_are_not_model_ready() -> None:
    """`pending = scheduled - completed` es colinealidad exacta.

    Se conservan como auxiliares para validar invariantes, nunca como features.
    """
    for column in AUXILIARY_COLUMNS:
        assert column not in MODEL_READY_FEATURES
        assert column in DATASET_COLUMNS


def test_ablation_feature_is_not_model_ready() -> None:
    for column in ABLATION_FEATURES:
        assert column not in MODEL_READY_FEATURES


def test_model_ready_features_are_the_approved_set() -> None:
    assert MODEL_READY_FEATURES == CORE_FEATURES + ("days_remaining_to_target",)
    assert len(CORE_FEATURES) == 14


def test_dtypes_follow_the_contract(frame: pd.DataFrame) -> None:
    for column in INTEGER_COLUMNS:
        assert pd.api.types.is_integer_dtype(frame[column]), column
    assert str(frame[TARGET_COLUMN].dtype) == "Int64"


def test_no_nan_where_the_contract_forbids_it(frame: pd.DataFrame) -> None:
    assert check_ranges(frame) == []


def test_one_row_per_process(frame: pd.DataFrame) -> None:
    assert check_uniqueness(frame) == []
    assert frame["vacancy_id"].is_unique


def test_observation_status_has_only_the_two_expected_values(frame: pd.DataFrame) -> None:
    assert set(frame["observation_status"].unique()) <= {STATUS_COMPLETED, STATUS_CENSORED}


def test_feature_matrix_exposes_only_model_ready_columns(dataset) -> None:
    matrix = dataset.feature_matrix()
    assert list(matrix.columns) == list(MODEL_READY_FEATURES)
    assert TARGET_COLUMN not in matrix.columns
    for column in METADATA_COLUMNS:
        assert column not in matrix.columns


# --- los validadores deben disparar cuando el contrato se rompe -------------
#
# Un guardian que nunca falla no esta demostrado. Estas pruebas corrompen el
# frame a proposito y exigen que la validacion lo detecte.


def test_validator_detects_a_forbidden_column(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    corrupted["candidate_email"] = "x@example.invalid"

    problems = check_columns(corrupted)
    assert any("prohibida" in problem for problem in problems)


def test_validator_detects_an_exported_latent_factor(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    corrupted["operational_capacity"] = 1.0

    problems = check_columns(corrupted)
    assert any("latente" in problem for problem in problems)


def test_validator_detects_a_wrong_dtype(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    corrupted["positions_count"] = corrupted["positions_count"].astype(float)

    assert any("entera" in problem for problem in check_columns(corrupted))


def test_validator_detects_duplicated_processes(frame: pd.DataFrame) -> None:
    corrupted = pd.concat([frame, frame.head(1)], ignore_index=True)

    assert check_uniqueness(corrupted) != []


def test_validator_detects_negative_counts(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    corrupted.loc[0, "applications_received_count"] = -1

    assert any("negativos" in problem for problem in check_ranges(corrupted))


def test_validator_detects_a_non_positive_remaining_horizon(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    corrupted.loc[0, "days_remaining_to_target"] = 0

    assert any("days_remaining_to_target" in problem for problem in check_ranges(corrupted))
