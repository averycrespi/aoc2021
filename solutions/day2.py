from typing import List
from helpers import read_input


def part1(lines: List[str]) -> int:
    """What do you get if you multiply your final horizontal position by your final depth?"""
    position = depth = 0
    for line in lines:
        direction, raw_amount = line.split()
        amount = int(raw_amount)
        if direction == "forward":
            position += amount
        elif direction == "up":
            depth -= amount
        elif direction == "down":
            depth += amount
    return position * depth


def part2(lines: List[str]) -> int:
    """What do you get if you multiply your final horizontal position by your final depth?"""
    position = depth = aim = 0
    for line in lines:
        direction, raw_amount = line.split()
        amount = int(raw_amount)
        if direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
        elif direction == "forward":
            position += amount
            depth += amount * aim
    return position * depth


lines = read_input(2)

print(part1(lines))
print(part2(lines))
