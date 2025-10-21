from PIL import Image
from typing import List


def mirror(raw: List[List[List[int]]]) -> None:
    """
    Assume raw is image data. Modifies raw by reversing all the rows
    of the data.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 255]],
               [[199, 201, 116], [1, 9, 0], [255, 255, 255]]]
    >>> mirror(raw)
    >>> raw
    [[[255, 255, 255], [0, 0, 0], [233, 100, 115]],
     [[255, 255, 255], [1, 9, 0], [199, 201, 116]]]
    """
    # TODO

    for image_row in raw:
        image_row = image_row.reverse()


def grey(raw: List[List[List[int]]]) -> None:
    """
    Assume raw is image data. Modifies raw "averaging out" each
    pixel of raw. Specifically, for each pixel it totals the RGB
    values, integer divides by three, and sets the all RGB values
    equal to this new value

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 255]],
               [[199, 201, 116], [1, 9, 0], [255, 255, 255]]]
    >>> grey(raw)
    >>> raw
    [[[149, 149, 149], [0, 0, 0], [255, 255, 255]],
     [[172, 172, 172], [3, 3, 3], [255, 255, 255]]]
    """

    for image_row in raw:
        for pixel in image_row:
            average = sum(pixel) // 3

            for i in range(len(pixel)):
                pixel[i] = average


def invert(raw: List[List[List[int]]]) -> None:
    """
    Assume raw is image data. Modifies raw inverting each pixel.
    To invert a pixel, you swap all the max values, with all the
    minimum values. See the doc tests for examples.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100]]]
    >>> invert(raw)
    >>> raw
    [[[100, 233, 115], [0, 0, 0], [0, 0, 255]],
        [[199, 116, 201], [1, 0, 9], [100, 255, 255]]]
    """

    for image in raw:
        for pixel in image:
            max_colour = max(pixel)
            min_colour = min(pixel)

            for i in range(len(pixel)):
                if pixel[i] == min_colour:
                    pixel[i] = max_colour
                elif pixel[i] == max_colour:
                    pixel[i] = min_colour

    return


def merge(
    raw1: List[List[List[int]]], raw2: List[List[List[int]]]
) -> List[List[List[int]]]:
    """
    Merges raw1 and raw2 into new raw image data and returns it.
    It merges them using the following rule/procedure.
    1) The new raw image data has height equal to the max height of raw1 and raw2
    2) The new raw image data has width equal to the max width of raw1 and raw2
    3) The pixel data at cell (i,j) in the new raw image data will be (in this order):
       3.1) a black pixel [0, 0, 0], if there is no pixel data in raw1 or raw2
       at cell (i,j)
       3.2) raw1[i][j] if there is no pixel data at raw2[i][j]
       3.3) raw2[i][j] if there is no pixel data at raw1[i][j]
       3.4) raw1[i][j] if i is even
       3.5) raw2[i][j] if i is odd
    """
    height = max(len(raw1), len(raw2))
    width = max(len(raw1[0]) if raw1 else 0, len(raw2[0]) if raw2 else 0)

    merged_output = []
    for image_row in range(height):
        merged_output.append([])

        for pixel_col in range(width):
            raw1_has_row = len(raw1) > image_row
            raw2_has_row = len(raw2) > image_row
            raw1_has_pixel = raw1_has_row and pixel_col < len(raw1[image_row])
            raw2_has_pixel = raw2_has_row and pixel_col < len(raw2[image_row])

            if not raw1_has_pixel and not raw2_has_pixel:
                merged_output[image_row][pixel_col] = [0, 0, 0]  # black pixel

            elif not raw2_has_pixel:
                merged_output[image_row].append(raw1[image_row][pixel_col])
            elif not raw1_has_pixel:
                merged_output[image_row].append(raw2[image_row][pixel_col])

            elif image_row % 2 == 0:
                merged_output[image_row].append(raw1[image_row][pixel_col])
            else:
                merged_output[image_row].append(raw2[image_row][pixel_col])
    return merged_output


def compress(raw: List[List[List[int]]]) -> List[List[List[int]]]:
    """
    Compresses raw by going through the pixels and combining a pixel with
    the ones directly to the right, below and diagonally to the lower right.
    For each RGB values it takes the average of these four pixels using integer
    division. If is is a pixel on the "edge" of the image, it only takes the
    relevant pixels to average across. See the second doctest for an example of
    this.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0], [3, 6, 7]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
               [[200, 200, 200], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
               [[50, 100, 150], [1, 9, 0], [211, 5, 22], [199, 0, 10]]]
    >>> raw1 = compress(raw)
    >>> raw1
    [[[108, 77, 57], [153, 115, 26]],
     [[63, 79, 87], [191, 51, 33]]]

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100]],
               [[123, 233, 151], [111, 99, 10], [0, 1, 1]]]
    >>> raw2 = compress(raw)
    >>> raw2
    [[[108, 77, 57], [255, 177, 50]],
     [[117, 166, 80], [0, 1, 1]]]
    """

    height = len(raw)
    width = len(raw[0]) if len(raw) > 0 else 0

    compressed_output = []
    for image_row in range(0, height, 2):
        compressed_output.append([])

        for pixel_col in range(0, width, 2):
            left_most_pixel = raw[image_row][pixel_col]
            data_to_process = [left_most_pixel]

            if len(raw) > image_row + 1:
                bottom_pixel = raw[image_row + 1][pixel_col]
                data_to_process.append(bottom_pixel)

            if len(raw[image_row]) > pixel_col + 1:
                right_pixel = raw[image_row][pixel_col + 1]
                data_to_process.append(right_pixel)

            if len(raw) > image_row + 1 and len(raw[image_row + 1]) > pixel_col + 1:
                down_right_pixel = raw[image_row + 1][pixel_col + 1]
                data_to_process.append(down_right_pixel)

            processed_pixel = [0, 0, 0]
            for pixel in data_to_process:
                processed_pixel[0] += pixel[0]
                processed_pixel[1] += pixel[1]
                processed_pixel[2] += pixel[2]

            # yes i am well aware that we haven't learnt lambdas yet
            processed_pixel = list(map(lambda x: x // len(data_to_process), processed_pixel))
            compressed_output[image_row // 2].append(processed_pixel)

    # dont worry about the space complexity
    return compressed_output


"""
**********************************************************

Do not worry about the code below. However, if you wish,
you can us it to read in images, modify the data, and save
new images.

**********************************************************
"""


def get_raw_image(name: str) -> List[List[List[int]]]:
    image = Image.open(name)
    num_rows = image.height
    num_columns = image.width
    pixels = image.getdata()
    new_data = []

    for i in range(num_rows):
        new_row = []
        for j in range(num_columns):
            new_pixel = list(pixels[i * num_columns + j])
            new_row.append(new_pixel)
        new_data.append(new_row)

    image.close()
    return new_data


def image_from_raw(raw: List[List[List[int]]], name: str) -> None:
    image = Image.new("RGB", (len(raw[0]), len(raw)))
    pixels = []
    for row in raw:
        for pixel in row:
            pixels.append(tuple(pixel))
    image.putdata(pixels)
    image.save(name)


# my own custom function
def test(base_file: str):
    mirrored = get_raw_image(base_file + ".jpg")
    inverted = get_raw_image(base_file + ".jpg")
    grayscaled = get_raw_image(base_file + ".jpg")
    compressed = get_raw_image(base_file + ".jpg")

    invert(inverted)
    grey(grayscaled)
    mirror(mirrored)
    compress(compressed)

    image_from_raw(mirrored, base_file + "-mirrored.jpg")
    image_from_raw(inverted, base_file + "-inverted.jpg")
    image_from_raw(grayscaled, base_file + "-grayscaled.jpg")
    image_from_raw(compressed, base_file + "-compressed.jpg")


# test("assets/lotus1/lotus")
# test("assets/lotus2/lotus")