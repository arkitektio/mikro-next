"""Unit tests for the CreateADatasetTrait axis validation."""

import numpy as np
import pytest
import xarray as xr
from pydantic import ValidationError

from mikro_next.api.schema import (
    AxisInput,
    CreateADatasetInput,
    ScaleInput,
)


def _data(dims: list[str]) -> xr.DataArray:
    return xr.DataArray(np.zeros((2,) * len(dims), dtype="uint16"), dims=dims)


def _axes(names: list[str]) -> list[AxisInput]:
    return [AxisInput(name=name, type="SPACE") for name in names]


def test_matching_axes_validate() -> None:
    """Axes that cover exactly the array's dims are accepted."""
    model = CreateADatasetInput(
        data=_data(["z", "y", "x", "c"]),
        scales=(),
        name="ds",
        axes=_axes(["z", "y", "x", "c"]),
    )
    assert model.data.value.dims == ("z", "y", "x", "c")


def test_axis_order_is_irrelevant() -> None:
    """Only the set of axis names must match, not their order."""
    CreateADatasetInput(
        data=_data(["z", "y", "x", "c"]),
        scales=(),
        name="ds",
        axes=_axes(["c", "x", "y", "z"]),
    )


def test_missing_axis_raises() -> None:
    """A data dim with no matching axis is rejected."""
    with pytest.raises(ValidationError):
        CreateADatasetInput(
            data=_data(["z", "y", "x", "c"]),
            scales=(),
            name="ds",
            axes=_axes(["z", "y", "x"]),
        )


def test_extra_axis_raises() -> None:
    """An axis that does not correspond to any data dim is rejected."""
    with pytest.raises(ValidationError):
        CreateADatasetInput(
            data=_data(["z", "y", "x"]),
            scales=(),
            name="ds",
            axes=_axes(["z", "y", "x", "c"]),
        )


def test_scale_dims_must_match() -> None:
    """A scale array whose dims differ from the data dims is rejected."""
    with pytest.raises(ValidationError):
        CreateADatasetInput(
            data=_data(["z", "y", "x"]),
            scales=(ScaleInput(level=0, array=_data(["z", "y", "c"])),),
            name="ds",
            axes=_axes(["z", "y", "x"]),
        )
