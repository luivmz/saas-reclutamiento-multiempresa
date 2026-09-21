"""Familias de distribucion usadas por el generador.

Cada funcion envuelve un sorteo de numpy con un nombre del dominio y la razon
por la que esa familia es apropiada. No hay uniformes disfrazadas: los tiempos
son positivos y asimetricos, los conteos tienen sobredispersion y los shocks
son raros pero grandes.

Ninguna de estas distribuciones describe al Colegio Andino de Huancayo. Son
supuestos sinteticos academicos.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "lognormal_days",
    "gamma_days",
    "negative_binomial_count",
    "truncated_poisson_count",
    "bounded_choice",
    "bernoulli",
    "rare_shock",
    "centered_effect",
]


def lognormal_days(rng: np.random.Generator, median: float, sigma: float, minimum: int = 0) -> int:
    """Duracion positiva y asimetrica a la derecha.

    La lognormal reproduce el patron habitual de un proceso operativo: la
    mayoria termina cerca de la mediana y una cola pequena tarda mucho mas.
    """
    value = float(rng.lognormal(mean=np.log(max(median, 1e-6)), sigma=sigma))
    return max(minimum, int(round(value)))


def gamma_days(rng: np.random.Generator, shape: float, scale: float, minimum: int = 0) -> int:
    """Duracion positiva con cola controlada por `shape`.

    Se usa cuando interesa una masa central mas compacta que la lognormal, por
    ejemplo la ventana de postulaciones.
    """
    value = float(rng.gamma(shape=shape, scale=scale))
    return max(minimum, int(round(value)))


def negative_binomial_count(rng: np.random.Generator, mean: float, dispersion: float) -> int:
    """Conteo con sobredispersion.

    Poisson subestimaria la varianza del volumen de postulaciones: hay
    convocatorias desiertas y convocatorias desbordadas. `dispersion` es el
    parametro de forma; valores bajos producen mas varianza.
    """
    mean = max(mean, 1e-6)
    dispersion = max(dispersion, 1e-6)
    probability = dispersion / (dispersion + mean)
    return int(rng.negative_binomial(dispersion, probability))


def truncated_poisson_count(rng: np.random.Generator, mean: float, maximum: int) -> int:
    """Conteo pequeno con techo operacional."""
    return int(min(maximum, rng.poisson(max(mean, 0.0))))


def bounded_choice(rng: np.random.Generator, values: tuple[int, ...], weights: tuple[float, ...]) -> int:
    """Sorteo discreto sobre un rango acotado, como el numero de plazas."""
    probabilities = np.asarray(weights, dtype=float)
    probabilities = probabilities / probabilities.sum()
    return int(rng.choice(np.asarray(values, dtype=int), p=probabilities))


def bernoulli(rng: np.random.Generator, probability: float) -> bool:
    """Evento binario. Solo donde el fenomeno es naturalmente binario."""
    return bool(rng.random() < min(max(probability, 0.0), 1.0))


def rare_shock(rng: np.random.Generator, probability: float, magnitude: float) -> float:
    """Multiplicador raro pero grande.

    Modela una interrupcion excepcional del proceso: ausencia prolongada,
    reprogramacion masiva o periodo de matricula. Devuelve 1.0 casi siempre.
    """
    if not bernoulli(rng, probability):
        return 1.0
    return 1.0 + float(rng.gamma(shape=2.0, scale=magnitude / 2.0))


def centered_effect(rng: np.random.Generator, sigma: float) -> float:
    """Efecto aleatorio multiplicativo de media aproximada 1.

    Se usa para heterogeneidad por organizacion y por periodo: desplaza sin
    determinar.
    """
    return float(np.exp(rng.normal(loc=0.0, scale=sigma)))
