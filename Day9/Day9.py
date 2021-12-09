from typing import List
from functools import reduce
import operator

testinput = [l.strip() for l in open("Day9/Day9TestInput.txt")]


def get_height(floormap: List[List[str]], x: int, y: int) -> int:
    if x < 0 or y < 0 or x >= len(floormap[0]) or y >= len(floormap):
        return 10
    return int(floormap[y][x])


def risk(height: int) -> int:
    return height + 1


def is_lowpoint(floormap: List[List[str]], x: int, y: int) -> bool:
    return get_height(floormap, x, y) < min(
        [
            get_height(floormap, x - 1, y),
            get_height(floormap, x + 1, y),
            get_height(floormap, x, y - 1),
            get_height(floormap, x, y + 1),
        ]
    )


def get_lowpoints(floormap: List[List[str]]):
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
        seen = [lowpoint]
        sz = 0
        while basin:
            x, y = basin.pop()
            sz += 1
            if get_height(floormap, x - 1, y) < 9 and (x - 1, y) not in seen:
                seen.append((x - 1, y))
                basin.append((x - 1, y))
            if get_height(floormap, x + 1, y) < 9 and (x + 1, y) not in seen:
                seen.append((x + 1, y))
                basin.append((x + 1, y))
            if get_height(floormap, x, y - 1) < 9 and (x, y - 1) not in seen:
                seen.append((x, y - 1))
                basin.append((x, y - 1))
            if get_height(floormap, x, y + 1) < 9 and (x, y + 1) not in seen:
                seen.append((x, y + 1))
                basin.append((x, y + 1))
        sizes.append(sz)

    return reduce(operator.mul, sorted(sizes)[-3:])


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day9/Day9TestInput.txt')}")
    print(f"Realinput value is {part_one('Day9/Day9Input.txt')}")

    print("B:")
    print(f"Testinput value is {part_two('Day9/Day9TestInput.txt')}")
    print(f"Realinput value is {part_two('Day9/Day9Input.txt')}")
