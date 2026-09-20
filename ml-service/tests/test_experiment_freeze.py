"""Congelacion del experimento y uso unico del conjunto de prueba.

El freeze es lo que separa una evaluacion honesta de un resultado ajustado a
posteriori: registra la configuracion completa **antes** de mirar el test y es
la llave que abre el conjunto sellado.
"""

from __future__ import annotations

import json

import pytest

from recruitment_ml.training.experiment import (
    VERDICT_CRITERIA,
    VERDICT_GO,
    VERDICT_GO_LIMITED,
    VERDICT_NO_GO,
    ExperimentFreeze,
    main,
)
from recruitment_ml.training.split import SealedTestSetError


def test_freeze_records_everything_needed_to_reproduce(experiment_result) -> None:
    freeze = experiment_result.to_dict()["freeze"]

    for key in (
        "feature_set",
        "features",
        "model_family",
        "model_params",
        "preprocessing",
        "calibrated",
        "threshold",
        "threshold_rule",
        "seed",
        "dataset_fingerprint",
        "config_fingerprint",
        "validation_metrics",
        "ablation_decision",
        "verdict_criteria",
    ):
        assert key in freeze, key

    assert freeze["is_frozen"] is True
    assert freeze["seed"] == 20260920
    assert len(freeze["features"]) == 15


def test_freeze_metrics_come_from_validation_not_test(experiment_result) -> None:
    payload = experiment_result.to_dict()
    freeze_metrics = payload["freeze"]["validation_metrics"]

    assert freeze_metrics["n"] == payload["split"]["validation"]["n"]
    assert freeze_metrics["n"] != payload["test"]["n"] or (
        payload["split"]["validation"]["n"] == payload["test"]["n"]
    )
    assert freeze_metrics["average_precision"] != payload["test"]["average_precision"]


def test_the_test_set_is_opened_exactly_once(experiment_result) -> None:
    payload = experiment_result.to_dict()

    assert payload["split"]["test_reveal_count"] == 1


def test_a_sealed_test_set_refuses_an_unfrozen_record(temporal_split) -> None:
    class Pretender:
        is_frozen = False

    with pytest.raises(SealedTestSetError):
        temporal_split.sealed_test.reveal(Pretender())


def test_a_frozen_record_opens_the_test_set(training_frame) -> None:
    from recruitment_ml.training.split import build_temporal_split

    split = build_temporal_split(training_frame)
    freeze = ExperimentFreeze(
        feature_set="core",
        features=[],
        model_family="logistic_regression",
        model_params={},
        preprocessing="scaler",
        calibrated=False,
        threshold=0.5,
        threshold_rule="regla",
        seed=20260920,
        dataset_fingerprint="x",
        config_fingerprint="y",
        validation_metrics={},
        ablation_decision={},
    )

    assert split.sealed_test.reveal_count == 0
    revealed = split.sealed_test.reveal(freeze)
    assert len(revealed) == len(split.sealed_test)
    assert split.sealed_test.reveal_count == 1


def test_the_threshold_used_on_test_is_the_frozen_one(experiment_result) -> None:
    payload = experiment_result.to_dict()

    assert payload["test"]["threshold"] == payload["freeze"]["threshold"]
    assert payload["test"]["threshold"] == payload["threshold"]["threshold"]


def test_verdict_criteria_are_comparative_not_invented(experiment_result) -> None:
    """La Fase 14 prohibio cifras absolutas de AP, recall o precision."""
    payload = experiment_result.to_dict()
    criteria = payload["freeze"]["verdict_criteria"]

    assert criteria == VERDICT_CRITERIA
    for text in criteria.values():
        # Cada criterio se ancla en una comparacion, no en una cifra objetivo.
        assert any(
            word in text
            for word in ("baseline", "validation", "predictor constante", "tolerancia")
        ), text
    # Ningun criterio puede exigir un desempeno absoluto: la Fase 14 lo prohibio.
    combined = " ".join(criteria.values())
    for forbidden in ("AP >", "AP>=", "recall >", "precision >", "AP superior a 0."):
        assert forbidden not in combined


def test_verdict_is_one_of_the_three_allowed_outcomes(experiment_result) -> None:
    decision = experiment_result.to_dict()["verdict"]["decision"]

    assert decision in {VERDICT_GO, VERDICT_GO_LIMITED, VERDICT_NO_GO}


def test_verdict_evidence_supports_the_decision(experiment_result) -> None:
    verdict = experiment_result.to_dict()["verdict"]
    evidence = verdict["evidence"]

    if verdict["decision"] != VERDICT_NO_GO:
        assert evidence["model_ap_test"] > evidence["dummy_ap_test"]
        assert evidence["model_ap_test"] > evidence["operational_ap_test"]
        assert evidence["brier_skill_score_test"] > 0
    assert verdict["checks"]["beats_dummy"] == (
        evidence["model_ap_test"] > evidence["dummy_ap_test"]
    )


def test_deployment_is_never_declared_while_gap_01_is_open(experiment_result) -> None:
    payload = experiment_result.to_dict()

    assert "GAP-01" in payload["verdict"]["deployment_note"]
    assert "no equivale a desplegable" in payload["validity_notice"]


def test_censoring_limitation_travels_with_the_result(experiment_result) -> None:
    censoring = experiment_result.to_dict()["censoring"]

    assert censoring["excluded_from_supervised_training"] is True
    assert censoring["labels_never_imputed"] is True
    assert "informativa" in censoring["limitation"]


def test_organization_id_is_metadata_only(experiment_result) -> None:
    payload = experiment_result.to_dict()

    assert "organization_id" not in payload["freeze"]["features"]
    assert "nunca entra en X" in payload["organizations"]["note"]
    assert payload["organizations"]["test"]


def test_cli_runs_and_writes_evidence(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "--rows",
            "800",
            "--skip-optional-model",
            "--output-dir",
            str(tmp_path / "artifacts"),
            "--evidence-dir",
            str(tmp_path / "evidence"),
        ]
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "veredicto" in output

    freeze_path = tmp_path / "evidence" / "phase-15b-experiment-freeze.json"
    summary_path = tmp_path / "evidence" / "phase-15b-results-summary.json"
    assert freeze_path.exists() and summary_path.exists()

    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    assert freeze["is_frozen"] is True

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert "verdict" in summary and "test_metrics" in summary
    assert (tmp_path / "artifacts" / "experiment.json").exists()


def test_cli_can_skip_the_optional_model(tmp_path) -> None:
    from recruitment_ml.training.experiment import run_experiment

    reduced = run_experiment(rows=800, include_optional_model=False).to_dict()
    families = {row["family"] for row in reduced["model_selection"]["leaderboard"]}

    assert "hist_gradient_boosting" not in families
    assert reduced["model_selection"]["configurations_evaluated"] == 18
