"""Unit tests for the client-side helpers that are not tied to one mutation."""

from collections.abc import Hashable

from mikro_next.errors import MikroError, NoDataLayerFound, NoMikroFound, NotQueriedError
from mikro_next.utils import rechunk


def test_mikro_error_classes() -> None:
    """Every mikro error is catchable as a ``MikroError``."""
    base_error = MikroError("Base error message")
    assert str(base_error) == "Base error message", "Error message should be preserved"
    assert isinstance(base_error, Exception), "Should be an Exception"

    assert isinstance(NoMikroFound("No mikro instance found"), MikroError)
    assert isinstance(NoDataLayerFound("No data layer found"), MikroError)
    assert isinstance(NotQueriedError("Field not queried"), MikroError)


def test_rechunk_picks_chunks_for_a_large_stack() -> None:
    """Chunking is per-plane: a channel is never chunked together with another,
    and the spatial chunk is capped so one chunk stays a reasonable request."""
    sizes: dict[Hashable, int] = {"c": 3, "t": 10, "z": 20, "y": 1024, "x": 1024}
    chunks = rechunk(sizes)

    assert set(chunks) == set(sizes), "Every dimension should be assigned a chunk"
    assert chunks["x"] <= 2048, "X chunk should not exceed 2048"
    assert chunks["y"] <= 2048, "Y chunk should not exceed 2048"
    assert chunks["c"] == 1, "C chunk should be 1"


def test_rechunk_leaves_a_small_stack_alone() -> None:
    """Nothing is gained by splitting an array that is already one chunk."""
    small_sizes: dict[Hashable, int] = {"c": 1, "t": 1, "z": 1, "y": 100, "x": 100}
    assert rechunk(small_sizes) == small_sizes, "Small images should not be rechunked"
