"""Metricas de evaluacion.

La metrica primaria aprobada es **Average Precision**: la clase positiva es
minoritaria y interesa el desempeno sobre ella sin depender de un unico umbral.
Accuracy aparece solo como dato secundario.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    fbeta_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

#: Numero de bins de la curva de calibracion.
CALIBRATION_BINS = 10


def evaluate_predictions(
    y_true: np.ndarray, y_score: np.ndarray, threshold: float, reference_rate: float | None = None
) -> dict[str, Any]:
    """Calcula el cuadro completo de metricas para una particion.

    `reference_rate` es la prevalencia de train; sirve como predictor constante
    de referencia para el Brier Skill Score. Se pasa explicitamente para que
    nunca se calcule con los datos que se estan evaluando.
    """
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)
    y_pred = (y_score >= threshold).astype(int)

    prevalence = float(y_true.mean()) if len(y_true) else float("nan")
    brier = float(brier_score_loss(y_true, y_score))

    metrics: dict[str, Any] = {
        "n": int(len(y_true)),
        "prevalence": round(prevalence, 6),
        # El umbral se conserva con toda su precision: redondearlo cambiaria
        # clasificaciones en la frontera y las metricas dejarian de reproducirse.
        "threshold": float(threshold),
        "threshold_display": round(float(threshold), 6),
        "average_precision": round(float(average_precision_score(y_true, y_score)), 6),
        "roc_auc": round(float(roc_auc_score(y_true, y_score)), 6),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 6),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 6),
        "f1": round(float(fbeta_score(y_true, y_pred, beta=1, zero_division=0)), 6),
        "f2": round(float(fbeta_score(y_true, y_pred, beta=2, zero_division=0)), 6),
        "balanced_accuracy": round(float(balanced_accuracy_score(y_true, y_pred)), 6),
        "accuracy": round(float((y_pred == y_true).mean()), 6),
        "brier": round(brier, 6),
        "alert_rate": round(float(y_pred.mean()), 6),
    }

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    metrics["confusion_matrix"] = {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}

    if reference_rate is not None:
        baseline_brier = float(np.mean((np.full_like(y_score, reference_rate) - y_true) ** 2))
        metrics["reference_rate"] = round(float(reference_rate), 6)
        metrics["brier_reference"] = round(baseline_brier, 6)
        metrics["brier_skill_score"] = round(
            float(1.0 - brier / baseline_brier) if baseline_brier > 0 else float("nan"), 6
        )

    metrics["calibration"] = calibration_report(y_true, y_score)
    return metrics


def calibration_report(y_true: np.ndarray, y_score: np.ndarray, bins: int = CALIBRATION_BINS) -> dict[str, Any]:
    """Curva de confiabilidad y error de calibracion esperado.

    El ECE resume la distancia media entre la probabilidad anunciada y la
    frecuencia observada; los bins se reportan para poder mirarla, no solo
    resumirla en un numero.
    """
    y_true = np.asarray(y_true).astype(float)
    y_score = np.asarray(y_score).astype(float)
    edges = np.linspace(0.0, 1.0, bins + 1)
    indices = np.clip(np.digitize(y_score, edges[1:-1], right=False), 0, bins - 1)

    rows: list[dict[str, Any]] = []
    expected_error = 0.0
    maximum_error = 0.0
    for index in range(bins):
        mask = indices == index
        count = int(mask.sum())
        if count == 0:
            continue
        predicted = float(y_score[mask].mean())
        observed = float(y_true[mask].mean())
        gap = abs(predicted - observed)
        expected_error += (count / len(y_true)) * gap
        maximum_error = max(maximum_error, gap)
        rows.append(
            {
                "bin_lower": round(float(edges[index]), 3),
                "bin_upper": round(float(edges[index + 1]), 3),
                "count": count,
                "mean_predicted": round(predicted, 6),
                "observed_rate": round(observed, 6),
            }
        )

    return {
        "expected_calibration_error": round(expected_error, 6),
        "maximum_calibration_error": round(maximum_error, 6),
        "bins": rows,
    }


def metrics_by_group(
    y_true: np.ndarray, y_score: np.ndarray, groups: np.ndarray, threshold: float, minimum: int = 50
) -> dict[str, Any]:
    """Metricas desagregadas por grupo, con un minimo de casos.

    Por debajo de `minimum` no se reporta AP: con pocos casos la metrica es
    ruido y sobreinterpretarla seria un error.
    """
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)
    groups = np.asarray(groups)

    report: dict[str, Any] = {}
    for value in sorted(set(groups.tolist())):
        mask = groups == value
        count = int(mask.sum())
        subset_true = y_true[mask]
        entry: dict[str, Any] = {
            "n": count,
            "prevalence": round(float(subset_true.mean()), 6) if count else None,
        }
        if count >= minimum and 0 < subset_true.sum() < count:
            subset_score = y_score[mask]
            subset_pred = (subset_score >= threshold).astype(int)
            entry["average_precision"] = round(
                float(average_precision_score(subset_true, subset_score)), 6
            )
            entry["recall"] = round(float(recall_score(subset_true, subset_pred, zero_division=0)), 6)
            entry["precision"] = round(
                float(precision_score(subset_true, subset_pred, zero_division=0)), 6
            )
        else:
            entry["note"] = f"n<{minimum} o una sola clase: no se reportan metricas"
        report[str(value)] = entry
    return report
