from typing import List, Tuple
from collections import Counter
import re

Position = Tuple[int, int]
VentDef = Tuple[Position, Position]

re_inputline = re.compile("^(\d*),(\d*) -> (\d*),(\d*)$")


def parse_line(s: str) -> VentDef:
    if m := re_inputline.match(s):
        return ((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4))))

    raise Exception(f"You're input is crap: '{s}'")


def read_vents(filename: str) -> Tuple[VentDef, ...]:
    return tuple(parse_line(line) for line in open(filename))


def direction(x: int) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def walk(
    xstart: int,
    ystart: int,
    xfinish: int,
    yfinish: int,
    xstep: int,
    ystep: int,
    cnts: Counter,
) -> Counter:

    x = xstart
    y = ystart
    while True:
        cnts[(x, y)] += 1
        if x == xfinish and y == yfinish:
            break
        x += xstep
        y += ystep

    return cnts


def find_counts(vents: Tuple[VentDef, ...], follow_diagonals: bool) -> Counter:
    cnts: Counter = Counter()
    for (xstart, ystart), (xfinish, yfinish) in vents:

        xstep = direction(xfinish - xstart)
        ystep = direction(yfinish - ystart)

        if follow_diagonals or xstep == 0 or ystep == 0:
            cnts = walk(xstart, ystart, xfinish, yfinish, xstep, ystep, cnts)

    return cnts


def day_one(filename: str) -> int:

    cnts = find_counts(read_vents(filename), follow_diagonals=False)
    return len([cnt for cnt in cnts.most_common() if cnt[1] >= 2])


def day_two(filename: str) -> int:

    cnts = find_counts(read_vents(filename), follow_diagonals=True)
    return len([cnt for cnt in cnts.most_common() if cnt[1] >= 2])


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {day_one('Day5/Day5Testinput.txt')}")
    print(f"Realinput value is {day_one('Day5/Day5Input.txt')}")

    print("B:")
    print(f"Testinput value is {day_two('Day5/Day5Testinput.txt')}")
    print(f"Realinput value is {day_two('Day5/Day5Input.txt')}")
