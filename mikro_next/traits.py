"""
Traits for mikro_next

Traits are mixins that are added to every graphql type that exists on the mikro schema.
We use them to add functionality to the graphql types that extend from the base type.

Every GraphQL Model on Mikro gets a identifier and shrinking methods to ensure the compatibliity
with arkitekt. This is done by adding the identifier and the shrinking methods to the graphql type.
If you want to add your own traits to the graphql type, you can do so by adding them in the graphql
.config.yaml file.

"""

from __future__ import annotations

"""A context manager to download the file and delete it after use"""
from collections import deque
from contextlib import contextmanager
from enum import Enum
import os
from typing import (
    Dict,
    Generator,
    List,
    Mapping,
    NamedTuple,
    NoReturn,
    Sequence,
    Type,
    TypeVar,
    Tuple,
    Protocol,
    Optional,
    Union,
)
import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, model_validator
import xarray as xr
from typing import TYPE_CHECKING, cast
from dask.array.core import from_zarr  # type: ignore
from zarr.storage import StorePath
from .scalars import ArrayCoercible, FiveDVector
from rath.scalars import ID, IDCoercible
from typing import Any
from rath.turms.utils import get_attributes_or_error
from rath.traits import FederationFetchable

_Given = TypeVar("_Given")

TwoDArray = NDArray[np.generic]
OneDArray = NDArray[np.generic]

#: A point or a stack of them: a (N,) vector, a (K, N) array, or anything
#: `np.asarray` turns into one.
PointsLike = Union[Sequence[float], Sequence[Sequence[float]], NDArray[np.generic]]


if TYPE_CHECKING:
    import duckdb
    from pyarrow.parquet import ParquetDataset  # type: ignore
    from mikro_next.api.schema import (
        HasZarrStoreAccessor,
        Image,
        RoiKind,
        Annotation,
        Axis,
        CoordinateSystem,
        CreateTransformationMutationCreatetransformationBase,
        GetCoordinateGraphQueryCoordinategraph,
        PhysicalAxisInput,
        DerivedFromInput,
        Lens,
        PlacementValidity,
        TransformInput,
        ValueRelation,
        Scene,
        ScenePolicyInput,
    )
    from mikro_next.rath import MikroNextRath

    from datetime import datetime

    #: What `create_transformation` hands back: the shared base of every edge
    #: kind the mutation can return, the catch-all included.
    CreatedTransformation = CreateTransformationMutationCreatetransformationBase


class _LivesInItsOwnGrid(Protocol):
    """A dataset: it calls the space it lives in its *intrinsic* system, because
    that space is its own pixel grid."""

    @property
    def intrinsic_system(self) -> Optional["CoordinateSystem"]:
        """The dataset's own grid."""
        ...


class _LivesInASpace(Protocol):
    """A table dataset, a mesh collection, an annotation collection: containers
    whose coordinates are given in a space they simply name."""

    @property
    def coordinate_system(self) -> Optional["CoordinateSystem"]:
        """The space this container's coordinates are given in."""
        ...


#: Anything that can be registered into a space. Structural rather than a union
#: of the concrete models, because the operation-specific variants turms
#: generates are different classes with the same shape — what matters is that
#: the source can name its space, not which query returned it.
Registrable = Union[_LivesInItsOwnGrid, _LivesInASpace, "CoordinateSystemTrait"]


_AXIS_TYPE_BY_NAME = {
    "t": "TIME",
    "time": "TIME",
    "c": "CHANNEL",
    "channel": "CHANNEL",
}


def _default_axis_type(name: str) -> str:
    """The conventional axis type for a bare axis name: ``t``/``time`` -> TIME,
    ``c``/``channel`` -> CHANNEL, everything else -> SPACE. Pass a full input
    object instead of a bare name when the convention does not apply."""
    return _AXIS_TYPE_BY_NAME.get(name.lower(), "SPACE")


class MikroFetchable(FederationFetchable):
    """A trait for Mikro Fetchable objects

    This trait allows to fetch an object from the mikro service using its ID.
    It is used to ensure that the object can be fetched from the mikro service.

    """

    @classmethod
    def get_rath(cls) -> "MikroNextRath":
        """Get the current Rath client from the context.

        Returns:
            The active mikro rath client.

        Raises:
            NoMikroFound: If no client is active.
        """
        from mikro_next.errors import NoMikroFound
        from mikro_next.rath import current_mikro_next_rath

        rath = current_mikro_next_rath.get()
        if rath is None:
            raise NoMikroFound("No rath client found in context. Please provide a rath client.")
        return rath


class HasZarrStoreTrait(BaseModel):
    """Image Trait

    Implements both identifier and shrinking methods.
    Also Implements the data attribute

    Attributes:
        data (xarray.Dataset): The data of the representation.

    """

    @property
    def data(self) -> xr.DataArray:
        """The data of this image as an xarray.DataArray"""
        from dask.array.core import Array

        store: HasZarrStoreAccessor = get_attributes_or_error(self, "store")

        array: Array = from_zarr(store.zarr_store)

        return xr.DataArray(array, dims=["c", "t", "z", "y", "x"])

    @property
    def multi_scale_data(self) -> List[xr.DataArray]:
        """The multi-scale data of this image as a list of xarray.DataArray"""
        scale_views = get_attributes_or_error(self, "derived_scale_views")

        if len(scale_views) == 0:
            raise ValueError(
                "No ScaleView found in views. Please create a ScaleView first."
            )

        sorted_views = sorted(scale_views, key=lambda image: image.scale_x)
        return [x.image.data for x in sorted_views]

    def get_pixel_size(self, stage: ID | None = None) -> Tuple[float, float, float]:
        """The pixel size of the representation

        Returns:
            Tuple[float, float, float]: The pixel size
        """
        from mikro_next.api.schema import AffineTransformationView

        views = get_attributes_or_error(self, "views")

        for view in views:
            if isinstance(view, AffineTransformationView):
                if stage is None:
                    return view.affine_matrix.as_matrix().diagonal()[:3]  # type: ignore
                else:
                    if get_attributes_or_error(view, "stage.id") == stage:
                        return view.affine_matrix.as_matrix().diagonal()[:3]  # type: ignore

        raise NotImplementedError(
            f"No pixel size found for this representation {self}. Have you attached any views?"
        )


class PhysicalSizeProtocol(Protocol):
    """A Protocol for Vectorizable data

    Attributes:
        x (float): The x value
        y (float): The y value
        z (float): The z value
        t (float): The t value
        c (float): The c value
    """

    x: float | None
    y: float | None
    z: float | None
    t: float | None
    c: float | None

    def __init__(
        self,
        x: Optional[float] = None,
        y: Optional[float] = None,
        z: Optional[float] = None,
        t: Optional[float] = None,
        c: Optional[float] = None,
    ) -> None:
        """Initialize the PhysicalSizeProtocol."""
        ...


class PhysicalSizeTrait:
    """Additional Methods for PhysicalSize"""

    def is_similar(
        self: PhysicalSizeProtocol,
        other: PhysicalSizeProtocol,
        tolerance: float = 0.02,
        raise_exception: Optional[bool] = False,
    ) -> bool:
        """Check whether this physical size is close to another within a tolerance.

        Args:
            other: The other physical size to compare against.
            tolerance: Maximum allowed absolute difference per axis.
            raise_exception: If True, raise ValueError instead of returning False.

        Returns:
            True if all non-None shared axes are within tolerance, False otherwise.
        """
        if hasattr(self, "x") and self.x is not None and other.x is not None:
            if abs(other.x - self.x) > tolerance:
                if raise_exception:
                    raise ValueError(
                        f"X values are not similar: {self.x} vs {other.x} is above tolerance {tolerance}"
                    )
                return False
        if hasattr(self, "y") and self.y is not None and other.y is not None:
            if abs(other.y - self.y) > tolerance:
                if raise_exception:
                    raise ValueError(
                        f"Y values are not similar: {self.y} vs {other.y} is above tolerance {tolerance}"
                    )
                return False
        if hasattr(self, "z") and self.z is not None and other.z is not None:
            if abs(other.z - self.z) > tolerance:
                if raise_exception:
                    raise ValueError(
                        f"Z values are not similar: {self.z} vs {other.z} is above tolerance {tolerance}"
                    )
                return False
        if hasattr(self, "t") and self.t is not None and other.t is not None:
            if abs(other.t - self.t) > tolerance:
                if raise_exception:
                    raise ValueError(
                        f"T values are not similar: {self.t} vs {other.t} is above tolerance {tolerance}"
                    )
                return False
        if hasattr(self, "c") and self.c is not None and other.c is not None:
            if abs(other.c - self.c) > tolerance:
                if raise_exception:
                    raise ValueError(
                        f"C values are not similar: {self.c} vs {other.c} is above tolerance {tolerance}"
                    )
                return False

        return True

    def to_scale(self) -> List[float]:
        """Get the scale of the physical size
        Returns:
            List[float]: The scale of the physical size
        """
        return [
            getattr(self, "t", 1),
            getattr(self, "c", 1),
            getattr(self, "z", 1),
            getattr(self, "y", 1),
            getattr(self, "x", 1),
        ]


class IsVectorizableTrait:
    """Additional Methods for ROI"""

    @property
    def vector_data(self) -> TwoDArray:
        """A numpy array of the vectors of the ROI

        Returns:
            np.ndarray: _description_
        """
        return self.get_vector_data(dims="yx")

    def get_vector_data(self, dims: str | list[str] = "yx") -> TwoDArray:
        """Get the vector data of the ROI as a numpy array"""
        vector_list = get_attributes_or_error(self, "vectors")
        assert vector_list, (
            "Please query 'vectors' in your request on 'ROI'. Data is not accessible otherwise"
        )
        vector_list: list[list[float]]

        mapper = {
            "y": 4,
            "x": 3,
            "z": 2,
            "t": 1,
            "c": 0,
        }

        return np.array([[v[mapper[ac]] for ac in dims] for v in vector_list])

    def to_slices(self) -> Tuple[slice, ...]:
        """Get the bounding box of the ROI as a tuple of slices"""
        vector_data = self.get_vector_data(dims="ctzyx")
        return tuple(
            slice(vector_data[:, i].min(), vector_data[:, i].max() + 1)
            for i in range(5)
        )

    def image_data(self) -> xr.DataArray:
        """Get the vector data of the ROI as a numpy array"""
        vector_list = get_attributes_or_error(self, "vectors")
        assert vector_list, (
            "Please query 'vectors' in your request on 'ROI'. Data is not accessible otherwise"
        )
        vector_list: list[list[float]]

        image: "Image" = get_attributes_or_error(self, "image")

        return image.data[*self.to_slices()]

    def center(self) -> FiveDVector:
        """The center of the ROI

        Caluclates the geometrical center of the ROI according to its type
        and the vectors of the ROI.

        Returns:
            InputVector: The center of the ROI
        """
        from mikro_next.api.schema import RoiKind, FiveDVector

        kind = get_attributes_or_error(self, "kind")
        if kind == RoiKind.RECTANGLE:
            return FiveDVector.validate(self.get_vector_data(dims="ctzyx").mean(axis=0))

        raise NotImplementedError(
            f"Center calculation not implemented for this ROI type {kind}"
        )

    def crop(self, data: xr.DataArray) -> xr.DataArray:
        """Crop the data to the ROI

        Args:
            data (xr.DataArray): The data to crop

        Returns:
            xr.DataArray: The cropped data
        """
        vector_data = self.get_vector_data(dims="ctzyx")
        return data.sel(  # type: ignore
            x=slice(vector_data[:, 3].min(), vector_data[:, 3].max()),
            y=slice(vector_data[:, 4].min(), vector_data[:, 4].max()),
            z=slice(vector_data[:, 2].min(), vector_data[:, 2].max()),
            t=slice(vector_data[:, 1].min(), vector_data[:, 1].max()),
            c=slice(vector_data[:, 0].min(), vector_data[:, 0].max()),
        )  # type: ignore

    def center_as_array(self) -> OneDArray:
        """The center of the ROI

        Caluclates the geometrical center of the ROI according to its type
        and the vectors of the ROI.

        Returns:
            InputVector: The center of the ROI
        """
        from mikro_next.api.schema import RoiKind

        kind = get_attributes_or_error(self, "kind")
        if kind == RoiKind.RECTANGLE:
            return self.get_vector_data(dims="ctzyx").mean(axis=0)
        if kind == RoiKind.POINT:
            return self.get_vector_data(dims="ctzyx")[0]

        raise NotImplementedError(
            f"Center calculation not implemented for this ROI kind {kind}"
        )


class HasParquestStoreTrait(BaseModel):
    """Table Trait

    Implements both identifier and shrinking methods.
    Also Implements the data attribute

    Attributes:
        data (pd.DataFrame): The data of the table.

    """

    @property
    def data(self) -> "duckdb.DuckDBPyRelation":
        """The data of this table as a lazy DuckDB relation.

        The relation queries the parquet object directly on S3 through DuckDB's
        ``httpfs`` extension, so the table is never fully downloaded into memory.
        Filter/aggregate on the relation and call ``.df()`` to materialise just
        the result into a pandas DataFrame.

        Returns:
            duckdb.DuckDBPyRelation: A lazy relation over the parquet object.
        """
        store: "HasParquetStoreAccesor" = get_attributes_or_error(self, "store")
        return store.duckdb_relation


V = TypeVar("V")


class HasZarrStoreAccessor(BaseModel):
    """Zarr Store Accessor

    Allows to access the python zarr store of
    a ZarrStore object.


    """

    _openstore: Any = None

    @property
    def zarr_store(self) -> StorePath:
        """The zarr store of the ZarrStore object"""
        from mikro_next.io.download import open_zarr_store

        if self._openstore is None:
            id = get_attributes_or_error(self, "id")
            self._openstore = open_zarr_store(id)
        return self._openstore


class HasParquetStoreAccesor(BaseModel):
    """Parquet Store Accessor"""

    _dataset: Any = None
    _duckdb_con: Any = None
    _duckdb_rel: Any = None

    @property
    def parquet_dataset(self) -> "ParquetDataset":
        """The Parquet Dataset of the ParquetStore object"""
        from mikro_next.io.download import open_parquet_filesystem

        if self._dataset is None:
            id = get_attributes_or_error(self, "id")
            self._dataset = open_parquet_filesystem(id)
        return self._dataset

    @property
    def duckdb_relation(self) -> "duckdb.DuckDBPyRelation":
        """A lazy DuckDB relation over the parquet object, queried directly on S3.

        Reads through DuckDB's ``httpfs`` extension so the object is never fully
        downloaded. The backing connection is cached for the lifetime of this
        accessor (the relation is only valid while its connection is alive).
        """
        from mikro_next.io.download import open_parquet_duckdb

        if self._duckdb_rel is None:
            id = get_attributes_or_error(self, "id")
            self._duckdb_con, self._duckdb_rel = open_parquet_duckdb(id)
        return self._duckdb_rel


class HasDownloadAccessor(BaseModel):
    """Download Accessor"""

    _dataset: Any = None

    def download(self, file_name: str | None = None) -> "str":
        """Download the file from the backing store.

        Args:
            file_name (str | None): The name of the file to save the downloaded file as
                If None, the key from the store will be used as the file name.
        Returns:
            str: The path to the downloaded file
        """
        from mikro_next.io.download import download_file

        store_id, key = get_attributes_or_error(self, "id", "key")
        return download_file(store_id, file_name=file_name or key)


class HasPresignedDownloadAccessor(BaseModel):
    """Presigned Download Accessor

    TODO: THis should probablry bre refactored to a more generic download accessor

    """

    _dataset: Any = None

    def download(self, file_name: str | None = None) -> str:
        """Download the file from the presigned URL

        Args:
            file_name (str | None): The name of the file to save the downloaded file as
                If None, the key from the presigned URL will be used as the file name.
        Returns:
            str: The path to the downloaded file
        """
        from mikro_next.io.download import download_presigned_file

        url, key = get_attributes_or_error(self, "presigned_url", "key")
        return download_presigned_file(url, file_name=file_name or key)


class Vector(Protocol):
    """A Protocol for Vectorizable data

    Attributes:
        x (float): The x value
        y (float): The y value
        z (float): The z value
        t (float): The t value
        c (float): The c value
    """

    x: float
    y: float
    z: float
    t: float
    c: float

    def __init__(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        z: Optional[int] = None,
        t: Optional[int] = None,
        c: Optional[int] = None,
    ) -> None: ...


T = TypeVar("T", bound=Vector)


class HasPixelSizeTrait:
    """Mixin for PixelTranslatable data"""

    @property
    def pixel_size(self) -> Tuple[float, float, float]:
        """The pixel size of the representation

        Returns:
            Tuple[float, float, float]: The pixel size
        """
        kind, matrix = get_attributes_or_error(self, "kind", "matrix")

        if kind == "AFFINE":
            return tuple(np.array(matrix).reshape(4, 4).diagonal()[:3])

        raise NotImplementedError(f"Pixel size not implemented for this kind {kind}")

    @property
    def position(self) -> Tuple[float, float, float]:
        """The pixel size of the representation

        Returns:
            Tuple[float, float, float]: The pixel size
        """
        kind, matrix = get_attributes_or_error(self, "kind", "matrix")

        if kind == "AFFINE":
            return tuple(np.array(matrix).reshape(4, 4)[:3, 3])

        raise NotImplementedError(f"Pixel size not implemented for this kind {kind}")


class HasFromNumpyArrayTrait:
    """Mixin for Vectorizable data
    adds functionality to convert a numpy array to a list of vectors
    """

    @classmethod
    def list_from_numpyarray(
        cls: Type[T],
        x: TwoDArray,
        t: Optional[int] = None,
        c: Optional[int] = None,
        z: Optional[int] = None,
    ) -> List[T]:
        """Creates a list of InputVector from a numpya array

        Args:
            vector_list (List[List[float]]): A list of lists of floats

        Returns:
            List[Vectorizable]: A list of InputVector
        """
        assert x.ndim == 2, "Needs to be a List array of vectors"
        if x.shape[1] == 4:
            return [cls(x=i[1], y=i[0], z=i[2], t=i[3], c=c) for i in x.tolist()]
        if x.shape[1] == 3:
            return [cls(x=i[1], y=i[0], z=i[2], t=t, c=c) for i in x.tolist()]
        elif x.shape[1] == 2:
            return [cls(x=i[1], y=i[0], t=t, c=c, z=z) for i in x.tolist()]
        else:
            raise NotImplementedError(
                f"Incompatible shape {x.shape} of {x}. List dimension needs to either be of size 2 or 3"
            )

    @classmethod
    def from_array(
        cls: Type[T],
        x: OneDArray,
    ) -> T:
        """Creates a InputVector from a numpy array"""
        assert x.ndim == 1, "Needs to be a 1D array of floats"
        return cls(x=x[4], y=x[3], z=x[2], t=x[1], c=x[0])


class FileTrait:
    """A trait for file-like objects that can be downloaded
    because they have a big file store attached to them.
    """

    def download(self, file_name: str | None = None) -> "str":
        """Download the file from the store

        Args:
            file_name (str | None): The name of the file to save the downloaded file as
                If None, the key from the store will be used as the file name.
        Returns:
            str: The path to the downloaded file
        """
        store: "HasPresignedDownloadAccessor" = get_attributes_or_error(self, "store")
        return store.download(file_name=file_name)

    @contextmanager
    def temporary(self) -> Generator[str, None, None]:
        """Download the file and yield its local path, deleting it on exit."""
        path = None
        try:
            path = self.download()
            yield path
        finally:
            if path and os.path.exists(path):
                os.remove(path)


class DataArrayTrait:
    """A trait for dataset-like objects that can be downloaded"""

    @property
    def data(self) -> xr.DataArray:
        """The data of this dataset as an xarray.DataArray"""
        store: HasZarrStoreAccessor = get_attributes_or_error(self, "store")
        array = from_zarr(store.zarr_store)
        return xr.DataArray(array)


class DatasetTrait:
    """A trait for dataset-like objects that can be downloaded
    because they have a big file store attached to them.
    """

    def level_data(self, level: int = 0) -> xr.DataArray:
        """One pyramid level of this dataset, with its axes named.

        Level 0 is the full-resolution array; higher levels are coarser.
        """
        arrays = get_attributes_or_error(self, "data_arrays")
        dims = get_attributes_or_error(self, "axis_names")
        for array in arrays:
            if array.level == level:
                return xr.DataArray(from_zarr(array.store.zarr_store), dims=list(dims))
        raise ValueError(
            f"This dataset has no pyramid level {level}. Available levels: "
            f"{sorted(a.level for a in arrays)}"
        )

    def multi_scale_data(self) -> List[xr.DataArray]:
        """Every pyramid level of this dataset, finest first."""
        arrays = get_attributes_or_error(self, "data_arrays")
        dims = get_attributes_or_error(self, "axis_names")
        return [
            xr.DataArray(from_zarr(array.store.zarr_store), dims=list(dims))
            for array in sorted(arrays, key=lambda a: a.level)
        ]

    @property
    def data(self) -> xr.DataArray:
        """This dataset's full-resolution array, with its axes named."""
        return self.level_data(0)

    def calibrate(
        self,
        axes: Union[Mapping[str, Tuple[float, str]], Sequence["PhysicalAxisInput"]],
        *,
        name: str = "physical",
        scale: Optional[Sequence[float]] = None,
        translation: Optional[Sequence[float]] = None,
        affine: Optional[Sequence[Sequence[float]]] = None,
        epoch: Optional["datetime"] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> "CoordinateSystem":
        """Give this dataset a physical size: a coordinate system carrying the
        units, and the edge registering the dataset's pixel grid into it.

        The primary form takes a mapping of every intrinsic axis name to a
        (factor, unit) pair, e.g. ``{"z": (0.5, "micrometer"), "y": (0.2,
        "micrometer"), "x": (0.2, "micrometer")}`` — axis name and type are
        copied from the intrinsic axis, and the factors become the edge's SCALE.
        Pass ``translation`` as well (a stage position, say) and the two fold
        into a single AFFINE, because an edge answers to exactly one kind.
        Power users can pass a sequence of ``PhysicalAxisInput`` directly,
        together with exactly one of ``scale=`` or ``affine=``.

        A physical space is not a kind of thing a dataset owns — it is an
        ordinary coordinate system with an edge into it — so this is one call,
        authored as one registration, rather than sugar on ingest:

            dataset.calibrate({d: (0.2, "micrometer") for d in "zyx"})

        Returns:
            The created coordinate system. The edge is authored with it.
        """
        from mikro_next.api.schema import (
            create_coordinate_system,
            PhysicalAxisInput,
            RegistrationPathInput,
        )

        intrinsic = get_attributes_or_error(self, "intrinsic_system")
        if intrinsic is None:
            raise ValueError(
                "This dataset has no intrinsic coordinate system to calibrate from"
            )

        intrinsic_axes = sorted(
            get_attributes_or_error(intrinsic, "axes"), key=lambda a: a.order
        )

        if isinstance(axes, Mapping):
            intrinsic_names = [a.name for a in intrinsic_axes]
            if set(axes) != set(intrinsic_names):
                raise ValueError(
                    f"The calibration must cover every intrinsic axis exactly: "
                    f"intrinsic axes are {intrinsic_names}, got {sorted(axes)}"
                )
            factors = [float(axes[a.name][0]) for a in intrinsic_axes]
            calibrated_axes = [
                PhysicalAxisInput(
                    name=a.name,
                    type=a.type,
                    unit=axes[a.name][1],
                    long_name=a.long_name,
                )
                for a in intrinsic_axes
            ]
            if affine is not None:
                if any(f != 1.0 for f in factors):
                    raise ValueError(
                        "When passing an explicit affine, all per-axis factors must "
                        "be 1.0 — otherwise the scaling would be applied twice"
                    )
                scale = None
            elif scale is not None:
                raise ValueError(
                    "Pass the factors in the axes mapping, not via scale=, when "
                    "using the mapping form"
                )
            else:
                scale = factors
        else:
            calibrated_axes = list(axes)
            if (scale is None) == (affine is None):
                raise ValueError(
                    "When passing PhysicalAxisInput objects directly, pass exactly "
                    "one of scale= or affine="
                )

        # One edge, one kind: a pixel size plus an offset is a single AFFINE, not
        # two stacked sugar fields.
        kind, scale, translation, affine = _infer_transform_kind(
            scale, translation, affine, None
        )

        registration: Dict[str, Any] = {
            "dataset": get_attributes_or_error(self, "id"),
            "name": f"{getattr(self, 'name', 'dataset')} -> {name}",
        }
        transform = _transform_member(
            kind, scale=scale, translation=translation, affine=affine
        )
        if transform is not None:
            registration["transform"] = transform

        kwargs: Dict[str, Any] = {}
        if epoch is not None:
            kwargs["epoch"] = epoch

        return create_coordinate_system(
            name=name,
            axes=calibrated_axes,
            registrations=[RegistrationPathInput(**registration)],
            rath=rath,
            **kwargs,
        )

    def lens(
        self,
        rath: Optional["MikroNextRath"] = None,
        **selections: Union[int, slice, Tuple[int, ...], Sequence[Optional[int]]],
    ) -> "Lens":
        """Create a lens on this dataset from pythonic per-axis selections.

        With no selections the lens frames the whole dataset — the tail every
        derivation edge starts from. Each keyword names an axis and selects
        along it: an ``int`` pins one index (a slice of size 1), a
        ``(start, stop)`` or ``(start, stop, step)`` tuple and a ``slice()``
        object select a range.

        ``crop.lens(z=16, y=32)`` is the row through (z=16, y=32);
        ``source.lens(x=(0, 128))`` is the left half.
        """
        from mikro_next.api.schema import create_lens, SliceInput

        axis_names = getattr(self, "axis_names", None)
        slices: List[SliceInput] = []
        for axis, selection in selections.items():
            if axis_names is not None and axis not in axis_names:
                raise ValueError(
                    f"Invalid axis {axis!r} for dataset with axes {list(axis_names)}"
                )
            if isinstance(selection, bool):
                raise TypeError(f"Invalid selection for axis {axis!r}: {selection!r}")
            if isinstance(selection, int):
                slices.append(
                    SliceInput(axis=axis, start=selection, stop=selection + 1)
                )
            elif isinstance(selection, slice):
                slices.append(
                    SliceInput(
                        axis=axis,
                        start=selection.start,
                        stop=selection.stop,
                        step=selection.step,
                    )
                )
            elif isinstance(selection, (tuple, list)) and 2 <= len(selection) <= 3:
                slices.append(
                    SliceInput(
                        axis=axis,
                        start=selection[0],
                        stop=selection[1],
                        step=selection[2] if len(selection) == 3 else None,
                    )
                )
            else:
                raise TypeError(
                    f"Invalid selection for axis {axis!r}: {selection!r}. Pass an "
                    f"int, a slice(), or a (start, stop[, step]) tuple"
                )

        return create_lens(
            dataset=get_attributes_or_error(self, "id"), slices=slices, rath=rath
        )

    def key_table(
        self,
        table: "Registrable",
        *,
        name: Optional[str] = None,
        validity: Optional["PlacementValidity"] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> "CreatedTransformation":
        """Register this label dataset's voxels as the FIELD edge keying `table`.

        A label mask is exactly the case where the array being mapped is the
        array doing the mapping: its pixels consume this dataset's axes and
        produce the table's coordinate axis (the object ids), so this dataset's
        intrinsic system is both the edge's input and its field. The edge is
        many-to-one on purpose — an object is a set of voxels — and is never
        walked backwards.

        For a table that does not exist yet, prefer ``create_table_dataset``'s
        ``keyed_by=[KeyedByInput(dataset=mask.id)]``: it says the same thing in
        the call that creates the table, so the pair is atomic, and the server
        derives the consumed and produced axes from the two spaces rather than
        taking them on trust. This method is the standalone form, for keying a
        table that already exists.

        Args:
            table: The table dataset keyed by these labels (anything with a
                ``coordinate_system``), or that coordinate system directly.
            name: An optional name for the edge.
            validity: An optional PlacementValidity for the edge.

        Returns:
            The created FIELD transformation.
        """
        from mikro_next.api.schema import create_transformation

        # The mixin has no fields of its own; the model it is mixed into has
        # `intrinsic_system`, which is what makes a dataset registrable.
        intrinsic = _space_of(cast("Registrable", self))

        target = _space_of(table)
        if getattr(target, "axes", None) is None:
            raise ValueError(
                "key_table needs the table's coordinate system with its axes "
                "selected in the query to order the output axes"
            )

        kwargs: Dict[str, Any] = {}
        if name is not None:
            kwargs["name"] = name
        if validity is not None:
            kwargs["validity"] = validity

        # Only IDENTITY has no member input, so a FIELD edge always builds one —
        # the return type just cannot say which kind it was asked for.
        transform = _transform_member(
            "FIELD",
            field=get_attributes_or_error(intrinsic, "id"),
            input_axes=_axis_names_in_order(intrinsic),
            output_axes=_axis_names_in_order(target),
        )
        assert transform is not None

        return create_transformation(
            input=get_attributes_or_error(intrinsic, "id"),
            output=get_attributes_or_error(target, "id"),
            transform=transform,
            rath=rath,
            **kwargs,
        )


class CreateADatasetTrait:
    """Validation trait for the generic ``create_a_dataset`` input.

    Unlike the classic image path, the dataset path lets the user supply an
    arbitrarily-labelled array. This trait enforces that the labels are coherent
    at the model level: every dimension of the ``data`` array must have exactly
    one matching ``axis`` (by name), and every scale's array must share that same
    set of dimensions.
    """

    @model_validator(mode="after")
    def _validate_dims_match_axes(self) -> "CreateADatasetTrait":
        """Ensure the axes (and scale arrays) match the data array dims."""
        data = getattr(self, "data", None)
        axes = getattr(self, "axes", None)
        if data is None or axes is None:
            return self

        array = getattr(data, "value", data)
        array_dims = tuple(str(dim) for dim in array.dims)
        axis_names = tuple(axis.name for axis in axes)

        if set(array_dims) != set(axis_names):
            raise ValueError(
                f"axes {axis_names} do not match the data array dimensions "
                f"{array_dims}. Every array dimension must have exactly one "
                f"matching axis (and vice versa)."
            )

        for scale in getattr(self, "scales", ()) or ():
            scale_array = getattr(getattr(scale, "array", None), "value", None)
            if scale_array is None:
                continue
            scale_dims = tuple(str(dim) for dim in scale_array.dims)
            if set(scale_dims) != set(array_dims):
                raise ValueError(
                    f"Scale level {getattr(scale, 'level', '?')} array dimensions "
                    f"{scale_dims} do not match the data array dimensions {array_dims}."
                )

        return self


class RGBAColorInputTrait(BaseModel):
    """Completes a colour to RGBA, and rejects one that cannot be completed.

    The server takes ``color`` as exactly four components — red, green, blue,
    alpha — but the field arrives here as a bare ``[Int!]``, so nothing in the
    generated model says so and a three-component colour travels all the way to
    the backend before being refused. Writing ``(0, 255, 255)`` for cyan is the
    obvious thing to write, and the round trip is a poor way to find out it is
    wrong.

    So a three-component colour is completed with an opaque alpha, which is what
    the caller meant, and anything else fails here with the length it actually
    had::

        TransferFunctionInput(color=(0, 255, 255))       # -> (0, 255, 255, 255)
        TransferFunctionInput(color=(0, 255, 255, 128))  # left alone
        TransferFunctionInput(color=(0, 255))            # ValueError

    Alpha is 255 rather than 1.0 because these components are 0-255 integers;
    ``mikro_next.scalars.RGBAColor`` completes with 1.0 for the same reason, its
    components being floats. That scalar is not what validates this field —
    nothing in the schema is typed ``RGBAColor`` — which is why this exists.
    """

    @model_validator(mode="before")
    @classmethod
    def _complete_rgba(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        color = value.get("color")
        if color is None or isinstance(color, (str, bytes)):
            return value
        try:
            components = [int(c) for c in color]
        except TypeError:
            return value  # not a sequence; let the field's own validation speak
        if len(components) == 3:
            components.append(255)
        elif len(components) != 4:
            raise ValueError(
                f"color is an RGBA colour, so it takes 3 components (alpha is "
                f"completed to 255) or 4, but got {len(components)}: {list(color)}"
            )
        return {**value, "color": components}


class AxisInputTrait(BaseModel):
    """Lets a structural axis be given as a bare name.

    ``axes=["z", "y", "x"]`` is enough for the common case: the axis type is
    inferred from the name (``t`` -> TIME, ``c`` -> CHANNEL, everything else
    SPACE). Pass a full ``AxisInput`` for anything the convention gets wrong.
    """

    @model_validator(mode="before")
    @classmethod
    def _coerce_bare_name(cls, value: Any) -> Any:
        if isinstance(value, str):
            return {"name": value, "type": _default_axis_type(value)}
        return value


class ValueHistogramInputTrait(BaseModel):
    """Builds the render metadata of an array in one call."""

    @classmethod
    def from_array(cls, array: ArrayCoercible, bins: int = 256) -> "ValueHistogramInputTrait":
        """Robust min/max, a 1st/99th-percentile contrast window and a UI
        histogram, computed from the array itself.

        The percentiles ignore hot/dead pixels so the default contrast sliders
        land somewhere sensible; compute on the base-resolution array.

        Args:
            array: Anything ``np.asarray`` accepts (numpy, xarray, dask).
            bins: The number of histogram bins.
        """
        clean = np.asarray(array)
        clean = clean[np.isfinite(clean)]
        if clean.size == 0:
            raise ValueError(
                "Cannot build a value histogram of an array with no finite values"
            )
        lo, hi = float(clean.min()), float(clean.max())
        p1, p99 = np.percentile(clean, [1, 99])
        counts, edges = np.histogram(clean, bins=bins, range=(lo, hi))
        return cls(
            min=lo,
            max=hi,
            p1=float(p1),
            p99=float(p99),
            bins=edges.tolist(),
            histogram=counts.tolist(),
        )


class CoordinateAnchorInputTrait(BaseModel):
    """Convenience constructors for coordinate anchors."""

    @classmethod
    def histogram_anchor(
        cls,
        array: ArrayCoercible,
        dims: Optional[Sequence[str]] = None,
        bins: int = 256,
        at: Optional[Mapping[str, int]] = None,
    ) -> "CoordinateAnchorInputTrait":
        """An anchor carrying the array's value histogram.

        A histogram is a single fact about the array it was computed from, so it
        hangs off one point rather than being repeated per position. By default
        that point is the origin — voxel (0, ..., 0) — which is what a histogram
        of the whole array wants.

        Pass ``at`` to say the fact is about one position instead: the usual case
        is one contrast window per channel, where each anchor is keyed by the
        channel it describes and the array handed in is that channel's slice::

            [CoordinateAnchorInput.histogram_anchor(arr.isel(c=i), at={"c": i})
             for i in range(arr.sizes["c"])]

        Args:
            array: The array to summarise. An ``xr.DataArray`` brings its own
                dims; anything else needs ``dims`` spelled out.
            dims: The axis names to pin at 0, in array order. Ignored when ``at``
                is given.
            bins: The number of histogram bins.
            at: Axis name -> position this anchor sits at.
        """
        from mikro_next.api.schema import AxisAnchorInput, ValueHistogramInput

        if at is not None:
            anchors = [
                AxisAnchorInput(axis=str(axis), value=int(value))
                for axis, value in at.items()
            ]
        else:
            if dims is None:
                dims = getattr(array, "dims", None)
                if dims is None:
                    raise ValueError(
                        "dims= is required when the array does not carry its own "
                        "dimension names (pass an xr.DataArray, or spell them out)"
                    )
            anchors = [AxisAnchorInput(axis=str(d), value=0) for d in dims]

        return cls(
            axis_anchors=anchors,
            value_histogram=ValueHistogramInput.from_array(array, bins=bins),
        )

    @classmethod
    def histogram_anchors(
        cls,
        # Narrower than its siblings on purpose: this one splits along a *named*
        # axis, so it needs an array that carries its own dimension names.
        array: xr.DataArray,
        axis: str = "c",
        bins: int = 256,
    ) -> List["CoordinateAnchorInputTrait"]:
        """One histogram anchor per position along ``axis`` — the whole
        ``anchors=`` argument in one call.

        A contrast window is per channel: a nuclear stain and a brightfield
        channel in the same stack share no sensible range, so one histogram over
        both describes neither. Each anchor is therefore computed from just that
        position's slice and keyed by it, which is what gives the frontend a
        usable default slider per channel.

        When the array has no such axis there is nothing to split on, so this
        falls back to a single anchor at the origin covering the whole array —
        meaning callers do not have to branch on whether the data has channels::

            anchors=CoordinateAnchorInput.histogram_anchors(arr)

        Args:
            array: An ``xr.DataArray`` to summarise.
            axis: The axis to produce one anchor per position of.
            bins: The number of histogram bins.
        """
        dims = getattr(array, "dims", None)
        if dims is None:
            raise ValueError(
                "histogram_anchors needs an array carrying its own dimension "
                "names (pass an xr.DataArray)"
            )
        if axis not in dims:
            return [cls.histogram_anchor(array, bins=bins)]
        return [
            cls.histogram_anchor(array.isel({axis: index}), bins=bins, at={axis: index})
            for index in range(array.sizes[axis])
        ]


class Lensable:
    """A trait for file-like objects that can be downloaded
    because they have a big file store attached to them.
    """

    @property
    def data(self) -> xr.DataArray:
        """Download the file from the store

        Args:
            file_name (str | None): The name of the file to save the downloaded file as
                If None, the key from the store will be used as the file name.
        Returns:
            str: The path to the downloaded file
        """
        from mikro_next.api.schema import Slice

        store: "DatasetTrait" = get_attributes_or_error(self, "dataset")
        slices: List[Slice] = get_attributes_or_error(self, "slices")

        data = store.data

        for lens_slice in slices:
            if lens_slice.axis not in data.dims:
                raise ValueError(
                    f"Invalid slice dimension {lens_slice.axis} for data with dimensions {data.dims}"
                )
            if lens_slice.start is None and lens_slice.stop is None:
                continue

            data = data.isel(
                {
                    lens_slice.axis: slice(
                        lens_slice.start,
                        lens_slice.stop,
                        lens_slice.step,
                    )
                }
            )  # type: ignore

        return data

    def draw(
        self,
        kind: "RoiKind",
        vectors: "TwoDArray",
        name: str | None = None,
        collection: str | None = None,
        scene: str | None = None,
    ) -> "Annotation":
        """Draw an annotation on the data of this lens

        The vectors are interpreted in the lens' own coordinate system, which already
        encodes the crop and step of its slices, so no dimension mapping is needed.
        Categorical axes that the lens pins to a single index (a channel) become
        pinned coordinates on the annotation.

        The annotation is drawn into `collection` or onto `scene` (at most one of
        the two). If neither is given, a new annotation collection is created on
        the lens' coordinate system.

        Args:
            kind (RoiKind): The kind of the annotation to draw
            vectors (TwoDArray): A 2D array of vectors to draw the annotation with. The last
                dimension needs to be of size 3 and represent the z, y, x values of the vectors.
            name (str | None): An optional name for the annotation
            collection (str | None): The ID of the annotation collection to draw into
            scene (str | None): The ID of the scene to draw onto

        Returns:
            Annotation: The drawn annotation
        """
        from mikro_next.api.schema import (
            AxisType,
            create_annotation,
            create_annotation_collection,
            CoordinateInput,
            Slice,
        )

        if collection is not None and scene is not None:
            raise ValueError("Pass either a collection or a scene, not both")

        coordinate_system = get_attributes_or_error(self, "coordinate_system")
        slices: List[Slice] = get_attributes_or_error(self, "slices")

        discrete_dims = {
            axis.name
            for axis in coordinate_system.axes
            if axis.type == AxisType.CHANNEL
        }

        coordinates = [
            CoordinateInput(name=lens_slice.axis, value=lens_slice.start)
            for lens_slice in slices
            if lens_slice.axis in discrete_dims and lens_slice.start is not None
        ]

        if collection is None and scene is None:
            collection = create_annotation_collection(
                name=name or f"Drawings on {coordinate_system.name}",
                coordinate_system=coordinate_system.id,
            ).id

        return create_annotation(
            collection=collection,
            scene=scene,
            vectors=vectors,
            kind=kind,
            name=name,
            coordinates=coordinates,
        )

    def derive(
        self,
        *,
        kind: Optional[Union[str, Enum]] = None,
        scale: Optional[Sequence[float]] = None,
        translation: Optional[Sequence[float]] = None,
        affine: Optional[Sequence[Sequence[float]]] = None,
        input_axes: Optional[Sequence[str]] = None,
        output_axes: Optional[Sequence[str]] = None,
        # `use_enum_values` means the generated input stores the enum's value, so
        # a bare string is exactly as valid as the member.
        value_relation: Optional[Union["ValueRelation", str]] = None,
        reason: Optional[str] = None,
    ) -> "DerivedFromInput":
        """A derivation edge pointing back into this lens, for a dataset about
        to be created from what the lens frames.

        The result goes into ``create_a_dataset(derived_from=[...])``. When
        `kind` is omitted it is inferred from which parameters are given:
        `affine` -> AFFINE, `scale` -> SCALE, `translation` -> TRANSLATION
        (scale and translation together fold into one AFFINE), `input_axes` ->
        MAP_AXIS, nothing -> IDENTITY. An IDENTITY derivation carries no
        transform at all — the data is in the lens' space as-is, and omitting
        the edge's map is how the schema says so.

        `value_relation` states what the derivation did to the *values* —
        orthogonal to the spatial kind: IDENTICAL for a cut, TRANSFORMED for a
        recomputation, CATEGORIZED for a labelling. `reason` is recorded only
        on an UNMAPPABLE derivation.
        """
        # `DerivedFromInput` is a union discriminated on the *source* kind, so it
        # is a typing alias and cannot be called. This method hangs off a lens, so
        # the member is the lens one — the transform kind (IDENTITY, SCALE, ...)
        # is a separate discriminator, carried inside `transform`.
        from mikro_next.api.schema import LensDerivedFromInput

        if kind is None:
            kind, scale, translation, affine = _infer_transform_kind(
                scale, translation, affine, input_axes
            )

        transform = _transform_member(
            kind,
            scale=scale,
            translation=translation,
            affine=affine,
            input_axes=input_axes,
            output_axes=output_axes,
            reason=reason,
        )

        kwargs: Dict[str, Any] = {}
        if transform is not None:
            kwargs["transform"] = transform
        if value_relation is not None:
            kwargs["value_relation"] = value_relation

        return LensDerivedFromInput(
            lens=get_attributes_or_error(self, "id"), **kwargs
        )

    def derive_identity(
        self,
        value_relation: Optional["ValueRelation"] = None,
    ) -> "DerivedFromInput":
        """An IDENTITY derivation edge: same axes, same voxels.

        The classic case is a dense computation on the same grid — a
        segmentation (`value_relation=CATEGORIZED`), a deconvolution
        (`value_relation=TRANSFORMED`). Why the computation happened belongs to
        task provenance, not to the edge — the edge carries no reason.
        """
        return self.derive(kind="IDENTITY", value_relation=value_relation)

    def derive_translation(
        self,
        offset: Sequence[float],
        *,
        # `use_enum_values` means the generated input stores the enum's value, so
        # the bare string this defaults to is exactly as valid as the member.
        value_relation: Optional[Union["ValueRelation", str]] = "IDENTICAL",
    ) -> "DerivedFromInput":
        """A TRANSLATION derivation edge: same axes, shifted origin — a crop.

        `offset` is forward, derived -> source: the derived dataset's voxel
        (0, ..., 0) lands on this position in the lens' space. A crop cuts but
        does not compute, so `value_relation` defaults to IDENTICAL (statistics
        transfer); override it when the values were also recomputed.
        """
        return self.derive(
            kind="TRANSLATION",
            translation=offset,
            value_relation=value_relation,
        )

    def derive_projection(
        self,
        axes: Sequence[str],
        *,
        value_relation: Optional["ValueRelation"] = None,
    ) -> "DerivedFromInput":
        """A rank-dropping BY_DIMENSION derivation edge keeping only `axes`.

        Naming an axis on both sides IS the map; the axes left unnamed are the
        dropped ones — a line through a volume keeps ``["x"]``, a projection
        keeps ``["y", "x"]``. *Where* the kept axes sit along the dropped ones
        is the lens' business: slice the lens, don't restate it here.
        """
        return self.derive(
            kind="BY_DIMENSION",
            input_axes=axes,
            output_axes=axes,
            value_relation=value_relation,
        )


def _normalize_kind(kind: Union[str, Enum]) -> str:
    """Normalize a transformation kind to its plain string value."""
    return str(getattr(kind, "value", kind))


def _axis_names_in_order(system: "CoordinateSystemTrait") -> List[str]:
    """The axis names of a coordinate system, ordered by their `order` field."""
    axes = get_attributes_or_error(system, "axes")
    return [a.name for a in sorted(axes, key=lambda a: a.order)]


def _space_of(source: "Registrable") -> "CoordinateSystem":
    """The coordinate system a registrable source lives in.

    Data lives in exactly one space and says so itself, but which field says it
    depends on the container: a dataset calls its own grid ``intrinsic_system``,
    while a table dataset, a mesh collection and an annotation collection each
    call theirs ``coordinate_system``. A coordinate system is its own space.

    Raises:
        ValueError: If the source has no space, or the query did not select it.
    """
    for field in ("intrinsic_system", "coordinate_system"):
        space = getattr(source, field, None)
        if space is not None:
            return space
    # A system passed directly: it has axes, and it is not a container.
    if getattr(source, "axes", None) is not None:
        return cast("CoordinateSystem", source)
    raise ValueError(
        f"{getattr(source, 'name', source)!r} has no coordinate system, so there "
        f"is nothing to register. Either it genuinely lives in no space, or the "
        f"query did not select `intrinsicSystem` / `coordinateSystem` on it."
    )


def _homogeneous_from_rows(rows: "np.ndarray", ndim_in: Optional[int]) -> "np.ndarray":
    """Turn an M x (N+1) affine (last column translation) into a homogeneous
    (M+1) x (N+1) matrix. A square N x N matrix (a rotation given without a
    translation column) gets a zero translation column appended first."""
    rows = np.asarray(rows, dtype=float)
    if rows.ndim != 2:
        raise ValueError(f"Expected a 2D affine matrix, got shape {rows.shape}")
    m, cols = rows.shape
    if ndim_in is not None and cols == ndim_in:
        rows = np.hstack([rows, np.zeros((m, 1))])
    n = rows.shape[1] - 1
    bottom = np.zeros((1, n + 1))
    bottom[0, n] = 1.0
    return np.vstack([rows, bottom])


def _apply_homogeneous(matrix: "np.ndarray", points: PointsLike) -> "np.ndarray":
    """Apply a homogeneous (M+1) x (N+1) matrix to an (K, N) or (N,) point array."""
    pts = np.atleast_2d(np.asarray(points, dtype=float))
    n = matrix.shape[1] - 1
    if pts.shape[1] != n:
        raise ValueError(
            f"Points have dimension {pts.shape[1]}, but the transformation expects {n}"
        )
    out = (matrix @ np.hstack([pts, np.ones((len(pts), 1))]).T).T[:, :-1]
    return out[0] if np.ndim(points) == 1 else out


def _infer_transform_kind(
    scale: Optional[Sequence[float]],
    translation: Optional[Sequence[float]],
    affine: Optional[Sequence[Sequence[float]]],
    input_axes: Optional[Sequence[str]],
) -> Tuple[
    str,
    Optional[Sequence[float]],
    Optional[Sequence[float]],
    Optional[Sequence[Sequence[float]]],
]:
    """Infer the transformation kind from which parameters were given.

    Returns (kind, scale, translation, affine); a combined scale + translation
    is folded into a single affine.
    """
    if affine is not None:
        if scale is not None or translation is not None:
            raise ValueError("Pass either affine= or scale=/translation=, not both")
        return "AFFINE", None, None, affine
    if scale is not None and translation is not None:
        if len(scale) != len(translation):
            raise ValueError(
                f"scale has {len(scale)} entries but translation has {len(translation)}"
            )
        folded = np.hstack(
            [
                np.diag(np.asarray(scale, dtype=float)),
                np.asarray(translation, dtype=float)[:, None],
            ]
        ).tolist()
        return "AFFINE", None, None, folded
    if scale is not None:
        return "SCALE", scale, None, None
    if translation is not None:
        return "TRANSLATION", None, translation, None
    if input_axes is not None:
        return "MAP_AXIS", None, None, None
    return "IDENTITY", None, None, None


def _transform_member(
    kind: Union[str, Enum],
    *,
    scale: Optional[Sequence[float]] = None,
    translation: Optional[Sequence[float]] = None,
    affine: Optional[Sequence[Sequence[float]]] = None,
    input_axes: Optional[Sequence[str]] = None,
    output_axes: Optional[Sequence[str]] = None,
    field: Optional[IDCoercible] = None,
    reason: Optional[str] = None,
) -> Optional["TransformInput"]:
    """Build the tagged member input for a transformation ``kind``.

    The schema publishes ``TransformInput`` as a tagged union of per-kind
    member inputs, each the strict truth about which fields its kind reads —
    anything else is rejected, never dropped. This is where the flat parameter
    surface of the sugar methods narrows to the kind's own fields.

    Returns ``None`` for IDENTITY: it has no member (GraphQL forbids an empty
    input object), so the schema expresses an identity by omitting the
    transform wherever that is possible.
    """
    from mikro_next.api import schema

    kind = _normalize_kind(kind)

    if reason is not None and kind != "UNMAPPABLE":
        raise ValueError(
            f"reason is only recorded on an UNMAPPABLE edge, not on a {kind}: "
            "the coordinate graph reads nothing else from it"
        )

    def require(name: str, value: Optional[_Given]) -> _Given:
        """The value, or a refusal naming the parameter the kind needs."""
        if value is None:
            raise ValueError(f"A {kind} transformation needs {name}=")
        return value

    if kind == "IDENTITY":
        given = (scale, translation, affine, input_axes, output_axes, field)
        if any(value is not None for value in given):
            raise ValueError("An IDENTITY transformation takes no parameters")
        return None
    if kind == "SCALE":
        return schema.ScaleTransformInput(
            scale=tuple(float(s) for s in require("scale", scale))
        )
    if kind == "TRANSLATION":
        return schema.TranslationTransformInput(
            translation=tuple(float(t) for t in require("translation", translation))
        )
    if kind == "AFFINE":
        return schema.AffineTransformInput(
            affine=np.asarray(require("affine", affine), dtype=float).tolist()
        )
    if kind == "ROTATION":
        return schema.RotationTransformInput(
            affine=np.asarray(require("affine", affine), dtype=float).tolist()
        )
    if kind == "MAP_AXIS":
        return schema.MapAxisTransformInput(
            input_axes=list(require("input_axes", input_axes)),
            output_axes=list(require("output_axes", output_axes)),
        )
    if kind == "BY_DIMENSION":
        optional: Dict[str, Any] = {}
        if scale is not None:
            optional["scale"] = [float(s) for s in scale]
        if translation is not None:
            optional["translation"] = [float(t) for t in translation]
        if affine is not None:
            optional["affine"] = np.asarray(affine, dtype=float).tolist()
        return schema.ByDimensionTransformInput(
            input_axes=list(require("input_axes", input_axes)),
            output_axes=list(require("output_axes", output_axes)),
            **optional,
        )
    if kind == "FIELD":
        return schema.FieldTransformInput(
            field=require("field", field),
            input_axes=list(require("input_axes", input_axes)),
            output_axes=list(require("output_axes", output_axes)),
        )
    if kind == "UNMAPPABLE":
        if reason is None:
            return schema.UnmappableTransformInput()
        return schema.UnmappableTransformInput(reason=reason)
    raise ValueError(f"Unknown transformation kind {kind!r}")


class PathStep(NamedTuple):
    """One edge of a composable path between coordinate systems.

    `inverted` is True when the edge is traversed output-to-input, in which
    case its matrix must be inverted before composing.
    """

    transformation: Any
    inverted: bool


class TransformationTrait:
    """A trait for transformation edges between coordinate systems.

    Turns the per-kind parameters (scale, translation, affine, ...) into
    homogeneous numpy matrices and applies them to points. The matrix maps
    points given in the *input* system's axis order to points in the *output*
    system's axis order; the server guarantees positional correspondence, and
    explicit axis reordering only ever happens through MAP_AXIS edges.
    """

    MATRIX_KINDS = (
        "IDENTITY",
        "SCALE",
        "TRANSLATION",
        "AFFINE",
        "ROTATION",
        "MAP_AXIS",
    )

    def ndim_in(self) -> Optional[int]:
        """Number of input axes, if the input system was selected in the query."""
        system = getattr(self, "input", None)
        axes = getattr(system, "axes", None) if system is not None else None
        return len(axes) if axes is not None else None

    def ndim_out(self) -> Optional[int]:
        """Number of output axes, if the output system was selected in the query."""
        system = getattr(self, "output", None)
        axes = getattr(system, "axes", None) if system is not None else None
        return len(axes) if axes is not None else None

    def as_matrix(self) -> NDArray[np.float64]:
        """This transformation as a homogeneous (M+1) x (N+1) numpy matrix.

        Only IDENTITY, SCALE, TRANSLATION, AFFINE, ROTATION and MAP_AXIS have
        a closed-form matrix. SEQUENCE requires `.resolve_matrix()` (a network
        round-trip); the remaining kinds have no matrix.
        """
        kind = _normalize_kind(get_attributes_or_error(self, "kind"))

        if kind == "IDENTITY":
            n = self.ndim_in() or self.ndim_out()
            if n is None:
                raise ValueError(
                    "Cannot determine the dimensionality of an IDENTITY transformation: "
                    "neither the input nor the output coordinate system (with axes) was "
                    "selected in the query"
                )
            return np.eye(n + 1)

        if kind == "SCALE":
            scale = get_attributes_or_error(self, "scale")
            return np.diag([float(s) for s in scale] + [1.0])

        if kind == "TRANSLATION":
            translation = get_attributes_or_error(self, "translation")
            n = len(translation)
            matrix = np.eye(n + 1)
            matrix[:n, n] = [float(t) for t in translation]
            return matrix

        if kind in ("AFFINE", "ROTATION"):
            affine = get_attributes_or_error(self, "affine")
            return _homogeneous_from_rows(
                np.asarray(affine, dtype=float), self.ndim_in()
            )

        if kind == "MAP_AXIS":
            input_axes, output_axes = get_attributes_or_error(
                self, "input_axes", "output_axes"
            )
            input_system = getattr(self, "input", None)
            output_system = getattr(self, "output", None)
            if input_system is None or output_system is None:
                raise ValueError(
                    "Building a MAP_AXIS matrix requires the input and output "
                    "coordinate systems (with axes) to be selected in the query"
                )
            in_names = _axis_names_in_order(input_system)
            out_names = _axis_names_in_order(output_system)
            matrix = np.zeros((len(out_names) + 1, len(in_names) + 1))
            matrix[len(out_names), len(in_names)] = 1.0
            for in_name, out_name in zip(input_axes, output_axes):
                if in_name not in in_names:
                    raise KeyError(
                        f"MAP_AXIS input axis {in_name!r} not in input system axes {in_names}"
                    )
                if out_name not in out_names:
                    raise KeyError(
                        f"MAP_AXIS output axis {out_name!r} not in output system axes {out_names}"
                    )
                matrix[out_names.index(out_name), in_names.index(in_name)] = 1.0
            return matrix

        if kind == "SEQUENCE":
            raise NotImplementedError(
                "SEQUENCE children carry only their id and kind in this query; call "
                ".resolve_matrix() to fetch and compose them (requires a network round-trip)"
            )
        if kind == "UNMAPPABLE":
            raise NotImplementedError(
                "An UNMAPPABLE transformation is a declared non-correspondence between "
                "two coordinate systems; it has no matrix by definition"
            )
        raise NotImplementedError(
            f"Transformations of kind {kind} have no closed-form matrix"
        )

    def inverse_matrix(self) -> NDArray[np.float64]:
        """The inverse of `as_matrix()`; raises ValueError if not invertible."""
        matrix = self.as_matrix()
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError(
                f"Cannot invert transformation {getattr(self, 'id', '?')}: it maps "
                f"{matrix.shape[1] - 1} -> {matrix.shape[0] - 1} dimensions"
            )
        try:
            return np.linalg.inv(matrix).astype(np.float64)
        except np.linalg.LinAlgError as e:
            kind = _normalize_kind(get_attributes_or_error(self, "kind"))
            raise ValueError(
                f"Transformation {getattr(self, 'id', '?')} ({kind}) is singular "
                f"and cannot be inverted"
            ) from e

    def apply(self, points: PointsLike) -> NDArray[np.float64]:
        """Map points from the input system to the output system.

        Accepts a (K, N) array or a single (N,) point in the input system's
        axis order; returns the matching shape in the output system's order.
        """
        return _apply_homogeneous(self.as_matrix(), points)

    def apply_inverse(self, points: PointsLike) -> NDArray[np.float64]:
        """Map points from the output system back to the input system."""
        return _apply_homogeneous(self.inverse_matrix(), points)

    def resolve_matrix(self, rath: Optional["MikroNextRath"] = None) -> NDArray[np.float64]:
        """Like `as_matrix()`, but resolves SEQUENCE transformations by fetching
        each child from the server and composing them first-to-last."""
        kind = _normalize_kind(get_attributes_or_error(self, "kind"))
        if kind != "SEQUENCE":
            return self.as_matrix()

        from mikro_next.api.schema import get_transformation

        children = get_attributes_or_error(self, "sequence_children")
        matrix: Optional[np.ndarray] = None
        for child in children:
            full = get_transformation(child.id, rath=rath)
            resolve = getattr(full, "resolve_matrix", None)
            if resolve is None:
                raise ValueError(
                    f"Child transformation {child.id} came back as a kind this "
                    f"client does not model, so its matrix cannot be composed"
                )
            child_matrix = resolve(rath=rath)
            matrix = child_matrix if matrix is None else child_matrix @ matrix
        if matrix is None:
            raise ValueError(
                f"SEQUENCE transformation {getattr(self, 'id', '?')} has no children"
            )
        return matrix


def _bfs_path(
    transformations: Sequence[Any],
    start_id: str,
    target_id: str,
    allow_fetch: bool = False,
) -> List[PathStep]:
    """Find the shortest composable path between two coordinate systems.

    Edges are walked forward (input -> output) and backward (output -> input,
    flagged inverted). Only kinds with a closed-form matrix are walkable
    (plus SEQUENCE when `allow_fetch` permits resolving children later).
    """
    adjacency: Dict[str, List[Tuple[PathStep, str]]] = {}
    for t in transformations:
        kind = _normalize_kind(get_attributes_or_error(t, "kind"))
        composable = kind in TransformationTrait.MATRIX_KINDS or (
            kind == "SEQUENCE" and allow_fetch
        )
        if not composable:
            continue
        input_system = getattr(t, "input", None)
        output_system = getattr(t, "output", None)
        if input_system is None or output_system is None:
            continue
        in_id, out_id = str(input_system.id), str(output_system.id)
        adjacency.setdefault(in_id, []).append((PathStep(t, False), out_id))
        adjacency.setdefault(out_id, []).append((PathStep(t, True), in_id))

    if start_id == target_id:
        return []

    queue = deque([start_id])
    predecessor: Dict[str, Tuple[str, PathStep]] = {}
    visited = {start_id}
    while queue:
        node = queue.popleft()
        for step, neighbor in adjacency.get(node, []):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            predecessor[neighbor] = (node, step)
            if neighbor == target_id:
                path: List[PathStep] = []
                current = neighbor
                while current != start_id:
                    current, prev_step = predecessor[current]
                    path.append(prev_step)
                return list(reversed(path))
            queue.append(neighbor)

    raise ValueError(
        f"No composable transformation path from coordinate system {start_id} to "
        f"{target_id}. Reachable systems: {sorted(visited)}"
    )


def _compose_steps(
    steps: Sequence[PathStep],
    identity_ndim: Optional[int] = None,
    allow_fetch: bool = False,
    rath: Optional["MikroNextRath"] = None,
) -> NDArray[np.float64]:
    """Compose a path of steps into one homogeneous matrix, applied first-to-last
    (the newest matrix multiplies on the left). Inverted steps are inverted first."""
    matrix: Optional[np.ndarray] = None
    for step in steps:
        t = step.transformation
        kind = _normalize_kind(get_attributes_or_error(t, "kind"))
        if kind == "SEQUENCE" and allow_fetch:
            step_matrix = t.resolve_matrix(rath=rath)
        else:
            step_matrix = t.as_matrix()
        if step.inverted:
            if step_matrix.shape[0] != step_matrix.shape[1]:
                raise ValueError(
                    f"The path needs the inverse of transformation "
                    f"{getattr(t, 'id', '?')} ({kind}), but it maps "
                    f"{step_matrix.shape[1] - 1} -> {step_matrix.shape[0] - 1} "
                    f"dimensions and is not invertible"
                )
            step_matrix = np.linalg.inv(step_matrix)
        if matrix is None:
            matrix = step_matrix
        elif step_matrix.shape[1] != matrix.shape[0]:
            raise ValueError(
                f"Transformation {getattr(t, 'id', '?')} expects "
                f"{step_matrix.shape[1] - 1} dimensions but the path so far "
                f"produces {matrix.shape[0] - 1}"
            )
        else:
            matrix = step_matrix @ matrix
    if matrix is None:
        if identity_ndim is None:
            raise ValueError("Cannot compose an empty path without a dimensionality")
        return np.eye(identity_ndim + 1)
    return matrix


class SceneTrait:
    """A trait for scenes: a *composition* of layers over a world space.

    A scene is not a space. It adopts one — many scenes can share a world, the
    world outlives each of them, and deleting a scene never deletes it. What a
    scene owns is view state: its layers, its snapshots, its animations, its
    camera preference, its background colour.

    So a scene has no way to place anything. A layer carries no affine, and
    where data sits is an edge of the coordinate graph landing in the world —
    a claim that belongs to the *space*, which is why every scene composing
    over that world sees it. Register through the world instead::

        scene.world.register(dataset, x=288.0)
    """

    @property
    def world(self) -> "CoordinateSystem":
        """The shared coordinate system this scene composes its layers over.

        Adopted, never owned: many scenes can compose over this same space, it
        outlives each of them, and deleting a scene never deletes it. Read
        straight off the scene — the same mutation that created it already
        returned this.
        """
        return get_attributes_or_error(self, "world_coordinate_system")

    def place(self, *args: Any, **kwargs: Any) -> NoReturn:
        """Removed: a scene composes, it does not place.

        Raises:
            AttributeError: Always, pointing at `scene.world.register`.
        """
        raise AttributeError(
            "a scene composes, it does not place: scene.world.register(dataset, "
            "x=...) authors the edge, and every scene over that world sees it"
        )

    def grid_cell(self, *args: Any, **kwargs: Any) -> NoReturn:
        """Removed: a scene composes, it does not place.

        Raises:
            AttributeError: Always, pointing at `scene.world.grid_cell`.
        """
        raise AttributeError(
            "a scene composes, it does not place: scene.world.grid_cell(dataset, "
            "index, cols, pitch) authors the edge, and every scene over that "
            "world sees it"
        )

    def clear(self, rath: Optional["MikroNextRath"] = None) -> "Scene":
        """Delete every layer of this scene, keeping the scene itself.

        A pure view-state reset: no coordinate system, registration or dataset
        is touched, and other scenes over the same world never notice.

        Args:
            rath: The mikro rath client.

        Returns:
            This scene, now empty.
        """
        from mikro_next.api.schema import clear_scene

        return clear_scene(id=get_attributes_or_error(self, "id"), rath=rath)

    def delete(self, rath: Optional["MikroNextRath"] = None) -> ID:
        """Delete this scene.

        Its world survives — a scene adopts a space, never owns it. Sweep the
        spaces nothing is left over with `delete_orphaned_coordinate_systems`.

        Args:
            rath: The mikro rath client.

        Returns:
            The id of the deleted scene.
        """
        from mikro_next.api.schema import delete_scene

        return delete_scene(id=get_attributes_or_error(self, "id"), rath=rath)


class CoordinateSystemTrait:
    """A trait for coordinate systems: a *space*, a node of the coordinate graph.

    A space belongs to nobody. It does not know what lives in it (ask it for its
    residents and it answers by looking at who points at it), it owns no scene,
    and it carries no classification — a space with no residents simply is a
    pure reference frame, a world or an atlas.

    What lands in a space is a registration: an edge claiming that some source
    is placed here. Those edges belong to the space, not to any composition over
    it, so every scene sharing this world sees the same ones — which is why
    `register`, `grid_cell` and `unregister` live here rather than on a scene.

    Also provides axis utilities and client-side navigation of the coordinate
    graph (the server returns edges; composing and inverting them is the
    client's job). SCALE and TRANSLATION parameters are positional in the input
    system's axis order; explicit axis reordering only ever happens through
    MAP_AXIS edges.
    """

    def register(
        self,
        source: "Registrable",
        *,
        scale: Optional[Union[Mapping[str, float], Sequence[float]]] = None,
        name: Optional[str] = None,
        validity: Optional["PlacementValidity"] = None,
        rath: Optional["MikroNextRath"] = None,
        **offsets: float,
    ) -> "CreatedTransformation":
        """Register `source` into this space, scaled and translated.

        `source` is anything that lives in a space — a dataset, a table dataset,
        a mesh collection, an annotation collection, or a coordinate system
        given directly.

        The edge is a BY_DIMENSION naming the axes the two spaces share, because
        that is the only shape that can say "these axes correspond one to one,
        and I claim nothing about the rest". A square edge cannot: a default
        world is ``(t, z, y, x)`` and a photograph is ``(c, y, x)``, so a plain
        translation sized to the source would be silently read positionally —
        mapping its ``c`` onto the world's ``t`` and its ``y`` onto ``z`` — and
        the rank check cannot catch it, because the vector length is right. It
        is also what lets an unshared axis simply not be claimed: a channel axis
        is not a position, and a physical world has no business naming it.

        `scale` is where a pixel size lives. It is a property of the edge, not
        of either space: the source's grid is in unitless indices, this space is
        in whatever its axes carry, and the factor between them is the claim.
        Give it per axis name (missing axes default to 1.0) or as a sequence
        positional against the shared axes.

        Offsets are given per axis name and default to 0, so registering at the
        origin needs no arguments. They are read against this space's axes, so
        what a unit means here is whatever those axes carry.

            world.register(dataset)                              # at the origin
            world.register(dataset, x=288.0)                     # shifted along x
            world.register(dataset, scale={"z": 1.0, "y": 0.2, "x": 0.2})
            world.register(table_dataset, y=144.0)               # any source with a space

        Args:
            source: Anything that lives in a space.
            scale: The per-axis factor from the source's coordinates into this
                space's, by axis name or positional against the shared axes.
            name: An optional name for the edge.
            validity: How far the claim is to be trusted.
            rath: The mikro rath client.
            **offsets: The per-axis offset in this space's coordinates.

        Returns:
            The created registration edge.

        Raises:
            ValueError: If the two spaces share no axis, if a scale or an offset
                names an unshared one, or if a positional scale is the wrong
                length.
        """
        space = _space_of(source)

        axis_names = _axis_names_in_order(space)
        my_names = _axis_names_in_order(self)

        # In the source's own axis order: the edge's parameters are positional
        # against `input_axes`, so the two lists have to agree.
        shared = [axis for axis in axis_names if axis in my_names]
        if not shared:
            raise ValueError(
                f"{getattr(source, 'name', source)} has axes {axis_names} and the "
                f"space '{getattr(self, 'name', '?')}' has {my_names}: they share "
                f"none, so there is no correspondence to register. Create the space "
                f"over axes the source actually has "
                f"(create_coordinate_system(axes=[...]))."
            )

        named = set(offsets) | (set(scale) if isinstance(scale, Mapping) else set())
        unplaceable = sorted(named - set(shared))
        if unplaceable:
            raise ValueError(
                f"Cannot scale or offset along {unplaceable}: the axis is not shared "
                f"between {getattr(source, 'name', source)} {axis_names} and the space "
                f"{my_names}, so a claim along it has nowhere to land."
            )

        # Both vectors are positional against `shared`, so they are built the
        # same way — a per-axis lookup in that one order — and cannot drift.
        if scale is None:
            factors = None
        elif isinstance(scale, Mapping):
            factors = [float(scale.get(axis, 1.0)) for axis in shared]
        else:
            factors = [float(s) for s in scale]
            if len(factors) != len(shared):
                raise ValueError(
                    f"scale has {len(factors)} entries but the edge acts on the "
                    f"shared axes {shared}. Pass a mapping of axis name to factor "
                    f"to say which is which."
                )

        return space.transform_to(
            self,
            kind="BY_DIMENSION",
            scale=factors,
            translation=[float(offsets.get(axis, 0.0)) for axis in shared],
            input_axes=shared,
            output_axes=shared,
            name=name
            or f"{getattr(source, 'name', 'source')} -> {getattr(self, 'name', 'space')}",
            validity=validity,
            rath=rath,
        )

    def grid_cell(
        self,
        source: "Registrable",
        index: int,
        cols: int,
        pitch: float,
        **kwargs: Any,
    ) -> "CreatedTransformation":
        """Register `source` into this space at grid cell `index`.

        Cells fill in reading order. `pitch` is the centre-to-centre spacing in
        this space's own units — at one unit per voxel that is the array's width
        plus whatever gutter you want. For laying variants of the same data out
        next to each other, which needs one source (and one edge) per cell.

        Args:
            source: Anything that lives in a space.
            index: Which cell to place it in, counting in reading order.
            cols: How many cells make a row.
            pitch: The centre-to-centre spacing, in this space's units.
            **kwargs: Passed through to `register` (`scale`, `name`, `validity`).

        Returns:
            The created registration edge.

        Raises:
            ValueError: If `cols` is less than 1.
        """
        if cols < 1:
            raise ValueError(f"cols must be at least 1, got {cols}")
        row, col = divmod(index, cols)
        return self.register(source, x=col * pitch, y=row * pitch, **kwargs)

    def unregister(
        self,
        *,
        dataset: Optional[IDCoercible] = None,
        table_dataset: Optional[IDCoercible] = None,
        mesh_collection: Optional[IDCoercible] = None,
        annotation_collection: Optional[IDCoercible] = None,
        coordinate_system: Optional[IDCoercible] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> Tuple[ID, ...]:
        """Un-register a source from this space, by naming the source.

        Deletes every edge from the source's space into this one — rival claims
        are allowed, so there is no single edge to mean — and returns their ids.
        An UNMAPPABLE declaration is not a placement and is never matched.

        Exactly one source must be named. The kind is not inferred: the models
        carry no ``__typename``, so a guess could be silently wrong.

        Args:
            dataset: The dataset to un-register.
            table_dataset: The table dataset to un-register.
            mesh_collection: The mesh collection to un-register.
            annotation_collection: The annotation collection to un-register.
            coordinate_system: The coordinate system to un-register.
            rath: The mikro rath client.

        Returns:
            The ids of the deleted edges.

        Raises:
            ValueError: If other than exactly one source is named.
        """
        from mikro_next.api.schema import delete_registration

        sources: Dict[str, Optional[IDCoercible]] = {
            "dataset": dataset,
            "table_dataset": table_dataset,
            "mesh_collection": mesh_collection,
            "annotation_collection": annotation_collection,
            "coordinate_system": coordinate_system,
        }
        named = {k: v for k, v in sources.items() if v is not None}
        if len(named) != 1:
            raise ValueError(
                f"Name exactly one source to un-register, got {sorted(named) or 'none'}. "
                f"Choose from {sorted(sources)}."
            )

        return delete_registration(
            world=get_attributes_or_error(self, "id"), rath=rath, **named
        )

    def stage(
        self,
        *,
        name: Optional[str] = None,
        policy: Optional["ScenePolicyInput"] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> "Scene":
        """Bootstrap a renderable scene over this space.

        The scene adopts this system as its world and no edges are authored —
        which is the whole point: what can be drawn here was decided when the
        sources were registered, so staging only composes. Over an ownerless
        shared space the sources already registered into it become layers, up to
        the policy's ``nchildren``; over an owned system (a dataset's intrinsic
        grid, a physical space, a collection's space) the container's own data
        becomes the layer.

        Rerunning makes another scene over this same space, which outlives them
        all.

        Args:
            name: An optional name for the scene.
            policy: A `ScenePolicyInput`. Omit to let the server choose.
            rath: The mikro rath client.

        Returns:
            The created scene.
        """
        from mikro_next.api.schema import (
            create_scene_from_coordinate_system,
            ScenePolicyInput,
        )

        kwargs: Dict[str, Any] = {}
        if name is not None:
            kwargs["name"] = name

        return create_scene_from_coordinate_system(
            coordinate_system=get_attributes_or_error(self, "id"),
            policy=policy if policy is not None else ScenePolicyInput(),
            rath=rath,
            **kwargs,
        )

    def clear(self, rath: Optional["MikroNextRath"] = None) -> Tuple[ID, ...]:
        """Delete every registration *into* this space, returning the edge ids.

        The space itself survives, so do the scenes composing over it (their
        layers drop to UNREGISTERED) and so do this space's own claims into
        wider spaces. Shared spaces only, and guarded by the space's creator:
        clearing a space is the space-owner's act.

        Args:
            rath: The mikro rath client.

        Returns:
            The ids of the deleted edges.
        """
        from mikro_next.api.schema import clear_coordinate_system

        return clear_coordinate_system(
            id=get_attributes_or_error(self, "id"), rath=rath
        )

    @property
    def ndim(self) -> int:
        """The number of axes of this coordinate system."""
        return len(get_attributes_or_error(self, "axes"))

    @property
    def axis_names(self) -> List[str]:
        """The axis names, ordered by their `order` field."""
        return _axis_names_in_order(self)

    @property
    def units(self) -> Dict[str, Optional[str]]:
        """A mapping of axis name to its unit (None for uncalibrated axes)."""
        axes = get_attributes_or_error(self, "axes")
        return {a.name: a.unit for a in sorted(axes, key=lambda a: a.order)}

    def get_axis(self, name: str) -> "Axis":
        """Get an axis by its name or long name."""
        axes = get_attributes_or_error(self, "axes")
        for axis in axes:
            if axis.name == name or getattr(axis, "long_name", None) == name:
                return axis
        raise KeyError(
            f"No axis {name!r} in coordinate system "
            f"{get_attributes_or_error(self, 'name')!r}. "
            f"Available axes: {[a.name for a in axes]}"
        )

    def transform_to(
        self,
        other: Union[str, ID, "CoordinateSystemTrait"],
        *,
        scale: Optional[Sequence[float]] = None,
        translation: Optional[Sequence[float]] = None,
        affine: Optional[Sequence[Sequence[float]]] = None,
        kind: Optional[str] = None,
        name: Optional[str] = None,
        input_axes: Optional[Sequence[str]] = None,
        output_axes: Optional[Sequence[str]] = None,
        reason: Optional[str] = None,
        validity: Optional["PlacementValidity"] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> "CreatedTransformation":
        """Create a transformation edge from this system to `other`.

        The kind is inferred from which parameters are given: `affine` ->
        AFFINE, `scale` -> SCALE, `translation` -> TRANSLATION (scale and
        translation together fold into one AFFINE), `input_axes` -> MAP_AXIS.
        Pass `kind` explicitly to override. An IDENTITY edge cannot be authored
        here — it has no member in the TransformInput union; registration and
        derivation express an identity by omitting the transform instead.
        `reason` is recorded only on an UNMAPPABLE edge.
        """
        from mikro_next.api.schema import create_transformation

        other_id = (
            other if isinstance(other, str) else get_attributes_or_error(other, "id")
        )

        if kind is None:
            kind, scale, translation, affine = _infer_transform_kind(
                scale, translation, affine, input_axes
            )

        # Parameters are positional against the axes the edge acts on. Naming
        # `input_axes` is what narrows that to a subset — the whole point of
        # naming them — so the rank they answer to is the subset's, not the
        # system's.
        if input_axes is not None:
            expected, against = len(list(input_axes)), f"input_axes {list(input_axes)}"
        else:
            expected, against = self.ndim, f"{self.ndim} axes ({self.axis_names})"

        for field, vector in (("scale", scale), ("translation", translation)):
            if vector is not None and len(vector) != expected:
                raise ValueError(
                    f"{field} has {len(vector)} entries but this transformation acts "
                    f"on {against}"
                )

        transform = _transform_member(
            kind,
            scale=scale,
            translation=translation,
            affine=affine,
            input_axes=input_axes,
            output_axes=output_axes,
            reason=reason,
        )
        if transform is None:
            raise ValueError(
                "An IDENTITY transformation edge cannot be authored through "
                "createTransformation: IDENTITY has no member in the TransformInput "
                "union (it has no fields). Registration and derivation express an "
                "identity by omitting the transform instead."
            )

        kwargs: Dict[str, Any] = {}
        if name is not None:
            kwargs["name"] = name
        if validity is not None:
            kwargs["validity"] = validity

        return create_transformation(
            input=get_attributes_or_error(self, "id"),
            output=other_id,
            transform=transform,
            rath=rath,
            **kwargs,
        )

    def graph(
        self, max_depth: Optional[int] = None, rath: Optional["MikroNextRath"] = None
    ) -> "GetCoordinateGraphQueryCoordinategraph":
        """Fetch the coordinate graph reachable from this system.

        Args:
            max_depth: How many edges out to walk. Omit for the server's default.
            rath: The mikro rath client.

        Returns:
            The reachable systems and the edges between them.
        """
        from mikro_next.api.schema import get_coordinate_graph

        kwargs: Dict[str, Any] = {}
        if max_depth is not None:
            kwargs["max_depth"] = max_depth
        return get_coordinate_graph(
            coordinate_system=get_attributes_or_error(self, "id"),
            rath=rath,
            **kwargs,
        )

    def path_to(
        self,
        other: Union[str, ID, "CoordinateSystemTrait"],
        *,
        max_depth: Optional[int] = None,
        allow_fetch: bool = False,
        graph: Optional["GetCoordinateGraphQueryCoordinategraph"] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> List[PathStep]:
        """The shortest composable path of transformation edges to `other`.

        Fetches the coordinate graph (or uses a pre-fetched `graph`) and walks
        it client-side; edges traversed against their stored direction are
        flagged inverted. Empty when `other` is this system.
        """
        my_id = str(get_attributes_or_error(self, "id"))
        other_id = str(
            other if isinstance(other, str) else get_attributes_or_error(other, "id")
        )
        if my_id == other_id:
            return []
        if graph is None:
            graph = self.graph(max_depth=max_depth, rath=rath)
        return _bfs_path(graph.transformations, my_id, other_id, allow_fetch)

    def matrix_to(
        self,
        other: Union[str, ID, "CoordinateSystemTrait"],
        *,
        max_depth: Optional[int] = None,
        allow_fetch: bool = False,
        graph: Optional["GetCoordinateGraphQueryCoordinategraph"] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> NDArray[np.float64]:
        """The composed homogeneous matrix mapping points of this system into
        `other`, found via the coordinate graph."""
        steps = self.path_to(
            other, max_depth=max_depth, allow_fetch=allow_fetch, graph=graph, rath=rath
        )
        return _compose_steps(
            steps, identity_ndim=self.ndim, allow_fetch=allow_fetch, rath=rath
        )

    def transform_points_to(
        self,
        other: Union[str, ID, "CoordinateSystemTrait"],
        points: PointsLike,
        *,
        max_depth: Optional[int] = None,
        allow_fetch: bool = False,
        graph: Optional["GetCoordinateGraphQueryCoordinategraph"] = None,
        rath: Optional["MikroNextRath"] = None,
    ) -> NDArray[np.float64]:
        """Map points given in this system's axis order into `other`.

        Accepts a (K, N) array or a single (N,) point; returns the matching
        shape in `other`'s axis order.
        """
        matrix = self.matrix_to(
            other, max_depth=max_depth, allow_fetch=allow_fetch, graph=graph, rath=rath
        )
        return _apply_homogeneous(matrix, points)
