import pytest
from typing import List

# Assuming the functions are imported from your assignment file
from assignment2 import mirror, grey, invert, merge, compress


# --------------------------------------------------------------------------
# Tests for mirror (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        # Basic 2x3 image
        (
            [
                [[233, 100, 115], [0, 0, 0], [255, 255, 255]],
                [[199, 201, 116], [1, 9, 0], [255, 255, 255]],
            ],
            [
                [[255, 255, 255], [0, 0, 0], [233, 100, 115]],
                [[255, 255, 255], [1, 9, 0], [199, 201, 116]],
            ],
        ),
        # Single row
        (
            [[[100, 50, 25], [200, 150, 100], [50, 50, 50]]],
            [[[50, 50, 50], [200, 150, 100], [100, 50, 25]]],
        ),
        # Single column (should remain same)
        (
            [[[100, 100, 100]], [[200, 200, 200]], [[50, 50, 50]]],
            [[[100, 100, 100]], [[200, 200, 200]], [[50, 50, 50]]],
        ),
        # Square 3x3 image
        (
            [
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
                [[19, 20, 21], [22, 23, 24], [25, 26, 27]],
            ],
            [
                [[7, 8, 9], [4, 5, 6], [1, 2, 3]],
                [[16, 17, 18], [13, 14, 15], [10, 11, 12]],
                [[25, 26, 27], [22, 23, 24], [19, 20, 21]],
            ],
        ),
        # Single pixel
        ([[[128, 128, 128]]], [[[128, 128, 128]]]),
        # Two pixels per row
        (
            [[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]],
            [[[0, 255, 0], [255, 0, 0]], [[255, 255, 0], [0, 0, 255]]],
        ),
    ],
)
def test_mirror_pass(raw, expected):
    """Tests cases where mirror should correctly reverse rows."""
    mirror(raw)
    assert raw == expected


@pytest.mark.parametrize(
    "raw, not_expected",
    [
        # Should NOT remain unchanged (testing it actually mirrors)
        ([[[100, 100, 100], [200, 200, 200]]], [[[100, 100, 100], [200, 200, 200]]]),
        # Should NOT produce this incorrect result
        (
            [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
            [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
        ),
        # Should NOT keep original order
        (
            [[[255, 0, 0], [0, 255, 0], [0, 0, 255]]],
            [[[255, 0, 0], [0, 255, 0], [0, 0, 255]]],
        ),
    ],
)
def test_mirror_fail(raw, not_expected):
    """Tests that mirror does not produce incorrect results."""
    mirror(raw)
    assert raw != not_expected


# --------------------------------------------------------------------------
# Tests for grey (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        # Basic greyscale conversion
        (
            [
                [[233, 100, 115], [0, 0, 0], [255, 255, 255]],
                [[199, 201, 116], [1, 9, 0], [255, 255, 255]],
            ],
            [
                [[149, 149, 149], [0, 0, 0], [255, 255, 255]],
                [[172, 172, 172], [3, 3, 3], [255, 255, 255]],
            ],
        ),
        # Already grey pixels
        (
            [[[100, 100, 100], [50, 50, 50]], [[200, 200, 200], [0, 0, 0]]],
            [[[100, 100, 100], [50, 50, 50]], [[200, 200, 200], [0, 0, 0]]],
        ),
        # Integer division test (10+10+11)/3 = 10.33... -> 10
        (
            [[[10, 10, 11], [5, 5, 5]], [[100, 101, 102], [7, 8, 9]]],
            [[[10, 10, 10], [5, 5, 5]], [[101, 101, 101], [8, 8, 8]]],
        ),
        # Single pixel
        ([[[60, 120, 180]]], [[[120, 120, 120]]]),
        # Extreme RGB values
        (
            [
                [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
                [[255, 255, 0], [255, 0, 255], [0, 255, 255]],
            ],
            [
                [[85, 85, 85], [85, 85, 85], [85, 85, 85]],
                [[170, 170, 170], [170, 170, 170], [170, 170, 170]],
            ],
        ),
        # Testing (1+2+3)/3 = 2
        ([[[1, 2, 3]]], [[[2, 2, 2]]]),
    ],
)
def test_grey_pass(raw, expected):
    """Tests cases where grey should correctly average RGB values."""
    grey(raw)
    assert raw == expected


@pytest.mark.parametrize(
    "raw, not_expected",
    [
        # Should NOT use regular division (would be 10.33, not 10)
        ([[[10, 10, 11]]], [[[10.33, 10.33, 10.33]]]),
        # Should NOT remain unchanged when colors differ
        ([[[255, 0, 0]]], [[[255, 0, 0]]]),
        # Should NOT produce wrong average
        ([[[100, 200, 150]]], [[[100, 100, 100]]]),  # Wrong average
    ],
)
def test_grey_fail(raw, not_expected):
    """Tests that grey does not produce incorrect results."""
    grey(raw)
    assert raw != not_expected


# --------------------------------------------------------------------------
# Tests for invert (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        # Basic inversion
        (
            [
                [[233, 100, 115], [0, 0, 0], [255, 255, 0]],
                [[199, 201, 116], [1, 9, 0], [255, 100, 100]],
            ],
            [
                [[100, 233, 115], [0, 0, 0], [0, 0, 255]],
                [[199, 116, 201], [1, 0, 9], [100, 255, 255]],
            ],
        ),
        # All same values (no change)
        (
            [[[100, 100, 100], [50, 50, 50]], [[200, 200, 200], [0, 0, 0]]],
            [[[100, 100, 100], [50, 50, 50]], [[200, 200, 200], [0, 0, 0]]],
        ),
        # Two identical values
        (
            [[[100, 100, 50], [200, 150, 200]], [[75, 75, 200], [0, 50, 0]]],
            [[[50, 50, 100], [150, 200, 150]], [[200, 200, 75], [50, 0, 50]]],
        ),
        # Extreme values
        (
            [[[255, 0, 128], [0, 255, 255]], [[100, 200, 150], [50, 50, 250]]],
            [[[0, 255, 128], [255, 0, 0]], [[200, 100, 150], [250, 250, 50]]],
        ),
        # Single pixel
        ([[[100, 200, 150]]], [[[200, 100, 150]]]),
        # All max and min distinct
        ([[[10, 50, 200]]], [[[200, 50, 10]]]),
    ],
)
def test_invert_pass(raw, expected):
    """Tests cases where invert should correctly swap min/max values."""
    invert(raw)
    assert raw == expected


@pytest.mark.parametrize(
    "raw, not_expected",
    [
        # Should NOT invert all values (255-value)
        (
            [[[100, 200, 150]]],
            [[[155, 55, 105]]],  # Wrong - this is 255-value inversion
        ),
        # Should NOT remain unchanged when values differ
        ([[[100, 200, 50]]], [[[100, 200, 50]]]),
        # Should NOT swap incorrectly
        ([[[255, 0, 128]]], [[[255, 128, 0]]]),  # Wrong swap pattern
    ],
)
def test_invert_fail(raw, not_expected):
    """Tests that invert does not produce incorrect results."""
    invert(raw)
    assert raw != not_expected


# --------------------------------------------------------------------------
# Tests for merge (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw1, raw2, expected",
    [
        # Same size images - alternates by row (even=raw1, odd=raw2)
        (
            [[[100, 0, 0], [0, 100, 0]], [[0, 0, 100], [100, 100, 0]]],
            [[[50, 50, 50], [150, 150, 150]], [[200, 200, 200], [250, 250, 250]]],
            [[[100, 0, 0], [0, 100, 0]], [[200, 200, 200], [250, 250, 250]]],
        ),
        # raw1 larger than raw2
        (
            [
                [[100, 100, 100], [150, 150, 150], [200, 200, 200]],
                [[50, 50, 50], [75, 75, 75], [100, 100, 100]],
            ],
            [[[255, 0, 0]], [[0, 255, 0]]],
            [
                [[100, 100, 100], [150, 150, 150], [200, 200, 200]],
                [[0, 255, 0], [75, 75, 75], [100, 100, 100]],
            ],
        ),
        # raw2 larger than raw1
        (
            [[[100, 0, 0]], [[0, 100, 0]]],
            [
                [[50, 50, 50], [100, 100, 100], [150, 150, 150]],
                [[200, 200, 200], [250, 250, 250], [255, 255, 255]],
                [[10, 10, 10], [20, 20, 20], [30, 30, 30]],
            ],
            [
                [[100, 0, 0], [100, 100, 100], [150, 150, 150]],
                [[200, 200, 200], [250, 250, 250], [255, 255, 255]],
                [[10, 10, 10], [20, 20, 20], [30, 30, 30]],
            ],
        ),
        # Black pixels fill empty spaces
        (
            [[[255, 255, 255]]],
            [[[100, 100, 100], [0, 0, 0]], [[50, 50, 50], [75, 75, 75]]],
            [[[255, 255, 255], [0, 0, 0]], [[50, 50, 50], [75, 75, 75]]],
        ),
        # Both images different sizes, gaps filled with black
        (
            [[[10, 20, 30]]],
            [[[40, 50, 60]], [[70, 80, 90]], [[100, 110, 120]]],
            [[[10, 20, 30]], [[70, 80, 90]], [[100, 110, 120]]],
        ),
        # Single pixel each
        ([[[100, 100, 100]]], [[[200, 200, 200]]], [[[100, 100, 100]]]),
    ],
)
def test_merge_pass(raw1, raw2, expected):
    """Tests cases where merge should correctly combine images."""
    result = merge(raw1, raw2)
    assert result == expected


@pytest.mark.parametrize(
    "raw1, raw2, not_expected",
    [
        # Should NOT just concatenate
        ([[[100, 0, 0]]], [[[0, 100, 0]]], [[[100, 0, 0]], [[0, 100, 0]]]),
        # Should NOT ignore raw1
        ([[[100, 100, 100]]], [[[200, 200, 200]]], [[[200, 200, 200]]]),
        # Should NOT use wrong alternation pattern
        (
            [[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]],
            [[[5, 5, 5], [6, 6, 6]], [[7, 7, 7], [8, 8, 8]]],
            [
                [[5, 5, 5], [6, 6, 6]],
                [[3, 3, 3], [4, 4, 4]],
            ],  # Wrong - should use row index not alternate pattern
        ),
    ],
)
def test_merge_fail(raw1, raw2, not_expected):
    """Tests that merge does not produce incorrect results."""
    result = merge(raw1, raw2)
    assert result != not_expected


# --------------------------------------------------------------------------
# Tests for compress (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        # Basic 4x4 compression
        (
            [
                [[233, 100, 115], [0, 0, 0], [255, 255, 0], [3, 6, 7]],
                [[199, 201, 116], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
                [[200, 200, 200], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
                [[50, 100, 150], [1, 9, 0], [211, 5, 22], [199, 0, 10]],
            ],
            [[[108, 77, 57], [153, 115, 26]], [[63, 79, 87], [191, 51, 33]]],
        ),
        # 3x3 image (edge cases)
        (
            [
                [[233, 100, 115], [0, 0, 0], [255, 255, 0]],
                [[199, 201, 116], [1, 9, 0], [255, 100, 100]],
                [[123, 233, 151], [111, 99, 10], [0, 1, 1]],
            ],
            [[[108, 77, 57], [255, 177, 50]], [[117, 166, 80], [0, 1, 1]]],
        ),
        # 2x2 image
        (
            [[[100, 100, 100], [200, 200, 200]], [[50, 50, 50], [150, 150, 150]]],
            [[[125, 125, 125]]],
        ),
        # Single pixel
        ([[[100, 150, 200]]], [[[100, 150, 200]]]),
        # 1x2 image (single row, multiple columns)
        ([[[100, 100, 100], [200, 200, 200]]], [[[150, 150, 150]]]),
        # 2x1 image (multiple rows, single column)
        ([[[100, 100, 100]], [[200, 200, 200]]], [[[150, 150, 150]]]),
    ],
)
def test_compress_pass(raw, expected):
    """Tests cases where compress should correctly reduce image size."""
    result = compress(raw)
    assert result == expected


@pytest.mark.parametrize(
    "raw, not_expected",
    [
        # Should NOT keep same size
        (
            [[[100, 100, 100], [200, 200, 200]], [[50, 50, 50], [150, 150, 150]]],
            [[[100, 100, 100], [200, 200, 200]], [[50, 50, 50], [150, 150, 150]]],
        ),
        # Should NOT use wrong averaging
        (
            [[[100, 100, 100], [200, 200, 200]], [[100, 100, 100], [200, 200, 200]]],
            [[[100, 100, 100]]],  # Wrong - should be 150
        ),
        # Should NOT produce wrong dimensions
        ([[[1, 1, 1], [2, 2, 2], [3, 3, 3]]], [[[1, 1, 1], [2, 2, 2]]]),  # Wrong size
    ],
)
def test_compress_fail(raw, not_expected):
    """Tests that compress does not produce incorrect results."""
    result = compress(raw)
    assert result != not_expected
