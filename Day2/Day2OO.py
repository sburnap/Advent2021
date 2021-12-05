testinput = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
realinput = [l for l in open("Day2Input.txt")]


def to_orders(l):
    return [(a, int(b)) for a, b in (i.split(" ") for i in l)]


class Traveler:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0

    def up(self, x):
        self.depth -= x

    def down(self, x):
        self.depth += x

    def forward(self, x):
        self.horizontal += x

    def extant(self):
        return self.depth * self.horizontal


class Traveler2:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0
        self.aim = 0

    def up(self, x):
        self.aim -= x

    def down(self, x):
        self.aim += x

    def forward(self, x):
        self.horizontal += x
        self.depth += x * self.aim

    def extant(self):
        return self.depth * self.horizontal


def travel(cls, l):
    traveler = cls()
    for cmd, x in l:
        getattr(traveler, cmd)(x)

    return traveler.extant()


if __name__ == "__main__":
    print("A:")
    print(f"Testinput travel is {travel(Traveler, to_orders(testinput))}")
    print(f"Realinput travel is {travel(Traveler, to_orders(realinput))}")

    print("B:")
    print(f"Testinput travel is {travel(Traveler2, to_orders(testinput))}")
    print(f"Realinput travel is {travel(Traveler2, to_orders(realinput))}")
