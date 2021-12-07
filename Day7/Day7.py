from typing import List
from statistics import mean, median

testinput = [int(s) for s in "16,1,2,0,4,2,7,1,2,14".split(",")]
realinput = [int(s) for s in [l for l in open("Day7/Day7Input.txt")][0].split(",")]


def day_one(inp: List[int]) -> int:
    return sum(list(abs(i - int(median(inp))) for i in inp))


def cost(i: int) -> int:
    return sum(range(1, i + 1))


def day_two(inp: List[int]) -> int:
    med = int(mean(inp))
    return min(
        sum(list(cost(abs(i - med)) for i in inp)),
        sum(list(cost(abs(i - (med + 1))) for i in inp)),
    )


if __name__ == "__main__":
    print("A:")
    print(f"Testinput value is {day_one(testinput)}")
    print(f"Realinput value is {day_one(realinput)}")

    print("B:")
    print(f"Testinput value is {day_two(testinput)}")
    print(f"Testinput value is {day_two(realinput)}")
