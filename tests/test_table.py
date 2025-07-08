import numpy as np
import pytest
from mikro_next.api.schema import from_parquet_like

from .conftest import DeployedMikro
import pandas as pd


@pytest.mark.integration
def test_write_random(deployed_app: DeployedMikro) -> None:
    """Test writing a random image."""

    simple_df = pd.DataFrame(
        {
            "x": np.random.random(1000),
            "y": np.random.random(1000),
            "z": np.random.random(1000),
            "value": np.random.random(1000),
        }
    )

    x = from_parquet_like(
        simple_df,
        name="test_random_write",
    )
    assert x.id, "Did not get a random rep"
