"""Tests for the table-dataset path -- ``create_table_dataset``.

This replaces the deprecated ``from_parquet_like`` / ``Table`` route. The
difference is not just a new mutation name: a table dataset *declares its
columns*, and those declarations are what the server builds a coordinate system
out of. A COORDINATE column becomes an axis of a space the table owns, which is
what makes a localization table placeable in a scene; a table with no coordinate
column is a measurement table whose rows enumerate objects.

Most of what can go wrong is decided client-side -- which Parquet-like things are
accepted, how each is handed to the object store, and whether the declared schema
is well formed -- so most of this file runs offline.
"""

import tempfile
import unittest.mock
from pathlib import Path
from typing import Any, Iterator, List, Tuple

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import xarray as xr
from pydantic import ValidationError

from mikro_next.api.schema import (
    AxisInput,
    AxisType,
    CreateTableDatasetInput,
    DatasetKeyedByInput,
    TableColumnInput,
    TableColumnRole,
    create_array_dataset,
    create_table_dataset,
    get_table_dataset,
    update_table_dataset,
)
from mikro_next.io.upload import _parquet_payload
from mikro_next.scalars import ParquetLike

from .conftest import DeployedMikro


def _localizations(rows: int = 32) -> pd.DataFrame:
    """A localization table: three coordinate columns plus a measurement."""
    rng = np.random.default_rng(seed=42)
    return pd.DataFrame(
        {
            "z": rng.random(rows) * 10.0,
            "y": rng.random(rows) * 100.0,
            "x": rng.random(rows) * 100.0,
            "photons": rng.random(rows) * 1000.0,
        }
    )


def _localization_columns() -> List[TableColumnInput]:
    """The declaration that turns those four columns into a placeable space.

    Only the three coordinate columns become axes; ``photons`` is data hanging
    off the row and places nothing.
    """
    return [
        TableColumnInput(
            name=axis,
            dtype="DOUBLE",
            role=TableColumnRole.COORDINATE,
            axisType=AxisType.SPACE,
            unit="micrometer",
        )
        for axis in ("z", "y", "x")
    ] + [
        TableColumnInput(
            name="photons",
            dtype="DOUBLE",
            role=TableColumnRole.ATTRIBUTE,
            longName="photon count",
        )
    ]


def _measurements(objects: int = 8) -> pd.DataFrame:
    """A measurement table: one row per segmented object, keyed by its id."""
    rng = np.random.default_rng(seed=7)
    return pd.DataFrame(
        {
            "object_id": np.arange(1, objects + 1, dtype="int64"),
            "voxel_count": rng.integers(10, 500, size=objects),
            "mean_intensity": rng.random(objects),
        }
    )


_MEASUREMENT_COLUMNS = [
    TableColumnInput(name="object_id", dtype="BIGINT", role=TableColumnRole.ID),
    TableColumnInput(name="voxel_count", dtype="BIGINT", role=TableColumnRole.ATTRIBUTE),
    TableColumnInput(
        name="mean_intensity", dtype="DOUBLE", role=TableColumnRole.ATTRIBUTE
    ),
]

#: The same table, declared so a mask can key into it. ``object_id`` has to be a
#: COORDINATE column with an INDEX axis type, not merely an ID: without one the
#: table's space is a synthetic axis that only enumerates rows, and there is no
#: column for a sampled pixel value to be looked up in -- so the ``keyedBy`` edge
#: would never resolve. An enumerating axis carries no unit, because there is
#: nothing to measure: the distance between object 3 and object 4 means nothing.
_KEYED_MEASUREMENT_COLUMNS = [
    TableColumnInput(
        name="object_id",
        dtype="BIGINT",
        role=TableColumnRole.COORDINATE,
        axisType=AxisType.INDEX,
        longName="object id",
    ),
    *_MEASUREMENT_COLUMNS[1:],
]


# ---------------------------------------------------------------------------
# Column declarations
# ---------------------------------------------------------------------------


def test_a_column_is_an_attribute_unless_it_says_otherwise() -> None:
    """``role`` carries the server's default rather than restating it here, so
    an undeclared role travels as null and is filled in server-side."""
    column = TableColumnInput(name="area", dtype="DOUBLE")
    assert column.role is None


def test_a_coordinate_column_carries_an_axis_type_and_a_unit() -> None:
    """These two are what make the column an axis of the table's own space: the
    kind of axis it is, and what its numbers are measured in."""
    column = TableColumnInput(
        name="x",
        dtype="DOUBLE",
        role=TableColumnRole.COORDINATE,
        axisType=AxisType.SPACE,
        unit="micrometer",
    )
    assert column.role == TableColumnRole.COORDINATE.value
    assert column.axis_type == AxisType.SPACE.value
    assert column.unit == "micrometer"


def test_an_index_column_is_the_axis_of_an_enumerating_table() -> None:
    """A per-object table has no metric axis -- the distance between object 3
    and object 4 means nothing -- so its coordinate axis is INDEX."""
    column = TableColumnInput(
        name="object_id",
        dtype="BIGINT",
        role=TableColumnRole.COORDINATE,
        axisType=AxisType.INDEX,
    )
    assert column.axis_type == AxisType.INDEX.value


def test_a_column_unit_must_be_a_real_unit() -> None:
    """Caught here rather than after the upload of a table has already run."""
    with pytest.raises(ValidationError):
        TableColumnInput(name="x", dtype="DOUBLE", unit="not a unit at all")


def test_an_unknown_column_field_is_rejected() -> None:
    """A misspelled field would otherwise be dropped silently, and the column
    would arrive declaring less than the caller wrote."""
    with pytest.raises(ValidationError):
        TableColumnInput(name="x", dtype="DOUBLE", axis="SPACE")


# ---------------------------------------------------------------------------
# The mutation input
# ---------------------------------------------------------------------------


def test_the_input_wraps_a_dataframe_as_parquet() -> None:
    frame = _localizations()
    model = CreateTableDatasetInput(
        name="localizations",
        data=frame,
        columns=_localization_columns(),
        validateSchema=True,
    )
    assert isinstance(model.data, ParquetLike)
    assert model.data.value.equals(frame)
    assert model.validate_schema is True


def test_the_input_takes_a_measurement_table_with_no_coordinate_columns() -> None:
    """No coordinate column is a legitimate declaration, not an omission: the
    rows enumerate objects and the table's lineage edge is UNMAPPABLE."""
    model = CreateTableDatasetInput(
        name="measurements", data=_measurements(), columns=_MEASUREMENT_COLUMNS
    )
    assert all(
        column.role != TableColumnRole.COORDINATE.value for column in model.columns
    )


def test_the_input_carries_the_mask_a_table_is_keyed_by() -> None:
    """``keyedBy`` authors the FIELD edge in the direction the map actually runs
    -- mask pixels -> table rows -- which is the opposite of ``derivedFrom``."""
    model = CreateTableDatasetInput(
        name="measurements",
        data=_measurements(),
        columns=_MEASUREMENT_COLUMNS,
        keyedBy=[DatasetKeyedByInput(dataset="17", name="object ids -> measurements")],
    )
    assert model.keyed_by is not None
    assert model.keyed_by[0].dataset == "17"


def test_the_input_rejects_an_unknown_field() -> None:
    with pytest.raises(ValidationError):
        CreateTableDatasetInput(
            name="localizations",
            data=_localizations(),
            columns=_localization_columns(),
            dataframe=_localizations(),
        )


def test_the_input_rejects_something_that_is_not_parquet_like() -> None:
    with pytest.raises(ValidationError):
        CreateTableDatasetInput(name="nope", data={"x": [1, 2, 3]}, columns=[])


# ---------------------------------------------------------------------------
# ParquetLike: what counts as a table
# ---------------------------------------------------------------------------


def test_parquet_like_accepts_a_dataframe() -> None:
    frame = _localizations()
    assert ParquetLike.validate(frame).value.equals(frame)


def test_parquet_like_accepts_an_arrow_table() -> None:
    """Serialized without the pandas round trip -- one fewer full copy of a
    table that is already the largest object in the process."""
    table = pa.table({"object_id": [1, 2, 3]})
    assert ParquetLike.validate(table).value is table


def test_parquet_like_accepts_a_record_batch_reader() -> None:
    """The streaming case: peak memory is one batch, not the whole table."""
    reader = pa.RecordBatchReader.from_batches(
        pa.schema([("a", pa.int64())]), [pa.record_batch({"a": pa.array([1, 2])})]
    )
    assert ParquetLike.validate(reader).value is reader


def test_parquet_like_accepts_a_path_to_an_existing_file(tmp_path: Path) -> None:
    """A file already on disk is never read into this process."""
    path = tmp_path / "table.parquet"
    pq.write_table(pa.Table.from_pandas(_measurements()), path)

    validated = ParquetLike.validate(str(path))
    assert validated.value == path


def test_parquet_like_rejects_a_path_that_is_not_there(tmp_path: Path) -> None:
    """A typo'd path should fail while the caller still knows which table it
    meant, not inside an upload link three mutations later."""
    with pytest.raises(ValueError, match="No parquet file at"):
        ParquetLike.validate(tmp_path / "missing.parquet")


def test_parquet_like_rejects_anything_else() -> None:
    with pytest.raises(ValueError, match="pandas DataFrame"):
        ParquetLike.validate([1, 2, 3])


def test_parquet_like_is_idempotent() -> None:
    once = ParquetLike.validate(_measurements())
    assert ParquetLike.validate(once) is once


def test_every_table_gets_its_own_upload_key() -> None:
    """The key is what the upload middleware stores the object under, so two
    tables in one mutation must not collide."""
    assert ParquetLike.validate(_measurements()).key != ParquetLike.validate(
        _measurements()
    ).key


# ---------------------------------------------------------------------------
# What each Parquet-like shape is handed to the object store as
# ---------------------------------------------------------------------------


def test_a_path_is_uploaded_as_is(tmp_path: Path) -> None:
    """obstore reads it in chunks and multipart-uploads it, so a 4 GB table
    never enters this process -- and there is no scratch file to clean up."""
    path = tmp_path / "table.parquet"
    pq.write_table(pa.Table.from_pandas(_measurements()), path)

    payload, scratch = _parquet_payload(path)
    assert payload == path
    assert scratch is None


def test_a_dataframe_is_serialized_in_memory() -> None:
    """The small case keeps the original in-memory path exactly: routing it
    through a temp file would make every caller depend on writable scratch."""
    frame = _measurements()
    payload, scratch = _parquet_payload(frame)

    assert scratch is None
    assert pq.read_table(payload).to_pandas().equals(frame)


def test_an_arrow_table_is_written_to_a_scratch_file() -> None:
    """Serialized to disk rather than to a buffer, because a second full copy of
    the largest object in the process is the thing worth avoiding."""
    table = pa.Table.from_pandas(_measurements())
    payload, scratch = _parquet_payload(table)

    try:
        assert payload == scratch
        assert scratch is not None and scratch.exists()
        assert pq.read_table(scratch).equals(table)
    finally:
        if scratch is not None:
            scratch.unlink(missing_ok=True)


def test_a_record_batch_reader_is_written_batch_by_batch() -> None:
    frame = _measurements()
    table = pa.Table.from_pandas(frame)
    reader = pa.RecordBatchReader.from_batches(table.schema, table.to_batches(max_chunksize=2))

    payload, scratch = _parquet_payload(reader)
    try:
        assert payload == scratch
        assert pq.read_table(scratch).to_pandas().equals(frame)
    finally:
        if scratch is not None:
            scratch.unlink(missing_ok=True)


def test_a_failed_write_leaves_no_scratch_file_behind() -> None:
    """A half-written scratch file is not a parquet file, and leaving it behind
    would be a silent disk leak on every failed upload."""
    written: List[Path] = []
    real_mkstemp = tempfile.mkstemp

    def _batches() -> Iterator[pa.RecordBatch]:
        yield pa.record_batch({"a": pa.array([1, 2])})
        raise RuntimeError("the source went away mid-stream")

    reader = pa.RecordBatchReader.from_batches(
        pa.schema([("a", pa.int64())]), _batches()
    )

    def _tracking_mkstemp(*args: Any, **kwargs: Any) -> Tuple[int, str]:  # noqa: ANN401
        handle, name = real_mkstemp(*args, **kwargs)
        written.append(Path(name))
        return handle, name

    with unittest.mock.patch.object(tempfile, "mkstemp", _tracking_mkstemp):
        with pytest.raises(RuntimeError, match="went away mid-stream"):
            _parquet_payload(reader)

    assert written, "the reader path should have opened a scratch file"
    assert not any(path.exists() for path in written)


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_create_a_measurement_table(deployed_app: DeployedMikro) -> None:
    """A table with no coordinate columns: its rows enumerate objects."""
    table = create_table_dataset(
        name="measurements_basic",
        data=_measurements(),
        columns=_MEASUREMENT_COLUMNS,
        validate_schema=True,
        description="one row per segmented object",
    )

    assert table.id, "Table dataset should have an ID"
    assert table.name == "measurements_basic"
    assert [column.name for column in table.columns] == [
        "object_id",
        "voxel_count",
        "mean_intensity",
    ]


@pytest.mark.integration
def test_a_measurement_table_reads_back_out_of_its_store(
    deployed_app: DeployedMikro,
) -> None:
    """The rows come off the Parquet store directly, not through GraphQL: the
    store hands out an access grant and DuckDB queries the object in place."""
    frame = _measurements()
    table = create_table_dataset(
        name="measurements_readback",
        data=frame,
        columns=_MEASUREMENT_COLUMNS,
        validate_schema=True,
    )

    relation = table.store.duckdb_relation
    assert relation.df().equals(frame), "Materialised rows should match the source"

    # The filter runs in DuckDB against the object store, not by downloading the
    # whole table into pandas first.
    filtered = relation.filter("voxel_count > 100").df()
    assert (filtered["voxel_count"] > 100).all()


@pytest.mark.integration
def test_coordinate_columns_become_the_axes_of_the_tables_own_space(
    deployed_app: DeployedMikro,
) -> None:
    """This is the whole point of declaring roles: the coordinate columns -- and
    only those -- turn into a coordinate system the table owns, which is what
    makes a localization table placeable next to the volume it came from."""
    table = create_table_dataset(
        name="localizations_spaced",
        data=_localizations(),
        columns=_localization_columns(),
        validate_schema=True,
    )

    assert tuple(table.axis_names) == ("z", "y", "x")
    assert table.coordinate_system.id
    assert [axis.name for axis in table.coordinate_system.axes] == ["z", "y", "x"]
    assert all(axis.unit == "micrometer" for axis in table.coordinate_system.axes)


@pytest.mark.integration
def test_a_table_is_keyed_by_the_mask_it_measures(deployed_app: DeployedMikro) -> None:
    """The modern successor of the image-plus-mask pairing.

    A label mask goes up as an array dataset whose pixel values are object ids;
    the measurements of those objects go up as a table dataset keyed by it.
    ``keyedBy`` alone is the link, and no ``derivedFrom`` accompanies it -- the
    two run in opposite directions, and a lineage edge would additionally claim
    the rows are a spatial transform of the mask, which they are not.
    """
    labels = np.zeros((4, 16, 16), dtype="uint16")
    for object_id in range(1, 9):
        labels[object_id % 4, object_id : object_id + 2, object_id : object_id + 2] = object_id

    mask = create_array_dataset(
        data=xr.DataArray(labels, dims=["z", "y", "x"]),
        scales=[],
        name="keyed_mask",
        axes=[AxisInput(name=axis, type=AxisType.SPACE) for axis in ("z", "y", "x")],
    )

    table = create_table_dataset(
        name="keyed_measurements",
        data=_measurements(),
        columns=_KEYED_MEASUREMENT_COLUMNS,
        validate_schema=True,
        keyed_by=[DatasetKeyedByInput(dataset=mask.id, name="object ids -> measurements")],
    )

    assert table.id
    assert tuple(table.axis_names) == ("object_id",), (
        "The column the mask keys into should be the table's axis"
    )
    assert get_table_dataset(id=table.id).id == table.id


@pytest.mark.integration
def test_a_table_can_be_renamed_and_redescribed(deployed_app: DeployedMikro) -> None:
    """The whole of what is editable. Its store, columns and coordinate system
    are fixed at creation -- a recomputation is a new table."""
    table = create_table_dataset(
        name="renamable", data=_measurements(), columns=_MEASUREMENT_COLUMNS, validate_schema=True
    )

    updated = update_table_dataset(
        id=table.id, name="renamed", description="now with a description"
    )
    assert updated.name == "renamed"
    assert updated.description == "now with a description"
    assert updated.id == table.id


@pytest.mark.integration
def test_a_declared_schema_that_does_not_match_the_data_is_rejected(
    deployed_app: DeployedMikro,
) -> None:
    """``validate_schema=True`` is what makes the declaration load-bearing: a
    column that is not in the Parquet file is an error, not a silent omission."""
    with pytest.raises(Exception):
        create_table_dataset(
            name="mismatched",
            data=_measurements(),
            columns=_MEASUREMENT_COLUMNS
            + [TableColumnInput(name="not_a_real_column", dtype="DOUBLE")],
            validate_schema=True,
        )
