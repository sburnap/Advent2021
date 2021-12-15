from typing import Tuple, List, Generator
from itertools import product


def print_map(cavemap: List[List[int]]) -> None:
    for y in cavemap:
        print("".join([str(r) for r in y]))


def get_map(filename: str) -> List[List[int]]:
    return [[int(ch) for ch in line.strip()] for line in open(filename)]


def get_bigmap(filename: str) -> List[List[int]]:
    lines = [line.strip() for line in open(filename)]

    bigmap = []
    for ty in range(5):
        for y in range(len(lines)):
            bigmap.append([None] * len(lines[y] * 5))
            for tx in range(5):
                for x in range(len(lines[y])):
                    bigmap[ty * len(lines) + y][tx * len(lines[0]) + x] = (
                        int(lines[y][x]) + ty + tx
                    )

                    if bigmap[ty * len(lines) + y][tx * len(lines[0]) + x] > 9:
                        bigmap[ty * len(lines) + y][tx * len(lines[0]) + x] -= 9

    return bigmap


def print_path(floormap, path):
    print(f"{path}: {risk(floormap, path)} -> {[floormap[y][x] for x,y in path]}")


def before(x: int, y: int) -> Generator[Tuple[int, int], None, None]:
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)


def iterate_x_y(two_d: List[List[int]]) -> Generator[Tuple[int, int], None, None]:
    return ((x, y) for y, x in product(range(len(two_d)), range(len(two_d[0]))))


def dijkstra(floormap: List[List[str]]) -> int:

    for x, y in iterate_x_y(floormap):
        if x > 0 or y > 0:
            floormap[y][x] += min([floormap[y][x] for x, y in before(x, y)])

    return floormap[-1][-1] - floormap[0][0]


def day_one(filename: str) -> int:
    floormap = get_map(filename)

    return dijkstra(floormap)


def day_two(filename: str) -> int:
    floormap = get_bigmap(filename)
    # print_map(floormap)
    return dijkstra(floormap)


if __name__ == "__main__":

    print("A:")
    print(f"Testinput value is {day_one('Day15/Day15TestInput.txt')}")
    print(f"Realinput value is {day_one('Day15/Day15Input.txt')}")

    print("B:")
    print(f"Testinput value is {day_two('Day15/Day15TestInput.txt')}")
    print(f"Realinput value is {day_two('Day15/Day15Input.txt')}")
