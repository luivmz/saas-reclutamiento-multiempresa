"""Componente Python del experimento academico de riesgo operacional.

Fase 15A: solo generacion de datos sinteticos. No contiene entrenamiento de
modelos, API HTTP ni integracion con Laravel.
"""

from recruitment_ml.config import DATASET_VERSION, DEFAULT_SEED, SyntheticConfig

__all__ = ["SyntheticConfig", "DEFAULT_SEED", "DATASET_VERSION"]
__version__ = "0.1.0"
