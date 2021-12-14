from typing import List, Tuple, Generator
from itertools import product
import re


def get_re_lines(lines: List[str], regex) -> List[Tuple[str, str]]:
    for line in lines:
        if m := regex.match(line):
            yield (m.group(1), m.group(2))


def get_paper(spots: List[Tuple[int, int]]) -> List[List[str]]:

    maxx: int = max(spot[0] for spot in spots) + 1
    maxy: int = max(spot[1] for spot in spots) + 1

    paper = [["."] * maxx for _ in range(maxy)]
    for x, y in spots:
        paper[y][x] = "#"

    return paper


def print_paper(paper: (List[List[str]])):
    for line in paper:
        print("".join(line))


def read_input(filename: str):
    lines = [line for line in open(filename)]

    paper = get_paper(
        [(int(x), int(y)) for x, y in get_re_lines(lines, re.compile(r"^(\d*),(\d*)$"))]
    )
    folds = [
        (x, int(y))
        for x, y in get_re_lines(lines, re.compile(r"^fold along (x|y)=(\d*)$"))
    ]

    return paper, folds


def iterate_x_y(two_d: List[List[int]]) -> Generator[Tuple[int, int], None, None]:
    return ((x, y) for y, x in product(range(len(two_d)), range(len(two_d[0]))))


def fold(paper, folds, only_once: bool):
    for axis, val in folds:
        if axis == "y":
            sideb = paper[:val:-1]
            paper = paper[:val]

            # Handle blank lines at the bottom
            while len(paper) != len(sideb):
                sideb.insert(0, ["."] * len(paper[0]))

        elif axis == "x":
            sideb = [line[:val:-1] for line in paper]
            paper = [line[:val] for line in paper]

            # Should handle blank columns at the sideb but I don't seem to need to

        for x, y in iterate_x_y(paper):
            if sideb[y][x] == "#":
                paper[y][x] = "#"

        if only_once:
            break

    return paper


def part_one(filename: str) -> int:
    paper = fold(*read_input(filename), only_once=True)
    return sum(len([spot for spot in row if spot == "#"]) for row in paper)


def part_two(filename: str) -> int:
    paper = fold(*read_input(filename), only_once=False)
    print_paper(paper)


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day13/Day13TestInput.txt')}")
    print(f"Realinput value is {part_one('Day13/Day13Input.txt')}")

    print("B:")
    print(f"Testinput value is {part_two('Day13/Day13TestInput.txt')}")
    print(f"Realinput value is {part_two('Day13/Day13Input.txt')}")
