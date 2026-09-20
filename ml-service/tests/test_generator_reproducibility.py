"""Reproducibilidad y linaje.

Validaciones 1, 2 y 20 de `dataset-specification.md`. Sin reproducibilidad, un
resultado no puede citarse en el informe academico.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from recruitment_ml.config import DATASET_VERSION, DEFAULT_SEED, SyntheticConfig
from recruitment_ml.synthetic.generator import build_dataset, dataset_fingerprint

SMALL = 400


def test_same_seed_and_config_produce_identical_dataset() -> None:
    first = build_dataset(SyntheticConfig(rows=SMALL))
    second = build_dataset(SyntheticConfig(rows=SMALL))

    assert first.manifest["dataset_fingerprint"] == second.manifest["dataset_fingerprint"]
    pd.testing.assert_frame_equal(first.frame, second.frame)


def test_different_seed_produces_different_dataset() -> None:
    base = build_dataset(SyntheticConfig(rows=SMALL, seed=DEFAULT_SEED))
    other = build_dataset(SyntheticConfig(rows=SMALL, seed=DEFAULT_SEED + 1))

    assert base.manifest["dataset_fingerprint"] != other.manifest["dataset_fingerprint"]


def test_changing_a_structural_parameter_changes_the_dataset() -> None:
    base = build_dataset(SyntheticConfig(rows=SMALL))
    drifted = build_dataset(SyntheticConfig(rows=SMALL, drift_strength=0.6))

    assert base.manifest["dataset_fingerprint"] != drifted.manifest["dataset_fingerprint"]
    assert base.config.fingerprint() != drifted.config.fingerprint()


def test_output_path_does_not_change_the_config_fingerprint() -> None:
    """La ruta de salida no altera el contenido, asi que no entra al hash."""
    without = SyntheticConfig(rows=SMALL)
    with_path = SyntheticConfig(rows=SMALL, output_path=Path("artifacts/x.csv"))

    assert without.fingerprint() == with_path.fingerprint()


def test_dataset_fingerprint_detects_any_content_change() -> None:
    dataset = build_dataset(SyntheticConfig(rows=SMALL))
    mutated = dataset.frame.copy()
    mutated.loc[0, "positions_count"] = int(mutated.loc[0, "positions_count"]) + 1

    assert dataset_fingerprint(mutated) != dataset.manifest["dataset_fingerprint"]


def test_manifest_records_the_lineage_required_by_phase_14() -> None:
    manifest = build_dataset(SyntheticConfig(rows=SMALL)).manifest

    assert manifest["seed"] == DEFAULT_SEED
    assert manifest["dataset_version"] == DATASET_VERSION
    assert manifest["feature_contract_version"] == "phase-14"
    assert manifest["data_nature"] == "synthetic"
    assert len(manifest["dataset_fingerprint"]) == 64
    assert len(manifest["config_fingerprint"]) == 64
    assert "autorizan uso institucional" in manifest["validity_notice"].lower()
    assert "no demuestran validez predictiva real" in manifest["validity_notice"].lower()


def test_manifest_flags_configurations_outside_the_approved_profile() -> None:
    """El perfil academico aprobado es 5 000-10 000 filas con la seed maestra."""
    small = build_dataset(SyntheticConfig(rows=SMALL))
    assert small.manifest["academic_profile_deviations"], "rows=400 esta fuera del perfil aprobado"

    approved = SyntheticConfig(rows=5_000)
    assert approved.is_within_approved_profile()


@pytest.mark.parametrize("rows", [49, 50_001])
def test_invalid_row_counts_are_rejected(rows: int) -> None:
    with pytest.raises(ValueError):
        SyntheticConfig(rows=rows)


def test_inverted_prevalence_band_is_rejected() -> None:
    with pytest.raises(ValueError):
        SyntheticConfig(rows=SMALL, prevalence_min=0.5, prevalence_max=0.2)


def test_config_is_immutable() -> None:
    config = SyntheticConfig(rows=SMALL)
    with pytest.raises(ValueError):
        config.rows = 999  # type: ignore[misc]


def test_unknown_config_field_is_rejected() -> None:
    with pytest.raises(ValueError):
        SyntheticConfig(rows=SMALL, unknown_knob=1)  # type: ignore[call-arg]


def test_lazy_reexport_exposes_the_public_api() -> None:
    """La reexportacion es perezosa para no disparar el RuntimeWarning de runpy."""
    from recruitment_ml import synthetic

    assert synthetic.build_dataset is build_dataset
    assert synthetic.SyntheticDataset.__name__ == "SyntheticDataset"


def test_lazy_reexport_rejects_unknown_attributes() -> None:
    from recruitment_ml import synthetic

    with pytest.raises(AttributeError):
        _ = synthetic.does_not_exist
