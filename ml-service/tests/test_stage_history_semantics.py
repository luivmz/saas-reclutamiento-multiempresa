"""Semantica del historial de etapas (HIGH-01).

El dominio real, verificado en codigo:

- `ApplicationService::apply()` crea **un** `ApplicationStageHistory` inicial
  (`null -> postulado`) en el mismo instante que `applied_at`
  (`app/Services/Applications/ApplicationService.php:60-67`), y la prueba
  `tests/Feature/Applications/ApplyToVacancyTest.php:51` afirma que tras
  postular existe exactamente 1 fila de historial;
- `ApplicationStageService::transition()` crea **uno** por cada cambio de etapa
  posterior (`app/Services/Applications/ApplicationStageService.php:71`).

Por tanto `stage_transition_count` nunca puede ser menor que el numero de
postulaciones anteriores al checkpoint.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pandas as pd
import pytest

from recruitment_ml.synthetic.timeline import (
    LatentFactors,
    ProcessTimeline,
    Session,
    start_of_day,
)


def _bare_timeline(closes: date = date(2024, 3, 10)) -> ProcessTimeline:
    """Cronologia minima y controlada, sin aleatoriedad."""
    published = start_of_day(date(2024, 2, 20)) + timedelta(hours=9)
    return ProcessTimeline(
        vacancy_id=1,
        organization_id=1,
        requested_at=start_of_day(date(2024, 2, 10)),
        published_at=published,
        opens_at=date(2024, 2, 22),
        closes_at=closes,
        checkpoint_at=start_of_day(closes + timedelta(days=1)),
        target_set_at=start_of_day(date(2024, 2, 10)),
        target_completion_at=start_of_day(closes + timedelta(days=40)),
        positions=1,
        criteria_count=4,
        stage_count=2,
        latent=LatentFactors(1.0, 1.0, 1.0, 1.0, 1.0),
    )


def test_a_single_application_produces_at_least_one_history_entry() -> None:
    """Escenario minimo: una postulacion equivale a un historial inicial."""
    timeline = _bare_timeline()
    applied_at = start_of_day(date(2024, 3, 1)) + timedelta(hours=10)
    timeline.application_times.append(applied_at)
    timeline.stage_events.append(applied_at)

    features = timeline.features()
    assert features["applications_received_count"] == 1
    assert features["stage_transition_count"] >= 1


def test_every_application_before_the_checkpoint_contributes_its_initial_history() -> None:
    timeline = _bare_timeline()
    for day in (1, 2, 3, 4, 5):
        moment = start_of_day(date(2024, 3, day)) + timedelta(hours=11)
        timeline.application_times.append(moment)
        timeline.stage_events.append(moment)

    features = timeline.features()
    assert features["applications_received_count"] == 5
    assert features["stage_transition_count"] == 5


def test_applications_after_the_checkpoint_do_not_count() -> None:
    timeline = _bare_timeline()
    before = start_of_day(date(2024, 3, 5)) + timedelta(hours=9)
    after = timeline.checkpoint_at + timedelta(days=4)
    for moment in (before, after):
        timeline.application_times.append(moment)
        timeline.stage_events.append(moment)

    features = timeline.features()
    assert features["applications_received_count"] == 1
    assert features["stage_transition_count"] == 1


def test_additional_transitions_add_to_the_initial_history() -> None:
    """Historial inicial + preseleccion + paso a evaluacion = 3 eventos."""
    timeline = _bare_timeline()
    applied_at = start_of_day(date(2024, 3, 1)) + timedelta(hours=10)
    shortlisted_at = applied_at + timedelta(days=2)
    moved_to_evaluation_at = shortlisted_at + timedelta(days=1)
    timeline.application_times.append(applied_at)
    timeline.stage_events.extend([applied_at, shortlisted_at, moved_to_evaluation_at])

    features = timeline.features()
    assert features["applications_received_count"] == 1
    assert features["stage_transition_count"] == 3


def test_transitions_after_the_checkpoint_are_excluded() -> None:
    timeline = _bare_timeline()
    applied_at = start_of_day(date(2024, 3, 1)) + timedelta(hours=10)
    timeline.application_times.append(applied_at)
    timeline.stage_events.extend(
        [applied_at, applied_at + timedelta(days=2), timeline.checkpoint_at + timedelta(days=3)]
    )

    assert timeline.features()["stage_transition_count"] == 2


def test_a_process_without_applications_has_no_stage_history() -> None:
    timeline = _bare_timeline()

    features = timeline.features()
    assert features["applications_received_count"] == 0
    assert features["stage_transition_count"] == 0


# --- la invariante debe cumplirse en el dataset completo -------------------


def test_stage_transitions_never_fall_below_applications(frame: pd.DataFrame) -> None:
    """La regresion que motivo HIGH-01: antes fallaba en gran parte de las filas."""
    shortfall = frame["stage_transition_count"] < frame["applications_received_count"]

    assert not shortfall.any(), (
        f"{int(shortfall.sum())} filas tienen menos historiales que postulaciones; "
        "cada Application crea un ApplicationStageHistory inicial"
    )


def test_processes_without_applications_report_no_transitions(frame: pd.DataFrame) -> None:
    empty = frame[frame["applications_received_count"] == 0]

    assert not empty.empty, "el dataset deberia contener convocatorias sin postulaciones"
    assert (empty["stage_transition_count"] == 0).all()


def test_transitions_exceed_applications_when_the_process_advances(frame: pd.DataFrame) -> None:
    """Preseleccionar y mover de etapa anade historiales sobre el inicial."""
    advanced = frame[frame["evaluations_scheduled_count"] > 0]

    assert not advanced.empty
    assert (advanced["stage_transition_count"] > advanced["applications_received_count"]).any()


@pytest.mark.parametrize("column", ["stage_transition_count", "applications_received_count"])
def test_counts_are_non_negative(frame: pd.DataFrame, column: str) -> None:
    assert (frame[column] >= 0).all()
