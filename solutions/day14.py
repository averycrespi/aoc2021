from helpers import read_input
from collections import defaultdict
from typing import Counter, DefaultDict, Dict, List, Tuple


def step_n(template: str, rules: Dict[str, str], n: int) -> int:
    """Apply the rules for n steps."""
    elements = Counter(template)
    bigrams: DefaultDict[str, int] = defaultdict(int)
    for i in range(len(template) - 1):
        bigrams[template[i : i + 2]] += 1
    for _ in range(n):
        delta: List[Tuple[str, int]] = []
        for bigram, count in bigrams.items():
            if count > 0 and bigram in rules:
                insertion = rules[bigram]
                delta.append((bigram[0] + insertion, count))
                delta.append((insertion + bigram[1], count))
                delta.append((bigram, -count))
                elements[insertion] += count
        for bigram, change in delta:
            bigrams[bigram] += change
    counts = elements.most_common()
    return counts[0][1] - counts[-1][1]


lines = read_input(14)
template = lines[0]
rules = dict(line.split(" -> ") for line in lines[2:])  # type: ignore

print(step_n(template, rules, 10))
print(step_n(template, rules, 40))
