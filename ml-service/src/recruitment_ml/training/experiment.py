"""Experimento completo de la Fase 15B.

Orden estricto: dataset -> particion temporal -> seleccion con train/validation
-> umbral con validation -> calibracion con train -> ablations -> **freeze** ->
apertura del conjunto de prueba **una sola vez** -> veredicto.

El conjunto de prueba esta sellado hasta que existe un registro de congelacion.
No es una formalidad: es lo que separa una evaluacion honesta de un resultado
ajustado a posteriori.

Uso:

    python -m recruitment_ml.training.experiment --rows 6000 --seed 20260920 \
        --output-dir artifacts/phase-15b
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from recruitment_ml.config import SyntheticConfig
from recruitment_ml.schema import TARGET_COLUMN
from recruitment_ml.synthetic.generator import build_dataset
from recruitment_ml.synthetic.timeline import TZ
from recruitment_ml.training.ablation import run_ablations
from recruitment_ml.training.baselines import OperationalRule, dummy_scores, fit_dummy
from recruitment_ml.training.calibration import calibrate, compare_calibration, positive_scores
from recruitment_ml.training.evaluation import evaluate_predictions, metrics_by_group
from recruitment_ml.training.models import SEED, ModelCandidate, candidate_grid
from recruitment_ml.training.preprocessing import (
    FEATURE_SET_CORE,
    build_matrix,
    build_target,
    feature_columns,
)
from recruitment_ml.training.split import TemporalSplit, build_temporal_split
from recruitment_ml.training.thresholds import (
    RULE_DESCRIPTION,
    ThresholdDecision,
    precision_recall_table,
    select_threshold,
)

__all__ = ["ExperimentFreeze", "ExperimentResult", "run_experiment", "main"]


#: Criterios de veredicto, **comparativos** y fijados antes de ver el test.
#:
#: La Fase 14 prohibio inventar cifras absolutas de AP, recall o precision. Por
#: eso todo criterio se expresa frente a un baseline o frente al propio
#: comportamiento en validation.
VERDICT_CRITERIA = {
    "must_beat_dummy_ap": "AP(test) del modelo > AP(test) del baseline trivial",
    "must_beat_operational_ap": "AP(test) del modelo > AP(test) del baseline operacional",
    "must_have_positive_bss": "Brier Skill Score(test) > 0 frente al predictor constante de train",
    "limitation_if_margin_halves": (
        "si el margen de AP sobre el baseline operacional en test cae por debajo "
        "de la mitad del margen en validation, se declara GO CON LIMITACIONES"
    ),
    "limitation_if_proxy_dependent": (
        "si quitar concurrent_open_vacancies_count degrada AP en mas de 0.02 respecto "
        "del conjunto core en validation, se declara GO CON LIMITACIONES por riesgo de "
        "atajo temporal. El 0.02 es una tolerancia de sensibilidad sobre una diferencia, "
        "declarada antes del freeze; no es un objetivo de desempeno"
    ),
}

VERDICT_GO = "PREDICTIVE GO"
VERDICT_GO_LIMITED = "PREDICTIVE GO WITH LIMITATIONS"
VERDICT_NO_GO = "PREDICTIVE NO-GO"


@dataclass(frozen=True)
class ExperimentFreeze:
    """Configuracion congelada. Su existencia autoriza abrir el conjunto de prueba."""

    feature_set: str
    features: list[str]
    model_family: str
    model_params: dict[str, Any]
    preprocessing: str
    calibrated: bool
    threshold: float
    threshold_rule: str
    seed: int
    dataset_fingerprint: str
    config_fingerprint: str
    validation_metrics: dict[str, Any]
    ablation_decision: dict[str, Any]
    verdict_criteria: dict[str, str] = field(default_factory=lambda: dict(VERDICT_CRITERIA))
    is_frozen: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_frozen": self.is_frozen,
            "feature_set": self.feature_set,
            "features": self.features,
            "model_family": self.model_family,
            "model_params": self.model_params,
            "preprocessing": self.preprocessing,
            "calibrated": self.calibrated,
            "threshold": round(float(self.threshold), 6),
            "threshold_rule": self.threshold_rule,
            "seed": self.seed,
            "dataset_fingerprint": self.dataset_fingerprint,
            "config_fingerprint": self.config_fingerprint,
            "validation_metrics": self.validation_metrics,
            "ablation_decision": self.ablation_decision,
            "verdict_criteria": self.verdict_criteria,
            "note": (
                "Registro congelado antes de abrir el conjunto de prueba. "
                "Ninguna decision posterior puede basarse en test."
            ),
        }


@dataclass
class ExperimentResult:
    """Resultado completo, listo para serializar."""

    dataset: dict[str, Any]
    split: dict[str, Any]
    model_selection: dict[str, Any]
    baselines: dict[str, Any]
    threshold: dict[str, Any]
    calibration: dict[str, Any]
    ablations: dict[str, Any]
    freeze: dict[str, Any]
    test: dict[str, Any]
    temporal: dict[str, Any]
    organizations: dict[str, Any]
    censoring: dict[str, Any]
    feature_importance: dict[str, Any]
    verdict: dict[str, Any]
    curves: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase": "15B",
            "dataset": self.dataset,
            "split": self.split,
            "model_selection": self.model_selection,
            "baselines": self.baselines,
            "threshold": self.threshold,
            "calibration": self.calibration,
            "ablations": self.ablations,
            "freeze": self.freeze,
            "test": self.test,
            "temporal_stability": self.temporal,
            "organizations": self.organizations,
            "censoring": self.censoring,
            "feature_importance": self.feature_importance,
            "verdict": self.verdict,
            "curves": self.curves,
            "validity_notice": (
                "Entrenado y evaluado exclusivamente con datos sinteticos. Cientificamente "
                "aceptable no equivale a desplegable: GAP-01 sigue abierto y el modelo no "
                "puede integrarse en Laravel."
            ),
        }


def run_experiment(
    rows: int = 6_000, seed: int = SEED, include_optional_model: bool = True
) -> ExperimentResult:
    """Ejecuta el experimento completo y devuelve el resultado estructurado."""
    # --- 1. dataset del generador de 15A, sin dataset paralelo --------
    config = SyntheticConfig(rows=rows, seed=seed)
    dataset = build_dataset(config)
    frame = dataset.model_ready()

    split = build_temporal_split(frame)
    train, validation = split.train, split.validation
    y_train = build_target(train)
    y_validation = build_target(validation)
    reference_rate = float(train[TARGET_COLUMN].astype(float).mean())

    X_train = build_matrix(train, FEATURE_SET_CORE)
    X_validation = build_matrix(validation, FEATURE_SET_CORE)

    # --- 2. baselines --------------------------------------------------
    baselines = _evaluate_baselines(
        train, validation, y_train, y_validation, reference_rate
    )

    # --- 3. seleccion de modelo con validation -------------------------
    grid = candidate_grid(include_optional=include_optional_model)
    leaderboard: list[dict[str, Any]] = []
    fitted: dict[str, Any] = {}
    for candidate in grid:
        pipeline = candidate.build()
        pipeline.fit(X_train, y_train)
        scores = positive_scores(pipeline, X_validation)
        metrics = evaluate_predictions(
            y_validation.to_numpy(), scores, threshold=0.5, reference_rate=reference_rate
        )
        key = f"{candidate.family}|{candidate.name}"
        fitted[key] = (candidate, pipeline, scores)
        leaderboard.append(
            {
                "family": candidate.family,
                "params": candidate.params,
                "average_precision": metrics["average_precision"],
                "roc_auc": metrics["roc_auc"],
                "brier": metrics["brier"],
                "expected_calibration_error": metrics["calibration"]["expected_calibration_error"],
            }
        )

    leaderboard.sort(key=lambda row: -row["average_precision"])
    selected_key, selected_candidate = _select_candidate(leaderboard, fitted)
    candidate, pipeline, validation_scores = fitted[selected_key]

    # --- 4. calibracion, ajustada solo con train -----------------------
    uncalibrated_metrics = evaluate_predictions(
        y_validation.to_numpy(), validation_scores, threshold=0.5, reference_rate=reference_rate
    )
    calibrated_model = calibrate(candidate.build(), X_train, y_train)
    calibrated_scores = positive_scores(calibrated_model, X_validation)
    calibrated_metrics = evaluate_predictions(
        y_validation.to_numpy(), calibrated_scores, threshold=0.5, reference_rate=reference_rate
    )
    calibration_report = compare_calibration(uncalibrated_metrics, calibrated_metrics)

    use_calibration = calibration_report["adopt_calibration"]
    final_model = calibrated_model if use_calibration else pipeline
    final_validation_scores = calibrated_scores if use_calibration else validation_scores

    # --- 5. umbral, elegido solo con validation ------------------------
    precision_floor = float(baselines["operational"]["validation"]["precision"])
    recall_floor = float(baselines["operational"]["validation"]["recall"])
    decision: ThresholdDecision = select_threshold(
        y_validation.to_numpy(),
        final_validation_scores,
        precision_floor=precision_floor,
        recall_floor=recall_floor,
    )

    validation_metrics = evaluate_predictions(
        y_validation.to_numpy(),
        final_validation_scores,
        threshold=decision.threshold,
        reference_rate=reference_rate,
    )

    # --- 6. ablations, tambien sobre validation ------------------------
    ablations = run_ablations(candidate, train, validation, threshold=decision.threshold)

    # --- 7. FREEZE -----------------------------------------------------
    freeze = ExperimentFreeze(
        feature_set=FEATURE_SET_CORE,
        features=list(feature_columns(FEATURE_SET_CORE)),
        model_family=candidate.family,
        model_params=candidate.params,
        preprocessing="StandardScaler dentro del Pipeline (solo para regresion logistica)",
        calibrated=bool(use_calibration),
        threshold=decision.threshold,
        threshold_rule=RULE_DESCRIPTION,
        seed=seed,
        dataset_fingerprint=str(dataset.manifest["model_ready_fingerprint"]),
        config_fingerprint=str(dataset.manifest["config_fingerprint"]),
        validation_metrics=validation_metrics,
        ablation_decision=ablations["interpretation"],
    )

    # --- 8. TEST: se abre una sola vez, ya congelado --------------------
    test = split.sealed_test.reveal(freeze)
    y_test = build_target(test)
    X_test = build_matrix(test, FEATURE_SET_CORE)
    test_scores = positive_scores(final_model, X_test)
    test_metrics = evaluate_predictions(
        y_test.to_numpy(), test_scores, threshold=freeze.threshold, reference_rate=reference_rate
    )

    baselines["dummy_prior"]["test"] = _dummy_on(test, y_train, y_test, reference_rate, freeze.threshold)
    baselines["operational"]["test"] = _operational_on(test, y_test, reference_rate)

    # --- 9. analisis posteriores (descriptivos, sin reajustar nada) ----
    temporal = _temporal_analysis(
        final_model, split, freeze, reference_rate, train, validation, test, test_scores
    )
    organizations = {
        "note": (
            "organization_id nunca entra en X; se usa solo como metadato de evaluacion. "
            "Las organizaciones son ficticias: no describen ninguna institucion real."
        ),
        "validation": metrics_by_group(
            y_validation.to_numpy(),
            final_validation_scores,
            validation["organization_id"].to_numpy(),
            freeze.threshold,
        ),
        "test": metrics_by_group(
            y_test.to_numpy(), test_scores, test["organization_id"].to_numpy(), freeze.threshold
        ),
    }
    censoring = _censoring_analysis(dataset, split)
    importance = _feature_importance(pipeline, candidate, list(feature_columns(FEATURE_SET_CORE)))
    verdict = _decide_verdict(test_metrics, baselines, validation_metrics, ablations)

    curves = {
        "validation_precision_recall": precision_recall_table(
            y_validation.to_numpy(), final_validation_scores
        ),
        "test_precision_recall": precision_recall_table(y_test.to_numpy(), test_scores),
    }

    split_summary = split.summary()
    split_summary["test_reveal_count"] = split.sealed_test.reveal_count

    return ExperimentResult(
        dataset={
            "rows_requested": rows,
            "seed": seed,
            "rows_model_ready": int(dataset.manifest["rows_model_ready"]),
            "censored_total": int(dataset.manifest["censored_total"]),
            "prevalence": dataset.manifest["prevalence"],
            "config_fingerprint": dataset.manifest["config_fingerprint"],
            "full_fingerprint": dataset.manifest["dataset_fingerprint"],
            "model_ready_fingerprint": dataset.manifest["model_ready_fingerprint"],
        },
        split=split_summary,
        model_selection={
            "feature_set": FEATURE_SET_CORE,
            "n_features": len(feature_columns(FEATURE_SET_CORE)),
            "configurations_evaluated": len(grid),
            "selection_metric": "average_precision en validation",
            "selection_rule": (
                "mayor AP; si otra familia mas simple queda dentro de 0.005 de AP, "
                "se prefiere la mas simple por estabilidad e interpretabilidad"
            ),
            "selected": selected_candidate,
            "leaderboard": leaderboard,
        },
        baselines=baselines,
        threshold=decision.to_dict(),
        calibration=calibration_report,
        ablations=ablations,
        freeze=freeze.to_dict(),
        test=test_metrics,
        temporal=temporal,
        organizations=organizations,
        censoring=censoring,
        feature_importance=importance,
        verdict=verdict,
        curves=curves,
    )


#: Orden de preferencia por simplicidad, para desempatar modelos equivalentes.
FAMILY_SIMPLICITY = {
    "logistic_regression": 0,
    "decision_tree": 1,
    "random_forest": 2,
    "hist_gradient_boosting": 3,
}

#: Margen de AP dentro del cual dos modelos se consideran equivalentes.
EQUIVALENCE_MARGIN = 0.005


def _select_candidate(
    leaderboard: list[dict[str, Any]], fitted: dict[str, Any]
) -> tuple[str, dict[str, Any]]:
    """Elige el modelo candidato con preferencia explicita por la simplicidad.

    No se toma el maximo de AP sin mas: si un modelo mas simple queda dentro del
    margen de equivalencia, se prefiere, porque es mas estable, mas facil de
    explicar y mas barato de desplegar.
    """
    best_ap = leaderboard[0]["average_precision"]
    contenders = [row for row in leaderboard if best_ap - row["average_precision"] <= EQUIVALENCE_MARGIN]
    contenders.sort(
        key=lambda row: (FAMILY_SIMPLICITY.get(row["family"], 99), -row["average_precision"])
    )
    chosen = contenders[0]

    for key, (candidate, _pipeline, _scores) in fitted.items():
        if candidate.family == chosen["family"] and candidate.params == chosen["params"]:
            return key, {
                "family": chosen["family"],
                "params": chosen["params"],
                "validation_average_precision": chosen["average_precision"],
                "best_available_average_precision": best_ap,
                "equivalence_margin": EQUIVALENCE_MARGIN,
                "simpler_model_preferred": chosen["average_precision"] < best_ap,
            }
    raise RuntimeError("no se encontro el pipeline del candidato elegido")  # pragma: no cover


def _evaluate_baselines(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    y_train: pd.Series,
    y_validation: pd.Series,
    reference_rate: float,
) -> dict[str, Any]:
    """Baseline trivial y baseline operacional, evaluados en validation."""
    prior = fit_dummy(y_train.to_numpy(), strategy="prior", seed=SEED)
    prior_scores = dummy_scores(prior, len(validation))
    most_frequent = fit_dummy(y_train.to_numpy(), strategy="most_frequent", seed=SEED)
    most_frequent_scores = dummy_scores(most_frequent, len(validation))

    rule = OperationalRule()
    rule_scores = rule.decide(validation)

    return {
        "dummy_prior": {
            "description": "DummyClassifier(strategy='prior'): predictor constante de train",
            "validation": evaluate_predictions(
                y_validation.to_numpy(), prior_scores, threshold=0.5, reference_rate=reference_rate
            ),
        },
        "dummy_most_frequent": {
            "description": "DummyClassifier(strategy='most_frequent')",
            "validation": evaluate_predictions(
                y_validation.to_numpy(),
                most_frequent_scores,
                threshold=0.5,
                reference_rate=reference_rate,
            ),
        },
        "operational": {
            "description": rule.describe(),
            "validation": evaluate_predictions(
                y_validation.to_numpy(), rule_scores, threshold=0.5, reference_rate=reference_rate
            ),
        },
    }


def _dummy_on(
    frame: pd.DataFrame, y_train: pd.Series, y_true: pd.Series, reference_rate: float, threshold: float
) -> dict[str, Any]:
    prior = fit_dummy(y_train.to_numpy(), strategy="prior", seed=SEED)
    scores = dummy_scores(prior, len(frame))
    return evaluate_predictions(
        y_true.to_numpy(), scores, threshold=threshold, reference_rate=reference_rate
    )


def _operational_on(frame: pd.DataFrame, y_true: pd.Series, reference_rate: float) -> dict[str, Any]:
    scores = OperationalRule().decide(frame)
    return evaluate_predictions(
        y_true.to_numpy(), scores, threshold=0.5, reference_rate=reference_rate
    )


def _temporal_analysis(
    model: Any,
    split: TemporalSplit,
    freeze: ExperimentFreeze,
    reference_rate: float,
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
    test_scores: np.ndarray,
) -> dict[str, Any]:
    """Desempeno por particion y por ano, para observar degradacion y drift."""
    train_scores = positive_scores(model, build_matrix(train, freeze.feature_set))
    validation_scores = positive_scores(model, build_matrix(validation, freeze.feature_set))

    partitions = {
        "train": evaluate_predictions(
            build_target(train).to_numpy(), train_scores, freeze.threshold, reference_rate
        ),
        "validation": evaluate_predictions(
            build_target(validation).to_numpy(), validation_scores, freeze.threshold, reference_rate
        ),
        "test": evaluate_predictions(
            build_target(test).to_numpy(), test_scores, freeze.threshold, reference_rate
        ),
    }

    by_year: dict[str, Any] = {}
    for label, frame, scores in (
        ("train", train, train_scores),
        ("validation", validation, validation_scores),
        ("test", test, test_scores),
    ):
        years = pd.to_datetime(frame["checkpoint_at"], utc=True).dt.year.to_numpy()
        by_year[label] = metrics_by_group(
            build_target(frame).to_numpy(), scores, years, freeze.threshold
        )

    return {
        "by_partition": {
            key: {
                "average_precision": value["average_precision"],
                "roc_auc": value["roc_auc"],
                "recall": value["recall"],
                "precision": value["precision"],
                "f2": value["f2"],
                "brier": value["brier"],
                "prevalence": value["prevalence"],
            }
            for key, value in partitions.items()
        },
        "by_year": by_year,
        "validation_to_test_ap_delta": round(
            float(partitions["test"]["average_precision"] - partitions["validation"]["average_precision"]),
            6,
        ),
    }


def _censoring_analysis(dataset: Any, split: TemporalSplit) -> dict[str, Any]:
    """Censura por bloque temporal, usando los mismos cortes de la particion."""
    full = dataset.frame.assign(
        _checkpoint=pd.to_datetime(dataset.frame["checkpoint_at"], utc=True)
    )
    boundaries = split.boundaries
    train_end = pd.Timestamp(boundaries["train_last_checkpoint"])
    validation_end = pd.Timestamp(boundaries["validation_last_checkpoint"])

    blocks = {
        "train_window": full[full["_checkpoint"] <= train_end],
        "validation_window": full[
            (full["_checkpoint"] > train_end) & (full["_checkpoint"] <= validation_end)
        ],
        "test_window": full[full["_checkpoint"] > validation_end],
    }

    contextual = {
        name: {
            "n_total": int(len(block)),
            "censored": int((block["observation_status"] == "censored").sum()),
            "censoring_rate": round(
                float((block["observation_status"] == "censored").mean()) if len(block) else 0.0, 6
            ),
        }
        for name, block in blocks.items()
    }

    return {
        "excluded_from_supervised_training": True,
        "labels_never_imputed": True,
        "dataset_censoring_ratio": dataset.manifest["censoring_ratio"],
        "mechanism": dataset.manifest["censoring_mechanism"],
        "standardised_mean_differences": dataset.manifest["censoring_comparison"][
            "standardised_mean_differences"
        ],
        "largest_absolute_smd": dataset.manifest["censoring_comparison"]["largest_absolute_smd"],
        "contextual_by_window": contextual,
        "limitation": (
            "La censura es informativa por diseno: los procesos estancados nunca cierran. "
            "El conjunto supervisado esta sesgado hacia procesos que terminaron, y ese sesgo "
            "acompana a toda conclusion."
        ),
    }


def _feature_importance(
    pipeline: Any, candidate: ModelCandidate, features: list[str]
) -> dict[str, Any]:
    """Coeficientes estandarizados o importancias, siempre como descripcion."""
    model = pipeline.named_steps["model"]
    entry: dict[str, Any] = {
        "family": candidate.family,
        "interpretation_warning": (
            "Los coeficientes y las importancias son descriptivos. No son causalidad. "
            "elapsed_days_since_publication y application_window_days estan casi colineales "
            "(Pearson 0.972), asi que su reparto de peso es inestable y no debe leerse "
            "como importancia relativa real."
        ),
    }
    if hasattr(model, "coef_"):
        coefficients = np.asarray(model.coef_).ravel()
        entry["standardised_coefficients"] = {
            name: round(float(value), 6)
            for name, value in sorted(
                zip(features, coefficients, strict=True), key=lambda pair: -abs(pair[1])
            )
        }
        entry["intercept"] = round(float(np.asarray(model.intercept_).ravel()[0]), 6)
    elif hasattr(model, "feature_importances_"):
        importances = np.asarray(model.feature_importances_).ravel()
        entry["feature_importances"] = {
            name: round(float(value), 6)
            for name, value in sorted(
                zip(features, importances, strict=True), key=lambda pair: -pair[1]
            )
        }
    else:  # pragma: no cover - toda familia usada expone una de las dos
        entry["note"] = "el modelo no expone coeficientes ni importancias"
    return entry


def _decide_verdict(
    test_metrics: dict[str, Any],
    baselines: dict[str, Any],
    validation_metrics: dict[str, Any],
    ablations: dict[str, Any],
) -> dict[str, Any]:
    """Aplica los criterios comparativos fijados antes de abrir el test."""
    model_ap = test_metrics["average_precision"]
    dummy_ap = baselines["dummy_prior"]["test"]["average_precision"]
    operational_ap = baselines["operational"]["test"]["average_precision"]
    bss = test_metrics.get("brier_skill_score", float("nan"))

    margin_validation = (
        validation_metrics["average_precision"]
        - baselines["operational"]["validation"]["average_precision"]
    )
    margin_test = model_ap - operational_ap

    concurrency_delta = ablations["results"]["core_without_concurrency"][
        "average_precision_delta_vs_core"
    ]

    checks = {
        "beats_dummy": bool(model_ap > dummy_ap),
        "beats_operational": bool(model_ap > operational_ap),
        "positive_brier_skill": bool(bss > 0),
        "margin_preserved": bool(margin_test >= 0.5 * margin_validation) if margin_validation > 0 else True,
        "not_proxy_dependent": bool(concurrency_delta >= -0.02),
    }

    limitations: list[str] = []
    if not checks["margin_preserved"]:
        limitations.append(
            f"el margen de AP sobre el baseline operacional cae de {margin_validation:.4f} "
            f"en validation a {margin_test:.4f} en test"
        )
    if not checks["not_proxy_dependent"]:
        limitations.append(
            f"quitar concurrent_open_vacancies_count degrada AP en {concurrency_delta:+.4f}: "
            "el modelo se apoya en una feature correlacionada con el calendario"
        )

    if not (checks["beats_dummy"] and checks["beats_operational"] and checks["positive_brier_skill"]):
        decision = VERDICT_NO_GO
    elif limitations:
        decision = VERDICT_GO_LIMITED
    else:
        decision = VERDICT_GO

    return {
        "decision": decision,
        "criteria": VERDICT_CRITERIA,
        "checks": checks,
        "limitations": limitations,
        "evidence": {
            "model_ap_test": model_ap,
            "dummy_ap_test": dummy_ap,
            "operational_ap_test": operational_ap,
            "brier_skill_score_test": bss,
            "margin_validation": round(float(margin_validation), 6),
            "margin_test": round(float(margin_test), 6),
            "concurrency_ablation_delta": concurrency_delta,
        },
        "deployment_note": (
            "Cientificamente aceptable no equivale a desplegable. GAP-01 sigue abierto: "
            "target_completion_at no existe en Laravel, RF-29 continua como candidato y no "
            "se autoriza integracion ni servicio HTTP."
        ),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def _evidence_summary(result: ExperimentResult) -> dict[str, Any]:
    """Resumen pequeno y versionable, sin curvas ni tablas extensas."""
    data = result.to_dict()
    return {
        "phase": "15B",
        "dataset": data["dataset"],
        "split": {
            key: value
            for key, value in data["split"].items()
            if key in {"ratios", "ordering", "train", "validation", "test", "boundaries"}
        },
        "selected_model": data["model_selection"]["selected"],
        "configurations_evaluated": data["model_selection"]["configurations_evaluated"],
        "threshold": data["threshold"],
        "calibration": data["calibration"],
        "validation_metrics": data["freeze"]["validation_metrics"],
        "test_metrics": data["test"],
        "baselines_test": {
            "dummy_prior": data["baselines"]["dummy_prior"]["test"],
            "operational": data["baselines"]["operational"]["test"],
        },
        "ablations": data["ablations"]["results"],
        "ablation_interpretation": data["ablations"]["interpretation"],
        "temporal_stability": data["temporal_stability"]["by_partition"],
        "organizations_test": data["organizations"]["test"],
        "censoring": data["censoring"],
        "feature_importance": data["feature_importance"],
        "verdict": data["verdict"],
        "validity_notice": data["validity_notice"],
    }


def main(argv: list[str] | None = None) -> int:
    """CLI reproducible del experimento."""
    parser = argparse.ArgumentParser(
        prog="recruitment_ml.training.experiment",
        description="Experimento de entrenamiento y evaluacion de la Fase 15B (datos sinteticos).",
    )
    parser.add_argument("--rows", type=int, default=6_000)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output-dir", type=Path, default=None, help="Artefactos completos (ignorados por Git)")
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=None,
        help="Evidencia academica reducida y versionable (freeze + resumen)",
    )
    parser.add_argument(
        "--skip-optional-model",
        action="store_true",
        help="Omite HistGradientBoosting de la rejilla",
    )
    args = parser.parse_args(argv)

    result = run_experiment(
        rows=args.rows, seed=args.seed, include_optional_model=not args.skip_optional_model
    )
    payload = result.to_dict()

    if args.output_dir is not None:
        directory = args.output_dir
        _write_json(directory / "metrics.json", payload["test"])
        _write_json(directory / "split-summary.json", payload["split"])
        _write_json(directory / "ablation-results.json", payload["ablations"])
        _write_json(directory / "calibration-results.json", payload["calibration"])
        _write_json(directory / "freeze.json", payload["freeze"])
        _write_json(directory / "experiment.json", payload)
        _write_json(
            directory / "curves.json",
            {
                **payload["curves"],
                "generated_at": datetime.now(tz=TZ).isoformat(),
            },
        )
        print(f"artefactos completos en {directory}")

    if args.evidence_dir is not None:
        _write_json(args.evidence_dir / "phase-15b-experiment-freeze.json", payload["freeze"])
        _write_json(args.evidence_dir / "phase-15b-results-summary.json", _evidence_summary(result))
        print(f"evidencia versionable en {args.evidence_dir}")

    print(f"configuraciones evaluadas : {payload['model_selection']['configurations_evaluated']}")
    print(f"modelo seleccionado       : {payload['model_selection']['selected']['family']}")
    print(f"umbral (solo validation)  : {payload['threshold']['threshold']}")
    print(f"AP validation             : {payload['freeze']['validation_metrics']['average_precision']}")
    print(f"AP test                   : {payload['test']['average_precision']}")
    print(f"aperturas del test        : {payload['split']['test_reveal_count']}")
    print(f"veredicto                 : {payload['verdict']['decision']}")
    if payload["verdict"]["limitations"]:
        for item in payload["verdict"]["limitations"]:
            print(f"  limitacion: {item}", file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover - entrada de linea de comandos
    raise SystemExit(main())
