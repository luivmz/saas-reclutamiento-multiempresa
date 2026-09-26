"""Calibracion de probabilidades.

La probabilidad que devuelve el modelo debe poder leerse como una frecuencia
esperada, no solo como un orden. Si esta descalibrada, cualquier umbral y
cualquier mensaje al usuario inducen a error.

La calibracion se ajusta **dentro de train**, con validacion cruzada interna.
No se usa validation para ajustarla, porque validation ya se emplea para elegir
modelo y umbral; y nunca se usa test.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold

from recruitment_ml.training.models import SEED

#: Metodo de primera opcion. La isotonica solo se justifica con mucha muestra
#: de calibracion y tiende a sobreajustar con pocos datos.
CALIBRATION_METHOD = "sigmoid"
CALIBRATION_FOLDS = 5


def calibrate(estimator: BaseEstimator, X_train: Any, y_train: Any) -> CalibratedClassifierCV:
    """Envuelve el estimador con calibracion ajustada solo en train."""
    folds = StratifiedKFold(n_splits=CALIBRATION_FOLDS, shuffle=True, random_state=SEED)
    calibrated = CalibratedClassifierCV(
        estimator=estimator, method=CALIBRATION_METHOD, cv=folds
    )
    calibrated.fit(X_train, y_train)
    return calibrated


def compare_calibration(
    uncalibrated_metrics: dict[str, Any], calibrated_metrics: dict[str, Any]
) -> dict[str, Any]:
    """Compara ambas variantes y recomienda una.

    Se adopta la calibracion solo si mejora Brier y el error de calibracion
    esperado **sin** degradar materialmente la discriminacion (AP). Mejorar la
    lectura de la probabilidad a costa de perder capacidad de ordenar no seria
    un buen intercambio.
    """
    brier_gain = uncalibrated_metrics["brier"] - calibrated_metrics["brier"]
    ece_gain = (
        uncalibrated_metrics["calibration"]["expected_calibration_error"]
        - calibrated_metrics["calibration"]["expected_calibration_error"]
    )
    ap_loss = uncalibrated_metrics["average_precision"] - calibrated_metrics["average_precision"]

    adopt = bool(brier_gain > 0 and ece_gain > 0 and ap_loss <= 0.01)
    return {
        "method": CALIBRATION_METHOD,
        "folds": CALIBRATION_FOLDS,
        "fitted_on": "train (validacion cruzada interna)",
        "brier_uncalibrated": uncalibrated_metrics["brier"],
        "brier_calibrated": calibrated_metrics["brier"],
        "brier_gain": round(float(brier_gain), 6),
        "ece_uncalibrated": uncalibrated_metrics["calibration"]["expected_calibration_error"],
        "ece_calibrated": calibrated_metrics["calibration"]["expected_calibration_error"],
        "ece_gain": round(float(ece_gain), 6),
        "average_precision_loss": round(float(ap_loss), 6),
        "adopt_calibration": adopt,
        "decision_rule": (
            "adoptar si mejora Brier y ECE y la perdida de AP no supera 0.01"
        ),
    }


def positive_scores(estimator: Any, X: Any) -> np.ndarray:
    """Probabilidad de la clase positiva."""
    return np.asarray(estimator.predict_proba(X))[:, 1]
