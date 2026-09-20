"""Particion temporal 70/15/15.

Un split aleatorio entrenaria con el futuro y evaluaria con el pasado. Estas
pruebas verifican la garantia experimental, no que el codigo se ejecute.
"""

from __future__ import annotations

import pandas as pd
import pytest

from recruitment_ml.schema import STATUS_CENSORED, TARGET_COLUMN
from recruitment_ml.training.split import (
    TRAIN_RATIO,
    VALIDATION_RATIO,
    build_temporal_split,
)


def test_partitions_respect_the_approved_ratios(temporal_split, training_frame) -> None:
    total = len(training_frame[training_frame[TARGET_COLUMN].notna()])
    assert len(temporal_split.train) == pytest.approx(total * TRAIN_RATIO, abs=2)
    assert len(temporal_split.validation) == pytest.approx(total * VALIDATION_RATIO, abs=2)
    assert len(temporal_split.sealed_test) == pytest.approx(total * 0.15, abs=3)


def test_train_precedes_validation_precedes_test(temporal_split) -> None:
    boundaries = temporal_split.boundaries
    train_last = pd.Timestamp(boundaries["train_last_checkpoint"])
    validation_first = pd.Timestamp(boundaries["validation_first_checkpoint"])
    validation_last = pd.Timestamp(boundaries["validation_last_checkpoint"])
    test_first = pd.Timestamp(boundaries["test_first_checkpoint"])

    assert train_last <= validation_first
    assert validation_last <= test_first


def test_no_process_appears_in_two_partitions(temporal_split) -> None:
    """La unidad es la vacante: no puede estar en dos conjuntos a la vez.

    Se auditan los identificadores, que son metadatos de linaje, sin tocar
    ninguna etiqueta del conjunto sellado.
    """
    train_ids = set(temporal_split.train["vacancy_id"])
    validation_ids = set(temporal_split.validation["vacancy_id"])
    test_ids = set(temporal_split.sealed_test.identifiers())

    assert not train_ids & validation_ids
    assert not train_ids & test_ids
    assert not validation_ids & test_ids


def test_every_labelled_row_lands_in_exactly_one_partition(temporal_split, training_frame) -> None:
    labelled = training_frame[training_frame[TARGET_COLUMN].notna()]
    total = (
        len(temporal_split.train)
        + len(temporal_split.validation)
        + len(temporal_split.sealed_test)
    )
    assert total == len(labelled)


def test_censored_processes_never_enter_the_split(training_frame) -> None:
    """Los censurados no reciben etiqueta y no forman parte del supervisado."""
    split = build_temporal_split(training_frame.copy())

    for partition in (split.train, split.validation):
        assert (partition["observation_status"] != STATUS_CENSORED).all()
        assert partition[TARGET_COLUMN].notna().all()

    # El conjunto sellado se audita por conteo: las tres particiones suman
    # exactamente las filas etiquetadas, así que ninguna censurada entró.
    labelled = training_frame[training_frame[TARGET_COLUMN].notna()]
    assert len(split.train) + len(split.validation) + len(split.sealed_test) == len(labelled)


def test_split_is_deterministic(training_frame) -> None:
    first = build_temporal_split(training_frame)
    second = build_temporal_split(training_frame)

    pd.testing.assert_frame_equal(first.train, second.train)
    pd.testing.assert_frame_equal(first.validation, second.validation)


def test_ordering_is_by_checkpoint_with_a_deterministic_tie_break(temporal_split) -> None:
    for partition in (temporal_split.train, temporal_split.validation):
        checkpoints = pd.to_datetime(partition["checkpoint_at"], utc=True)
        assert checkpoints.is_monotonic_increasing
    assert "vacancy_id" in temporal_split.summary()["ordering"]


def test_summary_reports_what_the_documentation_needs(temporal_split) -> None:
    summary = temporal_split.summary()
    for name in ("train", "validation", "test"):
        entry = summary[name]
        assert entry["n"] > 0
        assert entry["organizations"] >= 1
        assert entry["start"] <= entry["end"]

    for name in ("train", "validation"):
        assert 0.0 < summary[name]["prevalence"] < 1.0


def test_test_labels_are_not_disclosed_before_the_reveal(temporal_split) -> None:
    """Documentar tamaño y periodo es legítimo; conocer la prevalencia, no."""
    description = temporal_split.sealed_test.describe()

    assert description["labels_disclosed"] is False
    assert "prevalence" not in description
    assert "positives" not in description
    assert "note" in description


def test_boundary_note_does_not_claim_strict_inequality(temporal_split) -> None:
    """Los empates de timestamp se resuelven por vacancy_id, no desaparecen."""
    summary = temporal_split.summary()

    assert "vacancy_id" in summary["ordering"]
    assert "no se afirma desigualdad estricta" in summary["ordering"]
    assert "boundary_note" in summary["boundaries"]


def test_reveal_count_is_scoped_to_the_current_run(temporal_split) -> None:
    summary = temporal_split.summary()

    assert summary["test_reveal_count"] == temporal_split.sealed_test.reveal_count
    assert "no es un registro historico" in summary["test_reveal_count_scope"]


def test_an_unlabelled_frame_is_rejected(training_frame) -> None:
    empty = training_frame.iloc[0:0]
    with pytest.raises(ValueError):
        build_temporal_split(empty)
