testinput = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
realinput = [int(l) for l in open("Day1Input.txt")]


def number_increasing(l):
    return len([i for i in [a < b for a, b in zip(l, l[1:])] if i == True])


def in_threes(l):
    return [sum(x) for x in zip(l, l[1:], l[2:])]


if __name__ == "__main__":
    print("A:")
    print(f"Test input gives {number_increasing(testinput)} increasing")
    print(f"Real input gives {number_increasing(realinput)} increasing")

    print("B:")
    print(f"Test input gives {number_increasing(in_threes(testinput))} increasing")
    print(f"Real input gives {number_increasing(in_threes(realinput))} increasing")
