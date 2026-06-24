import numpy as np
import pytest
import xarray as xr
from mikro_next.api.schema import (
    RoiKind,
    create_roi,
    delete_roi,
    update_roi,
    get_roi,
    get_rois,
    from_array_like,
)
from mikro_next.scalars import FiveDVector
from .conftest import DeployedMikro


def _make_image() -> xr.DataArray:
    return xr.DataArray(np.random.random((100, 100, 5)), dims=["x", "y", "z"])


def _pt(x: float, y: float, z: float = 0, t: float = 0, c: float = 0) -> FiveDVector:
    return FiveDVector.from_params(c=int(c), t=int(t), z=int(z), x=x, y=y)


@pytest.mark.integration
def test_create_point_roi(deployed_app: DeployedMikro) -> None:
    """Create a point ROI on an image and verify it is stored."""
    image = from_array_like(_make_image(), name="roi_test_image")
    roi = create_roi(
        image=image.id,
        vectors=[_pt(10, 20)],
        kind=RoiKind.POINT,
    )
    assert roi.id, "ROI should have an ID"
    assert roi.kind == RoiKind.POINT


@pytest.mark.integration
def test_create_rectangle_roi(deployed_app: DeployedMikro) -> None:
    """Create a rectangle ROI defined by two corner points."""
    image = from_array_like(_make_image(), name="roi_rect_image")
    roi = create_roi(
        image=image.id,
        vectors=[_pt(0, 0), _pt(50, 50)],
        kind=RoiKind.RECTANGLE,
    )
    assert roi.id
    assert roi.kind == RoiKind.RECTANGLE
    assert len(roi.vectors) == 2


@pytest.mark.integration
def test_create_polygon_roi(deployed_app: DeployedMikro) -> None:
    """Create a polygon ROI with multiple vertices."""
    image = from_array_like(_make_image(), name="roi_polygon_image")
    roi = create_roi(
        image=image.id,
        vectors=[_pt(10, 10), _pt(40, 10), _pt(40, 40), _pt(10, 40)],
        kind=RoiKind.POLYGON,
    )
    assert roi.id
    assert roi.kind == RoiKind.POLYGON
    assert len(roi.vectors) == 4


@pytest.mark.integration
def test_get_roi(deployed_app: DeployedMikro) -> None:
    """Retrieve a ROI by ID and verify its fields."""
    image = from_array_like(_make_image(), name="roi_get_image")
    created = create_roi(
        image=image.id,
        vectors=[_pt(5, 5)],
        kind=RoiKind.POINT,
    )
    fetched = get_roi(id=created.id)
    assert fetched.id == created.id
    assert fetched.kind == RoiKind.POINT


@pytest.mark.integration
def test_get_rois_for_image(deployed_app: DeployedMikro) -> None:
    """List all ROIs for an image."""
    image = from_array_like(_make_image(), name="roi_list_image")
    create_roi(image=image.id, vectors=[_pt(1, 1)], kind=RoiKind.POINT)
    create_roi(image=image.id, vectors=[_pt(0, 0), _pt(30, 30)], kind=RoiKind.RECTANGLE)
    rois = get_rois(image=image.id)
    assert len(rois) >= 2


@pytest.mark.integration
def test_update_roi_vectors(deployed_app: DeployedMikro) -> None:
    """Update the vectors of an existing ROI."""
    image = from_array_like(_make_image(), name="roi_update_image")
    roi = create_roi(
        image=image.id,
        vectors=[_pt(10, 10)],
        kind=RoiKind.POINT,
    )
    updated = update_roi(
        roi=roi.id,
        vectors=[_pt(50, 60)],
    )
    assert updated.id == roi.id
    assert updated.vectors[0].x == 50
    assert updated.vectors[0].y == 60


@pytest.mark.integration
def test_delete_roi(deployed_app: DeployedMikro) -> None:
    """Delete a ROI and confirm it no longer appears in the image's ROI list."""
    image = from_array_like(_make_image(), name="roi_delete_image")
    roi = create_roi(
        image=image.id,
        vectors=[_pt(10, 10)],
        kind=RoiKind.POINT,
    )
    deleted_id = delete_roi(id=roi.id)
    assert deleted_id == roi.id

    remaining = get_rois(image=image.id)
    assert all(r.id != roi.id for r in remaining), "Deleted ROI should not appear in list"
