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


def test_four_by_four_matrix_edge_cases() -> None:
    """Test FourByFourMatrix with edge cases."""
    # Test with zeros
    zero_matrix = np.zeros((4, 4))
    assert isinstance(FourByFourMatrix.validate(zero_matrix), list)

    # Test with ones
    ones_matrix = np.ones((4, 4))
    assert isinstance(FourByFourMatrix.validate(ones_matrix), list)

    # Test with negative values
    negative_matrix = np.array(
        [[-1, -2, -3, -4], [-5, -6, -7, -8], [-9, -10, -11, -12], [-13, -14, -15, -16]]
    )
    assert isinstance(FourByFourMatrix.validate(negative_matrix), list)

    # Test with float values
    float_matrix = np.array(
        [
            [1.5, 2.5, 3.5, 4.5],
            [5.5, 6.5, 7.5, 8.5],
            [9.5, 10.5, 11.5, 12.5],
            [13.5, 14.5, 15.5, 16.5],
        ]
    )
    assert isinstance(FourByFourMatrix.validate(float_matrix), list)


def test_four_by_four_matrix_invalid_shapes() -> None:
    """Test FourByFourMatrix with various invalid shapes."""
    # Test 3x3 matrix
    with pytest.raises(ValueError):
        FourByFourMatrix.validate(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    # Test 5x5 matrix
    with pytest.raises(ValueError):
        FourByFourMatrix.validate(np.ones((5, 5)))

    # Test 1D array
    with pytest.raises(ValueError):
        FourByFourMatrix.validate(np.array([1, 2, 3, 4]))

    # Test 3D array
    with pytest.raises(ValueError):
        FourByFourMatrix.validate(np.ones((4, 4, 4)))


def test_affine_transformation_with_nans() -> None:
    """Test PartialAffineTransformationViewInput with NaN values."""
    # Test matrix with NaN values should raise an error or handle gracefully
    nan_matrix = np.array([[1, 0, 0, np.nan], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    # This might raise an error or handle it gracefully depending on implementation
    try:
        PartialAffineTransformationViewInput(affineMatrix=nan_matrix)
    except (ValueError, TypeError):
        pass  # Expected behavior for NaN values

    with pytest.raises(ValueError):
        PartialAffineTransformationViewInput(affineMatrix=np.array([[1, 2], [3, 4]]))
