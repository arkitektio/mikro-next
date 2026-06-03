"""Module for uploading various data types to a DataLayer.

Provides both async (aiobotocore/s3fs) and sync (obstore) upload paths:
    - Async: aupload_xarray, aupload_parquet, aupload_bigfile, astore_media_file, astore_mesh_file
    - Sync: upload_xarray, upload_parquet, upload_bigfile, store_media_file, store_mesh_file
"""

import logging
import os
from typing import TYPE_CHECKING
from mikro_next.scalars import ArrayLike, ImageFileLike, MeshLike, ParquetLike, FileLike
import asyncio
import s3fs  # type: ignore
from aiobotocore.session import get_session  # type: ignore
import botocore  # type: ignore
from concurrent.futures import ThreadPoolExecutor

from .errors import PermissionsError, UploadError
from zarr.storage import FsspecStore
import zarr.api.asynchronous as async_api


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from mikro_next.api.schema import (
        ZarrUploadGrant,
        ParquetUploadGrant,
        BigFileUploadGrant,
        MediaUploadGrant,
    )
    from mikro_next.datalayer import DataLayer


# ========================================================================
# Async upload functions (aiobotocore / s3fs)
# ========================================================================


async def astore_xarray_input(
    xarray: ArrayLike,
    credentials: "ZarrUploadGrant",
    endpoint_url: str,
) -> str:
    """Stores an xarray in the DataLayer"""

    os.environ["AWS_REQUEST_CHECKSUM_CALCULATION"] = (
        "when_required"  # TODO: This is a workaround for a bug in aiobotocore and s3fs https://github.com/fsspec/s3fs/issues/931
    )

    filesystem = s3fs.S3FileSystem(
        secret=credentials.secret_key,
        key=credentials.access_key,
        client_kwargs={
            "endpoint_url": endpoint_url,
            "aws_session_token": credentials.session_token,
        },
        asynchronous=True,
    )

    # random_uuid = uuid.uuid4()
    # s3_path = f"zarr/{random_uuid}.zarr"

    array = xarray.value

    s3_path = f"{credentials.bucket}/{credentials.key}"
    store = FsspecStore(filesystem, read_only=False, path=s3_path)

    try:
        logger.debug(
            f"Uploading zarr t to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        await async_api.save_array(store, array.to_numpy(), zarr_format=3)  # type: ignore
        logger.info(
            f"Successfully uploaded zarr to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )

        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to {s3_path} on {endpoint_url}"
        ) from e


def _store_parquet_input(
    parquet_input: ParquetLike,
    credentials: "ParquetUploadGrant",
    endpoint_url: str,
) -> str:
    """Stores an xarray in the DataLayer"""
    import pyarrow.parquet as pq  # type: ignore
    from pyarrow import Table  # type: ignore

    filesystem = s3fs.S3FileSystem(
        secret=credentials.secret_key,
        key=credentials.access_key,
        client_kwargs={
            "endpoint_url": endpoint_url,
            "aws_session_token": credentials.session_token,
        },
    )

    table: Table = Table.from_pandas(parquet_input.value)  # type: ignore

    s3_path = f"s3://{credentials.bucket}/{credentials.key}"
    try:
        logger.debug(
            f"Uploading parquet to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        pq.write_table(table, s3_path, filesystem=filesystem)  # type: ignore
        logger.info(
            f"Successfully uploaded parquet to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(f"Error while uploading to {s3_path}") from e


async def astore_mesh_file(
    mesh: MeshLike,
    credentials: "BigFileUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Store a mesh file in the DataLayer using presigned POST credentials."""
    from aiobotocore.session import get_session  # type: ignore
    import botocore  # type: ignore

    session = get_session()

    endpoint_url = await datalayer.get_endpoint_url()

    async with session.create_client(  # type: ignore
        "s3",
        region_name="us-west-2",
        endpoint_url=endpoint_url,
        aws_secret_access_key=credentials.secret_key,
        aws_access_key_id=credentials.access_key,
        aws_session_token=credentials.session_token,
    ) as client:
        try:
            logger.debug(
                f"Uploading mesh to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
            )
            await client.put_object(
                Bucket=credentials.bucket, Key=credentials.key, Body=mesh.value
            )  # type: ignore
        except botocore.exceptions.ClientError as e:  # type: ignore
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":  # type: ignore
                return PermissionsError(
                    "Access Key is invalid, trying to get new credentials"
                )  # type: ignore

            raise e

    logger.info(
        f"Successfully uploaded mesh to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
    )
    return credentials.store


async def astore_media_file(
    file: ImageFileLike,
    credentials: "MediaUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Store a media file in the DataLayer using presigned POST credentials."""
    """Store a mesh file in the DataLayer using presigned POST credentials."""
    from aiobotocore.session import get_session  # type: ignore
    import botocore  # type: ignore

    session = get_session()

    endpoint_url = await datalayer.get_endpoint_url()

    async with session.create_client(  # type: ignore
        "s3",
        region_name="us-west-2",
        endpoint_url=endpoint_url,
        aws_secret_access_key=credentials.secret_key,
        aws_access_key_id=credentials.access_key,
        aws_session_token=credentials.session_token,
    ) as client:
        try:
            logger.debug(
                f"Uploading file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
            )
            await client.put_object(
                Bucket=credentials.bucket, Key=credentials.key, Body=file.value
            )  # type: ignore
        except botocore.exceptions.ClientError as e:  # type: ignore
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":  # type: ignore
                return PermissionsError(
                    "Access Key is invalid, trying to get new credentials"
                )  # type: ignore

            raise e

    logger.info(
        f"Successfully uploaded file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
    )
    return credentials.store


async def aupload_bigfile(
    file: FileLike | ImageFileLike,
    credentials: "BigFileUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Store a DataFrame in the DataLayer"""
    session = get_session()

    endpoint_url = await datalayer.get_endpoint_url()

    async with session.create_client(  # type: ignore
        "s3",
        region_name="us-west-2",
        endpoint_url=endpoint_url,
        aws_secret_access_key=credentials.secret_key,
        aws_access_key_id=credentials.access_key,
        aws_session_token=credentials.session_token,
    ) as client:
        try:
            logger.debug(
                f"Uploading file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
            )
            await client.put_object(
                Bucket=credentials.bucket, Key=credentials.key, Body=file.value
            )  # type: ignore
        except botocore.exceptions.ClientError as e:  # type: ignore
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":  # type: ignore
                return PermissionsError(
                    "Access Key is invalid, trying to get new credentials"
                )  # type: ignore

            raise e

    logger.info(
        f"Successfully uploaded file to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
    )
    return credentials.store


async def aupload_xarray(
    array: ArrayLike,
    credentials: "ZarrUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Store a DataFrame in the DataLayer"""
    return await astore_xarray_input(
        array, credentials, await datalayer.get_endpoint_url()
    )


async def aupload_parquet(
    parquet: ParquetLike,
    credentials: "ParquetUploadGrant",
    datalayer: "DataLayer",
    executor: ThreadPoolExecutor,
) -> str:
    """Store a DataFrame in the DataLayer"""
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
    from mikro_next.io.obstore import create_s3_store
    from zarr.storage import ObjectStore, StorePath
    import zarr

    obstore_s3_store = create_s3_store(endpoint_url, credentials)
    zarr_store = ObjectStore(obstore_s3_store)
    store_path = StorePath(zarr_store, credentials.key)

    array = xarray.value.data

    try:
        logger.debug(
            f"Uploading zarr (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        zarr.save_array(store_path, array, zarr_format=3)  # type: ignore
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
    import obstore

    store = create_s3_store(endpoint_url, credentials)

    data = file.value.read()

    try:
        logger.debug(
            f"Uploading file (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        obstore.put(store, credentials.key, data)
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
    import obstore

    store = create_s3_store(endpoint_url, credentials)

    data = file.value.read()

    try:
        logger.debug(
            f"Uploading media file (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        obstore.put(store, credentials.key, data)
        logger.info(
            f"Successfully uploaded media file (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
        )
        return credentials.store
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e


def _store_mesh_via_obstore(
    mesh: MeshLike,
    credentials: "BigFileUploadGrant",
    endpoint_url: str,
) -> str:
    """Store a mesh file in the DataLayer synchronously via obstore."""
    from mikro_next.io.obstore import create_s3_store
    import obstore

    store = create_s3_store(endpoint_url, credentials)

    data = mesh.value.read()

    try:
        logger.debug(
            f"Uploading mesh (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}..."
        )
        obstore.put(store, credentials.key, data)
        logger.info(
            f"Successfully uploaded mesh (sync/obstore) to s3://{credentials.bucket}/{credentials.key} at {endpoint_url}"
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


def store_mesh_file(
    mesh: MeshLike,
    credentials: "BigFileUploadGrant",
    datalayer: "DataLayer",
) -> str:
    """Store a mesh file synchronously via obstore."""
    return _store_mesh_via_obstore(mesh, credentials, datalayer.endpoint_url)
