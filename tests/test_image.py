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


def test_array_like_scalar_validation() -> None:
    """Test ArrayLike scalar validation without integration."""
    from mikro_next.scalars import ArrayLike

    # Test with valid xarray DataArray
    valid_array = xr.DataArray(np.random.random((10, 10, 5)), dims=["x", "y", "z"])

    array_like = ArrayLike.validate(valid_array)
    assert array_like.value.dims == ("c", "t", "z", "y", "x"), "Should have correct dimensions"
    assert array_like.value.ndim == 5, "Should be 5-dimensional"
    assert hasattr(array_like, "key"), "Should have a key attribute"

    # Test with numpy array (gets converted)
    numpy_array = np.random.random((10, 10, 10))
    array_like_numpy = ArrayLike.validate(numpy_array)
    assert array_like_numpy.value.ndim == 5, "Should be 5-dimensional after conversion"

    # Test dimension requirements
    minimal_array = xr.DataArray(np.random.random((10, 10)), dims=["x", "y"])
    array_like_minimal = ArrayLike.validate(minimal_array)
    assert "x" in array_like_minimal.value.dims, "Must have x dimension"
    assert "y" in array_like_minimal.value.dims, "Must have y dimension"


def test_from_array_like_input_validation() -> None:
    """Test FromArrayLikeInput validation without integration."""
    from mikro_next.api.schema import FromArrayLikeInput

    test_array = xr.DataArray(np.random.random((10, 10, 5)), dims=["x", "y", "z"])

    # Test valid input
    valid_input = FromArrayLikeInput(array=test_array, name="test_image")
    assert valid_input.name == "test_image", "Name should be preserved"
    assert valid_input.array.value.dims == ("c", "t", "z", "y", "x"), "Array should be processed"

    # Test with dataset
    from rath.scalars import ID

    with_dataset = FromArrayLikeInput(
        array=test_array, name="test_image_with_dataset", dataset=ID("test_dataset_id")
    )
    assert with_dataset.dataset == ID("test_dataset_id"), "Dataset ID should be preserved"


def test_partial_mask_view_input_validation() -> None:
    """Test PartialMaskViewInput validation without integration."""
    from mikro_next.api.schema import PartialMaskViewInput
    from rath.scalars import ID

    # Test valid mask view input
    mask_input = PartialMaskViewInput(referenceView=ID("test_reference_view_id"))
    assert mask_input.reference_view == ID("test_reference_view_id"), (
        "Reference view should be preserved"
    )


def test_mikro_error_classes() -> None:
    """Test custom error classes."""
    from mikro_next.errors import MikroError, NoMikroFound, NoDataLayerFound, NotQueriedError

    # Test base error
    base_error = MikroError("Base error message")
    assert str(base_error) == "Base error message", "Error message should be preserved"
    assert isinstance(base_error, Exception), "Should be an Exception"

    # Test specific errors
    no_mikro_error = NoMikroFound("No mikro instance found")
    assert isinstance(no_mikro_error, MikroError), "Should inherit from MikroError"

    no_datalayer_error = NoDataLayerFound("No data layer found")
    assert isinstance(no_datalayer_error, MikroError), "Should inherit from MikroError"

    not_queried_error = NotQueriedError("Field not queried")
    assert isinstance(not_queried_error, MikroError), "Should inherit from MikroError"


def test_rechunk_utility_function() -> None:
    """Test the rechunk utility function."""
    from mikro_next.utils import rechunk
    from typing import Dict, Hashable

    # Test with standard image sizes
    sizes: Dict[Hashable, int] = {"c": 3, "t": 10, "z": 20, "y": 1024, "x": 1024}
    chunks = rechunk(sizes)

    assert "c" in chunks, "Should include c dimension"
    assert "t" in chunks, "Should include t dimension"
    assert "z" in chunks, "Should include z dimension"
    assert "y" in chunks, "Should include y dimension"
    assert "x" in chunks, "Should include x dimension"

    # Test chunk size constraints
    assert chunks["x"] <= 2048, "X chunk should not exceed 2048"
    assert chunks["y"] <= 2048, "Y chunk should not exceed 2048"
    assert chunks["c"] == 1, "C chunk should be 1"

    # Test with small image (should return original sizes)
    small_sizes: Dict[Hashable, int] = {"c": 1, "t": 1, "z": 1, "y": 100, "x": 100}
    small_chunks = rechunk(small_sizes)
    assert small_chunks == small_sizes, "Small images should not be rechunked"
