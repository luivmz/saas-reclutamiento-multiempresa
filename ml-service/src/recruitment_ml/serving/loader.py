"""Carga verificada del artefacto.

Cargar un `.joblib` y confiar en el seria exactamente el error que la Fase 15B
paso tres correcciones evitando en el freeze. Aqui se aplica el mismo criterio:
el artefacto solo se acepta si **demuestra** corresponder al protocolo
congelado, y si algo no encaja el servicio lo dice en lugar de fingir estar
listo.
"""

from __future__ import annotations

from pathlib import Path

import joblib

from recruitment_ml.serving.metadata import ARTIFACT_SCHEMA_VERSION, ArtifactMetadata
from recruitment_ml.serving.paths import (
    DEFAULT_FREEZE_PATH,
    artifact_dir,
    artifact_path,
    metadata_path,
)
from recruitment_ml.serving.predictor import RiskPredictor
from recruitment_ml.training.freeze import FreezeValidationError, load_freeze
from recruitment_ml.training.preprocessing import feature_columns


class ArtifactUnavailableError(RuntimeError):
    """No hay artefacto que servir: falta, esta ilegible o no es compatible."""


def load_predictor(
    directory: Path | None = None, freeze_path: Path = DEFAULT_FREEZE_PATH
) -> RiskPredictor:
    """Carga el artefacto y lo valida contra el freeze versionado."""
    folder = Path(directory) if directory is not None else artifact_dir()
    model_file = artifact_path(folder)
    metadata_file = metadata_path(folder)

    if not model_file.is_file():
        raise ArtifactUnavailableError(
            "no hay artefacto de modelo; reconstruyelo con "
            "'python -m recruitment_ml.serving.build_artifact'"
        )
    if not metadata_file.is_file():
        raise ArtifactUnavailableError(
            "el artefacto no trae metadatos: sin ellos no puede verificarse a que "
            "experimento pertenece"
        )

    try:
        metadata = ArtifactMetadata.read(metadata_file)
    except (ValueError, OSError) as error:
        raise ArtifactUnavailableError(f"metadatos ilegibles o incompletos: {error}") from error

    if metadata.schema_version != ARTIFACT_SCHEMA_VERSION:
        raise ArtifactUnavailableError(
            f"version de artefacto incompatible: {metadata.schema_version!r} != "
            f"{ARTIFACT_SCHEMA_VERSION!r}"
        )

    _assert_matches_freeze(metadata, Path(freeze_path))

    try:
        pipeline = joblib.load(model_file)
    except Exception as error:  # noqa: BLE001 - joblib no acota sus fallos
        raise ArtifactUnavailableError(f"el artefacto no pudo cargarse: {error}") from error

    if not hasattr(pipeline, "predict_proba"):
        raise ArtifactUnavailableError(
            "el artefacto cargado no expone predict_proba: no sirve para estimar riesgo"
        )

    return RiskPredictor(pipeline=pipeline, metadata=metadata)


def _assert_matches_freeze(metadata: ArtifactMetadata, freeze_path: Path) -> None:
    """El artefacto debe ser el del experimento aprobado, no uno parecido."""
    if not freeze_path.is_file():
        raise ArtifactUnavailableError(
            f"no se encuentra el protocolo congelado en {freeze_path}"
        )
    try:
        freeze = load_freeze(freeze_path)
    except FreezeValidationError as error:
        raise ArtifactUnavailableError(f"el protocolo congelado no es valido: {error}") from error

    mismatches = [
        ("freeze_fingerprint", metadata.freeze_fingerprint, freeze.freeze_fingerprint),
        ("model_family", metadata.model_family, freeze.model_family),
        ("experiment_id", metadata.experiment_id, freeze.experiment_id),
        ("dataset_fingerprint", metadata.dataset_fingerprint, freeze.dataset_fingerprint),
        ("feature_set", metadata.feature_set, freeze.feature_set),
    ]
    for name, found, expected in mismatches:
        if found != expected:
            raise ArtifactUnavailableError(
                f"el artefacto no corresponde al protocolo congelado ({name}): "
                f"{found!r} != {expected!r}"
            )

    if float(metadata.threshold) != float(freeze.threshold):
        raise ArtifactUnavailableError(
            "el umbral del artefacto no es el congelado: "
            f"{float(metadata.threshold)!r} != {float(freeze.threshold)!r}"
        )

    expected_order = list(feature_columns(freeze.feature_set))
    if list(metadata.feature_order) != expected_order:
        raise ArtifactUnavailableError(
            "el orden de features del artefacto no es el del conjunto congelado"
        )
    if list(metadata.feature_order) != list(freeze.features):
        raise ArtifactUnavailableError(
            "el orden de features del artefacto no coincide con el declarado en el freeze"
        )
