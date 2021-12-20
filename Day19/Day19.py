from enum import unique
from typing import Tuple, List
from math import dist, sqrt
import re


def read_input(filename: str):
    re_scanner = re.compile(r"--- scanner (\d+) ---")
    re_location = re.compile(r"([-\d]+),([-\d]+),([-\d]+)")

    scanners = {}

    for line in open(filename):
        if m := re_scanner.match(line):
            scanner = int(m.group(1))
            scanners[scanner] = []
        elif m := re_location.match(line):
            x, y, z = int(m.group(1)), int(m.group(2)), int(m.group(3))
            scanners[scanner].append((x, y, z))

    return scanners


def distance(b1: Tuple[int, int, int], b2: Tuple[int, int, int]) -> int:
    x1, y1, z1 = (float(d) for d in b1)
    x2, y2, z2 = (float(d) for d in b2)

    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def man_distance(b1: Tuple[int, int, int], b2: Tuple[int, int, int]) -> int:
    x1, y1, z1 = (d for d in b1)
    x2, y2, z2 = (d for d in b2)

    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


class Scanner:
    def __init__(self, pos=None, vec1=None, vec2=None):
        self.pos = None
        if pos:
            self.indices = []
            self.signs = []

            for i in range(3):
                self.indices.append([abs(j) for j in vec2].index(abs(vec1[i])))
            for i in range(3):
                self.signs.append(vec1[i] // vec2[self.indices[i]])

        else:
            self.indices = [0, 1, 2]
            self.signs = [1, 1, 1]
            self.pos = (0, 0, 0)

    def set_position(self, pos):
        self.pos = pos

    def transform(self, vec: Tuple[int, int, int]) -> Tuple[int, int, int]:
        return (
            self.signs[0] * vec[self.indices[0]],
            self.signs[1] * vec[self.indices[1]],
            self.signs[2] * vec[self.indices[2]],
        )

    def __repr__(self):
        return f"Scanner at {self.pos}"


def subtract(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:

    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:

    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


class Beacon:
    def __init__(self, num, pos):
        self.num = num
        self.pos = pos
        self.distances = {}

    def add_distance(self, distance: float, beacon):
        self.distances[distance] = beacon

    def __repr__(self):
        return f"Beacon {self.num} at {self.pos}"


def make_beacon_distances(beacon_list):
    beacon_distances = {}
    for b1 in beacon_list:
        for b2 in beacon_list:
            if b1 != b2:
                dist = distance(b1.pos, b2.pos)
                if dist not in beacon_distances:
                    beacon_distances[dist] = []

                beacon_distances[dist].append((b1, b2))
                b1.add_distance(dist, b2)
                b2.add_distance(dist, b1)

    return beacon_distances


def get_scanner_contents(scanner_def):
    beacon_list = [Beacon(i, pos) for i, pos in enumerate(scanner_def)]

    return (beacon_list, make_beacon_distances(beacon_list))


def get_scanner_position(scanner0, scanner0_contents, scanner1_contents):
    common_distances = set(scanner0_contents[1].keys()).intersection(
        set(scanner1_contents[1].keys())
    )
    for common_distance in common_distances:
        beacon1 = scanner0_contents[1][common_distance][0][0]

        for beacon in scanner1_contents[0]:
            x = len([dist for dist in beacon.distances if dist in beacon1.distances])

            # multiple common distances mean these are both the same beacon
            if x > 1:
                # create vectors for one of the edges between this beacon and another one
                vec1 = subtract(beacon1.pos, beacon1.distances[common_distance].pos)
                vec2 = subtract(beacon.pos, beacon.distances[common_distance].pos)

                # Use that to create a scanner with a transformed coordinate space
                scanner = Scanner(beacon.pos, vec1, vec2)

                # transform the beacon we just found into the common coordinate space
                bpos = scanner.transform(beacon.pos)

                # subtract off it's old positon, giving us the scanner position
                diffpos = subtract(beacon1.pos, bpos)
                scanner.set_position(diffpos)
                return scanner

    return None


def merge_scanner(scanner1, scanner1_contents, knownbeacons):

    newbeacons = []
    for beacon in scanner1_contents[0]:
        pos = add(scanner1.pos, scanner1.transform(beacon.pos))

        try:
            newbeacons.append(knownbeacons[pos])
        except:
            beacon.pos = pos
            newbeacons.append(beacon)
            knownbeacons[pos] = beacon

    return (newbeacons, scanner1_contents[1])


def calc_stuff(filename: str):
    scanner_input = read_input(filename)

    scanner_contents = [
        get_scanner_contents(scanner_input[i]) for i in range(len(scanner_input))
    ]

    knownbeacons = {beacon.pos: beacon for beacon in scanner_contents[0][0]}

    scanners = {0: Scanner()}
    while len(scanners) < len(scanner_contents):
        for i in range(1, len(scanner_contents)):
            if i not in scanners:
                for j in scanners.keys():
                    if scanner := get_scanner_position(
                        scanners[j], scanner_contents[j], scanner_contents[i]
                    ):
                        scanner_contents[i] = merge_scanner(
                            scanner, scanner_contents[i], knownbeacons
                        )
                        scanners[i] = scanner
                        break

    return scanners, knownbeacons


def part_one(knownbeacons) -> int:

    return len(knownbeacons)


def pairwise_manhattan_distances(scanners):
    for s1 in scanners:
        for s2 in scanners:
            if s1 != s2:
                yield man_distance(scanners[s1].pos, scanners[s2].pos)


def part_two(scanners) -> int:

    return max(dist for dist in pairwise_manhattan_distances(scanners))


if __name__ == "__main__":
    testinput = calc_stuff("Day19/Day19TestInput.txt")
    realinput = calc_stuff("Day19/Day19Input.txt")

    print("A:")
    print(f"Testinput value is {part_one(testinput[1])}")
    print(f"Realinput value is {part_one(realinput[1])}")

    print("B:")
    print(f"Testinput value is {part_two(testinput[0])}")
    print(f"Realinput value is {part_two(realinput[0])}")
