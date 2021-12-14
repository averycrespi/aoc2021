from helpers import read_input, Point
from typing import List


Grid = List[List[bool]]


def print_grid(grid: Grid):
    """Print a grid."""
    for row in grid:
        print("".join("#" if cell else "." for cell in row))


def fold_up(grid: Grid, line_y: int) -> Grid:
    """Fold a grid upwards along a horizontal line."""
    new_grid = [row[:] for row in grid]
    width, height = len(grid[0]), len(grid)
    for i in range(line_y):
        for j in range(width):
            new_grid[i][j] |= new_grid[height - i - 1][j]
    return new_grid[:line_y]


def fold_left(grid: Grid, line_x: int) -> Grid:
    """Fold a grid leftwards along a vertical line."""
    new_grid = [row[:] for row in grid]
    width, height = len(grid[0]), len(grid)
    for j in range(line_x):
        for i in range(height):
            new_grid[i][j] |= new_grid[i][width - j - 1]
    return [row[:line_x] for row in new_grid]


def apply_fold(grid: Grid, fold: str) -> Grid:
    """Apply a fold to a grid."""
    d, n = fold.split("=")
    if d == "y":
        return fold_up(grid, int(n))
    elif d == "x":
        return fold_left(grid, int(n))
    else:
        raise ValueError(fold)


def part1(grid: Grid, folds: List[str]) -> int:
    """How many dots are visible after completing just the first fold instruction on your transparent paper?"""
    return sum(sum(row) for row in apply_fold(grid, folds[0]))


def part2(grid: Grid, folds: List[str]) -> Grid:
    """What code do you use to activate the infrared thermal imaging camera system?"""
    curr = grid
    for fold in folds:
        curr = apply_fold(curr, fold)
    return curr


lines = read_input(13)
blank = lines.index("")
dots = [Point(*map(int, line.split(","))) for line in lines[:blank]]
folds = [line.strip("fold along ") for line in lines[blank + 1 :]]
width = max(d.x for d in dots) + 1
height = max(d.y for d in dots) + 1
grid = [[False] * width for _ in range(height)]
for d in dots:
    grid[d.y][d.x] = True

print(part1(grid, folds))
print_grid(part2(grid, folds))
