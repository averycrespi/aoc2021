from helpers import read_input
from typing import Any, List, Set


def chunks(seq: List[Any], n: int):
    """Yield successive n-sized chunks from a list."""
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


class Board:
    """Represents a bingo board."""

    def __init__(self, rows: List[List[int]]):
        self.rows = rows

    def __str__(self):
        return str(self.rows)

    def has_won(self, chosen: Set[int]) -> bool:
        """Determine if a board has won the game."""
        return (
            any(all(cell in chosen for cell in self.rows[i]) for i in range(5))  # rows
            or any(all(row[j] in chosen for row in self.rows) for j in range(5))  # cols
            or all(self.rows[k][k] in chosen for k in range(5))  # SE/NW
            or all(self.rows[k][5 - 1 - k] in chosen for k in range(5))  # SW/NE
        )

    def score(self, chosen: Set[int], last: int) -> int:
        """Calculate the score of a board."""
        return last * sum(
            sum(cell for cell in row if cell not in chosen) for row in self.rows
        )


def part1(choices: List[int], boards: List[Board]) -> int:
    """What will your final score be if you choose [the winning] board?"""
    chosen = set()
    for choice in choices:
        chosen.add(choice)
        for board in boards:
            if board.has_won(chosen):
                return board.score(chosen, choice)
    raise ValueError("no winner")


def part2(choices: List[int], boards: List[Board]) -> int:
    """Figure out which board will win last. Once it wins, what would its final score be?"""
    chosen = set()
    last_score = 0
    remaining = list(boards)
    for choice in choices:
        chosen.add(choice)
        winners = set()
        for i, board in enumerate(remaining):
            if board.has_won(chosen):
                last_score = board.score(chosen, choice)
                winners.add(i)
        remaining = [b for i, b in enumerate(remaining) if i not in winners]
        if len(remaining) == 0:
            break
    return last_score


lines = read_input(4)
choices = [int(n) for n in lines.pop(0).split(",")]
boards = [
    Board([[int(cell) for cell in row.split()] for row in board[1:]])
    for board in chunks(lines, 6)
]

print(part1(choices, boards))
print(part2(choices, boards))
