from mikro_next.api.schema import from_array_like, create_snapshot
from mikro_next import MikroNext
import xarray as xr
import numpy as np
import pytest
from PIL import Image


@pytest.mark.integration
def test_create_array(deployed_app: MikroNext):
    
    l = from_array_like(
        xr.DataArray(np.zeros((1000, 1000, 10)), dims=["x", "y", "z"]),
        name="Farter 1",
    )
    assert l.data.shape == (
        1,
        1,
        10,
        1000,
        1000,
    ), "Shape should be (10, 1000, 1000)"
    pass



@pytest.mark.integration
def upload_file(deployed_app: MikroNext):
    # Create an image file
    image_data = np.random.rand(100, 100, 3) * 255
    image_data = image_data.astype(np.uint8)
    image = xr.DataArray(image_data, dims=["x", "y", "color"])
    
    # Save the image to a temporary file
    image_file_path = "test_image.png"
    image_pil = Image.fromarray(image_data)
    
    image_pil.save(image_file_path)
    
    image = from_array_like(
        image_data,
        name="The image name"
    )
    
    t = create_snapshot(
        image_file_path,
        image 
    )
    return t
        