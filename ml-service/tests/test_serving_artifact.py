"""Artefacto servido: construccion reproducible y carga verificada.

La Fase 15B no versiono binarios. Servir un modelo obliga a tener uno, y la
unica forma honesta de tenerlo es **derivarlo del protocolo congelado** y
comprobar que lo que se carga es efectivamente eso.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pytest

from recruitment_ml.serving.build_artifact import ArtifactBuildError, build
from recruitment_ml.serving.loader import ArtifactUnavailableError, load_predictor
from recruitment_ml.serving.metadata import (
    ARTIFACT_SCHEMA_VERSION,
    DEPLOYMENT_STATUS,
    VERDICT,
    ArtifactMetadata,
    ServiceMetadata,
    library_versions,
)
from recruitment_ml.serving.paths import artifact_path, metadata_path
from recruitment_ml.serving.predictor import PredictionError
from recruitment_ml.training.freeze import load_freeze


# --- construccion ----------------------------------------------------------


def test_the_artifact_is_derived_from_the_frozen_protocol(built_artifact) -> None:
    """Nada se elige aqui: familia, hiperparametros y umbral vienen del freeze."""
    directory, metadata, freeze = built_artifact

    assert metadata.freeze_fingerprint == freeze.freeze_fingerprint
    assert metadata.model_family == freeze.model_family
    assert metadata.model_params == freeze.model_params
    assert metadata.threshold == freeze.threshold
    assert metadata.feature_set == freeze.feature_set
    assert metadata.feature_order == list(freeze.features)
    assert metadata.dataset_fingerprint == freeze.dataset_fingerprint
    assert metadata.config_fingerprint == freeze.config_fingerprint


def test_the_artifact_and_its_metadata_are_written(built_artifact) -> None:
    directory, metadata, _ = built_artifact

    assert artifact_path(directory).is_file()
    assert metadata_path(directory).is_file()
    assert metadata.schema_version == ARTIFACT_SCHEMA_VERSION
    assert metadata.n_train > 0


def test_the_artifact_is_fitted_only_on_train(built_artifact) -> None:
    """El conjunto de prueba no se abre para servir un modelo."""
    directory, metadata, freeze = built_artifact

    definition = freeze.split_definition
    assert metadata.n_train == definition["n_train"]
    assert metadata.n_train < definition["boundaries"]["total_rows"]


def test_metadata_records_the_library_versions(built_artifact) -> None:
    """Un artefacto serializado por otra version puede comportarse distinto."""
    _, metadata, _ = built_artifact

    for library in ("python", "scikit-learn", "numpy", "pandas", "joblib"):
        assert metadata.library_versions[library]
    assert metadata.library_versions == library_versions()


def test_building_with_the_wrong_row_count_is_rejected(tmp_path: Path, freeze_path) -> None:
    """Otro tamano de dataset produce otro modelo, aunque se le parezca."""
    with pytest.raises(ArtifactBuildError, match="no corresponde al experimento"):
        build(freeze_path=freeze_path, output_dir=tmp_path, rows=1_000)


def test_building_from_a_tampered_freeze_is_rejected(tmp_path: Path, freeze_path) -> None:
    payload = json.loads(Path(freeze_path).read_text(encoding="utf-8"))
    payload["model_family"] = "random_forest"
    tampered = tmp_path / "freeze.json"
    tampered.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(Exception, match="alterado"):
        build(freeze_path=tampered, output_dir=tmp_path, rows=6_000)


# --- metadatos -------------------------------------------------------------


def test_metadata_round_trips_through_disk(built_artifact) -> None:
    directory, metadata, _ = built_artifact

    assert ArtifactMetadata.read(metadata_path(directory)) == metadata


def test_metadata_keeps_the_exact_threshold(built_artifact) -> None:
    """El campo de lectura humana existe, pero no sustituye al valor exacto."""
    directory, metadata, _ = built_artifact
    payload = json.loads(metadata_path(directory).read_text(encoding="utf-8"))

    assert payload["threshold"] == metadata.threshold
    assert repr(payload["threshold"]) == repr(metadata.threshold)
    assert payload["threshold_display"] == round(metadata.threshold, 6)


def test_metadata_with_unknown_fields_is_rejected(built_artifact) -> None:
    directory, metadata, _ = built_artifact
    payload = dict(metadata.to_dict(), sorpresa=1)

    with pytest.raises(ValueError, match="campos desconocidos"):
        ArtifactMetadata.from_dict(payload)


def test_incomplete_metadata_is_rejected(built_artifact) -> None:
    _, metadata, _ = built_artifact
    payload = {k: v for k, v in metadata.to_dict().items() if k != "feature_order"}

    with pytest.raises(ValueError, match="incompletos"):
        ArtifactMetadata.from_dict(payload)


def test_service_metadata_states_the_limits(built_artifact) -> None:
    """Lo que el servicio publica no puede suavizar el veredicto de 15B."""
    _, metadata, _ = built_artifact
    service = ServiceMetadata.from_artifact(metadata)

    assert service.verdict == VERDICT == "PREDICTIVE GO WITH LIMITATIONS"
    assert service.deployment_status == DEPLOYMENT_STATUS == "experimental"
    assert service.gap_01_open is True
    assert "GAP-01" in service.gap_01_note
    assert "no evalua" in service.risk_score_meaning.lower()
    assert "revision humana" in service.risk_flag_meaning.lower()


def test_service_metadata_exposes_no_local_paths(built_artifact) -> None:
    _, metadata, _ = built_artifact
    payload = json.dumps(ServiceMetadata.from_artifact(metadata).to_dict())

    for leak in ("artifacts", ".joblib", "C:\\\\", "/home/", "built_at", "n_train"):
        assert leak not in payload


# --- carga verificada ------------------------------------------------------


def test_a_valid_artifact_loads(built_artifact, freeze_path) -> None:
    directory, metadata, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)

    assert predictor.metadata == metadata
    assert predictor.feature_order == metadata.feature_order
    assert predictor.threshold == metadata.threshold


def test_a_missing_artifact_is_reported(tmp_path: Path, freeze_path) -> None:
    with pytest.raises(ArtifactUnavailableError, match="no hay artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_an_artifact_without_metadata_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """Sin metadatos no puede saberse de que experimento salio el binario."""
    directory, _, _ = built_artifact
    joblib.dump(joblib.load(artifact_path(directory)), artifact_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="no trae metadatos"):
        load_predictor(tmp_path, freeze_path=freeze_path)


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("freeze_fingerprint", "0" * 64, "freeze_fingerprint"),
        ("model_family", "random_forest", "model_family"),
        ("experiment_id", "otro-experimento", "experiment_id"),
        ("dataset_fingerprint", "0" * 64, "dataset_fingerprint"),
    ],
)
def test_an_artifact_that_does_not_match_the_freeze_is_rejected(
    tmp_path: Path, built_artifact, freeze_path, field_name: str, value: str, message: str
) -> None:
    directory, metadata, _ = built_artifact
    joblib.dump(joblib.load(artifact_path(directory)), artifact_path(tmp_path))
    payload = dict(metadata.to_dict(), **{field_name: value})
    payload.pop("threshold_display", None)
    ArtifactMetadata.from_dict(payload).write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match=message):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_threshold_mismatch_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """Otro umbral clasifica distinto: no es el modelo que 15B aprobo."""
    directory, metadata, _ = built_artifact
    joblib.dump(joblib.load(artifact_path(directory)), artifact_path(tmp_path))
    payload = dict(metadata.to_dict(), threshold=0.5)
    payload.pop("threshold_display", None)
    ArtifactMetadata.from_dict(payload).write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="umbral del artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_feature_order_mismatch_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """El orden importa: la matriz dejaria de ser la que se entreno."""
    directory, metadata, _ = built_artifact
    joblib.dump(joblib.load(artifact_path(directory)), artifact_path(tmp_path))
    reordered = list(reversed(metadata.feature_order))
    payload = dict(metadata.to_dict(), feature_order=reordered)
    payload.pop("threshold_display", None)
    ArtifactMetadata.from_dict(payload).write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="orden de features"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_an_incompatible_schema_version_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    directory, metadata, _ = built_artifact
    joblib.dump(joblib.load(artifact_path(directory)), artifact_path(tmp_path))
    payload = dict(metadata.to_dict(), schema_version="15b.0")
    payload.pop("threshold_display", None)
    ArtifactMetadata.from_dict(payload).write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="version de artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_corrupted_artifact_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    directory, metadata, _ = built_artifact
    artifact_path(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    artifact_path(tmp_path).write_bytes(b"esto no es un modelo")
    metadata.write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="no pudo cargarse"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_an_object_without_predict_proba_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    directory, metadata, _ = built_artifact
    joblib.dump({"no": "soy un pipeline"}, artifact_path(tmp_path))
    metadata.write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="predict_proba"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_unreadable_metadata_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    directory, _, _ = built_artifact
    joblib.dump(joblib.load(artifact_path(directory)), artifact_path(tmp_path))
    metadata_path(tmp_path).write_text("{ esto no es json", encoding="utf-8")

    with pytest.raises(ArtifactUnavailableError):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_missing_freeze_is_reported(tmp_path: Path, built_artifact) -> None:
    directory, _, _ = built_artifact

    with pytest.raises(ArtifactUnavailableError, match="protocolo congelado"):
        load_predictor(directory, freeze_path=tmp_path / "no-existe.json")


def test_a_tampered_freeze_blocks_the_load(tmp_path: Path, built_artifact, freeze_path) -> None:
    directory, _, _ = built_artifact
    payload = json.loads(Path(freeze_path).read_text(encoding="utf-8"))
    payload["threshold"] = 0.5
    tampered = tmp_path / "freeze.json"
    tampered.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ArtifactUnavailableError, match="no es valido"):
        load_predictor(directory, freeze_path=tampered)


# --- inferencia ------------------------------------------------------------


def test_prediction_is_deterministic(built_artifact, freeze_path, sample_features) -> None:
    directory, _, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)

    first = predictor.predict(sample_features)
    second = predictor.predict(sample_features)

    assert first == second


def test_prediction_survives_a_reload(built_artifact, freeze_path, sample_features) -> None:
    """Recargar el artefacto no puede mover la prediccion."""
    directory, _, _ = built_artifact

    first = load_predictor(directory, freeze_path=freeze_path).predict(sample_features)
    second = load_predictor(directory, freeze_path=freeze_path).predict(sample_features)

    assert first.risk_score == second.risk_score
    assert first.risk_flag == second.risk_flag


def test_the_json_order_does_not_change_the_prediction(
    built_artifact, freeze_path, sample_features
) -> None:
    """El predictor reindexa por `feature_order`, no por el orden del payload."""
    directory, _, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)
    shuffled = dict(reversed(list(sample_features.items())))

    assert list(shuffled) != list(sample_features)
    assert predictor.predict(shuffled) == predictor.predict(sample_features)


def test_the_frame_is_built_in_the_frozen_order(
    built_artifact, freeze_path, sample_features
) -> None:
    directory, _, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)
    shuffled = dict(reversed(list(sample_features.items())))

    assert list(predictor.build_frame(shuffled).columns) == predictor.feature_order


def test_missing_features_are_reported(built_artifact, freeze_path, sample_features) -> None:
    directory, _, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)
    incomplete = {k: v for k, v in sample_features.items() if k != "positions_count"}

    with pytest.raises(PredictionError, match="positions_count"):
        predictor.predict(incomplete)


def test_the_score_is_a_probability(built_artifact, freeze_path, sample_features) -> None:
    directory, _, _ = built_artifact
    outcome = load_predictor(directory, freeze_path=freeze_path).predict(sample_features)

    assert 0.0 <= outcome.risk_score <= 1.0
    assert outcome.risk_flag == (outcome.risk_score >= outcome.threshold)


def test_the_flag_uses_the_exact_threshold(built_artifact, freeze_path) -> None:
    """Un score justo en el umbral marca; el redondeo lo habria movido."""
    directory, metadata, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)

    assert predictor.threshold == metadata.threshold
    assert repr(predictor.threshold) == repr(0.1679418172266036)
