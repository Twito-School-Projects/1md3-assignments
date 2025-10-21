import pytest
import math

# Assuming assignment1.py is available and contains the required functions
from assignment1 import (
    is_valid_number,
    is_valid_term,
    approx_equal,
    degree_of,
    get_coefficient,
)

# --------------------------------------------------------------------------
# Tests for is_valid_number (Aligned with TA requirements)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "test_input",
    [
        "10",  # Positive integer
        "-124",  # Negative integer
        "12.9",  # Positive float
        "0",  # Zero
        "-0",  # Negative zero
        "1234567890",  # Large integer
        "9999999999.0",  # Large float
    ],
)
def test_is_valid_number_pass(test_input):
    """Tests cases where is_valid_number should return True."""
    assert is_valid_number(test_input) is True


@pytest.mark.parametrize(
    "test_input",
    [
        "12.9.0",  # Multiple decimals
        "abc",  # Non-numeric
        "--10",  # Multiple signs (TA: invalid)
        "1-0",  # Sign not at start
        "1.0.",  # Multiple decimals
        "",  # Empty string
        "-",  # Only sign (TA: invalid)
        ".",  # Only decimal (TA: invalid)
        "-.",  # Sign and decimal only (TA: invalid)
        "10e55",  # Scientific notation (not valid)
        "1 2",  # Contains space (TA: invalid)
        "1,000",  # Contains comma (TA: invalid)
        "12-.",  # Sign after digits
        " 5",  # Leading space (TA: invalid)
        "5 ",  # Trailing space (TA: invalid)
        " 5 ",  # Spaces around (TA: invalid)
    ],
)
def test_is_valid_number_fail(test_input):
    """Tests cases where is_valid_number should return False."""
    assert is_valid_number(test_input) is False


# --------------------------------------------------------------------------
# Tests for approx_equal
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "x, y, tol",
    [
        (5, 4, 1),
        (0.999, 1, 0.0011),
        (4, 5, 1),
        (5, 5, 0),
        (-5, -4, 1),
        (-4, -5, 1),
        (1e-10, 0, 1e-9),  # Very small numbers
        (1.0, 1.0 + 1e-7, 1e-6),  # Large tolerance margin
    ],
)
def test_approx_equal_pass(x, y, tol):
    """Tests cases where approx_equal should return True."""
    assert approx_equal(x, y, tol) is True


@pytest.mark.parametrize(
    "x, y, tol",
    [
        (5, 3, 1),
        (0.999, 1, 0.0001),
        (3, 5, 1),
        (5, 5.0001, 0),
        (-5, -3, 1),
        (1e-10, 0, 1e-11),  # Very small numbers outside tolerance
        (1.0, 1.0 + 1e-5, 1e-6),  # Numbers barely outside tolerance
    ],
)
def test_approx_equal_fail(x, y, tol):
    """Tests cases where approx_equal should return False."""
    assert approx_equal(x, y, tol) is False


# --------------------------------------------------------------------------
# Tests for get_coefficient (ASSUMES VALID INPUT)
# Note: Leading/trailing decimals won't be tested per TA
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "term, expected",
    [
        ("55x^6", 55.0),
        ("-1.5x", -1.5),
        ("252.192", 252.192),
        ("1x^10", 1.0),
        ("-1x", -1.0),
        ("-10", -10.0),
        ("5x^1", 5.0),
    ],
)
def test_get_coefficient_pass(term, expected):
    """Tests valid cases for get_coefficient (assumes valid terms only)."""
    assert get_coefficient(term) == expected


# --------------------------------------------------------------------------
# Tests for degree_of (ASSUMES VALID INPUT)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "term, expected",
    [
        ("55x^6", 6),
        ("-1.5x", 1),
        ("252.192", 0),
        ("-2.5x^100", 100),
        ("1x", 1),
        ("-10", 0),
        ("5x^1", 1),
    ],
)
def test_degree_of_pass(term, expected):
    """Tests valid cases for degree_of (assumes valid terms only)."""
    assert degree_of(term) == expected


# --------------------------------------------------------------------------
# Tests for is_valid_term (Aligned with TA requirements)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "term",
    [
        "44.4x^6",  # Valid Degree > 1
        "-7x",  # Valid Degree 1
        "9.9",  # Valid Degree 0
        "23",  # Example from PDF
        "-1.5x",  # Example from PDF
        "1x^10",
        "1x",
        "-10",
        "5x^1",  # Valid exponent of 1
        "2.5x^99",  # Float coefficient, large exponent
    ],
)
def test_is_valid_term_pass(term):
    """Tests cases where is_valid_term should return True."""
    assert is_valid_term(term) is True


@pytest.mark.parametrize(
    "term",
    [
        "7y**8",  # Invalid variable/syntax
        "7x^8.8",  # Invalid exponent (not integer)
        "7*x^8.8",  # Invalid character ('*')
        "7x^ 8.8",  # Contains space (TA: invalid)
        "x^6",  # Missing valid coefficient
        "x",  # Missing valid coefficient
        "-x",  # Coefficient is just "-" (TA: invalid)
        "5x^-2",  # Negative exponent (TA: invalid)
        "5x^0",  # Zero exponent (must be positive non-zero)
        "1.2.3x^2",  # Invalid coefficient (multiple decimals)
        "5 x",  # Contains space (TA: invalid)
        "10x^10^10",  # Multiple carets
        "10x^2a",  # Junk after exponent
        "5x^",  # Empty exponent
        "",  # Empty string
        "--5x",  # Multiple negatives (TA: invalid)
        " 5x",  # Leading space (TA: invalid)
        "5x ",  # Trailing space (TA: invalid)
    ],
)
def test_is_valid_term_fail(term):
    """Tests cases where is_valid_term should return False."""
    assert is_valid_term(term) is False
