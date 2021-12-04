from collections import Counter

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


def count_digits(l):
    digits = len(l[0])
    total = len(l)
    counts = [Counter() for _ in range(digits)]
    for s in l:
        for i in range(digits):
            counts[i][s[i]] += 1
    return digits, counts


def day_one(l):
    digits, counts = count_digits(l)

    gamma = 0
    epsilon = 0
    for i in range(digits):
        gamma *= 2
        epsilon *= 2
        gamma += int(counts[i].most_common()[0][0])
        epsilon += int(counts[i].most_common()[-1][0])
    return gamma * epsilon


def to_dec(s):
    rc = 0
    for c in s:
        rc *= 2
        rc += int(c)

    return rc


def o2(l):
    digits = len(l[0])
    for i in range(digits):
        ones = len([s for s in l if s[i] == "1"])
        target = "1" if ones >= len(l) - ones else "0"
        l = [s for s in l if s[i] == target]
        if len(l) == 1:
            break

    return to_dec(l[0])


def co2(l):
    digits = len(l[0])
    for i in range(digits):
        ones = len([s for s in l if s[i] == "1"])
        target = "1" if ones < len(l) - ones else "0"
        l = [s for s in l if s[i] == target]
        if len(l) == 1:
            break

    return to_dec(l[0])


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {day_one(testinput)}")
    print(f"Realinput value is {day_one(realinput)}")

    print("B:")
    print(f"Testinput value is {o2(testinput) * co2(testinput)}")
    print(f"Realinput value is {o2(realinput) * co2(realinput)}")
