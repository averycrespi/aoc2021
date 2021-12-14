from typing import List
from helpers import read_input


def part1(measurements: List[int]) -> int:
    """How many measurements are larger than the previous measurement?"""
    return sum(
        measurements[i] > measurements[i - 1] for i in range(1, len(measurements))
    )


def part2(measurements: List[int]) -> int:
    """How many sums are larger than the previous sum?"""
    return sum(
        measurements[i] > measurements[i - 3] for i in range(3, len(measurements))
    )


measurements = list(map(int, read_input(1, sample=True)))

print(part1(measurements))
print(part2(measurements))
