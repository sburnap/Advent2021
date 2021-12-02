testinput = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
realinput = [l for l in open("Day2Input.txt")]


def to_orders(l):
    return [(a, int(b)) for a, b in (i.split(" ") for i in l)]


def travel(l):
    h = 0
    d = 0
    for c, x in to_orders(l):
        if c == "forward":
            h += x
        elif c == "down":
            d += x
        elif c == "up":
            d -= x

    return h, d


def travel2(l):
    h = 0
    d = 0
    aim = 0
    for c, x in to_orders(l):
        if c == "forward":
            h += x
            d += x * aim
        elif c == "down":
            aim += x
        elif c == "up":
            aim -= x

    return h, d


if __name__ == "__main__":
    print("A:")
    h, d = travel(testinput)
    print(f"Testinput travel is {h*d}")
    h, d = travel(realinput)
    print(f"Realinput travel is {h*d}")

    print("B:")
    h, d = travel2(testinput)
    print(f"Testinput travel is {h*d}")
    h, d = travel2(realinput)
    print(f"Realinput travel is {h*d}")
