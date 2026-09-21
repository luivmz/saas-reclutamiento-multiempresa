"""Reconstruccion reproducible del modelo servido.

La Fase 15B no versiono ningun binario, y con razon: un `.joblib` en el
repositorio es un objeto opaco que nadie puede auditar. Lo que si esta
versionado es el **protocolo congelado**, y de el se deriva el modelo.

Este comando:

1. lee el freeze de la Fase 15B y comprueba su integridad;
2. regenera el dataset sintetico con la configuracion aprobada;
3. **verifica que las huellas del dataset y de la configuracion coinciden**
   con las del freeze -- si no, el modelo no seria el mismo;
4. rehace la particion temporal y toma exclusivamente `train`;
5. ajusta el pipeline con la familia y los hiperparametros congelados;
6. escribe el artefacto y sus metadatos en un directorio ignorado por Git.

No elige modelo, no ajusta hiperparametros, no toca el umbral y no mira el
conjunto de prueba. Solo reconstruye lo que 15B decidio.

Uso:

    python -m recruitment_ml.serving.build_artifact
    python -m recruitment_ml.serving.build_artifact --rows 6000 --output-dir ruta
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import joblib

from recruitment_ml.config import SyntheticConfig
from recruitment_ml.serving.metadata import (
    APPROVED_FREEZE_FINGERPRINT,
    ARTIFACT_SCHEMA_VERSION,
    ArtifactMetadata,
    file_digest,
    library_versions,
)
from recruitment_ml.serving.paths import (
    DEFAULT_ARTIFACT_DIR,
    DEFAULT_FREEZE_PATH,
    artifact_path,
    metadata_path,
)
from recruitment_ml.synthetic.generator import build_dataset
from recruitment_ml.training.freeze import ExperimentFreeze, load_freeze
from recruitment_ml.training.models import build_pipeline
from recruitment_ml.training.preprocessing import build_matrix, build_target, feature_columns
from recruitment_ml.training.split import build_temporal_split


class ArtifactBuildError(RuntimeError):
    """La reconstruccion no reproduce el experimento congelado."""


def build(
    freeze_path: Path = DEFAULT_FREEZE_PATH,
    output_dir: Path = DEFAULT_ARTIFACT_DIR,
    rows: int = 6_000,
) -> ArtifactMetadata:
    """Reconstruye el artefacto a partir del freeze y lo persiste."""
    freeze = load_freeze(Path(freeze_path))
    _assert_reproduces(freeze, rows)

    config = SyntheticConfig(rows=rows, seed=freeze.seed)
    dataset = build_dataset(config)
    frame = dataset.model_ready()

    dataset_fingerprint = str(dataset.manifest["model_ready_fingerprint"])
    config_fingerprint = str(dataset.manifest["config_fingerprint"])
    if dataset_fingerprint != freeze.dataset_fingerprint:
        raise ArtifactBuildError(
            "el dataset regenerado no es el del experimento congelado: "
            f"{dataset_fingerprint!r} != {freeze.dataset_fingerprint!r}. "
            "Revisa --rows y la semilla."
        )
    if config_fingerprint != freeze.config_fingerprint:
        raise ArtifactBuildError(
            "la configuracion del generador no coincide con la congelada: "
            f"{config_fingerprint!r} != {freeze.config_fingerprint!r}"
        )

    split = build_temporal_split(
        frame,
        dataset_fingerprint=dataset_fingerprint,
        config_fingerprint=config_fingerprint,
    )
    if split.signature != freeze.split_signature:
        raise ArtifactBuildError(
            "la particion regenerada no es la congelada: "
            f"{split.signature!r} != {freeze.split_signature!r}"
        )

    # Solo train. El conjunto de prueba no se abre aqui: servir un modelo no
    # es motivo para volver a mirarlo.
    train = split.train
    X_train = build_matrix(train, freeze.feature_set)
    y_train = build_target(train)

    pipeline = build_pipeline(freeze.model_family, freeze.model_params)
    pipeline.fit(X_train, y_train)

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    binary = artifact_path(output)
    joblib.dump(pipeline, binary)

    metadata = ArtifactMetadata(
        schema_version=ARTIFACT_SCHEMA_VERSION,
        experiment_id=freeze.experiment_id,
        freeze_fingerprint=freeze.freeze_fingerprint,
        dataset_fingerprint=dataset_fingerprint,
        config_fingerprint=config_fingerprint,
        model_family=freeze.model_family,
        model_params=dict(freeze.model_params),
        preprocessing=freeze.preprocessing,
        feature_set=freeze.feature_set,
        feature_order=list(feature_columns(freeze.feature_set)),
        threshold=float(freeze.threshold),
        seed=int(freeze.seed),
        rows=int(rows),
        n_train=int(len(train)),
        built_at=datetime.now().astimezone().isoformat(),
        # El digest se calcula sobre el archivo ya escrito, no sobre el objeto
        # en memoria: lo que el loader va a leer es el archivo.
        artifact_sha256=file_digest(binary),
        library_versions=library_versions(),
    )
    metadata.write(metadata_path(output))
    return metadata


def _assert_reproduces(freeze: ExperimentFreeze, rows: int) -> None:
    """Comprobaciones baratas antes de gastar minutos generando el dataset."""
    if not freeze.is_intact():
        raise ArtifactBuildError("el freeze fue alterado: no se reconstruye nada a partir de el")
    if freeze.freeze_fingerprint != APPROVED_FREEZE_FINGERPRINT:
        # La integridad solo demuestra coherencia interna. Cambiar C=10 por
        # C=1 y recalcular la huella produce un freeze perfectamente integro
        # que describe otro experimento; este servicio sirve uno concreto.
        raise ArtifactBuildError(
            "el freeze no es el aprobado en la Fase 15B: "
            f"{freeze.freeze_fingerprint!r} != {APPROVED_FREEZE_FINGERPRINT!r}. "
            "Servir otro experimento exige una fase que lo apruebe."
        )
    expected_id = f"phase-15b-{freeze.seed}-{rows}"
    if freeze.experiment_id != expected_id:
        raise ArtifactBuildError(
            f"--rows {rows} no corresponde al experimento congelado "
            f"({freeze.experiment_id!r}; se esperaba {expected_id!r})"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruye el modelo de la Fase 15B a partir del protocolo congelado."
    )
    parser.add_argument("--rows", type=int, default=6_000, help="filas del dataset sintetico")
    parser.add_argument(
        "--freeze-path", type=Path, default=DEFAULT_FREEZE_PATH, help="ruta del freeze de 15B"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_ARTIFACT_DIR,
        help="directorio del artefacto (ignorado por Git)",
    )
    args = parser.parse_args(argv)

    try:
        metadata = build(
            freeze_path=args.freeze_path, output_dir=args.output_dir, rows=args.rows
        )
    except ArtifactBuildError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"artefacto            : {artifact_path(args.output_dir)}")
    print(f"metadatos            : {metadata_path(args.output_dir)}")
    print(f"experiment_id        : {metadata.experiment_id}")
    print(f"freeze fingerprint   : {metadata.freeze_fingerprint}")
    print(f"artifact sha256      : {metadata.artifact_sha256}")
    print(f"umbral exacto        : {metadata.threshold!r}")
    print(f"features             : {len(metadata.feature_order)}")
    print(f"filas de train       : {metadata.n_train}")
    print("estado               : experimental; GAP-01 abierto, sin autorizacion de despliegue")
    return 0


if __name__ == "__main__":  # pragma: no cover - entrada de linea de comandos
    raise SystemExit(main())
