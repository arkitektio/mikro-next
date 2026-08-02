"""Integration tests for the generic ``create_a_dataset`` (ArrayLike) path.

Mirrors ``test_image.py`` but exercises arbitrarily-*named* axes, multiscale
pyramids and coordinate anchors, end-to-end against a deployed Mikro instance.
Axis order is not arbitrary: the server requires axes sorted by type -- time,
then channel and custom types, then space -- and the array's dimension order is
that order.
"""

from typing import List

import numpy as np
import pytest
import xarray as xr

from mikro_next.api.schema import (
    AxisAnchorInput,
    AxisInput,
    CoordinateAnchorInput,
    ScaleInput,
    ValueHistogramInput,
    create_a_dataset,
)

from .conftest import DeployedMikro


def _make_volume() -> xr.DataArray:
    """A small labelled (c, z, y, x) volume suitable for fast uploads.

    The server requires axes ordered by type -- time, then channel and custom
    types, then space -- and the array's dimension order *is* that order, so the
    channel axis leads.
    """
    return xr.DataArray(
        np.random.random((2, 4, 64, 64)).astype("float32"),
        dims=["c", "z", "y", "x"],
    )


def _axes() -> List[AxisInput]:
    return [
        AxisInput(name="c", type="CHANNEL"),
        AxisInput(name="z", type="SPACE"),
        AxisInput(name="y", type="SPACE"),
        AxisInput(name="x", type="SPACE"),
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
        # ``data`` *is* level 0; listing it in ``scales`` too would upload it
        # twice, which the server rejects (one_data_array_per_level).
        scales=[],
        name="adataset_basic",
        axes=_axes(),
    )
    assert dataset.id, "Dataset should have an ID"
    assert dataset.name == "adataset_basic"
    # The axis names come back as given rather than being renamed into a fixed
    # t/c/z/y/x vocabulary. Their *order* is no longer free -- the server
    # requires axes sorted by type -- so only the names are asserted here.
    assert set(dataset.axis_names) == {"z", "y", "x", "c"}


@pytest.mark.integration
def test_create_a_dataset_with_pyramid(deployed_app: DeployedMikro) -> None:
    """Create a dataset with a multiscale pyramid of scale arrays."""
    data = _make_volume()
    pyramid = _pyramid(data, levels=3)
    # ``pyramid[0]`` is ``data`` itself, which travels as level 0 via ``data=``;
    # ``scales`` carries only the coarser levels, numbered from 1.
    scales = [
        ScaleInput(level=i, array=arr, scaleMethod="nearest")
        for i, arr in enumerate(pyramid[1:], start=1)
    ]

    dataset = create_a_dataset(
        data=data,
        scales=scales,
        name="adataset_pyramid",
        axes=_axes(),
    )
    assert dataset.id
    assert len(dataset.data_arrays) == len(pyramid), "All pyramid levels should be stored"
    assert {arr.level for arr in dataset.data_arrays} == set(range(len(pyramid))), (
        "Pyramid levels should be correctly labeled"
    )


@pytest.mark.integration
def test_create_a_dataset_with_anchors(deployed_app: DeployedMikro) -> None:
    """Create a dataset with per-channel coordinate anchors and histograms."""
    data = _make_volume()
    anchors = [
        CoordinateAnchorInput(
            axisAnchors=(AxisAnchorInput(axis="c", value=c),),
            valueHistogram=_histogram(data.isel(c=c).to_numpy()),
        )
        for c in range(data.sizes["c"])
    ]

    dataset = create_a_dataset(
        data=data,
        # ``data`` *is* level 0; listing it in ``scales`` too would upload it
        # twice, which the server rejects (one_data_array_per_level).
        scales=[],
        name="adataset_anchored",
        axes=_axes(),
        anchors=anchors,
    )
    assert dataset.id
    assert dataset.name == "adataset_anchored"


@pytest.mark.integration
def test_create_a_dataset_rejects_mismatched_axes(
    deployed_app: DeployedMikro,
) -> None:
    """The model-level trait rejects axes that don't cover the data dims."""
    data = _make_volume()
    with pytest.raises(Exception):
        create_a_dataset(
            data=data,
            scales=[],
            name="adataset_bad",
            # Missing the "c" axis -> should fail before any upload.
            axes=[
                AxisInput(name="z", type="SPACE"),
                AxisInput(name="y", type="SPACE"),
                AxisInput(name="x", type="SPACE"),
            ],
        )
