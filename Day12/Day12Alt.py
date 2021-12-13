import functools
from typing import Generator, List, Dict, Tuple, Generic, TypeVar
import re
from collections import defaultdict
from functools import lru_cache

re_line = re.compile(r"^([a-zA-Z]*)-([a-zA-Z]*)$")


def read_input(filename: str) -> Dict[str, List[str]]:

    out = defaultdict(list)
    for line in open(filename):
        if m := re_line.match(line):
            if m.group(2) != "start" and m.group(1) != "end":
                out[m.group(1)].append(m.group(2))
            if m.group(1) != "start" and m.group(2) != "end":
                out[m.group(2)].append(m.group(1))
        else:
            raise Exception(f"you done screwed up with {line}")

    return out


class Path:
    def __init__(self, nodes: Tuple[str, ...], small_twice: bool) -> None:
        self.nodes: Tuple[str, ...] = nodes
        self.small_twice: bool = small_twice

    def add(self, node: str) -> "Path":
        if not self.small_twice and node.islower() and node in self.nodes:
            self.small_twice = True
        self.nodes = self.nodes + (node,)
        return self

    def can_add(self, node: str):
        return not self.small_twice or node.isupper() or node not in self.nodes


T = TypeVar("T")


def stacker(paths: List[T]) -> Generator[T, None, None]:

    while paths:
        yield paths.pop()


def get_paths(
    graph: Dict[str, List[str]],
    small_twice,
) -> Generator[Tuple[str, ...], None, None]:

    paths: List[Path] = [Path(("start",), small_twice)]

    for path in stacker(paths):
        for next in graph[path.nodes[-1]]:
            if next == "end":
                yield path.nodes
            elif path.can_add(next):
                paths.append(Path(path.nodes, path.small_twice).add(next))


def part_one(filename: str) -> int:
    return len([path for path in get_paths(read_input(filename), small_twice=True)])


def part_two(filename: str) -> int:
    return len([path for path in get_paths(read_input(filename), small_twice=False)])


if __name__ == "__main__":
    print("A:")
    print(f"Testinput1 value is {part_one('Day12/Day12TestInput1.txt')}")
    print(f"Testinput2 value is {part_one('Day12/Day12TestInput2.txt')}")
    print(f"Realinput value is {part_one('Day12/Day12Input.txt')}")

    print("B:")
    print(f"Testinput1 value is {part_two('Day12/Day12TestInput1.txt')}")
    print(f"Testinput2 value is {part_two('Day12/Day12TestInput2.txt')}")
    print(f"Realinput value is {part_two('Day12/Day12Input.txt')}")
