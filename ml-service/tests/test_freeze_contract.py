"""Contrato del freeze: persistencia previa, integridad y reconstrucción.

Responde a los hallazgos MEDIUM-01 y MEDIUM-02 de la auditoría científica:

- el protocolo debe estar **en disco** antes de revelar el test;
- el freeze no puede contener resultados de test;
- `reveal()` no acepta cualquier objeto con `is_frozen=True`;
- el umbral persistido debe reproducir **exactamente** las decisiones.
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from recruitment_ml.training.evaluation import evaluate_predictions
from recruitment_ml.training.freeze import (
    FREEZE_SCHEMA_VERSION,
    ExperimentFreeze,
    FreezeValidationError,
    load_freeze,
    persist_freeze,
    validate_freeze_for_split,
)
from recruitment_ml.training.preprocessing import build_matrix, build_target
from recruitment_ml.training.split import SealedTestSetError, build_temporal_split


# --- estructura y huella del freeze ----------------------------------------


def test_freeze_declares_the_full_protocol(experiment_result) -> None:
    freeze = experiment_result.to_dict()["freeze"]

    for key in (
        "schema_version",
        "experiment_id",
        "seed",
        "dataset_fingerprint",
        "config_fingerprint",
        "split_signature",
        "split_definition",
        "feature_set",
        "features",
        "excluded_features",
        "ablation_feature_sets",
        "preprocessing",
        "model_family",
        "model_params",
        "threshold",
        "threshold_rule",
        "threshold_selection",
        "calibration_decision",
        "validation_metrics",
        "validation_baselines",
        "ablation_conclusions",
        "verdict_rule",
        "known_limitations",
        "frozen_at",
        "freeze_fingerprint",
    ):
        assert key in freeze, key

    assert freeze["schema_version"] == FREEZE_SCHEMA_VERSION
    assert len(freeze["freeze_fingerprint"]) == 64


def test_freeze_contains_no_test_results(experiment_result) -> None:
    """La dependencia va de resultados a protocolo, nunca al revés."""
    freeze = experiment_result.to_dict()["freeze"]

    assert freeze["contains_test_results"] is False

    # Buscar la subcadena "test" seria inutil: `split_definition.ratios.test` es
    # legitima y el propio campo `contains_test_results` la contiene. Lo que se
    # comprueba es que ninguna clave del protocolo aloje metricas del test.
    protocol_keys = set(freeze) - {"contains_test_results", "note"}
    for key in protocol_keys:
        assert not key.startswith("test_"), key
    assert "test_metrics" not in protocol_keys
    assert "metrics" not in protocol_keys

    # Las unicas metricas del freeze son de validation.
    assert set(freeze["validation_baselines"]) == {"dummy_prior", "operational"}
    assert freeze["validation_metrics"]["n"] > 0


def test_freeze_fingerprint_is_reproducible_and_excludes_timestamps(experiment_result) -> None:
    freeze = experiment_result.freeze_object

    assert freeze.is_intact()
    # Cambiar solo el instante de congelación no altera la huella del protocolo.
    moved = replace(freeze, frozen_at="1999-01-01T00:00:00+00:00")
    assert moved.compute_fingerprint() == freeze.compute_fingerprint()


def test_tampering_with_the_protocol_breaks_the_fingerprint(experiment_result) -> None:
    freeze = experiment_result.freeze_object

    tampered = replace(freeze, model_family="random_forest")
    assert not tampered.is_intact()

    retuned = replace(freeze, threshold=freeze.threshold + 0.01)
    assert not retuned.is_intact()


def test_a_tampered_file_is_rejected_on_load(tmp_path: Path, experiment_result) -> None:
    path = tmp_path / "freeze.json"
    persist_freeze(experiment_result.freeze_object, path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["threshold"] = 0.5
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(FreezeValidationError, match="alterado"):
        load_freeze(path)


# --- validación antes de abrir el conjunto de prueba -----------------------


def test_reveal_rejects_an_arbitrary_object_claiming_to_be_frozen(temporal_split) -> None:
    """`is_frozen=True` en un objeto cualquiera ya no basta."""

    class Pretender:
        is_frozen = True
        threshold = 0.5

    with pytest.raises(SealedTestSetError, match="ExperimentFreeze"):
        temporal_split.sealed_test.reveal(Pretender())


def test_reveal_rejects_a_freeze_that_was_never_persisted(experiment_result, training_frame) -> None:
    """El protocolo debe venir de disco: construirlo al vuelo no autoriza nada."""
    split = build_temporal_split(
        training_frame, dataset_fingerprint=experiment_result.dataset["model_ready_fingerprint"]
    )
    in_memory = replace(experiment_result.freeze_object, source_path=None)

    with pytest.raises(SealedTestSetError, match="persistido"):
        split.sealed_test.reveal(in_memory)


def test_reveal_rejects_a_freeze_from_another_dataset(tmp_path: Path, experiment_result, training_frame) -> None:
    split = build_temporal_split(training_frame, dataset_fingerprint="otro-dataset")
    path = tmp_path / "freeze.json"
    persist_freeze(experiment_result.freeze_object, path)

    with pytest.raises(SealedTestSetError, match="otro dataset"):
        split.sealed_test.reveal(load_freeze(path))


def test_reveal_rejects_a_freeze_from_another_split(tmp_path: Path, experiment_result, training_frame) -> None:
    fingerprint = experiment_result.dataset["model_ready_fingerprint"]
    split = build_temporal_split(training_frame, dataset_fingerprint=fingerprint)
    mismatched = replace(experiment_result.freeze_object, split_signature="otra-particion").with_fingerprint()
    path = tmp_path / "freeze.json"
    persist_freeze(mismatched, path)

    with pytest.raises(SealedTestSetError, match="otra particion"):
        split.sealed_test.reveal(load_freeze(path))


def test_incomplete_freeze_is_rejected(experiment_result) -> None:
    empty_features = replace(experiment_result.freeze_object, features=[]).with_fingerprint()

    with pytest.raises(FreezeValidationError, match="features"):
        validate_freeze_for_split(
            empty_features,
            empty_features.dataset_fingerprint,
            empty_features.split_signature,
        )


def test_incompatible_schema_version_is_rejected(experiment_result) -> None:
    old = replace(experiment_result.freeze_object, schema_version="15a.0").with_fingerprint()

    with pytest.raises(FreezeValidationError, match="contrato"):
        validate_freeze_for_split(old, old.dataset_fingerprint, old.split_signature)


# --- reconstrucción desde el artefacto persistido --------------------------


def test_predictions_can_be_rebuilt_from_the_persisted_freeze(
    tmp_path: Path, temporal_split, experiment_result
) -> None:
    """Prueba fuerte: reconstruir el comportamiento, no solo comparar el número.

    Se carga el freeze desde disco, se reconstruye el pipeline con sus
    hiperparámetros, se reentrena sobre train y se aplica el umbral persistido.
    Las métricas de validation deben salir idénticas a las congeladas.
    """
    from recruitment_ml.training.calibration import positive_scores
    from recruitment_ml.training.models import build_pipeline

    path = tmp_path / "freeze.json"
    persist_freeze(experiment_result.freeze_object, path)
    freeze = load_freeze(path)

    train, validation = temporal_split.train, temporal_split.validation
    X_train = build_matrix(train, freeze.feature_set)
    y_train = build_target(train)
    X_validation = build_matrix(validation, freeze.feature_set)
    y_validation = build_target(validation)

    pipeline = build_pipeline(freeze.model_family, freeze.model_params)
    pipeline.fit(X_train, y_train)
    scores = positive_scores(pipeline, X_validation)

    rebuilt = evaluate_predictions(
        y_validation.to_numpy(),
        scores,
        threshold=freeze.threshold,
        reference_rate=float(y_train.mean()),
    )
    frozen = freeze.validation_metrics

    assert rebuilt["confusion_matrix"] == frozen["confusion_matrix"]
    for metric in ("precision", "recall", "f1", "f2", "alert_rate", "average_precision", "brier"):
        assert rebuilt[metric] == pytest.approx(frozen[metric], abs=1e-9), metric


def test_a_rounded_threshold_can_change_a_classification(temporal_split, experiment_result) -> None:
    """El motivo de no redondear: la frontera puede mover una observación."""
    exact = experiment_result.freeze_object.threshold
    rounded = round(exact, 6)

    assert exact != rounded, "el umbral de referencia debe tener más de 6 decimales"

    scores = np.array([rounded, exact, (exact + rounded) / 2.0])
    assert not np.array_equal(scores >= exact, scores >= rounded), (
        "redondear el umbral cambia al menos una clasificación en la frontera"
    )


def test_persisted_threshold_keeps_full_precision(experiment_result, tmp_path: Path) -> None:
    path = tmp_path / "freeze.json"
    persist_freeze(experiment_result.freeze_object, path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["threshold"] == experiment_result.freeze_object.threshold
    assert repr(payload["threshold"]) == repr(experiment_result.freeze_object.threshold)
    # El campo de lectura humana existe pero es sólo presentación.
    assert payload["threshold_display"] == round(experiment_result.freeze_object.threshold, 6)


def test_reported_test_threshold_is_the_exact_frozen_one(experiment_result) -> None:
    payload = experiment_result.to_dict()

    assert payload["test"]["threshold"] == payload["freeze"]["threshold"]
    assert repr(payload["test"]["threshold"]) == repr(experiment_result.freeze_object.threshold)


# --- artefacto de resultados separado --------------------------------------


def test_test_results_reference_the_freeze(experiment_result) -> None:
    results = experiment_result.test_results.to_dict()

    assert results["references_freeze"] is True
    assert results["freeze_fingerprint"] == experiment_result.freeze_object.freeze_fingerprint
    assert results["threshold"] == experiment_result.freeze_object.threshold
    assert "metrics" in results and "verdict" in results
    assert results["limitations"] == experiment_result.freeze_object.known_limitations


def test_cli_writes_freeze_and_results_as_separate_artefacts(tmp_path: Path) -> None:
    from recruitment_ml.training.experiment import main

    evidence = tmp_path / "evidence"
    assert main(["--rows", "800", "--skip-optional-model", "--evidence-dir", str(evidence)]) == 0

    freeze_payload = json.loads(
        (evidence / "phase-15b-experiment-freeze.json").read_text(encoding="utf-8")
    )
    results_payload = json.loads(
        (evidence / "phase-15b-test-results.json").read_text(encoding="utf-8")
    )

    assert freeze_payload["contains_test_results"] is False
    assert results_payload["freeze_fingerprint"] == freeze_payload["freeze_fingerprint"]
    assert "metrics" in results_payload


def test_the_persisted_freeze_is_the_one_that_opened_the_test(tmp_path: Path) -> None:
    """El artefacto versionable debe ser literalmente el que autorizó el reveal."""
    from recruitment_ml.training.experiment import run_experiment

    path = tmp_path / "freeze.json"
    result = run_experiment(rows=800, include_optional_model=False, freeze_path=path)

    assert path.exists()
    on_disk = load_freeze(path)
    assert on_disk.freeze_fingerprint == result.freeze_object.freeze_fingerprint
    assert result.freeze_object.source_path == str(path)
    assert result.to_dict()["split"]["test_reveal_count"] == 1
