from typing import TYPE_CHECKING, Protocol, cast
import xarray as xr
from obstore.store import S3Store
from zarr.storage import ObjectStore, StorePath
import asyncio
import zarr.api.asynchronous as async_api


if TYPE_CHECKING:
    from obstore.store import ClientConfig, RetryConfig, S3Credential
    from mikro_next.datalayer import DataLayer


class S3UploadGrantLike(Protocol):
    @property
    def access_key(self) -> str: ...

    @property
    def secret_key(self) -> str: ...

    @property
    def session_token(self) -> str: ...

    @property
    def bucket(self) -> str: ...

    @property
    def key(self) -> str: ...

    @property
    def store(self) -> object: ...


def create_s3_store(
    endpoint_url: str,
    grant: "S3UploadGrantLike",
    client_options: "ClientConfig | None" = None,
    retry_config: "RetryConfig | None" = None,
) -> S3Store:
    normalized_client_options: dict[str, object] = dict(client_options or {})
    print(grant)

    def get_credentials() -> "S3Credential":
        return {
            "access_key_id": grant.access_key,
            "secret_access_key": grant.secret_key,
            "token": grant.session_token,
            "expires_at": None,  # Obstore does not currently support expiring credentials, but this field is required by the S3Credential protocol
        }

    # Using https for S3 if the endpoint URL specifies it or it will infer based on obstore handling
    return S3Store(
        grant.bucket,
        access_key_id=grant.access_key,
        secret_access_key=grant.secret_key,
        session_token=grant.session_token,
        endpoint=endpoint_url,
        virtual_hosted_style_request=False,
        client_options={"allow_http": True},
        credential_provider=get_credentials,
    )


async def acreate_s3_store(
    grant: "S3UploadGrantLike",
    datalayer: "DataLayer",
    client_options: "ClientConfig | None" = None,
    retry_config: "RetryConfig | None" = None,
) -> S3Store:
    endpoint_url = await datalayer.get_endpoint_url()

    return create_s3_store(
        endpoint_url,
        grant,
        client_options=client_options,
        retry_config=retry_config,
    )


async def awrite_xarray_to_obstore(
    da: xr.DataArray,
    grant: "S3UploadGrantLike",
    datalayer: "DataLayer",
) -> None:
    """
    Asynchronously write an xarray dataset to S3 via obstore and Zarr.
    """
    # 1. Await the HTTP store creation using your existing async function
    obstore_s3_store = await acreate_s3_store(grant, datalayer)

    # 2. Wrap the obstore backend in Zarr's ObjectStore so Xarray can interpret it
    zarr_store = ObjectStore(obstore_s3_store)
    store_path = StorePath(zarr_store, grant.key)
    print(f"Created Zarr ObjectStore with path: {store_path}")

    # 3. Offload Xarray's synchronous write to a thread pool
    await async_api.save_array(store_path, da.to_numpy(), zarr_format=3)  # type: ignore
