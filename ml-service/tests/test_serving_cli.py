"""Linea de comandos del constructor y ramas de guarda restantes.

Son caminos que nadie recorre a diario y que, precisamente por eso, conviene
fijar: el comando que reconstruye el artefacto, la guarda que impide que el
esquema de la API se separe del contrato de features y el fallo de inferencia.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from recruitment_ml.api.schemas import PredictionRequest, assert_schema_matches_contract
from recruitment_ml.serving.build_artifact import main
from recruitment_ml.serving.metadata import (
    APPROVED_FREEZE_FINGERPRINT,
    ArtifactMetadata,
    file_digest,
)
from recruitment_ml.serving.paths import artifact_path, metadata_path
from recruitment_ml.serving.predictor import PredictionError, RiskPredictor
from recruitment_ml.training.freeze import persist_freeze


# --- comando de construccion ----------------------------------------------


def test_the_cli_builds_the_artifact(tmp_path: Path, freeze_path, capsys) -> None:
    exit_code = main(
        ["--rows", "6000", "--freeze-path", str(freeze_path), "--output-dir", str(tmp_path)]
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert artifact_path(tmp_path).is_file()
    assert metadata_path(tmp_path).is_file()
    assert "9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2" in output
    assert "0.1679418172266036" in output
    assert "experimental" in output
    assert "GAP-01" in output


def test_the_cli_fails_cleanly_on_a_wrong_row_count(
    tmp_path: Path, freeze_path, capsys
) -> None:
    """Sin traza: un mensaje que dice que revisar."""
    exit_code = main(
        ["--rows", "1000", "--freeze-path", str(freeze_path), "--output-dir", str(tmp_path)]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "no corresponde al experimento" in captured.err
    assert "Traceback" not in captured.err
    assert not artifact_path(tmp_path).exists()


# --- guarda del esquema ----------------------------------------------------


def test_the_schema_guard_accepts_the_current_contract() -> None:
    assert_schema_matches_contract() is None


def test_the_schema_guard_detects_a_divergence(monkeypatch) -> None:
    """Si el esquema y el contrato se separan, el servicio no debe arrancar."""
    fields = dict(PredictionRequest.model_fields)
    fields.pop("positions_count")
    monkeypatch.setattr(PredictionRequest, "model_fields", fields)

    with pytest.raises(RuntimeError, match="positions_count"):
        assert_schema_matches_contract()


# --- ramas restantes del loader y del predictor ---------------------------


def test_the_builder_rejects_a_freeze_that_is_not_the_approved_one(
    tmp_path: Path, built_artifact, capsys
) -> None:
    """Integro no es lo mismo que aprobado.

    Cambiar `C=10` por `C=1` y recalcular la huella produce un freeze
    perfectamente coherente consigo mismo que describe **otro** experimento.
    El builder lo rechaza antes de generar nada.
    """
    _, _, freeze = built_artifact
    other = replace(freeze, model_params={"C": 1.0, "class_weight": None}).with_fingerprint()
    assert other.is_intact(), "el freeze manipulado debe ser internamente coherente"
    assert other.freeze_fingerprint != APPROVED_FREEZE_FINGERPRINT
    path = persist_freeze(other, tmp_path / "freeze.json")

    exit_code = main(
        ["--rows", "6000", "--freeze-path", str(path), "--output-dir", str(tmp_path / "salida")]
    )

    assert exit_code == 1
    assert "no es el aprobado" in capsys.readouterr().err
    assert not artifact_path(tmp_path / "salida").exists()


def test_the_builder_records_the_binary_digest(tmp_path: Path, freeze_path) -> None:
    """El digest se calcula sobre el archivo escrito, no sobre el objeto."""
    main(["--rows", "6000", "--freeze-path", str(freeze_path), "--output-dir", str(tmp_path)])
    metadata = ArtifactMetadata.read(metadata_path(tmp_path))

    assert metadata.artifact_sha256 == file_digest(artifact_path(tmp_path))
    assert len(metadata.artifact_sha256) == 64


def test_an_inference_failure_is_wrapped(built_artifact, sample_features) -> None:
    """Un fallo de scikit-learn se traduce a un error del dominio."""
    _, metadata, _ = built_artifact

    class Exploding:
        def predict_proba(self, frame):  # noqa: ANN001, ARG002
            raise ValueError("matriz singular")

    predictor = RiskPredictor(pipeline=Exploding(), metadata=metadata)

    with pytest.raises(PredictionError, match="la inferencia fallo"):
        predictor.predict(sample_features)


def test_metadata_read_rejects_a_file_with_missing_fields(tmp_path: Path, built_artifact) -> None:
    directory, metadata, _ = built_artifact
    partial = {k: v for k, v in metadata.to_dict().items() if k != "seed"}
    target = tmp_path / "metadata.json"
    target.write_text(__import__("json").dumps(partial), encoding="utf-8")

    with pytest.raises(ValueError, match="incompletos"):
        ArtifactMetadata.read(target)
