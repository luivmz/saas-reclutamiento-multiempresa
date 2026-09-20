"""Integridad temporal de la cronologia.

Validaciones 6, 7, 8 y 9. El checkpoint y el plazo objetivo son el corazon del
diseno aprobado: si su orden se rompe, el problema deja de ser una prediccion.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd

from recruitment_ml.config import LIMA_TZ
from recruitment_ml.synthetic.timeline import ProcessTimeline, start_of_day


def test_chronological_order_holds(timelines: list[ProcessTimeline]) -> None:
    for timeline in timelines:
        assert timeline.requested_at <= timeline.published_at
        assert timeline.published_at.date() <= timeline.closes_at
        assert timeline.published_at < timeline.checkpoint_at
        assert start_of_day(timeline.closes_at) < timeline.checkpoint_at


def test_checkpoint_is_the_start_of_the_day_after_applications_close(
    timelines: list[ProcessTimeline],
) -> None:
    for timeline in timelines:
        expected = start_of_day(timeline.closes_at + timedelta(days=1))
        assert timeline.checkpoint_at == expected
        assert timeline.checkpoint_at.hour == 0
        assert timeline.checkpoint_at.minute == 0
        assert timeline.checkpoint_at.second == 0


def test_all_timestamps_are_lima_aware(timelines: list[ProcessTimeline]) -> None:
    """Sin zona explicita, comparar fechas seria una fuente silenciosa de error."""
    for timeline in timelines:
        for moment in (
            timeline.requested_at,
            timeline.published_at,
            timeline.checkpoint_at,
            timeline.target_completion_at,
            timeline.target_set_at,
        ):
            assert isinstance(moment, datetime)
            assert moment.tzinfo is not None
            assert str(moment.tzinfo) == LIMA_TZ


def test_target_is_fixed_before_publication_and_after_the_checkpoint(
    timelines: list[ProcessTimeline],
) -> None:
    for timeline in timelines:
        assert timeline.target_set_at <= timeline.published_at
        assert timeline.target_completion_at > timeline.checkpoint_at


def test_target_resolves_to_the_end_of_its_day(timelines: list[ProcessTimeline]) -> None:
    """El plazo es una fecha sin hora: se resuelve al ultimo instante del dia."""
    for timeline in timelines:
        assert (timeline.target_completion_at.hour, timeline.target_completion_at.minute) == (23, 59)


def test_target_is_immutable_across_the_simulation(timelines: list[ProcessTimeline]) -> None:
    """El plazo no puede reajustarse durante el proceso: filtraria el desenlace."""
    for timeline in timelines:
        snapshot = timeline.target_completion_at
        timeline.features()
        timeline.pending_workload()
        assert timeline.target_completion_at == snapshot


def test_closure_happens_after_the_checkpoint(timelines: list[ProcessTimeline]) -> None:
    for timeline in timelines:
        if timeline.closed_at is not None:
            assert timeline.closed_at > timeline.checkpoint_at


def test_stalled_processes_never_close(timelines: list[ProcessTimeline]) -> None:
    """Refleja el hecho verificado: cerrar exige decision y seleccion humanas."""
    stalled = [t for t in timelines if t.stalled]
    assert stalled, "la muestra deberia contener procesos estancados"
    for timeline in stalled:
        assert timeline.closed_at is None


def test_elapsed_and_remaining_days_are_strictly_positive(frame: pd.DataFrame) -> None:
    assert (frame["elapsed_days_since_publication"] > 0).all()
    assert (frame["days_remaining_to_target"] > 0).all()


def test_checkpoints_are_parseable_and_carry_an_offset(frame: pd.DataFrame) -> None:
    parsed = pd.to_datetime(frame["checkpoint_at"], utc=True)
    assert parsed.notna().all()
    assert frame["checkpoint_at"].str.contains("-05:00").all()


def test_application_window_falls_back_to_publication_when_opens_at_is_null(
    timelines: list[ProcessTimeline],
) -> None:
    """La columna real es nullable; la regla de respaldo debe ejercitarse."""
    without_opening = [t for t in timelines if t.opens_at is None]
    assert without_opening, "la muestra deberia incluir vacantes sin opens_at"
    for timeline in without_opening:
        expected = (timeline.closes_at - timeline.published_at.date()).days
        assert timeline.application_window_days() == expected
