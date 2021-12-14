from dataclasses import dataclass
from pathlib import Path
from typing import List

INPUT_DIR = Path(__file__).parent.parent / "inputs"


@dataclass(frozen=True, eq=True)
class Point:
    """Represents a point on a 2D grid."""

    x: int
    y: int


def read_input(day: int, sample: bool = False) -> List[str]:
    """Read the lines from an input file."""
    file_name = f"day{day}{'.sample' if sample else ''}.txt"
    with open(INPUT_DIR / file_name) as f:
        return [line.strip() for line in f.readlines()]
