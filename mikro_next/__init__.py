import logging

from .mikro_next import MikroNext
from .pyramid import build_pyramid, canonical, dataset_arrays, scales_from
from .spaces import create_space, space_2d, space_3d, timelapse_3d
from .utils import rechunk


logger = logging.getLogger(__name__)

try:
    #
    from .arkitekt import MikroService
except ImportError as e:
    try:
        import arkitekt_next

        raise ImportError(
            "Arkitekt is installed, but the MikroService could not be imported. This may indicate a version mismatch or missing dependencies."
        ) from e
    except ImportError:
        pass


try:
    from .rekuest import structure_reg

except ImportError as e:
    try:
        import rekuest_next

        raise ImportError(
            "Rekuest is installed, but the structure_reg could not be imported. This may indicate a version mismatch or missing dependencies."
        ) from e
    except ImportError:
        pass


__all__ = [
    "MikroNext",
    "build_pyramid",
    "canonical",
    "dataset_arrays",
    "scales_from",
    "create_space",
    "space_2d",
    "space_3d",
    "timelapse_3d",
    "rechunk",
    "structure_reg",
    "MikroService",
]
