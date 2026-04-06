import zarr.storage
import asyncio
from mikro_next.api.schema import (
    ZarrAccessGrant,
    arequest_zarr_access,
    arequest_parquet_access,
    arequest_bigfile_access,
    ParquetAccessGrant,
    BigFileAccessGrant,
)
from mikro_next.datalayer import DataLayer, current_next_datalayer
import s3fs  # type: ignore
from koil import unkoil
import zarr
import aiohttp
from pathlib import Path
from typing import Tuple
from typing import TYPE_CHECKING

from rath.scalars import ID

if TYPE_CHECKING:
    import pyarrow.parquet as pq  # type: ignore


async def aget_zarr_credentials_and_endpoint(
    store: str,
) -> Tuple[ZarrAccessGrant, str]:
    datalayer = current_next_datalayer.get()
    if not datalayer:
        raise ValueError("Datalayer is not set")
    credentials = await arequest_zarr_access(ID.validate(store))

    endpoint_url = await datalayer.get_endpoint_url()
    return credentials, endpoint_url


async def aget_table_credentials_and_endpoint(
    store: str,
) -> Tuple[ParquetAccessGrant, str]:
    datalayer = current_next_datalayer.get()
    if not datalayer:
        raise ValueError("Datalayer is not set")

    credentials = await arequest_parquet_access(ID.validate(store))
    endpoint_url = await datalayer.get_endpoint_url()
    return credentials, endpoint_url


async def aget_bigfile_credentials_and_endpoint(
    store: str,
) -> Tuple[BigFileAccessGrant, str]:
    datalayer = current_next_datalayer.get()
    if not datalayer:
        raise ValueError("Datalayer is not set")

    credentials = await arequest_bigfile_access(ID.validate(store))
    endpoint_url = await datalayer.get_endpoint_url()
    return credentials, endpoint_url


async def aopen_zarr_store(store_id: str, cache: int = 2**30):
    credentials, endpoint_url = await aget_zarr_credentials_and_endpoint(store_id)

    _s3fs = s3fs.S3FileSystem(
        secret=credentials.secret_key,
        key=credentials.access_key,
        client_kwargs={
            "endpoint_url": endpoint_url,
            "aws_session_token": credentials.session_token,
        },
        asynchronous=True,
    )

    return zarr.storage.FsspecStore(
        _s3fs, read_only=False, path=f"{credentials.bucket}/{credentials.key}"
    )


def open_zarr_store(store_id: str, cache: int = 2**30):
    credentials, endpoint_url = unkoil(aget_zarr_credentials_and_endpoint, store_id)

    _s3fs = s3fs.S3FileSystem(
        secret=credentials.secret_key,
        key=credentials.access_key,
        client_kwargs={
            "endpoint_url": endpoint_url,
            "aws_session_token": credentials.session_token,
        },
        asynchronous=True,
    )
    return zarr.storage.FsspecStore(
        _s3fs, read_only=False, path=f"{credentials.bucket}/{credentials.key}"
    )


async def aopen_parquet_filesytem(store_id: str):
    try:
        import pyarrow.parquet as pq  # type: ignore
    except ImportError as e:
        raise ImportError("You need to install pyarrow to use this function") from e
    credentials, endpoint_url = await aget_table_credentials_and_endpoint(store_id)

    _s3fs = s3fs.S3FileSystem(
        secret=credentials.secret_key,
        key=credentials.access_key,
        client_kwargs={
            "endpoint_url": endpoint_url,
            "aws_session_token": credentials.session_token,
        },
        asynchronous=True,
    )

    return pq.ParquetDataset(credentials.path, filesystem=_s3fs)


def open_parquet_filesystem(store_id: str):
    try:
        import pyarrow.parquet as pq  # type: ignore
    except ImportError as e:
        raise ImportError("You need to install pyarrow to use this function") from e
    credentials, endpoint_url = unkoil(aget_table_credentials_and_endpoint, store_id)

    _s3fs = s3fs.S3FileSystem(
        secret=credentials.secret_key,
        key=credentials.access_key,
        client_kwargs={
            "endpoint_url": endpoint_url,
            "aws_session_token": credentials.session_token,
        },
        asynchronous=False,
    )

    return pq.ParquetDataset(credentials.path, filesystem=_s3fs)


def _ensure_parent_directory(file_name: str) -> None:
    parent = Path(file_name).expanduser().resolve().parent
    parent.mkdir(parents=True, exist_ok=True)


async def adownload_presigned_file(
    presigned_url: str,
    file_name: str,
    datalayer: DataLayer | None = None,
):
    datalayer = datalayer or current_next_datalayer.get()
    if not datalayer:
        raise ValueError("Datalayer is not set")

    endpoint_url = await datalayer.get_endpoint_url()
    _ensure_parent_directory(file_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint_url + presigned_url) as response:
            response.raise_for_status()
            with open(file_name, "wb") as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)

    return file_name


def download_presigned_file(
    presigned_url: str, file_name: str, datalayer: DataLayer | None = None
):
    return unkoil(
        adownload_presigned_file,
        presigned_url,
        file_name=file_name,
        datalayer=datalayer,
    )


async def adownload_file(
    store_id: str,
    file_name: str,
    datalayer: DataLayer | None = None,
):
    return await asyncio.to_thread(
        download_file,
        store_id,
        file_name,
        datalayer,
    )


def download_file(store_id: str, file_name: str, datalayer: DataLayer | None = None):
    if datalayer is not None:
        token = current_next_datalayer.set(datalayer)
    else:
        token = None

    try:
        credentials, endpoint_url = unkoil(
            aget_bigfile_credentials_and_endpoint, store_id
        )
    finally:
        if token is not None:
            current_next_datalayer.reset(token)

    _ensure_parent_directory(file_name)

    _s3fs = s3fs.S3FileSystem(
        secret=credentials.secret_key,
        key=credentials.access_key,
        client_kwargs={
            "endpoint_url": endpoint_url,
            "aws_session_token": credentials.session_token,
        },
        asynchronous=False,
    )

    _s3fs.get_file(credentials.path, file_name)  # type: ignore[reportUnknownMemberType]
    return file_name
