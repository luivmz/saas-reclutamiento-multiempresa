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
import math
import re
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Any

from recruitment_ml.schema import ABLATION_REQUIRED_IN_15B

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


#: Secciones cientificas que deben existir **y documentar algo verificable**.
#:
#: Comprobar que la clave existe no basta, y comprobar que no esta vacia tampoco:
#: `{"placeholder": true}` no es vacio y no documenta nada. Cada seccion tiene
#: ademas un validador propio mas abajo.
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

#: Metricas de validation que el protocolo debe dejar congeladas. Son las que
#: el veredicto compara despues contra test; si falta una, la comparacion no
#: puede hacerse sin recalcular, y recalcular ya no seria preregistro.
REQUIRED_VALIDATION_METRICS = (
    "average_precision",
    "roc_auc",
    "precision",
    "recall",
    "f1",
    "f2",
    "balanced_accuracy",
    "brier",
    "alert_rate",
)

#: Baselines contra los que se juzga el modelo, y metricas minimas de cada uno.
REQUIRED_BASELINES = ("dummy_prior", "operational")
REQUIRED_BASELINE_METRICS = ("average_precision", "precision", "recall", "brier")

#: Reglas que el veredicto debe declarar antes de ver el test.
REQUIRED_VERDICT_RULE_KEYS = (
    "must_beat_dummy_ap",
    "must_beat_operational_ap",
    "must_have_positive_bss",
    "limitations_downgrade_the_verdict",
    "not_deployable_while_gap_01_open",
)

#: Limitaciones que el experimento conoce antes del test. Se comprueba la
#: **cobertura tematica**, no el texto exacto: la redaccion puede evolucionar,
#: pero ninguno de estos hechos puede desaparecer del protocolo.
REQUIRED_LIMITATION_TOPICS = (
    ("datos sinteticos", ("sintetic",)),
    ("tasa de alerta", ("tasa de alerta", "alert rate", "alert_rate")),
    ("heterogeneidad entre organizaciones", ("heterogeneidad",)),
    ("concurrency como posible proxy temporal", ("proxy temporal", "concurrent_open_vacancies_count")),
    ("censura informativa", ("censura",)),
    ("colinealidad", ("colinealidad",)),
    ("contaminacion procedimental", ("contaminacion",)),
    ("GAP-01 / no desplegable", ("gap-01",)),
)

#: Unico formato de huella que usa el proyecto: sha256 en hexadecimal.
_FINGERPRINT_PATTERN = re.compile(r"[0-9a-f]{64}")

#: Una lectura de ablation debe traer un numero: "sin cambios relevantes" no
#: seria una conclusion verificable.
_DECIMAL_PATTERN = re.compile(r"[+-]?\d+\.\d+")

#: Deteccion de "test" como palabra, no como subcadena de "latest" o similares.
_TEST_WORD_PATTERN = re.compile(r"\btest\w*\b")


# -- utilidades de validacion ---------------------------------------------


def _fold(text: str) -> str:
    """Minusculas sin acentos, para comparar temas y no ortografias."""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char)).lower()


def require_fingerprint(value: Any, name: str) -> str:
    """Exige una huella sha256 real.

    Es la funcion que cierra la puerta a construir una particion sin enlace
    efectivo al dataset y a la configuracion que la produjeron: no hay valor
    por defecto ni cadena vacia que pase por aqui.
    """
    if not isinstance(value, str):
        raise FreezeValidationError(
            f"{name} es obligatorio y debe ser una cadena, no {type(value).__name__}"
        )
    candidate = value.strip()
    if not candidate:
        raise FreezeValidationError(f"{name} es obligatorio y no puede quedar vacio")
    if not _FINGERPRINT_PATTERN.fullmatch(candidate):
        raise FreezeValidationError(
            f"{name} no tiene formato de huella sha256 (64 caracteres hexadecimales): {value!r}"
        )
    return candidate


def _require_mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FreezeValidationError(
            f"{where} debe ser un objeto con contenido, no {type(value).__name__}"
        )
    return value


def _require_number(container: Mapping[str, Any], key: str, where: str) -> float:
    if key not in container:
        raise FreezeValidationError(f"{where} no documenta {key}")
    value = container[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FreezeValidationError(f"{where}.{key} no es un valor numerico: {value!r}")
    number = float(value)
    if math.isnan(number) or math.isinf(number):
        raise FreezeValidationError(f"{where}.{key} no es un numero finito: {value!r}")
    return number


def _require_text(container: Mapping[str, Any], key: str, where: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise FreezeValidationError(f"{where}.{key} debe ser texto no vacio")
    return value.strip()


# -- validadores por seccion ----------------------------------------------
#
# Uno por seccion, con nombre propio: el mensaje de error dice que falta y el
# lector puede auditar cada contrato por separado.


def validate_threshold_selection(freeze: ExperimentFreeze) -> None:
    """El umbral documentado debe ser el congelado, y elegido con validation."""
    section = _require_mapping(freeze.threshold_selection, "threshold_selection")
    threshold = _require_number(section, "threshold", "threshold_selection")
    if threshold != float(freeze.threshold):
        raise FreezeValidationError(
            "threshold_selection.threshold no coincide con el umbral congelado: "
            f"{threshold!r} != {float(freeze.threshold)!r}"
        )
    _require_text(section, "rule", "threshold_selection")

    declared = _require_text(section, "selected_on", "threshold_selection")
    source = _fold(declared)
    if _TEST_WORD_PATTERN.search(source):
        raise FreezeValidationError(
            "threshold_selection declara el test como fuente de seleccion: "
            f"selected_on={declared!r}. El umbral se elige con validation"
        )
    if "validation" not in source:
        raise FreezeValidationError(
            f"threshold_selection.selected_on debe declarar validation como fuente: {declared!r}"
        )


def validate_calibration_decision(freeze: ExperimentFreeze) -> None:
    """La decision de calibrar debe ser explicita, negativa y sostenida por numeros.

    El protocolo de 15B es el del **modelo sin calibrar**: la calibracion se
    evaluo y se rechazo porque empeoraba el ECE. Un freeze que declare
    `adopt_calibration=True` describe otro modelo distinto del que produjo estas
    metricas, asi que no puede abrir este conjunto de prueba, por mucho que el
    metodo declarado sea uno conocido.
    """
    section = _require_mapping(freeze.calibration_decision, "calibration_decision")

    adopted = section.get("adopt_calibration")
    if not isinstance(adopted, bool):
        raise FreezeValidationError(
            "calibration_decision.adopt_calibration debe ser booleano; "
            f"recibido {section.get('adopt_calibration')!r}"
        )
    if adopted:
        raise FreezeValidationError(
            "calibration_decision declara adopt_calibration=True, pero el protocolo de 15B "
            "corresponde al modelo sin calibrar: el freeze describiria un modelo distinto "
            "del que produjo las metricas congeladas"
        )
    _require_text(section, "method", "calibration_decision")
    _require_text(section, "decision_rule", "calibration_decision")
    for key in ("brier_uncalibrated", "brier_calibrated", "ece_uncalibrated", "ece_calibrated"):
        _require_number(section, key, "calibration_decision")

    fitted_on = _require_text(section, "fitted_on", "calibration_decision")
    if "train" not in _fold(fitted_on):
        raise FreezeValidationError(
            "calibration_decision.fitted_on debe declarar que la calibracion se ajusto con "
            f"train: {fitted_on!r}"
        )

    if "calibrad" in _fold(freeze.preprocessing):
        raise FreezeValidationError(
            "calibration_decision no adopta calibracion pero el preprocesamiento declara una: "
            f"{freeze.preprocessing!r}"
        )


def validate_validation_metrics(freeze: ExperimentFreeze) -> None:
    """Las metricas de validation son el punto de comparacion; deben estar todas."""
    section = _require_mapping(freeze.validation_metrics, "validation_metrics")
    if "average_precision" not in section:
        raise FreezeValidationError(
            "validation_metrics no contiene la metrica primaria (average_precision)"
        )
    for key in REQUIRED_VALIDATION_METRICS:
        _require_number(section, key, "validation_metrics")

    threshold = _require_number(section, "threshold", "validation_metrics")
    if threshold != float(freeze.threshold):
        raise FreezeValidationError(
            "validation_metrics se calcularon con otro umbral: "
            f"{threshold!r} != {float(freeze.threshold)!r}"
        )

    matrix = _require_mapping(
        section.get("confusion_matrix"), "validation_metrics.confusion_matrix"
    )
    for cell in ("tp", "fp", "tn", "fn"):
        value = matrix.get(cell)
        if isinstance(value, bool) or not isinstance(value, int):
            raise FreezeValidationError(
                f"validation_metrics.confusion_matrix.{cell} no es un conteo entero: {value!r}"
            )


def validate_validation_baselines(freeze: ExperimentFreeze) -> None:
    """Sin baselines no hay con que comparar, y el veredicto es comparativo."""
    section = _require_mapping(freeze.validation_baselines, "validation_baselines")
    for name in REQUIRED_BASELINES:
        entry = section.get(name)
        if not isinstance(entry, Mapping) or not entry:
            raise FreezeValidationError(f"validation_baselines no documenta el baseline {name}")
        for key in REQUIRED_BASELINE_METRICS:
            _require_number(entry, key, f"validation_baselines.{name}")


def validate_ablation_conclusions(freeze: ExperimentFreeze) -> None:
    """Las tres features senaladas por la auditoria de 15A deben tener lectura."""
    section = _require_mapping(freeze.ablation_conclusions, "ablation_conclusions")
    for feature in ABLATION_REQUIRED_IN_15B:
        reading = section.get(feature)
        if not isinstance(reading, str) or not reading.strip():
            raise FreezeValidationError(f"ablation_conclusions no documenta {feature}")
        if not _DECIMAL_PATTERN.search(reading):
            raise FreezeValidationError(
                f"ablation_conclusions.{feature} no reporta ninguna diferencia medible"
            )


def validate_verdict_rule(freeze: ExperimentFreeze) -> None:
    """La regla del veredicto se declara antes, o el veredicto no significa nada."""
    section = _require_mapping(freeze.verdict_rule, "verdict_rule")
    for key in REQUIRED_VERDICT_RULE_KEYS:
        _require_text(section, key, "verdict_rule")


def validate_known_limitations(freeze: ExperimentFreeze) -> None:
    """Lista real de limitaciones, con cobertura de los temas conocidos."""
    limitations = freeze.known_limitations
    if isinstance(limitations, str) or not isinstance(limitations, Sequence):
        raise FreezeValidationError(
            f"known_limitations debe ser una lista, no {type(limitations).__name__}"
        )
    for index, item in enumerate(limitations):
        if not isinstance(item, str) or not item.strip():
            raise FreezeValidationError(
                f"known_limitations[{index}] esta vacia o no es texto: {item!r}"
            )

    folded = _fold(" | ".join(limitations))
    missing = [
        topic
        for topic, markers in REQUIRED_LIMITATION_TOPICS
        if not any(marker in folded for marker in markers)
    ]
    if missing:
        raise FreezeValidationError(
            "known_limitations no cubre limitaciones conocidas del experimento: "
            + ", ".join(missing)
        )


#: Validadores por seccion, en el orden en que se aplican.
_SECTION_VALIDATORS = (
    validate_threshold_selection,
    validate_calibration_decision,
    validate_validation_metrics,
    validate_validation_baselines,
    validate_ablation_conclusions,
    validate_verdict_rule,
    validate_known_limitations,
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
    if freeze.model_params is None:
        raise FreezeValidationError("el freeze esta incompleto: model_params ausente")
    if not isinstance(freeze.threshold, float) or not 0.0 < freeze.threshold < 1.0:
        raise FreezeValidationError(f"umbral fuera del rango valido (0, 1): {freeze.threshold!r}")

    for section in REQUIRED_SCIENTIFIC_SECTIONS:
        value = getattr(freeze, section)
        if value is None or len(value) == 0:
            raise FreezeValidationError(
                f"seccion cientifica vacia o ausente: {section}. Un protocolo sin ella "
                "no documenta el experimento y no puede autorizar la apertura del test"
            )

    for validator in _SECTION_VALIDATORS:
        validator(freeze)


def validate_freeze_for_split(
    freeze: Any,
    dataset_fingerprint: str,
    split_signature: str,
    config_fingerprint: str,
) -> ExperimentFreeze:
    """Valida un freeze antes de permitir el acceso al conjunto de prueba.

    No basta con un objeto que declare `is_frozen=True`. Se exige el tipo del
    dominio, la version del contrato, integridad de la huella, **procedencia de
    un archivo real y coincidente**, correspondencia con el dataset, la
    configuracion y la particion concretos, y **contenido cientifico efectivo**
    en cada seccion obligatoria.

    Las tres huellas son argumentos **obligatorios**: no existe ruta valida que
    abra el test sin declarar a que dataset, a que configuracion del generador
    y a que particion pertenece el protocolo.
    """
    expected_dataset = require_fingerprint(dataset_fingerprint, "dataset_fingerprint")
    expected_config = require_fingerprint(config_fingerprint, "config_fingerprint")
    expected_split = require_fingerprint(split_signature, "split_signature")

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

    if freeze.dataset_fingerprint != expected_dataset:
        raise FreezeValidationError(
            "el freeze corresponde a otro dataset: "
            f"{freeze.dataset_fingerprint!r} != {expected_dataset!r}"
        )
    if freeze.config_fingerprint != expected_config:
        raise FreezeValidationError(
            "el freeze corresponde a otra configuracion del generador: "
            f"{freeze.config_fingerprint!r} != {expected_config!r}"
        )
    if freeze.split_signature != expected_split:
        raise FreezeValidationError(
            "el freeze corresponde a otra particion temporal: "
            f"{freeze.split_signature!r} != {expected_split!r}"
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
