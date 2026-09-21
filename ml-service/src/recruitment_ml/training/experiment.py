"""Experimento completo de la Fase 15B.

Orden estricto, impuesto por el codigo:

1. dataset del generador de 15A;
2. particion temporal;
3. seleccion de modelo con train/validation;
4. umbral con validation;
5. calibracion ajustada solo con train;
6. ablations sobre validation;
7. **persistencia del freeze en disco**;
8. recarga del freeze y verificacion de integridad;
9. apertura del conjunto de prueba con ese freeze;
10. evaluacion de test y resultados en artefacto **separado**.

El paso 7 ocurre **antes** del 9: el protocolo se materializa en disco antes de
que exista cualquier numero de test, y el artefacto de resultados referencia su
huella. La direccion de la dependencia es `resultados -> protocolo`.

Uso:

    python -m recruitment_ml.training.experiment --rows 6000 --seed 20260920 \
        --output-dir artifacts/phase-15b --evidence-dir ../docs/v1.1/ml
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from recruitment_ml.config import SyntheticConfig
from recruitment_ml.schema import TARGET_COLUMN
from recruitment_ml.synthetic.generator import build_dataset
from recruitment_ml.synthetic.timeline import TZ
from recruitment_ml.training.ablation import ABLATION_FEATURE_SETS, run_ablations
from recruitment_ml.training.baselines import OperationalRule, dummy_scores, fit_dummy
from recruitment_ml.training.calibration import calibrate, compare_calibration, positive_scores
from recruitment_ml.training.evaluation import evaluate_predictions, metrics_by_group
from recruitment_ml.training.freeze import (
    FREEZE_SCHEMA_VERSION,
    ExperimentFreeze,
    TestResults,
    build_freeze,
    load_freeze,
    persist_freeze,
    persist_test_results,
)
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

__all__ = [
    "ExperimentResult",
    "run_experiment",
    "main",
    "VERDICT_GO",
    "VERDICT_GO_LIMITED",
    "VERDICT_NO_GO",
    "VERDICT_CRITERIA",
    "KNOWN_LIMITATIONS",
]


#: Criterios de veredicto, **comparativos** y fijados antes de ver el test.
#:
#: La Fase 14 prohibio inventar cifras absolutas de AP, recall o precision. Cada
#: criterio se expresa frente a un baseline o frente al comportamiento en
#: validation. La dependencia de `concurrent_open_vacancies_count` **no** es un
#: criterio de gate: se reporta de forma descriptiva.
VERDICT_CRITERIA = {
    "must_beat_dummy_ap": "AP(test) del modelo por encima de AP(test) del baseline trivial",
    "must_beat_operational_ap": "AP(test) del modelo por encima de AP(test) del baseline operacional",
    "must_have_positive_bss": "Brier Skill Score(test) positivo frente al predictor constante de train",
    "limitation_if_margin_halves": (
        "si el margen de AP sobre el baseline operacional en test cae por debajo "
        "de la mitad del margen en validation, se anota como limitacion"
    ),
    "limitations_downgrade_the_verdict": (
        "si se cumplen los criterios comparativos pero persisten limitaciones conocidas, "
        "el veredicto es GO CON LIMITACIONES, no GO a secas"
    ),
    "not_deployable_while_gap_01_open": (
        "ningun veredicto favorable autoriza despliegue mientras GAP-01 siga abierto: "
        "target_completion_at no existe en Laravel, asi que days_remaining_to_target no es "
        "computable en produccion y el modelo no puede servirse"
    ),
}

#: Limitaciones conocidas **antes** de mirar el test. Forman parte del protocolo
#: congelado y por si solas degradan el veredicto a GO CON LIMITACIONES.
KNOWN_LIMITATIONS = [
    "Datos exclusivamente sinteticos: el resultado demuestra metodo, no validez institucional.",
    "Censura informativa por diseno: el conjunto supervisado esta sesgado hacia procesos que cerraron.",
    "Colinealidad fuerte entre features (elapsed/window y applications/stage_transitions): "
    "los coeficientes no son interpretables como importancia relativa.",
    "concurrent_open_vacancies_count correlaciona con el calendario y puede actuar como proxy temporal.",
    "Heterogeneidad esperada entre organizaciones sinteticas.",
    "Tasa de alerta elevada en el punto de operacion elegido: la regla de umbral prioriza "
    "recall sobre precision y en validation marca una fraccion alta de los procesos. El coste "
    "de revisar cada alerta no esta modelado, asi que la carga operativa real es desconocida.",
    "CONTAMINACION PROCEDIMENTAL MENOR: durante el desarrollo de 15B se observo la AP de test "
    "antes de cerrar la version final de la regla de umbral. AP es invariante al umbral y "
    "ninguna metrica de test dependiente del umbral se inspecciono antes de esa correccion, "
    "pero el holdout no puede describirse como intacto.",
    "GAP-01 abierto: days_remaining_to_target no es computable en Laravel, asi que el modelo "
    "no es desplegable aunque sea cientificamente aceptable.",
]

VERDICT_GO = "PREDICTIVE GO"
VERDICT_GO_LIMITED = "PREDICTIVE GO WITH LIMITATIONS"
VERDICT_NO_GO = "PREDICTIVE NO-GO"


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
    freeze_object: ExperimentFreeze
    test_results: TestResults

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
    rows: int = 6_000,
    seed: int = SEED,
    include_optional_model: bool = True,
    freeze_path: Path | None = None,
) -> ExperimentResult:
    """Ejecuta el experimento completo y devuelve el resultado estructurado.

    `freeze_path` es donde se materializa el protocolo antes de tocar el test.
    Si no se indica, se usa un archivo temporal: la persistencia ocurre igual,
    porque es un paso del protocolo y no una opcion de salida.
    """
    with tempfile.TemporaryDirectory() as scratch:
        target_path = freeze_path or Path(scratch) / "phase-15b-experiment-freeze.json"
        return _run(rows, seed, include_optional_model, Path(target_path))


def _run(
    rows: int, seed: int, include_optional_model: bool, freeze_path: Path
) -> ExperimentResult:
    # --- 1. dataset del generador de 15A, sin dataset paralelo --------
    config = SyntheticConfig(rows=rows, seed=seed)
    dataset = build_dataset(config)
    frame = dataset.model_ready()
    dataset_fingerprint = str(dataset.manifest["model_ready_fingerprint"])
    config_fingerprint = str(dataset.manifest["config_fingerprint"])

    split = build_temporal_split(
        frame,
        dataset_fingerprint=dataset_fingerprint,
        config_fingerprint=config_fingerprint,
    )
    train, validation = split.train, split.validation
    y_train = build_target(train)
    y_validation = build_target(validation)
    reference_rate = float(train[TARGET_COLUMN].astype(float).mean())

    X_train = build_matrix(train, FEATURE_SET_CORE)
    X_validation = build_matrix(validation, FEATURE_SET_CORE)

    # --- 2. baselines --------------------------------------------------
    baselines = _evaluate_baselines(validation, y_train, y_validation, reference_rate)

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

    # --- 7. FREEZE: se construye y se PERSISTE antes de tocar el test --
    freeze = build_freeze(
        experiment_id=f"phase-15b-{seed}-{rows}",
        seed=seed,
        dataset_fingerprint=dataset_fingerprint,
        config_fingerprint=config_fingerprint,
        split_signature=split.signature,
        split_definition={
            "ratios": {"train": 0.70, "validation": 0.15, "test": 0.15},
            "ordering": "checkpoint_at ascendente, desempate determinista por vacancy_id",
            "boundaries": split.boundaries,
            "n_train": int(len(train)),
            "n_validation": int(len(validation)),
            "n_test": int(len(split.sealed_test)),
        },
        feature_set=FEATURE_SET_CORE,
        features=list(feature_columns(FEATURE_SET_CORE)),
        excluded_features=["configured_stage_count", "evaluations_pending_count", "interviews_pending_count"],
        ablation_feature_sets=list(ABLATION_FEATURE_SETS),
        preprocessing="StandardScaler dentro del Pipeline (solo para regresion logistica)",
        model_family=candidate.family,
        model_params=candidate.params,
        threshold=float(decision.threshold),
        threshold_rule=RULE_DESCRIPTION,
        threshold_selection=decision.to_dict(),
        calibration_decision=calibration_report,
        validation_metrics=validation_metrics,
        validation_baselines={
            "dummy_prior": baselines["dummy_prior"]["validation"],
            "operational": baselines["operational"]["validation"],
        },
        ablation_conclusions=ablations["interpretation"],
        verdict_rule=dict(VERDICT_CRITERIA),
        known_limitations=list(KNOWN_LIMITATIONS),
    )
    persist_freeze(freeze, freeze_path)

    # --- 8. se recarga desde disco y se verifica su integridad ---------
    persisted_freeze = load_freeze(freeze_path)
    if persisted_freeze.freeze_fingerprint != freeze.freeze_fingerprint:  # pragma: no cover
        raise RuntimeError("el freeze persistido no coincide con el construido en memoria")

    # --- 9. TEST: se abre con el freeze persistido ---------------------
    test = split.sealed_test.reveal(persisted_freeze)
    y_test = build_target(test)
    X_test = build_matrix(test, FEATURE_SET_CORE)
    test_scores = positive_scores(final_model, X_test)
    test_metrics = evaluate_predictions(
        y_test.to_numpy(),
        test_scores,
        threshold=persisted_freeze.threshold,
        reference_rate=reference_rate,
    )

    baselines["dummy_prior"]["test"] = _dummy_on(
        test, y_train, y_test, reference_rate, persisted_freeze.threshold
    )
    baselines["operational"]["test"] = _operational_on(test, y_test, reference_rate)

    # --- 10. analisis posteriores (descriptivos, sin reajustar nada) ---
    temporal = _temporal_analysis(
        final_model, persisted_freeze, reference_rate, train, validation, test, test_scores
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
            persisted_freeze.threshold,
        ),
        "test": metrics_by_group(
            y_test.to_numpy(),
            test_scores,
            test["organization_id"].to_numpy(),
            persisted_freeze.threshold,
        ),
    }
    censoring = _censoring_analysis(dataset, split)
    importance = _feature_importance(pipeline, candidate, list(feature_columns(FEATURE_SET_CORE)))
    verdict = _decide_verdict(test_metrics, baselines, validation_metrics, ablations, persisted_freeze)

    curves = {
        "validation_precision_recall": precision_recall_table(
            y_validation.to_numpy(), final_validation_scores
        ),
        "test_precision_recall": precision_recall_table(y_test.to_numpy(), test_scores),
    }

    test_results = TestResults(
        schema_version=FREEZE_SCHEMA_VERSION,
        experiment_id=persisted_freeze.experiment_id,
        freeze_fingerprint=persisted_freeze.freeze_fingerprint,
        dataset_fingerprint=dataset_fingerprint,
        threshold=float(persisted_freeze.threshold),
        metrics=test_metrics,
        baselines={
            "dummy_prior": baselines["dummy_prior"]["test"],
            "operational": baselines["operational"]["test"],
        },
        organizations=organizations["test"],
        temporal_stability=temporal,
        verdict=verdict,
        limitations=list(persisted_freeze.known_limitations),
        evaluated_at=datetime.now(tz=TZ).isoformat(),
        curves=curves,
    )

    return ExperimentResult(
        dataset={
            "rows_requested": rows,
            "seed": seed,
            "rows_model_ready": int(dataset.manifest["rows_model_ready"]),
            "censored_total": int(dataset.manifest["censored_total"]),
            "prevalence": dataset.manifest["prevalence"],
            "config_fingerprint": dataset.manifest["config_fingerprint"],
            "full_fingerprint": dataset.manifest["dataset_fingerprint"],
            "model_ready_fingerprint": dataset_fingerprint,
        },
        split=split.summary(),
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
        freeze=persisted_freeze.to_dict(),
        test=test_metrics,
        temporal=temporal,
        organizations=organizations,
        censoring=censoring,
        feature_importance=importance,
        verdict=verdict,
        curves=curves,
        freeze_object=persisted_freeze,
        test_results=test_results,
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
    """Elige el modelo candidato con preferencia explicita por la simplicidad."""
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
            "(Pearson 0.972), y applications_received_count y stage_transition_count lo estan "
            "por construccion, asi que el reparto de peso es inestable y no debe leerse como "
            "importancia relativa real."
        ),
    }
    if hasattr(model, "coef_"):
        coefficients = np.asarray(model.coef_).ravel()
        ranked = sorted(zip(features, coefficients, strict=True), key=lambda pair: -abs(pair[1]))
        entry["standardised_coefficients_ranked"] = [
            {"feature": name, "coefficient": round(float(value), 6)} for name, value in ranked
        ]
        entry["intercept"] = round(float(np.asarray(model.intercept_).ravel()[0]), 6)
    elif hasattr(model, "feature_importances_"):
        importances = np.asarray(model.feature_importances_).ravel()
        ranked = sorted(zip(features, importances, strict=True), key=lambda pair: -pair[1])
        entry["feature_importances_ranked"] = [
            {"feature": name, "importance": round(float(value), 6)} for name, value in ranked
        ]
    else:  # pragma: no cover - toda familia usada expone una de las dos
        entry["note"] = "el modelo no expone coeficientes ni importancias"
    return entry


def _decide_verdict(
    test_metrics: dict[str, Any],
    baselines: dict[str, Any],
    validation_metrics: dict[str, Any],
    ablations: dict[str, Any],
    freeze: ExperimentFreeze,
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
    }

    limitations = list(freeze.known_limitations)
    if not checks["margin_preserved"]:
        limitations.append(
            f"el margen de AP sobre el baseline operacional cae de {margin_validation:.4f} "
            f"en validation a {margin_test:.4f} en test"
        )
    limitations.append(
        f"Tasa de alerta en test {test_metrics['alert_rate']:.3f} con el umbral congelado: "
        "el punto de operacion marca una fraccion alta de los procesos."
    )

    if not (checks["beats_dummy"] and checks["beats_operational"] and checks["positive_brier_skill"]):
        decision = VERDICT_NO_GO
    elif limitations:
        decision = VERDICT_GO_LIMITED
    else:  # pragma: no cover - siempre hay limitaciones conocidas en este experimento
        decision = VERDICT_GO

    return {
        "decision": decision,
        "criteria": dict(VERDICT_CRITERIA),
        "checks": checks,
        "limitations": limitations,
        "evidence": {
            "model_ap_test": model_ap,
            "dummy_ap_test": dummy_ap,
            "operational_ap_test": operational_ap,
            "brier_skill_score_test": bss,
            "margin_validation": round(float(margin_validation), 6),
            "margin_test": round(float(margin_test), 6),
        },
        "concurrency_ablation": {
            "average_precision_delta_vs_core": concurrency_delta,
            "reported_as": "descriptivo, no criterio de gate",
            "reading": (
                "la dependencia observada de concurrent_open_vacancies_count es pequena o "
                "moderada en este experimento; no se preregistro ningun umbral que la "
                "convierta en criterio de aprobacion"
            ),
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
        help="Evidencia academica versionable: freeze pre-test y resultados post-test",
    )
    parser.add_argument(
        "--skip-optional-model",
        action="store_true",
        help="Omite HistGradientBoosting de la rejilla",
    )
    args = parser.parse_args(argv)

    # El freeze se materializa en el directorio de evidencia cuando existe, de
    # modo que el artefacto versionable sea literalmente el que abrio el test.
    freeze_path = (
        args.evidence_dir / "phase-15b-experiment-freeze.json" if args.evidence_dir else None
    )
    result = run_experiment(
        rows=args.rows,
        seed=args.seed,
        include_optional_model=not args.skip_optional_model,
        freeze_path=freeze_path,
    )
    payload = result.to_dict()

    if args.evidence_dir is not None:
        persist_test_results(
            result.test_results, args.evidence_dir / "phase-15b-test-results.json"
        )
        _write_json(
            args.evidence_dir / "phase-15b-results-summary.json", _evidence_summary(result)
        )
        print(f"freeze pre-test y resultados post-test en {args.evidence_dir}")

    if args.output_dir is not None:
        directory = args.output_dir
        _write_json(directory / "metrics.json", payload["test"])
        _write_json(directory / "split-summary.json", payload["split"])
        _write_json(directory / "ablation-results.json", payload["ablations"])
        _write_json(directory / "calibration-results.json", payload["calibration"])
        _write_json(directory / "freeze.json", payload["freeze"])
        _write_json(directory / "test-results.json", result.test_results.to_dict())
        _write_json(directory / "experiment.json", payload)
        _write_json(
            directory / "curves.json",
            {**payload["curves"], "generated_at": datetime.now(tz=TZ).isoformat()},
        )
        print(f"artefactos completos en {directory}")

    print(f"configuraciones evaluadas : {payload['model_selection']['configurations_evaluated']}")
    print(f"modelo seleccionado       : {payload['model_selection']['selected']['family']}")
    print(f"umbral exacto             : {payload['freeze']['threshold']!r}")
    print(f"freeze fingerprint        : {payload['freeze']['freeze_fingerprint']}")
    print(f"AP validation             : {payload['freeze']['validation_metrics']['average_precision']}")
    print(f"AP test                   : {payload['test']['average_precision']}")
    print(f"aperturas del test        : {payload['split']['test_reveal_count']} (en esta ejecucion)")
    print(f"veredicto                 : {payload['verdict']['decision']}")
    for item in payload["verdict"]["limitations"]:
        print(f"  limitacion: {item}", file=sys.stderr)
    return 0


def _evidence_summary(result: ExperimentResult) -> dict[str, Any]:
    """Resumen pequeno y versionable, sin curvas ni tablas extensas."""
    data = result.to_dict()
    return {
        "phase": "15B",
        "dataset": data["dataset"],
        "split": {
            key: value
            for key, value in data["split"].items()
            if key in {"ratios", "ordering", "train", "validation", "test", "boundaries", "signature"}
        },
        "selected_model": data["model_selection"]["selected"],
        "configurations_evaluated": data["model_selection"]["configurations_evaluated"],
        "threshold": data["threshold"],
        "freeze_fingerprint": data["freeze"]["freeze_fingerprint"],
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


if __name__ == "__main__":  # pragma: no cover - entrada de linea de comandos
    raise SystemExit(main())
