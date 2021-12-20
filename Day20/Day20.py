from typing import Generator, Tuple, Set


def read_input(filename: str) -> Tuple[str, Set[Tuple[int, int]]]:
    lines = [line for line in open(filename)]

    mapping = lines[0].strip()

    spots = set()
    y = 0
    for line in lines[2:]:
        for x in range(len(line)):
            if line[x] == "#":
                spots.add((x, y))
        y += 1

    return mapping, spots


Image = Set[Tuple[int, int]]


def map_range(spots: Image) -> Tuple[Tuple[int, int], Tuple[int, int]]:

    minx = min(spot[0] for spot in spots)
    maxx = max(spot[0] for spot in spots)
    miny = min(spot[1] for spot in spots)
    maxy = max(spot[1] for spot in spots)

    return ((minx, maxx), (miny, maxy))


def adjacent(x: int, y: int) -> Generator[Tuple[int, int], None, None]:
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1

    yield x - 1, y
    yield x, y
    yield x + 1, y

    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1


def pixel_on(spots: Image, x: int, y: int, mapping):
    value = int(
        "".join("1" if (x1, y1) in spots else "0" for x1, y1 in adjacent(x, y)), 2
    )
    return mapping[value] == "#"


def one_step(spots: Image, mapping: str, steps: int) -> Image:

    (minx, maxx), (miny, maxy) = map_range(spots)
    if mapping[0] == "#":
        minx -= steps * 2 - 1
        miny -= steps * 2 - 1
        maxx += steps * 2 - 1
        maxy += steps * 2 - 1
    else:
        minx -= 1
        miny -= 1
        maxx += 1
        maxy += 1

    newspots = set()

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if pixel_on(spots, x, y, mapping):
                newspots.add((x, y))

    return newspots


def print_map(spots: Image):

    (minx, maxx), (miny, maxy) = map_range(spots)

    print(f"{minx},{miny} - {maxx},{maxy}")
    for y in range(miny, maxy + 1):
        print("".join("#" if (x, y) in spots else "." for x in range(minx, maxx + 1)))


def do_steps(filename: str, steps) -> int:
    mapping, spots = read_input(filename)

    for i in range(steps):
        spots = one_step(spots, mapping, steps)

        if i % 2 == 1:

            if mapping[0] == "#":
                (minx, maxx), (miny, maxy) = map_range(spots)
                minx += steps * 2
                miny += steps * 2
                maxx -= steps * 2
                maxy -= steps * 2

                newspots = set()
                for y in range(miny, maxy + 1):
                    for x in range(minx, maxx + 1):
                        if (x, y) in spots:
                            newspots.add((x, y))
                spots = newspots
    # print_map(spots)
    return len(spots)


def day_one(filename: str) -> int:
    return do_steps(filename, 2)


def day_two(filename: str) -> int:
    return do_steps(filename, 50)


if __name__ == "__main__":

    print("A:")
    print(f"Testinput value is {day_one('Day20/Day20TestInput.txt')}")
    print(f"Realinput value is {day_one('Day20/Day20Input.txt')}")

    print("B:")
    print(f"Testinput value is {day_two('Day20/Day20TestInput.txt')}")
    print(f"Realinput value is {day_two('Day20/Day20Input.txt')}")
