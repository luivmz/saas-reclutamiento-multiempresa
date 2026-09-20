"""Reproducibilidad de modelos y baselines.

Misma semilla y misma configuracion deben producir el mismo resultado. Sin eso,
ninguna cifra del informe academico es citable.
"""

from __future__ import annotations

import numpy as np
import pytest

from recruitment_ml.training.baselines import OperationalRule, dummy_scores, fit_dummy
from recruitment_ml.training.calibration import positive_scores
from recruitment_ml.training.models import SEED, build_pipeline, candidate_grid
from recruitment_ml.training.preprocessing import FEATURE_SET_CORE, build_matrix, build_target


@pytest.fixture(scope="module")
def matrices(temporal_split):
    train, validation = temporal_split.train, temporal_split.validation
    return (
        build_matrix(train, FEATURE_SET_CORE),
        build_target(train),
        build_matrix(validation, FEATURE_SET_CORE),
    )


@pytest.mark.parametrize(
    ("family", "params"),
    [
        ("logistic_regression", {"C": 1.0, "class_weight": None}),
        ("decision_tree", {"max_depth": 5, "min_samples_leaf": 20}),
        ("random_forest", {"n_estimators": 50, "max_depth": 6, "min_samples_leaf": 20}),
        ("hist_gradient_boosting", {"max_depth": 3, "max_iter": 50, "early_stopping": False}),
    ],
)
def test_every_family_is_deterministic(matrices, family: str, params: dict) -> None:
    X_train, y_train, X_validation = matrices

    first = build_pipeline(family, params).fit(X_train, y_train)
    second = build_pipeline(family, params).fit(X_train, y_train)

    np.testing.assert_allclose(
        positive_scores(first, X_validation), positive_scores(second, X_validation), rtol=1e-12
    )


def test_seed_is_the_approved_one() -> None:
    assert SEED == 20260920


def test_unknown_family_is_rejected() -> None:
    with pytest.raises(ValueError):
        build_pipeline("red_neuronal", {})


def test_grid_stays_small_and_reviewable() -> None:
    """Sin AutoML: la rejilla debe caber en una tabla."""
    full = candidate_grid(include_optional=True)
    reduced = candidate_grid(include_optional=False)

    assert len(full) == 22
    assert len(reduced) == 18
    assert len({(c.family, tuple(sorted(c.params.items(), key=str))) for c in full}) == len(full)


def test_forbidden_model_families_are_absent() -> None:
    families = {candidate.family for candidate in candidate_grid()}

    assert families == {
        "logistic_regression",
        "decision_tree",
        "random_forest",
        "hist_gradient_boosting",
    }


def test_only_logistic_regression_is_scaled() -> None:
    """Escalar arboles anadiria un paso sin efecto y ruido a la auditoria."""
    logistic = build_pipeline("logistic_regression", {"C": 1.0})
    tree = build_pipeline("decision_tree", {"max_depth": 3})

    assert "scaler" in logistic.named_steps
    assert "scaler" not in tree.named_steps


def test_dummy_baseline_returns_the_train_prevalence(temporal_split) -> None:
    y_train = build_target(temporal_split.train)
    model = fit_dummy(y_train.to_numpy(), strategy="prior", seed=SEED)

    scores = dummy_scores(model, 25)

    assert np.allclose(scores, float(y_train.mean()))
    assert len(scores) == 25


def test_operational_rule_is_deterministic(temporal_split) -> None:
    rule = OperationalRule()

    np.testing.assert_array_equal(
        rule.decide(temporal_split.validation), rule.decide(temporal_split.validation)
    )


def test_whole_experiment_is_reproducible() -> None:
    """Dos ejecuciones independientes deben coincidir en todo lo cientifico."""
    from recruitment_ml.training.experiment import run_experiment

    first = run_experiment(rows=800, include_optional_model=False).to_dict()
    second = run_experiment(rows=800, include_optional_model=False).to_dict()

    assert first["dataset"]["model_ready_fingerprint"] == second["dataset"]["model_ready_fingerprint"]
    # `frozen_at` es metadato operativo y varia entre ejecuciones; la huella
    # del protocolo, que lo excluye, debe ser identica.
    assert first["freeze"]["freeze_fingerprint"] == second["freeze"]["freeze_fingerprint"]
    assert first["freeze"]["threshold"] == second["freeze"]["threshold"]
    assert first["test"] == second["test"]
    assert first["verdict"]["decision"] == second["verdict"]["decision"]


def test_a_different_seed_changes_the_experiment() -> None:
    from recruitment_ml.training.experiment import run_experiment

    base = run_experiment(rows=800, include_optional_model=False).to_dict()
    other = run_experiment(rows=800, seed=7, include_optional_model=False).to_dict()

    assert base["dataset"]["model_ready_fingerprint"] != other["dataset"]["model_ready_fingerprint"]
