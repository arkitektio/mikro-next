"""Module for uploading various data types to a DataLayer.

Provides both async and sync upload paths via obstore:
    - Async: aupload_xarray, aupload_parquet, aupload_bigfile, astore_media_file,
      astore_fabriks_collection
    - Sync: upload_xarray, upload_parquet, upload_bigfile, store_media_file,
      store_fabriks_collection
"""

from io import BytesIO
import logging
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING
import asyncio
from concurrent.futures import ThreadPoolExecutor

import obstore
from mikro_next.scalars import (
    ArrayLike,
    FileLike,
    ImageFileLike,
    FabriksLike,
    ParquetLike,
)

from .errors import UploadError


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from mikro_next.api.schema import (
        ZarrUploadGrant,
        ParquetUploadGrant,
        BigFileUploadGrant,
        FabriksUploadGrant,
        MediaUploadGrant,
    )
    from mikro_next.datalayer import DataLayer


# ========================================================================
# Async upload functions (obstore)
# ========================================================================


async def astore_xarray_input(
    xarray: ArrayLike,
    credentials: "ZarrUploadGrant",
    endpoint_url: str,
) -> str:
    """Stores an xarray in the DataLayer"""
    from mikro_next.io.obstore import awrite_dataarray_to_zarr, create_zarr_store_path

    array = xarray.value
    store_path = create_zarr_store_path(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading zarr t to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        await awrite_dataarray_to_zarr(store_path, array)
        logger.info(
            f"Successfully uploaded zarr to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )

        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


def _parquet_payload(value: object) -> "tuple[object, Path | None]":
    """What to hand ``obstore.put``, and the scratch file to delete afterwards.

    Four inputs, three shapes of answer (see :class:`mikro_next.scalars.ParquetLike`):

    - a ``Path`` is already a parquet file, so it goes to obstore as-is — obstore reads
      it in chunks and multipart-uploads it, so a 4 GB table never enters this process;
    - a ``RecordBatchReader`` is written batch by batch to a scratch file and then
      streamed, which is the whole point of accepting one: peak memory is a batch;
    - a ``Table`` is serialized to that same scratch file rather than to a ``BytesIO``,
      because it is already the largest object in the process and a second full copy of
      it is the thing worth avoiding;
    - a ``DataFrame`` keeps the original in-memory path exactly. It is the small case,
      and routing it through a temp file would make every existing caller depend on
      writable scratch space for no gain.

    Returns:
        ``(payload, scratch)`` — ``scratch`` is None when nothing needs cleaning up.
    """
    import pyarrow.parquet as pq  # type: ignore
    from pyarrow import RecordBatchReader, Table  # type: ignore

    if isinstance(value, Path):
        return value, None

    if isinstance(value, (Table, RecordBatchReader)):
        handle, name = tempfile.mkstemp(suffix=".parquet", prefix="mikro-parquet-")
        os.close(handle)
        scratch = Path(name)
        try:
            if isinstance(value, Table):
                pq.write_table(value, scratch)
            else:
                with pq.ParquetWriter(scratch, value.schema) as writer:
                    for batch in value:
                        writer.write_batch(batch)
        except BaseException:
            # A half-written scratch file is not a parquet file, and leaving it behind
            # would be a silent disk leak on every failed upload.
            scratch.unlink(missing_ok=True)
            raise
        return scratch, scratch

    table = Table.from_pandas(value)  # type: ignore
    buffer = BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)
    return buffer, None


def _store_parquet_input(
    parquet_input: ParquetLike,
    credentials: "ParquetUploadGrant",
    endpoint_url: str,
) -> str:
    """Store a parquet table in the DataLayer via obstore."""
    from mikro_next.io.obstore import create_s3_store

    store = create_s3_store(endpoint_url, credentials)

    payload, scratch = _parquet_payload(parquet_input.value)

    s3_path = f"s3://{credentials.bucket}/{credentials.key}"
    try:
        logger.debug(
            f"Uploading parquet to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        obstore.put(store, credentials.key, payload)
        logger.info(
            f"Successfully uploaded parquet to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(f"Error while uploading to {s3_path}") from e
    finally:
        if scratch is not None:
            scratch.unlink(missing_ok=True)


async def astore_fabriks_collection(
    collection: FabriksLike,
    credentials: "FabriksUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Write a fabriks collection into the granted prefix, and return the store it landed in.

    A whole tree rather than one object -- ``fabriks.json``, both catalogs and a part file per
    octree level -- which is why the grant covers a prefix and permits reading and deleting
    inside it. The ordering is fabriks's and is load-bearing: every file the manifest names is
    written before the manifest is, so a prefix without one is an interrupted write rather than
    a collection. ``finishFabriksUpload`` is the other half of that protocol -- it reads the
    manifest and refuses a prefix that has none -- so nothing here retries or reorders the
    write; the writer owns it.

    ``awrite_collection`` does the whole write in a worker thread, since Parquet serialization
    is CPU-bound and obstore's ``put`` releases the GIL -- which also keeps the manifest-last
    ordering trivially true rather than a scheduling question.
    """
    from fabriks import awrite_collection

    from mikro_next.io.obstore import create_s3_store

    endpoint_url = await datalayer.get_endpoint_url()
    store = create_s3_store(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading fabriks collection to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        manifest = await awrite_collection(collection.value, store, credentials.key)
        logger.info(
            f"Successfully uploaded fabriks collection to s3://{credentials.bucket}/{credentials.key} "
            f"at {endpoint_url} ({manifest.counts})"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


async def astore_media_file(
    file: ImageFileLike,
    credentials: "MediaUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Store a media file in the DataLayer asynchronously via obstore."""
    from mikro_next.io.obstore import create_s3_store

    endpoint_url = await datalayer.get_endpoint_url()
    store = create_s3_store(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        await obstore.put_async(store, credentials.key, file.value)
        logger.info(
            f"Successfully uploaded file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


async def aupload_bigfile(
    file: FileLike | ImageFileLike,
    credentials: "BigFileUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Upload a big file to the DataLayer asynchronously via obstore."""
    from mikro_next.io.obstore import create_s3_store

    endpoint_url = await datalayer.get_endpoint_url()
    store = create_s3_store(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        await obstore.put_async(store, credentials.key, file.value)
        logger.info(
            f"Successfully uploaded file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


async def aupload_xarray(
    array: ArrayLike,
    credentials: "ZarrUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Upload an xarray to the DataLayer asynchronously via obstore."""
    return await astore_xarray_input(array, credentials, await datalayer.get_endpoint_url())


async def aupload_parquet(
    parquet: ParquetLike,
    credentials: "ParquetUploadGrant",
    datalayer: "DataLayer",
    executor: ThreadPoolExecutor,
) -> str:
    """Upload a parquet table to the DataLayer asynchronously via a thread executor."""
    co_future = executor.submit(
        _store_parquet_input, parquet, credentials, await datalayer.get_endpoint_url()
    )
    return await asyncio.wrap_future(co_future)


# ========================================================================
# Sync upload functions (obstore)
# ========================================================================


def _store_xarray_via_obstore(
    xarray: ArrayLike,
    credentials: "ZarrUploadGrant",
    endpoint_url: str,
) -> str:
    """Stores an xarray in the DataLayer synchronously via obstore/zarr."""
    from mikro_next.io.obstore import create_zarr_store_path, write_dataarray_to_zarr

    store_path = create_zarr_store_path(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading zarr (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        write_dataarray_to_zarr(store_path, xarray.value)
        logger.info(
            f"Successfully uploaded zarr (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


def _store_bigfile_via_obstore(
    file: FileLike | ImageFileLike,
    credentials: "BigFileUploadGrant",
    endpoint_url: str,
) -> str:
    """Store a big file in the DataLayer synchronously via obstore."""
    from mikro_next.io.obstore import create_s3_store

    store = create_s3_store(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading file (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        obstore.put(store, credentials.key, file.value)
        logger.info(
            f"Successfully uploaded file (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


def _store_media_file_via_obstore(
    file: ImageFileLike,
    credentials: "MediaUploadGrant",
    endpoint_url: str,
) -> str:
    """Store a media file in the DataLayer synchronously via obstore."""
    from mikro_next.io.obstore import create_s3_store

    store = create_s3_store(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading media file (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        obstore.put(store, credentials.key, file.value)
        logger.info(
            f"Successfully uploaded media file (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


def store_fabriks_collection(
    collection: FabriksLike,
    credentials: "FabriksUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Write a fabriks collection into the granted prefix synchronously.

    The same write as :func:`astore_fabriks_collection` -- fabriks's writer is synchronous and the
    async path is it in a worker thread -- so this is the writer itself rather than a second
    implementation of it.
    """
    from fabriks import write_collection

    from mikro_next.io.obstore import create_s3_store

    endpoint_url = datalayer.endpoint_url
    store = create_s3_store(endpoint_url, credentials)

    try:
        logger.debug(
            f"Uploading fabriks collection to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        manifest = write_collection(collection.value, store, credentials.key)
        logger.info(
            f"Successfully uploaded fabriks collection to s3://{credentials.bucket}/{credentials.key} "
            f"at {endpoint_url} ({manifest.counts})"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


def upload_xarray(
    array: ArrayLike,
    credentials: "ZarrUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Upload an xarray synchronously via obstore."""
    return _store_xarray_via_obstore(array, credentials, datalayer.endpoint_url)


def upload_parquet(
    parquet: ParquetLike,
    credentials: "ParquetUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Upload a parquet file synchronously."""
    return _store_parquet_input(parquet, credentials, datalayer.endpoint_url)


def upload_bigfile(
    file: FileLike | ImageFileLike,
    credentials: "BigFileUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Upload a big file synchronously via obstore."""
    return _store_bigfile_via_obstore(file, credentials, datalayer.endpoint_url)


def store_media_file(
    file: ImageFileLike,
    credentials: "MediaUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Store a media file synchronously via obstore."""
    return _store_media_file_via_obstore(file, credentials, datalayer.endpoint_url)
