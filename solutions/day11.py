from helpers import Point, read_input
from collections import deque
from typing import Deque, List, Set, Tuple


WIDTH = HEIGHT = 10


def adjacent_to(p: Point) -> Set[Point]:
    """Returns the set of points cardinally or diagonally adjacent to a point."""
    return set(
        Point(ax, ay)
        for ax, ay in [
            (p.x - 1, p.y - 1),  # NW
            (p.x - 1, p.y + 0),  # N
            (p.x - 1, p.y + 1),  # NE
            (p.x + 0, p.y - 1),  # W
            (p.x + 0, p.y + 1),  # E
            (p.x + 1, p.y - 1),  # SW
            (p.x + 1, p.y + 0),  # S
            (p.x + 1, p.y + 1),  # SE
        ]
        if 0 <= ay < HEIGHT and 0 <= ax < WIDTH
    )


def step(grid: List[List[int]]) -> Tuple[List[List[int]], int]:
    """Advance the grid one step forwards, returning the number of flashes."""
    new_grid = [row[:] for row in grid]
    queue: Deque[Point] = deque()

    # first pass: increment and mark initial flashing
    for y in range(HEIGHT):
        for x in range(WIDTH):
            new_grid[y][x] += 1
            if new_grid[y][x] > 9:
                queue.append(Point(x, y))

    # second pass: propagate flashes
    flashed: Set[Point] = set()
    while len(queue) > 0:
        curr = queue.popleft()
        if curr in flashed:
            continue  # octopus can only flash once
        flashed.add(curr)
        for adj in adjacent_to(curr):
            new_grid[adj.y][adj.x] += 1
            if new_grid[adj.y][adj.x] > 9:
                queue.append(adj)

    # third pass: reset flashed to zero
    for p in flashed:
        new_grid[p.y][p.x] = 0

    return new_grid, len(flashed)


def part1(grid: List[List[int]]) -> int:
    """How many total flashes are there after 100 steps?"""
    total_flashes = 0
    new_grid = grid
    for _ in range(100):
        new_grid, flashes = step(new_grid)
        total_flashes += flashes
    return total_flashes


def part2(grid: List[List[int]]) -> int:
    """What is the first step during which all octopuses flash?"""
    i = 1
    new_grid = grid
    while True:
        new_grid, flashes = step(new_grid)
        if flashes == WIDTH * HEIGHT:
            return i
        i += 1


lines = read_input(11)
grid = [list(map(int, list(line))) for line in lines]
print(part1(grid))
print(part2(grid))
