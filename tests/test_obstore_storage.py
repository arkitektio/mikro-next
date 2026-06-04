from io import BytesIO
from types import SimpleNamespace

import dask.array as da
import numpy as np
import obstore
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import xarray as xr
import zarr
from obstore.store import MemoryStore
from zarr.storage import ObjectStore as ZarrObjectStore, StorePath

from mikro_next.io.download import download_file
from mikro_next.io.obstore import (
    ParquetDatasetViaObstore,
    awrite_dataarray_to_zarr,
    write_dataarray_to_zarr,
)
from mikro_next.scalars import ArrayLike, ImageLike


def test_parquet_dataset_via_obstore_reads_dataframe() -> None:
    store = MemoryStore()
    dataframe = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    buffer = BytesIO()

    pq.write_table(pa.Table.from_pandas(dataframe), buffer)
    obstore.put(store, "tables/example.parquet", buffer.getvalue())

    dataset = ParquetDatasetViaObstore(store, "tables/example.parquet")

    assert dataset.read_pandas().to_pandas().equals(dataframe)


def test_download_file_reads_bytes_via_obstore(tmp_path, monkeypatch) -> None:
    store = MemoryStore()
    payload = b"hello via obstore"
    target = tmp_path / "download.bin"
    credentials = SimpleNamespace(
        access_key="access",
        secret_key="secret",
        session_token="token",
        bucket="bucket",
        key="files/download.bin",
        path="bucket/files/download.bin",
    )

    obstore.put(store, credentials.key, payload)

    monkeypatch.setattr(
        "mikro_next.io.download.unkoil",
        lambda function, store_id: (credentials, "http://example.invalid"),
    )
    monkeypatch.setattr("mikro_next.io.download.create_s3_store", lambda *_args: store)

    result = download_file("store-id", str(target))

    assert result == str(target)
    assert target.read_bytes() == payload


def _store_path(key: str = "arr") -> StorePath:
    return StorePath(ZarrObjectStore(MemoryStore()), key)


def test_write_dataarray_to_zarr_numpy_roundtrips_with_chunks() -> None:
    array = xr.DataArray(
        np.arange(1 * 1 * 4 * 64 * 64, dtype="uint16").reshape(1, 1, 4, 64, 64),
        dims=list("ctzyx"),
    )
    sp = _store_path()

    write_dataarray_to_zarr(sp, array)

    back = zarr.open_array(sp, mode="r")
    assert back.shape == (1, 1, 4, 64, 64)
    assert np.array_equal(back[:], array.to_numpy())


def test_write_dataarray_to_zarr_streams_dask_arrays() -> None:
    # A larger array so rechunk actually splits it into multiple on-disk chunks.
    source = np.arange(2 * 50 * 2048 * 2048, dtype="uint16").reshape(1, 2, 50, 2048, 2048)
    array = xr.DataArray(
        da.from_array(source, chunks=(1, 1, 10, 2048, 2048)), dims=list("ctzyx")
    )
    sp = _store_path("big")

    write_dataarray_to_zarr(sp, array)

    back = zarr.open_array(sp, mode="r")
    # rechunk targets ~20MB chunks, so the z axis is split rather than written whole.
    assert back.chunks[2] < 50
    assert np.array_equal(back[:], source)


@pytest.mark.asyncio
async def test_awrite_dataarray_to_zarr_roundtrips() -> None:
    array = xr.DataArray(
        np.arange(1 * 1 * 2 * 32 * 32, dtype="float32").reshape(1, 1, 2, 32, 32),
        dims=list("ctzyx"),
    )
    sp = _store_path("async")

    await awrite_dataarray_to_zarr(sp, array)

    back = zarr.open_array(sp, mode="r")
    assert np.array_equal(back[:], array.to_numpy())


def test_array_scalars_coerce_to_ctzyx() -> None:
    # Bare numpy gets its trailing dims labelled and expanded to a 5D ctzyx layout.
    arr = ArrayLike.validate(np.zeros((4, 8, 8), dtype="uint16"))
    assert arr.value.dims == ("c", "t", "z", "y", "x")
    assert arr.value.shape == (1, 1, 4, 8, 8)

    img = ImageLike.validate(np.zeros((8, 8), dtype="uint16"))
    assert img.value.dims == ("c", "t", "z", "y", "x")
