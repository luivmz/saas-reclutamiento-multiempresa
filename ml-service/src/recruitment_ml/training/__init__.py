"""Entrenamiento y evaluacion cientifica (Fase 15B).

Contiene el experimento completo: particion temporal, preprocesamiento,
baselines, modelos, calibracion, seleccion de umbral, ablations y evaluacion
final sobre un conjunto de prueba sellado.

No contiene servicio HTTP, integracion con Laravel ni artefactos de despliegue:
eso pertenece a 15C y 16.
"""

from recruitment_ml.training.split import TemporalSplit, build_temporal_split

__all__ = ["TemporalSplit", "build_temporal_split"]
