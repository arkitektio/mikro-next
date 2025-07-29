import numpy as np
import pytest
from mikro_next.api.schema import create_dataset, from_array_like, get_random_image
from mikro_next.api.schema import (
    create_reference_view,
    PartialMaskViewInput,
)
import xarray as xr
from .conftest import DeployedMikro


@pytest.mark.integration
def test_write_random(deployed_app: DeployedMikro) -> None:
    """Test writing a random image."""
    x = from_array_like(
        xr.DataArray(data=np.random.random((1000, 1000, 10)), dims=["x", "y", "z"]),
        name="test_random_write",
    )
    assert x.id, "Did not get a random rep"
    assert x.data.shape == (
        1,
        1,
        10,
        1000,
        1000,
    ), "Did not write data according to schema ( T, C, Z, Y, X )"


@pytest.mark.integration
def test_get_random(deployed_app: DeployedMikro) -> None:
    """Test getting a random image. This should return the image written in the previous test."""
    x = from_array_like(
        xr.DataArray(data=np.random.random((1000, 1000, 10)), dims=["x", "y", "z"]),
        name="test_random_write",
    )
    x = get_random_image()
    assert x.id, "Did not get a random rep even though one was written"


@pytest.mark.integration
def test_create_dataset(deployed_app: DeployedMikro) -> None:
    """Test creating a dataset."""
    x = create_dataset(name="johannes")
    assert x.id, "Was not able to create a dataset"


@pytest.mark.integration
def test_create_dataset_in_parent(deployed_app: DeployedMikro) -> None:
    """Test creating a dataset with a parent."""
    x = create_dataset(name="johannes")

    create_dataset(name="johannes", parent=x.id)

    pass


@pytest.mark.integration
def test_create_image_with_mask(deployed_app: DeployedMikro) -> None:
    initial_image = xr.DataArray(np.zeros((100, 100, 3), dtype=np.uint8), dims=("y", "x", "c"))

    initial_image[0:50, 0:50, :] = [255, 0, 0]  # Red square
    initial_image[50:100, 50:100, :] = [0, 34, 0]  # Green square
    initial_image[0:50, 50:100, :] = [0, 0, 123]  # Blue square

    image = from_array_like(
        array=initial_image,
        name="FUCK IMAGE HARD",
        tags=["test", "image"],
    )

    ref_frame = create_reference_view(image, c_min=0, c_max=1)

    from_array_like(
        array=xr.DataArray(np.zeros((100, 100, 1), dtype=np.uint8), dims=("y", "x", "c")),
        name="Test Mask",
        mask_views=[
            PartialMaskViewInput(
                referenceView=ref_frame,
            )
        ],
    )
