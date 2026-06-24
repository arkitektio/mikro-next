"""Unit tests for the CreateADatasetTrait dim-descriptor validation."""

import numpy as np
import pytest
import xarray as xr
from pydantic import ValidationError

from mikro_next.api.schema import (
    CreateADatasetInput,
    DimensionDescriptorInput,
    ScaleInput,
)


def _data(dims: list[str]) -> xr.DataArray:
    return xr.DataArray(np.zeros((2,) * len(dims), dtype="uint16"), dims=dims)


def _descriptors(keys: list[str]) -> list[DimensionDescriptorInput]:
    return [DimensionDescriptorInput(key=k, kind="space") for k in keys]


def test_matching_descriptors_validate() -> None:
    """Descriptors that cover exactly the array's dims are accepted."""
    model = CreateADatasetInput(
        data=_data(["z", "y", "x", "c"]),
        scales=(),
        name="ds",
        dimDescriptors=_descriptors(["z", "y", "x", "c"]),
    )
    assert model.data.value.dims == ("z", "y", "x", "c")


def test_descriptor_order_is_irrelevant() -> None:
    """Only the set of dim keys must match, not their order."""
    CreateADatasetInput(
        data=_data(["z", "y", "x", "c"]),
        scales=(),
        name="ds",
        dimDescriptors=_descriptors(["c", "x", "y", "z"]),
    )


def test_missing_descriptor_raises() -> None:
    """A data dim with no matching descriptor is rejected."""
    with pytest.raises(ValidationError):
        CreateADatasetInput(
            data=_data(["z", "y", "x", "c"]),
            scales=(),
            name="ds",
            dimDescriptors=_descriptors(["z", "y", "x"]),
        )


def test_extra_descriptor_raises() -> None:
    """A descriptor that does not correspond to any data dim is rejected."""
    with pytest.raises(ValidationError):
        CreateADatasetInput(
            data=_data(["z", "y", "x"]),
            scales=(),
            name="ds",
            dimDescriptors=_descriptors(["z", "y", "x", "c"]),
        )


def test_scale_dims_must_match() -> None:
    """A scale array whose dims differ from the data dims is rejected."""
    with pytest.raises(ValidationError):
        CreateADatasetInput(
            data=_data(["z", "y", "x"]),
            scales=(ScaleInput(level=0, array=_data(["z", "y", "c"])),),
            name="ds",
            dimDescriptors=_descriptors(["z", "y", "x"]),
        )
