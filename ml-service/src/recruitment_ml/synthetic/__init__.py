"""Generacion sintetica event-first del dataset academico.

La reexportacion es perezosa a proposito: importar `generator` aqui de forma
temprana haria que `python -m recruitment_ml.synthetic.generator` cargase el
modulo dos veces y emitiese un RuntimeWarning de runpy.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - solo para analisis estatico
    from recruitment_ml.synthetic.generator import SyntheticDataset, build_dataset

__all__ = ["build_dataset", "SyntheticDataset"]


def __getattr__(name: str) -> Any:
    if name in __all__:
        from recruitment_ml.synthetic import generator

        return getattr(generator, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
