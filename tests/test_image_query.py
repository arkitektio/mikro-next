import numpy as np
import pytest
import xarray as xr
from mikro_next.api.schema import (
    from_array_like,
    get_image,
    search_images,
)
from .conftest import DeployedMikro


def _make_image() -> xr.DataArray:
    return xr.DataArray(np.random.random((50, 50, 3)), dims=["x", "y", "z"])


@pytest.mark.integration
def test_get_image(deployed_app: DeployedMikro) -> None:
    """Write an image and retrieve it by ID."""
    written = from_array_like(_make_image(), name="get_image_target")
    fetched = get_image(id=written.id)
    assert fetched.id == written.id
    assert fetched.name == "get_image_target"


@pytest.mark.integration
def test_search_images(deployed_app: DeployedMikro) -> None:
    """Search for an image by name substring."""
    written = from_array_like(_make_image(), name="searchable_image_xyzzy")
    results = search_images(search="searchable_image_xyzzy")
    assert any(o.value == written.id for o in results), (
        "Created image should appear in search results"
    )
