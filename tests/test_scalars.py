"""Test cases for the FourByFourMatrix scalar and PartialAffineTransformationViewInput schema."""

import numpy as np
import pytest
from mikro_next.scalars import FourByFourMatrix
from mikro_next.api.schema import (
    PartialAffineTransformationViewInput,
)


def test_four_by_four_matrix() -> None:
    """Test the FourByFourMatrix scalar for valid and invalid inputs."""
    # Test valid 4x4 matrix
    valid_matrix = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    assert isinstance(FourByFourMatrix.validate(valid_matrix), list)

    # Test invalid matrix (not 4x4)
    invalid_matrix = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        FourByFourMatrix.validate(invalid_matrix)


def test_partial_affine_transformation_view_input() -> None:
    """Test the PartialAffineTransformationViewInput schema for valid and invalid inputs."""
    # Test valid PartialAffineTransformationViewInput
    PartialAffineTransformationViewInput(
        affineMatrix=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    )

    # Test invalid PartialAffineTransformationViewInput (non-4x4 matrix)

    with pytest.raises(ValueError):
        PartialAffineTransformationViewInput(affineMatrix=np.array([[1, 2], [3, 4]]))
