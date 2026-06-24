from typing import Callable

import pytest
from rath.operation import GraphQLException
from mikro_next.api.schema import (
    create_dataset,
    search_datasets,
    search_images,
    search_files,
    search_meshes,
    search_rois,
    search_scenes,
    search_stages,
    search_snapshots,
    search_tables,
    search_table_cells,
    search_table_rows,
    search_rgb_views,
)
from .conftest import DeployedMikro


# A unique substring shared by all datasets created in this module, so that the
# search filter isolates exactly the datasets we create here.
PREFIX = "paginated_dataset_qwoptyz"


@pytest.fixture(scope="module")
def paginated_datasets(deployed_app: DeployedMikro) -> list:
    """Create a known set of searchable datasets to paginate over."""
    return [create_dataset(name=f"{PREFIX}_{i:02d}") for i in range(5)]


@pytest.mark.integration
def test_search_limit_caps_results(paginated_datasets: list) -> None:
    """`limit` should cap the number of returned options."""
    results = search_datasets(search=PREFIX, limit=2)
    assert len(results) == 2, "limit=2 should return at most two options"


@pytest.mark.integration
def test_search_offset_skips_results(paginated_datasets: list) -> None:
    """`offset` should skip leading results within a stable ordering."""
    first_two = search_datasets(search=PREFIX, limit=2, offset=0)
    next_two = search_datasets(search=PREFIX, limit=2, offset=2)

    first_ids = {o.value for o in first_two}
    next_ids = {o.value for o in next_two}

    assert len(first_two) == 2
    assert len(next_two) == 2
    assert first_ids.isdisjoint(next_ids), (
        "Offset pages should not overlap when limit divides the offset evenly"
    )


@pytest.mark.integration
def test_search_pagination_covers_all(paginated_datasets: list) -> None:
    """Paging through with limit/offset should surface every created dataset."""
    created_ids = {d.id for d in paginated_datasets}

    seen: set = set()
    offset = 0
    page_size = 2
    # Guard against an unexpectedly large result set / infinite loop.
    for _ in range(20):
        page = search_datasets(search=PREFIX, limit=page_size, offset=offset)
        if not page:
            break
        seen.update(o.value for o in page)
        offset += page_size

    assert created_ids.issubset(seen), (
        "Every created dataset should be reachable by paging through with limit/offset"
    )


@pytest.mark.integration
def test_search_offset_defaults_to_zero(paginated_datasets: list) -> None:
    """Omitting `offset` should behave like offset=0."""
    without_offset = search_datasets(search=PREFIX, limit=3)
    with_zero_offset = search_datasets(search=PREFIX, limit=3, offset=0)

    assert [o.value for o in without_offset] == [o.value for o in with_zero_offset]


@pytest.mark.integration
@pytest.mark.parametrize(
    "search_func, extra_kwargs",
    [
        (search_datasets, {}),
        (search_images, {}),
        (search_files, {}),
        (search_meshes, {}),
        (search_rois, {}),
        (search_scenes, {}),
        (search_stages, {}),
        (search_snapshots, {}),
        (search_tables, {}),
        # tableCells/tableRows are scoped to a table, so they take a required
        # `table` argument. The id need not resolve to real data here; we only
        # check that limit/offset are accepted (a missing table yields a
        # non-pagination server error, which is tolerated below).
        (search_table_cells, {"table": "1"}),
        (search_table_rows, {"table": "1"}),
        (search_rgb_views, {}),
    ],
)
def test_search_widgets_accept_limit_and_offset(
    deployed_app: DeployedMikro, search_func: Callable, extra_kwargs: dict
) -> None:
    """Every search widget should accept optional limit/offset arguments.

    The server must validate and accept the `limit`/`offset` variables. If a
    resource has no rows the resolver may still raise an unrelated server-side
    error; that is tolerated here as long as it is not about pagination, which
    is what this change introduces.
    """
    try:
        results = search_func(limit=1, offset=0, **extra_kwargs)
    except GraphQLException as exc:
        message = str(exc).lower()
        for arg in ("pagination", "limit", "offset"):
            assert arg not in message, (
                f"{search_func.__name__} rejected the {arg} argument: {exc}"
            )
        return

    assert isinstance(results, tuple)
    assert len(results) <= 1, f"{search_func.__name__} should respect limit=1"
