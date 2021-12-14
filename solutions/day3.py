from helpers import read_input
from typing import List


def mcb(numbers: List[List[int]], index: int) -> int:
    """Determine the most common bit at an index."""
    return 1 if sum(n[index] for n in numbers) >= len(numbers) / 2 else 0


def btoi(number: List[int]) -> int:
    """Convert a bit sequence to an integer."""
    return int("".join(str(b) for b in number), base=2)


def part1(numbers: List[List[int]]) -> int:
    """What is the power consumption of the submarine?"""
    gamma_bits = []
    epsilon_bits = []
    for i in range(len(numbers[0])):
        bit = mcb(numbers, i)
        gamma_bits.append(bit)
        epsilon_bits.append(int(not bit))
    return btoi(gamma_bits) * btoi(epsilon_bits)


def part2(numbers: List[List[int]]) -> int:
    """What is the life support rating of the submarine?"""
    oxygen_numbers = list(numbers)
    oxygen_index = 0
    while len(oxygen_numbers) > 1:
        bit = mcb(oxygen_numbers, oxygen_index)
        oxygen_numbers = [on for on in oxygen_numbers if on[oxygen_index] == bit]
        oxygen_index += 1

    co2_numbers = list(numbers)
    co2_index = 0
    while len(co2_numbers) > 1:
        bit = mcb(co2_numbers, co2_index)
        co2_numbers = [cn for cn in co2_numbers if cn[co2_index] != bit]
        co2_index += 1

    return btoi(oxygen_numbers[0]) * btoi(co2_numbers[0])


lines = read_input(3)
numbers = [[int(bit) for bit in line] for line in lines]

print(part1(numbers))
print(part2(numbers))
