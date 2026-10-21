"""Regresiones de la revision Sonar: conservar calculos y validacion del freeze."""

from dataclasses import replace

import pandas as pd
import pytest

from recruitment_ml.schema import ABLATION_REQUIRED_IN_15B, MODEL_READY_FEATURES, STATUS_CENSORED, STATUS_COMPLETED
from recruitment_ml.synthetic.generator import censoring_comparison
from recruitment_ml.training.freeze import FreezeValidationError, load_freeze, validate_ablation_conclusions


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([0.0, 0.0, 0.0, 0.0], 0.0, id="zero-variance"),
        pytest.param([0.0, 0.0, 1.0, 1.0], 0.0, id="constant-groups-existing-policy"),
        pytest.param([0.0, 1e-12, 1e-12, 2e-12], -2.0, id="positive-variance-must-not-be-rounded-to-zero"),
    ],
)
def test_censoring_comparison_preserves_zero_and_small_positive_variances(values, expected):
    frame = pd.DataFrame({feature: values for feature in MODEL_READY_FEATURES})
    frame["observation_status"] = [STATUS_CENSORED, STATUS_CENSORED, STATUS_COMPLETED, STATUS_COMPLETED]

    result = censoring_comparison(frame)

    assert result["available"] is True
    assert result["standardised_mean_differences"] == {feature: expected for feature in MODEL_READY_FEATURES}


@pytest.mark.parametrize(
    ("reading", "accepted"),
    [
        pytest.param("La diferencia es -0.25 puntos", True, id="negative-decimal"),
        pytest.param("Diferencia +1.00", True, id="positive-decimal"),
        pytest.param("Valor 12.34.56", True, id="existing-substring-semantics"),
        pytest.param("Valor \u0660.\u0665", True, id="unicode-digits-preserved"),
        pytest.param("sin cambios relevantes", False, id="no-number"),
        pytest.param("Solo 123", False, id="integer-is-not-a-decimal"),
        pytest.param("Solo .25", False, id="missing-integer-part"),
        pytest.param("Solo 1e-2", False, id="scientific-notation-not-accepted"),
        pytest.param("7" * 30_000, False, id="long-integer-without-decimal-point"),
        pytest.param("7" * 30_000 + ".5", True, id="long-valid-decimal"),
    ],
)
def test_ablation_readings_preserve_the_decimal_requirement(freeze_path, reading, accepted):
    freeze = replace(
        load_freeze(freeze_path),
        ablation_conclusions={feature: reading for feature in ABLATION_REQUIRED_IN_15B},
    )

    if accepted:
        validate_ablation_conclusions(freeze)
    else:
        with pytest.raises(FreezeValidationError, match="no reporta ninguna diferencia medible"):
            validate_ablation_conclusions(freeze)
