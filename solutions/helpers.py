from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Set

INPUT_DIR = Path(__file__).parent.parent / "inputs"


@dataclass(frozen=True, eq=True)
class Point:
    """Represents a point on a 2D grid."""

    x: int
    y: int

    @staticmethod
    def range(x: int, y: int) -> Iterator["Point"]:
        """Generate a range of points from (0,0) to (x-1,y-1)."""
        for px in range(x):
            for py in range(y):
                yield Point(px, py)

    def neighbours(self) -> Set["Point"]:
        """Generate the cardinal neighbours of a point."""
        return set(
            [
                Point(self.x - 1, self.y),
                Point(self.x + 1, self.y),
                Point(self.x, self.y - 1),
                Point(self.x, self.y + 1),
            ]
        )


def read_input(day: int, sample: bool = False) -> List[str]:
    """Read the lines from an input file."""
    file_name = f"day{day}{'.sample' if sample else ''}.txt"
    with open(INPUT_DIR / file_name) as f:
        return [line.strip() for line in f.readlines()]
