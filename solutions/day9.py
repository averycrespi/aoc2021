from helpers import read_input, Point
from collections import deque
from functools import reduce
from operator import mul
from typing import List, Optional, Set


DrainageMap = List[List[Optional[Point]]]


def adjacent_to(p: Point, height: int, width: int) -> Set[Point]:
    """Returns the set of points cardinally adjacent to a point."""
    return set(
        Point(ax, ay)
        for ax, ay in [(p.x - 1, p.y), (p.x, p.y - 1), (p.x + 1, p.y), (p.x, p.y + 1)]
        if 0 <= ay < height and 0 <= ax < width
    )


def part1(height_map: List[List[int]]) -> int:
    """What is the sum of the risk levels of all low points on your heightmap?"""
    risk = 0
    height, width = len(height_map), len(height_map[0])
    for y in range(height):
        for x in range(width):
            cell = height_map[y][x]
            if all(
                cell < height_map[p.y][p.x]
                for p in adjacent_to(Point(x, y), height, width)
            ):
                risk += cell + 1
    return risk


def explore_basin(
    bottom: Point, drains_to: DrainageMap, height: int, width: int
) -> Set[Point]:
    """Explore a basin from the bottom upwards."""
    visited: Set[Point] = set()
    queue = deque([bottom])
    while len(queue) > 0:
        curr = queue.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        for adj in adjacent_to(curr, height, width):
            if drains_to[adj.y][adj.x] == curr:
                queue.append(adj)
    return visited


def part2(height_map: List[List[int]]) -> int:
    """What do you get if you multiply together the sizes of the three largest basins?"""
    height, width = len(height_map), len(height_map[0])
    drains_to: DrainageMap = [[None] * width for _ in range(height)]
    bottoms: Set[Point] = set()
    for y in range(height):
        for x in range(width):
            cell = height_map[y][x]
            if cell == 9:
                continue  # locations of size 9 are not in any basin
            lower_adj = [
                p
                for p in adjacent_to(Point(x, y), height, width)
                if cell > height_map[p.y][p.x]
            ]
            if len(lower_adj) == 0:
                bottoms.add(Point(x, y))
            else:
                drains_to[y][x] = min(lower_adj, key=lambda p: height_map[p.y][p.x])

    basin_sizes = [len(explore_basin(b, drains_to, height, width)) for b in bottoms]
    return reduce(mul, sorted(basin_sizes, reverse=True)[:3])


lines = read_input(9)
height_map = [list(map(int, list(line))) for line in lines]
print(part1(height_map))
print(part2(height_map))
