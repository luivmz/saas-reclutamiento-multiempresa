"""Modelos candidatos y sus rejillas de hiperparametros.

Las rejillas son deliberadamente pequenas y justificadas. No hay AutoML ni
busqueda masiva: con un dataset sintetico, exprimir la ultima decima de metrica
produciria sobreajuste a la simulacion, no conocimiento.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

#: Semilla del experimento, la misma del dataset (decision 4 de la Fase 14).
SEED = 20260920


@dataclass(frozen=True)
class ModelCandidate:
    """Una configuracion concreta lista para entrenar."""

    family: str
    name: str
    params: dict[str, Any]

    def build(self) -> Pipeline:
        return build_pipeline(self.family, self.params)


def build_pipeline(family: str, params: dict[str, Any]) -> Pipeline:
    """Construye el pipeline de una familia.

    El escalado solo se aplica a la regresion logistica: los arboles son
    invariantes a transformaciones monotonas y escalarlos anadiria un paso sin
    efecto que solo complicaria la auditoria.
    """
    if family == "logistic_regression":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        solver="lbfgs",
                        max_iter=2000,
                        random_state=SEED,
                        **params,
                    ),
                ),
            ]
        )
    if family == "decision_tree":
        return Pipeline([("model", DecisionTreeClassifier(random_state=SEED, **params))])
    if family == "random_forest":
        return Pipeline(
            [("model", RandomForestClassifier(random_state=SEED, n_jobs=1, **params))]
        )
    if family == "hist_gradient_boosting":
        return Pipeline(
            [("model", HistGradientBoostingClassifier(random_state=SEED, **params))]
        )
    raise ValueError(f"familia de modelo desconocida: {family!r}")


def candidate_grid(include_optional: bool = True) -> list[ModelCandidate]:
    """Rejilla completa de configuraciones a evaluar en validation.

    22 configuraciones con el modelo opcional, 18 sin el. Es un numero que
    cabe en una tabla y que un revisor puede recorrer entero.
    """
    candidates: list[ModelCandidate] = []
    candidates.extend(_logistic_grid())
    candidates.extend(_tree_grid())
    candidates.extend(_forest_grid())
    if include_optional:
        candidates.extend(_boosting_grid())
    return candidates


def _logistic_grid() -> Iterator[ModelCandidate]:
    for C in (0.1, 1.0, 10.0):
        for class_weight in (None, "balanced"):
            params = {"C": C, "class_weight": class_weight}
            label = f"C={C},class_weight={class_weight}"
            yield ModelCandidate("logistic_regression", label, params)


def _tree_grid() -> Iterator[ModelCandidate]:
    for max_depth in (3, 5, 8):
        for min_samples_leaf in (20, 50):
            params = {
                "max_depth": max_depth,
                "min_samples_leaf": min_samples_leaf,
                "min_samples_split": 2 * min_samples_leaf,
            }
            label = f"max_depth={max_depth},min_samples_leaf={min_samples_leaf}"
            yield ModelCandidate("decision_tree", label, params)


def _forest_grid() -> Iterator[ModelCandidate]:
    for max_depth in (6, 10, None):
        for min_samples_leaf in (5, 20):
            params = {
                "n_estimators": 300,
                "max_depth": max_depth,
                "min_samples_leaf": min_samples_leaf,
                "max_features": "sqrt",
            }
            label = f"max_depth={max_depth},min_samples_leaf={min_samples_leaf}"
            yield ModelCandidate("random_forest", label, params)


def _boosting_grid() -> Iterator[ModelCandidate]:
    """HistGradientBoosting: opcional, incluido por venir en scikit-learn.

    No anade dependencias y ofrece una referencia no lineal mas potente que el
    bosque. Si no aporta mejora estable, la comparacion tambien es informativa.
    """
    for max_depth in (3, 6):
        for learning_rate in (0.05, 0.1):
            params = {
                "max_depth": max_depth,
                "learning_rate": learning_rate,
                "max_iter": 200,
                "min_samples_leaf": 20,
                "early_stopping": False,
            }
            label = f"max_depth={max_depth},learning_rate={learning_rate}"
            yield ModelCandidate("hist_gradient_boosting", label, params)
