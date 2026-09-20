"""Simulacion event-first de un proceso de seleccion sintetico.

El orden importa y es el aprobado en la Fase 14: primero se construye una
cronologia de eventos, despues se corta en el checkpoint para derivar las
features, y solo al final se compara el cierre real contra el plazo objetivo
para obtener la etiqueta.

En ningun punto se calcula la etiqueta a partir del vector de features.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import numpy as np

from recruitment_ml.config import LIMA_TZ, SyntheticConfig
from recruitment_ml.synthetic.distributions import (
    bernoulli,
    bounded_choice,
    centered_effect,
    gamma_days,
    lognormal_days,
    negative_binomial_count,
    rare_shock,
    truncated_poisson_count,
)

TZ = ZoneInfo(LIMA_TZ)


def start_of_day(day: date) -> datetime:
    """Inicio del dia en America/Lima."""
    return datetime(day.year, day.month, day.day, 0, 0, 0, tzinfo=TZ)


def end_of_day(day: date) -> datetime:
    """Fin del dia en America/Lima.

    El plazo objetivo es una fecha sin hora, asi que se resuelve al ultimo
    instante del dia, tal como exige `problem-definition.md`.
    """
    return datetime(day.year, day.month, day.day, 23, 59, 59, tzinfo=TZ)


@dataclass(frozen=True)
class OrganizationProfile:
    """Rasgos latentes estables de una organizacion ficticia."""

    organization_id: int
    capacity: float
    volume_scale: float
    friction_base: float


@dataclass(frozen=True)
class LatentFactors:
    """Factores no observables que causan la covariacion.

    Nunca se exportan. Existen para que features y desenlace compartan causa
    sin que el target sea funcion de las features.
    """

    operational_capacity: float
    coordination_friction: float
    workload_pressure: float
    random_shock: float
    period_effect: float


@dataclass
class Session:
    """Evaluacion o entrevista sintetica.

    `created_at` es el instante en que se programa; `scheduled_at`, el momento
    para el que se agenda; `completed_at`, cuando se realiza.
    """

    created_at: datetime
    scheduled_at: datetime
    completed_at: datetime | None = None


@dataclass
class ProcessTimeline:
    """Cronologia completa de un proceso, antes y despues del checkpoint."""

    vacancy_id: int
    organization_id: int
    requested_at: datetime
    published_at: datetime
    opens_at: date | None
    closes_at: date
    checkpoint_at: datetime
    target_set_at: datetime
    target_completion_at: datetime
    positions: int
    criteria_count: int
    stage_count: int
    latent: LatentFactors
    application_times: list[datetime] = field(default_factory=list)
    evaluations: list[Session] = field(default_factory=list)
    interviews: list[Session] = field(default_factory=list)
    stage_events: list[datetime] = field(default_factory=list)
    shortlisted_before_checkpoint: int = 0
    stalled: bool = False
    closed_at: datetime | None = None
    concurrent_open_vacancies_count: int = 0

    # -- derivaciones truncadas en el checkpoint -------------------------

    def _sessions_scheduled(self, sessions: list[Session]) -> int:
        return sum(1 for s in sessions if s.created_at <= self.checkpoint_at)

    def _sessions_completed(self, sessions: list[Session]) -> int:
        return sum(
            1 for s in sessions if s.completed_at is not None and s.completed_at <= self.checkpoint_at
        )

    def _sessions_overdue_pending(self, sessions: list[Session]) -> int:
        return sum(
            1
            for s in sessions
            if s.created_at <= self.checkpoint_at
            and s.scheduled_at < self.checkpoint_at
            and (s.completed_at is None or s.completed_at > self.checkpoint_at)
        )

    def application_window_days(self) -> int:
        """Diferencia entre apertura y cierre de postulaciones.

        Regla de respaldo del contrato: si `opens_at` es nulo se usa la fecha
        de publicacion, porque la columna real es nullable.
        """
        opening = self.opens_at if self.opens_at is not None else self.published_at.date()
        return max(0, (self.closes_at - opening).days)

    def last_operational_event(self) -> datetime:
        """Ultimo evento operacional anterior o igual al checkpoint."""
        candidates: list[datetime] = [self.published_at]
        candidates.extend(t for t in self.application_times if t <= self.checkpoint_at)
        candidates.extend(t for t in self.stage_events if t <= self.checkpoint_at)
        for session in (*self.evaluations, *self.interviews):
            if session.created_at <= self.checkpoint_at:
                candidates.append(session.created_at)
            if session.completed_at is not None and session.completed_at <= self.checkpoint_at:
                candidates.append(session.completed_at)
        return max(candidates)

    def features(self) -> dict[str, int]:
        """Vector operacional del contrato, calculado solo con el pasado."""
        evaluations_scheduled = self._sessions_scheduled(self.evaluations)
        evaluations_completed = self._sessions_completed(self.evaluations)
        interviews_scheduled = self._sessions_scheduled(self.interviews)
        interviews_completed = self._sessions_completed(self.interviews)
        return {
            "elapsed_days_since_publication": (
                self.checkpoint_at.date() - self.published_at.date()
            ).days,
            "application_window_days": self.application_window_days(),
            "positions_count": self.positions,
            "applications_received_count": sum(
                1 for t in self.application_times if t <= self.checkpoint_at
            ),
            "configured_criteria_count": self.criteria_count,
            "evaluations_scheduled_count": evaluations_scheduled,
            "evaluations_completed_count": evaluations_completed,
            "evaluations_overdue_pending_count": self._sessions_overdue_pending(self.evaluations),
            "interviews_scheduled_count": interviews_scheduled,
            "interviews_completed_count": interviews_completed,
            "interviews_overdue_pending_count": self._sessions_overdue_pending(self.interviews),
            "stage_transition_count": sum(1 for t in self.stage_events if t <= self.checkpoint_at),
            "days_since_last_operational_event": (
                self.checkpoint_at.date() - self.last_operational_event().date()
            ).days,
            "concurrent_open_vacancies_count": self.concurrent_open_vacancies_count,
            "days_remaining_to_target": (self.target_completion_at - self.checkpoint_at).days,
            "configured_stage_count": self.stage_count,
            "evaluations_pending_count": evaluations_scheduled - evaluations_completed,
            "interviews_pending_count": interviews_scheduled - interviews_completed,
        }

    def pending_workload(self) -> tuple[int, int, int]:
        """Carga pendiente en el checkpoint: (pendientes, vencidas, sin procesar)."""
        pending = (
            self._sessions_scheduled(self.evaluations)
            - self._sessions_completed(self.evaluations)
            + self._sessions_scheduled(self.interviews)
            - self._sessions_completed(self.interviews)
        )
        overdue = self._sessions_overdue_pending(self.evaluations) + self._sessions_overdue_pending(
            self.interviews
        )
        received = sum(1 for t in self.application_times if t <= self.checkpoint_at)
        unprocessed = max(0, received - self.shortlisted_before_checkpoint)
        return pending, overdue, unprocessed


def simulate_process(
    rng: np.random.Generator,
    config: SyntheticConfig,
    organization: OrganizationProfile,
    vacancy_id: int,
    request_day: date,
    period_effect: float,
    workload_pressure: float,
) -> ProcessTimeline:
    """Construye la cronologia completa de un proceso.

    El plazo objetivo se fija al registrar el requerimiento, antes de publicar,
    y no vuelve a tocarse.
    """
    # 1. Solicitud del requerimiento.
    requested_at = start_of_day(request_day) + timedelta(hours=int(rng.integers(8, 18)))

    # 2. Configuracion de la vacante, conocida antes de publicar.
    positions = bounded_choice(rng, (1, 2, 3, 4), (0.62, 0.24, 0.09, 0.05))
    criteria_count = 3 + truncated_poisson_count(rng, mean=2.2, maximum=5)
    stage_count = 2 if bernoulli(rng, 0.82) else 1
    window_days = gamma_days(rng, shape=4.0, scale=4.0, minimum=3)

    # 3. Publicacion.
    lead_days = gamma_days(rng, shape=3.0, scale=3.0, minimum=1)
    published_day = request_day + timedelta(days=lead_days)
    published_at = start_of_day(published_day) + timedelta(hours=int(rng.integers(8, 18)))

    # 4. Ventana de postulaciones. `opens_at` puede ser nulo, como en el esquema real.
    opens_at: date | None = None if bernoulli(rng, config.null_opens_at_rate) else published_day
    opening_day = opens_at if opens_at is not None else published_day
    closes_at = opening_day + timedelta(days=window_days)

    # 5. Checkpoint: inicio del dia siguiente al cierre de postulaciones.
    checkpoint_at = start_of_day(closes_at + timedelta(days=1))

    # 6. Plazo objetivo, fijado al registrar el requerimiento.
    days_after_close = 4 + gamma_days(rng, shape=5.0, scale=9.0, minimum=0)
    target_completion_at = end_of_day(closes_at + timedelta(days=days_after_close))
    target_set_at = requested_at

    # 7. Factores latentes.
    latent = LatentFactors(
        operational_capacity=organization.capacity * centered_effect(rng, 0.18),
        coordination_friction=organization.friction_base
        * centered_effect(rng, 0.20)
        * (1.0 + config.drift_strength * (period_effect - 1.0)),
        workload_pressure=workload_pressure,
        random_shock=rare_shock(rng, probability=0.035, magnitude=1.6),
        period_effect=period_effect,
    )

    timeline = ProcessTimeline(
        vacancy_id=vacancy_id,
        organization_id=organization.organization_id,
        requested_at=requested_at,
        published_at=published_at,
        opens_at=opens_at,
        closes_at=closes_at,
        checkpoint_at=checkpoint_at,
        target_set_at=target_set_at,
        target_completion_at=target_completion_at,
        positions=positions,
        criteria_count=criteria_count,
        stage_count=stage_count,
        latent=latent,
    )

    # 8. Llegada de postulaciones dentro de la ventana.
    expected_applications = (
        6.5 * organization.volume_scale * (1.0 + 0.45 * (positions - 1)) * period_effect
    )
    application_count = negative_binomial_count(rng, mean=expected_applications, dispersion=2.0)
    window_span = max(1, (closes_at - opening_day).days)
    for _ in range(application_count):
        offset_days = int(rng.integers(0, window_span + 1))
        applied_at = start_of_day(opening_day + timedelta(days=offset_days)) + timedelta(
            hours=int(rng.integers(7, 23))
        )
        if applied_at < published_at:
            applied_at = published_at + timedelta(hours=1)
        timeline.application_times.append(applied_at)
    timeline.application_times.sort()

    # 9. Tramitacion operativa mientras la ventana sigue abierta.
    throughput = float(
        np.clip(latent.operational_capacity / (latent.coordination_friction * latent.random_shock), 0.25, 2.2)
    )
    shortlist_probability = float(np.clip(0.30 + 0.22 * throughput, 0.15, 0.80))
    schedule_probability = float(np.clip(0.38 + 0.30 * throughput, 0.15, 0.92))
    completion_probability = float(np.clip(0.35 + 0.32 * throughput, 0.15, 0.93))

    for applied_at in timeline.application_times:
        if not bernoulli(rng, shortlist_probability):
            continue
        shortlisted_at = applied_at + timedelta(
            days=lognormal_days(rng, median=3.0, sigma=0.7, minimum=1)
        )
        timeline.stage_events.append(shortlisted_at)
        if shortlisted_at > checkpoint_at:
            continue
        timeline.shortlisted_before_checkpoint += 1

        if not bernoulli(rng, schedule_probability):
            continue
        evaluation = _make_session(rng, origin=shortlisted_at, completion_probability=completion_probability)
        timeline.evaluations.append(evaluation)
        timeline.stage_events.append(evaluation.created_at)

        completed_before_checkpoint = (
            evaluation.completed_at is not None and evaluation.completed_at <= checkpoint_at
        )
        if completed_before_checkpoint and bernoulli(rng, schedule_probability * 0.7):
            interview = _make_session(
                rng,
                origin=evaluation.completed_at,
                completion_probability=completion_probability * 0.85,
            )
            timeline.interviews.append(interview)
            timeline.stage_events.append(interview.created_at)

    timeline.stage_events.sort()
    return timeline


def _make_session(
    rng: np.random.Generator, origin: datetime, completion_probability: float
) -> Session:
    """Programa una sesion y decide si llega a realizarse."""
    created_at = origin + timedelta(days=lognormal_days(rng, median=2.0, sigma=0.6, minimum=1))
    scheduled_at = created_at + timedelta(days=lognormal_days(rng, median=6.0, sigma=0.55, minimum=1))
    completed_at: datetime | None = None
    if bernoulli(rng, completion_probability):
        completed_at = scheduled_at + timedelta(hours=int(rng.integers(1, 30)))
    return Session(created_at=created_at, scheduled_at=scheduled_at, completed_at=completed_at)


def resolve_closure(
    rng: np.random.Generator, config: SyntheticConfig, timeline: ProcessTimeline
) -> None:
    """Continuacion estocastica posterior al checkpoint.

    El tiempo restante depende del backlog observable, de los factores latentes
    y de un ruido irreducible. Por eso dos procesos con features identicas
    pueden terminar dentro y fuera de plazo.
    """
    if bernoulli(rng, config.stall_rate):
        timeline.stalled = True
        timeline.closed_at = None
        return

    # Coeficientes calibrados para que la configuracion por defecto
    # (`delay_pressure=1.0`) situe la prevalencia en el centro de la banda
    # aprobada 25-40 %. La calibracion es estructural: ajusta el proceso, no
    # filtra etiquetas ni remuestrea el resultado.
    pending, overdue, unprocessed = timeline.pending_workload()
    base_days = (
        9.25
        + 1.75 * pending
        + 2.38 * overdue
        + 0.56 * unprocessed
        + 1.13 * timeline.positions
        + 0.83 * timeline.criteria_count
    )
    latent = timeline.latent
    friction = (
        latent.coordination_friction
        * (1.0 + 0.30 * latent.workload_pressure)
        * latent.random_shock
        / max(latent.operational_capacity, 0.2)
    )
    noise = float(rng.lognormal(mean=0.0, sigma=0.45))
    remaining_days = max(3, int(round(base_days * friction * noise * config.delay_pressure)))
    timeline.closed_at = timeline.checkpoint_at + timedelta(
        days=remaining_days, hours=int(rng.integers(9, 18))
    )
