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


class Beacon:
    def __init__(self, scanner, pos):

        self.scanners = {}
        self.beacons = {}
        self.position = pos
        self.home_scanner = scanner
        self.scanners[scanner] = distance((0, 0, 0), pos)

    def add_beacon(self, beacon):
        if beacon.home_scanner == self.home_scanner:
            self.beacons[distance(beacon.position, self.position)] = beacon

    def get_distances(self):
        return [d for d in self.beacons.keys()]


def part_one(filename: str) -> int:
    scanners = read_input(filename)

    beacons: List[Beacon] = []

    for s in range(len(scanners)):
        for i in range(len(scanners[s])):
            beacon = Beacon(s, scanners[s][i])

            for j in range(len(beacons)):
                beacons[j].add_beacon(beacon)
                beacon.add_beacon(beacons[j])

            beacons.append(beacon)

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
                    break

        if is_unique:
            unique_beacons.append(b1)

    return len(unique_beacons)


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day19/Day19TestInput.txt')}")
    print(f"Realinput value is {part_one('Day19/Day19Input.txt')}")

    print("B:")
    # print(f"Testinput value is {part_two(testinput)}")
    # print(f"Realinput value is {part_two(realinput)}")
