"""Registro de congelacion del experimento.

El freeze es el **protocolo previo al test**: fija features, preprocesamiento,
modelo, hiperparametros, umbral exacto, calibracion, ablations, metricas de
validation, criterios de veredicto y limitaciones conocidas. Se persiste en
disco **antes** de revelar el conjunto de prueba, y es el artefacto que
autoriza esa revelacion.

Dos reglas que lo sostienen:

1. **El freeze no contiene resultados de test.** Los resultados posteriores
   viven en un artefacto separado que referencia su huella.
2. **La huella se calcula sobre el protocolo**, excluyendo `frozen_at` y la
   propia huella. Asi es reproducible entre ejecuciones y a la vez detecta
   cualquier alteracion del contenido.

Vive en su propio modulo para que `split.py` pueda validarlo sin crear un ciclo
de importacion con `experiment.py`.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Any

#: Version del contrato del freeze. Cambiarla invalida las comparaciones.
FREEZE_SCHEMA_VERSION = "15b.1"

#: Campos que no entran en la huella: son metadatos operativos, no protocolo.
_FINGERPRINT_EXCLUDED = frozenset({"frozen_at", "freeze_fingerprint", "source_path"})


class FreezeValidationError(RuntimeError):
    """El registro de congelacion no es valido para la operacion solicitada."""


@dataclass(frozen=True)
class ExperimentFreeze:
    """Protocolo congelado del experimento, anterior a cualquier mirada al test."""

    schema_version: str
    experiment_id: str
    seed: int
    dataset_fingerprint: str
    config_fingerprint: str
    split_signature: str
    split_definition: dict[str, Any]
    feature_set: str
    features: list[str]
    excluded_features: list[str]
    ablation_feature_sets: list[str]
    preprocessing: str
    model_family: str
    model_params: dict[str, Any]
    threshold: float
    threshold_rule: str
    threshold_selection: dict[str, Any]
    calibration_decision: dict[str, Any]
    validation_metrics: dict[str, Any]
    validation_baselines: dict[str, Any]
    ablation_conclusions: dict[str, Any]
    verdict_rule: dict[str, Any]
    known_limitations: list[str]
    frozen_at: str
    freeze_fingerprint: str = ""
    source_path: str | None = None
    is_frozen: bool = True

    # -- huella -----------------------------------------------------------

    def protocol_payload(self) -> dict[str, Any]:
        """Contenido sobre el que se calcula la huella.

        `threshold` se serializa con `repr` para conservar el float exacto: un
        umbral redondeado cambiaria clasificaciones en la frontera.
        """
        payload = {
            key: value
            for key, value in self.__dict__.items()
            if key not in _FINGERPRINT_EXCLUDED
        }
        payload["threshold"] = repr(float(self.threshold))
        return payload

    def compute_fingerprint(self) -> str:
        canonical = json.dumps(
            self.protocol_payload(), sort_keys=True, separators=(",", ":"), default=str
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def with_fingerprint(self) -> ExperimentFreeze:
        return replace(self, freeze_fingerprint=self.compute_fingerprint())

    def is_intact(self) -> bool:
        """True si el contenido coincide con la huella que declara."""
        return bool(self.freeze_fingerprint) and self.freeze_fingerprint == self.compute_fingerprint()

    # -- serializacion ----------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        payload = dict(self.__dict__)
        payload.pop("source_path", None)
        # `threshold` se escribe con toda su precision; el campo de lectura
        # humana es informativo y nunca debe usarse para inferir.
        payload["threshold"] = float(self.threshold)
        payload["threshold_display"] = round(float(self.threshold), 6)
        payload["contains_test_results"] = False
        payload["note"] = (
            "Protocolo congelado antes de revelar el conjunto de prueba. No contiene "
            "resultados de test: estos viven en el artefacto de resultados, que referencia "
            "esta huella."
        )
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any], source_path: str | None = None) -> ExperimentFreeze:
        data = dict(payload)
        for derived in ("threshold_display", "contains_test_results", "note"):
            data.pop(derived, None)
        data["threshold"] = float(data["threshold"])
        data["source_path"] = source_path
        return cls(**data)


def build_freeze(**fields: Any) -> ExperimentFreeze:
    """Construye el freeze y le calcula su huella."""
    fields.setdefault("schema_version", FREEZE_SCHEMA_VERSION)
    fields.setdefault("frozen_at", datetime.now().astimezone().isoformat())
    return ExperimentFreeze(**fields).with_fingerprint()


def persist_freeze(freeze: ExperimentFreeze, path: Path) -> Path:
    """Escribe el freeze en disco. Debe ocurrir **antes** de revelar el test."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(freeze.to_dict(), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    return path


def load_freeze(path: Path) -> ExperimentFreeze:
    """Lee el freeze desde disco y comprueba su integridad.

    Se devuelve con `source_path`, que es la prueba de que el registro llego
    desde un artefacto persistido y no se construyo al vuelo.
    """
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    freeze = ExperimentFreeze.from_dict(payload, source_path=str(path))
    if not freeze.is_intact():
        raise FreezeValidationError(
            f"el freeze de {path} fue alterado: su contenido no coincide con freeze_fingerprint"
        )
    return freeze


#: Secciones cientificas que deben existir **y tener contenido**.
#:
#: Comprobar que la clave existe no basta: un freeze con `validation_metrics`
#: vacio no documenta nada y no puede autorizar la apertura del test.
REQUIRED_SCIENTIFIC_SECTIONS = (
    "threshold_selection",
    "calibration_decision",
    "validation_metrics",
    "validation_baselines",
    "ablation_conclusions",
    "verdict_rule",
    "known_limitations",
)

#: Campos escalares que no pueden quedar vacios.
REQUIRED_SCALAR_FIELDS = (
    "feature_set",
    "model_family",
    "threshold_rule",
    "preprocessing",
    "experiment_id",
    "dataset_fingerprint",
    "config_fingerprint",
    "split_signature",
)


def _validate_source_file(freeze: ExperimentFreeze) -> None:
    """Comprueba que el freeze proviene de un archivo real y coincidente.

    Declarar una ruta no es prueba de nada: se exige que exista, que sea un
    archivo regular, que pueda cargarse y que el registro recargado tenga la
    misma huella. Un objeto construido en memoria con una ruta inventada no
    abre el conjunto de prueba.
    """
    if freeze.source_path is None:
        raise FreezeValidationError(
            "el freeze debe haberse persistido y recargado desde disco antes de revelar el test"
        )

    path = Path(freeze.source_path)
    if not path.exists():
        raise FreezeValidationError(
            f"source_path no existe: {freeze.source_path!r}; el freeze no fue persistido"
        )
    if not path.is_file():
        raise FreezeValidationError(
            f"source_path no es un archivo regular: {freeze.source_path!r}"
        )

    reloaded = load_freeze(path)
    if reloaded.freeze_fingerprint != freeze.freeze_fingerprint:
        raise FreezeValidationError(
            "el archivo de source_path contiene un freeze distinto: "
            f"{reloaded.freeze_fingerprint!r} != {freeze.freeze_fingerprint!r}"
        )


def _validate_scientific_content(freeze: ExperimentFreeze) -> None:
    """Valida que el protocolo documenta de verdad lo que dice documentar."""
    for name in REQUIRED_SCALAR_FIELDS:
        if not getattr(freeze, name):
            raise FreezeValidationError(f"el freeze esta incompleto: {name} vacio o ausente")

    if not freeze.features:
        raise FreezeValidationError("el freeze esta incompleto: no declara features")
    if not freeze.model_params and freeze.model_params != {}:  # pragma: no cover - defensivo
        raise FreezeValidationError("el freeze esta incompleto: model_params ausente")
    if freeze.model_params is None:
        raise FreezeValidationError("el freeze esta incompleto: model_params ausente")
    if not isinstance(freeze.threshold, float) or not 0.0 < freeze.threshold < 1.0:
        raise FreezeValidationError(
            f"umbral fuera del rango valido (0, 1): {freeze.threshold!r}"
        )

    for section in REQUIRED_SCIENTIFIC_SECTIONS:
        value = getattr(freeze, section)
        if value is None or len(value) == 0:
            raise FreezeValidationError(
                f"seccion cientifica vacia o ausente: {section}. Un protocolo sin ella "
                "no documenta el experimento y no puede autorizar la apertura del test"
            )

    if "average_precision" not in freeze.validation_metrics:
        raise FreezeValidationError(
            "validation_metrics no contiene la metrica primaria (average_precision)"
        )
    if "threshold" not in freeze.threshold_selection:
        raise FreezeValidationError("threshold_selection no documenta el umbral elegido")


def validate_freeze_for_split(
    freeze: Any,
    dataset_fingerprint: str,
    split_signature: str,
    config_fingerprint: str | None = None,
) -> ExperimentFreeze:
    """Valida un freeze antes de permitir el acceso al conjunto de prueba.

    No basta con un objeto que declare `is_frozen=True`. Se exige el tipo del
    dominio, la version del contrato, integridad de la huella, **procedencia de
    un archivo real y coincidente**, correspondencia con el dataset, la
    configuracion y la particion concretos, y **contenido cientifico efectivo**
    en cada seccion obligatoria.
    """
    if not isinstance(freeze, ExperimentFreeze):
        raise FreezeValidationError(
            "se requiere un ExperimentFreeze; un objeto cualquiera con is_frozen no basta"
        )
    if not freeze.is_frozen:
        raise FreezeValidationError("el registro no esta congelado")
    if freeze.schema_version != FREEZE_SCHEMA_VERSION:
        raise FreezeValidationError(
            f"version de contrato incompatible: {freeze.schema_version!r} != {FREEZE_SCHEMA_VERSION!r}"
        )
    if not freeze.is_intact():
        raise FreezeValidationError("la huella del freeze no coincide con su contenido")

    _validate_source_file(freeze)

    if freeze.dataset_fingerprint != dataset_fingerprint:
        raise FreezeValidationError(
            "el freeze corresponde a otro dataset: "
            f"{freeze.dataset_fingerprint!r} != {dataset_fingerprint!r}"
        )
    if config_fingerprint is not None and freeze.config_fingerprint != config_fingerprint:
        raise FreezeValidationError(
            "el freeze corresponde a otra configuracion del generador: "
            f"{freeze.config_fingerprint!r} != {config_fingerprint!r}"
        )
    if freeze.split_signature != split_signature:
        raise FreezeValidationError(
            "el freeze corresponde a otra particion temporal: "
            f"{freeze.split_signature!r} != {split_signature!r}"
        )

    _validate_scientific_content(freeze)
    return freeze


@dataclass(frozen=True)
class TestResults:
    """Resultados posteriores al test, separados del protocolo.

    Referencia la huella del freeze: la direccion de la dependencia es
    `resultados -> protocolo`, nunca al reves.
    """

    schema_version: str
    experiment_id: str
    freeze_fingerprint: str
    dataset_fingerprint: str
    threshold: float
    metrics: dict[str, Any]
    baselines: dict[str, Any]
    organizations: dict[str, Any]
    temporal_stability: dict[str, Any]
    verdict: dict[str, Any]
    limitations: list[str]
    evaluated_at: str
    curves: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = dict(self.__dict__)
        payload["threshold"] = float(self.threshold)
        payload["threshold_display"] = round(float(self.threshold), 6)
        payload["references_freeze"] = True
        payload["note"] = (
            "Resultados obtenidos tras revelar el conjunto de prueba con el protocolo "
            "congelado identificado por freeze_fingerprint."
        )
        return payload


def persist_test_results(results: TestResults, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(results.to_dict(), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    return path
