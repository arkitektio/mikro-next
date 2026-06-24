"""
Custom scalars for mikro_next


"""

from __future__ import annotations

import io
from typing import Any, IO, Dict, List, Optional, TypeAlias, TYPE_CHECKING
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema


from collections.abc import Iterable
import mimetypes
from pathlib import Path
from pydantic_core import core_schema
import xarray as xr
import numpy as np
import uuid
from numpy.typing import NDArray

if TYPE_CHECKING:
    import pandas as pd

OneDArray = NDArray[np.generic]
FiveDArray = NDArray[np.generic]
TwoDArray = NDArray[np.generic]


TwoDVectorCoercible: TypeAlias = List[float] | OneDArray | List[int]
""" A type alias for 2D vector-like structures that can be coerced into a TwoDVector."""

ThreeDVectorCoercible: TypeAlias = List[float] | OneDArray | List[int]
""" A type alias for 3D vector-like structures that can be coerced into a ThreeDVector."""

FourDVectorCoercible: TypeAlias = List[float] | OneDArray | List[int]
""" A type alias for 4D vector-like structures that can be coerced into a FourDVector."""

FiveDVectorCoercible: TypeAlias = List[float] | OneDArray | List[List[float]] | List[List[int]]
""" A type alias for 5D vector-like structures that can be coerced into a FiveDVector."""

ArrayCoercible: TypeAlias = xr.DataArray | OneDArray | List[float] | List[List[float]]
""" A type alias for array-like structures that can be coerced into an xarray DataArray."""

ImageCoercible: TypeAlias = xr.DataArray | FiveDArray | List[float] | List[List[float]]

LabelsLikeCoercible: TypeAlias = xr.DataArray | OneDArray | List[List[str]] | Dict[str, List[str]]
""" A type alias for label-like structures that can be coerced into an xarray DataArray"""

ImageFileCoercible: TypeAlias = str | bytes | Path | io.BufferedReader
""" A type alias for image file-like structures that can be coerced into an xarray DataArray."""

ParquetCoercible: TypeAlias = "pd.DataFrame"
""" A type alias for parquet-like structures that can be coerced into an xarray DataArray."""

MeshCoercible: TypeAlias = str | bytes | Path | io.BufferedReader
""" A type alias for mesh-like structures that can be coerced into an xarray DataArray."""

FileCoercible: TypeAlias = str | bytes | Path | io.BufferedReader
""" A type alias for file-like structures that can be coerced into an xarray DataArray."""

FourByFourMatrixCoercible: TypeAlias = list[list[float]] | TwoDArray | list[list[int]]
""" A type alias for 4x4 matrix-like structures that can be coerced into an xarray DataArray."""

MillisecondsCoercible: TypeAlias = int | float
""" A type alias for millisecond-like structures that can be coerced into an xarray DataArray."""

MicrometersCoercible: TypeAlias = int | float
""" A type alias for micrometer-like structures that can be coerced into an xarray DataArray."""

RGBAColorCoercible: TypeAlias = List[float] | List[int] | OneDArray
""" A type alias for RGBA color-like structures that can be coerced into an RGBA Value"""


def _require_pandas() -> "Any":  # noqa: ANN401
    """Import pandas lazily, raising a helpful error if the extra is missing.

    pandas is only needed for the table/labels (parquet) paths, so it is an
    optional dependency. Install it via ``mikro-next[table]``.
    """
    try:
        import pandas as pd
    except ImportError as e:  # pragma: no cover - exercised only without the extra
        raise ImportError(
            "pandas is required for table/labels support. "
            "Install it with `pip install mikro-next[table]`."
        ) from e
    return pd


def is_dask_array(v: Any) -> bool:  # noqa: ANN401
    """Check if the input is a dask array."""
    try:
        import dask.array.core as da

        return isinstance(v, da.Array)
    except ImportError:
        return False
    except Exception as e:
        raise ValueError(f"Error checking for dask array: {e}")


def coerce_to_ctzyx(v: ArrayCoercible) -> xr.DataArray:
    """Coerce array-like input into a mikro-compliant 5D ``ctzyx`` DataArray.

    Bare numpy/dask arrays get their trailing dimensions labelled (``c, t, z, y, x``);
    explicitly labelled DataArrays must carry ``x`` and ``y`` dimensions and have any
    missing ``t``/``c``/``z`` dimensions expanded. The result is always transposed to
    ``ctzyx`` so that it round-trips with the reader, which assumes that layout.

    The array is returned lazily (dask chunks are preserved when present) so the upload
    path can stream it to zarr chunk-by-chunk instead of materialising it in memory.
    """
    was_labeled = True
    # If a bare array is passed, the user did not label the dimensions, so we assign
    # the trailing ctzyx dims and run extra sanity checks on the inferred layout.
    if isinstance(v, np.ndarray) or is_dask_array(v):
        dims = ["c", "t", "z", "y", "x"]
        v = xr.DataArray(v, dims=dims[5 - v.ndim :])
        was_labeled = False

    if not isinstance(v, xr.DataArray):
        raise ValueError("This needs to be a instance of xarray.DataArray")

    if "x" not in v.dims:
        raise ValueError("Representations must always have a 'x' Dimension")

    if "y" not in v.dims:
        raise ValueError("Representations must always have a 'y' Dimension")

    if "t" not in v.dims:
        v = v.expand_dims("t")
    if "c" not in v.dims:
        v = v.expand_dims("c")
    if "z" not in v.dims:
        v = v.expand_dims("z")

    if not was_labeled:
        if v.sizes["t"] > v.sizes["x"] or v.sizes["t"] > v.sizes["y"]:
            raise ValueError(
                f"Probably Non sensical dimensions. T is bigger than x or y: Sizes {v.sizes}"
            )
        if v.sizes["z"] > v.sizes["x"] or v.sizes["z"] > v.sizes["y"]:
            raise ValueError(
                f"Probably Non sensical dimensions. Z is bigger than x or y: Sizes {v.sizes}"
            )
        if v.sizes["c"] > v.sizes["x"] or v.sizes["c"] > v.sizes["y"]:
            raise ValueError(
                f"Probably Non sensical dimensions. C is bigger than x or y: Sizes {v.sizes}"
            )

    return v.transpose(*"ctzyx")


def coerce_to_labeled_array(v: ArrayCoercible) -> xr.DataArray:
    """Coerce array-like input into a labelled ``xr.DataArray`` without forcing ``ctzyx``.

    Unlike :func:`coerce_to_ctzyx` (used by ``ImageLike``), this preserves the
    caller's dimension labels and order verbatim: no dimensions are added,
    removed, or transposed. This is the generic dataset path where the user
    supplies arbitrary, explicitly-labelled dimensions alongside matching
    ``dim_descriptors`` (validated at the model level by ``CreateADatasetTrait``).

    Bare numpy/dask arrays carry no labels, so they are wrapped with xarray's
    default dimension names (``dim_0``, ``dim_1``, ...). The array is returned
    lazily (dask chunks preserved) so the upload path can stream it to zarr.
    """
    if isinstance(v, np.ndarray) or is_dask_array(v):
        return xr.DataArray(v)

    if not isinstance(v, xr.DataArray):
        raise ValueError("This needs to be a instance of xarray.DataArray")

    return v


class RGBAColor(list[float]):
    """A custom scalar to represent an affine matrix."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(float))

    @classmethod
    def validate(cls, v: RGBAColorCoercible) -> "RGBAColor":
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            if v.ndim == 1:
                v = v.tolist()
            else:
                raise ValueError("The input array must be a 1D array")

        if not isinstance(v, list):
            raise ValueError("The input must be a list or a 1-D numpy array.")

        v = [float(i) for i in v]  # Convert all elements to float

        if len(v) == 3:
            v.append(1.0)  # Add alpha channel if not present

        if len(v) != 4:
            raise ValueError(
                f"The input must be a list of 3 or 4 elements (R, G, B, [A]). You provided a list of {len(v)} elements"
            )

        return cls(v)


class XArrayConversionException(Exception):
    """An exception that is raised when a conversion to xarray fails."""

    pass


MetricValue = Any
FeatureValue = Any


class Micrometers(float):
    """A custom scalar to represent a micrometer."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(float))

    @classmethod
    def validate(cls, v: MicrometersCoercible) -> "Micrometers":
        """Validate the input array and convert it to a xr.DataArray."""
        return cls(v)


class Milliseconds(float):
    """A custom scalar to represent a millisecond."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(float))

    @classmethod
    def validate(cls, v: MillisecondsCoercible) -> "Milliseconds":
        """Validate the input array and convert it to a xr.DataArray."""
        return cls(v)


class TwoDVector(list[float]):
    """A custom scalar to represent a vector."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        _handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: TwoDVectorCoercible) -> "TwoDVector":
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 1
            v = v.tolist()  # Convert numpy array to list #type: ignore

        assert isinstance(v, list)
        assert len(v) == 3
        return cls(v)

    def as_vector(self) -> OneDArray:
        """Convert the TwoDVector to a numpy array."""
        return np.array(self)


class ThreeDVector(list[float]):
    """A custom scalar to represent a vector."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        _handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: ThreeDVectorCoercible) -> "ThreeDVector":
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 1
            v = v.tolist()

        assert isinstance(v, list)
        assert len(v) == 3
        return cls(v)

    def as_vector(self) -> OneDArray:
        """Convert the ThreeDVector to a numpy array."""
        return np.array(self)


class FourDVector(list[float]):
    """A custom scalar to represent a vector."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        _handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: FourDVectorCoercible) -> "FourDVector":
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 1
            v = v.tolist()

        assert isinstance(v, list)
        assert len(v) == 4
        return cls(v)

    def as_vector(self) -> OneDArray:
        """Convert the FourDVector to a numpy array."""
        return np.array(self).reshape(-1)


class FiveDVector(list[float]):
    """A custom scalar to represent a vector."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        _handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_plain_validator_function(cls.validate)

    @property
    def x(self) -> float:
        """Get the x coordinate."""
        return self[4]

    @property
    def y(self) -> float:
        """Get the y coordinate."""
        return self[3]

    @property
    def z(self) -> float:
        """Get the z coordinate."""
        return self[2]

    @property
    def t(self) -> float:
        """Get the t coordinate."""
        return self[1]

    @property
    def c(self) -> float:
        """Get the c coordinate."""
        return self[0]

    @classmethod
    def from_params(cls, c: int, t: int, z: int, x: float, y: float) -> "FiveDVector":
        """Create a FiveDVector from individual parameters."""
        return cls([float(c), float(t), float(z), float(y), float(x)])

    @classmethod
    def validate(cls, v: FiveDVectorCoercible) -> "FiveDVector":
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, np.ndarray):
            if not v.ndim == 1:
                raise ValueError("The input array must be a 1D array")
            v = v.tolist()

        if not isinstance(v, Iterable):  # type: ignore
            raise ValueError("The input must be a list or a 1-D numpy array.")

        if not isinstance(v, list):
            v = list(v)

        for i in v:
            if not isinstance(i, (int, float)):
                raise ValueError(
                    f"The input must be a list of integers or floats. You provided a list of {type(i)}"
                )

        if len(v) < 2 or len(v) > 5:
            raise ValueError(
                f"The input must be a list or at least 2 elements (x, y) but not more than 5e lements (c, t, z, x, y). Every additional element is a z value (c, t, z, x, y). You provided a list o {len(v)} elements"
            )

        return cls(v)  # type: ignore

    @classmethod
    def list_from_numpyarray(
        cls,
        x: OneDArray,
        t: Optional[int] = None,
        c: Optional[int] = None,
        z: Optional[int] = None,
    ) -> List["FiveDVector"]:
        """Creates a list of FiveDVectors from a numpy array

        Args:
            vector_list (List[List[float]]): A list of lists of floats

        Returns:
            List[Vectorizable]: A list of InputVector
        """
        assert x.ndim == 2, "Needs to be a List array of vectors"
        if x.shape[1] == 4:
            return [FiveDVector([c] + i) for i in x.tolist()]
        elif x.shape[1] == 3:
            return [FiveDVector([c, t] + i) for i in x.tolist()]
        elif x.shape[1] == 2:
            return [FiveDVector([c, t, z] + i) for i in x.tolist()]
        else:
            raise NotImplementedError(
                f"Incompatible shape {x.shape} of {x}. List dimension needs to either be of size 2 or 3"
            )

    def as_vector(self) -> OneDArray:
        """Convert the FiveDVector to a numpy array."""
        return np.array(self)


class FourByFourMatrix(list[list[float]]):
    """A custom scalar to represent a four by four matrix (e.g 3D affine matrix.)"""

    def __get__(self, instance, owner) -> "FourByFourMatrix": ...  # type: ignore # noqa: ANN001, D105

    def __set__(self, instance, value: FourByFourMatrixCoercible) -> None: ...  # type: ignore # noqa: ANN001, D105

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(list))

    @classmethod
    def validate(cls, v: FourByFourMatrixCoercible) -> "FourByFourMatrix":
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            if not v.ndim == 2:
                raise ValueError("The input array must be a 2D array")
            if not v.shape[0] == v.shape[1]:
                raise ValueError("The input array must be a square matrix")
            if not v.shape == (4, 4):
                raise ValueError("The input array must be a 4x4 matrix")
            clean = [[float(v[i, j]) for j in range(4)] for i in range(4)]
        else:
            clean = v

        if not isinstance(clean, list):  # type: ignore
            raise ValueError(
                f"Expected a list or numpy array, got {type(clean)}. Please provide a 4x4 matrix."
            )

        if len(clean) != 4 or any(len(row) != 4 for row in clean):
            raise ValueError(
                f"Expected a 4x4 matrix, got {len(clean)} rows and {[len(row) for row in clean]} columns."
            )

        for row in clean:
            if not all(isinstance(x, (int, float)) for x in row):  # type: ignore
                raise ValueError("All elements of the 4x4 matrix must be integers or floats.")

        return cls(clean)  # type: ignore

    def as_matrix(self) -> TwoDArray:
        """Convert the FourByFourMatrix to a numpy array."""
        return np.array(self).reshape(4, 4)

    @classmethod
    def from_np(cls, v: TwoDArray) -> "FourByFourMatrix":
        """Validate the input array and convert it to a xr.DataArray."""
        return cls.validate(v)


class ArrayLike:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: xr.DataArray) -> None:
        """Initialize the ArrayLike scalar with an xarray DataArray."""
        self.value = value
        self.key = str(uuid.uuid4())

    def __get__(self, instance, owner) -> "ArrayLike": ...  # noqa: ANN001, D105 #type: ignore

    def __set__(self, instance, value: ArrayCoercible) -> None: ...  # noqa: ANN001, D105 #type: ignore

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: ArrayCoercible) -> "ArrayLike":
        """Validate the input array, preserving its labelled dimensions as-is."""
        return cls(coerce_to_labeled_array(v))

    def __repr__(self) -> str:
        """Return a string representation of the ArrayLike scalar."""
        return f"InputArray({self.value})"


class ImageLike:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: xr.DataArray) -> None:
        """Initialize the ArrayLike scalar with an xarray DataArray."""
        self.value = value
        self.key = str(uuid.uuid4())

    def __get__(self, instance, owner) -> "ImageLike": ...  # noqa: ANN001, D105 #type: ignore

    def __set__(self, instance, value: ArrayCoercible) -> None: ...  # noqa: ANN001, D105 #type: ignore

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: ArrayCoercible) -> "ImageLike":
        """Validate the input array and convert it to a ``ctzyx`` xr.DataArray."""
        return cls(coerce_to_ctzyx(v))

    def __repr__(self) -> str:
        """Return a string representation of the ImageLike scalar."""
        return f"ImageLike({self.value})"


class LabelsLike:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: pd.DataFrame) -> None:
        """Initialize the ArrayLike scalar with an xarray DataArray."""
        self.value = value
        self.key = str(uuid.uuid4())

    def __get__(self, instance, owner) -> "ArrayLike": ...  # noqa: ANN001, D105 #type: ignore

    def __set__(self, instance, value: ArrayCoercible) -> None: ...  # noqa: ANN001, D105 #type: ignore

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: LabelsLikeCoercible) -> "LabelsLike":
        """Validate the input array and convert it to a pandas DataFrame."""
        pd = _require_pandas()
        if isinstance(v, dict):
            mask_to_labels: Dict[int, List[str]] = {}

            for key, value in v.items():
                if not isinstance(key, int):
                    raise ValueError(
                        f"Expected a string or integer key for mask value, got {type(key)}"
                    )

                if isinstance(value, str):
                    value = [value]

                if not isinstance(value, list):
                    raise ValueError(f"Expected a list of strings for key {key}, got {type(value)}")

                if not all(isinstance(i, str) for i in value):
                    raise ValueError(f"Expected a list of strings for key {key}, got {value}")

                mask_to_labels[int(key)] = value

            v = pd.DataFrame.from_dict(mask_to_labels, orient="index")

        if isinstance(v, list):
            assert all(isinstance(i, list) or isinstance(i, str) for i in v), (
                f"Expected a list of lists, got {v}"
            )

            v = pd.DataFrame(v, columns=["label"])

        if not isinstance(v, pd.DataFrame):
            raise ValueError("This needs to be a instance of xarray.DataArray")

        return cls(v)

    def __repr__(self) -> str:
        """Return a string representation of the ArrayLike scalar."""
        return f"InputArray({self.value})"


class BigFile:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: IO[bytes]) -> None:
        """Initialize the BigFile scalar with a file-like object."""
        self.value = value
        self.key = str(value.name)

    def __get__(self, instance, owner) -> "BigFile": ...  # noqa: ANN001, D105 # type: ignore

    def __set__(self, instance, value: FileCoercible) -> None: ...  # noqa: ANN001, D105 # type: ignore

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: FileCoercible) -> "BigFile":
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, str):
            v = open(v, "rb")

        if not isinstance(v, io.IOBase):
            raise ValueError("This needs to be a instance of a file")

        return cls(v)

    def __repr__(self) -> str:
        """Return a string representation of the BigFile scalar."""
        return f"BigFile({self.value})"


class ParquetLike:
    """A custom scalar for ensuring a common format to support write to the
    parquet api supported by mikro_next It converts the passed value into
    a compliant format.."""

    def __init__(self, value: pd.DataFrame) -> None:
        """Initialize the ParquetLike scalar with a pandas DataFrame."""
        self.value = value
        self.key = str(uuid.uuid4())

    def __get__(self, instance, owner) -> "ParquetLike": ...  # noqa: ANN001, D105 # type: ignore

    def __set__(self, instance, value: ParquetCoercible) -> None: ...  # noqa: ANN001, D105 # type: ignore

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: ParquetCoercible) -> "ParquetLike":
        """Validate the validator function"""
        pd = _require_pandas()
        if not isinstance(v, pd.DataFrame):
            raise ValueError("This needs to be a instance of pandas DataFrame")

        return cls(v)

    def __repr__(self) -> str:
        """Return a string representation of the ParquetLike scalar."""
        return f"ParquetLike({self.value})"


class ImageFileLike:
    """A custom scalar for ensuring a common format to support write to the
    parquet api supported by mikro_next It converts the passed value into
    a compliant format.."""

    def __init__(self, value: io.BufferedReader, name: str = "") -> None:
        """Initialize the ImageFileLike scalar with a file-like object."""
        self.value = value
        self.file_name = Path(name).name
        self.mime_type = mimetypes.guess_type(self.file_name)[0]

    def __get__(self, instance, owner) -> "FileLike": ...  # noqa: ANN001, D105 # type: ignore

    def __set__(self, instance, value: FileCoercible) -> None: ...  # noqa: ANN001, D105 # type: ignore

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: FileCoercible) -> "ImageFileLike":
        """Validate the validator function"""

        if isinstance(v, str):
            file = open(v, "rb")
            name = v
        elif isinstance(v, io.IOBase):
            file = v
            name = v.name
        elif isinstance(v, Path):
            file = open(v, "rb")
            name = str(v)
        else:
            raise ValueError(
                f"Unsupported type {type(v)}. Please provide a string or a Path object. Or a file object that is opened in binary mode."
            )

        if not isinstance(file, io.BufferedReader):  # type: ignore
            raise ValueError("This needs to be a instance of a file")

        return cls(file, name=name)

    def __repr__(self) -> str:
        """Return a string representation of the ImageFileLike scalar."""
        return f"FileLike({self.value})"


class FileLike:
    """A custom scalar for ensuring a common format to support write to the
    parquet api supported by mikro_next It converts the passed value into
    a compliant format.."""

    def __init__(self, value: IO[bytes], name: str = "") -> None:
        """Initialize the FileLike scalar with a file-like object."""
        self.value = value
        self.file_name = Path(name).name
        self.mime_type = mimetypes.guess_type(self.file_name)[0]

    def __get__(self, instance, owner) -> "FileLike": ...  # noqa: ANN001, D105 # type: ignore

    def __set__(self, instance, value: FileCoercible) -> None: ...  # noqa: ANN001, D105 # type: ignore

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: FileCoercible) -> "FileLike":
        """Validate the validator function"""

        if isinstance(v, str):
            file = open(v, "rb")
            name = v
        elif isinstance(v, io.IOBase):
            file = v
            name = v.name
        elif isinstance(v, Path):
            file = open(v, "rb")
            name = str(v)
        else:
            raise ValueError(
                f"Unsupported type {type(v)}. Please provide a string or a Path object. Or a file object that is opened in binary mode."
            )

        if not isinstance(file, io.IOBase):  # type: ignore
            raise ValueError("This needs to be a instance of a file")

        return cls(file, name=name)

    def __repr__(self) -> str:
        """Return a string representation of the FileLike scalar."""
        return f"FileLike({self.value})"


class MeshLike:
    """A custom scalar for ensuring a common format to support write to the
    mesh api supported by mikro_next It converts the passed value into
    a compliant format.."""

    def __init__(self, value: IO[bytes], name: str = "") -> None:
        """Initialize the MeshLike scalar with a file-like object."""
        self.value = value
        self.key = str(name)

    def __get__(self, instance, owner) -> "MeshLike":  # noqa: ANN001 # type: ignore
        """Get the MeshLike scalar from the instance."""
        ...

    def __set__(self, instance, value: MeshCoercible):  # noqa: ANN001, ANN204 # type: ignore
        """Set the MeshLike scalar on the instance."""
        ...  # noqa: ANN001

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: MeshCoercible) -> "MeshLike":
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, str):
            file = open(v, "rb")
            name = v
        elif isinstance(v, io.IOBase):
            file = v
            name = "Random Name"
        else:
            file = v
            name = str(v)

        if not isinstance(file, io.BufferedReader):
            raise ValueError("This needs to be a instance of a file")

        return cls(file, name=name)

    def __repr__(self) -> str:
        """Return a string representation of the MeshLike scalar."""
        return f"MeshLike({self.value})"
