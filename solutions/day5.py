from helpers import read_input, Point
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple


Vent = namedtuple("Vent", "start,end")


def delta(start: Point, end: Point) -> Tuple[int, int]:
    """Compute the directional delta between two points."""
    x = end.x - start.x
    y = end.y - start.y
    return 0 if x == 0 else x / abs(x), 0 if y == 0 else y / abs(y)


def count_overlap_points(vents: List[Vent]) -> int:
    """At how many points do at least two lines overlap?"""
    terrain: Dict[Point, int] = defaultdict(int)
    for v in vents:
        dx, dy = delta(v.start, v.end)
        curr = v.start
        while curr != v.end:
            terrain[curr] += 1
            curr = Point(x=curr.x + dx, y=curr.y + dy)
        terrain[v.end] += 1
    return sum(True for n in terrain.values() if n >= 2)


lines = read_input(5)
vents = [
    Vent(
        start=Point(*map(int, entry[0].split(","))),
        end=Point(*map(int, entry[1].split(","))),
    )
    for entry in [line.split(" -> ") for line in lines]
]

orthogonal_vents = [v for v in vents if v.start.x == v.end.x or v.start.y == v.end.y]
print(count_overlap_points(orthogonal_vents))
print(count_overlap_points(vents))
