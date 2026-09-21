"""Seleccion del umbral operativo.

La regla debe ser reproducible, relativa al baseline y no degenerar en un punto
que alerte sobre casi todo: el plan de evaluacion aprobado advierte contra la
fatiga de alertas.
"""

from __future__ import annotations

import numpy as np
import pytest

from recruitment_ml.training.baselines import OPERATIONAL_D, OPERATIONAL_K, OperationalRule
from recruitment_ml.training.thresholds import (
    RULE_DESCRIPTION,
    precision_recall_table,
    select_threshold,
)


@pytest.fixture(scope="module")
def scored_validation() -> tuple[np.ndarray, np.ndarray]:
    """Puntuaciones sinteticas con senal real pero no perfecta."""
    rng = np.random.default_rng(20260920)
    y = rng.binomial(1, 0.35, size=1200)
    scores = np.clip(0.25 + 0.35 * y + rng.normal(0, 0.22, size=1200), 0.001, 0.999)
    return y, scores


def test_selected_point_dominates_the_operational_baseline(scored_validation) -> None:
    y, scores = scored_validation

    decision = select_threshold(y, scores, precision_floor=0.45, recall_floor=0.35)

    assert decision.floor_satisfied
    assert decision.precision >= 0.45
    assert decision.recall >= 0.35


def test_rule_does_not_degenerate_into_alerting_on_everything(scored_validation) -> None:
    """La regresion que motivo cambiar la regla: maximizar recall sin mas
    llevaba el umbral al minimo admisible y alertaba sobre casi todo."""
    y, scores = scored_validation

    decision = select_threshold(y, scores, precision_floor=0.45, recall_floor=0.35)
    alert_rate = float((scores >= decision.threshold).mean())

    assert alert_rate < 0.95, "el punto elegido marca practicamente todos los procesos"
    assert decision.recall < 1.0 or decision.precision > 0.45


def test_selection_maximises_f2_within_the_eligible_region(scored_validation) -> None:
    from sklearn.metrics import fbeta_score

    y, scores = scored_validation
    decision = select_threshold(y, scores, precision_floor=0.45, recall_floor=0.35)
    chosen_f2 = fbeta_score(y, (scores >= decision.threshold).astype(int), beta=2)

    # Ningun otro umbral elegible puede tener mayor F2.
    for candidate in np.unique(np.round(scores, 3)):
        predictions = (scores >= candidate).astype(int)
        if predictions.sum() == 0:
            continue
        precision = float((y[predictions == 1]).mean())
        recall = float(predictions[y == 1].mean())
        if precision >= 0.45 and recall >= 0.35:
            assert fbeta_score(y, predictions, beta=2) <= chosen_f2 + 1e-6


def test_fallback_is_flagged_when_no_threshold_dominates(scored_validation) -> None:
    y, scores = scored_validation

    decision = select_threshold(y, scores, precision_floor=0.99, recall_floor=0.99)

    assert not decision.floor_satisfied
    assert "respaldo por F2" in decision.rule
    assert 0.0 < decision.threshold < 1.0


def test_selection_is_deterministic(scored_validation) -> None:
    y, scores = scored_validation

    first = select_threshold(y, scores, precision_floor=0.45, recall_floor=0.35)
    second = select_threshold(y, scores, precision_floor=0.45, recall_floor=0.35)

    assert first.threshold == second.threshold
    assert first.to_dict() == second.to_dict()


def test_decision_records_the_rule_and_its_provenance(scored_validation) -> None:
    y, scores = scored_validation

    payload = select_threshold(y, scores, precision_floor=0.45, recall_floor=0.35).to_dict()

    assert payload["selected_on"] == "validation"
    assert payload["rule"] == RULE_DESCRIPTION
    assert payload["candidates_considered"] > 0
    assert payload["eligible_thresholds"] > 0


def test_precision_recall_table_is_small_and_ordered(scored_validation) -> None:
    """Se versiona una tabla reproducible en vez de una figura binaria."""
    y, scores = scored_validation

    table = precision_recall_table(y, scores, points=25)

    assert 0 < len(table) <= 25
    thresholds = [row["threshold"] for row in table]
    assert thresholds == sorted(thresholds)


def test_operational_rule_parameters_are_the_documented_ones() -> None:
    rule = OperationalRule()

    assert (rule.k, rule.d) == (OPERATIONAL_K, OPERATIONAL_D) == (1, 10)
    assert rule.describe()["tuned_on"].startswith("ninguno")


def test_operational_rule_matches_its_formula(temporal_split) -> None:
    frame = temporal_split.validation
    decisions = OperationalRule().decide(frame)

    expected = (
        (
            frame["evaluations_overdue_pending_count"]
            + frame["interviews_overdue_pending_count"]
            >= 1
        )
        | (frame["days_since_last_operational_event"] >= 10)
    ).to_numpy()

    np.testing.assert_array_equal(decisions.astype(bool), expected)


def test_threshold_in_the_experiment_is_selected_on_validation_only(experiment_result) -> None:
    payload = experiment_result.to_dict()

    assert payload["threshold"]["selected_on"] == "validation"
    assert payload["threshold"]["precision_floor"] == pytest.approx(
        payload["baselines"]["operational"]["validation"]["precision"]
    )
    assert payload["threshold"]["recall_floor"] == pytest.approx(
        payload["baselines"]["operational"]["validation"]["recall"]
    )
