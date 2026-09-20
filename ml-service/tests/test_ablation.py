"""Ablations obligatorias.

Dos de ellas responden a la pregunta central de la auditoria de 15A: si el
modelo aprende senal operacional o simplemente el paso del calendario.
"""

from __future__ import annotations

import pytest

from recruitment_ml.schema import ABLATION_REQUIRED_IN_15B
from recruitment_ml.training.ablation import ABLATION_FEATURE_SETS, run_ablations
from recruitment_ml.training.models import ModelCandidate
from recruitment_ml.training.preprocessing import (
    FEATURE_SET_CORE,
    FEATURE_SET_NO_CONCURRENCY,
    FEATURE_SET_NO_ELAPSED,
    FEATURE_SET_WITH_STAGE_COUNT,
    feature_columns,
)


def test_the_four_mandatory_feature_sets_are_compared() -> None:
    assert set(ABLATION_FEATURE_SETS) == {
        FEATURE_SET_CORE,
        FEATURE_SET_NO_CONCURRENCY,
        FEATURE_SET_NO_ELAPSED,
        FEATURE_SET_WITH_STAGE_COUNT,
    }


def test_each_ablation_removes_or_adds_exactly_one_feature() -> None:
    core = set(feature_columns(FEATURE_SET_CORE))

    assert core - set(feature_columns(FEATURE_SET_NO_CONCURRENCY)) == {
        "concurrent_open_vacancies_count"
    }
    assert core - set(feature_columns(FEATURE_SET_NO_ELAPSED)) == {
        "elapsed_days_since_publication"
    }
    assert set(feature_columns(FEATURE_SET_WITH_STAGE_COUNT)) - core == {"configured_stage_count"}


def test_every_feature_flagged_by_the_15a_audit_is_covered() -> None:
    """La auditoria dejo tres obligaciones; ninguna puede quedarse fuera."""
    covered = set()
    core = set(feature_columns(FEATURE_SET_CORE))
    for feature_set in ABLATION_FEATURE_SETS:
        covered |= core.symmetric_difference(set(feature_columns(feature_set)))

    for feature in ABLATION_REQUIRED_IN_15B:
        assert feature in covered, f"{feature} no se compara en ninguna ablation"


@pytest.fixture(scope="module")
def ablation_report(temporal_split):
    candidate = ModelCandidate(
        "logistic_regression", "C=1.0", {"C": 1.0, "class_weight": None}
    )
    return run_ablations(
        candidate, temporal_split.train, temporal_split.validation, threshold=0.4
    )


def test_ablations_are_evaluated_on_validation(ablation_report) -> None:
    assert ablation_report["evaluated_on"] == "validation"


def test_hyperparameters_are_not_retuned_per_feature_set(ablation_report) -> None:
    """Reajustarlos confundiria el efecto de la feature con otro ajuste."""
    assert ablation_report["hyperparameters_retuned_per_set"] is False


def test_every_set_reports_the_comparable_metrics(ablation_report) -> None:
    for feature_set, entry in ablation_report["results"].items():
        for key in ("average_precision", "recall", "precision", "f2", "brier"):
            assert key in entry, f"{feature_set} no reporta {key}"
        assert entry["n_features"] == len(feature_columns(feature_set))


def test_deltas_are_measured_against_the_core_set(ablation_report) -> None:
    results = ablation_report["results"]
    core_ap = results[FEATURE_SET_CORE]["average_precision"]

    assert results[FEATURE_SET_CORE]["average_precision_delta_vs_core"] == 0.0
    for feature_set, entry in results.items():
        expected = round(entry["average_precision"] - core_ap, 6)
        assert entry["average_precision_delta_vs_core"] == pytest.approx(expected, abs=1e-6)


def test_interpretation_covers_the_three_audited_features(ablation_report) -> None:
    interpretation = ablation_report["interpretation"]

    for feature in (
        "concurrent_open_vacancies_count",
        "elapsed_days_since_publication",
        "configured_stage_count",
    ):
        assert feature in interpretation
        assert "delta=" in interpretation[feature]


def test_experiment_reports_the_ablation_table(experiment_result) -> None:
    payload = experiment_result.to_dict()["ablations"]

    assert set(payload["results"]) == set(ABLATION_FEATURE_SETS)
    assert payload["candidate"]["family"] in {
        "logistic_regression",
        "decision_tree",
        "random_forest",
        "hist_gradient_boosting",
    }
