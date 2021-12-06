from typing import List

testinput = [int(s) for s in "3,4,3,1,2".split(",")]
realinput = [int(s) for s in [l for l in open("Day6/Day6Input.txt")][0].split(",")]


def breed(counts):
    for i in range(len(counts)):
        if i == 0:
            breeders: int = counts[0]
        else:
            counts[i - 1] = counts[i]
    counts[6] += breeders
    counts[8] = breeders


def generations(gens: int, inp) -> int:
    counts: List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in inp:
        counts[i] += 1

    for i in range(gens):
        breed(counts)

    return sum(counts)


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {generations(80,testinput)}")
    print(f"Testinput value is {generations(80,realinput)}")

    print("B:")
    print(f"Testinput value is {generations(256,testinput)}")
    print(f"Testinput value is {generations(256,realinput)}")
