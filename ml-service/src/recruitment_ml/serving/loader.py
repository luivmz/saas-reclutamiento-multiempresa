"""Carga verificada del artefacto.

Cargar un `.joblib` y confiar en el seria exactamente el error que la Fase 15B
paso tres correcciones evitando en el freeze. Aqui se aplica el mismo criterio:
el artefacto solo se acepta si **demuestra** corresponder al protocolo
congelado, y si algo no encaja el servicio lo dice en lugar de fingir estar
listo.

Sobre joblib y la confianza
---------------------------
**`joblib.load` no es seguro frente a entradas no confiables**: deserializar
usa `pickle`, y un archivo malicioso ejecuta codigo al cargarse. Ninguna
comprobacion de este modulo cambia ese hecho.

Lo que si se hace, y conviene no confundir con seguridad frente a un atacante:

- **solo se cargan artefactos locales producidos por el builder**, nunca
  archivos recibidos de terceros, descargados ni subidos por un cliente;
- el digest SHA-256 se comprueba **antes** de deserializar, de modo que un
  binario sustituido o corrompido se detecta sin ejecutarlo;
- tras cargarlo se valida la **estructura real** del objeto, no solo que tenga
  un metodo con el nombre adecuado.

El digest vive en los metadatos, que estan en el mismo directorio: detecta que
el binario cambio por su cuenta -- una copia a medias, una sustitucion, una
corrupcion --, **no** a quien pueda reescribir ambos archivos. Contra eso, la
proteccion real es de donde viene el artefacto, no su hash.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
from sklearn.pipeline import Pipeline

from recruitment_ml.serving.metadata import (
    APPROVED_FREEZE_FINGERPRINT,
    ARTIFACT_SCHEMA_VERSION,
    CRITICAL_LIBRARIES,
    ArtifactMetadata,
    file_digest,
    library_versions,
)
from recruitment_ml.serving.paths import (
    DEFAULT_FREEZE_PATH,
    artifact_dir,
    artifact_path,
    metadata_path,
)
from recruitment_ml.serving.predictor import RiskPredictor
from recruitment_ml.training.freeze import ExperimentFreeze, FreezeValidationError, load_freeze
from recruitment_ml.training.models import build_pipeline
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

    freeze = _load_approved_freeze(Path(freeze_path))
    _assert_matches_freeze(metadata, freeze)
    _assert_library_versions(metadata)
    # El digest se comprueba **antes** de deserializar: un binario sustituido
    # no llega a ejecutarse.
    _assert_digest(metadata, model_file)

    try:
        pipeline = joblib.load(model_file)
    except Exception as error:  # noqa: BLE001 - joblib no acota sus fallos
        raise ArtifactUnavailableError(f"el artefacto no pudo cargarse: {error}") from error

    _assert_pipeline_structure(pipeline, metadata, freeze)

    return RiskPredictor(pipeline=pipeline, metadata=metadata)


# -- procedencia ------------------------------------------------------------


def _load_approved_freeze(freeze_path: Path) -> ExperimentFreeze:
    """El freeze debe existir, ser integro y ser **el aprobado**."""
    if not freeze_path.is_file():
        raise ArtifactUnavailableError(
            f"no se encuentra el protocolo congelado en {freeze_path}"
        )
    try:
        freeze = load_freeze(freeze_path)
    except FreezeValidationError as error:
        raise ArtifactUnavailableError(f"el protocolo congelado no es valido: {error}") from error

    if freeze.freeze_fingerprint != APPROVED_FREEZE_FINGERPRINT:
        raise ArtifactUnavailableError(
            "el protocolo congelado no es el aprobado en la Fase 15B: "
            f"{freeze.freeze_fingerprint!r} != {APPROVED_FREEZE_FINGERPRINT!r}"
        )
    return freeze


def _assert_digest(metadata: ArtifactMetadata, model_file: Path) -> None:
    """El binario debe ser el que el builder escribio."""
    if not metadata.artifact_sha256:
        raise ArtifactUnavailableError(
            "los metadatos no declaran artifact_sha256: el binario no puede verificarse"
        )
    found = file_digest(model_file)
    if found != metadata.artifact_sha256:
        raise ArtifactUnavailableError(
            "el digest del artefacto no coincide con el declarado en sus metadatos: "
            f"{found!r} != {metadata.artifact_sha256!r}"
        )


def _assert_library_versions(metadata: ArtifactMetadata) -> None:
    """Deserializar con otra version puede predecir distinto sin fallar."""
    current = library_versions()
    for library in CRITICAL_LIBRARIES:
        declared = metadata.library_versions.get(library)
        if declared != current.get(library):
            raise ArtifactUnavailableError(
                f"el artefacto se construyo con otra version de {library}: "
                f"{declared!r} != {current.get(library)!r}. Reconstruyelo."
            )


def _assert_matches_freeze(metadata: ArtifactMetadata, freeze: ExperimentFreeze) -> None:
    """El artefacto debe ser el del experimento aprobado, no uno parecido."""
    mismatches = [
        ("freeze_fingerprint", metadata.freeze_fingerprint, freeze.freeze_fingerprint),
        ("model_family", metadata.model_family, freeze.model_family),
        ("experiment_id", metadata.experiment_id, freeze.experiment_id),
        ("dataset_fingerprint", metadata.dataset_fingerprint, freeze.dataset_fingerprint),
        ("config_fingerprint", metadata.config_fingerprint, freeze.config_fingerprint),
        ("feature_set", metadata.feature_set, freeze.feature_set),
        ("preprocessing", metadata.preprocessing, freeze.preprocessing),
    ]
    for name, found, expected in mismatches:
        if found != expected:
            raise ArtifactUnavailableError(
                f"el artefacto no corresponde al protocolo congelado ({name}): "
                f"{found!r} != {expected!r}"
            )

    if dict(metadata.model_params) != dict(freeze.model_params):
        raise ArtifactUnavailableError(
            "los hiperparametros del artefacto no son los congelados: "
            f"{metadata.model_params!r} != {freeze.model_params!r}"
        )
    if float(metadata.threshold) != float(freeze.threshold):
        raise ArtifactUnavailableError(
            "el umbral del artefacto no es el congelado: "
            f"{float(metadata.threshold)!r} != {float(freeze.threshold)!r}"
        )

    # Basta comparar contra el conjunto congelado: como el freeze es el
    # aprobado, `freeze.features` y `feature_columns(freeze.feature_set)` son
    # necesariamente la misma lista. Comprobar las dos seria codigo muerto.
    expected_order = list(feature_columns(freeze.feature_set))
    if list(metadata.feature_order) != expected_order:
        raise ArtifactUnavailableError(
            "el orden de features del artefacto no es el del conjunto congelado: "
            f"{list(metadata.feature_order)} != {expected_order}"
        )


# -- estructura del objeto cargado -----------------------------------------


def _assert_pipeline_structure(
    pipeline: Any, metadata: ArtifactMetadata, freeze: ExperimentFreeze
) -> None:
    """Comprueba que lo cargado **es** el pipeline congelado.

    Exigir solo `predict_proba` dejaria pasar cualquier estimador con ese
    metodo. La comparacion se hace contra un pipeline de referencia construido
    con la misma familia y los mismos hiperparametros que el freeze, de modo
    que el solver, `max_iter`, `random_state`, `C` y `class_weight` se validan
    sin duplicar literales aqui.
    """
    reference = build_pipeline(freeze.model_family, dict(freeze.model_params))

    if not isinstance(pipeline, Pipeline):
        raise ArtifactUnavailableError(
            f"el artefacto no es un Pipeline de scikit-learn, sino {type(pipeline).__name__}"
        )

    found_steps = [(name, type(step)) for name, step in pipeline.steps]
    expected_steps = [(name, type(step)) for name, step in reference.steps]
    if found_steps != expected_steps:
        raise ArtifactUnavailableError(
            "la estructura del pipeline no es la congelada: "
            f"{[(n, t.__name__) for n, t in found_steps]} != "
            f"{[(n, t.__name__) for n, t in expected_steps]}"
        )

    for (name, step), (_, expected_step) in zip(pipeline.steps, reference.steps):
        found_params = step.get_params(deep=False)
        expected_params = expected_step.get_params(deep=False)
        if found_params != expected_params:
            differing = sorted(
                key
                for key in set(found_params) | set(expected_params)
                if found_params.get(key) != expected_params.get(key)
            )
            raise ArtifactUnavailableError(
                f"el paso {name!r} del pipeline no tiene los parametros congelados: {differing}"
            )

    _assert_fitted_on_the_frozen_features(pipeline, metadata)


def _assert_fitted_on_the_frozen_features(
    pipeline: Pipeline, metadata: ArtifactMetadata
) -> None:
    """El pipeline debe estar ajustado sobre las features congeladas."""
    expected = list(metadata.feature_order)

    n_features = getattr(pipeline, "n_features_in_", None)
    if n_features is None:
        raise ArtifactUnavailableError("el artefacto no esta ajustado: no expone n_features_in_")
    if int(n_features) != len(expected):
        raise ArtifactUnavailableError(
            f"el artefacto se ajusto con {int(n_features)} features y el protocolo declara "
            f"{len(expected)}"
        )

    names = getattr(pipeline, "feature_names_in_", None)
    if names is None:
        raise ArtifactUnavailableError(
            "el artefacto no conserva los nombres de sus features: no puede verificarse el orden"
        )
    if [str(name) for name in names] != expected:
        raise ArtifactUnavailableError(
            "el artefacto se ajusto con otro orden de features que el congelado"
        )
