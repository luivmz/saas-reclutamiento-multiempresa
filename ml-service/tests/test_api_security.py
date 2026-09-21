"""Autenticacion de servicio a servicio (Fase 16).

El servicio deja de estar solo: Laravel lo consume por red interna. Un token
compartido acota quien puede pedir predicciones, sin convertir al servicio en
algo publicable.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from recruitment_ml.api.app import create_app
from recruitment_ml.api.security import (
    MISCONFIGURED_MESSAGE,
    TOKEN_ENV,
    TOKEN_HEADER,
    authentication_enabled,
    configured_token,
)
from recruitment_ml.serving.paths import ARTIFACT_DIR_ENV

TOKEN = "token-ficticio-de-pruebas"


@pytest.fixture
def payload(sample_features) -> dict[str, int]:
    return {name: int(value) for name, value in sample_features.items()}


@pytest.fixture
def protected_client(monkeypatch, built_artifact) -> TestClient:
    """Servicio con modelo cargado y autenticacion activa."""
    directory, _, _ = built_artifact
    monkeypatch.setenv(ARTIFACT_DIR_ENV, str(directory))
    monkeypatch.setenv(TOKEN_ENV, TOKEN)
    with TestClient(create_app()) as client:
        yield client


@pytest.fixture
def unconfigured_client(monkeypatch, built_artifact) -> TestClient:
    """Servicio con modelo cargado pero SIN token configurado."""
    directory, _, _ = built_artifact
    monkeypatch.setenv(ARTIFACT_DIR_ENV, str(directory))
    monkeypatch.delenv(TOKEN_ENV, raising=False)
    with TestClient(create_app()) as client:
        yield client


# --- configuracion ---------------------------------------------------------


def test_the_token_comes_only_from_the_environment(monkeypatch) -> None:
    monkeypatch.delenv(TOKEN_ENV, raising=False)
    assert configured_token() is None
    assert authentication_enabled() is False

    monkeypatch.setenv(TOKEN_ENV, TOKEN)
    assert configured_token() == TOKEN
    assert authentication_enabled() is True


@pytest.mark.parametrize("blank", ["", "   "])
def test_a_blank_token_disables_authentication(monkeypatch, blank: str) -> None:
    """Una variable vacia no es un token: seria uno trivial de adivinar."""
    monkeypatch.setenv(TOKEN_ENV, blank)

    assert configured_token() is None
    assert authentication_enabled() is False


@pytest.mark.parametrize("value", ["abc", "otro-token", "  con-espacios  "])
def test_the_token_is_exactly_what_the_environment_says(monkeypatch, value: str) -> None:
    """Sin valor por defecto oculto: lo que vale es el entorno y nada mas."""
    monkeypatch.setenv(TOKEN_ENV, value)

    assert configured_token() == value.strip()


def test_the_module_reads_the_token_from_the_environment() -> None:
    """Un valor por defecto en el codigo seria un secreto versionado."""
    source = Path("src/recruitment_ml/api/security.py").read_text(encoding="utf-8")

    assert 'os.environ.get(TOKEN_ENV, "")' in source
    assert "hmac.compare_digest" in source


# --- rutas protegidas ------------------------------------------------------


def test_predict_requires_the_token(protected_client: TestClient, payload) -> None:
    response = protected_client.post("/v1/predict", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Credencial de servicio ausente o invalida."


def test_model_info_requires_the_token(protected_client: TestClient) -> None:
    assert protected_client.get("/v1/model-info").status_code == 401


@pytest.mark.parametrize(
    "wrong",
    ["otro-token", TOKEN + "x", TOKEN[:-1], TOKEN.upper(), ""],
)
def test_a_wrong_token_is_rejected(protected_client: TestClient, payload, wrong: str) -> None:
    response = protected_client.post(
        "/v1/predict", json=payload, headers={TOKEN_HEADER: wrong}
    )

    assert response.status_code == 401


def test_the_correct_token_is_accepted(protected_client: TestClient, payload) -> None:
    response = protected_client.post(
        "/v1/predict", json=payload, headers={TOKEN_HEADER: TOKEN}
    )

    assert response.status_code == 200
    assert 0.0 <= response.json()["risk_score"] <= 1.0


def test_model_info_with_the_token_is_accepted(protected_client: TestClient) -> None:
    response = protected_client.get("/v1/model-info", headers={TOKEN_HEADER: TOKEN})

    assert response.status_code == 200
    assert response.json()["deployment_status"] == "experimental"


def test_the_rejection_does_not_echo_the_token(protected_client: TestClient, payload) -> None:
    """Ni el enviado ni el esperado pueden aparecer en la respuesta."""
    response = protected_client.post(
        "/v1/predict", json=payload, headers={TOKEN_HEADER: "intento-de-token"}
    )

    assert TOKEN not in response.text
    assert "intento-de-token" not in response.text


# --- health se mantiene abierto -------------------------------------------


def test_health_stays_open(protected_client: TestClient) -> None:
    """Es una sonda de vida: sin token, y sin nada que proteger.

    Devuelve estado del proceso, si hay modelo y la version del componente. Ni
    rutas, ni huellas, ni versiones de bibliotecas, ni nada del experimento.
    """
    response = protected_client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"status", "model_ready", "version", "detail"}
    assert body["model_ready"] is True


# --- sin token configurado: falla cerrado ---------------------------------
#
# Olvidar la variable en un despliegue no puede dejar `/v1/*` accesible a quien
# llegue. El servicio se cierra y lo dice; el modelo no responde hasta que haya
# credencial.


def test_without_a_configured_token_the_model_routes_are_closed(
    unconfigured_client: TestClient, payload
) -> None:
    for response in (
        unconfigured_client.post("/v1/predict", json=payload),
        unconfigured_client.get("/v1/model-info"),
    ):
        assert response.status_code == 503
        assert response.json()["detail"] == MISCONFIGURED_MESSAGE


def test_a_token_in_the_header_does_not_open_an_unconfigured_service(
    unconfigured_client: TestClient, payload
) -> None:
    """Enviar una cabecera no suple la configuracion que falta."""
    response = unconfigured_client.post(
        "/v1/predict", json=payload, headers={TOKEN_HEADER: "cualquier-cosa"}
    )

    assert response.status_code == 503


def test_the_closed_response_reveals_no_configuration_detail(
    unconfigured_client: TestClient, payload
) -> None:
    body = unconfigured_client.post("/v1/predict", json=payload).text

    for leak in (TOKEN_ENV, "Traceback", "site-packages", "artifacts"):
        assert leak not in body


def test_health_still_answers_without_a_configured_token(
    unconfigured_client: TestClient,
) -> None:
    """La sonda de vida sigue util aunque el modelo no atienda."""
    response = unconfigured_client.get("/health")

    assert response.status_code == 200
    assert response.json()["model_ready"] is True


def test_a_blank_token_also_closes_the_service(monkeypatch, built_artifact, payload) -> None:
    directory, _, _ = built_artifact
    monkeypatch.setenv(ARTIFACT_DIR_ENV, str(directory))
    monkeypatch.setenv(TOKEN_ENV, "   ")

    with TestClient(create_app()) as client:
        assert client.post("/v1/predict", json=payload).status_code == 503


# --- documentacion ---------------------------------------------------------


def test_openapi_documents_the_protected_routes(protected_client: TestClient) -> None:
    schema = protected_client.get("/openapi.json").json()

    assert "401" in schema["paths"]["/v1/predict"]["post"]["responses"]
    assert "401" in schema["paths"]["/v1/model-info"]["get"]["responses"]
    assert "401" not in schema["paths"]["/health"]["get"]["responses"]
