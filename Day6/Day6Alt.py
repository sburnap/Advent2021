from typing import List
from collections import Counter

testinput: Counter = Counter(int(s) for s in "3,4,3,1,2".split(","))
realinput: Counter = Counter(
    int(s) for s in [l for l in open("Day6/Day6Input.txt")][0].split(",")
)


def breed(counts: List[int]) -> List[int]:
    #      |  0 .. 5   |            6            |      7      |      8
    return counts[1:7] + [counts[7] + counts[0]] + [counts[8]] + [counts[0]]


def generations(gens: int, inp) -> int:

    counts: List[int] = [inp[i] for i in range(9)]

    for i in range(gens):
        counts = breed(counts)

    return sum(counts)


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {generations(80,testinput)}")
    print(f"Testinput value is {generations(80,realinput)}")

    print("B:")
    print(f"Testinput value is {generations(256,testinput)}")
    print(f"Testinput value is {generations(256,realinput)}")
