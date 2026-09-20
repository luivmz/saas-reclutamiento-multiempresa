"""Fixtures compartidas de la suite de la Fase 15A."""

from __future__ import annotations

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
