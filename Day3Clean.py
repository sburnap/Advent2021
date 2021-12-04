testinput = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]
realinput = [l.strip() for l in open("Day3Input.txt")]


def common(l, digit):
    ones = len([s for s in l if s[digit] == "1"])

    return "1" if ones >= len(l) / 2 else "0"


def times_inverse(bin, digits):
    return bin * (bin ^ (2 ** digits - 1))


def day_one(l):
    digits = len(l[0])
    gamma = eval("0b" + "".join([common(l, i) for i in range(digits)]))
    return times_inverse(gamma, digits)


def day_two(l):
    o2 = co2 = l
    for i in range(len(l[0])):
        o2 = o2 if len(o2) == 1 else [s for s in o2 if s[i] == common(o2, i)]
        co2 = co2 if len(co2) == 1 else [s for s in co2 if s[i] != common(co2, i)]

    return eval(f"0b{o2[0]} * 0b{co2[0]}")


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {day_one(testinput)}")
    print(f"Realinput value is {day_one(realinput)}")

    print("B:")
    print(f"Testinput value is {day_two(testinput)}")
    print(f"Realinput value is {day_two(realinput)}")
