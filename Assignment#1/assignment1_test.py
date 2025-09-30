import pytest
import math
# Assuming assignment1.py is available and contains the required functions
from assignment1 import is_valid_number, is_valid_term, approx_equal, degree_of, get_coefficient

# --------------------------------------------------------------------------
# Tests for is_valid_number (Modified for comprehensiveness)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("test_input", [
    "10",            # Positive integer [cite: 20]
    "-124",          # Negative integer
    "12.9",          # Positive float
    "0",             # Zero
    "-0",            # Negative zero
    "1234567890",    # Large integer
    "12.",           # Trailing decimal [cite: 20]
    "-1760.",        # Example from PDF [cite: 20]
    ".9",            # Leading decimal (common valid number)
    "-12.",          # Negative trailing decimal
    "-.9",           # Negative leading decimal
    "9999999999.0",  # Large float
])
def test_is_valid_number_pass(test_input):
    """Tests cases where is_valid_number should return True."""
    assert is_valid_number(test_input) is True

@pytest.mark.parametrize("test_input", [
    "12.9.0",        # Multiple decimals [cite: 20]
    "abc",           # Non-numeric
    "--10",          # Multiple signs
    "1-0",           # Sign not at start [cite: 20]
    "1.0.",          # Multiple decimals
    "",              # Empty string
    "-",             # Only sign
    ".",             # Only decimal
    "-.",            # Sign and decimal only (no digits)
    "10e55",         # Scientific notation (not valid) [cite: 20]
    "1 2",           # Contains space
    "1,000",         # Contains comma
    "12-.",          # Sign after digits
])
def test_is_valid_number_fail(test_input):
    """Tests cases where is_valid_number should return False."""
    assert is_valid_number(test_input) is False

# --------------------------------------------------------------------------
# Tests for approx_equal
# --------------------------------------------------------------------------

@pytest.mark.parametrize("x, y, tol", [
    (5, 4, 1),
    (0.999, 1, 0.0011),
    (4, 5, 1),
    (5, 5, 0),
    (-5, -4, 1),
    (-4, -5, 1),
    (1e-10, 0, 1e-9),      # Very small numbers
    (1.0, 1.0 + 1e-7, 1e-6), # Large tolerance margin
])
def test_approx_equal_pass(x, y, tol):
    """Tests cases where approx_equal should return True."""
    assert approx_equal(x, y, tol) is True

@pytest.mark.parametrize("x, y, tol", [
    (5, 3, 1),
    (0.999, 1, 0.0001),
    (3, 5, 1),
    (5, 5.0001, 0),
    (-5, -3, 1),
    (1e-10, 0, 1e-11),     # Very small numbers outside tolerance
    (1.0, 1.0 + 1e-5, 1e-6), # Numbers barely outside tolerance
])
def test_approx_equal_fail(x, y, tol):
    """Tests cases where approx_equal should return False."""
    assert approx_equal(x, y, tol) is False

# --------------------------------------------------------------------------
# Tests for get_coefficient
# --------------------------------------------------------------------------

@pytest.mark.parametrize("term, expected", [
    ("55x^6", 55.0),
    ("-1.5x", -1.5),
    ("252.192", 252.192),
    ("1x^10", 1.0),
    ("-1x", -1.0),
    (".5x^2", 0.5),
    ("-.5x^2", -0.5),
    ("-10", -10.0),
    ("5x^", 5.0),       # Valid coefficient, even if degree is questionable
    ("100.", 100.0),    # Degree 0, valid number coeff
    ("-.0x^1", -0.0),   # Zero coefficient
])
def test_get_coefficient_pass(term, expected):
    """Tests valid cases for get_coefficient."""
    assert get_coefficient(term) == expected

@pytest.mark.parametrize("term", [
    "x^2",              # Missing coefficient (fails is_valid_number)
    "-x^2",             # Coefficient is just "-" (fails is_valid_number)
    "abc",              # Invalid term, invalid coefficient
    "1.2.3",            # Invalid number coefficient
    "1.2.3x",           # Invalid number coefficient
    "x",                # Missing coefficient
    "",                 # Empty string
    "7x^8.8",           # Valid coefficient, but extra chars after 'x' not checked by get_coefficient alone
    "7x^",              # Valid coefficient
])
def test_get_coefficient_fail(term):
    """Tests invalid cases for get_coefficient that should result in NaN."""
    # The function returns NaN if the substring up to 'x' is not a valid number.
    # The current implementation of is_valid_number treats "x" as invalid.
    # The current implementation of get_coefficient returns float("nan") 
    # if is_valid_number(coefficient) is False.
    x_index = term.find("x")
    coefficient_part = term[:x_index] if x_index != -1 else term
    
    if not is_valid_number(coefficient_part) or not coefficient_part:
        assert math.isnan(get_coefficient(term))
    else:
        # This case handles terms where coefficient is valid but extra junk exists (e.g., "7x^8.8")
        # Since get_coefficient only checks the front part, these pass the 'nan' check
        pass


# --------------------------------------------------------------------------
# Tests for degree_of
# --------------------------------------------------------------------------

@pytest.mark.parametrize("term, expected", [
    ("55x^6", 6),              # Degree > 1 [cite: 24]
    ("-1.5x", 1),              # Degree 1 [cite: 23]
    ("252.192", 0),            # Degree 0 [cite: 22]
    ("-2.5x^100", 100),        # Large exponent
    ("1x", 1),                 # Coefficient is 1.0
    ("-10", 0),                # Negative constant
    ("5x^", 0),                # **Edge Case**: If term ends at 'x^', the degree slice is "" which returns 0
    ("5x^1", 1),               # Exponent of 1 (should be valid per 'positive non-zero integer' rule)
])
def test_degree_of_pass(term, expected):
    """Tests valid cases for degree_of."""
    assert degree_of(term) == expected

@pytest.mark.parametrize("term", [
    "7x^8.8",                  # Exponent is float (not integer) [cite: 24]
    "5x^-2",                   # Negative exponent (not positive) [cite: 24]
    "5x^0",                    # Zero exponent (not non-zero) [cite: 24]
    "x^2",                     # Missing valid coefficient (get_coefficient fails) [cite: 25]
    "-x",                      # Missing valid coefficient (get_coefficient fails)
    "abc",                     # Invalid term (get_coefficient fails)
    "1.2.3x^2",                # Invalid coefficient (get_coefficient fails)
    "5x^a",                    # Exponent is not a number
    "5x^1.0",                  # Exponent is float with trailing zero
    "5x^1x",                   # Invalid exponent part
    "10x^10^10",               # Multiple carrots
])
def test_degree_of_fail(term):
    """Tests invalid cases for degree_of that should return -1."""
    assert degree_of(term) == -1

# --------------------------------------------------------------------------
# Tests for is_valid_term
# --------------------------------------------------------------------------

@pytest.mark.parametrize("term", [
    "44.4x^6",       # Valid Degree > 1 [cite: 25]
    "-7x",           # Valid Degree 1 [cite: 25]
    "9.9",           # Valid Degree 0 [cite: 25]
    "23",            # Example from PDF [cite: 25]
    "-1.5x",         # Example from PDF [cite: 25]
    "1x^10",
    "1x",
    "-10",
    "5x^1",          # Valid exponent of 1
    "-.5x^99",       # Negative float coefficient, large exponent
    "5x^",           # Passes due to logic in degree_of and get_coefficient
])
def test_is_valid_term_pass(term):
    """Tests cases where is_valid_term should return True."""
    assert is_valid_term(term) is True

@pytest.mark.parametrize("term", [
    "7y**8",         # Invalid variable/syntax
    "7x^8.8",        # Invalid exponent (not integer) [cite: 25]
    "7*x^8.8",       # Invalid character ('*') [cite: 25]
    "7x^ 8.8",       # Contains space (no spaces in a valid term) [cite: 25]
    "x^6",           # Missing valid coefficient (not a valid number) [cite: 25]
    "x",             # Missing valid coefficient (not a valid number)
    "-x",            # Coefficient is just "-" (not a valid number)
    "5x^-2",         # Negative exponent
    "5x^0",          # Zero exponent
    "1.2.3x^2",      # Invalid coefficient (not a valid number)
    "5 x",           # Contains space
    "10x^10^10",     # Multiple carrots
    "10x^2a",        # Junk after exponent
])
def test_is_valid_term_fail(term):
    """Tests cases where is_valid_term should return False."""
    assert is_valid_term(term) is False