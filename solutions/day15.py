from typing import Dict, List, Optional, Set
from helpers import Point, read_input
from skimage.graph import route_through_array


def part1(cave: List[List[int]]) -> int:
    """What is the lowest total risk of any path from the top left to the bottom right?"""
    # Dijkstra's algorithm from: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    height, width = len(cave), len(cave[0])
    Q: Set[Point] = set()
    dist: Dict[Point, int] = {}
    prev: Dict[Point, Optional[Point]] = {}
    for p in Point.range(width, height):
        dist[p] = int(1e9)
        prev[p] = None
        Q.add(p)
    dist[Point(0, 0)] = 0
    while len(Q) > 0:
        u = min(Q, key=lambda p: dist[p])
        Q.remove(u)
        for v in u.neighbours():
            if v in Q:
                alt = dist[u] + cave[v.y][v.x]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    return dist[Point(width - 1, height - 1)]


def expand_cave(cave: List[List[int]], factor: int) -> List[List[int]]:
    """Expand a cave by a factor."""
    height, width = len(cave), len(cave[0])
    expanded_cave = [[0] * width * factor for _ in range(height * factor)]
    for tile_y in range(factor):
        for tile_x in range(factor):
            for y in range(height):
                for x in range(width):
                    expanded_y = (tile_y * height) + y
                    expanded_x = (tile_x * width) + x
                    if tile_y == tile_x == 0:  # copy directly from cave
                        source = cave[y][x]
                    elif tile_y == 0:  # copy and increment from tile to left
                        source_x = ((tile_x - 1) * width) + x
                        source = expanded_cave[expanded_y][source_x] + 1
                    else:  # copy and increment from tile above
                        source_y = ((tile_y - 1) * height) + y
                        source = expanded_cave[source_y][expanded_x] + 1
                    expanded_cave[expanded_y][expanded_x] = (
                        source - 9 if source > 9 else source
                    )
    return expanded_cave


def part2(cave: List[List[int]]) -> int:
    """What is the lowest total risk of any path from the top left to the bottom right?"""
    return part1(expand_cave(cave, 5))


lines = read_input(15)
cave = [[int(char) for char in line] for line in lines]

print(part1(cave))
# This is correct, but takes way too long:
# print(part2(cave))
# Luckily, scikit is magic!
print(
    route_through_array(
        expand_cave(cave, 5), [0, 0], [499, 499], geometric=False, fully_connected=False
    )[1]
    - cave[0][0]
)
