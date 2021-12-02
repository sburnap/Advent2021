from itertools import accumulate
from functools import reduce

testinput = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
realinput = [l for l in open("Day2Input.txt")]


def to_orders(l):
    return [(a, int(b)) for a, b in (i.split(" ") for i in l)]


def to_dir(cmd, x):
    if cmd == "forward":
        return (x, 0)
    if cmd == "down":
        return (0, x)
    if cmd == "up":
        return (0, -x)


def to_dirs(l):
    return (to_dir(cmd, x) for cmd, x in l)


def sum_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


def product(l):
    return reduce(lambda x, y: x * y, l)


def day_one(l):
    return product(
        reduce(
            sum_tuple,
            to_dirs(l),
        )
    )


def sum_tuple_2nd(t1, t2):
    return (t2[0], t1[1] + t2[1])


def sum_with_aim(t1, t2):
    return (t1[0] + t2[0], t1[1] + (t2[1] * t2[0]))


def day_two(l):

    return product(
        reduce(
            sum_with_aim,
            accumulate(to_dirs(l), sum_tuple_2nd, initial=(0, 0)),
        )
    )


if __name__ == "__main__":
    print("A:")
    print(f"Testinput travel is {day_one(to_orders(testinput))}")
    print(f"Realinput travel is {day_one(to_orders(realinput))}")

    print("B:")
    print(f"Testinput travel is {day_two(to_orders(testinput))}")
    print(f"Realinput travel is {day_two(to_orders(realinput))}")
