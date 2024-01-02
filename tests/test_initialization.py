from mikro_next.api.schema import from_array_like
from mikro_next.deployed import DeployedMikroNext
import xarray as xr
import numpy as np
import pytest


@pytest.mark.integration
def test_create_array(deployed_app: DeployedMikroNext):
    with deployed_app.deployment.logswatcher("mikro"):
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
