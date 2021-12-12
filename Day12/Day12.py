import functools
from typing import Generator, List, Dict, Tuple
import re
from collections import defaultdict
from functools import lru_cache

re_line = re.compile(r"^([a-zA-Z]*)-([a-zA-Z]*)$")


def read_input(filename: str) -> Dict[str, List[str]]:

    out = defaultdict(list)
    for line in open(filename):
        if m := re_line.match(line):
            if m.group(2) != "start":
                out[m.group(1)].append(m.group(2))
            if m.group(1) != "start":
                out[m.group(2)].append(m.group(1))
        else:
            raise Exception(f"you done screwed up with {line}")

    return out


def eval_good_one(path: Tuple[str], next: str) -> bool:
    return next.isupper() or next not in path


@functools.lru_cache
def check_lowers(path: Tuple[str]) -> bool:
    seen = set()
    for node in path:
        if node.islower():
            if node in seen:
                return False
            seen.add(node)
    return True


def eval_good_two(path: Tuple[str], next) -> bool:

    return next.isupper() or next not in path or check_lowers(path)


def get_paths(
    graph: Dict[str, List[str]],
    eval_good,
) -> Generator[Tuple[str, ...], None, None]:

    paths: List[Tuple[str, ...]] = [("start",)]

    while len(paths) > 0:
        path = paths.pop()
        for next in graph[path[-1]]:
            if next == "end":
                yield path
            elif eval_good(path, next):
                paths.append(path + (next,))


def part_one(filename: str) -> int:
    return len([path for path in get_paths(read_input(filename), eval_good_one)])


def part_two(filename: str) -> int:
    return len([path for path in get_paths(read_input(filename), eval_good_two)])


if __name__ == "__main__":
    print("A:")
    print(f"Testinput1 value is {part_one('Day12/Day12TestInput1.txt')}")
    print(f"Testinput2 value is {part_one('Day12/Day12TestInput2.txt')}")
    print(f"Realinput value is {part_one('Day12/Day12Input.txt')}")

    print("B:")
    print(f"Testinput1 value is {part_two('Day12/Day12TestInput1.txt')}")
    print(f"Testinput2 value is {part_two('Day12/Day12TestInput2.txt')}")
    print(f"Realinput value is {part_two('Day12/Day12Input.txt')}")
