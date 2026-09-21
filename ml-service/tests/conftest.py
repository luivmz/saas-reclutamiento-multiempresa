"""Fixtures compartidas de la suite de la Fase 15A."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from recruitment_ml.config import SyntheticConfig
from recruitment_ml.synthetic.generator import SyntheticDataset, build_dataset
from recruitment_ml.synthetic.timeline import (
    OrganizationProfile,
    ProcessTimeline,
    resolve_closure,
    simulate_process,
)

#: Tamano de trabajo de la suite. Mas pequeno que el entregable academico
#: (6 000) para que las pruebas sean rapidas, y suficiente para que las
#: invariantes estadisticas sean estables.
TEST_ROWS = 2_500


@pytest.fixture(scope="session")
def config() -> SyntheticConfig:
    return SyntheticConfig(rows=TEST_ROWS)


@pytest.fixture(scope="session")
def dataset(config: SyntheticConfig) -> SyntheticDataset:
    """Dataset compartido: generarlo una vez por sesion basta."""
    return build_dataset(config)


@pytest.fixture(scope="session")
def frame(dataset: SyntheticDataset):
    return dataset.frame


@pytest.fixture(scope="session")
def model_ready(dataset: SyntheticDataset):
    return dataset.model_ready()


#: Tamano de los experimentos de la suite de 15B. Mas pequeno que el
#: entregable academico (6 000) para que las pruebas sean rapidas, y suficiente
#: para que las invariantes experimentales se sostengan.
TRAINING_ROWS = 2_000


@pytest.fixture(scope="session")
def training_dataset() -> SyntheticDataset:
    """Dataset de 15A que alimenta la suite de 15B, con su manifiesto."""
    return build_dataset(SyntheticConfig(rows=TRAINING_ROWS))


@pytest.fixture(scope="session")
def training_frame(training_dataset: SyntheticDataset):
    """Frame model-ready del generador de 15A, fuente unica para 15B."""
    return training_dataset.model_ready()


@pytest.fixture(scope="session")
def training_fingerprints(training_dataset: SyntheticDataset) -> dict[str, str]:
    """Huellas reales del dataset y de la configuracion que lo produjo.

    La particion ya no acepta huellas vacias, asi que las pruebas usan las del
    manifiesto: el enlace que se valida en produccion es el mismo que se ejercita
    en la suite.
    """
    return {
        "dataset_fingerprint": str(training_dataset.manifest["model_ready_fingerprint"]),
        "config_fingerprint": str(training_dataset.manifest["config_fingerprint"]),
    }


@pytest.fixture(scope="session")
def temporal_split(training_frame, training_fingerprints):
    from recruitment_ml.training.split import build_temporal_split

    return build_temporal_split(training_frame, **training_fingerprints)


@pytest.fixture(scope="session")
def experiment_result():
    """Experimento completo, ejecutado una sola vez por sesion."""
    from recruitment_ml.training.experiment import run_experiment

    return run_experiment(rows=TRAINING_ROWS, include_optional_model=False)


@pytest.fixture(scope="session")
def timelines(config: SyntheticConfig) -> list[ProcessTimeline]:
    """Cronologias completas, para verificar invariantes que no se exportan.

    El dataset no contiene `target_completion_at` ni `closed_at` porque estan
    prohibidos como columnas; las invariantes temporales solo pueden
    comprobarse sobre la simulacion.
    """
    from datetime import date

    rng = np.random.default_rng(config.seed)
    organization = OrganizationProfile(
        organization_id=1, capacity=1.0, volume_scale=1.0, friction_base=1.0
    )
    built: list[ProcessTimeline] = []
    for index in range(250):
        timeline = simulate_process(
            rng=rng,
            config=config,
            organization=organization,
            vacancy_id=index + 1,
            request_day=date(2024, 1 + index % 12, 1 + index % 27),
            period_effect=1.0 + 0.2 * (index % 7) / 6,
            workload_pressure=0.8 + 0.4 * (index % 5) / 4,
        )
        resolve_closure(rng, config, timeline)
        built.append(timeline)
    return built


# --- Fase 15C: artefacto servido y cliente de la API -----------------------
#
# El artefacto se construye **una vez por sesion** en un directorio temporal:
# reconstruirlo por prueba costaria minutos, y usar el de `artifacts/` haria
# que la suite dependiera de un paso manual previo.


@pytest.fixture(scope="session")
def freeze_path() -> Path:
    """Protocolo congelado de la Fase 15B, versionado en `docs/`."""
    from recruitment_ml.serving.paths import DEFAULT_FREEZE_PATH

    assert DEFAULT_FREEZE_PATH.is_file(), f"falta el freeze en {DEFAULT_FREEZE_PATH}"
    return DEFAULT_FREEZE_PATH


@pytest.fixture(scope="session")
def built_artifact(tmp_path_factory, freeze_path):
    """Artefacto reconstruido desde el freeze, con sus metadatos y el freeze."""
    from recruitment_ml.serving.build_artifact import build
    from recruitment_ml.training.freeze import load_freeze

    directory = tmp_path_factory.mktemp("model-artifact")
    metadata = build(freeze_path=freeze_path, output_dir=directory, rows=6_000)
    return directory, metadata, load_freeze(freeze_path)


@pytest.fixture(scope="session")
def sample_features() -> dict[str, float]:
    """Proceso ficticio, en un orden distinto del canonico a proposito."""
    from recruitment_ml.api.schemas import json_schema_example

    return {name: float(value) for name, value in json_schema_example().items()}
