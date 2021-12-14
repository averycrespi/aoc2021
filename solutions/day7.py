from helpers import read_input
from typing import List


def part1(crabs: List[int]) -> int:
    """How much fuel must they spend to align to [the optimal] position?"""
    best_score = int(1e9)
    for pos in range(min(crabs), max(crabs) + 1):
        score = sum(abs(crab - pos) for crab in crabs)
        if score < best_score:
            best_score = score
    return best_score


def part2(crabs: List[int]) -> int:
    """How much fuel must they spend to align to [the optimal] position?"""
    best_score = int(1e9)
    for pos in range(min(crabs), max(crabs) + 1):
        score = 0
        for crab in crabs:
            diff = abs(crab - pos)
            score += (diff * (diff + 1)) // 2  # summation formula: 1 to diff
        if score < best_score:
            best_score = score
    return best_score


lines = read_input(7)
crabs = [int(crab) for crab in lines[0].split(",")]

print(part1(crabs))
print(part2(crabs))
