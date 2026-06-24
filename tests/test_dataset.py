import pytest
from mikro_next.api.schema import (
    create_dataset,
    get_dataset,
    update_dataset,
    search_datasets,
)
from .conftest import DeployedMikro


@pytest.mark.integration
def test_get_dataset(deployed_app: DeployedMikro) -> None:
    """Create a dataset and retrieve it by ID."""
    created = create_dataset(name="fetchable_dataset")
    fetched = get_dataset(id=created.id)
    assert fetched.id == created.id
    assert fetched.name == "fetchable_dataset"


@pytest.mark.integration
def test_update_dataset(deployed_app: DeployedMikro) -> None:
    """Rename a dataset and verify the change is persisted."""
    created = create_dataset(name="dataset_before_rename")
    updated = update_dataset(id=created.id, name="dataset_after_rename")
    assert updated.id == created.id, "Updating should keep the same ID"
    assert updated.name == "dataset_after_rename"


@pytest.mark.integration
def test_search_datasets(deployed_app: DeployedMikro) -> None:
    """Search for a dataset by name substring."""
    created = create_dataset(name="searchable_dataset_xyzzy")
    results = search_datasets(search="searchable_dataset_xyzzy")
    assert any(o.label == "searchable_dataset_xyzzy" for o in results), (
        "Created dataset should appear in search results"
    )
    assert any(o.value == created.id for o in results), (
        "Search results should include the created dataset's ID"
    )
