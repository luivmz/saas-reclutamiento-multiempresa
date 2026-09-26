"""Contrato del freeze: persistencia previa, integridad y reconstrucción.

Responde a los hallazgos MEDIUM-01 y MEDIUM-02 de la auditoría científica:

- el protocolo debe estar **en disco** antes de revelar el test;
- el freeze no puede contener resultados de test;
- `reveal()` no acepta cualquier objeto con `is_frozen=True`;
- el umbral persistido debe reproducir **exactamente** las decisiones.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from recruitment_ml.training.evaluation import evaluate_predictions
from recruitment_ml.schema import ABLATION_REQUIRED_IN_15B
from recruitment_ml.training.freeze import (
    FREEZE_SCHEMA_VERSION,
    REQUIRED_VERDICT_RULE_KEYS,
    ExperimentFreeze,
    FreezeValidationError,
    load_freeze,
    persist_freeze,
    validate_freeze_for_split,
    validate_known_limitations,
)
from recruitment_ml.training.preprocessing import build_matrix, build_target
from recruitment_ml.training.split import SealedTestSetError, build_temporal_split

#: Huella con formato valido que no pertenece a este experimento. Tiene que ser
#: sha256 bien formada: el contrato rechaza cualquier otra cosa por formato, y
#: entonces la prueba no demostraria el fallo de correspondencia que busca.
OTHER_FINGERPRINT = hashlib.sha256(b"otro-experimento").hexdigest()


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


def test_reveal_rejects_a_freeze_that_was_never_persisted(
    experiment_result, training_frame, training_fingerprints
) -> None:
    """El protocolo debe venir de disco: construirlo al vuelo no autoriza nada."""
    split = build_temporal_split(training_frame, **training_fingerprints)
    in_memory = replace(experiment_result.freeze_object, source_path=None)

    with pytest.raises(SealedTestSetError, match="persistido"):
        split.sealed_test.reveal(in_memory)


def test_reveal_rejects_a_freeze_from_another_dataset(
    tmp_path: Path, experiment_result, training_frame, training_fingerprints
) -> None:
    split = build_temporal_split(
        training_frame,
        dataset_fingerprint=OTHER_FINGERPRINT,
        config_fingerprint=training_fingerprints["config_fingerprint"],
    )
    path = tmp_path / "freeze.json"
    persist_freeze(experiment_result.freeze_object, path)

    with pytest.raises(SealedTestSetError, match="otro dataset"):
        split.sealed_test.reveal(load_freeze(path))


def test_reveal_rejects_a_freeze_from_another_split(
    tmp_path: Path, experiment_result, training_frame, training_fingerprints
) -> None:
    split = build_temporal_split(training_frame, **training_fingerprints)
    mismatched = replace(
        experiment_result.freeze_object, split_signature=OTHER_FINGERPRINT
    ).with_fingerprint()
    path = tmp_path / "freeze.json"
    persist_freeze(mismatched, path)

    with pytest.raises(SealedTestSetError, match="otra particion"):
        split.sealed_test.reveal(load_freeze(path))


def test_incomplete_freeze_is_rejected(tmp_path: Path, experiment_result) -> None:
    """Sin features declaradas el protocolo no documenta el experimento."""
    empty_features = replace(experiment_result.freeze_object, features=[]).with_fingerprint()
    persist_freeze(empty_features, tmp_path / "freeze.json")
    loaded = load_freeze(tmp_path / "freeze.json")

    with pytest.raises(FreezeValidationError, match="features"):
        validate_freeze_for_split(
            loaded,
            dataset_fingerprint=loaded.dataset_fingerprint,
            split_signature=loaded.split_signature,
            config_fingerprint=loaded.config_fingerprint,
        )


def test_incompatible_schema_version_is_rejected(tmp_path: Path, experiment_result) -> None:
    old = replace(experiment_result.freeze_object, schema_version="15a.0").with_fingerprint()
    path = persist_freeze(old, tmp_path / "freeze.json")

    with pytest.raises(FreezeValidationError, match="contrato"):
        validate_freeze_for_split(
            ExperimentFreeze.from_dict(
                __import__("json").loads(path.read_text(encoding="utf-8")), source_path=str(path)
            ),
            dataset_fingerprint=old.dataset_fingerprint,
            split_signature=old.split_signature,
            config_fingerprint=old.config_fingerprint,
        )


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


# --- huecos residuales cerrados en la correccion final ---------------------
#
# Codex verifico que `validate_freeze_for_split` todavia aceptaba un freeze con
# config_fingerprint incorrecto, con source_path inexistente y con secciones
# cientificas vacias. Cada caso se prueba ahora **a nivel del flujo real de
# reveal**, no solo llamando al validador.


@pytest.fixture
def aligned_split(training_frame, experiment_result):
    """Particion alineada con el freeze de referencia: el caso que SI funciona."""
    freeze = experiment_result.freeze_object
    split = build_temporal_split(
        training_frame,
        dataset_fingerprint=freeze.dataset_fingerprint,
        config_fingerprint=freeze.config_fingerprint,
    )
    return split, replace(freeze, split_signature=split.signature).with_fingerprint()


def _gutted(freeze, **fields):
    """Freeze internamente coherente pero con una seccion degradada."""
    return replace(freeze, **fields).with_fingerprint()


def test_an_aligned_and_persisted_freeze_is_accepted(tmp_path: Path, aligned_split) -> None:
    """Control positivo: sin el, las pruebas negativas no demuestran nada."""
    split, freeze = aligned_split
    path = persist_freeze(freeze, tmp_path / "freeze.json")

    revealed = split.sealed_test.reveal(load_freeze(path))

    assert len(revealed) == len(split.sealed_test)
    assert split.sealed_test.reveal_count == 1


def test_reveal_rejects_a_wrong_config_fingerprint(tmp_path: Path, aligned_split) -> None:
    """La huella interna se regenera: no basta con la deteccion de manipulacion.

    El freeze es internamente coherente e integro; lo que falla es que no
    pertenece a la configuracion del generador que produjo esta particion.
    """
    split, freeze = aligned_split
    wrong = replace(freeze, config_fingerprint=OTHER_FINGERPRINT).with_fingerprint()
    assert wrong.is_intact(), "la huella debe regenerarse para aislar el fallo de config"
    path = persist_freeze(wrong, tmp_path / "freeze.json")

    with pytest.raises(SealedTestSetError, match="otra configuracion"):
        split.sealed_test.reveal(load_freeze(path))
    assert split.sealed_test.reveal_count == 0


def test_reveal_rejects_a_nonexistent_source_path(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    phantom = replace(freeze, source_path=str(tmp_path / "no-existe.json"))

    with pytest.raises(SealedTestSetError, match="no existe"):
        split.sealed_test.reveal(phantom)
    assert split.sealed_test.reveal_count == 0


def test_reveal_rejects_a_source_path_pointing_to_a_directory(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    directory = tmp_path / "carpeta"
    directory.mkdir()
    as_directory = replace(freeze, source_path=str(directory))

    with pytest.raises(SealedTestSetError, match="no es un archivo regular"):
        split.sealed_test.reveal(as_directory)
    assert split.sealed_test.reveal_count == 0


def test_reveal_rejects_a_source_path_holding_a_different_freeze(
    tmp_path: Path, aligned_split
) -> None:
    """La ruta existe y es legible, pero contiene otro protocolo."""
    split, freeze = aligned_split
    other = replace(freeze, experiment_id="otro-experimento").with_fingerprint()
    decoy = persist_freeze(other, tmp_path / "otro.json")
    mismatched = replace(freeze, source_path=str(decoy))

    with pytest.raises(SealedTestSetError, match="un freeze distinto"):
        split.sealed_test.reveal(mismatched)
    assert split.sealed_test.reveal_count == 0


def test_reveal_rejects_a_tampered_source_file(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    path = persist_freeze(freeze, tmp_path / "freeze.json")
    loaded = load_freeze(path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["model_family"] = "random_forest"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SealedTestSetError, match="alterado"):
        split.sealed_test.reveal(loaded)
    assert split.sealed_test.reveal_count == 0


@pytest.mark.parametrize(
    "section",
    [
        "threshold_selection",
        "calibration_decision",
        "validation_metrics",
        "validation_baselines",
        "ablation_conclusions",
        "verdict_rule",
        "known_limitations",
    ],
)
def test_reveal_rejects_an_empty_scientific_section(
    tmp_path: Path, aligned_split, section: str
) -> None:
    """Que la clave exista no basta: un protocolo vacio no documenta nada."""
    split, freeze = aligned_split
    empty = [] if section == "known_limitations" else {}
    gutted = replace(freeze, **{section: empty}).with_fingerprint()
    path = persist_freeze(gutted, tmp_path / "freeze.json")

    with pytest.raises(SealedTestSetError, match=f"seccion cientifica vacia.*{section}"):
        split.sealed_test.reveal(load_freeze(path))
    assert split.sealed_test.reveal_count == 0


def test_reveal_rejects_validation_metrics_without_the_primary_metric(
    tmp_path: Path, aligned_split
) -> None:
    split, freeze = aligned_split
    without_ap = {k: v for k, v in freeze.validation_metrics.items() if k != "average_precision"}
    gutted = replace(freeze, validation_metrics=without_ap).with_fingerprint()
    path = persist_freeze(gutted, tmp_path / "freeze.json")

    with pytest.raises(SealedTestSetError, match="metrica primaria"):
        split.sealed_test.reveal(load_freeze(path))


@pytest.mark.parametrize(
    "field_name", ["feature_set", "model_family", "threshold_rule", "preprocessing", "experiment_id"]
)
def test_reveal_rejects_an_empty_scalar_field(
    tmp_path: Path, aligned_split, field_name: str
) -> None:
    split, freeze = aligned_split
    gutted = replace(freeze, **{field_name: ""}).with_fingerprint()
    path = persist_freeze(gutted, tmp_path / "freeze.json")

    with pytest.raises(SealedTestSetError, match=f"{field_name} vacio"):
        split.sealed_test.reveal(load_freeze(path))


def test_reveal_rejects_an_out_of_range_threshold(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    invalid = replace(freeze, threshold=1.5).with_fingerprint()
    path = persist_freeze(invalid, tmp_path / "freeze.json")

    with pytest.raises(SealedTestSetError, match="rango valido"):
        split.sealed_test.reveal(load_freeze(path))

# --- validacion semantica de las secciones cientificas ---------------------
#
# Codex verifico que un diccionario con contenido arbitrario -- el caso limite
# es `{"placeholder": true}` -- pasaba la comprobacion de "no vacio" y abria el
# test. Cada seccion tiene ahora un contrato propio, y se prueba a nivel del
# flujo real de reveal, no llamando al validador por separado.

PLACEHOLDER = {"placeholder": True}


def _reveal_must_fail(split, freeze, tmp_path: Path, message: str) -> None:
    """Persiste el freeze degradado y comprueba que no abre el test."""
    path = persist_freeze(freeze, tmp_path / "freeze.json")
    with pytest.raises(SealedTestSetError, match=message):
        split.sealed_test.reveal(load_freeze(path))
    assert split.sealed_test.reveal_count == 0


# threshold_selection ------------------------------------------------------


def test_reveal_rejects_a_placeholder_threshold_selection(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, threshold_selection=dict(PLACEHOLDER)),
        tmp_path,
        "threshold_selection no documenta threshold",
    )


def test_reveal_rejects_a_threshold_selection_without_the_threshold(
    tmp_path: Path, aligned_split
) -> None:
    split, freeze = aligned_split
    without = {k: v for k, v in freeze.threshold_selection.items() if k != "threshold"}
    _reveal_must_fail(
        split,
        _gutted(freeze, threshold_selection=without),
        tmp_path,
        "threshold_selection no documenta threshold",
    )


def test_reveal_rejects_a_threshold_selection_with_a_different_threshold(
    tmp_path: Path, aligned_split
) -> None:
    """Documentar un umbral distinto del congelado rompe la trazabilidad."""
    split, freeze = aligned_split
    shifted = dict(freeze.threshold_selection)
    shifted["threshold"] = float(freeze.threshold) + 0.01
    _reveal_must_fail(
        split,
        _gutted(freeze, threshold_selection=shifted),
        tmp_path,
        "no coincide con el umbral congelado",
    )


def test_reveal_rejects_a_threshold_chosen_on_test(tmp_path: Path, aligned_split) -> None:
    """Elegir el umbral con el holdout seria la contaminacion que 15B evita."""
    split, freeze = aligned_split
    leaked = dict(freeze.threshold_selection)
    leaked["selected_on"] = "test"
    _reveal_must_fail(
        split,
        _gutted(freeze, threshold_selection=leaked),
        tmp_path,
        "declara el test como fuente de seleccion",
    )


def test_reveal_rejects_a_threshold_selection_without_a_rule(
    tmp_path: Path, aligned_split
) -> None:
    split, freeze = aligned_split
    ruleless = dict(freeze.threshold_selection)
    ruleless["rule"] = "   "
    _reveal_must_fail(
        split,
        _gutted(freeze, threshold_selection=ruleless),
        tmp_path,
        "threshold_selection.rule",
    )


# calibration_decision -----------------------------------------------------


def test_reveal_rejects_a_placeholder_calibration_decision(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, calibration_decision=dict(PLACEHOLDER)),
        tmp_path,
        "adopt_calibration debe ser booleano",
    )


@pytest.mark.parametrize(
    "missing", ["method", "decision_rule", "fitted_on", "brier_calibrated", "ece_uncalibrated"]
)
def test_reveal_rejects_an_incomplete_calibration_decision(
    tmp_path: Path, aligned_split, missing: str
) -> None:
    split, freeze = aligned_split
    incomplete = {k: v for k, v in freeze.calibration_decision.items() if k != missing}
    _reveal_must_fail(
        split,
        _gutted(freeze, calibration_decision=incomplete),
        tmp_path,
        f"calibration_decision.*{missing}",
    )


def test_reveal_rejects_a_calibration_fitted_outside_train(tmp_path: Path, aligned_split) -> None:
    """Ajustarla con validation contaminaria la eleccion del umbral."""
    split, freeze = aligned_split
    leaked = dict(freeze.calibration_decision)
    leaked["fitted_on"] = "validation"
    _reveal_must_fail(
        split,
        _gutted(freeze, calibration_decision=leaked),
        tmp_path,
        "fitted_on debe declarar",
    )


def test_the_official_freeze_does_not_adopt_calibration(experiment_result) -> None:
    """El modelo final no adopta calibracion, y el protocolo lo refleja."""
    decision = experiment_result.freeze_object.calibration_decision

    assert decision["adopt_calibration"] is False
    assert decision["method"] == "sigmoid"
    assert "train" in decision["fitted_on"]


# validation_metrics -------------------------------------------------------


def test_reveal_rejects_a_placeholder_validation_metrics(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=dict(PLACEHOLDER)),
        tmp_path,
        "metrica primaria",
    )


def test_reveal_rejects_validation_metrics_with_only_the_primary_metric(
    tmp_path: Path, aligned_split
) -> None:
    """AP sola no describe el punto de operacion que el test debe reproducir."""
    split, freeze = aligned_split
    only_ap = {"average_precision": freeze.validation_metrics["average_precision"]}
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=only_ap),
        tmp_path,
        "validation_metrics no documenta",
    )


@pytest.mark.parametrize(
    "metric",
    ["roc_auc", "precision", "recall", "f1", "f2", "balanced_accuracy", "brier", "alert_rate"],
)
def test_reveal_rejects_validation_metrics_missing_a_metric(
    tmp_path: Path, aligned_split, metric: str
) -> None:
    split, freeze = aligned_split
    incomplete = {k: v for k, v in freeze.validation_metrics.items() if k != metric}
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=incomplete),
        tmp_path,
        f"validation_metrics no documenta {metric}",
    )


def test_reveal_rejects_a_nan_validation_metric(tmp_path: Path, aligned_split) -> None:
    """NaN sobrevive al JSON, pero no es una metrica: es una comparacion imposible."""
    split, freeze = aligned_split
    broken = dict(freeze.validation_metrics)
    broken["recall"] = float("nan")
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=broken),
        tmp_path,
        "no es un numero finito",
    )


def test_reveal_rejects_validation_metrics_computed_with_another_threshold(
    tmp_path: Path, aligned_split
) -> None:
    split, freeze = aligned_split
    shifted = dict(freeze.validation_metrics)
    shifted["threshold"] = float(freeze.threshold) + 0.05
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=shifted),
        tmp_path,
        "se calcularon con otro umbral",
    )


def test_reveal_rejects_a_broken_confusion_matrix(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    broken = dict(freeze.validation_metrics)
    broken["confusion_matrix"] = dict(broken["confusion_matrix"], tp="muchos")
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=broken),
        tmp_path,
        "no es un conteo entero",
    )


# validation_baselines -----------------------------------------------------


def test_reveal_rejects_placeholder_validation_baselines(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_baselines=dict(PLACEHOLDER)),
        tmp_path,
        "no documenta el baseline",
    )


@pytest.mark.parametrize("baseline", ["dummy_prior", "operational"])
def test_reveal_rejects_validation_baselines_missing_one(
    tmp_path: Path, aligned_split, baseline: str
) -> None:
    """El veredicto es comparativo: sin los dos baselines no hay con que comparar."""
    split, freeze = aligned_split
    incomplete = {k: v for k, v in freeze.validation_baselines.items() if k != baseline}
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_baselines=incomplete),
        tmp_path,
        f"no documenta el baseline {baseline}",
    )


def test_reveal_rejects_a_baseline_without_its_metrics(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    hollow = dict(freeze.validation_baselines)
    hollow["operational"] = {"nota": "pendiente"}
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_baselines=hollow),
        tmp_path,
        "validation_baselines.operational no documenta",
    )


# ablation_conclusions -----------------------------------------------------


def test_reveal_rejects_placeholder_ablation_conclusions(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, ablation_conclusions=dict(PLACEHOLDER)),
        tmp_path,
        "ablation_conclusions no documenta",
    )


@pytest.mark.parametrize("feature", list(ABLATION_REQUIRED_IN_15B))
def test_reveal_rejects_ablation_conclusions_missing_a_required_feature(
    tmp_path: Path, aligned_split, feature: str
) -> None:
    """Las tres features senaladas por la auditoria de 15A no son opcionales."""
    split, freeze = aligned_split
    incomplete = {k: v for k, v in freeze.ablation_conclusions.items() if k != feature}
    _reveal_must_fail(
        split,
        _gutted(freeze, ablation_conclusions=incomplete),
        tmp_path,
        f"ablation_conclusions no documenta {feature}",
    )


def test_reveal_rejects_an_ablation_reading_without_a_number(
    tmp_path: Path, aligned_split
) -> None:
    """Una lectura sin cifra no es una conclusion verificable."""
    split, freeze = aligned_split
    vague = dict(freeze.ablation_conclusions)
    vague["concurrent_open_vacancies_count"] = "sin cambios relevantes"
    _reveal_must_fail(
        split,
        _gutted(freeze, ablation_conclusions=vague),
        tmp_path,
        "no reporta ninguna diferencia medible",
    )


# verdict_rule -------------------------------------------------------------


def test_reveal_rejects_a_placeholder_verdict_rule(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, verdict_rule=dict(PLACEHOLDER)),
        tmp_path,
        "verdict_rule",
    )


@pytest.mark.parametrize("key", list(REQUIRED_VERDICT_RULE_KEYS))
def test_reveal_rejects_a_verdict_rule_missing_a_criterion(
    tmp_path: Path, aligned_split, key: str
) -> None:
    """Un veredicto cuya regla no estaba declarada antes no significa nada."""
    split, freeze = aligned_split
    incomplete = {k: v for k, v in freeze.verdict_rule.items() if k != key}
    _reveal_must_fail(
        split,
        _gutted(freeze, verdict_rule=incomplete),
        tmp_path,
        f"verdict_rule.{key}",
    )


def test_the_official_verdict_rule_blocks_deployment_while_gap_01_is_open(
    experiment_result,
) -> None:
    rule = experiment_result.freeze_object.verdict_rule

    assert "GAP-01" in rule["not_deployable_while_gap_01_open"]
    assert "GO CON LIMITACIONES" in rule["limitations_downgrade_the_verdict"]


# known_limitations --------------------------------------------------------


@pytest.mark.parametrize("limitations", [[""], ["   "], ["texto valido", "  "]])
def test_reveal_rejects_blank_known_limitations(
    tmp_path: Path, aligned_split, limitations: list[str]
) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, known_limitations=limitations),
        tmp_path,
        "esta vacia o no es texto",
    )


@pytest.mark.parametrize(
    ("marker", "topic"),
    [
        ("sintetic", "datos sinteticos"),
        ("tasa de alerta", "tasa de alerta"),
        ("heterogeneidad", "heterogeneidad entre organizaciones"),
        ("concurrent_open_vacancies_count", "concurrency como posible proxy temporal"),
        ("censura", "censura informativa"),
        ("colinealidad", "colinealidad"),
        ("contaminacion", "contaminacion procedimental"),
        ("GAP-01", "GAP-01 / no desplegable"),
    ],
)
def test_reveal_rejects_known_limitations_missing_a_key_topic(
    tmp_path: Path, aligned_split, marker: str, topic: str
) -> None:
    """Se comprueba la cobertura tematica, no la redaccion exacta."""
    split, freeze = aligned_split
    survivors = [item for item in freeze.known_limitations if marker.lower() not in item.lower()]
    assert len(survivors) < len(freeze.known_limitations), f"{marker} no aparece en el freeze"
    _reveal_must_fail(
        split,
        _gutted(freeze, known_limitations=survivors),
        tmp_path,
        f"no cubre limitaciones conocidas del experimento: {topic}",
    )


def test_the_official_freeze_covers_every_required_limitation(experiment_result) -> None:
    """Control positivo de la cobertura: el protocolo real las declara todas."""
    validate_known_limitations(experiment_result.freeze_object)

    text = " | ".join(experiment_result.freeze_object.known_limitations).lower()
    for marker in ("sintetic", "tasa de alerta", "censura", "colinealidad", "gap-01"):
        assert marker in text


# caso positivo despues de endurecer el contrato ---------------------------


def test_the_official_freeze_still_passes_every_section_validator(
    tmp_path: Path, aligned_split
) -> None:
    """Sin esto, las pruebas negativas solo demostrarian que todo se rechaza."""
    split, freeze = aligned_split
    path = persist_freeze(freeze, tmp_path / "freeze.json")
    loaded = load_freeze(path)

    validated = validate_freeze_for_split(
        loaded,
        dataset_fingerprint=split.sealed_test.dataset_fingerprint,
        split_signature=split.signature,
        config_fingerprint=split.sealed_test.config_fingerprint,
    )

    assert validated.freeze_fingerprint == freeze.freeze_fingerprint
    assert len(split.sealed_test.reveal(loaded)) == len(split.sealed_test)


def test_validate_freeze_for_split_requires_the_config_fingerprint(
    tmp_path: Path, aligned_split
) -> None:
    """Omitir el argumento ya no es posible: dejo de tener valor por defecto."""
    split, freeze = aligned_split
    path = persist_freeze(freeze, tmp_path / "freeze.json")
    loaded = load_freeze(path)

    with pytest.raises(TypeError, match="config_fingerprint"):
        validate_freeze_for_split(
            loaded,
            dataset_fingerprint=split.sealed_test.dataset_fingerprint,
            split_signature=split.signature,
        )


@pytest.mark.parametrize("invalid", ["", "   ", "no-es-una-huella", None])
def test_validate_freeze_for_split_rejects_an_invalid_config_fingerprint(
    tmp_path: Path, aligned_split, invalid
) -> None:
    split, freeze = aligned_split
    path = persist_freeze(freeze, tmp_path / "freeze.json")
    loaded = load_freeze(path)

    with pytest.raises(FreezeValidationError, match="config_fingerprint"):
        validate_freeze_for_split(
            loaded,
            dataset_fingerprint=split.sealed_test.dataset_fingerprint,
            split_signature=split.signature,
            config_fingerprint=invalid,
        )


# --- ramas restantes del contrato -----------------------------------------
#
# Reglas que ninguna prueba anterior ejercitaba. Son contrato real: si no se
# prueban, nadie sabria que dejaron de aplicarse.


def _validated(split, freeze):
    return validate_freeze_for_split(
        freeze,
        dataset_fingerprint=split.sealed_test.dataset_fingerprint,
        split_signature=split.signature,
        config_fingerprint=split.sealed_test.config_fingerprint,
    )


def test_reveal_rejects_a_threshold_selection_without_validation_as_source(
    tmp_path: Path, aligned_split
) -> None:
    """Ni test ni una fuente indefinida: el umbral se elige con validation."""
    split, freeze = aligned_split
    vague = dict(freeze.threshold_selection)
    vague["selected_on"] = "conjunto de desarrollo"
    _reveal_must_fail(
        split,
        _gutted(freeze, threshold_selection=vague),
        tmp_path,
        "debe declarar validation como fuente",
    )


def test_reveal_rejects_a_freeze_that_adopts_calibration(tmp_path: Path, aligned_split) -> None:
    """El protocolo de 15B es el del modelo sin calibrar.

    Declarar `adopt_calibration=True` describe otro modelo, distinto del que
    produjo las metricas congeladas, aunque el metodo sea uno conocido y el
    freeze sea internamente integro.
    """
    split, freeze = aligned_split
    calibrated = dict(freeze.calibration_decision, adopt_calibration=True, method="sigmoid")
    adopting = _gutted(freeze, calibration_decision=calibrated)

    assert adopting.is_intact(), "la huella debe regenerarse para aislar el fallo de calibracion"
    _reveal_must_fail(split, adopting, tmp_path, "modelo sin calibrar")


@pytest.mark.parametrize("method", ["sigmoid", "isotonic", "a-ojo"])
def test_no_calibration_method_rescues_an_adopting_freeze(
    tmp_path: Path, aligned_split, method: str
) -> None:
    split, freeze = aligned_split
    calibrated = dict(freeze.calibration_decision, adopt_calibration=True, method=method)
    _reveal_must_fail(
        split,
        _gutted(freeze, calibration_decision=calibrated),
        tmp_path,
        "modelo sin calibrar",
    )


def test_reveal_rejects_a_calibration_decision_incoherent_with_the_pipeline(
    tmp_path: Path, aligned_split
) -> None:
    """El protocolo no puede decir que no calibra y describir un modelo calibrado."""
    split, freeze = aligned_split
    contradictory = _gutted(
        freeze, preprocessing="StandardScaler y salida calibrada con sigmoid"
    )
    _reveal_must_fail(
        split,
        contradictory,
        tmp_path,
        "el preprocesamiento declara una",
    )


def test_reveal_rejects_a_section_that_is_not_an_object(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=["average_precision", 0.75]),
        tmp_path,
        "debe ser un objeto con contenido",
    )


def test_reveal_rejects_a_metric_that_is_not_numeric(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    textual = dict(freeze.validation_metrics, recall="alto")
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=textual),
        tmp_path,
        "no es un valor numerico",
    )


def test_reveal_rejects_known_limitations_that_are_not_a_list(
    tmp_path: Path, aligned_split
) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, known_limitations={"limitacion": "una sola"}),
        tmp_path,
        "known_limitations debe ser una lista",
    )


def test_reveal_rejects_a_freeze_without_model_params(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, model_params=None),
        tmp_path,
        "model_params ausente",
    )


def test_an_unfrozen_record_is_rejected(aligned_split) -> None:
    """`is_frozen=False` describe un protocolo todavia abierto."""
    split, freeze = aligned_split

    with pytest.raises(FreezeValidationError, match="no esta congelado"):
        _validated(split, _gutted(freeze, is_frozen=False))


def test_a_stale_fingerprint_is_rejected(aligned_split) -> None:
    """Modificar el contenido sin recalcular la huella es la deteccion basica."""
    split, freeze = aligned_split
    stale = replace(freeze, model_family="random_forest")

    assert not stale.is_intact()
    with pytest.raises(FreezeValidationError, match="no coincide con su contenido"):
        _validated(split, stale)


def test_reveal_rejects_an_infinite_validation_metric(tmp_path: Path, aligned_split) -> None:
    """Infinity tambien sobrevive al JSON, y tampoco es una metrica comparable."""
    split, freeze = aligned_split
    broken = dict(freeze.validation_metrics, brier=float("inf"))
    _reveal_must_fail(
        split,
        _gutted(freeze, validation_metrics=broken),
        tmp_path,
        "no es un numero finito",
    )


def test_reveal_rejects_a_non_string_limitation(tmp_path: Path, aligned_split) -> None:
    split, freeze = aligned_split
    _reveal_must_fail(
        split,
        _gutted(freeze, known_limitations=[42]),
        tmp_path,
        "esta vacia o no es texto",
    )


def test_reveal_rejects_a_freeze_without_the_concurrency_proxy_limitation(
    tmp_path: Path, aligned_split
) -> None:
    """La ablation de 15A la senalo: no puede desaparecer del protocolo.

    `concurrent_open_vacancies_count` correlaciona con el calendario, asi que
    puede estar midiendo el paso del tiempo y no carga operativa. Un freeze que
    calle ese riesgo no documenta el experimento.
    """
    split, freeze = aligned_split
    survivors = [
        item
        for item in freeze.known_limitations
        if "concurrent_open_vacancies_count" not in item and "proxy temporal" not in item
    ]
    assert len(survivors) == len(freeze.known_limitations) - 1

    without = _gutted(freeze, known_limitations=survivors)
    assert without.is_intact(), "la huella debe regenerarse para aislar el fallo de cobertura"
    _reveal_must_fail(split, without, tmp_path, "concurrency como posible proxy temporal")
