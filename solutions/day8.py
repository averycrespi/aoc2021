from helpers import read_input
from collections import namedtuple
from itertools import permutations


DIGITS = frozenset(range(10))
SEGMENTS = "abcdefg"
DIGIT_TO_SEGMENTS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}
SEGMENTS_TO_DIGIT = {s: d for d, s in DIGIT_TO_SEGMENTS.items()}
ALL_DIGIT_SEGMENTS = frozenset(DIGIT_TO_SEGMENTS.values())


Display = namedtuple("Display", ("patterns", "outputs"))


def transform(pattern: str, key: str) -> str:
    """Apply a transformation key to a pattern."""
    lookup = {s: key[i] for i, s in enumerate(SEGMENTS)}
    return "".join(sorted(lookup[s] for s in pattern))


def is_valid_transformation(display: Display, key: str) -> bool:
    """Check if a transformation is valid."""
    for p in display.patterns:
        if transform(p, key) not in ALL_DIGIT_SEGMENTS:
            return False
    for o in display.outputs:
        if transform(o, key) not in ALL_DIGIT_SEGMENTS:
            return False
    return True


def solve_display(display: Display):
    """Solve a display by brute-force."""
    for perm in permutations(SEGMENTS):
        key = "".join(perm)
        if is_valid_transformation(display, key):
            return [SEGMENTS_TO_DIGIT[transform(o, key)] for o in display.outputs]
    else:  # nobreak
        raise ValueError(str(display))


lines = read_input(8)
displays = [
    Display(
        patterns=tuple(row[0].split()),
        outputs=tuple(row[1].split()),
    )
    for row in [line.split(" | ") for line in lines]
]

part1 = 0
part2 = 0
for display in displays:
    solution = solve_display(display)
    for d in solution:
        if d in [1, 4, 7, 8]:
            part1 += 1
    part2 += int("".join(str(d) for d in solution))
print(part1)
print(part2)
