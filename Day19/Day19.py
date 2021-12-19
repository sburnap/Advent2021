from enum import unique
from typing import Tuple, List
from math import sqrt
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


class Beacon:
    def __init__(self, scanner, pos):

        self.scanners = {}
        self.beacons = {}
        self.position = pos
        self.home_scanner = scanner

    def add_beacon(self, beacon):
        if beacon.home_scanner == self.home_scanner:
            self.beacons[distance(beacon.position, self.position)] = (beacon,)

    def add_scanner(self, scanner, pos):
        self.scanners[scanner] = pos

    def get_distances(self):
        return [d for d in self.beacons.keys()]


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


def subtract(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:

    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:

    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def make_data(scanners) -> List[Beacon]:
    beacons: List[Beacon] = []

    for s in range(len(scanners)):
        for i in range(len(scanners[s])):
            beacon = Beacon(s, scanners[s][i])

            for j in range(len(beacons)):
                beacons[j].add_beacon(beacon)
                beacon.add_beacon(beacons[j])

            beacons.append(beacon)

    scanner_dict = {0: Scanner()}

    unique_beacons: Beacon = []
    for b1 in beacons:
        is_unique = True
        for b2 in unique_beacons:
            if b1.home_scanner != b2.home_scanner:
                dist1 = set(b1.get_distances())
                dist2 = set(b2.get_distances())

                common = dist1.intersection(dist2)
                if len(common) > 1:
                    is_unique = False
                    b2.add_scanner(b1.home_scanner, b1.position)
                    if (
                        b2.home_scanner in scanner_dict.keys()
                        and b1.home_scanner not in scanner_dict.keys()
                    ):
                        one = next(iter(common))

                        b1_other = b1.beacons[one]
                        b2_other = b2.beacons[one]
                        vec1 = subtract(
                            b1_other[0].position, b1_other[0].beacons[one][0].position
                        )
                        vec2 = subtract(
                            b2_other[0].position, b2_other[0].beacons[one][0].position
                        )
                        scanner_dict[b1.home_scanner] = Scanner(
                            b2_other[0].position,
                            vec1,
                            vec2,
                        )

        if is_unique:
            unique_beacons.append(b1)

    return unique_beacons, scanner_dict


def part_one(filename: str) -> int:
    scanners = read_input(filename)

    data, _ = make_data(scanners)
    return len(data)


def part_two(filename: str) -> int:

    scanners = read_input(filename)

    unique_beacons, scanner_dict = make_data(scanners)

    for s in range(len(scanners)):
        if not scanner_dict[s].pos:
            for b1 in unique_beacons:
                if s in b1.scanners:
                    s2_beacon_pos = b1.scanners[s]
                    t_pos = scanner_dict[s].transform(s2_beacon_pos)
                    s_pos = subtract(b1.position, t_pos)
                    s_pos = add(s_pos, scanner_dict[b1.home_scanner].pos)
                    scanner_dict[s].set_position(s_pos)
                    print("Figure Out this")
                    break

    mx = 0
    for s1 in scanner_dict:
        for s2 in scanner_dict:
            if s1 != s2:
                m = man_distance(scanner_dict[s1].pos, scanner_dict[s2].pos)
                if m > mx:
                    mx = m
    return mx


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day19/Day19TestInput.txt')}")
    print(f"Realinput value is {part_one('Day19/Day19Input.txt')}")

    print("B:")
    print(f"Testinput value is {part_two('Day19/Day19TestInput.txt')}")
    print(f"Realinput value is {part_two('Day19/Day19Input.txt')}")
