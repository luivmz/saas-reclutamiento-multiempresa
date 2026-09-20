"""Orquestacion del dataset sintetico y CLI.

Uso:

    python -m recruitment_ml.synthetic.generator --rows 6000 --seed 20260920 \
        --output artifacts/synthetic-v1.csv

El archivo generado nunca se versiona.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from calendar import monthrange
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from recruitment_ml.config import (
    DATASET_VERSION,
    DEFAULT_SEED,
    SyntheticConfig,
    validate_academic_profile,
)
from recruitment_ml.schema import (
    DATASET_COLUMNS,
    INTEGER_COLUMNS,
    MODEL_READY_FEATURES,
    STATUS_CENSORED,
    STATUS_COMPLETED,
    TARGET_COLUMN,
)
from recruitment_ml.synthetic.distributions import centered_effect
from recruitment_ml.synthetic.timeline import (
    OrganizationProfile,
    ProcessTimeline,
    resolve_closure,
    simulate_process,
    start_of_day,
)

__all__ = ["SyntheticDataset", "build_dataset", "main"]


@dataclass(frozen=True)
class SyntheticDataset:
    """Dataset generado junto con su manifiesto de linaje."""

    frame: pd.DataFrame
    manifest: dict[str, Any]
    config: SyntheticConfig

    def model_ready(self) -> pd.DataFrame:
        """Subconjunto etiquetado: excluye los procesos censurados.

        Los censurados no reciben etiqueta artificial; simplemente no forman
        parte del conjunto supervisado.
        """
        completed = self.frame[self.frame["observation_status"] == STATUS_COMPLETED]
        return completed.reset_index(drop=True)

    def feature_matrix(self) -> pd.DataFrame:
        """Matriz X: solo las features model-ready del contrato."""
        return self.model_ready()[list(MODEL_READY_FEATURES)]

    def prevalence(self) -> float:
        ready = self.model_ready()
        if ready.empty:
            return float("nan")
        return float(ready[TARGET_COLUMN].mean())


def _add_months(anchor: date, months: int) -> date:
    """Suma meses conservando un dia valido."""
    total = anchor.month - 1 + months
    year = anchor.year + total // 12
    month = total % 12 + 1
    day = min(anchor.day, monthrange(year, month)[1])
    return date(year, month, day)


def _normalised_effects(rng: np.random.Generator, count: int, sigma: float, low: float, high: float) -> list[float]:
    """Efectos multiplicativos con media geometrica exactamente 1.

    La normalizacion importa: con pocas organizaciones, la media muestral de
    un sorteo lognormal se desplaza segun la seed y arrastraria consigo la
    prevalencia global. Normalizando, los perfiles describen heterogeneidad
    *relativa* entre organizaciones y el nivel agregado deja de depender del
    azar de la seed.
    """
    draws = np.array([centered_effect(rng, sigma) for _ in range(count)], dtype=float)
    draws = draws / float(np.exp(np.log(draws).mean()))
    return [float(np.clip(value, low, high)) for value in draws]


def _build_organizations(rng: np.random.Generator, count: int) -> list[OrganizationProfile]:
    """Organizaciones ficticias con rasgos latentes moderadamente distintos.

    Las diferencias son suficientes para que la heterogeneidad multiempresa
    sea visible, pero ninguna organizacion determina el desenlace.
    """
    capacities = _normalised_effects(rng, count, sigma=0.22, low=0.55, high=1.9)
    volumes = _normalised_effects(rng, count, sigma=0.28, low=0.45, high=2.1)
    frictions = _normalised_effects(rng, count, sigma=0.20, low=0.6, high=1.8)
    return [
        OrganizationProfile(
            organization_id=index + 1,
            capacity=capacities[index],
            volume_scale=volumes[index],
            friction_base=frictions[index],
        )
        for index in range(count)
    ]


def build_dataset(config: SyntheticConfig | None = None) -> SyntheticDataset:
    """Genera el dataset completo siguiendo el orden event-first aprobado."""
    config = config or SyntheticConfig()
    rng = np.random.default_rng(config.seed)

    organizations = _build_organizations(rng, config.organizations)

    # --- asignacion de procesos a (organizacion, mes) -------------------
    # El drift temporal aumenta suavemente el volumen a lo largo del periodo.
    month_weights = np.array(
        [1.0 + config.drift_strength * (index / max(config.months - 1, 1)) for index in range(config.months)],
        dtype=float,
    )
    month_weights /= month_weights.sum()
    org_weights = np.array([org.volume_scale for org in organizations], dtype=float)
    org_weights /= org_weights.sum()

    month_index = rng.choice(config.months, size=config.rows, p=month_weights)
    org_index = rng.choice(len(organizations), size=config.rows, p=org_weights)

    # Presion de carga latente por (organizacion, mes).
    #
    # Se sortea como factor propio, no como recuento de filas de la celda: si
    # dependiera del recuento, su varianza cambiaria con `rows` y la
    # prevalencia dejaria de ser una propiedad de la simulacion para volverse
    # un artefacto del tamano de muestra. La feature observable
    # `concurrent_open_vacancies_count` sigue correlacionando con ella porque
    # ambas dependen del drift y del volumen de la organizacion.
    pressure_map: dict[tuple[int, int], float] = {}
    for org_i in range(len(organizations)):
        for month_i in range(config.months):
            drift = 1.0 + config.drift_strength * (month_i / max(config.months - 1, 1))
            pressure_map[(org_i, month_i)] = float(
                np.clip(centered_effect(rng, 0.30) * drift, 0.2, 3.5)
            )

    # --- simulacion proceso a proceso -----------------------------------
    timelines: list[ProcessTimeline] = []
    for row in range(config.rows):
        org_i = int(org_index[row])
        month_i = int(month_index[row])
        organization = organizations[org_i]

        month_start = _add_months(config.start_date, month_i)
        days_in_month = monthrange(month_start.year, month_start.month)[1]
        request_day = date(month_start.year, month_start.month, int(rng.integers(1, days_in_month + 1)))

        period_effect = 1.0 + config.drift_strength * (month_i / max(config.months - 1, 1))
        workload_pressure = pressure_map[(org_i, month_i)]

        timeline = simulate_process(
            rng=rng,
            config=config,
            organization=organization,
            vacancy_id=row + 1,
            request_day=request_day,
            period_effect=period_effect,
            workload_pressure=workload_pressure,
        )
        resolve_closure(rng, config, timeline)
        timelines.append(timeline)

    # --- segunda pasada: concurrencia observable en el checkpoint --------
    _assign_concurrency(timelines)

    # --- ventana observacional y estado de cada proceso -----------------
    observation_end = start_of_day(
        _add_months(config.start_date, config.months + config.observation_tail_months)
    )

    records: list[dict[str, Any]] = []
    censored_stalled = 0
    censored_window = 0
    for timeline in timelines:
        features = timeline.features()

        if timeline.closed_at is None:
            status = STATUS_CENSORED
            delayed: int | None = None
            censored_stalled += 1
        elif timeline.closed_at > observation_end:
            status = STATUS_CENSORED
            delayed = None
            censored_window += 1
        else:
            status = STATUS_COMPLETED
            # La etiqueta se deriva al final, comparando cierre real contra plazo.
            delayed = int(timeline.closed_at > timeline.target_completion_at)

        record: dict[str, Any] = {
            "vacancy_id": timeline.vacancy_id,
            "organization_id": timeline.organization_id,
            "checkpoint_at": timeline.checkpoint_at.isoformat(),
            "observation_status": status,
            "dataset_version": config.dataset_version,
            TARGET_COLUMN: delayed,
        }
        record.update(features)
        records.append(record)

    frame = pd.DataFrame.from_records(records)
    frame = frame[list(DATASET_COLUMNS)]
    for column in INTEGER_COLUMNS:
        frame[column] = frame[column].astype("int64")
    frame[TARGET_COLUMN] = frame[TARGET_COLUMN].astype("Int64")

    manifest = _build_manifest(
        config=config,
        frame=frame,
        censored_stalled=censored_stalled,
        censored_window=censored_window,
        observation_end=observation_end,
    )
    return SyntheticDataset(frame=frame, manifest=manifest, config=config)


def _assign_concurrency(timelines: list[ProcessTimeline]) -> None:
    """Cuenta vacantes abiertas de la misma organizacion en cada checkpoint.

    Una vacante esta abierta si ya se publico y aun no se habia cerrado en ese
    instante. Es informacion disponible en el checkpoint: no mira al futuro.
    """
    by_org: dict[int, list[ProcessTimeline]] = {}
    for timeline in timelines:
        by_org.setdefault(timeline.organization_id, []).append(timeline)

    for group in by_org.values():
        published = np.array([t.published_at.timestamp() for t in group])
        closed = np.array(
            [t.closed_at.timestamp() if t.closed_at is not None else np.inf for t in group]
        )
        for index, timeline in enumerate(group):
            moment = timeline.checkpoint_at.timestamp()
            open_mask = (published <= moment) & (closed > moment)
            open_mask[index] = False
            timeline.concurrent_open_vacancies_count = int(open_mask.sum())


def dataset_fingerprint(frame: pd.DataFrame) -> str:
    """Hash estable del contenido del dataset."""
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _build_manifest(
    config: SyntheticConfig,
    frame: pd.DataFrame,
    censored_stalled: int,
    censored_window: int,
    observation_end: datetime,
) -> dict[str, Any]:
    """Manifiesto de linaje. Sin el, un resultado no es reproducible."""
    completed = frame[frame["observation_status"] == STATUS_COMPLETED]
    censored_total = censored_stalled + censored_window
    prevalence = float(completed[TARGET_COLUMN].mean()) if not completed.empty else float("nan")

    return {
        "dataset_version": config.dataset_version,
        "feature_contract_version": config.feature_contract_version,
        "seed": config.seed,
        "config_fingerprint": config.fingerprint(),
        "dataset_fingerprint": dataset_fingerprint(frame),
        "rows_generated": int(len(frame)),
        "rows_model_ready": int(len(completed)),
        "censored_total": censored_total,
        "censored_stalled": censored_stalled,
        "censored_observation_window": censored_window,
        "censoring_ratio": round(censored_total / max(len(frame), 1), 6),
        "prevalence": None if np.isnan(prevalence) else round(prevalence, 6),
        "prevalence_target": [config.prevalence_min, config.prevalence_max],
        "observation_end": observation_end.isoformat(),
        "model_ready_features": list(MODEL_READY_FEATURES),
        "academic_profile_deviations": validate_academic_profile(config),
        "tool": "recruitment_ml.synthetic.generator",
        "data_nature": "synthetic",
        "validity_notice": (
            "Los datos sinteticos permiten demostrar metodologia, entrenamiento, "
            "integracion y evaluacion tecnica. No demuestran validez predictiva real "
            "sobre procesos del Colegio Andino de Huancayo ni autorizan uso institucional."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada de la CLI."""
    parser = argparse.ArgumentParser(
        prog="recruitment_ml.synthetic.generator",
        description="Genera el dataset sintetico academico (Fase 15A). No versionar la salida.",
    )
    parser.add_argument("--rows", type=int, default=6_000, help="Numero de procesos (aprobado 5000-10000)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Seed maestra")
    parser.add_argument("--organizations", type=int, default=6, help="Organizaciones ficticias (aprobado 4-8)")
    parser.add_argument("--months", type=int, default=42, help="Meses sinteticos (minimo aprobado 36)")
    parser.add_argument("--output", type=Path, default=None, help="Ruta CSV de salida (ignorada por Git)")
    parser.add_argument(
        "--model-ready",
        action="store_true",
        help="Exporta solo las filas etiquetadas, sin censurados",
    )
    args = parser.parse_args(argv)

    config = SyntheticConfig(
        rows=args.rows,
        seed=args.seed,
        organizations=args.organizations,
        months=args.months,
        output_path=args.output,
        dataset_version=DATASET_VERSION,
    )
    dataset = build_dataset(config)

    deviations = dataset.manifest["academic_profile_deviations"]
    if deviations:
        print("AVISO: configuracion fuera del perfil academico aprobado:", file=sys.stderr)
        for item in deviations:
            print(f"  - {item}", file=sys.stderr)

    frame = dataset.model_ready() if args.model_ready else dataset.frame
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(args.output, index=False, lineterminator="\n")
        print(f"dataset escrito en {args.output}")

    for key in (
        "dataset_version",
        "seed",
        "config_fingerprint",
        "dataset_fingerprint",
        "rows_generated",
        "rows_model_ready",
        "censored_total",
        "censoring_ratio",
        "prevalence",
    ):
        print(f"{key}: {dataset.manifest[key]}")
    print(f"validity_notice: {dataset.manifest['validity_notice']}")
    return 0


if __name__ == "__main__":  # pragma: no cover - entrada de linea de comandos
    raise SystemExit(main())
