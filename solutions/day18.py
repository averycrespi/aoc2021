from ast import literal_eval
from copy import deepcopy
from dataclasses import dataclass
from helpers import read_input
from math import ceil, floor
from typing import Iterator, Optional, Tuple, Union


@dataclass
class SFN:
    """Represents a snailfish number."""

    left: Union["SFN", int]
    right: Union["SFN", int]
    parent: Optional["SFN"] = None

    @staticmethod
    def from_nested_list(a: list) -> "SFN":
        """Create a snailfish number from a nested list."""
        assert len(a) == 2
        sfn = SFN(
            left=SFN.from_nested_list(a[0]) if isinstance(a[0], list) else a[0],
            right=SFN.from_nested_list(a[1]) if isinstance(a[1], list) else a[1],
        )
        if isinstance(sfn.left, SFN):
            sfn.left.parent = sfn
        if isinstance(sfn.right, SFN):
            sfn.right.parent = sfn
        return sfn

    def to_nested_list(self) -> list:
        """Convert a snailfish number to a nested list."""
        return [
            self.left.to_nested_list() if isinstance(self.left, SFN) else self.left,
            self.right.to_nested_list() if isinstance(self.right, SFN) else self.right,
        ]

    def propagate_left(self) -> "SFN":
        """
        Propagate a left value to the left of a snailfish number.

        Returns the (possible-mutated) snailfish number.
        """
        # Ascend tree until the node is a right child
        assert isinstance(self.left, int)
        up = self
        while True:
            if up.parent is None:
                return self  # Found root node
            elif up == up.parent.right:
                if isinstance(up.parent.left, int):
                    up.parent.left += self.left
                    return self  # Special case: sibling is regular
                # Descend tree until the right child is regular
                down = up.parent.left
                while isinstance(down.right, SFN):
                    down = down.right
                down.right += self.left
                return self
            else:
                up = up.parent

    def propagate_right(self) -> "SFN":
        """
        Propagate a right value to the right of a snailfish number.

        Returns the (possibly-mutated) snailfish number.
        """
        # Ascend tree until the node is a left child
        assert isinstance(self.right, int)
        up = self
        while True:
            if up.parent is None:
                return self  # Found root node
            elif up == up.parent.left:
                if isinstance(up.parent.right, int):
                    up.parent.right += self.right
                    return self  # Special case: sibling is regular
                # Descend tree until left child is regular
                down = up.parent.right
                while isinstance(down.left, SFN):
                    down = down.left
                down.left += self.right
                return self
            else:
                up = up.parent

    def explode(self) -> Tuple["SFN", bool]:
        """
        Try to explode a snailfish number.

        Returns the (possibly mutated) snailfish number and whether the explosion succeeded.
        """
        stack: list[Tuple[SFN, int]] = [(self, 0)]
        while len(stack) > 0:
            sfn, depth = stack.pop()
            if depth == 4:
                sfn.propagate_left()
                sfn.propagate_right()
                assert sfn.parent is not None
                if sfn == sfn.parent.left:
                    sfn.parent.left = 0
                elif sfn == sfn.parent.right:
                    sfn.parent.right = 0
                else:
                    raise ValueError(sfn.parent)
                return self, True
            if isinstance(sfn.right, SFN):
                stack.append((sfn.right, depth + 1))
            if isinstance(sfn.left, SFN):
                stack.append((sfn.left, depth + 1))
        return self, False

    def inorder(self) -> Iterator["SFN"]:
        """Traverse a snailfish number in-order."""
        if isinstance(self.left, SFN):
            for sfn in self.left.inorder():
                yield sfn
        yield self
        if isinstance(self.right, SFN):
            for sfn in self.right.inorder():
                yield sfn

    def split(self) -> Tuple["SFN", bool]:
        """
        Try to split a snailfish number.

        Returns the (possibly mutated) snailfish number and whether the split succeeded.
        """
        for sfn in self.inorder():
            if isinstance(sfn.left, int) and sfn.left >= 10:
                sfn.left = SFN(
                    left=floor(sfn.left / 2), right=ceil(sfn.left / 2), parent=sfn
                )
                return self, True
            if isinstance(sfn.right, int) and sfn.right >= 10:
                sfn.right = SFN(
                    left=floor(sfn.right / 2), right=ceil(sfn.right / 2), parent=sfn
                )
                return self, True
        return self, False

    def reduce(self) -> "SFN":
        """
        Reduce a snailfish number by repeatedly exploding and splitting.

        Returns the (possibly mutated) snailfish number
        """
        while True:
            _, did_explode = self.explode()
            if did_explode:
                continue
            _, did_split = self.split()
            if did_split:
                continue
            return self

    def magnitude(self) -> int:
        """Calculate the magnitude of a snailfish number."""
        return (
            3 * (self.left.magnitude() if isinstance(self.left, SFN) else self.left)
        ) + (
            2 * (self.right.magnitude() if isinstance(self.right, SFN) else self.right)
        )

    def __add__(self, other: "SFN") -> "SFN":
        sfn = SFN(left=deepcopy(self), right=deepcopy(other))
        assert isinstance(sfn.left, SFN) and isinstance(sfn.right, SFN)
        sfn.left.parent = sfn
        sfn.right.parent = sfn
        return sfn.reduce()

    def __eq__(self, other) -> bool:
        return isinstance(other, SFN) and id(self) == id(other)


def test_explode():
    data = [
        ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
        ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
        ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
        (
            [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
        ),
        (
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        ),
        (
            [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]],
            [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]],
        ),
        (
            [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]],
            [[[[0, 7], 4], [15, [0, 13]]], [1, 1]],
        ),
        (
            [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]],
            [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]],
        ),
    ]
    for input, expected in data:
        output, did_explode = SFN.from_nested_list(input).explode()
        assert did_explode and output.to_nested_list() == expected


def test_split():
    data = [
        (
            [[[[0, 7], 4], [15, [0, 13]]], [1, 1]],
            [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
        ),
        (
            [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
            [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]],
        ),
    ]
    for input, expected in data:
        output, did_split = SFN.from_nested_list(input).split()
        assert did_split and output.to_nested_list() == expected


def test_add():
    data = [
        (
            [[[[4, 3], 4], 4], [7, [[8, 4], 9]]],
            [1, 1],
            [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]],
        )
    ]
    for a, b, expected in data:
        output = SFN.from_nested_list(a) + SFN.from_nested_list(b)
        assert output.to_nested_list() == expected


test_explode()
test_split()
test_add()


def part1(sfns: list[SFN]) -> int:
    """What is the magnitude of the final sum?"""
    curr = sfns[0]
    for sfn in sfns[1:]:
        curr += sfn
    return curr.magnitude()


def part2(sfns: list[SFN]) -> int:
    """What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment?"""
    best = 0
    for a in sfns:
        for b in sfns:
            if a != b:
                best = max(best, (a + b).magnitude())
                best = max(best, (b + a).magnitude())
    return best


lines = read_input(18)
sfns = [SFN.from_nested_list(literal_eval(line)) for line in lines]

print(part1(sfns))
print(part2(sfns))
