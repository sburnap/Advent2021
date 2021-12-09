from typing import List, Tuple, Generator
from functools import reduce
import operator

testinput = [l.strip() for l in open("Day9/Day9TestInput.txt")]


def get_height(floormap: List[str], x: int, y: int) -> int:
    if x < 0 or y < 0 or x >= len(floormap[0]) or y >= len(floormap):
        return 10
    return int(floormap[y][x])


def risk(height: int) -> int:
    return height + 1


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
    lowpoints = []
    for y in range(len(floormap)):
        for x in range(len(floormap[0])):
            if is_lowpoint(floormap, x, y):
                lowpoints.append((x, y))
    return lowpoints


def part_one(filename: str) -> int:
    floormap = [l.strip() for l in open(filename)]

    return sum([risk(get_height(floormap, x, y)) for x, y in get_lowpoints(floormap)])


def part_two(filename: str) -> int:
    floormap = [l.strip() for l in open(filename)]

    lowpoints = get_lowpoints(floormap)
    sizes = []
    for lowpoint in lowpoints:
        basin = [lowpoint]
        sz = 0
        i = 0
        while i < len(basin):
            x, y = basin[i]
            sz += 1
            for xa, ya in adjacent(x, y):
                if get_height(floormap, xa, ya) < 9 and (xa, ya) not in basin:
                    basin.append((xa, ya))
            i += 1

        sizes.append(sz)

    return reduce(operator.mul, sorted(sizes)[-3:])


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day9/Day9TestInput.txt')}")
    print(f"Realinput value is {part_one('Day9/Day9Input.txt')}")

    print("B:")
    print(f"Testinput value is {part_two('Day9/Day9TestInput.txt')}")
    print(f"Realinput value is {part_two('Day9/Day9Input.txt')}")
