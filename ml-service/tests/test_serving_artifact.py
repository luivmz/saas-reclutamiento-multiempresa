"""Artefacto servido: construccion reproducible y carga verificada.

La Fase 15B no versiono binarios. Servir un modelo obliga a tener uno, y la
unica forma honesta de tenerlo es **derivarlo del protocolo congelado** y
comprobar que lo que se carga es efectivamente eso.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import joblib
import pytest

from recruitment_ml.serving.build_artifact import ArtifactBuildError, build
from recruitment_ml.serving.loader import ArtifactUnavailableError, load_predictor
from recruitment_ml.serving.metadata import (
    APPROVED_FREEZE_FINGERPRINT,
    ARTIFACT_SCHEMA_VERSION,
    CRITICAL_LIBRARIES,
    DEPLOYMENT_STATUS,
    VERDICT,
    ArtifactMetadata,
    ServiceMetadata,
    file_digest,
    library_versions,
)
from recruitment_ml.serving.paths import artifact_path, metadata_path
from recruitment_ml.serving.predictor import PredictionError
from recruitment_ml.training.freeze import load_freeze



def _clone_artifact(directory: Path, target: Path) -> None:
    """Copia el binario **byte a byte**, para que su digest siga siendo valido."""
    artifact_path(target).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(artifact_path(directory), artifact_path(target))


def _rewrite_metadata(metadata: ArtifactMetadata, target: Path, **changes) -> None:
    """Escribe unos metadatos alterados junto al binario copiado."""
    payload = dict(metadata.to_dict(), **changes)
    payload.pop("threshold_display", None)
    ArtifactMetadata.from_dict(payload).write(metadata_path(target))


def _degraded_copy(directory: Path, metadata: ArtifactMetadata, target: Path, **changes) -> None:
    """Artefacto valido con unos metadatos que ya no lo describen."""
    _clone_artifact(directory, target)
    _rewrite_metadata(metadata, target, **changes)


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
    _clone_artifact(directory, tmp_path)

    with pytest.raises(ArtifactUnavailableError, match="no trae metadatos"):
        load_predictor(tmp_path, freeze_path=freeze_path)


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("freeze_fingerprint", "0" * 64, "freeze_fingerprint"),
        ("model_family", "random_forest", "model_family"),
        ("experiment_id", "otro-experimento", "experiment_id"),
        ("dataset_fingerprint", "0" * 64, "dataset_fingerprint"),
        ("config_fingerprint", "0" * 64, "config_fingerprint"),
        ("preprocessing", "sin escalado", "preprocessing"),
        ("feature_set", "core_without_elapsed", "feature_set"),
    ],
)
def test_an_artifact_that_does_not_match_the_freeze_is_rejected(
    tmp_path: Path, built_artifact, freeze_path, field_name: str, value: str, message: str
) -> None:
    """Cada campo del protocolo se contrasta, no solo la huella."""
    directory, metadata, _ = built_artifact
    _degraded_copy(directory, metadata, tmp_path, **{field_name: value})

    with pytest.raises(ArtifactUnavailableError, match=message):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_altered_hyperparameters_are_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """C=1 no es el modelo que 15B selecciono, aunque la familia coincida."""
    directory, metadata, _ = built_artifact
    _degraded_copy(directory, metadata, tmp_path, model_params={"C": 1.0, "class_weight": None})

    with pytest.raises(ArtifactUnavailableError, match="hiperparametros del artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_threshold_mismatch_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """Otro umbral clasifica distinto: no es el modelo que 15B aprobo."""
    directory, metadata, _ = built_artifact
    _degraded_copy(directory, metadata, tmp_path, threshold=0.5)

    with pytest.raises(ArtifactUnavailableError, match="umbral del artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_feature_order_mismatch_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """El orden importa: la matriz dejaria de ser la que se entreno."""
    directory, metadata, _ = built_artifact
    _degraded_copy(
        directory, metadata, tmp_path, feature_order=list(reversed(metadata.feature_order))
    )

    with pytest.raises(ArtifactUnavailableError, match="orden de features"):
        load_predictor(tmp_path, freeze_path=freeze_path)


@pytest.mark.parametrize("library", list(CRITICAL_LIBRARIES))
def test_altered_library_versions_are_rejected(
    tmp_path: Path, built_artifact, freeze_path, library: str
) -> None:
    """Deserializar con otra version puede predecir distinto sin fallar."""
    directory, metadata, _ = built_artifact
    versions = dict(metadata.library_versions, **{library: "0.0.0"})
    _degraded_copy(directory, metadata, tmp_path, library_versions=versions)

    with pytest.raises(ArtifactUnavailableError, match=f"otra version de {library}"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_wrong_digest_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """El binario debe ser el que el builder escribio."""
    directory, metadata, _ = built_artifact
    _degraded_copy(directory, metadata, tmp_path, artifact_sha256="0" * 64)

    with pytest.raises(ArtifactUnavailableError, match="digest del artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_metadata_without_a_digest_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    directory, metadata, _ = built_artifact
    _degraded_copy(directory, metadata, tmp_path, artifact_sha256="")

    with pytest.raises(ArtifactUnavailableError, match="no declaran artifact_sha256"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_freeze_that_is_not_the_approved_one_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """Integro no es lo mismo que aprobado.

    Este freeze se recalculo correctamente, asi que `load_freeze` lo acepta;
    lo que falla es que describe otro experimento.
    """
    from dataclasses import replace

    from recruitment_ml.training.freeze import persist_freeze

    directory, _, freeze = built_artifact
    other = replace(freeze, model_params={"C": 1.0, "class_weight": None}).with_fingerprint()
    assert other.is_intact()
    assert other.freeze_fingerprint != APPROVED_FREEZE_FINGERPRINT
    path = persist_freeze(other, tmp_path / "freeze.json")

    with pytest.raises(ArtifactUnavailableError, match="no es el aprobado"):
        load_predictor(directory, freeze_path=path)


# --- estructura real del objeto cargado -----------------------------------
#
# Exigir solo `predict_proba` dejaria pasar cualquier estimador con ese metodo.
# En estas pruebas el digest se recalcula a proposito para que el artefacto
# llegue a cargarse: asi lo que rechaza es la validacion estructural, no el
# hash.


def _substitute(target: Path, estimator, metadata: ArtifactMetadata) -> None:
    joblib.dump(estimator, artifact_path(target))
    _rewrite_metadata(metadata, target, artifact_sha256=file_digest(artifact_path(target)))


def _dummy_frame(columns: list[str], rows: int = 8):
    import numpy as np
    import pandas as pd

    return pd.DataFrame(
        np.random.default_rng(0).random((rows, len(columns))), columns=columns
    )


def test_a_substituted_estimator_with_predict_proba_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """Un bosque tiene `predict_proba` y no es el pipeline congelado."""
    from sklearn.ensemble import RandomForestClassifier

    _, metadata, _ = built_artifact
    intruder = RandomForestClassifier(n_estimators=2, random_state=0)
    intruder.fit(_dummy_frame(metadata.feature_order), [0, 1] * 4)
    _substitute(tmp_path, intruder, metadata)

    with pytest.raises(ArtifactUnavailableError, match="no es un Pipeline"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_pipeline_with_another_scaler_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """Mismo tipo de objeto, otra estructura interna."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler

    _, metadata, _ = built_artifact
    impostor = Pipeline([("scaler", MinMaxScaler()), ("model", LogisticRegression())])
    impostor.fit(_dummy_frame(metadata.feature_order), [0, 1] * 4)
    _substitute(tmp_path, impostor, metadata)

    with pytest.raises(ArtifactUnavailableError, match="estructura del pipeline"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_pipeline_with_other_hyperparameters_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """La estructura coincide, pero `C` no: se compara parametro a parametro."""
    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    impostor = build_pipeline("logistic_regression", {"C": 1.0, "class_weight": None})
    impostor.fit(_dummy_frame(metadata.feature_order), [0, 1] * 4)
    _substitute(tmp_path, impostor, metadata)

    with pytest.raises(ArtifactUnavailableError, match="parametros congelados"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_pipeline_fitted_on_other_features_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    impostor = build_pipeline("logistic_regression", dict(metadata.model_params))
    impostor.fit(_dummy_frame(["a", "b", "c"]), [0, 1] * 4)
    _substitute(tmp_path, impostor, metadata)

    with pytest.raises(ArtifactUnavailableError, match="features"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_pipeline_fitted_on_a_different_feature_order_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    impostor = build_pipeline("logistic_regression", dict(metadata.model_params))
    impostor.fit(_dummy_frame(list(reversed(metadata.feature_order))), [0, 1] * 4)
    _substitute(tmp_path, impostor, metadata)

    with pytest.raises(ArtifactUnavailableError, match="otro orden de features"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_an_unfitted_pipeline_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    _substitute(
        tmp_path, build_pipeline("logistic_regression", dict(metadata.model_params)), metadata
    )

    with pytest.raises(ArtifactUnavailableError, match="no esta completamente ajustado"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_pipeline_with_only_the_scaler_fitted_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """El hueco que cerro este hotfix.

    Con el `StandardScaler` ajustado, el pipeline ya expone `n_features_in_` y
    `feature_names_in_` -- ambos delegan en el **primer** paso --, asi que las
    comprobaciones de features pasaban y el servicio se declaraba listo. La
    regresion logistica seguia sin entrenar y `/v1/predict` fallaba en la
    primera peticion.

    El digest y los metadatos son correctos a proposito: lo que rechaza el
    artefacto es el estado de entrenamiento incompleto.
    """
    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    half_fitted = build_pipeline("logistic_regression", dict(metadata.model_params))
    half_fitted.named_steps["scaler"].fit(_dummy_frame(metadata.feature_order))

    # Precondiciones: el artefacto es coherente en todo lo demas.
    assert half_fitted.n_features_in_ == len(metadata.feature_order)
    assert list(half_fitted.feature_names_in_) == metadata.feature_order

    _substitute(tmp_path, half_fitted, metadata)
    assert (
        ArtifactMetadata.read(metadata_path(tmp_path)).artifact_sha256
        == file_digest(artifact_path(tmp_path))
    ), "el digest debe ser valido para que el fallo sea el estado de entrenamiento"

    with pytest.raises(ArtifactUnavailableError, match="no esta completamente ajustado") as failure:
        load_predictor(tmp_path, freeze_path=freeze_path)

    assert "LogisticRegression" in str(failure.value)


def test_a_pipeline_with_only_the_final_estimator_fitted_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """El caso inverso, que `check_is_fitted` sobre el pipeline no detecta.

    `check_is_fitted(pipeline)` delega en el **ultimo** paso, asi que un
    estimador final entrenado lo satisface aunque el scaler no lo este. Por eso
    se comprueba cada paso por separado.
    """
    from sklearn.exceptions import NotFittedError
    from sklearn.utils.validation import check_is_fitted

    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    inverted = build_pipeline("logistic_regression", dict(metadata.model_params))
    frame = _dummy_frame(metadata.feature_order)
    inverted.named_steps["model"].fit(frame, [0, 1] * 4)

    check_is_fitted(inverted)  # el pipeline "parece" ajustado
    with pytest.raises(NotFittedError):
        check_is_fitted(inverted.named_steps["scaler"])

    _substitute(tmp_path, inverted, metadata)

    with pytest.raises(ArtifactUnavailableError, match="no esta completamente ajustado") as failure:
        load_predictor(tmp_path, freeze_path=freeze_path)

    assert "StandardScaler" in str(failure.value)


def test_the_official_artifact_is_fully_fitted(built_artifact, freeze_path) -> None:
    """Control positivo: el pipeline real pasa las tres comprobaciones."""
    from sklearn.utils.validation import check_is_fitted

    directory, _, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)

    check_is_fitted(predictor.pipeline)
    check_is_fitted(predictor.pipeline.named_steps["scaler"])
    check_is_fitted(predictor.pipeline.named_steps["model"])


def test_a_partially_fitted_artifact_never_reports_a_ready_model(
    monkeypatch, tmp_path: Path, built_artifact, sample_features
) -> None:
    """Y el servicio no lo anuncia como listo: 503, no un 500 en la primera peticion."""
    from fastapi.testclient import TestClient

    from recruitment_ml.api.app import create_app
    from recruitment_ml.api.security import TOKEN_ENV, TOKEN_HEADER
    from recruitment_ml.serving.paths import ARTIFACT_DIR_ENV
    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    half_fitted = build_pipeline("logistic_regression", dict(metadata.model_params))
    half_fitted.named_steps["scaler"].fit(_dummy_frame(metadata.feature_order))
    _substitute(tmp_path, half_fitted, metadata)
    monkeypatch.setenv(ARTIFACT_DIR_ENV, str(tmp_path))
    # Con credencial valida, para que el 503 sea atribuible al artefacto a
    # medio ajustar y no a la autenticacion.
    monkeypatch.setenv(TOKEN_ENV, "token-de-suite")

    payload = {name: int(value) for name, value in sample_features.items()}
    with TestClient(create_app(), headers={TOKEN_HEADER: "token-de-suite"}) as client:
        assert client.get("/health").json()["model_ready"] is False
        assert client.post("/v1/predict", json=payload).status_code == 503


def test_the_official_artifact_passes_the_structural_check(built_artifact, freeze_path) -> None:
    """Control positivo: el endurecimiento no puede rechazarlo todo."""
    directory, metadata, _ = built_artifact
    predictor = load_predictor(directory, freeze_path=freeze_path)

    assert predictor.metadata.artifact_sha256 == metadata.artifact_sha256
    assert list(predictor.pipeline.feature_names_in_) == metadata.feature_order
    assert predictor.pipeline.named_steps["model"].C == 10.0
    assert predictor.pipeline.named_steps["model"].class_weight is None


def test_an_incompatible_schema_version_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    directory, metadata, _ = built_artifact
    _clone_artifact(directory, tmp_path)
    payload = dict(metadata.to_dict(), schema_version="15b.0")
    payload.pop("threshold_display", None)
    ArtifactMetadata.from_dict(payload).write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="version de artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_a_corrupted_artifact_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    """El digest lo detecta **antes** de deserializar: nada llega a ejecutarse."""
    directory, metadata, _ = built_artifact
    artifact_path(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    artifact_path(tmp_path).write_bytes(b"esto no es un modelo")
    metadata.write(metadata_path(tmp_path))

    with pytest.raises(ArtifactUnavailableError, match="digest del artefacto"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_an_unreadable_binary_with_a_matching_digest_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """Y si alguien actualiza tambien el digest, falla al deserializar."""
    _, metadata, _ = built_artifact
    artifact_path(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    artifact_path(tmp_path).write_bytes(b"esto no es un modelo")
    _rewrite_metadata(metadata, tmp_path, artifact_sha256=file_digest(artifact_path(tmp_path)))

    with pytest.raises(ArtifactUnavailableError, match="no pudo cargarse"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_an_object_that_is_not_a_pipeline_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """Con el digest correcto llega a cargarse, y ahi se comprueba que **es**."""
    _, metadata, _ = built_artifact
    joblib.dump({"no": "soy un pipeline"}, artifact_path(tmp_path))
    _rewrite_metadata(metadata, tmp_path, artifact_sha256=file_digest(artifact_path(tmp_path)))

    with pytest.raises(ArtifactUnavailableError, match="no es un Pipeline"):
        load_predictor(tmp_path, freeze_path=freeze_path)


def test_unreadable_metadata_is_rejected(tmp_path: Path, built_artifact, freeze_path) -> None:
    directory, _, _ = built_artifact
    _clone_artifact(directory, tmp_path)
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


def test_a_pipeline_fitted_without_feature_names_is_rejected(
    tmp_path: Path, built_artifact, freeze_path
) -> None:
    """Ajustar con un array pierde los nombres, y el orden deja de ser auditable."""
    import numpy as np

    from recruitment_ml.training.models import build_pipeline

    _, metadata, _ = built_artifact
    impostor = build_pipeline("logistic_regression", dict(metadata.model_params))
    impostor.fit(np.random.default_rng(0).random((8, len(metadata.feature_order))), [0, 1] * 4)
    assert not hasattr(impostor, "feature_names_in_")
    _substitute(tmp_path, impostor, metadata)

    with pytest.raises(ArtifactUnavailableError, match="no conserva los nombres"):
        load_predictor(tmp_path, freeze_path=freeze_path)
