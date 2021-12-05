from typing import Tuple, Generator
from collections import Counter
import re

Position = Tuple[int, int]
VentDef = Tuple[Position, Position]

re_inputline = re.compile("^(\d*),(\d*) -> (\d*),(\d*)$")


def parse_line(s: str) -> VentDef:
    if m := re_inputline.match(s):
        return ((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4))))

    raise Exception(f"Your input is crap: '{s}'")


def read_vents(filename: str) -> Tuple[VentDef, ...]:
    return tuple(parse_line(line) for line in open(filename))


def rev_range_inclusive(a: int, b: int) -> range:
    if b >= a:
        return range(a, b + 1)
    else:
        return range(a, b - 1, -1)


def walk(start: Position, finish: Position) -> Generator[Position, None, None]:

    (xstart, ystart), (xfinish, yfinish) = start, finish

    if xstart != xfinish and ystart != yfinish:
        for x, y in zip(
            rev_range_inclusive(xstart, xfinish),
            rev_range_inclusive(ystart, yfinish),
        ):
            yield x, y
    elif xstart == xfinish:
        for y in rev_range_inclusive(ystart, yfinish):
            yield xstart, y
    elif ystart == yfinish:
        for x in rev_range_inclusive(xstart, xfinish):
            yield x, ystart


def is_diagonal(start: Position, finish: Position) -> bool:
    return start[0] != finish[0] and start[1] != finish[1]


def walk_vents(
    vents: Tuple[VentDef, ...], follow_diagonals: bool
) -> Generator[Position, None, None]:
    for vent in vents:
        if follow_diagonals or not is_diagonal(vent[0], vent[1]):
            for x, y in walk(vent[0], vent[1]):
                yield x, y


def find_overlaps(filename: str, follow_diagonals: bool) -> int:
    return len(
        [
            cnt
            for cnt in Counter(
                walk_vents(read_vents(filename), follow_diagonals=follow_diagonals)
            ).most_common()
            if cnt[1] >= 2
        ]
    )


def day_one(filename: str) -> int:
    return find_overlaps(filename, follow_diagonals=False)


def day_two(filename: str) -> int:
    return find_overlaps(filename, follow_diagonals=True)


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {day_one('Day5/Day5Testinput.txt')}")
    print(f"Realinput value is {day_one('Day5/Day5Input.txt')}")

    print("B:")
    print(f"Testinput value is {day_two('Day5/Day5Testinput.txt')}")
    print(f"Realinput value is {day_two('Day5/Day5Input.txt')}")
