"""Baselines de referencia.

Son dos cosas distintas y no deben confundirse con un modelo candidato:

- el **baseline trivial** fija el suelo que cualquier modelo debe superar;
- el **baseline operacional** representa lo que el equipo podria hacer hoy con
  una regla simple, y es la comparacion que de verdad importa.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier

#: Parametros de la regla operacional documentada en la Fase 15A.
#: Se mantienen fijos para que la comparacion sea honesta: optimizarlos contra
#: el conjunto de prueba convertiria el baseline en un modelo encubierto.
OPERATIONAL_K = 1
OPERATIONAL_D = 10


@dataclass(frozen=True)
class OperationalRule:
    """Regla de backlog e inactividad.

    ``alerta  <=>  (evaluaciones vencidas + entrevistas vencidas) >= k
                   o  dias sin actividad >= d``

    Devuelve una puntuacion binaria: no tiene probabilidad que calibrar. Por eso
    su Average Precision se lee como referencia, no como discriminacion fina.
    """

    k: int = OPERATIONAL_K
    d: int = OPERATIONAL_D

    def decide(self, frame: pd.DataFrame) -> np.ndarray:
        overdue = (
            frame["evaluations_overdue_pending_count"] + frame["interviews_overdue_pending_count"]
        )
        idle = frame["days_since_last_operational_event"]
        return ((overdue >= self.k) | (idle >= self.d)).to_numpy().astype(float)

    def describe(self) -> dict[str, object]:
        return {
            "name": "operational_rule",
            "k": self.k,
            "d": self.d,
            "formula": (
                "(evaluations_overdue_pending_count + interviews_overdue_pending_count) >= k "
                "OR days_since_last_operational_event >= d"
            ),
            "tuned_on": "ninguno: parametros fijos documentados en la Fase 15A",
        }


def fit_dummy(y_train: np.ndarray, strategy: str = "prior", seed: int = 0) -> DummyClassifier:
    """Baseline trivial.

    `prior` devuelve siempre la prevalencia de train, que es el predictor
    constante contra el que se mide el Brier Skill Score. `most_frequent` da la
    misma decision dura pero probabilidades degeneradas, asi que se reporta como
    comparacion secundaria.
    """
    model = DummyClassifier(strategy=strategy, random_state=seed)
    model.fit(np.zeros((len(y_train), 1)), np.asarray(y_train))
    return model


def dummy_scores(model: DummyClassifier, n_rows: int) -> np.ndarray:
    """Probabilidades del baseline trivial para `n_rows` observaciones."""
    return model.predict_proba(np.zeros((n_rows, 1)))[:, 1]
