from helpers import read_input
from collections import defaultdict
from typing import DefaultDict


Population = DefaultDict[int, int]


def step(population: Population) -> Population:
    """Advance the population by one step."""
    after = defaultdict(int)
    for age in range(8):
        after[age] = population[age + 1]
    after[6] += population[0]
    after[8] = population[0]
    return after


def simulate(population: Population, days: int) -> int:
    """Simulate the population size after a number of days."""
    curr = population
    for _ in range(days):
        curr = step(curr)
    return sum(curr.values())


lines = read_input(6)
population: Population = defaultdict(int)
for raw_fish in lines[0].split(","):
    population[int(raw_fish)] += 1

print(simulate(population, 80))
print(simulate(population, 256))
