import logging

from .mikro_next import MikroNext
from .utils import rechunk


logger = logging.getLogger(__name__)

try:
    #
    from .arkitekt import MikroService
except ImportError as e:
    try:
        import arkitekt

        raise ImportError(
            "Arkitekt is installed, but the MikroService could not be imported. This may indicate a version mismatch or missing dependencies."
        ) from e
    except ImportError:
        pass


try:
    from .rekuest import structure_reg

except ImportError as e:
    logger.debug("Could not import structure_reg", e)
    pass


__all__ = [
    "MikroNext",
    "rechunk",
    "structure_reg",
    "MikroService",
]
