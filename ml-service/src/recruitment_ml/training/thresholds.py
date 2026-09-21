"""Seleccion del umbral operativo.

La Fase 14 prohibio fijar un umbral arbitrario y **no aprobo ninguna cifra**
minima de precision o recall. Por eso la regla implementada aqui es
**relativa**, no absoluta: los suelos no se inventan, se toman de la regla
operacional que el equipo podria aplicar hoy sin modelo.

Regla, aplicada **solo sobre validation**:

1. calcular la curva precision-recall del modelo en validation;
2. tomar como referencia la precision y el recall que obtiene el baseline
   operacional sobre esa misma particion;
3. considerar elegibles los umbrales que **no empeoran ninguno de los dos
   ejes**: precision >= precision del baseline y recall >= recall del baseline;
4. entre los elegibles, elegir el de **mayor F2**, que pondera el recall cuatro
   veces mas que la precision y es por tanto recall-oriented por construccion;
5. desempatar por mayor recall y, si persiste, por el umbral mas bajo;
6. si ningun umbral domina al baseline, elegir el de mayor F2 sobre toda la
   curva y marcarlo con `floor_satisfied=false`.

Por que dominar en ambos ejes y no solo poner un suelo de precision: una regla
que solo exigiera precision >= la del baseline y despues maximizara recall
converge al umbral mas bajo admisible y termina alertando sobre la gran mayoria
de los procesos. El plan de evaluacion aprobado advierte expresamente contra la
fatiga de alertas, asi que un punto de operacion que marca casi todo no seria
util aunque satisficiera la restriccion. Maximizar F2 dentro de la region que
domina al baseline conserva la orientacion al recall sin degenerar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from sklearn.metrics import precision_recall_curve


@dataclass(frozen=True)
class ThresholdDecision:
    """Umbral elegido y la evidencia que lo respalda."""

    threshold: float
    precision: float
    recall: float
    f2: float
    precision_floor: float
    recall_floor: float
    floor_satisfied: bool
    rule: str
    candidates_considered: int
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            # Precision completa: el valor redondeado es solo para lectura y
            # nunca debe usarse para inferir.
            "threshold": float(self.threshold),
            "threshold_display": round(float(self.threshold), 6),
            "precision": round(float(self.precision), 6),
            "recall": round(float(self.recall), 6),
            "f2": round(float(self.f2), 6),
            "precision_floor": round(float(self.precision_floor), 6),
            "recall_floor": round(float(self.recall_floor), 6),
            "floor_satisfied": bool(self.floor_satisfied),
            "rule": self.rule,
            "candidates_considered": int(self.candidates_considered),
            "selected_on": "validation",
            **self.details,
        }


RULE_DESCRIPTION = (
    "Referencia = precision y recall del baseline operacional en validation. "
    "Elegibles: umbrales que no empeoran ninguno de los dos ejes "
    "(precision >= precision_floor y recall >= recall_floor). "
    "Entre ellos se elige el de mayor F2; desempate por mayor recall y luego "
    "por umbral menor. Si ninguno domina al baseline, se elige el de mayor F2 "
    "sobre toda la curva y se marca floor_satisfied=false."
)


def _fbeta(precision: np.ndarray, recall: np.ndarray, beta: float) -> np.ndarray:
    beta2 = beta * beta
    denominator = beta2 * precision + recall
    with np.errstate(divide="ignore", invalid="ignore"):
        score = (1 + beta2) * precision * recall / denominator
    return np.nan_to_num(score, nan=0.0, posinf=0.0, neginf=0.0)


def select_threshold(
    y_validation: np.ndarray,
    scores_validation: np.ndarray,
    precision_floor: float,
    recall_floor: float,
) -> ThresholdDecision:
    """Elige el umbral operativo usando exclusivamente validation."""
    y_validation = np.asarray(y_validation).astype(int)
    scores_validation = np.asarray(scores_validation).astype(float)

    precision, recall, cut_points = precision_recall_curve(y_validation, scores_validation)
    # `precision_recall_curve` devuelve un punto final sin umbral asociado.
    precision = precision[:-1]
    recall = recall[:-1]
    f2 = _fbeta(precision, recall, beta=2.0)

    eligible = (precision >= precision_floor) & (recall >= recall_floor)
    floor_satisfied = bool(eligible.any())

    if floor_satisfied:
        indices = np.flatnonzero(eligible)
        # Mayor F2; desempate por mayor recall y despues por umbral mas bajo.
        order = sorted(
            indices.tolist(),
            key=lambda i: (-f2[i], -recall[i], cut_points[i]),
        )
        chosen = order[0]
        rule = RULE_DESCRIPTION
    else:
        chosen = int(np.argmax(f2))
        rule = RULE_DESCRIPTION + " (ningun umbral domino al baseline: respaldo por F2)"

    return ThresholdDecision(
        threshold=float(cut_points[chosen]),
        precision=float(precision[chosen]),
        recall=float(recall[chosen]),
        f2=float(f2[chosen]),
        precision_floor=float(precision_floor),
        recall_floor=float(recall_floor),
        floor_satisfied=floor_satisfied,
        rule=rule,
        candidates_considered=int(len(cut_points)),
        details={"eligible_thresholds": int(eligible.sum())},
    )


def precision_recall_table(
    y_true: np.ndarray, y_score: np.ndarray, points: int = 25
) -> list[dict[str, float]]:
    """Curva precision-recall muestreada, para versionar como evidencia.

    Se guarda una tabla pequena en vez de una figura: es reproducible,
    comparable y no anade artefactos binarios al repositorio.
    """
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)
    precision, recall, cut_points = precision_recall_curve(y_true, y_score)
    precision, recall = precision[:-1], recall[:-1]
    if len(cut_points) == 0:  # pragma: no cover - no ocurre con datos reales
        return []
    indices = np.unique(np.linspace(0, len(cut_points) - 1, num=min(points, len(cut_points))).astype(int))
    return [
        {
            "threshold": round(float(cut_points[i]), 6),
            "precision": round(float(precision[i]), 6),
            "recall": round(float(recall[i]), 6),
        }
        for i in indices
    ]
