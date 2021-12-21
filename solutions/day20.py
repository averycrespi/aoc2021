from collections import defaultdict
from copy import deepcopy
from typing import DefaultDict, Tuple
from helpers import read_input


BUFFER = 25


class Image:
    def __init__(self, pixels: DefaultDict[Tuple[int, int], int]):
        """Create an image from pixels."""
        self.pixels = pixels

    @staticmethod
    def from_lines(lines: list[str]) -> "Image":
        """Create an image from lines."""
        # Down/right are positive, up/left are negative
        pixels = defaultdict(int)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                pixels[(y, x)] = 1 if char == "#" else 0
        return Image(pixels)

    def corners(self) -> Tuple[int, int, int, int]:
        """Find the corners of an image."""
        top = left = bottom = right = 0
        for (y, x), pixel in self.pixels.items():
            if pixel == 1:
                top = min(top, y)
                bottom = max(bottom, y)
                left = min(left, x)
                right = max(right, x)
        return top, bottom, left, right

    def display(self):
        top, bottom, left, right = self.corners()
        for y in range(top, bottom + 1):
            line = []
            for x in range(left, right + 1):
                line.append("#" if self.pixels[(y, x)] == 1 else ".")
            print("".join(line))
        print()

    def apply(self, algorithm: str) -> "Image":
        """Apply an algorithm to an image."""
        output = deepcopy(self.pixels)
        top, bottom, left, right = self.corners()
        for y in range(top - BUFFER, bottom + BUFFER + 1):
            for x in range(left - BUFFER, right + BUFFER + 1):
                neighborhood = [
                    self.pixels[(y, x)]
                    for y, x in [
                        (y - 1, x - 1),
                        (y - 1, x),
                        (y - 1, x + 1),
                        (y, x - 1),
                        (y, x),
                        (y, x + 1),
                        (y + 1, x - 1),
                        (y + 1, x),
                        (y + 1, x + 1),
                    ]
                ]
                lookup = int("".join(map(str, neighborhood)), base=2)
                assert 0 <= lookup <= 512
                output[(y, x)] = 1 if algorithm[lookup] == "#" else 0
        return Image(output)

    def trim(self) -> "Image":
        top, bottom, left, right = self.corners()
        output = defaultdict(int)
        for (y, x), pixel in self.pixels.items():
            if (
                top + BUFFER < y < bottom - BUFFER
                and left + BUFFER < x < right - BUFFER
            ):
                output[(y, x)] = pixel
        return Image(output)

    def count_lit(self) -> int:
        """Count the number of lit pixels."""
        return sum(self.pixels.values())


def part1(image: Image, algorithm: str) -> int:
    """How many pixels are lit in the resulting image?"""
    curr = image
    curr = curr.apply(algorithm)
    curr = curr.apply(algorithm)
    curr = curr.trim()
    return curr.count_lit()


def part2(image: Image, algorithm: str) -> int:
    """How many pixels are lit in the resulting image?"""
    curr = image
    for _ in range(25):
        curr = curr.apply(algorithm).apply(algorithm).trim()
    return curr.count_lit()


# To make the sample work, remove BUFFER
lines = read_input(20)
algorithm = lines[0]
image = Image.from_lines(lines[2:])

print(part1(image, algorithm))
print(part2(image, algorithm))
