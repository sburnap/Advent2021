from typing import Tuple, List, Generator
from itertools import product
from copy import deepcopy
from heapq import heappush, heappop, heapify


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


def adjacent(
    x: int, y: int, maxx: int, maxy: int
) -> Generator[Tuple[int, int], None, None]:
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)
    if x < maxx:
        yield (x + 1, y)
    if y < maxy:
        yield (x, y + 1)


def dijkstra(floormap: List[List[str]]) -> int:

    distances = deepcopy(floormap)
    for y in range(len(distances)):
        for x in range(len(distances[0])):
            distances[y][x] = None

    distances[0][0] = floormap[0][0]
    stack = []
    heapify(stack)
    heappush(stack, (distances[0][0], 0, 0))
    while True:
        risk, x1, y1 = heappop(stack)

        for x, y in adjacent(x1, y1, len(distances[0]) - 1, len(distances) - 1):
            if not distances[y][x]:
                distances[y][x] = floormap[y][x] + distances[y1][x1]
                heappush(stack, (distances[y][x], x, y))

        if distances[-1][-1]:
            return distances[-1][-1] - distances[0][0]


def day_one(filename: str) -> int:
    return dijkstra(get_map(filename))


def day_two(filename: str) -> int:
    return dijkstra(get_bigmap(filename))


if __name__ == "__main__":

    print("A:")
    print(f"Testinput value is {day_one('Day15/Day15TestInput.txt')}")
    print(f"Realinput value is {day_one('Day15/Day15Input.txt')}")

    print("B:")
    print(f"Testinput value is {day_two('Day15/Day15TestInput.txt')}")
    print(f"Realinput value is {day_two('Day15/Day15Input.txt')}")
