"""Particion temporal 70/15/15 con conjunto de prueba sellado.

La particion es **temporal**, no aleatoria: entrenar con procesos posteriores y
evaluar con anteriores seria mirar al futuro, y ademas ocultaria el drift que el
generador introduce a proposito.

El conjunto de prueba se entrega envuelto en `SealedTestSet`, que solo libera
las filas cuando existe un registro de congelacion. No es una barrera
criptografica: es una barrera de proceso que hace que usar el test antes de
tiempo tenga que ser deliberado y quede registrado.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from recruitment_ml.schema import STATUS_COMPLETED, TARGET_COLUMN

#: Proporciones aprobadas en la Fase 14 (decision 5).
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


class SealedTestSetError(RuntimeError):
    """Se intento leer el conjunto de prueba antes de congelar el experimento."""


@dataclass
class SealedTestSet:
    """Conjunto de prueba que solo se abre con un experimento congelado.

    `describe()` expone estadisticas descriptivas de la particion, que son
    necesarias para documentarla. `reveal()` entrega las filas y exige el
    registro de congelacion; cada apertura queda contada.
    """

    _frame: pd.DataFrame
    reveal_count: int = 0

    def __len__(self) -> int:
        return len(self._frame)

    def describe(self) -> dict[str, Any]:
        """Resumen descriptivo. No permite entrenar ni ajustar nada."""
        return summarise_partition(self._frame)

    def reveal(self, freeze: Any) -> pd.DataFrame:
        """Entrega las filas de prueba. Exige un `ExperimentFreeze` congelado."""
        if freeze is None or not getattr(freeze, "is_frozen", False):
            raise SealedTestSetError(
                "El conjunto de prueba solo puede abrirse con un experimento congelado. "
                "Toda decision (features, hiperparametros, modelo, umbral, calibracion) "
                "se toma con train y validation."
            )
        self.reveal_count += 1
        return self._frame.copy()


@dataclass(frozen=True)
class TemporalSplit:
    """Particion temporal del dataset model-ready."""

    train: pd.DataFrame
    validation: pd.DataFrame
    sealed_test: SealedTestSet
    boundaries: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        """Resumen de las tres particiones, para documentar el experimento."""
        return {
            "ratios": {"train": TRAIN_RATIO, "validation": VALIDATION_RATIO, "test": TEST_RATIO},
            "ordering": "checkpoint_at ascendente, desempate determinista por vacancy_id",
            "train": summarise_partition(self.train),
            "validation": summarise_partition(self.validation),
            "test": self.sealed_test.describe(),
            "boundaries": self.boundaries,
            "test_reveal_count": self.sealed_test.reveal_count,
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


def build_temporal_split(frame: pd.DataFrame) -> TemporalSplit:
    """Ordena por checkpoint y corta 70/15/15 respetando la cronologia.

    Solo entran filas etiquetadas: los procesos censurados no forman parte del
    conjunto supervisado y no se les asigna etiqueta artificial.
    """
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
    }

    return TemporalSplit(
        train=train,
        validation=validation,
        sealed_test=SealedTestSet(_frame=test),
        boundaries=boundaries,
    )


def _first_checkpoint(frame: pd.DataFrame) -> str:
    return pd.to_datetime(frame["checkpoint_at"], utc=True).min().isoformat()


def _last_checkpoint(frame: pd.DataFrame) -> str:
    return pd.to_datetime(frame["checkpoint_at"], utc=True).max().isoformat()
