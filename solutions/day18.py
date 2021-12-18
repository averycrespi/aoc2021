from ast import literal_eval
from dataclasses import dataclass
from math import ceil, floor
from typing import Optional, Tuple
from helpers import read_input


@dataclass
class SnailfishNumber:
    """Represents a snailfish number."""

    left: Optional["SnailfishNumber"] = None
    right: Optional["SnailfishNumber"] = None
    value: Optional[int] = None
    parent: Optional["SnailfishNumber"] = None

    @staticmethod
    def from_nested_list(a: list) -> "SnailfishNumber":
        """Create a snailfish number from a nested list."""
        assert len(a) == 2
        sn = SnailfishNumber(
            left=SnailfishNumber.from_nested_list(a[0])
            if isinstance(a[0], list)
            else SnailfishNumber(value=a[0]),
            right=SnailfishNumber.from_nested_list(a[1])
            if isinstance(a[1], list)
            else SnailfishNumber(value=a[1]),
        )
        if sn.left and sn.right:
            sn.left.parent = sn
            sn.right.parent = sn
        return sn

    def is_pair(self) -> bool:
        """Check if a snailfish number is a pair."""
        return self.left is not None and self.right is not None

    def is_regular(self) -> bool:
        """Check is a snailfish number is regular."""
        return self.value is not None

    def to_nested_list(self) -> list:
        """Convert a snailfish number to a nested list."""
        assert self.left is not None and self.right is not None
        return [
            self.left.to_nested_list() if self.left.is_pair() else self.left.value,
            self.right.to_nested_list() if self.right.is_pair() else self.right.value,
        ]

    def propagate_left(self):
        """Propagate the left value to the left."""
        curr = self
        while True:
            if curr.parent is None:
                return
            elif curr == curr.parent.right:
                curr = curr.parent.left
                while curr.right:
                    curr = curr.right
                curr.value += self.left
                return
            else:
                curr = curr.parent

    def propagate_right(self):
        """Propagate the right value to the right."""
        curr = self
        while True:
            if curr.parent is None:
                return
            elif curr == curr.parent.left:
                curr = curr.parent.right
                while curr.left:
                    curr = curr.left
                curr.value += self.right
                return
            else:
                curr = curr.parent

    def explode(self) -> bool:
        """Explode a snailfish number, returning True if the explosion succeeded."""
        stack: list[Tuple[SnailfishNumber, int]] = [(self, 0)]
        while len(stack) > 0:
            sn, depth = stack.pop()
            if depth == 4:
                sn.propagate_left()
                sn.propagate_right()
                sn.value = 0
                return True
            if sn.right:
                stack.append((sn.right, depth + 1))
            if sn.left:
                stack.append((sn.left, depth + 1))
        return False

    def split(self) -> bool:
        """Split a snailfish number, returning True if the split succeeded."""
        stack: list[SnailfishNumber] = [self]
        while len(stack) > 0:
            sn = stack.pop()
            if sn.left and sn.left.value and sn.left.value >= 10:
                sn.left = SnailfishNumber(
                    left=floor(sn.left.value / 2),
                    right=ceil(sn.left.value / 2),
                    parent=sn,
                )
                return True
            if isinstance(pair.right, int) and pair.right >= 10:
                pair.right = Pair(
                    left=floor(pair.right / 2), right=ceil(pair.right / 2), parent=pair
                )
                return True
            if isinstance(pair.right, Pair):
                stack.append(pair.right)
            if isinstance(pair.left, Pair):
                stack.append(pair.left)
        return False

    def reduce(self):
        """Reduce a pair by repeatedly exploding and splitting."""
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break

    def magnitude(self) -> int:
        """Calculate the magnitude of a pair."""
        return (
            3 * (self.left.magnitude() if isinstance(self.left, Pair) else self.left)
        ) + (
            2 * (self.right.magnitude() if isinstance(self.right, Pair) else self.right)
        )

    def __add__(self, other: "Pair") -> "Pair":
        pair = Pair(left=self, right=other)
        assert isinstance(pair.left, Pair) and isinstance(pair.right, Pair)
        pair.left.parent = pair
        pair.right.parent = pair
        pair.reduce()
        return pair

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Pair) and id(self) == id(other)

    def __str__(self) -> str:
        return str(self.to_nested_list())


def part1(pairs: list[Pair]) -> int:
    """What is the magnitude of the final sum?"""
    curr = pairs[0]
    for pair in pairs[1:]:
        print("  ", str(curr))
        print("+ ", str(pair))
        curr += pair
        print("= ", str(curr))
        print()
    return curr.magnitude()


def part2():
    pass


def test():
    p = Pair.from_nested_list([[[[[9, 8], 1], 2], 3], 4])
    p.explode()
    assert p.to_nested_list() == [[[[0, 9], 2], 3], 4]

    p = Pair.from_nested_list([7, [6, [5, [4, [3, 2]]]]])
    p.explode()
    assert p.to_nested_list() == [7, [6, [5, [7, 0]]]]

    p = Pair.from_nested_list([[6, [5, [4, [3, 2]]]], 1])
    p.explode()
    assert p.to_nested_list() == [[6, [5, [7, 0]]], 3]

    p = Pair.from_nested_list([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    p.explode()
    assert p.to_nested_list() == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]

    p = Pair.from_nested_list([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    p.explode()
    assert p.to_nested_list() == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]


lines = read_input(18, sample=True)
numbers = [literal_eval(line) for line in lines]
pairs = [Pair.from_nested_list(n) for n in numbers]

test()
print(part1(pairs))
