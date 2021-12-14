from helpers import read_input
from typing import List, Tuple

OPENING = "([{<"
CLOSING = ")]}>"
PAIRS = set("".join([o, c]) for o, c in zip(OPENING, CLOSING))
ILLEGAL_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
COMPLETION_SCORES = {"(": 1, "[": 2, "{": 3, "<": 4}


def part1(lines: List[str]) -> Tuple[int, List[str]]:
    """What is the total syntax error score for those errors?"""
    scores = []
    incomplete = []
    for line in lines:
        illegal: List[str] = []
        stack: List[str] = []
        for i, c in enumerate(line):
            if c in OPENING:
                stack.append(c)
            elif len(stack) == 0:
                illegal.append(c)
            else:
                prev = stack.pop()
                if f"{prev}{c}" not in PAIRS:
                    stack.append(prev)
                    illegal.append(c)
        if len(illegal) > 0:
            scores.append(ILLEGAL_SCORES[illegal[0]])
        else:
            incomplete.append(line)  # for part 2
    return sum(scores), incomplete


def part2(incomplete: List[str]) -> int:
    """What is the middle score?"""
    scores = []
    for line in incomplete:
        stack = []
        for c in line:
            if c in OPENING:
                stack.append(c)
            else:
                stack.pop()
        score = 0
        while len(stack) > 0:
            score = (score * 5) + COMPLETION_SCORES[stack.pop()]
        scores.append(score)
    scores = list(sorted(scores))
    return scores[len(scores) // 2]


lines = read_input(10)
part1_score, incomplete = part1(lines)
print(part1_score)
print(part2(incomplete))
