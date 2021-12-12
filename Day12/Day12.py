from typing import Generator, List, Dict
import re
from collections import defaultdict

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


def get_paths(
    graph: Dict[str, List[str]], start="start"
) -> Generator[List[str], None, None]:

    paths = [[start]]

    while len(paths) > 0:
        path = paths.pop()
        for next in graph[path[-1]]:
            newpath = path + [next]
            if next == "end":
                yield newpath
            elif next.isupper() or next not in path:
                paths.append(newpath)


def part_one(filename: str) -> int:
    return len([path for path in get_paths(read_input(filename))])


if __name__ == "__main__":
    print("A:")
    print(f"Testinput1 value is {part_one('Day12/Day12TestInput1.txt')}")
    print(f"Testinput2 value is {part_one('Day12/Day12TestInput2.txt')}")
    print(f"Realinput value is {part_one('Day12/Day12Input.txt')}")

    # print("B:")
    # print(f"Testinput value is {part_two('Day12/Day12TestInput.txt')}")
    # print(f"Realinput value is {part_two('Day12/Day12Input.txt')}")
