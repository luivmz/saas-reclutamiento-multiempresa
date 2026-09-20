"""Ausencia de fuga de informacion.

Validaciones 8, 9, 13 y 14. Un dataset con fuga produce metricas excelentes y
conclusiones falsas: es el modo de fallo mas peligroso de todo el experimento.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from datetime import timedelta

import numpy as np
import pandas as pd

from recruitment_ml.schema import MODEL_READY_FEATURES, STATUS_CENSORED, STATUS_COMPLETED, TARGET_COLUMN
from recruitment_ml.synthetic.generator import build_dataset
from recruitment_ml.synthetic.timeline import ProcessTimeline, Session, stall_probability
from recruitment_ml.synthetic.validators import SUSPICIOUS_CORRELATION, check_censoring, check_leakage_signals


def test_events_after_the_checkpoint_do_not_change_any_feature(
    timelines: list[ProcessTimeline],
) -> None:
    """La prueba decisiva: el futuro no puede tocar el vector de features."""
    timeline = timelines[0]
    before = timeline.features()

    future = timeline.checkpoint_at + timedelta(days=5)
    timeline.evaluations.append(
        Session(created_at=future, scheduled_at=future + timedelta(days=2), completed_at=future + timedelta(days=3))
    )
    timeline.interviews.append(
        Session(created_at=future, scheduled_at=future + timedelta(days=1), completed_at=None)
    )
    timeline.application_times.append(future)
    timeline.stage_events.append(future)

    assert timeline.features() == before


def test_sessions_completed_after_the_checkpoint_are_not_counted_as_completed(
    timelines: list[ProcessTimeline],
) -> None:
    timeline = timelines[1]
    before = timeline.features()["evaluations_completed_count"]

    created = timeline.checkpoint_at - timedelta(days=3)
    timeline.evaluations.append(
        Session(
            created_at=created,
            scheduled_at=timeline.checkpoint_at - timedelta(days=1),
            completed_at=timeline.checkpoint_at + timedelta(days=4),
        )
    )
    after = timeline.features()

    assert after["evaluations_completed_count"] == before
    # Programada antes y aun sin realizar en el checkpoint: cuenta como vencida.
    assert after["evaluations_overdue_pending_count"] >= 1


def test_no_feature_correlates_suspiciously_with_the_target(frame: pd.DataFrame) -> None:
    assert check_leakage_signals(frame) == []


def test_the_strongest_signal_is_informative_but_far_from_deterministic(
    model_ready: pd.DataFrame,
) -> None:
    target = model_ready[TARGET_COLUMN].astype(float)
    correlations = {
        column: abs(float(np.corrcoef(model_ready[column].astype(float), target)[0, 1]))
        for column in MODEL_READY_FEATURES
        if model_ready[column].std(ddof=0) > 0
    }
    strongest = max(correlations.values())

    assert strongest > 0.05, "el dataset deberia contener senal operacional real"
    assert strongest < SUSPICIOUS_CORRELATION, "una correlacion casi perfecta delataria fuga"


def test_similar_processes_can_end_differently(model_ready: pd.DataFrame) -> None:
    """Solapamiento de clases: sin el, el target seria una regla disfrazada."""
    profile = pd.DataFrame(
        {
            "remaining": pd.qcut(model_ready["days_remaining_to_target"], 4, labels=False, duplicates="drop"),
            "volume": pd.qcut(
                model_ready["applications_received_count"].rank(method="first"),
                4,
                labels=False,
                duplicates="drop",
            ),
            "overdue": np.minimum(model_ready["evaluations_overdue_pending_count"], 2),
        }
    )
    grouped = model_ready[TARGET_COLUMN].astype(int).groupby(
        [profile["remaining"], profile["volume"], profile["overdue"]]
    )
    summary = grouped.agg(["size", "mean"])
    mixed = (summary["mean"] > 0) & (summary["mean"] < 1)
    covered = float(summary.loc[mixed, "size"].sum() / summary["size"].sum())

    assert covered > 0.80, (
        "la mayoria de los procesos debe vivir en perfiles donde ocurren ambos desenlaces"
    )


def test_censored_processes_never_receive_a_label(frame: pd.DataFrame) -> None:
    censored = frame[frame["observation_status"] == STATUS_CENSORED]

    assert not censored.empty, "el dataset debe contener procesos censurados"
    assert censored[TARGET_COLUMN].isna().all()
    assert check_censoring(frame) == []


def test_completed_processes_always_receive_a_label(frame: pd.DataFrame) -> None:
    completed = frame[frame["observation_status"] == STATUS_COMPLETED]
    assert completed[TARGET_COLUMN].notna().all()
    assert set(completed[TARGET_COLUMN].unique()) == {0, 1}


def test_model_ready_excludes_every_censored_process(dataset) -> None:
    ready = dataset.model_ready()
    assert (ready["observation_status"] == STATUS_COMPLETED).all()
    assert ready[TARGET_COLUMN].notna().all()
    assert len(ready) == dataset.manifest["rows_model_ready"]
    assert len(ready) + dataset.manifest["censored_total"] == dataset.manifest["rows_generated"]


def test_censoring_statistics_are_reported(dataset) -> None:
    """La decision 10 exige conservar la estadistica, no solo excluir filas."""
    manifest = dataset.manifest
    assert manifest["censored_total"] > 0
    assert manifest["censored_stalled"] >= 0
    assert manifest["censored_observation_window"] >= 0
    assert (
        manifest["censored_stalled"] + manifest["censored_observation_window"]
        == manifest["censored_total"]
    )
    assert 0.0 < manifest["censoring_ratio"] < 0.5


def test_target_is_derived_only_from_the_final_closure(timelines: list[ProcessTimeline]) -> None:
    """Un proceso sin cierre no puede producir etiqueta por ningun camino."""
    stalled = [t for t in timelines if t.closed_at is None]
    assert stalled
    for timeline in stalled:
        assert "delayed" not in timeline.features()


# --- los guardias de fuga deben dispararse cuando corresponde ---------------


def test_leakage_guard_detects_a_target_revealing_column(model_ready: pd.DataFrame) -> None:
    """Si una feature copiase el target, la validacion tiene que gritarlo."""
    corrupted = model_ready.copy()
    corrupted["days_remaining_to_target"] = corrupted[TARGET_COLUMN].astype(int) * 100 + 1

    problems = check_leakage_signals(corrupted)
    assert any("sospechosa" in problem for problem in problems)


def test_censoring_guard_detects_a_labelled_censored_row(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    censored_index = corrupted.index[corrupted["observation_status"] == STATUS_CENSORED][0]
    corrupted.loc[censored_index, TARGET_COLUMN] = 0

    problems = check_censoring(corrupted)
    assert any("censurados con etiqueta" in problem for problem in problems)


def test_censoring_guard_detects_an_unlabelled_completed_row(frame: pd.DataFrame) -> None:
    corrupted = frame.copy()
    completed_index = corrupted.index[corrupted["observation_status"] == STATUS_COMPLETED][0]
    corrupted.loc[completed_index, TARGET_COLUMN] = pd.NA

    problems = check_censoring(corrupted)
    assert any("completados sin etiqueta" in problem for problem in problems)


# --- MEDIUM-03: la censura es informativa, no MCAR ni determinista --------


def test_stall_probability_depends_on_operational_conditions(
    config, timelines: list[ProcessTimeline]
) -> None:
    """Mas friccion y menos capacidad deben elevar el riesgo de estancamiento."""
    easy = deepcopy(timelines[0])
    hard = deepcopy(timelines[0])
    easy.latent = replace(
        easy.latent, coordination_friction=0.6, operational_capacity=1.6, workload_pressure=0.5
    )
    hard.latent = replace(
        hard.latent, coordination_friction=1.7, operational_capacity=0.7, workload_pressure=2.5
    )

    assert stall_probability(config, hard) > stall_probability(config, easy), (
        "la censura debe depender de las condiciones operacionales"
    )


def test_stall_probability_rises_with_inactivity(config, timelines: list[ProcessTimeline]) -> None:
    active = deepcopy(timelines[0])
    idle = deepcopy(timelines[0])
    idle.application_times.clear()
    idle.stage_events.clear()
    idle.evaluations.clear()
    idle.interviews.clear()

    assert stall_probability(config, idle) >= stall_probability(config, active)


def test_stall_probability_is_never_deterministic(
    config, timelines: list[ProcessTimeline]
) -> None:
    """Ningun proceso puede tener censura garantizada ni imposible."""
    probabilities = [stall_probability(config, timeline) for timeline in timelines]

    assert all(0.0 < value < 1.0 for value in probabilities)
    assert max(probabilities) <= 0.60
    assert min(probabilities) >= 0.005


def test_censored_and_completed_differ_without_separating_perfectly(dataset) -> None:
    """Debe haber diferencia medible y, a la vez, solapamiento amplio."""
    comparison = dataset.manifest["censoring_comparison"]
    assert comparison["available"]

    differences = comparison["standardised_mean_differences"]
    largest = max(abs(value) for value in differences.values())

    assert largest > 0.05, "la censura seria practicamente MCAR"
    assert largest < 1.5, "una separacion tan grande delataria censura casi determinista"
    assert dataset.manifest["censoring_mechanism"] == "informative-by-design"


def test_censored_and_completed_overlap_in_the_feature_space(frame: pd.DataFrame) -> None:
    censored = frame[frame["observation_status"] == STATUS_CENSORED]
    completed = frame[frame["observation_status"] == STATUS_COMPLETED]

    for column in ("days_since_last_operational_event", "applications_received_count"):
        low = max(censored[column].min(), completed[column].min())
        high = min(censored[column].max(), completed[column].max())
        assert low <= high, f"{column}: los rangos no se solapan"


def test_censoring_is_reproducible(dataset) -> None:
    repeated = build_dataset(dataset.config)

    assert repeated.manifest["censored_total"] == dataset.manifest["censored_total"]
    assert repeated.manifest["censoring_ratio"] == dataset.manifest["censoring_ratio"]
    pd.testing.assert_series_equal(
        repeated.frame["observation_status"], dataset.frame["observation_status"]
    )


def test_censoring_ratio_stays_in_a_reasonable_range(dataset) -> None:
    ratio = dataset.manifest["censoring_ratio"]
    assert 0.01 < ratio < 0.30, f"tasa de censura fuera de rango razonable: {ratio}"
