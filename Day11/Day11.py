from typing import Generator, Tuple, List
from itertools import product


def adjacent(
    x: int, y: int, use_diagonals: bool = True
) -> Generator[Tuple[int, int], None, None]:
    yield (x - 1, y)
    yield (x, y - 1)
    yield (x, y + 1)
    yield (x + 1, y)

    if use_diagonals:
        yield (x + 1, y + 1)
        yield (x + 1, y - 1)
        yield (x - 1, y + 1)
        yield (x - 1, y - 1)


def read_input(filename: str) -> List[List[int]]:

    return [[int(ch) for ch in line] for line in [l.strip() for l in open(filename)]]


def iterate_x_y(two_d) -> Generator[Tuple[int, int], None, None]:
    return ((x, y) for x, y in product(range(len(two_d)), range(len(two_d[0]))))


def check_for_flash(octopi: List[List[int]], x: int, y: int) -> int:
    flashes = 0

    if octopi[y][x] > 9:
        octopi[y][x] = 0
        flashes += 1

        for x, y in adjacent(x, y):
            if x >= 0 and y >= 0 and y < len(octopi) and x < len(octopi[0]):
                if octopi[y][x] != 0:
                    octopi[y][x] += 1
                    flashes += check_for_flash(octopi, x, y)

    return flashes


def do_step(octopi: List[List[int]]) -> int:
    for x, y in iterate_x_y(octopi):
        octopi[y][x] += 1

    return sum(check_for_flash(octopi, x, y) for x, y in iterate_x_y(octopi))


def part_one(filename: str, steps) -> int:
    octopi = read_input(filename)

    return sum(do_step(octopi) for i in range(steps))


def part_two(filename: str) -> int:
    octopi = read_input(filename)

    flashes = 0
    steps = 0
    while flashes < len(octopi) * len(octopi[0]):
        flashes = do_step(octopi)
        steps += 1

    return steps


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day11/Day11TestInput.txt', 100)}")
    print(f"Realinput value is {part_one('Day11/Day11Input.txt', 100)}")

    print("B:")
    print(f"Testinput value is {part_two('Day11/Day11TestInput.txt')}")
    print(f"Realinput value is {part_two('Day11/Day11Input.txt')}")
