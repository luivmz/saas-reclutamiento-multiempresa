"""Configuracion centralizada del generador sintetico.

Todo parametro que gobierna la simulacion vive aqui. El resto del paquete no
define constantes magicas: las lee de `SyntheticConfig`.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

#: Zona horaria unica del proyecto. Toda fecha se interpreta aqui.
LIMA_TZ = "America/Lima"

#: Seed maestra aprobada en la Fase 14 (decision 4).
DEFAULT_SEED = 20260920

#: Version conceptual del dataset aprobada en la Fase 14.
DATASET_VERSION = "synthetic-v1"

#: Version del contrato de features que este generador implementa.
FEATURE_CONTRACT_VERSION = "phase-14"

#: Rango academico aprobado de observaciones (decision 4).
APPROVED_ROWS_MIN = 5_000
APPROVED_ROWS_MAX = 10_000

#: Periodo sintetico minimo aprobado, en meses.
APPROVED_MONTHS_MIN = 36


class SyntheticConfig(BaseModel):
    """Parametros reproducibles de una generacion.

    El modelo es inmutable: una configuracion no cambia despues de construirse,
    de modo que el hash que la identifica no puede quedar obsoleto.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    seed: int = Field(default=DEFAULT_SEED, ge=0)
    """Seed maestra. Misma seed + misma configuracion => mismo dataset."""

    rows: int = Field(default=6_000, ge=50, le=50_000)
    """Numero de procesos sinteticos a generar.

    El rango aprobado para la entrega academica es 5 000-10 000
    (`validate_academic_profile`). Se admiten valores menores para que las
    pruebas automatizadas corran rapido; la CLI advierte cuando se sale del
    rango aprobado.
    """

    organizations: int = Field(default=6, ge=1, le=20)
    """Organizaciones ficticias. Rango aprobado: 4-8."""

    months: int = Field(default=42, ge=6, le=180)
    """Meses de periodo sintetico. Minimo aprobado: 36."""

    start_date: date = Field(default=date(2023, 1, 1))
    """Primer mes del periodo simulado, en America/Lima."""

    prevalence_min: float = Field(default=0.25, ge=0.0, le=1.0)
    prevalence_max: float = Field(default=0.40, ge=0.0, le=1.0)
    """Banda objetivo de prevalencia de `delayed=1` en el dataset model-ready.

    Es una decision de simulacion, no una estadistica institucional.
    """

    stall_rate: float = Field(default=0.06, ge=0.0, le=0.5)
    """Probabilidad de que un proceso quede estancado y nunca cierre.

    Modela el hecho verificado de que una vacante solo se cierra tras la
    decision y la seleccion humanas: un proceso atascado nunca produce
    `closed_at` y por tanto queda censurado.
    """

    drift_strength: float = Field(default=0.30, ge=0.0, le=1.0)
    """Intensidad del drift temporal (volumen y friccion crecen con el tiempo)."""

    delay_pressure: float = Field(default=1.0, gt=0.0, le=5.0)
    """Multiplicador estructural del tiempo restante tras el checkpoint.

    Es la palanca para situar la prevalencia en la banda objetivo sin filtrar
    etiquetas ni remuestrear.
    """

    observation_tail_months: int = Field(default=9, ge=0, le=36)
    """Meses de seguimiento tras el ultimo mes de solicitudes.

    Los procesos que no cierran dentro de esa ventana quedan censurados.
    """

    null_opens_at_rate: float = Field(default=0.12, ge=0.0, le=1.0)
    """Proporcion de vacantes sin `opens_at`, que ejercita la regla de respaldo
    de `application_window_days`."""

    dataset_version: str = Field(default=DATASET_VERSION)
    feature_contract_version: str = Field(default=FEATURE_CONTRACT_VERSION)

    output_path: Path | None = Field(default=None)
    """Destino opcional del CSV. Nunca se versiona."""

    @model_validator(mode="after")
    def _check_prevalence_band(self) -> SyntheticConfig:
        if self.prevalence_min >= self.prevalence_max:
            raise ValueError("prevalence_min debe ser estrictamente menor que prevalence_max")
        return self

    def fingerprint(self) -> str:
        """Hash estable de la configuracion, sin la ruta de salida.

        La ruta no altera el contenido del dataset, asi que no entra al hash.
        """
        payload = self.model_dump(mode="json", exclude={"output_path"})
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def is_within_approved_profile(self) -> bool:
        """True si la configuracion respeta el perfil academico aprobado."""
        return (
            APPROVED_ROWS_MIN <= self.rows <= APPROVED_ROWS_MAX
            and 4 <= self.organizations <= 8
            and self.months >= APPROVED_MONTHS_MIN
            and self.seed == DEFAULT_SEED
            and self.dataset_version == DATASET_VERSION
        )


def validate_academic_profile(config: SyntheticConfig) -> list[str]:
    """Devuelve las desviaciones respecto del perfil aprobado en la Fase 14.

    Una lista vacia significa que la configuracion es la entregable.
    """
    problems: list[str] = []
    if not APPROVED_ROWS_MIN <= config.rows <= APPROVED_ROWS_MAX:
        problems.append(
            f"rows={config.rows} fuera del rango academico aprobado "
            f"[{APPROVED_ROWS_MIN}, {APPROVED_ROWS_MAX}]"
        )
    if not 4 <= config.organizations <= 8:
        problems.append(f"organizations={config.organizations} fuera del rango aprobado [4, 8]")
    if config.months < APPROVED_MONTHS_MIN:
        problems.append(f"months={config.months} por debajo del minimo aprobado {APPROVED_MONTHS_MIN}")
    if config.seed != DEFAULT_SEED:
        problems.append(f"seed={config.seed} distinta de la seed maestra aprobada {DEFAULT_SEED}")
    if config.dataset_version != DATASET_VERSION:
        problems.append(f"dataset_version={config.dataset_version!r} distinta de {DATASET_VERSION!r}")
    return problems
