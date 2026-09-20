"""Validaciones automaticas del dataset sintetico.

Implementan la lista aprobada en `docs/v1.1/ml/dataset-specification.md`
seccion 5. Cada funcion devuelve los problemas encontrados; una lista vacia
significa que la invariante se cumple.

Estas validaciones no son decorativas: son la defensa contra un dataset con
fuga, con etiquetas artificiales o con columnas prohibidas.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from recruitment_ml.schema import (
    ABLATION_FEATURES,
    AUXILIARY_COLUMNS,
    DATASET_COLUMNS,
    INTEGER_COLUMNS,
    LATENT_FACTORS,
    METADATA_COLUMNS,
    MODEL_READY_FEATURES,
    STATUS_CENSORED,
    STATUS_COMPLETED,
    TARGET_COLUMN,
    is_forbidden_column,
)

#: Umbral por encima del cual una correlacion feature-target exige revision
#: manual de fuga. No es un limite estadistico universal: es un disparador.
SUSPICIOUS_CORRELATION = 0.92


@dataclass
class ValidationReport:
    """Resultado de validar un dataset."""

    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def extend(self, problems: list[str]) -> None:
        self.issues.extend(problems)

    def __str__(self) -> str:  # pragma: no cover - ayuda de diagnostico
        if self.ok and not self.warnings:
            return "dataset valido"
        lines = [f"issues={len(self.issues)} warnings={len(self.warnings)}"]
        lines.extend(f"  ISSUE: {item}" for item in self.issues)
        lines.extend(f"  WARN : {item}" for item in self.warnings)
        return "\n".join(lines)


def check_columns(frame: pd.DataFrame) -> list[str]:
    """Validaciones 5, 10, 11 y 18: columnas, prohibidas, latentes y tipos."""
    problems: list[str] = []

    expected = list(DATASET_COLUMNS)
    if list(frame.columns) != expected:
        problems.append(f"columnas inesperadas: {list(frame.columns)!r} != {expected!r}")

    for column in frame.columns:
        if is_forbidden_column(column):
            problems.append(f"columna prohibida presente: {column!r}")

    for latent in LATENT_FACTORS:
        if latent in frame.columns:
            problems.append(f"factor latente exportado: {latent!r}")

    for column in INTEGER_COLUMNS:
        if column in frame.columns and not pd.api.types.is_integer_dtype(frame[column]):
            problems.append(f"columna {column!r} deberia ser entera, es {frame[column].dtype}")

    if TARGET_COLUMN in frame.columns and str(frame[TARGET_COLUMN].dtype) != "Int64":
        problems.append(f"{TARGET_COLUMN!r} deberia ser Int64 nullable, es {frame[TARGET_COLUMN].dtype}")

    return problems


def check_uniqueness(frame: pd.DataFrame) -> list[str]:
    """Validaciones 3 y 17: una fila por proceso, sin duplicados."""
    problems: list[str] = []
    if frame["vacancy_id"].duplicated().any():
        problems.append("hay vacancy_id duplicados: la unidad de analisis exige una fila por proceso")
    if frame.duplicated(subset=["vacancy_id", "checkpoint_at"]).any():
        problems.append("hay pares (vacancy_id, checkpoint_at) duplicados")
    return problems


def check_ranges(frame: pd.DataFrame) -> list[str]:
    """Validaciones 14 y 19: rangos validos y ausencia de NaN indebidos."""
    problems: list[str] = []

    for column in INTEGER_COLUMNS:
        if (frame[column] < 0).any():
            problems.append(f"{column!r} tiene valores negativos")

    non_nullable = list(MODEL_READY_FEATURES) + list(ABLATION_FEATURES) + list(AUXILIARY_COLUMNS)
    for column in non_nullable + list(METADATA_COLUMNS):
        if frame[column].isna().any():
            problems.append(f"{column!r} contiene NaN y el contrato no lo permite")

    if (frame["positions_count"] < 1).any():
        problems.append("positions_count debe ser >= 1, como el CHECK del esquema real")
    if (frame["elapsed_days_since_publication"] <= 0).any():
        problems.append("elapsed_days_since_publication debe ser > 0 en el checkpoint")
    if (frame["days_remaining_to_target"] <= 0).any():
        problems.append("days_remaining_to_target debe ser > 0: el plazo es posterior al checkpoint")
    if frame["configured_stage_count"].max() > 2:
        problems.append("configured_stage_count supera el maximo real de 2 etapas")

    return problems


def check_count_invariants(frame: pd.DataFrame) -> list[str]:
    """Validaciones 10, 11 y 12 de la especificacion: coherencia de conteos."""
    problems: list[str] = []
    for kind in ("evaluations", "interviews"):
        scheduled = frame[f"{kind}_scheduled_count"]
        completed = frame[f"{kind}_completed_count"]
        pending = frame[f"{kind}_pending_count"]
        overdue = frame[f"{kind}_overdue_pending_count"]

        if (completed > scheduled).any():
            problems.append(f"{kind}: completadas > programadas")
        if not (pending == scheduled - completed).all():
            problems.append(f"{kind}: pending != scheduled - completed")
        if (overdue > pending).any():
            problems.append(f"{kind}: vencidas pendientes > pendientes")
    return problems


def check_censoring(frame: pd.DataFrame) -> list[str]:
    """Validacion 13 y decision 10: los censurados no reciben etiqueta."""
    problems: list[str] = []

    statuses = set(frame["observation_status"].unique())
    unexpected = statuses - {STATUS_COMPLETED, STATUS_CENSORED}
    if unexpected:
        problems.append(f"estados de observacion inesperados: {sorted(unexpected)!r}")

    censored = frame[frame["observation_status"] == STATUS_CENSORED]
    if not censored.empty and censored[TARGET_COLUMN].notna().any():
        problems.append("hay procesos censurados con etiqueta asignada: prohibido por la decision 10")

    completed = frame[frame["observation_status"] == STATUS_COMPLETED]
    if completed[TARGET_COLUMN].isna().any():
        problems.append("hay procesos completados sin etiqueta")

    return problems


def check_prevalence(frame: pd.DataFrame, minimum: float, maximum: float) -> list[str]:
    """Validacion 16: prevalencia dentro de la banda de simulacion."""
    completed = frame[frame["observation_status"] == STATUS_COMPLETED]
    if completed.empty:
        return ["no hay filas etiquetadas para medir prevalencia"]
    prevalence = float(completed[TARGET_COLUMN].mean())
    if not minimum <= prevalence <= maximum:
        return [
            f"prevalencia {prevalence:.4f} fuera de la banda objetivo [{minimum}, {maximum}]"
        ]
    return []


def check_leakage_signals(frame: pd.DataFrame) -> list[str]:
    """Validacion 14: correlacion sospechosa entre feature y target.

    Una correlacion casi perfecta no prueba fuga por si sola, pero obliga a
    revisar antes de seguir. Con un generador honesto no deberia aparecer.
    """
    problems: list[str] = []
    completed = frame[frame["observation_status"] == STATUS_COMPLETED]
    if completed.empty:
        return problems
    target = completed[TARGET_COLUMN].astype(float)
    for column in MODEL_READY_FEATURES:
        values = completed[column].astype(float)
        if values.std(ddof=0) == 0:
            continue
        correlation = float(np.corrcoef(values, target)[0, 1])
        if abs(correlation) >= SUSPICIOUS_CORRELATION:
            problems.append(
                f"correlacion sospechosa entre {column!r} y el target: r={correlation:.4f}"
            )
    return problems


def check_extreme_cases(frame: pd.DataFrame) -> list[str]:
    """Validacion 15: los casos extremos obligatorios estan representados."""
    warnings: list[str] = []
    checks = {
        "cero postulaciones": (frame["applications_received_count"] == 0).any(),
        "volumen alto de postulaciones": (
            frame["applications_received_count"] >= frame["applications_received_count"].quantile(0.99)
        ).any(),
        "ninguna sesion programada": (
            (frame["evaluations_scheduled_count"] == 0) & (frame["interviews_scheduled_count"] == 0)
        ).any(),
        "sesiones vencidas sin completar": (frame["evaluations_overdue_pending_count"] > 0).any(),
        "ventana de postulaciones minima": (frame["application_window_days"] <= 3).any(),
        "periodo largo sin actividad": (frame["days_since_last_operational_event"] >= 10).any(),
        "carga concurrente alta": (frame["concurrent_open_vacancies_count"] > 0).any(),
    }
    for label, present in checks.items():
        if not present:
            warnings.append(f"caso extremo ausente del dataset: {label}")
    return warnings


def validate_frame(frame: pd.DataFrame, minimum: float, maximum: float) -> ValidationReport:
    """Ejecuta todas las validaciones estructurales sobre un frame."""
    report = ValidationReport()
    report.extend(check_columns(frame))
    report.extend(check_uniqueness(frame))
    report.extend(check_ranges(frame))
    report.extend(check_count_invariants(frame))
    report.extend(check_censoring(frame))
    report.extend(check_prevalence(frame, minimum, maximum))
    report.extend(check_leakage_signals(frame))
    report.warnings.extend(check_extreme_cases(frame))
    return report


def validate_dataset(dataset: "object") -> ValidationReport:
    """Valida un `SyntheticDataset` completo, incluido su manifiesto."""
    frame = getattr(dataset, "frame")
    config = getattr(dataset, "config")
    manifest = getattr(dataset, "manifest")

    report = validate_frame(frame, config.prevalence_min, config.prevalence_max)

    for key in ("dataset_fingerprint", "config_fingerprint", "seed", "dataset_version"):
        if not manifest.get(key):
            report.issues.append(f"manifiesto incompleto: falta {key!r}")

    if manifest.get("data_nature") != "synthetic":
        report.issues.append("el manifiesto debe declarar que los datos son sinteticos")

    return report
