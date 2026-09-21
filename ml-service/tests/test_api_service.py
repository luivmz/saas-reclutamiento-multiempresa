"""API HTTP del servicio experimental.

Las pruebas atraviesan la aplicacion entera con `TestClient`: validacion,
dependencias, manejo de errores y serializacion. Probar las funciones sueltas
dejaria fuera precisamente lo que puede fallar en un servicio.

Dos garantias reciben atencion especial:

- el contrato de features es una **frontera**: un identificador o un atributo
  personal en el payload se rechaza, no se ignora;
- el orden del JSON **no** puede cambiar la prediccion.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pytest
from fastapi.testclient import TestClient

from recruitment_ml.api.app import SERVICE_VERSION, create_app
from recruitment_ml.serving.metadata import ArtifactMetadata
from recruitment_ml.serving.paths import ARTIFACT_DIR_ENV, artifact_path, metadata_path

THRESHOLD = 0.1679418172266036
FREEZE_FINGERPRINT = "9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2"


@pytest.fixture
def client(monkeypatch, built_artifact) -> TestClient:
    """Servicio con el artefacto cargado, como en una ejecucion real."""
    directory, _, _ = built_artifact
    monkeypatch.setenv(ARTIFACT_DIR_ENV, str(directory))
    with TestClient(create_app()) as test_client:
        yield test_client


@pytest.fixture
def client_without_model(monkeypatch, tmp_path: Path) -> TestClient:
    """Servicio vivo pero sin artefacto: el caso que no debe fingir estar listo."""
    monkeypatch.setenv(ARTIFACT_DIR_ENV, str(tmp_path / "vacio"))
    with TestClient(create_app()) as test_client:
        yield test_client


@pytest.fixture
def payload(sample_features) -> dict[str, int]:
    return {name: int(value) for name, value in sample_features.items()}


# --- /health ---------------------------------------------------------------


def test_health_reports_a_live_service_with_a_ready_model(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_ready"] is True
    assert body["version"] == SERVICE_VERSION
    assert body["detail"] is None


def test_health_separates_process_from_model(client_without_model: TestClient) -> None:
    """Sin modelo el proceso sigue vivo, y lo dice: es mas util que morir."""
    response = client_without_model.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_ready"] is False
    assert body["detail"] == "modelo no cargado"


def test_health_leaks_no_paths_or_traces(client_without_model: TestClient) -> None:
    body = client_without_model.get("/health").text

    for leak in ("artifacts", ".joblib", "Traceback", "site-packages", "C:\\\\"):
        assert leak not in body


# --- /v1/model-info --------------------------------------------------------


def test_model_info_describes_the_frozen_experiment(client: TestClient) -> None:
    response = client.get("/v1/model-info")

    assert response.status_code == 200
    body = response.json()
    assert body["model_family"] == "logistic_regression"
    assert body["experiment_id"] == "phase-15b-20260920-6000"
    assert body["freeze_fingerprint"] == FREEZE_FINGERPRINT
    assert body["threshold"] == THRESHOLD
    assert len(body["feature_order"]) == 15


def test_model_info_states_the_verdict_and_the_limits(client: TestClient) -> None:
    """La API no puede presentar el modelo como mas solido de lo que es."""
    body = client.get("/v1/model-info").json()

    assert body["verdict"] == "PREDICTIVE GO WITH LIMITATIONS"
    assert body["deployment_status"] == "experimental"
    assert body["gap_01_open"] is True
    assert "GAP-01" in body["gap_01_note"]
    assert "target_completion_at" in body["gap_01_note"]


def test_model_info_explains_what_the_score_is_not(client: TestClient) -> None:
    body = client.get("/v1/model-info").json()

    assert "no evalua" in body["risk_score_meaning"].lower()
    assert "revision humana" in body["risk_flag_meaning"].lower()
    for forbidden in ("candidate score", "hiring", "suitability", "ranking de candidatos"):
        assert forbidden not in json.dumps(body).lower()


def test_model_info_exposes_no_training_data_or_paths(client: TestClient) -> None:
    body = client.get("/v1/model-info").text

    for leak in ("artifacts", ".joblib", "n_train", "built_at", "rows"):
        assert leak not in body


def test_model_info_is_unavailable_without_a_model(client_without_model: TestClient) -> None:
    response = client_without_model.get("/v1/model-info")

    assert response.status_code == 503
    assert response.json()["error"] == "model_unavailable"


# --- /v1/predict: camino valido -------------------------------------------


def test_predict_returns_a_probability_and_a_flag(client: TestClient, payload) -> None:
    response = client.post("/v1/predict", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert 0.0 <= body["risk_score"] <= 1.0
    assert body["risk_flag"] == (body["risk_score"] >= body["threshold"])
    assert body["status"] == "experimental"


def test_predict_reports_the_exact_frozen_threshold(client: TestClient, payload) -> None:
    body = client.post("/v1/predict", json=payload).json()

    assert body["threshold"] == THRESHOLD
    assert repr(body["threshold"]) == repr(THRESHOLD)


def test_predict_identifies_the_model_that_answered(client: TestClient, payload) -> None:
    body = client.post("/v1/predict", json=payload).json()

    assert body["model_version"] == "phase-15b-20260920-6000"
    assert body["freeze_fingerprint"] == FREEZE_FINGERPRINT


def test_predict_is_deterministic(client: TestClient, payload) -> None:
    first = client.post("/v1/predict", json=payload).json()
    second = client.post("/v1/predict", json=payload).json()

    assert first == second


def test_the_json_field_order_does_not_change_the_answer(client: TestClient, payload) -> None:
    """El JSON conserva el orden de insercion; la matriz no debe heredarlo."""
    reversed_payload = dict(reversed(list(payload.items())))
    assert list(reversed_payload) != list(payload)

    first = client.post("/v1/predict", json=payload).json()
    second = client.post("/v1/predict", json=reversed_payload).json()

    assert first["risk_score"] == second["risk_score"]
    assert first["risk_flag"] == second["risk_flag"]


def test_a_different_process_gets_a_different_score(client: TestClient, payload) -> None:
    """Prueba de cordura: el modelo responde al input, no devuelve una constante."""
    stressed = dict(
        payload,
        days_remaining_to_target=1,
        evaluations_overdue_pending_count=25,
        interviews_overdue_pending_count=18,
        days_since_last_operational_event=60,
    )

    calm = client.post("/v1/predict", json=payload).json()
    risky = client.post("/v1/predict", json=stressed).json()

    assert calm["risk_score"] != risky["risk_score"]


# --- /v1/predict: validacion ----------------------------------------------


def test_an_unknown_field_is_rejected(client: TestClient, payload) -> None:
    response = client.post("/v1/predict", json=dict(payload, sorpresa=1))

    assert response.status_code == 422


@pytest.mark.parametrize(
    "identifier",
    ["vacancy_id", "organization_id", "candidate_id", "user_id", "job_request_id"],
)
def test_identifiers_are_rejected(client: TestClient, payload, identifier: str) -> None:
    """El contrato de features es una frontera, no una recomendacion."""
    response = client.post("/v1/predict", json=dict(payload, **{identifier: 7}))

    assert response.status_code == 422
    assert identifier in response.text


@pytest.mark.parametrize(
    "attribute",
    ["candidate_name", "email", "edad", "gender", "selected_score", "ranking", "cv_text"],
)
def test_personal_and_outcome_attributes_are_rejected(
    client: TestClient, payload, attribute: str
) -> None:
    response = client.post("/v1/predict", json=dict(payload, **{attribute: "x"}))

    assert response.status_code == 422


def test_a_missing_field_is_rejected(client: TestClient, payload) -> None:
    incomplete = {k: v for k, v in payload.items() if k != "positions_count"}
    response = client.post("/v1/predict", json=incomplete)

    assert response.status_code == 422
    assert "positions_count" in response.text


def test_an_empty_payload_is_rejected(client: TestClient) -> None:
    assert client.post("/v1/predict", json={}).status_code == 422


@pytest.mark.parametrize("value", ["12", "doce", None, True, [1], {"a": 1}])
def test_a_wrong_type_is_rejected(client: TestClient, payload, value) -> None:
    """En modo estricto `"12"` no se convierte en 12: seria tapar un error."""
    response = client.post("/v1/predict", json=dict(payload, positions_count=value))

    assert response.status_code == 422


def test_a_decimal_count_is_rejected(client: TestClient, payload) -> None:
    """Las features son conteos enteros; 3.5 evaluaciones no existe."""
    response = client.post("/v1/predict", json=dict(payload, evaluations_scheduled_count=3.5))

    assert response.status_code == 422


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_nan_and_infinity_are_rejected(client: TestClient, payload, literal: str) -> None:
    """Sobreviven al JSON de Python; no sobreviven al contrato."""
    body = json.dumps(dict(payload, applications_received_count=0)).replace(
        '"applications_received_count": 0', f'"applications_received_count": {literal}'
    )
    response = client.post(
        "/v1/predict", content=body, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422


def test_a_negative_count_is_rejected(client: TestClient, payload) -> None:
    response = client.post("/v1/predict", json=dict(payload, applications_received_count=-1))

    assert response.status_code == 422


def test_a_non_positive_days_remaining_is_rejected(client: TestClient, payload) -> None:
    """El contrato sintetico exige plazo posterior al checkpoint."""
    response = client.post("/v1/predict", json=dict(payload, days_remaining_to_target=0))

    assert response.status_code == 422


def test_an_impossible_day_count_is_rejected(client: TestClient, payload) -> None:
    """Por encima del periodo maximo aprobado el valor no viene de este contrato."""
    response = client.post(
        "/v1/predict", json=dict(payload, elapsed_days_since_publication=10**6)
    )

    assert response.status_code == 422


def test_malformed_json_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/v1/predict", content="{ esto no es json", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422


# --- /v1/predict: modelo no disponible ------------------------------------


def test_predict_without_a_model_returns_503(client_without_model: TestClient, payload) -> None:
    response = client_without_model.post("/v1/predict", json=payload)

    assert response.status_code == 503
    body = response.json()
    assert body["error"] == "model_unavailable"
    assert "build_artifact" in body["detail"]


def test_the_unavailable_response_leaks_nothing(client_without_model: TestClient, payload) -> None:
    body = client_without_model.post("/v1/predict", json=payload).text

    for leak in ("Traceback", "site-packages", "File \\\"", "artifacts/"):
        assert leak not in body


def test_an_incompatible_artifact_keeps_the_service_unready(
    monkeypatch, tmp_path: Path, built_artifact, payload
) -> None:
    """Un artefacto que no corresponde al freeze no habilita el servicio."""
    directory, metadata, _ = built_artifact
    joblib.dump(joblib.load(artifact_path(directory)), artifact_path(tmp_path))
    corrupted = dict(metadata.to_dict(), freeze_fingerprint="0" * 64)
    corrupted.pop("threshold_display", None)
    ArtifactMetadata.from_dict(corrupted).write(metadata_path(tmp_path))
    monkeypatch.setenv(ARTIFACT_DIR_ENV, str(tmp_path))

    with TestClient(create_app()) as client:
        assert client.get("/health").json()["model_ready"] is False
        assert client.post("/v1/predict", json=payload).status_code == 503
        assert client.get("/v1/model-info").status_code == 503


def test_an_inference_failure_is_reported_without_a_trace(
    monkeypatch, client: TestClient, payload
) -> None:
    """Un fallo inesperado devuelve una categoria, nunca el detalle interno."""
    from recruitment_ml.serving.predictor import PredictionError, RiskPredictor

    def explode(self, features):  # noqa: ANN001, ARG001
        raise PredictionError("detalle interno que el cliente no debe ver")

    monkeypatch.setattr(RiskPredictor, "predict", explode)
    response = client.post("/v1/predict", json=payload)

    assert response.status_code == 500
    body = response.json()
    assert body["error"] == "inference_failed"
    assert "detalle interno" not in body["detail"]


# --- contrato y documentacion ---------------------------------------------


def test_the_request_schema_matches_the_feature_contract() -> None:
    from recruitment_ml.api.schemas import PredictionRequest, expected_feature_names

    assert set(PredictionRequest.model_fields) == set(expected_feature_names())


def test_openapi_documents_the_endpoints_with_a_fictional_example(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()

    assert set(schema["paths"]) == {"/health", "/v1/model-info", "/v1/predict"}
    example = schema["components"]["schemas"]["PredictionRequest"]["example"]
    assert set(example) == set(
        client.get("/v1/model-info").json()["feature_order"]
    )


def test_the_documentation_states_that_it_is_not_deployable(client: TestClient) -> None:
    description = client.get("/openapi.json").json()["info"]["description"]

    assert "EXPERIMENTAL" in description
    assert "GAP-01" in description
    assert "decision final es humana" in description


def test_no_cors_headers_are_emitted(client: TestClient, payload) -> None:
    """El consumidor sera Laravel por red interna, no un navegador."""
    response = client.post(
        "/v1/predict", json=payload, headers={"Origin": "http://ejemplo.invalido"}
    )

    assert "access-control-allow-origin" not in {k.lower() for k in response.headers}
