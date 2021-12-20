from dataclasses import dataclass
from typing import Optional, Tuple
from helpers import read_input


@dataclass(eq=True, frozen=True)
class Beacon:
    """Represents the relative position of a beacon."""

    x: int
    y: int
    z: int

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    def __add__(self, other: "Beacon") -> "Beacon":
        return Beacon(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Beacon") -> "Beacon":
        return Beacon(self.x - other.x, self.y - other.y, self.z - other.z)

    def manhattan_distance_to(self, other: "Beacon") -> int:
        """Calculate the Manhattan distance to another beacon."""
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def all_orientations(self) -> list["Beacon"]:
        """Return all possible orientations of a beacon."""
        rotations = [
            Beacon(self.x, self.y, self.z),  # +x -> +x (identity)
            Beacon(-self.x, -self.y, self.z),  # +x -> -x
            Beacon(self.y, -self.x, self.z),  # +x -> +y
            Beacon(-self.y, self.x, self.z),  # +x -> -y
            Beacon(self.z, self.y, -self.x),  # +x -> +z
            Beacon(-self.z, self.y, self.x),  # +x -> -z
        ]
        orientations = []
        for r in rotations:
            orientations.extend(
                [
                    Beacon(r.x, r.y, r.z),  # +y -> +y (identity)
                    Beacon(r.x, -r.y, -r.z),  # +y -> -y
                    Beacon(r.x, r.z, -r.y),  # +y -> +z
                    Beacon(r.x, -r.z, r.y),  # +y -> -z
                ]
            )
        return orientations


@dataclass(eq=True, frozen=True)
class Scanner:
    """Represents a scanner."""

    name: str
    beacons: list[Beacon]
    centers: frozenset[Beacon] = frozenset()

    def all_orientations(self) -> list["Scanner"]:
        """Return all possible orientations of a scanner."""
        beacon_orientations = [b.all_orientations() for b in self.beacons]
        return [
            Scanner(
                name=f"{self.name}-{i}", beacons=[o[i] for o in beacon_orientations]
            )
            for i in range(24)
        ]

    def align(self, other: "Scanner") -> Optional["Scanner"]:
        """Attempt to align two scanners, returning a composite scanner."""
        reference = frozenset(self.beacons)
        for candidate in other.all_orientations():
            for b in self.beacons:
                for c in candidate.beacons:
                    offset = c - b
                    corrected = {d - offset for d in candidate.beacons}
                    if len(reference & corrected) >= 12:
                        return Scanner(
                            name=f"({self.name}) + ({candidate.name})",
                            beacons=list(reference | corrected),
                            centers=self.centers | {offset},
                        )
        return None


def part1_2(scanners: list[Scanner]) -> Tuple[int, int]:
    composite = scanners[0]
    unused = scanners[1:]
    while len(unused) > 0:
        for candidate in unused:
            aligned = composite.align(candidate)
            if aligned:
                composite = aligned
                unused.remove(candidate)
                break
    largest_distance = 0
    for c in composite.centers:
        for d in composite.centers:
            largest_distance = max(largest_distance, c.manhattan_distance_to(d))
    return len(composite.beacons), largest_distance


lines = read_input(19)
scanners: list[Scanner] = []
chunk: list[str] = []
for line in [*lines, ""]:
    if len(line) == 0:
        name = chunk[0].strip("-").strip()
        beacons = [Beacon(*map(int, b.split(","))) for b in chunk[1:]]
        scanners.append(Scanner(name, beacons))
        chunk = []
    else:
        chunk.append(line)


print(part1_2(scanners))
