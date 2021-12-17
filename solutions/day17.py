from collections import namedtuple
import re
from typing import Optional, Tuple
from helpers import read_input


Region = namedtuple("Region", ("x1", "x2", "y1", "y2"))


def apply_drag(dx: int) -> int:
    """Apply drag to a horizontal velocity."""
    if dx > 0:
        return dx - 1
    elif dx < 0:
        return dx + 1
    else:
        return dx


def step(x: int, y: int, dx: int, dy: int) -> Tuple[int, int, int, int]:
    """Advance the simulation by one step."""
    return x + dx, y + dy, apply_drag(dx), dy - 1


def simulate(target: Region, dx: int, dy: int) -> Optional[int]:
    """Simulate the probe, returning the best y position or None if the probe misses."""
    best_y = 0
    x, y = 0, 0
    while True:
        if x > target.x2:
            return None  # overshot
        if y < target.y1:
            return None  # undershot
        if target.x1 <= x <= target.x2 and target.y1 <= y <= target.y2:
            return best_y
        x, y, dx, dy = step(x, y, dx, dy)
        best_y = max(y, best_y)


def part1(target: Region) -> int:
    """What is the highest y position it reaches on this trajectory?"""
    best_y = 0
    for dx in range(500):
        for dy in range(-500, 500):
            result = simulate(target, dx, dy)
            if result is not None:
                best_y = max(best_y, result)
    return best_y


def part2(target: Region) -> int:
    """How many distinct initial velocity values cause the probe to be within the target area after any step?"""
    solutions = 0
    for dx in range(1000):
        for dy in range(-1000, 1000):
            result = simulate(target, dx, dy)
            if result is not None:
                solutions += 1
    return solutions


lines = read_input(17)
pattern = r"^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)$"
target = Region(*[int(g) for g in re.match(pattern, lines[0]).groups()])  # type: ignore

print(part1(target))
print(part2(target))
