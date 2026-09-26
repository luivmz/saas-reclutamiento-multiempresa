"""Metricas de evaluacion, comprobadas contra valores calculados a mano."""

from __future__ import annotations

import numpy as np
import pytest

from recruitment_ml.training.evaluation import (
    calibration_report,
    evaluate_predictions,
    metrics_by_group,
)


def test_perfect_separation_yields_perfect_metrics() -> None:
    y_true = np.array([0, 1, 1, 0])
    y_score = np.array([0.1, 0.9, 0.8, 0.2])

    metrics = evaluate_predictions(y_true, y_score, threshold=0.5)

    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0
    assert metrics["f2"] == 1.0
    assert metrics["average_precision"] == 1.0
    assert metrics["roc_auc"] == 1.0
    assert metrics["confusion_matrix"] == {"tn": 2, "fp": 0, "fn": 0, "tp": 2}


def test_confusion_matrix_matches_the_threshold() -> None:
    y_true = np.array([1, 1, 0, 0, 1])
    y_score = np.array([0.9, 0.4, 0.6, 0.1, 0.2])

    metrics = evaluate_predictions(y_true, y_score, threshold=0.5)

    # Predichos positivos: 0.9 (tp) y 0.6 (fp). Negativos: 0.4, 0.1, 0.2.
    assert metrics["confusion_matrix"] == {"tn": 1, "fp": 1, "fn": 2, "tp": 1}
    assert metrics["precision"] == pytest.approx(0.5)
    assert metrics["recall"] == pytest.approx(1 / 3)
    assert metrics["alert_rate"] == pytest.approx(0.4)


def test_f2_weights_recall_more_than_f1() -> None:
    """F2 debe premiar el recall: es la razon de incluirla."""
    y_true = np.array([1, 1, 1, 0, 0, 0])
    high_recall = np.array([0.6, 0.6, 0.6, 0.6, 0.6, 0.1])

    metrics = evaluate_predictions(y_true, high_recall, threshold=0.5)

    assert metrics["recall"] == 1.0
    assert metrics["f2"] > metrics["f1"]


def test_brier_skill_score_is_zero_for_the_reference_predictor() -> None:
    y_true = np.array([1, 0, 1, 0])
    constant = np.full(4, 0.5)

    metrics = evaluate_predictions(y_true, constant, threshold=0.5, reference_rate=0.5)

    assert metrics["brier"] == pytest.approx(0.25)
    assert metrics["brier_skill_score"] == pytest.approx(0.0)


def test_brier_skill_score_is_positive_when_the_model_beats_the_reference() -> None:
    y_true = np.array([1, 1, 0, 0])
    sharp = np.array([0.9, 0.9, 0.1, 0.1])

    metrics = evaluate_predictions(y_true, sharp, threshold=0.5, reference_rate=0.5)

    assert metrics["brier_skill_score"] > 0.5


def test_average_precision_of_a_random_score_approaches_prevalence() -> None:
    rng = np.random.default_rng(20260920)
    y_true = rng.binomial(1, 0.3, size=4000)
    noise = rng.random(4000)

    metrics = evaluate_predictions(y_true, noise, threshold=0.5)

    assert metrics["average_precision"] == pytest.approx(y_true.mean(), abs=0.03)


def test_calibration_report_detects_a_well_calibrated_score() -> None:
    rng = np.random.default_rng(20260920)
    probabilities = rng.uniform(0.05, 0.95, size=8000)
    outcomes = rng.binomial(1, probabilities)

    report = calibration_report(outcomes, probabilities)

    assert report["expected_calibration_error"] < 0.05
    assert len(report["bins"]) > 5
    assert all(bin_["count"] > 0 for bin_ in report["bins"])


def test_calibration_report_detects_a_badly_calibrated_score() -> None:
    """Probabilidades infladas deben producir un error de calibracion grande."""
    rng = np.random.default_rng(7)
    outcomes = rng.binomial(1, 0.2, size=4000)
    inflated = np.full(4000, 0.9)

    report = calibration_report(outcomes, inflated)

    assert report["expected_calibration_error"] > 0.5


def test_group_metrics_skip_groups_that_are_too_small() -> None:
    y_true = np.array([1, 0] * 60)
    y_score = np.linspace(0.01, 0.99, 120)
    groups = np.array(["big"] * 110 + ["tiny"] * 10)

    report = metrics_by_group(y_true, y_score, groups, threshold=0.5, minimum=50)

    assert "average_precision" in report["big"]
    assert "average_precision" not in report["tiny"]
    assert "note" in report["tiny"]


def test_group_metrics_skip_single_class_groups() -> None:
    y_true = np.concatenate([np.ones(60), np.zeros(60)])
    y_score = np.linspace(0.01, 0.99, 120)
    groups = np.array(["positives"] * 60 + ["negatives"] * 60)

    report = metrics_by_group(y_true, y_score, groups, threshold=0.5, minimum=10)

    assert "note" in report["positives"]
    assert "note" in report["negatives"]
