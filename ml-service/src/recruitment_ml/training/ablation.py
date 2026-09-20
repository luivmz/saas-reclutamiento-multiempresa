"""Ablations obligatorias sobre el conjunto de features.

La auditoria de 15A dejo tres obligaciones. Dos responden a la misma pregunta:
**¿el modelo aprende senal operacional o simplemente el paso del calendario?**

- `concurrent_open_vacancies_count` correlaciona 0.685 con el tiempo, en parte
  porque los procesos estancados nunca cierran y se acumulan;
- `elapsed_days_since_publication` queda casi colineal con
  `application_window_days` por construccion del checkpoint;
- `configured_stage_count` tiene cardinalidad maxima 2 y se evalua como
  experimental.

Los hiperparametros **no** se reajustan por conjunto: se mantiene la
configuracion elegida para aislar el efecto de la feature y no confundirlo con
un ajuste distinto.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from recruitment_ml.schema import TARGET_COLUMN
from recruitment_ml.training.calibration import positive_scores
from recruitment_ml.training.evaluation import evaluate_predictions
from recruitment_ml.training.models import ModelCandidate
from recruitment_ml.training.preprocessing import (
    FEATURE_SET_CORE,
    FEATURE_SET_NO_CONCURRENCY,
    FEATURE_SET_NO_ELAPSED,
    FEATURE_SET_WITH_STAGE_COUNT,
    build_matrix,
    build_target,
    feature_columns,
)

#: Conjuntos comparados. Cuatro, no una explosion combinatoria.
ABLATION_FEATURE_SETS = (
    FEATURE_SET_CORE,
    FEATURE_SET_NO_CONCURRENCY,
    FEATURE_SET_NO_ELAPSED,
    FEATURE_SET_WITH_STAGE_COUNT,
)


def run_ablations(
    candidate: ModelCandidate,
    train: pd.DataFrame,
    validation: pd.DataFrame,
    threshold: float,
) -> dict[str, Any]:
    """Entrena la configuracion elegida sobre cada conjunto y compara en validation."""
    y_train = build_target(train)
    y_validation = build_target(validation)
    reference_rate = float(train[TARGET_COLUMN].astype(float).mean())

    results: dict[str, Any] = {}
    for feature_set in ABLATION_FEATURE_SETS:
        X_train = build_matrix(train, feature_set)
        X_validation = build_matrix(validation, feature_set)

        pipeline = candidate.build()
        pipeline.fit(X_train, y_train)
        scores = positive_scores(pipeline, X_validation)
        metrics = evaluate_predictions(
            y_validation.to_numpy(), scores, threshold=threshold, reference_rate=reference_rate
        )
        results[feature_set] = {
            "n_features": len(feature_columns(feature_set)),
            "features": list(feature_columns(feature_set)),
            "average_precision": metrics["average_precision"],
            "roc_auc": metrics["roc_auc"],
            "recall": metrics["recall"],
            "precision": metrics["precision"],
            "f2": metrics["f2"],
            "brier": metrics["brier"],
            "expected_calibration_error": metrics["calibration"]["expected_calibration_error"],
        }

    baseline_ap = results[FEATURE_SET_CORE]["average_precision"]
    for feature_set, entry in results.items():
        entry["average_precision_delta_vs_core"] = round(
            float(entry["average_precision"] - baseline_ap), 6
        )

    return {
        "candidate": {"family": candidate.family, "params": candidate.params},
        "threshold_used": round(float(threshold), 6),
        "evaluated_on": "validation",
        "hyperparameters_retuned_per_set": False,
        "results": results,
        "interpretation": _interpret(results),
    }


def _interpret(results: dict[str, Any]) -> dict[str, str]:
    """Lectura textual de las diferencias, sin atribuir causalidad."""
    core = results[FEATURE_SET_CORE]["average_precision"]
    readings: dict[str, str] = {}

    for feature_set, label in (
        (FEATURE_SET_NO_CONCURRENCY, "concurrent_open_vacancies_count"),
        (FEATURE_SET_NO_ELAPSED, "elapsed_days_since_publication"),
    ):
        delta = results[feature_set]["average_precision"] - core
        if delta >= -0.005:
            readings[label] = (
                f"quitarla no degrada AP (delta={delta:+.4f}): el modelo no depende de ella"
            )
        elif delta >= -0.02:
            readings[label] = (
                f"quitarla degrada AP levemente (delta={delta:+.4f}): aporta senal moderada"
            )
        else:
            readings[label] = (
                f"quitarla degrada AP de forma apreciable (delta={delta:+.4f}): el modelo "
                "se apoya en ella y conviene vigilar el riesgo de atajo temporal"
            )

    delta_stage = results[FEATURE_SET_WITH_STAGE_COUNT]["average_precision"] - core
    if delta_stage <= 0.005:
        readings["configured_stage_count"] = (
            f"anadirla no mejora AP (delta={delta_stage:+.4f}): se mantiene fuera del nucleo"
        )
    else:
        readings["configured_stage_count"] = (
            f"anadirla mejora AP (delta={delta_stage:+.4f}): merece revision en fases futuras"
        )
    return readings
