"""Metadatos del artefacto servido y del servicio.

El artefacto binario por si solo no dice de que experimento salio. Estos
metadatos son el puente entre el `.joblib` local -- que no se versiona -- y el
freeze versionado de la Fase 15B: sin ellos, cargar un modelo seria un acto de
fe.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

#: Version del contrato de metadatos del artefacto. Cambiarla invalida los
#: artefactos anteriores a proposito: el loader los rechaza.
ARTIFACT_SCHEMA_VERSION = "15c.2"

#: Huella del **unico** protocolo aprobado en la Fase 15B.
#:
#: El freeze ya se valida por integridad, pero eso solo demuestra que un
#: registro es coherente consigo mismo: alguien puede cambiar `C=10` por `C=1`,
#: recalcular la huella y obtener un freeze perfectamente integro que describe
#: otro experimento. Fijar aqui la huella aprobada convierte "integro" en "es
#: este". Cambiar este valor exige una fase que apruebe otro experimento.
APPROVED_FREEZE_FINGERPRINT = (
    "9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2"
)

#: Bibliotecas cuya version condiciona el comportamiento de la inferencia.
#: Un pipeline serializado por otra version de scikit-learn puede deserializar
#: sin error y predecir distinto.
CRITICAL_LIBRARIES = ("scikit-learn", "numpy", "joblib")

#: Veredicto cientifico de la Fase 15B. No se reinterpreta aqui.
VERDICT = "PREDICTIVE GO WITH LIMITATIONS"

#: Estado de despliegue. `GAP-01` sigue abierto, asi que el servicio es
#: experimental y ninguna respuesta debe sugerir lo contrario.
DEPLOYMENT_STATUS = "experimental"

GAP_01_NOTE = (
    "GAP-01 abierto: target_completion_at no existe en Laravel, asi que "
    "days_remaining_to_target no es computable en produccion. El servicio es "
    "experimental y no esta autorizado para integracion."
)

RISK_SCORE_MEANING = (
    "Probabilidad estimada de retraso operacional del proceso de la vacante. "
    "No evalua, puntua ni clasifica personas."
)

RISK_FLAG_MEANING = (
    "risk_score >= threshold. Es una senal operativa para revision humana: no "
    "es una decision, ni una recomendacion de contratacion, ni un descarte, ni "
    "un ranking, ni dispara ninguna accion automatica."
)


@dataclass(frozen=True)
class ArtifactMetadata:
    """Lo que el artefacto declara de si mismo.

    Se persiste junto al `.joblib` y el loader lo contrasta contra el freeze.
    """

    schema_version: str
    experiment_id: str
    freeze_fingerprint: str
    dataset_fingerprint: str
    config_fingerprint: str
    model_family: str
    model_params: dict[str, Any]
    preprocessing: str
    feature_set: str
    feature_order: list[str]
    threshold: float
    seed: int
    rows: int
    n_train: int
    built_at: str
    #: SHA-256 del `.joblib`, calculado tras escribirlo. Permite detectar que
    #: el binario cambio sin que cambiaran sus metadatos.
    artifact_sha256: str = ""
    library_versions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        # El umbral se escribe con toda su precision; el campo de lectura
        # humana existe solo para informes y nunca debe usarse para inferir.
        payload["threshold"] = float(self.threshold)
        payload["threshold_display"] = round(float(self.threshold), 6)
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ArtifactMetadata:
        data = {key: value for key, value in payload.items() if key != "threshold_display"}
        known = {field_name for field_name in cls.__dataclass_fields__}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"metadatos con campos desconocidos: {sorted(unknown)}")
        missing = known - set(data)
        if missing:
            raise ValueError(f"metadatos incompletos: faltan {sorted(missing)}")
        data["threshold"] = float(data["threshold"])
        data["feature_order"] = list(data["feature_order"])
        return cls(**data)

    def write(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        return path

    @classmethod
    def read(cls, path: Path) -> ArtifactMetadata:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


@dataclass(frozen=True)
class ServiceMetadata:
    """Lo que el servicio expone sobre el modelo que sirve.

    Deliberadamente **no** incluye rutas locales, filas de entrenamiento ni
    nada que pudiera identificar a una persona: es informacion tecnica del
    experimento, no de sus datos.
    """

    model_family: str
    experiment_id: str
    freeze_fingerprint: str
    threshold: float
    feature_order: list[str]
    verdict: str
    deployment_status: str
    gap_01_open: bool
    gap_01_note: str
    risk_score_meaning: str
    risk_flag_meaning: str
    artifact_schema_version: str
    library_versions: dict[str, str]

    @classmethod
    def from_artifact(cls, metadata: ArtifactMetadata) -> ServiceMetadata:
        return cls(
            model_family=metadata.model_family,
            experiment_id=metadata.experiment_id,
            freeze_fingerprint=metadata.freeze_fingerprint,
            threshold=float(metadata.threshold),
            feature_order=list(metadata.feature_order),
            verdict=VERDICT,
            deployment_status=DEPLOYMENT_STATUS,
            gap_01_open=True,
            gap_01_note=GAP_01_NOTE,
            risk_score_meaning=RISK_SCORE_MEANING,
            risk_flag_meaning=RISK_FLAG_MEANING,
            artifact_schema_version=metadata.schema_version,
            library_versions=dict(metadata.library_versions),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def file_digest(path: Path) -> str:
    """SHA-256 de un archivo, leido por bloques.

    El artefacto ronda las decenas de kilobytes, pero leerlo por bloques
    mantiene la funcion utilizable si algun dia crece.
    """
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def library_versions() -> dict[str, str]:
    """Versiones que condicionan la reproducibilidad de la inferencia.

    Un artefacto serializado por una version de scikit-learn y cargado por otra
    puede comportarse de forma distinta; dejarlo escrito permite detectarlo.
    """
    import joblib
    import numpy
    import pandas
    import sklearn

    return {
        "python": ".".join(str(part) for part in sys.version_info[:3]),
        "scikit-learn": sklearn.__version__,
        "numpy": numpy.__version__,
        "pandas": pandas.__version__,
        "joblib": joblib.__version__,
    }
