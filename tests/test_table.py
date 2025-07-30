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


def test_parquet_like_scalar_validation() -> None:
    """Test ParquetLike scalar validation without integration."""
    from mikro_next.scalars import ParquetLike

    # Test valid DataFrame
    valid_df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "value": [0.1, 0.2, 0.3]})

    parquet_like = ParquetLike.validate(valid_df)
    assert parquet_like.value.equals(valid_df), "DataFrame should be preserved"
    assert hasattr(parquet_like, "key"), "Should have a key attribute"

    # Test DataFrame with missing values
    df_with_nans = pd.DataFrame({"x": [1, 2, np.nan], "y": [4, np.nan, 6]})

    parquet_like_nans = ParquetLike.validate(df_with_nans)
    assert parquet_like_nans.value.isnull().any().any(), "NaN values should be preserved"


def test_from_parquet_like_input_validation() -> None:
    """Test FromParquetLike input validation without integration."""
    from mikro_next.api.schema import FromParquetLike

    test_df = pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})

    # Test valid input
    valid_input = FromParquetLike(dataframe=test_df, name="test_table")
    assert valid_input.name == "test_table", "Name should be preserved"
    assert valid_input.dataframe.value.equals(test_df), "DataFrame should be preserved"

    # Test with optional fields
    from rath.scalars import ID

    with_dataset = FromParquetLike(
        dataframe=test_df, name="test_table_with_dataset", dataset=ID("test_dataset_id")
    )
    assert with_dataset.dataset == ID("test_dataset_id"), "Dataset ID should be preserved"
