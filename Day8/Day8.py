from typing import List
from collections import Counter


def part_one(filename):
    inp = list(
        (a.split(" "), b.split(" "))
        for a, b in (l.strip().split(" | ") for l in open(filename))
    )

    cnts = Counter()
    for l in inp:
        cnts.update((len(digit) for digit in l[1]))

    #          1         7         4          8
    return cnts[2] + cnts[3] + cnts[4] + cnts[7]


def find_digits(l: List[str]):

    all = set(["".join(sorted(digit)) for digit in l])
    cnts = Counter()
    for digit in all:
        cnts.update(digit)

    # Utterly relies on all ten digits appearing in a line
    spots = {}
    for ch in cnts:
        if cnts[ch] == 6:
            spots["b"] = ch
        elif cnts[ch] == 4:
            spots["e"] = ch
        elif cnts[ch] == 9:
            spots["f"] = ch

    for digit in all:
        if len(digit) == 2:  # c + f  -> c unknown
            spots["c"] = next(ch for ch in digit if ch != spots["f"])
            break

    for digit in all:
        if len(digit) == 3:  # a + c + f -> a unknown
            spots["a"] = next(ch for ch in digit if ch not in (spots["c"], spots["f"]))
            break

    for digit in all:
        if len(digit) == 4:  # b + c + d + f -> d unknown
            spots["d"] = next(
                ch for ch in digit if ch not in (spots["b"], spots["c"], spots["f"])
            )
            break

    # g only unknown left
    spots["g"] = next(
        ch
        for ch in "abcdefg"
        if ch
        not in [spots["a"], spots["b"], spots["c"], spots["d"], spots["e"], spots["f"]]
    )

    dig_defs = {
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "abdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg",
    }

    return {"".join(sorted([spots[ch] for ch in dig_defs[i]])): i for i in range(10)}


def part_two(filename):
    inp = list(
        (a.split(" "), b.split(" "))
        for a, b in (l.strip().split(" | ") for l in open(filename))
    )

    s = 0
    for i, o in inp:
        calcs = find_digits(i + o)

        s += int(
            "".join([str(calcs[sdig]) for sdig in ["".join(sorted(dig)) for dig in o]])
        )

    return s


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {part_one('Day8/Day8TestInput.txt')}")
    print(f"Realinput value is {part_one('Day8/Day8Input.txt')}")

    print("B:")
    print(f"Testinput value is {part_two('Day8/Day8TestInput.txt')}")
    print(f"Realinput value is {part_two('Day8/Day8Input.txt')}")
