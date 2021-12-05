from itertools import accumulate

testinput = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
realinput = [l for l in open("Day2Input.txt")]


def to_orders(l):
    return [(a, int(b)) for a, b in (i.split(" ") for i in l)]


def day_one(l):
    def direction(cmd):
        return {"down": 1, "up": -1, "forward": 0}[cmd]

    def depth(l):
        return sum(x * direction(cmd) for cmd, x in l)

    def horizontal(l):
        return sum(x for cmd, x in l if cmd == "forward")

    return depth(l) * horizontal(l)


def day_two(l):
    def direction(cmd):
        return {"down": 1, "up": -1, "forward": 0}[cmd]

    def aim(l):
        return accumulate(direction(cmd) * x for cmd, x in l)

    def depth(aim, l):
        return sum(
            a * b for a, b in zip(aim, (x if cmd == "forward" else 0 for cmd, x in l))
        )

    def horizontal(l):
        return sum(x if cmd == "forward" else 0 for cmd, x in l)

    return depth(aim(l), l) * horizontal(l)


if __name__ == "__main__":
    print("A:")
    print(f"Testinput travel is {day_one(to_orders(testinput))}")
    print(f"Realinput travel is {day_one(to_orders(realinput))}")

    print("B:")
    print(f"Testinput travel is {day_two(to_orders(testinput))}")
    print(f"Realinput travel is {day_two(to_orders(realinput))}")
