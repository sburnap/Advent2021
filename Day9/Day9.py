from os import walk
from typing import List, Tuple, Generator
from functools import reduce
from itertools import product
import operator


def get_height(floormap: List[str], x: int, y: int) -> int:
    if x < 0 or y < 0 or x >= len(floormap[0]) or y >= len(floormap):
        return 10
    return int(floormap[y][x])


def risk(floormap: List[str], x: int, y: int) -> int:
    return get_height(floormap, x, y) + 1


def adjacent(x: int, y: int) -> Generator[Tuple[int, int], None, None]:
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y - 1)
    yield (x, y + 1)


def is_lowpoint(floormap: List[str], x: int, y: int) -> bool:
    return get_height(floormap, x, y) < min(
        [get_height(floormap, xa, ya) for xa, ya in adjacent(x, y)]
    )


def get_lowpoints(floormap: List[str]):

    return [
        (x, y)
        for x, y in product(range(len(floormap[0])), range(len(floormap)))
        if is_lowpoint(floormap, x, y)
    ]


def parse_floormap(filename: str) -> List[str]:
    return [l.strip() for l in open(filename)]


def part_one(filename: str) -> int:
    floormap = [l.strip() for l in open(filename)]

    return sum([risk(floormap, x, y) for x, y in get_lowpoints(floormap)])


def basin_size(floormap: List[str], lowpoint: Tuple[int]):
    basin = [lowpoint]
    i = 0
    while i < len(basin):
        for xa, ya in adjacent(*basin[i]):
            if get_height(floormap, xa, ya) < 9 and (xa, ya) not in basin:
                basin.append((xa, ya))
        i += 1

    return len(basin)


def part_two(filename: str) -> int:
    floormap = [l.strip() for l in open(filename)]

    return reduce(
        operator.mul,
        sorted(
            [basin_size(floormap, lowpoint) for lowpoint in get_lowpoints(floormap)]
        )[-3:],
    )


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day9/Day9TestInput.txt')}")
    print(f"Realinput value is {part_one('Day9/Day9Input.txt')}")

    print("B:")
    print(f"Testinput value is {part_two('Day9/Day9TestInput.txt')}")
    print(f"Realinput value is {part_two('Day9/Day9Input.txt')}")
