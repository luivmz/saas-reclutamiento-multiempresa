"""Rutas del artefacto local y del freeze versionado.

El artefacto **no se versiona**: se reconstruye con
`python -m recruitment_ml.serving.build_artifact`. El freeze si esta en el
repositorio, y es la referencia contra la que se valida todo lo demas.
"""

from __future__ import annotations

import os
from pathlib import Path

#: Raiz del componente Python (`ml-service/`).
ML_SERVICE_ROOT = Path(__file__).resolve().parents[3]

#: Directorio ignorado por Git donde vive el artefacto reconstruido.
DEFAULT_ARTIFACT_DIR = ML_SERVICE_ROOT / "artifacts" / "model"

#: Protocolo congelado de la Fase 15B, versionado en `docs/`.
DEFAULT_FREEZE_PATH = (
    ML_SERVICE_ROOT.parent / "docs" / "v1.1" / "ml" / "phase-15b-experiment-freeze.json"
)

ARTIFACT_FILENAME = "risk_model.joblib"
METADATA_FILENAME = "risk_model.metadata.json"

#: Variable de entorno para apuntar a otro directorio de artefacto, util en
#: pruebas y en un contenedor. No acepta secretos ni credenciales.
ARTIFACT_DIR_ENV = "RECRUITMENT_ML_ARTIFACT_DIR"


def artifact_dir() -> Path:
    """Directorio efectivo del artefacto."""
    override = os.environ.get(ARTIFACT_DIR_ENV)
    return Path(override) if override else DEFAULT_ARTIFACT_DIR


def artifact_path(directory: Path | None = None) -> Path:
    return (directory or artifact_dir()) / ARTIFACT_FILENAME


def metadata_path(directory: Path | None = None) -> Path:
    return (directory or artifact_dir()) / METADATA_FILENAME
