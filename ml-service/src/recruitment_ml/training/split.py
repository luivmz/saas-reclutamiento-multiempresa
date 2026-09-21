"""Particion temporal 70/15/15 con conjunto de prueba sellado.

La particion es **temporal**, no aleatoria: entrenar con procesos posteriores y
evaluar con anteriores seria mirar al futuro, y ademas ocultaria el drift que el
generador introduce a proposito.

Sobre el sellado del conjunto de prueba
---------------------------------------
`SealedTestSet` es una **garantia de protocolo de software**, no una prueba
historica ni una barrera criptografica. Reduce las rutas accidentales de acceso
y obliga a que abrir el test sea un acto deliberado y registrado:

- las filas viven en un atributo con *name mangling*, no en un campo publico;
- antes de revelar, `describe()` **no expone etiquetas**: ni prevalencia ni
  numero de positivos;
- `reveal()` exige un `ExperimentFreeze` valido, integro y **cargado desde
  disco**, que ademas corresponda a este dataset, a esta configuracion del
  generador y a esta particion; las tres huellas son obligatorias y no admiten
  valor por defecto.

Nada de esto impide que alguien con acceso al proceso lea el atributo privado.
No se afirma lo contrario.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from recruitment_ml.schema import STATUS_COMPLETED, TARGET_COLUMN
from recruitment_ml.training.freeze import (
    FreezeValidationError,
    require_fingerprint,
    validate_freeze_for_split,
)

#: Proporciones aprobadas en la Fase 14 (decision 5).
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


class SealedTestSetError(RuntimeError):
    """Se intento acceder al conjunto de prueba sin un protocolo valido."""


class SealedTestSet:
    """Conjunto de prueba que solo se abre con un freeze persistido y valido."""

    def __init__(
        self,
        frame: pd.DataFrame,
        dataset_fingerprint: str,
        split_signature: str,
        config_fingerprint: str,
    ) -> None:
        #: Las tres huellas son obligatorias y se validan aqui: no existe forma
        #: publica de construir un conjunto sellado sin enlace efectivo al
        #: dataset, a la configuracion del generador y a la particion.
        self.__frame = frame
        self.dataset_fingerprint = require_fingerprint(dataset_fingerprint, "dataset_fingerprint")
        self.config_fingerprint = require_fingerprint(config_fingerprint, "config_fingerprint")
        self.split_signature = require_fingerprint(split_signature, "split_signature")
        #: Aperturas en **esta instancia y esta ejecucion**. No es un registro
        #: historico: no demuestra cuantas veces se observo el test a lo largo
        #: del proyecto.
        self.reveal_count = 0

    def __len__(self) -> int:
        return len(self.__frame)

    def __repr__(self) -> str:  # pragma: no cover - ayuda de diagnostico
        return f"SealedTestSet(n={len(self.__frame)}, revealed={self.reveal_count})"

    @property
    def revealed(self) -> bool:
        return self.reveal_count > 0

    def identifiers(self) -> pd.Series:
        """Identificadores de las vacantes del test, sin etiquetas.

        Permite auditar que las particiones son disjuntas sin revelar nada del
        desenlace. `vacancy_id` es metadato de linaje: nunca entra en X.
        """
        return self.__frame["vacancy_id"].copy()

    def describe(self) -> dict[str, Any]:
        """Resumen de la particion.

        **Antes de revelar no expone etiquetas**: ni prevalencia ni positivos.
        Documentar el tamano y el periodo de la particion es legitimo; conocer
        su distribucion de clases antes de congelar el protocolo, no.
        """
        checkpoints = pd.to_datetime(self.__frame["checkpoint_at"], utc=True)
        summary: dict[str, Any] = {
            "n": int(len(self.__frame)),
            "organizations": int(self.__frame["organization_id"].nunique()),
            "start": checkpoints.min().isoformat(),
            "end": checkpoints.max().isoformat(),
            "labels_disclosed": self.revealed,
        }
        if not self.revealed:
            summary["note"] = (
                "Etiquetas no divulgadas: la prevalencia del test solo se reporta "
                "despues de revelarlo con un protocolo congelado."
            )
            return summary

        target = self.__frame[TARGET_COLUMN].astype(float)
        summary["prevalence"] = round(float(target.mean()), 6)
        summary["positives"] = int(target.sum())
        return summary

    def reveal(self, freeze: Any) -> pd.DataFrame:
        """Entrega las filas de prueba. Exige un freeze valido y persistido."""
        try:
            validate_freeze_for_split(
                freeze,
                dataset_fingerprint=self.dataset_fingerprint,
                split_signature=self.split_signature,
                config_fingerprint=self.config_fingerprint,
            )
        except FreezeValidationError as error:
            raise SealedTestSetError(
                f"no se puede abrir el conjunto de prueba: {error}"
            ) from error
        self.reveal_count += 1
        return self.__frame.copy()


@dataclass(frozen=True)
class TemporalSplit:
    """Particion temporal del dataset model-ready."""

    train: pd.DataFrame
    validation: pd.DataFrame
    sealed_test: SealedTestSet
    signature: str
    boundaries: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        """Resumen de las tres particiones, para documentar el experimento."""
        return {
            "ratios": {"train": TRAIN_RATIO, "validation": VALIDATION_RATIO, "test": TEST_RATIO},
            "ordering": (
                "checkpoint_at ascendente. Los empates de timestamp se resuelven de forma "
                "determinista por vacancy_id, de modo que la frontera entre particiones puede "
                "contener el mismo instante en ambos lados; no se afirma desigualdad estricta "
                "fila a fila."
            ),
            "signature": self.signature,
            "train": summarise_partition(self.train),
            "validation": summarise_partition(self.validation),
            "test": self.sealed_test.describe(),
            "boundaries": self.boundaries,
            "test_reveal_count": self.sealed_test.reveal_count,
            "test_reveal_count_scope": (
                "aperturas en esta instancia y ejecucion; no es un registro historico"
            ),
        }


def summarise_partition(frame: pd.DataFrame) -> dict[str, Any]:
    """Estadisticas descriptivas de una particion."""
    checkpoints = pd.to_datetime(frame["checkpoint_at"], utc=True)
    target = frame[TARGET_COLUMN].astype(float)
    return {
        "n": int(len(frame)),
        "prevalence": round(float(target.mean()), 6),
        "positives": int(target.sum()),
        "organizations": int(frame["organization_id"].nunique()),
        "start": checkpoints.min().isoformat(),
        "end": checkpoints.max().isoformat(),
    }


def build_temporal_split(
    frame: pd.DataFrame, dataset_fingerprint: str, config_fingerprint: str
) -> TemporalSplit:
    """Ordena por checkpoint y corta 70/15/15 respetando la cronologia.

    Solo entran filas etiquetadas: los procesos censurados no forman parte del
    conjunto supervisado y no se les asigna etiqueta artificial.

    Ambas huellas son **obligatorias**. Antes tenian un valor por defecto vacio
    y esa comodidad permitia construir una particion sin enlace real con la
    configuracion que la produjo, de modo que la comprobacion posterior del
    freeze se saltaba sin que nadie lo notara.
    """
    dataset_fingerprint = require_fingerprint(dataset_fingerprint, "dataset_fingerprint")
    config_fingerprint = require_fingerprint(config_fingerprint, "config_fingerprint")

    if "observation_status" in frame.columns:
        labelled = frame[frame["observation_status"] == STATUS_COMPLETED]
    else:  # pragma: no cover - el dataset siempre trae la columna
        labelled = frame
    labelled = labelled[labelled[TARGET_COLUMN].notna()]

    if labelled.empty:
        raise ValueError("no hay filas etiquetadas para particionar")

    ordered = labelled.assign(
        _checkpoint=pd.to_datetime(labelled["checkpoint_at"], utc=True)
    ).sort_values(["_checkpoint", "vacancy_id"], kind="mergesort")

    total = len(ordered)
    train_end = int(round(total * TRAIN_RATIO))
    validation_end = train_end + int(round(total * VALIDATION_RATIO))

    train = ordered.iloc[:train_end].drop(columns="_checkpoint").reset_index(drop=True)
    validation = (
        ordered.iloc[train_end:validation_end].drop(columns="_checkpoint").reset_index(drop=True)
    )
    test = ordered.iloc[validation_end:].drop(columns="_checkpoint").reset_index(drop=True)

    boundaries = {
        "train_end_index": train_end,
        "validation_end_index": validation_end,
        "total_rows": total,
        "train_last_checkpoint": _last_checkpoint(train),
        "validation_first_checkpoint": _first_checkpoint(validation),
        "validation_last_checkpoint": _last_checkpoint(validation),
        "test_first_checkpoint": _first_checkpoint(test),
        "boundary_note": (
            "Un mismo checkpoint_at puede aparecer a ambos lados de una frontera; el corte "
            "es por posicion tras un orden determinista, no por desigualdad estricta de tiempo."
        ),
    }

    signature = _split_signature(dataset_fingerprint, boundaries, len(train), len(validation), len(test))

    return TemporalSplit(
        train=train,
        validation=validation,
        sealed_test=SealedTestSet(
            frame=test,
            dataset_fingerprint=dataset_fingerprint,
            split_signature=signature,
            config_fingerprint=config_fingerprint,
        ),
        signature=signature,
        boundaries=boundaries,
    )


def _split_signature(
    dataset_fingerprint: str,
    boundaries: dict[str, Any],
    n_train: int,
    n_validation: int,
    n_test: int,
) -> str:
    """Huella de la particion, para que un freeze no sirva con otra."""
    material = "|".join(
        [
            dataset_fingerprint,
            str(n_train),
            str(n_validation),
            str(n_test),
            str(boundaries["train_last_checkpoint"]),
            str(boundaries["validation_first_checkpoint"]),
            str(boundaries["validation_last_checkpoint"]),
            str(boundaries["test_first_checkpoint"]),
        ]
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _first_checkpoint(frame: pd.DataFrame) -> str:
    return pd.to_datetime(frame["checkpoint_at"], utc=True).min().isoformat()


def _last_checkpoint(frame: pd.DataFrame) -> str:
    return pd.to_datetime(frame["checkpoint_at"], utc=True).max().isoformat()
