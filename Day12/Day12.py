from typing import Generator, List, Dict
import re
from collections import defaultdict, Counter

re_line = re.compile(r"^([a-zA-Z]*)-([a-zA-Z]*)$")


def read_input(filename: str) -> Dict[str, List[str]]:

    out = defaultdict(list)
    for line in open(filename):
        if m := re_line.match(line):
            out[m.group(1)].append(m.group(2))
            out[m.group(2)].append(m.group(1))
        else:
            raise Exception(f"you done screwed up with {line}")

    return out


def eval_good_one(path: List[str]) -> bool:
    return path[-1].isupper() or path[-1] not in path[:-1]


def eval_good_two(path: List[str]) -> bool:
    if path[-1].isupper():
        return True

    lowers = tuple(node for node in path if node.islower())
    return len(set(lowers)) + 1 >= len(lowers)


def get_paths(
    graph: Dict[str, List[str]],
    eval_good,
) -> Generator[List[str], None, None]:

    paths = [["start"]]

    while len(paths) > 0:
        path = paths.pop()
        for next in graph[path[-1]]:
            if next != "start":
                newpath = path + [next]
                if next == "end":
                    yield newpath
                elif eval_good(newpath):
                    paths.append(newpath)


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
