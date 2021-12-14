from helpers import read_input
from collections import defaultdict, deque
from typing import DefaultDict, Deque, List, Set, Tuple

Graph = DefaultDict[str, Set[str]]
Path = List[str]


def is_small_cave(cave: str) -> bool:
    """Returns true if a cave is small."""
    return cave == cave.lower()


def part1(graph: Graph) -> int:
    paths: List[Path] = []
    queue: Deque[Path] = deque([["start"]])
    while len(queue) > 0:
        path = queue.pop()
        src = path[-1]
        if src == "end":
            paths.append(path)
            continue
        for dest in graph[src]:
            if is_small_cave(dest) and dest in path:
                continue
            queue.append([*path, dest])
    return len(paths)


def part2(graph: Graph) -> int:
    paths: List[Path] = []
    queue: Deque[Tuple[Path, bool]] = deque([(["start"], False)])
    while len(queue) > 0:
        path, visited_twice = queue.pop()
        src = path[-1]
        if src == "end":
            paths.append(path)
            continue
        for dest in graph[src]:
            if dest == "start":
                continue
            elif is_small_cave(dest):
                if dest in path:
                    if not visited_twice:
                        queue.append(([*path, dest], True))
                else:
                    queue.append(([*path, dest], visited_twice))
            else:  # big cave
                queue.append(([*path, dest], visited_twice))
    return len(paths)


lines = read_input(12)
graph = defaultdict(set)
for line in lines:
    src, dest = line.split("-")
    graph[src].add(dest)
    graph[dest].add(src)

print(part1(graph))
print(part2(graph))
