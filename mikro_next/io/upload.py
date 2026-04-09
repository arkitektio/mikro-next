"""Module for uploading various data types to a DataLayer using asynchronous methods."""

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
        raise UploadError(f"Error while uploading to {s3_path} on {endpoint_url}") from e


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
            await client.put_object(Bucket=credentials.bucket, Key=credentials.key, Body=mesh.value)  # type: ignore
        except botocore.exceptions.ClientError as e:  # type: ignore
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":  # type: ignore
                return PermissionsError("Access Key is invalid, trying to get new credentials")  # type: ignore

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
            await client.put_object(Bucket=credentials.bucket, Key=credentials.key, Body=file.value)  # type: ignore
        except botocore.exceptions.ClientError as e:  # type: ignore
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":  # type: ignore
                return PermissionsError("Access Key is invalid, trying to get new credentials")  # type: ignore

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
            await client.put_object(Bucket=credentials.bucket, Key=credentials.key, Body=file.value)  # type: ignore
        except botocore.exceptions.ClientError as e:  # type: ignore
            if e.response["Error"]["Code"] == "InvalidAccessKeyId":  # type: ignore
                return PermissionsError("Access Key is invalid, trying to get new credentials")  # type: ignore

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
    return await astore_xarray_input(array, credentials, await datalayer.get_endpoint_url())


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
