import pytest
from mikro_next.api.schema import (
    create_folder,
    get_folder,
    update_folder,
    search_folders,
)
from .conftest import DeployedMikro


@pytest.mark.integration
def test_get_folder(deployed_app: DeployedMikro) -> None:
    """Create a folder and retrieve it by ID."""
    created = create_folder(name="fetchable_folder")
    fetched = get_folder(id=created.id)
    assert fetched.id == created.id
    assert fetched.name == "fetchable_folder"


@pytest.mark.integration
def test_update_folder(deployed_app: DeployedMikro) -> None:
    """Rename a folder and verify the change is persisted."""
    created = create_folder(name="folder_before_rename")
    updated = update_folder(id=created.id, name="folder_after_rename")
    assert updated.id == created.id, "Updating should keep the same ID"
    assert updated.name == "folder_after_rename"


@pytest.mark.integration
def test_search_folders(deployed_app: DeployedMikro) -> None:
    """Search for a folder by name substring."""
    created = create_folder(name="searchable_folder_xyzzy")
    results = search_folders(search="searchable_folder_xyzzy")
    assert any(o.label == "searchable_folder_xyzzy" for o in results), (
        "Created folder should appear in search results"
    )
    assert any(o.value == created.id for o in results), (
        "Search results should include the created folder's ID"
    )
