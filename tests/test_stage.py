import numpy as np
import pytest
import xarray as xr
from mikro_next.api.schema import (
    create_stage,
    get_stage,
    search_stages,
    from_array_like,
)
from .conftest import DeployedMikro


@pytest.mark.integration
def test_create_stage(deployed_app: DeployedMikro) -> None:
    """Create a stage and verify it gets an ID."""
    stage = create_stage(name="test_stage")
    assert stage.id, "Stage should have an ID"
    assert stage.name == "test_stage"


@pytest.mark.integration
def test_get_stage(deployed_app: DeployedMikro) -> None:
    """Retrieve a stage by ID."""
    created = create_stage(name="fetchable_stage")
    fetched = get_stage(id=created.id)
    assert fetched.id == created.id
    assert fetched.name == "fetchable_stage"


@pytest.mark.integration
def test_search_stages(deployed_app: DeployedMikro) -> None:
    """Search for stages by name substring."""
    create_stage(name="unique_stage_xyzzy")
    results = search_stages(search="unique_stage_xyzzy")
    assert any(s.label == "unique_stage_xyzzy" for s in results), (
        "Created stage should appear in search results"
    )


@pytest.mark.integration
def test_stage_affine_views(deployed_app: DeployedMikro) -> None:
    """Images with affine transformation views reference their stage."""
    from mikro_next.api.schema import PartialAffineTransformationViewInput

    stage = create_stage(name="affine_stage")
    image = from_array_like(
        xr.DataArray(np.random.random((50, 50, 3)), dims=["x", "y", "z"]),
        name="affine_image",
        transformation_views=[
            PartialAffineTransformationViewInput(
                stage=stage.id,
                affine_matrix=[
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
            )
        ],
    )
    assert image.id

    fetched_stage = get_stage(id=stage.id)
    assert fetched_stage.id == stage.id
