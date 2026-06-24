"""Integration tests for the generic ``create_a_dataset`` (ArrayLike) path.

Mirrors ``test_image.py`` but exercises arbitrarily-labelled arrays, multiscale
pyramids, dimension descriptors and coordinate anchors, end-to-end against a
deployed Mikro instance.
"""

from typing import List

import numpy as np
import pytest
import xarray as xr

from mikro_next.api.schema import (
    CoordinateAnchorInput,
    DimAnchorInput,
    DimensionDescriptorInput,
    ScaleInput,
    ValueHistogramInput,
    create_a_dataset,
)

from .conftest import DeployedMikro


def _make_volume() -> xr.DataArray:
    """A small labelled (z, y, x, c) volume suitable for fast uploads."""
    return xr.DataArray(
        np.random.random((4, 64, 64, 2)).astype("float32"),
        dims=["z", "y", "x", "c"],
    )


def _descriptors() -> List[DimensionDescriptorInput]:
    return [
        DimensionDescriptorInput(key="z", kind="space"),
        DimensionDescriptorInput(key="y", kind="space"),
        DimensionDescriptorInput(key="x", kind="space"),
        DimensionDescriptorInput(key="c", kind="channel"),
    ]


def _pyramid(base: xr.DataArray, levels: int = 3) -> List[xr.DataArray]:
    """Downsample the spatial dims (z, y, x) by 2 per level, keeping all dims."""
    arrays = [base]
    for _ in range(levels - 1):
        current = arrays[-1]
        coarsen_dims = {dim: 2 for dim in ["z", "y", "x"] if current.sizes[dim] >= 2}
        if not coarsen_dims:
            break
        downscaled = current.coarsen(boundary="trim", **coarsen_dims).mean().astype(base.dtype)
        arrays.append(downscaled)
    return arrays


def _histogram(values: np.ndarray, bins: int = 32) -> ValueHistogramInput:
    counts, edges = np.histogram(values, bins=bins)
    p1, p99 = np.percentile(values, [1, 99])
    return ValueHistogramInput(
        histogram=counts.tolist(),
        bins=edges.tolist(),
        min=float(values.min()),
        max=float(values.max()),
        p1=float(p1),
        p99=float(p99),
    )


@pytest.mark.integration
def test_create_a_dataset(deployed_app: DeployedMikro) -> None:
    """Create a dataset from a single arbitrarily-labelled array."""
    data = _make_volume()
    dataset = create_a_dataset(
        data=data,
        scales=[ScaleInput(level=0, array=data, scale_factors=[1, 1, 1, 1])],
        name="adataset_basic",
        dim_descriptors=_descriptors(),
    )
    assert dataset.id, "Dataset should have an ID"
    assert dataset.name == "adataset_basic"
    # The arbitrary labels must round-trip rather than being coerced to ctzyx.
    assert set(dataset.dims) == {"z", "y", "x", "c"}


@pytest.mark.integration
def test_create_a_dataset_with_pyramid(deployed_app: DeployedMikro) -> None:
    """Create a dataset with a multiscale pyramid of scale arrays."""
    data = _make_volume()
    pyramid = _pyramid(data, levels=3)
    scales = [
        ScaleInput(
            level=i,
            array=arr,
            scale_method="nearest" if i > 0 else None,
            scale_factors=[2**i, 2**i, 2**i, 1],
        )
        for i, arr in enumerate(pyramid)
    ]

    dataset = create_a_dataset(
        data=data,
        scales=scales,
        name="adataset_pyramid",
        dim_descriptors=_descriptors(),
    )
    assert dataset.id
    assert len(dataset.data_arrays) == len(pyramid + [data]), "All pyramid levels should be stored"
    assert {arr.level for arr in dataset.data_arrays} == set(range(len(pyramid))), (
        "Pyramid levels should be correctly labeled"
    )


@pytest.mark.integration
def test_create_a_dataset_with_anchors(deployed_app: DeployedMikro) -> None:
    """Create a dataset with per-channel coordinate anchors and histograms."""
    data = _make_volume()
    anchors = [
        CoordinateAnchorInput(
            dimAnchors=(DimAnchorInput(dim="c", value=c),),
            valueHistogram=_histogram(data.isel(c=c).to_numpy()),
        )
        for c in range(data.sizes["c"])
    ]

    dataset = create_a_dataset(
        data=data,
        scales=[ScaleInput(level=0, array=data, scale_factors=[1, 1, 1, 1])],
        name="adataset_anchored",
        dim_descriptors=_descriptors(),
        anchors=anchors,
    )
    assert dataset.id
    assert dataset.name == "adataset_anchored"


@pytest.mark.integration
def test_create_a_dataset_rejects_mismatched_descriptors(
    deployed_app: DeployedMikro,
) -> None:
    """The model-level trait rejects descriptors that don't cover the data dims."""
    data = _make_volume()
    with pytest.raises(Exception):
        create_a_dataset(
            data=data,
            scales=[ScaleInput(level=0, array=data, scale_factors=[1, 1, 1, 1])],
            name="adataset_bad",
            # Missing the "c" descriptor -> should fail before any upload.
            dim_descriptors=[
                DimensionDescriptorInput(key="z", kind="space"),
                DimensionDescriptorInput(key="y", kind="space"),
                DimensionDescriptorInput(key="x", kind="space"),
            ],
        )
