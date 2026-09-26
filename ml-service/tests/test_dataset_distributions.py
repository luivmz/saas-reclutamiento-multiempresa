"""Distribuciones, prevalencia, drift y heterogeneidad multiempresa.

Validaciones 10, 11, 12, 15 y 16. Comprueban que el generador produce un
proceso con estructura realista y no un muestreo uniforme con una etiqueta
pegada encima.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from recruitment_ml.config import SyntheticConfig
from recruitment_ml.schema import STATUS_CENSORED, TARGET_COLUMN
from recruitment_ml.synthetic.generator import build_dataset
from recruitment_ml.synthetic.validators import (
    check_count_invariants,
    check_extreme_cases,
    check_prevalence,
    validate_dataset,
)


def test_prevalence_sits_inside_the_simulated_band(dataset, config: SyntheticConfig) -> None:
    """25-40 % es una decision de simulacion, no una estadistica institucional."""
    assert check_prevalence(dataset.frame, config.prevalence_min, config.prevalence_max) == []
    assert config.prevalence_min <= dataset.prevalence() <= config.prevalence_max


def test_prevalence_is_not_an_artifact_of_the_sample_size() -> None:
    """Debe ser una propiedad de la simulacion, no del numero de filas."""
    prevalences = [build_dataset(SyntheticConfig(rows=rows)).prevalence() for rows in (600, 1_500, 3_000)]
    assert max(prevalences) - min(prevalences) < 0.12
    for value in prevalences:
        assert 0.25 <= value <= 0.40


def test_prevalence_emerges_from_the_process_not_from_resampling(dataset) -> None:
    """Subir la presion estructural debe mover la prevalencia hacia arriba."""
    pressured = build_dataset(SyntheticConfig(rows=dataset.config.rows, delay_pressure=1.6))
    relaxed = build_dataset(SyntheticConfig(rows=dataset.config.rows, delay_pressure=0.6))

    assert relaxed.prevalence() < dataset.prevalence() < pressured.prevalence()


def test_count_invariants_hold(frame: pd.DataFrame) -> None:
    assert check_count_invariants(frame) == []


@pytest.mark.parametrize("kind", ["evaluations", "interviews"])
def test_pending_is_exactly_scheduled_minus_completed(frame: pd.DataFrame, kind: str) -> None:
    scheduled = frame[f"{kind}_scheduled_count"]
    completed = frame[f"{kind}_completed_count"]
    pending = frame[f"{kind}_pending_count"]

    assert (pending == scheduled - completed).all()
    assert (frame[f"{kind}_overdue_pending_count"] <= pending).all()


def test_application_counts_are_overdispersed(model_ready: pd.DataFrame) -> None:
    """Una Poisson subestimaria la varianza del volumen de postulaciones."""
    values = model_ready["applications_received_count"].astype(float)
    assert values.var(ddof=0) > values.mean() * 1.5


def test_durations_are_right_skewed(model_ready: pd.DataFrame) -> None:
    """Los tiempos positivos no son uniformes: tienen cola a la derecha."""
    window = model_ready["application_window_days"].astype(float)
    assert window.mean() > window.median()
    assert window.max() > window.quantile(0.99)


def test_temporal_drift_is_present_and_moderate(model_ready: pd.DataFrame) -> None:
    """Debe existir drift suficiente para justificar el split temporal."""
    ordered = model_ready.assign(_cp=pd.to_datetime(model_ready["checkpoint_at"], utc=True)).sort_values("_cp")
    blocks = np.array_split(np.arange(len(ordered)), 3)
    prevalences = [float(ordered.iloc[idx][TARGET_COLUMN].astype(float).mean()) for idx in blocks]

    assert prevalences[0] < prevalences[-1], "el drift deberia aumentar el riesgo con el tiempo"
    assert prevalences[-1] - prevalences[0] < 0.35, "el drift no puede ser extremo"


def test_several_fictitious_organizations_are_present(model_ready: pd.DataFrame, config: SyntheticConfig) -> None:
    assert model_ready["organization_id"].nunique() == config.organizations
    share = model_ready["organization_id"].value_counts(normalize=True)
    assert share.max() < 0.60, "ninguna organizacion debe dominar el dataset"


def test_no_organization_determines_the_target(model_ready: pd.DataFrame) -> None:
    """La heterogeneidad multiempresa es moderada, no determinista."""
    by_org = model_ready.groupby("organization_id")[TARGET_COLUMN].mean().astype(float)
    assert by_org.min() > 0.05
    assert by_org.max() < 0.95
    assert by_org.max() - by_org.min() < 0.40


def test_extreme_cases_are_represented(frame: pd.DataFrame) -> None:
    assert check_extreme_cases(frame) == []


def test_zero_application_processes_exist(frame: pd.DataFrame) -> None:
    assert (frame["applications_received_count"] == 0).any()


def test_censoring_rate_is_configurable(dataset) -> None:
    high = build_dataset(SyntheticConfig(rows=1_200, stall_rate=0.30))
    low = build_dataset(SyntheticConfig(rows=1_200, stall_rate=0.01))

    assert high.manifest["censoring_ratio"] > low.manifest["censoring_ratio"]
    assert (high.frame["observation_status"] == STATUS_CENSORED).mean() > 0.2


def test_full_validation_suite_passes(dataset) -> None:
    report = validate_dataset(dataset)
    assert report.ok, str(report)
    assert report.warnings == [], str(report)


# --- los guardias de distribucion deben dispararse cuando corresponde -------


def test_count_invariant_guard_detects_a_broken_identity(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    corrupted.loc[0, "evaluations_pending_count"] = (
        int(corrupted.loc[0, "evaluations_pending_count"]) + 3
    )

    assert any("pending" in problem for problem in check_count_invariants(corrupted))


def test_count_invariant_guard_detects_more_completed_than_scheduled(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    corrupted.loc[0, "interviews_completed_count"] = (
        int(corrupted.loc[0, "interviews_scheduled_count"]) + 1
    )

    assert any("completadas > programadas" in problem for problem in check_count_invariants(corrupted))


def test_prevalence_guard_detects_an_out_of_band_dataset(frame: pd.DataFrame) -> None:
    problems = check_prevalence(frame, minimum=0.80, maximum=0.95)
    assert any("fuera de la banda" in problem for problem in problems)


def test_extreme_case_guard_reports_a_missing_scenario(frame: pd.DataFrame) -> None:
    corrupted = frame[frame["applications_received_count"] > 0].copy()

    warnings = check_extreme_cases(corrupted)
    assert any("cero postulaciones" in warning for warning in warnings)


def test_cli_generates_a_dataset_and_prints_its_lineage(tmp_path, capsys) -> None:
    """La CLI es la via de uso real; debe funcionar y no versionar nada."""
    from recruitment_ml.synthetic.generator import main

    destination = tmp_path / "synthetic-test.csv"
    exit_code = main(["--rows", "300", "--months", "36", "--output", str(destination)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert destination.exists()
    assert "dataset_fingerprint" in captured.out
    assert "validity_notice" in captured.out
    assert "fuera del perfil academico aprobado" in captured.err

    written = pd.read_csv(destination)
    assert len(written) == 300
    assert TARGET_COLUMN in written.columns


def test_cli_can_export_only_labelled_rows(tmp_path) -> None:
    from recruitment_ml.synthetic.generator import main

    destination = tmp_path / "model-ready.csv"
    assert main(["--rows", "300", "--model-ready", "--output", str(destination)]) == 0

    written = pd.read_csv(destination)
    assert (written["observation_status"] == "completed").all()
    assert written[TARGET_COLUMN].notna().all()
    assert len(written) < 300, "los censurados deben quedar fuera"
